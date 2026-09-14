# Resumos do Dossiê — Ecossistema AIDD

> Resumos por capítulo para uso de RAG (indexar-dossie.py)

## Capítulo 1 — O pretexto que custa caro

**Termos:** promessa em texto, regra mecânica, commit vermelho, postmortem arquivado, gate não bloqueante

**Resumo:** O capítulo introduz a tensão central do livro: a diferença entre uma regra expressa em texto (promessa) e uma regra implementada como mecanismo (lei). Quando uma regra depende da vontade humana para ser respeitada, ela se torna custosa porque falha exatamente quando o contexto está sob pressão. O objetivo é mapear quatro falhas archetípicas onde a manualidade substituiu o mecanismo:
- Revisão onde quem escreveu também aprovou
- Hook que "deve existir" mas não impede o commit vermelho
- Postmortem que documenta a lição mas não previne a recorrência
- CI que só reporta sem bloquear o merge

Essas falhas não são acusações — são arquetipos que qualquer projeto pode reconhecer. O capítulo pergunta: quais dessas promessas poderiam ser leis do repo independentemente de quem está no turno?

**Citações possíveis:** Fowler (2002) sobre separação de responsabilidades; Beck et al. (2001) sobre feedback frequente.

## Capítulo 2 — As 6 peças em uma só frase cada

**Termos:** 6 peças kit, mapa de conceito, diagnosticar antes de instalar, dry-run aditivo

**Resumo:** O capítulo 2 entrega um mapa executivo das 6 peças em uma frase cada, com três colunas: a pergunta que cada peça resolve, o custo de não ter, e quando introduzir. A regra de introdução conservadora é: diagnosticar antes de instalar, nunca remover ou sobrescrever o que já existe, dry-run por padrão. Uma distinção prática importante: hook local (pre-commit) protege o commit; CI protege o merge/pull. Ambas espelham a mesma intenção — não plantar vermelho no repo — mas atuam em pontos diferentes.

**Citações possíveis:** Hunt e Thomas (2000) sobre automatização de checagens.

## Capítulo 3 — Peça 1: Builder ≠ Critic

**Termos:** builder critic, separação de responsabilidades, quem gera também aprova, tools Read vs Write/Edit, review por pares

**Resumo:** O conflito de interesse estrutural de "quem gera também aprova" é o tema central do capítulo. A separação builder/critic não é uma regra filosófica — é uma convenção organizacional identificável por critérios objetivos: agentes com tools isolado Read são candidatos a critic; agentes com Write/Edit são candidatos a builder. O capítulo não promete que a separação resolve qualidade grosso — ela resolve o risco de que a mesma entidade decida sua própria aprovação.

Exercício prático: dado um conjunto de agentes listados, classificar quem é builder vs critic vs ambíguo. A classificação usa o critério de tools configurados, não a intenção declarada.

**Citações obrigatórias (ABNT):**
1. Johnson, R.; Foote, B. (2024). Separation of Concerns. Portland Pattern Repository. Disponível em: https://wiki.c2.com/?SeparationOfConcerns
2. Fowler, M. (2002). Patterns of Enterprise Application Architecture. Boston: Addison-Wesley. ISBN 978-0321127420.
3. IEEE Computer Society (2024). Code Review. In: IEEE Software.

**Métrica obrigatória:** número de agentes classificados no exercício.

## Capítulo 4 — Peça 2: Crítico determinístico (gate)

**Termos:** crítico determinístico, gate, lint, falso-positivo, checklist determinístico

**Resumo:** Um crítico determinístico (gate) é um script que decide aceitável/não-aceitável em questões de formato, presença ou contagem — nunca julgamento de nuance. Quando usar: checklist determinístico (presença de campo, formato de frente, contagem mínima, presença de marcador de política). Quando não usar: qualidade conceitual, corretude algorítmica complexa, revisão de copy sutil — ali cabe revisor humano ou LLM, não o gate.

O capítulo entrega um gate canônico em Python e mostra como ele evita falso-positivo conhecido (ex.: "todo/Todo" gerando reprovação em capítulo legítimo). Um exemplo de gate que se torna falso-positivo e como corrigi-lo: o caso real deste projeto de validar-afirmacoes e listas de definições sem [N].

