# Capítulo 13: Fine-Tuning Local: Personalizando o Modelo

## 1. Introdução

No Capítulo 12, você construiu um pipeline RAG para dar memória de longo prazo ao agente. Mas e se o próprio modelo pudesse ser treinado para entender melhor seu domínio específico? O fine-tuning é essa personalização — ajustar os pesos de um modelo genérico para que ele seja um especialista no seu nicho [1].

O fine-tuning não é mágica — é uma técnica poderosa que, quando bem aplicada, pode transformar um bom modelo em um excelente modelo para seu caso de uso específico. Mas quando mal aplicada, pode piorar a performance geral do modelo [2].

Neste capítulo, você vai realizar fine-tuning de um modelo DeepSeek com LoRA e QLoRA usando Axolotl ou Unsloth, preparar datasets, avaliar resultados, e exportar o modelo treinado para GGUF.

## 2. Explica

### LoRA vs QLoRA

**LoRA (Low-Rank Adaptation)** é uma técnica que adapta apenas uma fração dos parâmetros do modelo, preservando os pesos originais. Em vez de ajustar bilhões de parâmetros, LoRA ajusta matrizes de baixa dimensão — reduzindo o custo de treinamento em 90%+ [3].

**QLoRA** combina LoRA com quantização 4-bit. O modelo base fica em 4 bits (reduzindo VRAM drasticamente), e os adaptadores LoRA ficam em FP16. Resultado: fine-tuning de um modelo 7B com apenas ~5GB de VRAM [4].

| Método | VRAM Necessária (7B) | Qualidade | Velocidade |
|--------|---------------------|-----------|------------|
| Full fine-tune | ~56GB | Máxima | Lenta |
| LoRA (FP16) | ~28GB | Alta | Média |
| QLoRA (4-bit) | ~5GB | Boa | Rápida |

### Como o QLoRA Comprime sem Destruir a Qualidade

O truque central do QLoRA não é só "quantizar em 4 bits" — é a combinação de três técnicas [4][23]:

1. **NF4 (4-bit NormalFloat):** um tipo de dado quantizado desenhado especificamente para pesos com distribuição normal (como os de uma rede neural treinada), que representa a informação com menos erro do que um INT4 genérico de propósito geral.
2. **Double Quantization:** quantiza também as constantes de quantização (os fatores de escala usados para converter de volta para FP16), economizando ~0,4 bit por parâmetro adicional — pouco por parâmetro isolado, mas relevante multiplicado por bilhões de parâmetros.
3. **Paged Optimizers:** usa memória paginada da GPU (unified memory da NVIDIA) para absorver picos de uso de VRAM durante o backward pass, evitando erros de out-of-memory em sequências longas ou batches maiores.

O paper original do QLoRA [23] demonstra o resultado prático dessa combinação: um modelo de 65B parâmetros treinado em uma única GPU de 48GB, preservando 99,3% da performance de um fine-tuning completo em 16-bit. O ajuste em 4-bit não é apenas "mais barato" — ele chega perto da qualidade do treino em precisão total.

### Variantes Recentes de LoRA

O LoRA clássico ganhou variantes que vale conhecer antes de escolher a receita de treino [21][22][24][25]:

| Variante | Ideia central | Quando considerar |
|----------|---------------|-------------------|
| LoRA | Duas matrizes de baixo rank (A, B) somadas aos pesos originais | Padrão — comece por aqui |
| QLoRA | LoRA + modelo base em NF4 | VRAM limitada (menos de 24GB) |
| DoRA | Decompõe o peso em magnitude + direção, aplica LoRA só na direção [21] | Quando um LoRA "raso" (r baixo) perde qualidade |
| LoRAPrune | Combina LoRA com pruning estrutural, remove neurônios pouco usados durante o próprio treino [22] | Quando o objetivo final é um modelo menor, não só especializado |
| La-LoRA | Rank adaptativo por camada — camadas mais "importantes" recebem rank maior [25] | Datasets heterogêneos com muitas tarefas distintas |

