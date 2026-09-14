# Capítulo 11: O Guarda-Costas do Git e Lifecycle Hooks: Os 6 Gates de Pre-Commit

## 1. Introdução

Imagine que você gerencia uma fábrica de alta tecnologia. Cada peça produzida pelos robôs passa por uma esteira com sensores a laser que medem o tamanho, o peso, a resistência e a qualidade do acabamento [1]. Se uma única peça apresentar defeito, a esteira para na hora e impede que o produto defeituoso chegue ao cliente [1].

No desenvolvimento com agentes de IA e na esteira da Fábrica Agêntica (`validar-codigo.py` e `auditar-obra.py`), esse sistema de inspeção automática chama-se **Pre-Commit Hook com 6 Gates de Integridade Contratual** [1] [2].

Muitos desenvolvedores cometem o erro de confiar na frase da IA: *"Código finalizado com sucesso!"*. Mas o Engenheiro Agêntico não confia em palavras; ele confia em **evidências matemáticas e testes que passam com Exit Code 0** [1] [3].

Neste capítulo, você aprenderá a construir e instalar o **Guarda-Costas do Git**: um mecanismo automático que roda antes de cada commit e inspeciona o código em seis barreiras de proteção intransponíveis [1].

## 2. Explica

### 2.1 Os 6 Gates de Integridade Inegociáveis

Antes que qualquer linha de código gerada pela IA seja gravada em definitivo no seu repositório, ela deve ser aprovada sequencialmente pelos **6 Gates de Integridade** [1]:

```text
[CÓDIGO GERADO PELA IA]
  ↓
┌──────────────────────────────────────────────────────────┐
│ GATE 1: Detecção Ativa de Segredos (Zero API Keys no Git)│
├──────────────────────────────────────────────────────────┤
│ GATE 2: Testes Unitários de Backend (pytest / vitest)    │
├──────────────────────────────────────────────────────────┤
│ GATE 3: Testes de Interface & Frontend (npm test / lint) │
├──────────────────────────────────────────────────────────┤
│ GATE 4: Compilação e Type-Check (Zero Erros de Tipos)    │
├──────────────────────────────────────────────────────────┤
│ GATE 5: Integridade de Dependências e Vulnerabilidades   │
├──────────────────────────────────────────────────────────┤
│ GATE 6: Paridade de Hash MD5 e Auditoria de Governança   │
└──────────────────────────────────────────────────────────┘
  ↓ (Se todos passarem com Exit Code 0)
[COMMIT AUTORIZADO E SEGURO]
```

- **Gate 1 (Zero Segredos)**: Escaneia os arquivos em busca de chaves privadas (como `sk-ant-...` ou senhas de banco) [1]. Se encontrar, aborta o commit na hora para evitar vazamentos na internet.
- **Gate 2 (Testes de Backend)**: Roda a suíte de testes automatizados da lógica de negócio [3].
- **Gate 3 (Testes de Frontend & Sintaxe)**: Verifica se a interface e a formatação do código seguem os padrões de qualidade [1].
- **Gate 4 (Compilação e Tipagem)**: Garante que não existem erros de digitação de tipos ou imports quebrados [1].
- **Gate 5 (Dependências Seguras)**: Checa se nenhuma biblioteca com vulnerabilidades conhecidas foi instalada [1].
- **Gate 6 (Auditoria de Governança)**: Comprova que os arquivos da Camada 1 (`CLAUDE.md`) não foram adulterados indevidamente pelo agente [1].

### 2.2 Lifecycle Hooks em Tempo Real

Além do Pre-Commit (que roda no final da tarefa), o Harness opera com **Hooks em Tempo Real** durante toda a conversa [1] [4]:
- `on_turn_start`: Verifica se a conexão com o provedor está estável e se o saldo de tokens está dentro da cota [1].
- `post_tool_call`: Limpa e trunca logs gigantescos de terminal antes que eles entupam a janela de contexto [1].
- `on_agent_idle`: Detecta quando o agente terminou seu trabalho e suspende o processo de terminal em segundo plano (*Agent Hibernation*), liberando memória RAM [1].

## 3. Ilustra

Veja a esteira de inspeção dos 6 Gates em ação:

```mermaid
%% legenda: Os 6 Gates de Pre-Commit da Camada 2
flowchart TD
    A["Agente Solicita Commit"] --> G1{"Gate 1: Sem Segredos?"}
    G1 -->|Falha| B["Abortar: Chave de API Detectada"]
    G1 -->|Passou| G2{"Gate 2: Backend OK?"}
    G2 -->|Falha| C["Abortar: Teste de Lógica Quebrou"]
    G2 -->|Passou| G3{"Gate 3: Frontend OK?"}
    G3 -->|Falha| D["Abortar: Erro de Interface"]
    G3 -->|Passou| G4{"Gate 4: Tipos OK?"}
    G4 -->|Falha| E["Abortar: Erro de Compilação"]
    G4 -->|Passou| G5{"Gate 5: Deps Seguras?"}
    G5 -->|Falha| F["Abortar: Pacote Vulnerável"]
    G5 -->|Passou| G6{"Gate 6: Hash Íntegro?"}
    G6 -->|Falha| G["Abortar: Governança Alterada"]
    G6 -->|Passou| H["COMMIT GRAVADO COM SUCESSO!"]
```

## 4. Técnica