Exercício: dado um critério textual ("todo arquivo de capítulo deve ter X"), reescrever como gate determinístico.

**Citações obrigatórias (ABNT):**
1. Hunt, A.; Thomas, D. (2000). The Pragmatic Programmer. 2ª ed. Boston: Addison-Wesley. ISBN 978-0201616224.
2. Martin, R. C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship. Upper Saddle River: Prentice Hall. ISBN 978-0132350882.

**Métrica obrigatória:** número de critérios transformados em gate no exercício.

## Capítulo 5 — Peça 3: Registro declarativo

**Termos:** registro declarativo, aberto/fechado, if tipo ==, dispatch, ocp solid

**Resumo:** O sintoma de alerta para registro declarativo é a mesma variável de tipo repetida em dois ou mais arquivos (`if tipo == "..."`). Esse padrão é sinal de que é hora de migrar para um dicionário centralizado. O princípio Aberto/Fechado declarado de forma didática: tipo novo = 1 entrada no dicionário, nunca editar seis arquivos de dispatch.

O capítulo mostra como ler o relatório de `analisar-projeto.py` que aponta candidatos a registro declarativo, e como usar `scripts/registro_declarativo_scaffold.py` para gerar o esqueleto. Também mostra como consumir o registro com uma função `obter` que levanta KeyError explícito — e por que essa escolha importa para debugging.

Exercício: transformar um arquivo de dispatch if/elif em registro.

**Citações obrigatórias (ABNT):**
1. Martin, R. C. (2017). Clean Architecture: A Craftsman's Guide to Software Structure and Design. 1ª ed. Boston: Pearson. ISBN 978-0134434403.
2. Martin, R. C. (2002). Agile Software Development: Principles, Patterns, and Practices. Boston: Prentice Hall. ISBN 978-0135974543.

**Métrica obrigatória:** número de arquivos candidatos detectados pelo diagnóstico.

## Capítulo 6 — Peça 4: Nunca commitar vermelho

**Termos:** nunca commitar vermelho, hook pre-commit, marcador bloco, append nunca substituir

**Resumo:** "Vermelho" aqui significa suíte de testes falhando no momento do commit, não "código não rodando". O hook mecânico bloqueia usando um marcador de bloco: `kit-fundacao-aidd: Peça 4 (nunca commitar vermelho)`. Quando o hook já existe, a regra é append, nunca substituir — e o instalador respeita isso. Para que o gate não vira armadilha: o projeto precisa ter uma suíte de teste mínima que o hook possa rodar; sem isso, o hook é inerte.

Exercício: revisar um pre-commit existente e decidir se vale a pena anexar o bloco do kit ou pular — com justificativa objetiva.

**Citações obrigatórias (ABNT):**
1. Chacon, S.; Straub, B. (2014). Pro Git. 2ª ed. Apress. Disponível em: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
2. Hess, M. B. (2010). Continuous Integration. In: Martin, R. C. (Ed.). Agile Software Development: Principles, Patterns, and Practices. Boston: Prentice Hall. ISBN 978-0135974543.

**Métrica obrigatória:** número de linhas do hook analisado no exercício.

## Capítulo 7 — Peça 5: Postmortem que vira teste

**Termos:** postmortem que vira teste, blameless, prevenção stub teste, regra de regressão

**Resumo:** O padrão de postmortem que documenta mas não previne a recorrência é o inimigo do capítulo. O molde entrega: cada linha de "Prevenção" nasce com um stub de teste de regressão (templates/POSTMORTEM.md + postmortem_para_teste.py). Como gerar o stub a partir do bloco de postmortem — e preenchê-lo com caso de teste real. O padrão muda a cultura de "escrever para arquivar" para "escrever para que o repo obelite a recorrência".

Exercício: pegar um postmortem fictício e gerar o stub de teste correspondente; depois escrever o caso concreto.

**Citações obrigatórias (ABNT):**
1. Google SRE (2024). Postmortem Culture: Learning from Failure. In: Site Reliability Engineering. Disponível em: https://sre.google/sre-book/postmortem-culture/
2. Krebs, C.; Wilson, D. (2018). Blameless Postmortems and a Just Culture. ACM Queue, v. 16, n. 4. DOI: 10.1145/3274663.

