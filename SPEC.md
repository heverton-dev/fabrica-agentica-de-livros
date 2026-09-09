# SPEC.md — livro "Ecossistema AIDD: Fundação Prática para Projetos com Agentes Autônomos de IA"

> Generado por /esbocar. Revisar antes de /criar-livro.

## Obra

- **slug:** `ecossistema-aidd`
- **tipo_obra:** livro
- **nivel:** intermediario *(badge obrigatório, validado por validar-capa-nivel.py)*
- **tema:** os pilares de engenharia do kit-fundacao-aidd explicados e ensinados com exemplos reais do projeto, incluindo hook de pre-commit e CI/CD como prática mecânica de integridade
- **persona_leitor:** praticante de engenharia de software que quer entender e aplicar as decisões de projeto em qualquer repositório
- **motivo_condutor:** o autor sofreu (ou acompanhou) falhas reais onde "promessa em texto" e "quem gera também aprova" custaram produção — o livro transforma essas lições em hábitos de projeto replicáveis

## Persona / Leitor-alvo

- Já escreve código em Python/Node e já atropela um repo novo ocasionalmente
- Ouviu falar de "separar builder de critic", "hook de pre-commit", "registro declarativo" mas não sabe por que valem a pena nem como introduzi-los num projeto existente sem destruir o que já funciona
- Não quer teoria genérica — quer ver o princípio, ver o arquivo, ver o teste, ver o diff, poder reaplicar na prática

## Objetivo pedagógico (não só informativo)

Ao fim, o leitor deve ser capaz de:

1. Decir, num repo novo, quais das 6 peças valem a pena adicionar agora e quais esperar
2. Instalar uma peça sem remover/sobreschrever o que já existe (regra do instalador aditivo)
3. Ler um postmortem existente e transformar cada linha de "Prevenção" em teste de regressão
4. Escrever um criterio deterministico simples que hoje é checado "no olhômetro"
5. Explicar para um colega por que o critico nunca deve ser o mesmo agente do builder
6. Configurar um hook de pre-commit mínimo e um pipeline CI básico que respeita o gate de "nunca commitar vermelho"

## Escopo (o que entra)

- As 6 peças do kit-fundacao-aidd como capítulo temático, não como documentação seca do submodule:
  1. Builder ≠ Critic — quem gera nunca é quem aprova
  2. Crítico determinístico (gate) — checagem de formato/presença/contagem é script, nunca LLM
  3. Registro declarativo — princípio Aberto/Fechado: tipo novo = 1 entrada no dicionário, nunca `if tipo == ...` espalhado
  4. Nunca commitar vermelho — hook mecânico, não promessa em texto
  5. Postmortem que vira teste — toda linha de "Prevenção" nasce junto com um teste de regressão
  6. Hook + CI/CD — integridade mecânica do repo: hook local de pre-commit + pipeline CI básico que respeita o gate de "nunca commitar vermelho" (CI não substitui hook, complementa; cobertura vs. prevenção)
- Exemplo canônico em Python (porque é a stack detectada deste projeto: requirements.txt/pyproject.toml) e exemplo paralelo em Node onde fazer sentido
- Como diagnosticar um projeto existente antes de instalar (analisar-projeto.py como caso de uso), e como o instalador decide não forçar nada
- O que NÃO é o kit: não é framework de agentes, não éimento de LLM, não é orquestração — é disciplina de projeto que qualquer repo pode absorver cedo

## Escopo (o que NÃO entra — para não inflar)

- Não é tutorial de Claude Code / Codex / qualquer harness específico (o kit é harness-agnostic)
- Não é livro de testes unitários em geral (o foco é a disciplina de transformar prevenção em teste, não cobertura exhaustiva)
- Não é DRG ou token economy detalhada (o livro pode citar como convite, não como capítulo principal)
- Não substitui a leitura do manual de cada peça no repo do kit — o livro ensina o PORQUÉ e o COMO introduzir; cada peça tem seu molde no submodule
- CI/CD não é guia de infraestrutura completa (GitHub Actions/GitLab CI) — é a disciplina de ter um mecanismo que bloqueia commits vermelhos, com exemplo mínimo funcional

## Pré-requisitos do leitor