Unsloth e Axolotl implementam LoRA e QLoRA nativamente; DoRA e variantes mais recentes normalmente exigem habilitar uma flag específica (`use_dora: true` no Axolotl) ou usar o LlamaFactory [24], que unifica mais de 100 arquiteturas de modelo e as principais técnicas de PEFT (parameter-efficient fine-tuning) em uma única interface de configuração YAML.

### Como Escolher o Rank (r) na Prática

A literatura de PEFT que se seguiu ao LoRA original converge em uma observação prática: aumentar o rank (r) tem retornos decrescentes rápidos [26]. Para a maioria das tarefas de fine-tuning de instrução, r entre 8 e 32 captura quase todo o ganho possível; ir de r=16 para r=64 raramente melhora a qualidade final de forma perceptível, mas quadruplica o número de parâmetros treináveis e o tempo de treino. O que importa mais do que o valor do rank é *quais* módulos recebem os adaptadores: aplicar LoRA só em `q_proj`/`v_proj` (atenção) é mais barato, mas para tarefas que exigem mudança de conhecimento factual (não só de estilo de escrita), incluir as camadas MLP (`gate_proj`, `up_proj`, `down_proj`) tende a ajudar mais do que simplesmente subir o rank [26].

### Preparação de Dados

O dataset de fine-tuning segue formatos padrão [3]:

**Alpaca Format:**
```json
{"instruction": "Explique o que é Docker", "input": "", "output": "Docker é uma plataforma de containerização..."}
```

**ShareGPT Format:**
```json
{"conversations": [{"from": "human", "value": "Como instalar Ollama?"}, {"from": "gpt", "value": "Para instalar o Ollama..."}]}
```

### Proporção de Dados: Especializar sem Apagar

O erro mais comum de quem começa em fine-tuning é montar um dataset 100% focado no domínio-alvo. A recomendação usual em fine-tuning eficiente por parâmetros é misturar 10% a 20% de exemplos genéricos (instruções gerais, outros idiomas, outros formatos de tarefa) junto aos exemplos de domínio [21][6][8]. Essa fração de "reforço geral" ocupa pouco espaço no dataset, mas ancora o modelo nas capacidades que ele já tinha antes do fine-tuning — é a diferença entre especializar e substituir o conhecimento do modelo base.

### Pipeline Completo

1. **Preparar dados** → formato JSON/JSONL
2. **Configurar treino** → Axolotl ou Unsloth
3. **Treinar** → fine-tuning com QLoRA
4. **Avaliar** → métricas de perplexidade e testes qualitativos
5. **Exportar** → converter para GGUF
6. **Integrar** → carregar no Ollama

## 3. Ilustra

### Calibrando o Motor

Na sua oficina de agentes, o fine-tuning é como calibrar um motor para um combustível específico. O motor genérico (modelo base) funciona com qualquer gasolina, mas quando você calibra ele para o gasolina do seu posto (seu domínio específico), ele roda mais eficiente, mais suave, e gasta menos combustível [5].

O LoRA é como trocar apenas as velas e o filtro de ar — não precisa desmontar o motor inteiro. Você ajusta as peças que fazem a diferença (os adaptadores de baixa dimensão) e deixa o resto do motor original intacto. É mais barato, mais rápido, e mais seguro que um rebuild completo.

O QLoRA vai além: é como usar gasolina de octanagem menor no tanque (quantização 4-bit) enquanto mantém as peças novas em alta qualidade (adaptadores FP16). O motor roda um pouco mais quente, mas consome muito menos combustível (VRAM).

```mermaid
%% legenda: Pipeline de fine-tuning local — dados → treino → exportação → deploy
flowchart LR
    A[Preparar Dataset] --> B[Configurar Axolotl/Unsloth]
    B --> C[QLoRA Training]
    C --> D[Evaluar Métricas]
    D -->|Insuficiente| B
    D -->|Suficiente| E[Exportar GGUF]
    E --> F[Carregar no Ollama]
    F --> G[Testar no Harness]
    
    style C fill:#7C3AED,color:#fff
    style G fill:#10B981,color:#fff
```