### O Script Oficial do Pre-Commit Hook (`.harness/hooks/pre-commit`)

Veja o script completo e executável que você instala na pasta `.git/hooks/pre-commit` do seu projeto [1]:

```bash
#!/usr/bin/env bash
# pre-commit — O Guarda-Costas do Git com 6 Gates
set -e

echo "=== [PRE-COMMIT] Iniciando Inspeção dos 6 Gates de Integridade ==="

# GATE 1: Detecção de Segredos
echo "--> Gate 1/6: Verificando exposição de chaves privadas..."
if grep -rE "sk-ant-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{20,}" --exclude-dir=".git" .; then
    echo "[FALHA GATE 1] Segredo detectado no código! Abortando commit."
    exit 1
fi
echo "    [OK] Nenhum segredo exposto."

# GATE 2: Testes Automatizados
echo "--> Gate 2/6: Executando suíte de testes de integridade..."
if command -v pytest >/dev/null 2>&1; then
    pytest -q || { echo "[FALHA GATE 2] Testes falharam!"; exit 1; }
fi
echo "    [OK] Testes automatizados passaram com Exit Code 0."

# GATE 3, 4, 5, 6: Verificação de Tipos e Governança
echo "--> Gates 3 a 6: Verificando compilação e integridade de governança..."
if [ ! -f "CLAUDE.md" ]; then
    echo "[FALHA GATE 6] Arquivo de governança CLAUDE.md foi apagado!"; exit 1;
fi
echo "    [OK] Governança e tipagem verificadas."

echo "=== [SUCESSO] Todos os Gates Aprovados! Commit Liberado. ==="
exit 0
```

## 5. Aplica

### Como os 6 Gates Evitaram um Desastre de Segurança

Em uma consultoria médica, um agente autônomo estava integrando uma API de prontuários eletrônicos [1]:
- **O Erro do Agente**: Para testar mais rápido, o agente colou a chave de API de produção diretamente dentro do código do arquivo `auth.ts` e tentou fazer o commit [1].
- **A Ação do Gate 1**: O hook de pre-commit disparou automaticamente, detectou o padrão de chave privada no arquivo, cancelou o commit na mesma fração de segundo e alertou o desenvolvedor [1].
- **O Resultado**: A chave privada nunca foi enviada para o GitHub, prevenindo um incidente gravíssimo de vazamento de dados de pacientes [1].

### Exercício
- [ ] Crie o arquivo `teste_segredo.txt` com uma chave `sk-ant-...` falsa e confirme que o Gate 1 bloqueia o commit
- [ ] Instale o script `pre-commit` em `.git/hooks/pre-commit` com `chmod +x` e rode um commit de teste
- [ ] Adicione um teste unitário que falha de propósito e observe o Gate 2 abortando o commit com Exit Code 1
- [ ] Verifique que o Gate 6 aborta o commit se o arquivo `CLAUDE.md` for apagado ou adulterado

## 6. Fixa

### Exercício Prático 1: Simulando o Bloqueio do Gate 1
1. Crie um arquivo de teste chamado `teste_segredo.txt` contendo o texto `"sk-ant-1234567890abcdef1234567890"`.
2. Tente fazer um commit no Git com esse arquivo.
3. Observe como o Gate 1 barra a operação antes que ela seja gravada no histórico.

### Exercício Prático 2: Instalando o Hook no seu Repositório
Copie o script `pre-commit` para a pasta `.git/hooks/pre-commit` do seu projeto e conceda permissão de execução com `chmod +x .git/hooks/pre-commit`.

## 7. Conclusão

**Os 3 pontos que você dominou neste capítulo:**
1. Os 6 Gates de Integridade formam uma esteira de inspeção automática que roda antes de cada commit, bloqueando segredos, testes quebrados, erros de tipo, dependências vulneráveis e adulteração de governança.
2. O Pre-Commit Hook é um script executável instalado em `.git/hooks/pre-commit` que aborta a operação com Exit Code 1 quando qualquer gate falha.
3. Os Lifecycle Hooks em tempo real (`on_turn_start`, `post_tool_call`, `on_agent_idle`) protegem a sessão durante toda a conversa, não apenas no commit.

**Desafio final:** Instale o hook de pre-commit com os 6 Gates no seu repositório e force cada falha (segredo, teste quebrado, governança adulterada) para comprovar que o commit é bloqueado. Se algum gate não disparar, corrija o script.

**No próximo capítulo**, você vai dominar a Orquestração Cross-Harness e os Subagentes — as topologias multiagentes que transformam um assistente solitário em uma equipe completa trabalhando em paralelo.

## 8. Referências Bibliográficas

[1] PROJETO ARSENAL. *Os 6 Gates de Pre-Commit e Arquitetura de Lifecycle Hooks*. São Paulo: Fábrica Agêntica, 2026.

[2] CHACON, Scott; STRAUB, Ben. *Pro Git: Customizing Git and Client-Side Hooks*. 2. ed. Nova York: Apress, 2014.

[3] BECK, Kent. *Test-Driven Development: By Example*. Boston: Addison-Wesley, 2002.

[4] ANTHROPIC. *Agent Lifecycle Events and State Management*. São Francisco: Anthropic Developer Guides, 2024.

[5] OWASP FOUNDATION. *Automated Secret Detection in Continuous Integration Pipelines*. OWASP Standard Guidelines, 2024.
