# Capítulo 8: O Perito Permanente: Seu Protocolo Para Qualquer Manual Novo

## 1. Introdução

No Capítulo 7, você fez a perícia mais densa do livro: mapeou, um a um, os comandos fabricados de skill, cron, memória e sessão que o manual v3.1 atribuía ao Hermes Agent, cruzando cada um com a CLI real documentada pelo próprio projeto [1]. Aquele capítulo fechou com uma regra simples, quase óbvia depois de dita: rode `--help` antes de automatizar uma ferramenta nova, nunca depois de o comando já ter falhado em produção. Esse é o último tijolo solto do caso. Chegou a hora de parar de tratar aquilo como uma regra isolada para o Hermes e transformá-la em protocolo permanente — algo que você carrega para o próximo manual, a próxima ferramenta, o próximo notebook.

Este capítulo fecha o livro em três movimentos. Primeiro, você consolida o checklist de perícia que já vem aplicando, capítulo após capítulo, num formato portátil que cabe em qualquer manual futuro — incluindo o que fazer quando a resposta é "não dá para confirmar". Segundo, você versiona o que já foi confirmado (o `CLAUDE.md`, as configurações de terminal, os segredos de API) para nunca mais refazer a perícia do zero numa máquina nova. Terceiro, e mais importante: você mede a distância entre quem abriu este livro no Capítulo 1 e quem o fecha agora.

## 2. Explica

Todo o método deste livro repousa sobre uma única ideia: nem toda fonte de informação tem o mesmo peso de prova. Ao longo dos sete capítulos anteriores, você aplicou, sem nomear formalmente, uma hierarquia de três classes de fonte. A **Classe A** é a documentação oficial publicada pelo próprio fornecedor da ferramenta — a página de configurações do Claude Code [2], a referência de hooks da Anthropic [3], a configuração oficial do Gemini CLI [4]. A **Classe B** é o repositório oficial do projeto, o pacote no PyPI ou no npm — o código-fonte do chezmoi [5], o pacote real do LLMLingua no GitHub da Microsoft [6], o repositório do próprio `ccusage` [7]. A **Classe C** é tudo o que vem de terceiros: blogs, agregadores, cobertura de imprensa especializada — útil para entender como as pessoas usam uma ferramenta na prática — foi assim que você leu, no Capítulo 2, uma cobertura de terceiro sobre economia de custo com cache de prompt [8] — mas nunca a prova final de que um comando existe. O mesmo vale para um FAQ de comunidade sobre o `ccusage`: ajuda a entender o contexto de uso, mas o veredito sobre sintaxe exata continua vindo da Classe A ou B, mesmo quando o texto é claro e bem escrito [9].

A lição mais cara deste livro é que o padrão de erro mais perigoso não nasce da Classe C sozinha. Nasce de um produto genuíno, confirmável na Classe A ou B, ao qual alguém anexa uma sintaxe que nunca existiu. O manual auditado citava o Hermes Agent (produto real, Classe B confirmada [1]) com uma sintaxe de comando (`hermes skill activate`, `hermes memory add --target`) que nunca foi documentada na referência de CLI do projeto [10], nem na referência de configuração que descreve os campos reais de memória e skills [11]. Citava o `chezmoi` (real, Classe A confirmada [5]) com um subcomando `commit` que o projeto nunca implementou. Em ambos os casos, o nome familiar do produto é o que baixa a guarda do operador — ninguém desconfia de um comando anexado a uma ferramenta que ele já usa há meses. É exatamente esse mecanismo psicológico, não a falta de familiaridade, que faz a fabricação parcial ser mais perigosa que a fabricação total.

Isso leva à regra mais contraintuitiva do checklist: **NÃO VERIFICÁVEL não é sinônimo de aprovado.** Ao longo do livro, você viu casos em que o produto é real e a documentação primária simplesmente não confirma (nem desmente) um detalhe específico — o caminho de configuração da Google Antigravity, por exemplo, não tem confirmação em nenhuma fonte primária consultada, mesmo o produto sendo genuíno [4]. A tentação natural é tratar "não achei nada contra" como "então deve estar certo". O protocolo correto é o oposto: um item Não Verificável fica retido, como evidência pendente, até que uma fonte primária — não uma dedução, não uma suposição plausível — confirme ou refute. Ele nunca migra automaticamente para "aprovado" só porque o tempo passou sem contestação.