## 4. Técnica

### Setup com Unsloth

```bash
# Instalar Unsloth
pip install unsloth

# Script de fine-tuning
python << 'EOF'
from unsloth import FastLanguageModel
import torch

# Carregar modelo base com QLoRA
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/DeepSeek-V4-7B",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Adicionar adaptadores LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
)

# Treinar
from trl import SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        output_dir="outputs",
    ),
)
trainer.train()

# Salvar adaptador
model.save_pretrained("deepseek-finetuned")
EOF
```

### Configuração Alternativa com Axolotl

Para quem prefere um arquivo de configuração declarativo em vez de um script Python, o Axolotl é a alternativa mais usada em pipelines de produção [3][24]:

```yaml
# axolotl-config.yaml
base_model: deepseek-ai/DeepSeek-V4-7B
load_in_4bit: true
adapter: qlora

lora_r: 16
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj

datasets:
  - path: ./dataset_alpaca.jsonl
    type: alpaca

sequence_len: 2048
sample_packing: true
num_epochs: 3
micro_batch_size: 2
gradient_accumulation_steps: 4
learning_rate: 0.0002
```

```bash
accelerate launch -m axolotl.cli.train axolotl-config.yaml
```

### Fundindo o Adaptador ao Modelo Base

Antes de converter para GGUF, você tem duas opções: manter o adaptador LoRA separado (carregado em tempo de execução por cima do modelo base) ou fundir os pesos em um único checkpoint [6][9]:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-V4-7B")
modelo = PeftModel.from_pretrained(base, "deepseek-finetuned")

# Funde os pesos LoRA no modelo base — resultado é um único checkpoint
modelo_fundido = modelo.merge_and_unload()
modelo_fundido.save_pretrained("deepseek-finetuned-merged")
```

Fundir é obrigatório antes de converter para GGUF (o formato não entende adaptadores LoRA separados), mas tem um custo: você perde a flexibilidade de trocar de adaptador sem re-exportar o modelo inteiro. Se você mantém vários adaptadores para domínios diferentes (um para código, outro para atendimento ao cliente), versione os `.safetensors` do adaptador separadamente antes da fusão, para poder refazer o merge com outra base sem re-treinar.

### Avaliando Antes de Exportar

Antes de converter para GGUF, meça se o fine-tuning realmente melhorou o modelo — comparar perplexidade antes/depois é o mínimo [9]:

```python
import torch

def perplexidade(modelo, tokenizer, textos):
    modelo.eval()
    losses = []
    for texto in textos:
        ids = tokenizer(texto, return_tensors="pt").input_ids
        with torch.no_grad():
            saida = modelo(ids, labels=ids)
        losses.append(saida.loss.item())
    media = sum(losses) / len(losses)
    return torch.exp(torch.tensor(media)).item()

# Comparar modelo base vs modelo fine-tuned no mesmo conjunto de teste
ppl_base = perplexidade(modelo_base, tokenizer, textos_teste)
ppl_finetuned = perplexidade(modelo_finetuned, tokenizer, textos_teste)
print(f"Perplexidade base: {ppl_base:.2f} | fine-tuned: {ppl_finetuned:.2f}")
```

Uma perplexidade menor no domínio-alvo é bom sinal. Se a perplexidade em textos gerais (fora do domínio) subir de forma acentuada em relação ao modelo base, é indício de catastrophic forgetting [26] — volte ao dataset e aumente a proporção de exemplos genéricos antes de exportar.

### Exportando para GGUF

```bash
# Converter adaptador para GGUF
python scripts/convert_lora_to_gguf.py \
  --base-model deepseek-ai/DeepSeek-V4-7B \
  --lora-model ./deepseek-finetuned \
  --output deepseek-finetuned-Q4_K_M.gguf