- Saber o que é um script Python básico e um arquivo de configuração (pyproject.toml / package.json)
- Ter noção do que é um hook de git, do que é uma review/merge, e o básico de um pipeline CI (o que é, para que serve)
- Não exigido: ser autor de agentes de IA — a inspiração vem de projetos agênticos, mas as 6 peças servem qualquer projeto

## Design de capa (R5)

- Livro → capa 2D plano (padrão `docs/referencia-capa-design.md`)
- Badge de nível obrigatório ("intermediário") — validado por `validar-capa-nivel.py`
- Paleta derivada do manifesto da coleção quando existir; até lá, neutra com acento que contraste com o badge

## Estrutura

### Parte 1 — Por que o kit existe (contexto + motivação, não divulgação)

**Cap 1 — O pretexto que custa caro**
- "promessa em texto" vs "regra mecânica": o custo real de depender da vontade humana para coerência
- Exemplos anedóticos tidos como archetipo (sem acusar repo específico): review onde quem escreveu também aprovou; hook que "deve existir" mas não impede o commit vermelho; postmortem que documenta a lição mas não previne a recorrência; CI que só reporta sem bloquear
- A pergunta do livro: quais dessas promessas poderiam ser leis do repo independentemente de quem está no turno?

**Cap 2 — As 6 peças em uma só frase cada**
- Mapa de concepto: uma tabela com peça / pergunta que ela resolve / custo de não ter / quando introduzir
- Regra de introdução conservadora: diagnosticar antes de instalar; nunca remover/sobrescrever; dry-run por padrão
- Distinção prática: hook local (pre-commit) protege o commit; CI protege o merge/pull. Ambas espelham a mesma intenção: não plantar vermelho no repo.

### Parte 2 — As 6 peças, uma por capítulo (o núcleo ensinável)

**Cap 3 — Peça 1: Builder ≠ Critic**
- O conflito de interesse estrutural de "quem gera também aprova"
- Como identificar a separação no projeto atual (.claude/agents, agentic/agents, etc.) usando critérios objetivos (tools: Read isolado vs Write/Edit)
- O que acontece quando não há separação — e o que NÃO se promete (a separação é uma convenção organizacional, não um filtro de qualidade grosso)
- Exercício prático: dado um conjunto de agentes listados, classificar quem é builder vs critic vs ambíguo
- Referência: separação de responsabilidades / revisão por pares em engenharia de software (citar fonte canônica, ABNT)

**Cap 4 — Peça 2: Crítico determinístico (gate)**
- O que é um critico/gate: script que decide aceitável/não-aceitável em questões de formato/presença/contagem — nunca julgamento nuance de LLM
- Quando usar: checklist determinístico: presença de campo, formato de frente, contagem mínima, presença de um marcador de política
- Quando NÃO usar: qualidade conceitual, corretude algorítmica complexa, revisão de copy sutil — ali cabe revisor humano/LLM, não o gate
- Exemplo canônico em Python (template do gate) + como ele evita falso-positivo conhecido (ex.: "todo/Todo" gerando reprovação em capítulo legítimo)
- Exemplo de gate que se torna falso-positivo e como corrigir (caso real deste projeto: validar-afirmacoes e listas de definições sem [N])
- Exercício: dado um critério textual ("todo arquivo de capítulo deve ter X"), reescrever como gate determinístico
- Referência: teste determinístico vs. revisão humana; linting como gate de formato (citar fonte reconhecida)

**Cap 5 — Peça 3: Registro declarativo**
- O sintoma de alerta: mesma variável de tipo repetida em >=2 arquivos (`if tipo == "..."`) — sinal de que é hora de migrar para registro
- Princípio Aberto/Fechado declarado de forma didática: tipo novo = 1 entrada no dicionário, nunca editar 6 arquivos de dispatch
- Como ler o relatório de analisar-projeto.py que mostra os candidatos a registro declarativo
- Exemplo canônico: `scripts/registro_declarativo_scaffold.py` gerando o esqueleto para um conceito
- Como consumir o registro (função obter que levanta KeyError explícito) e por que essa escolha importa para debugging
- Exercício: transformar um arquivo de dispatch `if/elif` em registro
- Referência: princípio SOLID Open/Closed — fonte canônica (Martin/SOLID) em ABNT