A mesma hierarquia de evidência explica por que a técnica de cache de contexto que você usa desde o Capítulo 2 continua de pé até aqui, sem nenhuma correção. Manter o `CLAUDE.md` estático, com a mesma ordem de blocos em toda sessão, maximiza o acerto de cache pela razão mais literal possível: o mecanismo de cache da Anthropic funciona sobre um prefixo idêntico byte a byte no início da requisição — qualquer alteração no texto anterior a um ponto invalida o cache a partir dali [12]. Isso não é opinião de blog de terceiros: é a mecânica documentada oficialmente, e o desconto de leitura de cache chega a 90% do preço padrão de input quando o prefixo se mantém intacto [12]. Um script que calcula o hash SHA-256 do seu `CLAUDE.md` antes de cada sessão para detectar mudança silenciosa não depende de nenhuma ferramenta fabricada — é utilitário padrão de qualquer sistema Unix, e por isso sobrevive intacto à perícia.

Vale revisitar, em ritmo rápido, o painel de casos que já sustentou cada veredito deste livro — é o material bruto sobre o qual o checklist foi treinado. O Capítulo 2 confirmou que o Aider liga cache de prompt automático do provedor através de um campo real do seu arquivo de configuração, sem inventar granularidade que a ferramenta não expõe [13]. O Capítulo 6, na mesma linha, confirmou que o catálogo de modelos locais da Ollama é público e nomeado com precisão, o que tornou o fallback offline uma escolha auditável, não uma aposta [14].

A CLI real por trás desse fallback também resistiu à perícia sem nenhuma correção — o binário documentado é exatamente o que o manual usa [15]. O mesmo vale, num tema diferente, para o GPTCache: uma biblioteca genuína de cache semântico, ainda que o manual tenha anexado a ela comandos de terminal que o projeto nunca documentou [16].

O Capítulo 7 mostrou a versão mais concentrada desse padrão, ao separar dois produtos reais e completamente distintos que o manual tratava como se fossem o mesmo pacote: `agenttrace`, biblioteca de observabilidade em Python [17], e `agentlytics`, painel de análise em Node — dois ecossistemas diferentes, duas fontes primárias diferentes [18].

Mesmo os casos mais discretos reforçam a régua. O `llama.cpp` continua sendo o mesmo projeto real de sempre, só com o binário renomeado numa atualização do próprio mantenedor [19]; o vLLM tem uma CLI dedicada, documentada linha a linha na referência oficial do projeto [20].

O Codex CLI da OpenAI usa uma seção do arquivo de configuração diferente da que o manual descreveu, mas o arquivo em si e o restante da sintaxe batem com a documentação [21]. O OpenCode, por sua vez, grava as próprias preferências num arquivo com nome e campos documentados na referência do projeto [22].

Fechando o painel: o gateway de modelos gratuitos que o OpenCode expõe — o Zen — é real, mas exige conferência de nomenclatura a cada consulta ao catálogo vigente, porque a lista muda [23]. E, entre as sete outras ferramentas mapeadas no Capítulo 7, o `gemini-cli` do Google é o único caso da lista com repositório e configuração confirmados nas duas pontas por fonte primária [24].

Colocado lado a lado, esse painel de casos forma o que a auditoria completa do manual chama de núcleo genuíno e ensinável, ordenado pela solidez da fonte que o confirma: o prompt caching real da Anthropic, com seus multiplicadores de preço documentados oficialmente [12]; o paralelismo real via `asyncio`/`xargs`/GNU Parallel combinado com circuit breaker e backoff exponencial, o único capítulo do livro que não precisou de nenhuma correção; o Ollama com catálogo de modelos e fallback local auditável [14][15]; o `chezmoi` para versionamento de dotfiles, com apenas o instalador e o `commit` corrigidos [5]; o LLMLingua e o GPTCache como bibliotecas Python genuínas de compressão de prompt e cache semântico, usadas de forma errada no manual como se tivessem CLI própria [6][16]; o `ccusage` como ferramenta real de análise de uso via npm [7]; e o próprio Hermes Agent, com memória, skills, cron e delegação todos confirmados como mecanismo, mesmo com a sintaxe de comando fabricada [1][10][11]. Sete itens, sete fontes primárias diferentes, um padrão idêntico se repetindo em cada um: produto genuíno, detalhe de superfície errado. Esse mesmo padrão de sete casos é o que, mais adiante nesta conclusão, se traduz nos números fechados da perícia inteira.