# Carregar no Ollama
ollama create deepseek-custom -f Modelfile
```

```dockerfile
# Modelfile
FROM ./deepseek-finetuned-Q4_K_M.gguf
PARAMETER temperature 0.7
SYSTEM "Você é um assistente especializado em [seu domínio]"
```

### Escolhendo o Nível de Quantização do GGUF

`Q4_K_M` no comando acima não é a única opção — e a escolha afeta diretamente a qualidade do modelo fine-tuned exportado [27][28]:

| Quantização | Bits efetivos | Qualidade retida (aprox.) | Tamanho (7B) |
|-------------|---------------|---------------------------|--------------|
| Q8_0 | 8 | ~99% | ~7,5 GB |
| Q5_K_M | 5 | ~97% | ~4,8 GB |
| Q4_K_M | 4 | ~92% | ~4,1 GB |
| Q3_K_M | 3 | ~85% | ~3,3 GB |

Modelos fine-tuned tendem a ser mais sensíveis à quantização agressiva do que o modelo base, porque os adaptadores LoRA concentram informação em poucas direções do espaço de pesos — comprimir demais essas direções apaga justamente o que o fine-tuning ensinou [27]. Para um modelo especializado que você pretende usar em produção, `Q5_K_M` costuma ser o ponto de equilíbrio; reserve `Q4_K_M` para hardware muito limitado, e valide a perplexidade (seção anterior) antes de aceitar a perda de qualidade.

### Hot-Swapping de Adaptadores em Produção

A exportação para GGUF fundindo o adaptador ao modelo base (seção anterior) é a rota mais simples, mas não é a única — e não é a melhor quando você mantém mais de um adaptador especializado para o mesmo modelo base (um para o domínio de suporte ao cliente, outro para geração de código interno, por exemplo). Fundir cada adaptador gera uma cópia completa do modelo por especialização — desperdício de armazenamento e de VRAM se você precisa trocar de especialização com frequência.

A alternativa é manter o modelo base carregado uma única vez em memória e trocar apenas o adaptador LoRA (que pesa uma fração do modelo completo) conforme a requisição chega — o padrão chamado de hot-swapping ou multi-adapter serving. Engines de inferência voltados a produção (vLLM é o exemplo já mencionado neste livro) suportam servir múltiplos adaptadores LoRA simultaneamente sobre o mesmo modelo base carregado, roteando cada requisição para o adaptador certo por parâmetro da chamada, sem precisar recarregar nada entre uma requisição e outra.

O trade-off é operacional, não técnico: hot-swapping exige uma camada de roteamento entre requisição e adaptador — alguma coisa precisa decidir, para cada chamada, qual especialização usar — que a rota de "exportar um GGUF fundido por especialização" simplesmente não precisa ter, porque cada modelo fundido já é uma unidade de deploy independente. Para duas ou três especializações usadas raramente, fundir e trocar manualmente ainda é mais simples de operar; para dezenas de especializações trocadas a cada requisição, hot-swapping é a única opção que escala sem multiplicar o consumo de VRAM por especialização ativa.

## 5. Aplica

### O Fine-Tuning que Piorou o Modelo

Um desenvolvedor treinou um modelo com 100 exemplos de código Python. O resultado: o modelo ficou excelente para Python, mas esqueceu como escrever JavaScript, SQL, e até respostas em português. O fine-tuning causou catastrophic forgetting [1].

A causa: dataset pequeno e sem diversidade. O modelo "esqueceu" conceitos gerais porque só viu um tipo de dado durante o treino.

### A Prática Correta

Regras para fine-tuning de qualidade:

| Parâmetro | Recomendação |
|-----------|-------------|
| Tamanho do dataset | 500-5000 exemplos |
| Épocas | 2-5 (evitar overfitting) |
| Learning rate | 1e-4 a 3e-4 |
| LoRA rank (r) | 8-32 |
| Batch size | 2-8 (depende da VRAM) |

Sempre inclua exemplos diversificados no dataset para evitar catastrophic forgetting.

### Até Onde o Fine-Tuning Local Escala

Fine-tuning local com LoRA/QLoRA tem um limite claro de escala: acima de ~70B parâmetros, mesmo em 4-bit, o ajuste exige múltiplas GPUs de 24GB+ trabalhando em paralelo (sharding do adaptador ou do próprio modelo base), e deixa de ser "fine-tuning local" no sentido de uma única máquina de desenvolvedor [4][11]. Abaixo de 500 exemplos de qualidade, o dataset é pequeno demais e o modelo satura em overfitting rápido — nesse volume, prefira few-shot prompting em vez de treinar. E quando o conhecimento a incorporar é volátil (preços, notícias, dados que mudam todo dia), fine-tuning não é a ferramenta certa: cada atualização exigiria retraining, o que não escala; RAG (Capítulo 12) resolve esse caso melhor porque atualiza o conhecimento sem tocar nos pesos do modelo [6].

## 6. Conclusão

Neste capítulo, você aprendeu a personalizar modelos DeepSeek com LoRA/QLoRA — ajustando os pesos para seu domínio específico sem precisar de hardware massivo. O pipeline completo (dados → treino → avaliação → exportação GGUF → Ollama) permite criar modelos customizados que se integram perfeitamente ao DeepSeek Harness.

No próximo capítulo, você vai coordenar múltiplos agentes trabalhando em paralelo — a equipe de agentes da sua oficina.

## 7. Referências Bibliográficas

[1] CODERFILE. *Fine-Tuning Local LLMs for Code Generation*. Disponível em: https://coderfile.io/blog/local-llm-fine-tuning-code-2026. Acesso em: 23 ago. 2026.

[2] FUTURE AGI. *Fine-Tuning LLMs 2026: LoRA, QLoRA, DPO, GRPO*. Disponível em: https://futureagi.com/blog/fine-tuning-llms-unlocking-peak-performance/. Acesso em: 23 ago. 2026.

[3] CODERSERA. *Fine-Tuning LLMs in 2026*. Disponível em: https://codersera.com/blog/fine-tuning-llms-complete-guide-2026/. Acesso em: 23 ago. 2026.

[4] EFFLOOW. *Fine-Tune LLMs with LoRA and QLoRA*. Disponível em: https://effloow.com/articles/llm-fine-tuning-lora-qlora-guide-2026. Acesso em: 23 ago. 2026.

[5] AIRBYTE. *How to Train an LLM on Your Own Data*. Disponível em: https://airbyte.com/data-engineering-resources/how-to-train-llm-with-your-own-data. Acesso em: 23 ago. 2026.

[6] ZYLOS.AI. *Open-Source LLM Fine-Tuning and Serving Infrastructure*. Disponível em: https://zylos.ai/research/2026-03-22-open-source-llm-fine-tuning-serving-ai-agent-platforms/. Acesso em: 23 ago. 2026.

[7] BRAINTRUST. *Best LLM fine-tuning platforms in 2026*. Disponível em: https://www.braintrust.dev/articles/best-llm-fine-tuning-platforms-2026. Acesso em: 23 ago. 2026.

[8] REDDIT (r/learnmachinelearning). *Practical Lessons from Running Local LLMs for Fine-Tuning*. Disponível em: https://www.reddit.com/r/learnmachinelearning/comments/1sibi3j/. Acesso em: 23 ago. 2026.

[9] LLMS3.COM. *Fine-Tuning an LLM on Your Own Data, Locally*. Disponível em: https://llms3.com/blog/fine-tune-llm-on-your-own-data-locally-2026. Acesso em: 23 ago. 2026.

[10] TECH-INSIDER. *How to Fine-Tune an LLM: 13 Steps, 90 Min*. Disponível em: https://tech-insider.org/how-to-fine-tune-an-llm-2026/. Acesso em: 23 ago. 2026.

[11] DEEPSEEK AI. *DeepSeek Harness developer preview*. Disponível em: https://deepseek.com/harness/en/. Acesso em: 23 ago. 2026.

[12] HABR. *Inside DeepSeek Harness*. Disponível em: https://habr.com/en/articles/1070958/. Acesso em: 23 ago. 2026.

[13] FLOATBOAT.AI. *Cordis — The Plugin Kernel*. Disponível em: https://floatboat.ai/blog/cordis-plugin-framework. Acesso em: 23 ago. 2026.

[14] AGENTATLAS. *Cordis Explained*. Disponível em: https://agentatlas.org/blog/cordis-explained-how-deepseek-harness-plugin-framework-works/. Acesso em: 23 ago. 2026.

[15] MEDIUM (data-and-beyond). *Decoding DeepSeek Harness*. Disponível em: https://medium.com/data-and-beyond/decoding-deepseek-harness-the-open-source-runtime-behind-composable-ai-agents-c2299e992870. Acesso em: 23 ago. 2026.

[16] TOWARDS AI. *DeepSeek Harness vs Claude Code*. Disponível em: https://pub.towardsai.net/deepseek-harness-vs-claude-code-a-plugin-architecture-teardown-da3c916f3af1. Acesso em: 23 ago. 2026.

[17] YOUTUBE. *Every Deepseek Harness Concept Explained*. Disponível em: https://www.youtube.com/watch?v=24UCnAs7MVg. Acesso em: 23 ago. 2026.

[18] YOUTUBE. *NEW Deepseek Agent Harness EXPLAINED*. Disponível em: https://www.youtube.com/watch?v=Hpw4fAHlHDw. Acesso em: 23 ago. 2026.

[19] EXPLOREX.AI. *DeepSeek Harness v0.1*. Disponível em: https://explainx.ai/blog/deepseek-harness-v0-1-plugin-first-agent-stack-august-2026. Acesso em: 23 ago. 2026.

[20] DEEPSEEKHARNESSAI. *Security Plugins for DeepSeek Harness*. Disponível em: https://deepseekharnessai.com/categories/security. Acesso em: 23 ago. 2026.

[21] LIU, Shih-Yang et al. *DoRA: Weight-Decomposed Low-Rank Adaptation*. In: arXiv (Cornell University). 2024. Disponível em: http://arxiv.org/abs/2402.09353. Acesso em: 23 ago. 2026.

[22] ZHANG, Mingyang et al. *LoRAPrune: Structured Pruning Meets Low-Rank Parameter-Efficient Fine-Tuning*. 2024. Disponível em: https://doi.org/10.18653/v1/2024.findings-acl.178. Acesso em: 23 ago. 2026.

[23] DETTMERS, Tim et al. *QLoRA: Efficient Finetuning of Quantized LLMs*. In: arXiv (Cornell University). 2023. Disponível em: http://arxiv.org/abs/2305.14314. Acesso em: 23 ago. 2026.

[24] ZHENG, Yaowei et al. *LlamaFactory: Unified Efficient Fine-Tuning of 100+ Language Models*. 2024. Disponível em: https://doi.org/10.18653/v1/2024.acl-demos.38. Acesso em: 23 ago. 2026.

[25] GU, Jiancheng et al. *La-LoRA: Parameter-efficient fine-tuning with layer-wise adaptive low-rank adaptation*. In: Neural Networks. 2026. Disponível em: https://doi.org/10.1016/j.neunet.2025.108095. Acesso em: 23 ago. 2026.

[26] MAO, Yuren et al. *A survey on LoRA of large language models*. In: Frontiers of Computer Science. 2024. Disponível em: https://doi.org/10.1007/s11704-024-40663-9. Acesso em: 23 ago. 2026.

[27] ZENG, Chao et al. *GQSA: Group Quantization and Sparsity for Accelerating Large Language Model Inference*. In: arXiv (Cornell University). 2024. Disponível em: http://arxiv.org/abs/2412.17560. Acesso em: 23 ago. 2026.

[28] TRIPATHI, OM. *"GGUF Models and Quantization"*. 2025. Disponível em: https://doi.org/10.2139/ssrn.5044207. Acesso em: 23 ago. 2026.