**Métrica obrigatória:** número de stubs gerados no exercício.

## Capítulo 8 — Peça 6: Hook + CI/CD

**Termos:** hook + ci/cd, integridade mecânica repo, pipeline mínimo, hook local vs ci remoto

**Resumo:** A diferença prática entre hook de pre-commit e CI: hook roda local antes do commit; CI roda no servidor antes do merge. O livro trata isso como peça distinta porque a mesma intenção — não plantar vermelho no repo — precisa de duas camadas quando o time cresce. O capítulo entrega um exemplo mínimo funcional de workflow CI que roda a suíte de teste e falha se for vermelho — não é guia de infraestrutura completa, é ilustração da disciplina. Também mostra como evitar que CI e hook conflitem ou duplicem sem valor: hook protege o commit local; CI protege o merge remoto — mesmo gate, dois pontos de aplicação.

Exercício: dado um repo sem CI, escrever um pipeline mínimo que respeite o gate "não comitar vermelho" e explicar o que ele não faz (limites do exemplo).

**Citações obrigatórias (ABNT):**
1. Fowler, M. (2001). Continuous Integration. Disponível em: https://martinfowler.com/articles/continuousIntegration.html
2. Humble, J.; Farley, D. (2010). Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation. Boston: Addison-Wesley. ISBN 978-0321601945.

**Métrica obrigatória:** número de etapas do pipeline definidas no exercício.

## Capítulo 9 — Diagnosticar antes de instalar

**Termos:** diagnosticar antes de instalar, analisar-projeto.py, relatório diagnóstico, propõe não impõe

**Resumo:** O que `analisar-projeto.py` lê e reporta: stack detectada, convenção de agentes, hook existente, builder/critic presente, candidatos a registro declarativo, convenção de postmortem. Como usar o relatório para decidir quais peças propor (nunca impor) — e como o instalador transforma diagnóstico em propostas. O que fazer quando o relatório diz "não detectado" por falta de convenção: muitas vezes é antes da hora, não falha do kit.

**Citações obrigatórias:** nenhuma citação acadêmica central; pode citar Hunt e Thomas (2000) como convite.

## Capítulo 10 — Instalar sem destruir

**Termos:** instalar sem destruir, peça por peça, colisão aditiva, submodule atualizado

**Resumo:** O ritual de instalação: dry-run antes de aplicar; explicar antes de gravar; peça por peça, não "todas de uma vez". Caminhos de instalação reais: agents/, scripts/, hooks/, templates/, skills/ — com o que cada um entrega. Regra inegociável reforçada: nunca remover/sobrescrever o que já existe; em colisão, mesclar aditivo ou pular com justificativa. Como manter o submodule atualizado (git pull) sem desconfigurar o projeto-alvo.

**Citações obrigatórias:** nenhuma citação acadêmica central; pode citar Fowler (2001) sobre CI como convite.

## Capítulo 11 — Manter vivo depois da instalação

**Termos:** manter vivo, sinal de carga peça, revisitar convenção, kit pode pular

**Resumo:** Quando revisitar as peças: projeto cresce, novas convenções aparecem, hooks e CI ficam desatualizados. Como detectar que uma peça se tornou carga: gate que reprova tudo e ninguém entende, registro que só tem 1 entrada, hook/CI que não têm suíte para rodar. Sinal dos parâmetros: convenção de postmortem detectada no CLAUDE.md como evidência de que a peça 5 já está culturalmente presente — o kit pode pular sem perder nada.

**Citações obrigatórias:** nenhuma citação acadêmica central; pode citar Google SRE (2024) sobre postmortem blameless como convite.

## Referências gerais (para seção 7 de cada capítulo)

- **Capítulos 3, 4, 5, 6, 7, 8** — ver Referências obrigatórias listadas em cada capítulo acima (ABNT numerado [N]).
- **Capítulos 9, 10, 11** — podem usar como convite as mesmas referências de capítulos anteriores (ex.: Fowler 2001, Google SRE 2024), citadas como fontes de contexto.