## 3. Ilustra

Pense num perito de verdade — não o que investiga um caso específico, mas o que a corregedoria chama para treinar os novos. Ele não ensina "como resolver o caso do manual v3.1". Ele ensina um procedimento de bancada que serve para qualquer documento suspeito que chegar depois: primeiro, identifique de onde o documento diz que veio; segundo, classifique essa origem numa das três gavetas (letra timbrada oficial, cópia de cartório, boato de rua); terceiro, procure o sinal de alerta específico — a assinatura bonita demais, o carimbo no lugar errado; quarto, só então lavre o laudo. É esse procedimento — não o caso individual — que você carrega na maleta para a próxima perícia.

A parte mais traiçoeira do checklist merece uma segunda cena. Imagine que, depois de investigar um documento a fundo, o laboratório devolve um resultado "inconclusivo" — nem confirma, nem refuta a autenticidade. Um perito de verdade nunca arquiva um laudo inconclusivo na gaveta de "autenticado": ele fica na gaveta de "pendente", visível, esperando um novo exame, porque tratá-lo como aprovado por omissão é exatamente o erro que deixa passar uma falsificação. É esse mesmo instinto — pendência visível, nunca aprovação por padrão — que você aplica a qualquer item marcado NÃO VERIFICÁVEL neste livro ou em qualquer manual futuro.

```mermaid
%% legenda: Protocolo de pericia portatil aplicado a qualquer comando de manual novo
flowchart TD
  A[Documento chega ate voce: comando de um manual novo] --> B{Classificar a fonte}
  B -->|Classe A: doc oficial| C[Contraprova direta na fonte primaria]
  B -->|Classe B: repositorio ou pacote oficial| C
  B -->|Classe C: blog ou terceiro| D[Tratar como pista, nunca como prova]
  D --> C
  C --> E{Sinal de alerta? sintaxe exata confere?}
  E -->|confere| F[Laudo: Aprovado]
  E -->|nao confere| G[Laudo: Rejeitado - usar correcao real]
  E -->|sem fonte para confirmar| H[Laudo: Pendente - NAO igual a aprovado]
  H --> I[Reter ate nova fonte primaria surgir]
```

Como Perito de Configuração Agêntica, este é o momento em que você percebe que nunca mais vai precisar confiar cegamente num tutorial só porque o nome da ferramenta é conhecido.

## 4. Técnica

### O Protocolo de perícia em Formato Portátil

O checklist só é útil se puder ser aplicado sem este livro do lado. A forma mais simples de torná-lo portátil é um modelo de registro estruturado — um arquivo curto que você preenche a cada comando suspeito de um manual futuro, seja ele sobre IA, sobre banco de dados ou sobre infraestrutura de nuvem. O YAML abaixo é o mesmo esqueleto que sustentou, informalmente, cada linha da auditoria feita nos Capítulos 1 a 7: qual comando está sob suspeita, de que classe de fonte ele afirma vir, qual sinal de alerta apareceu e qual foi o veredito final.

```yaml
# protocolo-pericia.yaml
# Preencha um bloco destes por comando suspeito de um manual/tutorial novo.
comando_sob_suspeita: "chezmoi commit -m \"atualiza dotfiles\""
produto_citado: "chezmoi"
fonte_classificada:
  classe: "A"          # A = doc oficial | B = repo/pacote oficial | C = terceiro
  origem: "https://www.chezmoi.io/install/"
sinais_de_alerta:
  - "subcomando nao aparece na lista de comandos do --help oficial"
  - "nome do produto e real, o que reduz a desconfianca natural do operador"
contraprova_realizada: true
veredito: "rejeitado"   # aprovado | pendente | rejeitado
correcao_aplicada: "chezmoi cd && git commit -m \"atualiza dotfiles\""
observacao: "chezmoi nao tem subcomando commit nativo; commit acontece no repositorio git do diretorio-fonte"
```

Repare que o campo `veredito` tem três, não dois, valores possíveis — `pendente` existe como categoria de primeira classe, não como um `aprovado` disfarçado. Isso é o checklist forçando, na estrutura do próprio arquivo, a regra da seção Explica: sem fonte primária, o item não pode migrar para `aprovado` só por conveniência.