**Cap 6 — Peça 4: Nunca commitar vermelho**
- O que "vermelho" significa aqui: suíte de testes falhando no momento do commit, não "código não rodando"
- Como o hook mecânico bloqueia (exemplo de marcador de bloco no pre-commit: `kit-fundacao-aidd: Peça 4 (nunca commitar vermelho)`)
- Por que a regra é "append, nunca substituir" quando o hook já existe — e como o instalador respeita isso
- Para que esse gate NÃO vira armadilha: garantir que o projeto tenha uma suíte de teste mínima que o hook possa rodar — sem isso, o hook é inerte
- Exercício: revisar um pre-commit existente e decidir se vale a pena anexar o bloco do kit ou pular (justificativa objetiva)
- Referência: integridade de commit / pre-commit hooks — convenção de Git / workflow de integração contínua (citar fonte reconhecida)

**Cap 7 — Peça 5: Postmortem que vira teste**
- O padrão de postmortem que documenta mas não previne a recorrência
- O molde: cada linha de "Prevenção" nasce com um stub de teste de regressão (templates/POSTMORTEM.md + postmortem_para_teste.py)
- Como gerar o stub a partir do bloco de postmortem — e preenchê-lo com caso de teste real
- Como esse padrão muda a cultura de "escrever para arquivar" para "escrever para que o repo obelite a recorrência"
- Exercício: pegar um postmortem fictício e gerar o stub de teste correspondente; depois escrever o caso concreto
- Referência: blameless postmortem / cultura de aprendizado com SRE — Google SRE Book ("Postmortem Culture"), ABNT

**Cap 8 — Peça 6: Hook + CI/CD (integridade mecânica do repo)**
- A diferença prática: hook de pre-commit roda local antes do commit; CI roda no servidor antes do merge
- Por que o livro trata isso como peça distinta e não como subitem de "nunca commitar vermelho": porque a mesma intenção (não plantar vermelho no repo) precisa de duas camadas quando o time cresce
- Exemplo mínimo funcional: um workflow CI básico que roda a suíte de teste e falha se for vermelho — não é guia de infraestrutura completa, é ilustração da disciplina
- Como evitar que CI e hook conflitem ou duplicem sem valor: hook protege o commit local; CI protege o merge remoto — mesmo gate, dois pontos de aplicação
- Exercício: dado um repo sem CI, escrever um pipeline mínimo que respeite o gate "não comitar vermelho" e explicar o que ele não faz (limites do exemplo)
- Referência: pipeline de integração contínua como prática de qualidade (citar fonte reconhecida sobre CI)

### Parte 3 — Como aplicar no seu projeto (síntese prática)

**Cap 9 — Diagnosticar antes de instalar**
- O que analisar-projeto.py lê e reporta: stack detectada, convenção de agentes, hook existente, builder/critic presente?, candidatos a registro declarativo, convencao de postmortem
- Como usar o relatório para decidir quais peças propor (nunca impor) — e como o instalador transforma diagnóstico em propostas
- O que fazer quando o relatório diz "não detectado" por falta de convenção (muitas vezes é antes da hora, não falha do kit)

**Cap 10 — Instalar sem destruir**
- O ritual: dry-run antes de aplicar; explicar antes de gravar; peça por peça, não "todas de uma vez"
- Caminhos de instalação reais: agents/, scripts/, hooks/, templates/, skills/ — com o que cada um entrega
- Regra inegociável reforçada: nunca remover/sobrescrever o que já existe; em colisão, mesclar aditivo ou pular com justificativa
- Como manter o submodule atualizado (git pull) sem desconfigurar o projeto-alvo

**Cap 11 — Manter vivo depois da instalação**
- Quando revisitar as peças: projeto cresce, novas convenções aparecem, hooks e CI ficam desatualizados
- Como detectar que uma peça se tornou carga: gate que reprova tudo e ninguém entende, registro que só tem 1 entrada, hook/CI que não têm suíte para rodar
- Sinal dos parâmetros: convenção de postmortem detectada no CLAUDE.md como evidência de que a peça 5 já está culturalmente presente — o kit pode pular sem perder nada

## Mapa de referências por capítulo (padrão fabrica)