### Restaurando o Cofre Confirmado com chezmoi (Sintaxe Real)

O manual v3.1 acertou que um gerenciador de dotfiles é a ferramenta certa para não repetir a perícia do zero em cada notebook novo — e o `chezmoi` é, de fato, real e maduro para essa tarefa [5]. Onde ele errou foi em dois pontos específicos de sintaxe, e é exatamente aí que o checklist do Pilar 1 precisa ser aplicado antes de copiar qualquer coisa. O instalador `curl -sL https://git.io/chezmoi | sh` usa um encurtador de link (`git.io`) que o GitHub descontinuou para novos links desde 2022 — funciona por enquanto, mas depende de um redirecionamento legado sem garantia de permanência; o instalador oficial documentado hoje é outro [5]. E `chezmoi commit -m "..."` simplesmente não existe como subcomando nativo: o `chezmoi` gerencia o diretório-fonte dos seus dotfiles, mas o commit em si acontece pelo Git dentro desse diretório [5].

A sessão abaixo mostra a sequência real, do instalador correto ao commit correto, incluindo a verificação de hash SHA-256 do `CLAUDE.md` restaurado e a injeção de segredo via 1Password CLI — real e compatível com a sintaxe documentada da versão 2 [25].

```console
$ sh -c "$(curl -fsLS https://get.chezmoi.io)"
chezmoi: instalado em ~/.local/bin/chezmoi

$ chezmoi init
chezmoi: repositorio fonte inicializado em ~/.local/share/chezmoi

$ chezmoi add ~/.claude/CLAUDE.md
$ chezmoi add ~/.claude/settings.json

$ chezmoi status
A  .claude/CLAUDE.md
A  .claude/settings.json

$ sha256sum ~/.claude/CLAUDE.md
a3f2c9e7d1b04f6c8a2e9d5b7c1f0a4e6d8b2c4f  /home/voce/.claude/CLAUDE.md

$ chezmoi cd
$ git commit -am "cofre confirmado: CLAUDE.md e settings.json do Capitulo 8"
$ exit

$ chezmoi git commit -- -m "alternativa sem sair do diretorio fonte, mesmo efeito"

$ op signin
Digite sua senha mestra do 1Password: ****************
Sessao autenticada.

$ op item create --title "API Key" --vault Private --generate-password
Criado item "API Key" no cofre "Private".

$ op read "op://Private/API Key/credential"
sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Repare que `chezmoi status` entra na sequência exatamente entre o `add` e o `commit`: é o comando real que mostra, letra por caminho (`A` de adicionado, `M` de modificado), o que vai mudar no diretório-fonte antes de você confirmar qualquer coisa — a mesma disciplina de "nunca aplicar sem revisar antes" que perpassa este livro inteiro, aplicada agora ao seu próprio cofre de configuração [5]. E o `op item create` que precede a leitura do segredo fecha o ciclo completo do 1Password CLI: não basta saber *ler* uma credencial já guardada — o mesmo binário documentado também cria o item do zero, com `--generate-password` delegando ao próprio cofre a geração da senha, sem que você precise inventar ou digitar uma manualmente [25].

Duas observações fecham este pilar. A primeira: se você preferir não digitar `git commit` manualmente toda vez, o próprio `chezmoi` documenta um campo `autoCommit: true` na sua configuração — uma terceira forma real de resolver o mesmo problema que o manual tentou nomear com um subcomando inexistente [5]. A segunda: o segredo (a chave de API) nunca entra no `CLAUDE.md` versionado em texto puro — ele é lido em tempo de uso direto do cofre do 1Password [25], o que significa que o repositório de dotfiles pode ser público ou compartilhado com a equipe sem vazar nenhuma credencial.

### O Script de Alerta Rápido

Como consolidação final, o script abaixo automatiza a primeira triagem do checklist: ele varre um trecho de texto (colado de um manual ou tutorial novo) em busca de padrões que, ao longo deste livro, mais vezes precederam um veredito Fabricado ou Parcialmente Correto — nomes de subcomando muito específicos ao lado de um verbo pouco comum, ou caminhos de configuração dentro de `~/.config/<produto>/` que soam plausíveis demais. Ele não substitui a perícia manual; serve como primeiro filtro, um lembrete automático para abrir o `--help` antes de copiar.

```bash
#!/usr/bin/env bash
# auditar-comando.sh — triagem heuristica de comandos suspeitos em um manual novo
# Uso: auditar-comando.sh < trecho-do-manual.txt

set -euo pipefail

PADROES_SUSPEITOS=(
  '--target [a-z]+ --content'
  'skill activate'
  '~/\.config/[a-z-]+/config\.(json|yaml)'
  'commit -m'
  'session (search|read) --'
)

echo "== Triagem heuristica (Capitulo 8) =="
while IFS= read -r linha; do
  for padrao in "${PADROES_SUSPEITOS[@]}"; do
    if echo "$linha" | grep -qE "$padrao"; then
      echo "SUSPEITO: $linha"
      echo "  -> classifique a fonte (A/B/C), rode --help, preencha o protocolo-pericia.yaml"
    fi
  done
done

echo "== Fim da triagem: nenhum item aqui foi aprovado automaticamente =="
```

### Blindagem Extra: Grep de Segredo Antes do Commit

O cofre versionado do Pilar 2 (`chezmoi` + Git) só cumpre a promessa de "restaurar em minutos numa máquina nova" se nenhum segredo em texto puro entrar no repositório por descuido — porque um repositório de dotfiles, diferente de uma credencial isolada, costuma ser compartilhado com a equipe ou até publicado. O script abaixo é o mesmo tipo de triagem heurística do `auditar-comando.sh`, aplicado agora à sua própria mudança antes do commit, não ao texto de um manual de terceiros: ele varre o diff staged do diretório-fonte do `chezmoi` em busca dos dois padrões mais comuns de segredo esquecido — uma chave de API colada por engano e uma chave privada completa.

```bash
#!/usr/bin/env bash
# blindar-commit.sh -- grep de seguranca antes de commitar o cofre de dotfiles.
# Uso: dentro do diretorio-fonte do chezmoi (apos `chezmoi cd`), antes do commit:
#   ./blindar-commit.sh

set -euo pipefail

PADROES_SEGREDO=(
  'sk-[a-zA-Z0-9_-]{20,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'AKIA[0-9A-Z]{16}'
)

echo "== Blindagem de segredo antes do commit =="

encontrou=0
for padrao in "${PADROES_SEGREDO[@]}"; do
  if git diff --cached | grep -qE "$padrao"; then
    echo "BLOQUEADO: padrao de segredo encontrado no diff staged ($padrao)"
    encontrou=1
  fi
done

if [ "$encontrou" -eq 1 ]; then
  echo "Remova o segredo do arquivo e injete via 'op read' em tempo de uso."
  exit 1
fi