- Cada capítulo da Parte 2 deve ter ao menos 1 referência real rastreável (autor-data, ABNT) sobre o princípio envolvido:
  - Cap 3 (Builder≠Critic / revisão por pares) → fonte canônica de engenharia de software
  - Cap 4 (Crítico determinístico / gate vs. revisão) → fonte reconhecida sobre lint/testing como gate
  - Cap 5 (Registro declarativo / Aberto/Fechado) → SOLID Open/Closed (Martin), ABNT
  - Cap 6 (Nunca commitar vermelho / hook) → convenção de Git / workflow de integração contínua
  - Cap 7 (Postmortem que vira teste) → Google SRE Book, "Postmortem Culture", ABNT
  - Cap 8 (Hook + CI/CD) → fonte reconhecida sobre CI como prática de qualidade
- As referências devem ter URL/DOI real se possível (gate R-RF); ao menos Autor-Data e título 확인áveis

## Gates de conteúdo ativados para este livro

- **R-RF (referências):** URL/DOI reais, 4xx/DNS reprova, cache + --sem-rede
- **R-MT (máscaras):** >=1 metrica com valor+unidade+citação por capítulo (ex.: número de arquivos candidatos ao registro, número de linhas do hook, número de peças propostas pelo diagnóstico)
- **R-AF (afirmações):** dado factual sem [N] no parágrafo reprova (evitar generalizações não marcadas)
- **R-FT (fontes):** hierarquia A/B/C do dossiê >=70% A+B

> **Nota:** R-CLI (comandos CLI) NÃO está ativo neste livro — opt-in via config_obra.json:categoria_tecnica, e o operador decidiu manter gates padrão apenas. Scripts de exemplo do livro ainda devem ser executáveis (validar-codigo.py --executar), mas bloco de comando sem marcação não reprova.

> **validar-codigo.py --executar:** scripts de exemplo do livro devem executar (smoke test real)

## Arquivos de suporte que o livro deve ler para escrever

- `tooling/kit-fundacao-aidd/README.md` (as 6 peças, uso)
- `tooling/kit-fundacao-aidd/analisar-projeto.py` (diagnóstico — ler assinaturas + main)
- `tooling/kit-fundacao-aidd/instalar.py` (instalador aditivo — ler assinaturas + main)
- `tooling/kit-fundacao-aidd/scripts/registro_declarativo_scaffold.py` (esqueleto registro)
- `tooling/kit-fundacao-aidd/scripts/postmortem_para_teste.py` (conversor postmortem→teste)
- `tooling/kit-fundacao-aidd/templates/POSTMORTEM.md` (molde)
- `tooling/kit-fundacao-aidd/hooks/pre-commit.template` (molde hook)
- `tooling/kit-fundacao-aidd/agents/builder.md.template` e `critic.md.template` (convenção builder/critic)
- `tooling/kit-fundacao-aidd/skills/kit-fundacao-aidd/SKILL.md` (versão interativa)
- `docs/manual-replicar-praticas-acima-media.md` (origem das 5 peças, se relevante para citações)
- `relatorios/12-08-2026-kit-fundacao-aidd.md` (o que foi feito na sessão de extração — para contexto, não copiar)

## Critérios de aceitação do SPEC (para revisor/arquiteto antes de /criar-livro)

- [x] Tema, slug, nível e persona consistentes entre si
- [x] Escopo entra / não-entra claramente delineado (evita inflar para tutorial de harness ou de testes em geral)
- [x] Parte 2 (as 6 peças) tem 6 capítulos, cada um com exemplo/prática, não só definição
- [x] Parte 3 dá fluxo de aplicação real (diagnosticar → instalar sem destruir → manter)
- [x] Referências por capítulo listadas como campo, com 1+ citação real por capítulo (ABNT, URL/DOI quando disponível)
- [x] Gates de conteúdo: padrão (R-RF, R-MT, R-AF, R-FT) + validar-codigo --executar; R-CLI NÃO ativo (categoria_tecnica=False)
- [x] Lista de arquivos de suporte suficiente para que o redator não precisa alucinar neutrão

## Pendências antes de /criar-livro

- Confirmar slug não conflita com obra já existente em output/ (verificado: output/ não tem ecossistema-aidd; coleções existentes são temáticas de livros AIDD, não deste)
- Validar se coleção/cross-references com outros livros da fábrica se fazem necessários (este é sobre fundamentação do kit, não sobre produto específico — o vínculo é o caso de uso AIDD; cross-ref opcional)
- Se operador quiser incluir campanha/máquina na coleção correspondente, decidir na chamada de /esbocar ou depois via /campanha e /criar-maquina — o livro em si não depende disso