echo "Nenhum padrao de segredo encontrado. Commit liberado."
```

Isso não substitui o hábito de nunca digitar o segredo no arquivo em primeiro lugar — mas funciona como a mesma rede de segurança automática que o `auditar-comando.sh` oferece para comandos suspeitos de um manual: um filtro de primeira linha, nunca a prova final. A prova final, aqui como em todo o resto do livro, continua sendo a fonte primária — neste caso, a confirmação visual de que o `git diff --cached` não carrega nada que devesse ter ficado só no cofre do 1Password.

## 5. Aplica

Imagine a cena: você acabou de entrar num time novo, e alguém compartilha no canal um artigo recém-publicado prometendo "o guia definitivo" de automação para uma ferramenta de agente que você já usa no dia a dia. O artigo tem comandos formatados com sintaxe realista, nomes de flag plausíveis, até um bloco de configuração YAML bonito. Você reconhece o nome do produto — usa ele há meses — e o instinto manda copiar e colar direto no terminal, porque "é a mesma ferramenta que eu já conheço, só um recurso novo que eu não tinha visto". Você cola. O terminal devolve `unrecognized flag` ou, pior, aceita silenciosamente e não faz nada do que o artigo prometeu.

O diagnóstico é exatamente o padrão da seção Explica: o nome familiar do produto desarmou sua desconfiança antes mesmo de você ler a segunda linha do comando. Você tratou familiaridade com o produto como se fosse prova de que a sintaxe exata estava certa — mas são duas coisas completamente diferentes, e é aí que mora quase todo erro deste livro, do Hermes Agent ao `chezmoi`. A correção não é desconfiar de tudo que parece bom demais; é aplicar o mesmo protocolo de sempre, sem exceção para ferramentas "que você já conhece": classificar a fonte do artigo (quase certamente Classe C), procurar a confirmação na Classe A ou B correspondente (a documentação oficial ou o repositório do projeto) e só então rodar o comando.

Vale registrar até onde esse protocolo escala sozinho. Para um punhado de comandos novos por semana, a checagem manual do checklist é rápida e não pesa na rotina. O gargalo aparece quando o volume cresce — dezenas de comandos novos por dia, num time inteiro adotando ferramentas diferentes — porque aí o tempo humano de contraprova na fonte primária vira o fator limitante, não a vontade de fazer a perícia direito. Nesse cenário, o script de triagem automatiza só a primeira filtragem (sinalizar o que parece suspeito); ele nunca substitui a confirmação humana na fonte oficial, porque automatizar o próprio veredito reintroduziria o mesmo risco que o checklist existe para eliminar.

Armadilhas comuns que valem a pena revisar antes de fechar este livro:

- Tratar "o produto é real, eu já uso ele" como equivalente a "esse comando específico é real".
- Aceitar um resultado NÃO VERIFICÁVEL como se fosse aprovado só porque ninguém desmentiu.
- Copiar configuração de um blog (Classe C) sem checar se ela ainda bate com a versão instalada — ferramentas mudam de schema entre versões, e o artigo pode estar correto para uma versão antiga.
- Versionar segredo (chave de API, token) direto no arquivo de dotfiles em vez de injetá-lo via cofre em tempo de uso.

### Exercício
- [ ] Rode `--help` (ou equivalente) numa ferramenta de agente que você já usa antes de copiar qualquer comando novo de um tutorial está semana
- [ ] Classifique 3 fontes que você consulta no trabalho hoje como Classe A, B ou C, usando os critérios deste capítulo
- [ ] Preencha um `protocolo-perícia.yaml` para 1 comando que você copiou de algum lugar sem checar nos últimos 30 dias
- [ ] Rode `chezmoi init` num diretório de teste e confirme o hash SHA-256 do seu próprio `CLAUDE.md` antes e depois de uma edição
- [ ] Identifique, no seu ambiente de trabalho, algo que você trata hoje como "aprovado" mas que na verdade nunca teve fonte primária confirmando — reclassifique como pendente

## 6. Conclusão

Você fecha este livro com três ferramentas permanentes, não com uma lista de correções para o manual v3.1. A primeira é o checklist de perícia — hierarquia de fontes A/B/C, atenção redobrada ao padrão "produto real com sintaxe fabricada", e a regra de que NÃO VERIFICÁVEL fica pendente, nunca aprovado. A segunda é o cofre versionado: `CLAUDE.md` estático para preservar cache, hash SHA-256 para detectar mudança silenciosa, `chezmoi` com a sintaxe real (nunca o `commit` fabricado) para restaurar tudo isso em minutos numa máquina nova, e o 1Password CLI para que nenhum segredo trafegue em texto puro. A terceira é a mais difícil de medir, mas a mais real: a virada de protagonismo.

O caso deste livro, encerrado agora, tem um placar final. Dos itens auditados no manual v3.1, ao longo dos oito capítulos, 26 foram confirmados batendo com a fonte primária, 13 eram parcialmente corretos — produto real, detalhe errado —, 18 foram integralmente fabricados e 4 permanecem não verificáveis até hoje. Isso significa que perto de 40% do manual original tinha núcleo técnico genuíno e ensinável — o mesmo núcleo que sustentou, por exemplo, o mecanismo de cache real que você usa desde o Capítulo 2 [12] e o gerenciador de dotfiles que acabou de restaurar seu cofre de configurações [5]. Não é pouco — é o suficiente para explicar por que tanta gente confiou nele. E não é muito — é o suficiente para explicar por que copiar e colar sem perícia teria quebrado, silenciosamente, boa parte dos fluxos de trabalho de quem seguiu o manual à risca.

Você não fecha este livro sabendo mais comandos. Fecha sabendo o que fazer quando o próximo manual, sobre uma ferramenta que ainda nem existe hoje, chegar até você.

## 7. Referências Bibliográficas

[1] NOUSRESEARCH. *hermes-agent*. Disponível em: https://github.com/NousResearch/hermes-agent. Acesso em: 20 ago. 2026.

[2] ANTHROPIC. *Claude Code settings*. Disponível em: https://code.claude.com/docs/en/settings. Acesso em: 20 ago. 2026.

[3] ANTHROPIC. *Hooks reference*. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 20 ago. 2026.

[4] GOOGLE. *Gemini CLI — Configuration*. Disponível em: https://geminicli.com/docs/reference/configuration/. Acesso em: 20 ago. 2026.

[5] CHEZMOI. *Install* e *Daily operations*. Disponível em: https://www.chezmoi.io/install/. Acesso em: 20 ago. 2026.

[6] MICROSOFT. *LLMLingua* (repositório oficial). Disponível em: https://github.com/microsoft/LLMLingua. Acesso em: 20 ago. 2026.

[7] RYOPPIPPI. *ccusage: A CLI tool for analyzing Claude Code/Codex CLI usage from local JSONL files*. Disponível em: https://github.com/ryoppippi/ccusage. Acesso em: 20 ago. 2026.

[8] AGENTBRISK. *Prompt Caching Deep Dive: How to Cut Anthropic API Costs by 90%*. Disponível em: https://agentbrisk.com/blog/prompt-caching-deep-dive-2026/. Acesso em: 20 ago. 2026.

[9] CLAUDELOG. *What is ccusage tool for Claude Code*. Disponível em: https://claudelog.com/faqs/what-is-ccusage-tool/. Acesso em: 20 ago. 2026.

[10] NOUSRESEARCH. *CLI Interface — Hermes Agent*. Disponível em: https://hermes-agent.nousresearch.com/docs/user-guide/cli. Acesso em: 20 ago. 2026.

[11] NOUSRESEARCH. *Configuration — Hermes Agent*. Disponível em: https://hermes-agent.nousresearch.com/docs/user-guide/configuration. Acesso em: 20 ago. 2026.

[12] ANTHROPIC. *Prompt caching*. Disponível em: https://platform.claude.com/docs/en/build-with-claude/prompt-caching. Acesso em: 20 ago. 2026.

[13] AIDER. *Prompt caching*. Disponível em: https://aider.chat/docs/usage/caching.html. Acesso em: 20 ago. 2026.

[14] OLLAMA. *Library* (catálogo de modelos). Disponível em: https://ollama.com/library. Acesso em: 20 ago. 2026.

[15] OLLAMA. *ollama/ollama*. Disponível em: https://github.com/ollama/ollama. Acesso em: 20 ago. 2026.

[16] ZILLIZTECH. *GPTCache: A Library for Creating Semantic Cache for LLM Queries* (docs/usage.md). Disponível em: https://github.com/zilliztech/GPTCache/blob/main/docs/usage.md. Acesso em: 20 ago. 2026.

[17] TENSORSTAX. *agenttrace: lightweight observability library to trace and evaluate agentic systems*. Disponível em: https://github.com/tensorstax/agenttrace. Acesso em: 20 ago. 2026.

[18] F. *agentlytics: Comprehensive analytics dashboard for AI coding agents*. Disponível em: https://github.com/f/agentlytics. Acesso em: 20 ago. 2026.

[19] GGML-ORG. *llama.cpp*. Disponível em: https://github.com/ggml-org/llama.cpp. Acesso em: 20 ago. 2026.

[20] VLLM PROJECT. *CLI Reference — serve*. Disponível em: https://docs.vllm.ai/en/stable/cli/serve/. Acesso em: 20 ago. 2026.

[21] OPENAI. *Configuration Reference — Codex CLI*. Disponível em: https://developers.openai.com/codex/config-basic. Acesso em: 20 ago. 2026.

[22] OPENCODE. *Config*. Disponível em: https://opencode.ai/v2/docs/config. Acesso em: 20 ago. 2026.

[23] OPENCODE. *Zen*. Disponível em: https://opencode.ai/docs/zen/. Acesso em: 20 ago. 2026.

[24] GOOGLE-GEMINI. *gemini-cli*. Disponível em: https://github.com/google-gemini/gemini-cli. Acesso em: 20 ago. 2026.

[25] 1PASSWORD. *op signin — CLI command reference*. Disponível em: https://developer.1password.com/docs/cli/reference/commands/signin. Acesso em: 20 ago. 2026.
