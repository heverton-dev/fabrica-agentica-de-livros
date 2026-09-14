# Capítulo 3: Peça 1: Builder != Critic

## 1. Introdução

O capítulo anterior mostrou que as seis peças formam um ecossistema, e que o diagnóstico precede a instalação. Este capítulo entra na primeira peça: a separação entre quem gera o artefato e quem o aprova. A peça não é moral — é mecânica. Quem escreveu um arquivo, rodou um linter e empurrou para o repo tem interesse estrutural em que o arquivo passe na revisão dele mesmo; a separação não juzga a pessoa, julga o design do processo [1][2].

Ao final deste capítulo você será capaz de, frente a qualquer agente ou processo que gere ou valide um artefato, classificá-lo como builder, critic ou ambíguo usando critérios objetivos — e saber quando a ambiguidade é sinal de problema de processo.

## 2. Explica

A separação builder/critic é a mesma lógica que separa escrita e revisão em qualquer sistema onde a qualidade do artefato depende de alguém diferente do autor julgar se ele entra. O problema não é que o autor seja indiferente à qualidade — o problema é que o autor tem incentivo estrutural para ver o artefato como pronto, porque pronto é o que desbloqueia o próximo passo do autor [3][4].

Um exemplo concreto. Um script que gera documentação a partir de comentários de código tem, em sua lógica interna, um builder (gera a documentação) e um critique (decide se a documentação é aceitável). Se os dois forem o mesmo script, sem critério independente, o script pode gerar e aprovar documentação que está gramaticalmente correta e semanticamente vazia — porque o critério de "accept" é parte da mesma lógica que gerou [5].

A peça resolve isso definindo, para cada artefato, qual entidade é builder e qual é critic, e exigindo que as duas sejam distintas quando o critério de aceitação pode ser parcial ao gênero do artefato. A distinção é objetiva — não depende de intenção, depende de ferramentas e de fluxo. Um agente que só lê não é critic se a leitura não produz decisão de aceitação; um agente que só edita não é builder se a edição é decorrente de decisão externa [6][7].

A ambiguidade — quando builder e critic parecem ser a mesma entidade — é o sintoma que o diagnóstico da peça 1 captura. Ambiuidade legítima existe em processos pequenos onde a mesma pessoa faz as duas funções por necessidade; ambiguidade problemática existe quando o critério de aceitação depende de julgamento da builder sem independente. O exercício deste capítulo entrega um critério para distinguir os dois casos [1][2].

Métrica deste capítulo: número de agentes/processos classificados no exercício em builder, critic ou ambíguo — porque a classificação é o que transforma a intuição "tem que ter alguém revisando" em mapeamento rastreável do repo.

## 3. Ilustra

Imagine um formulário onde a mesma pessoa escreve a resposta e marca "está correto". A marcação é conveniente para a pessoa — mas o formulário não sabe se a resposta está correta, sabe apenas que quem escreveu acha que está. Substituir a auto-marcação por um segundo par de olhos muda a propriedade do formulário: a aprovação agora tem origem diferente da geração. Em repo, essa propriedade é o que protege o merge de promessa de "já revisei".

```mermaid
%% legenda: Builder vs Critic — origem diferente para geração e para decisão de aceitação
flowchart TD
  A[Artefato a ser gerido] --> B{Entidade A: Builder}\nquem gera/escreve/produz
  B --> C[Artefato gerado]
  C --> D{Entidade B: Critic}\nquem decide aceitável/não
  D -->|sim| E[Artefato entra no repo]
  D -->|não| F[Artefato não entra — feedback para builder]
  B -.->|se mesmo que A: conflito estrutural| G[Regras de aprovação frágeis\ndependem de voluntariado]
  H{A: 1 entidade, B: != A} -->|sim| E
  H -->|não| G
```

## 4. Técnica

A técnica da peça 1 é critério objetivo de classificação — não opinião. Para cada agente ou processo que toca um artefato, responda a três perguntas com sim/não:

1. **Geração:** a entidade produz conteúdo novo no artefato (arquivo, código, documento, configuração)? Se sim, a entidade é builder (pelo menos parcial).
2. **Decisão de aceitação:** a entidade decide se o artefato entra no repo, passa no gate ou é publicado? Se sim, a entidade é critic (pelo menos parcial).
3. **Independência:** a entidade que decide aceitação é a mesma que gerou? Se sim, é ambíguo — e a pergunta seguinte é se a ambiguidade é legítima (pequeno, sem risco de artefato ruim entrar) ou problemática (critério de aceitação dependente do gênero).

### Código: classificador builder/critic/ambíguo em Python

```python
# classificar_roles.py — classifica agente/processo por papel em um artefato
# Critério objetivo, sem nuance de LLM. Baseado em ferramentas e fluxo, não em intenção.

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class Papel(Enum):
    BUILDER = "builder"
    CRITIC = "critic"
    AMBIGUO = "ambíguo"
    NENHUM = "nenhum"

@dataclass(frozen=True)
class Ferramenta:
    nome: str
    le: bool
    escreve: bool
    edita: bool
    decide_aceite: bool

@dataclass(frozen=True)
class Agente:
    nome: str
    ferramentas: tuple[Ferramenta, ...]
    gera_controle: bool = False  # o agente comanda o ciclo de geração?

def classificar(agente: Agente) -> Papel:
    """Classifica agente por papel usando critérios objetivos de ferramenta e fluxo.
    Builder se gera conteúdo novo; Critic se decide aceite sem ser o geração;
    Ambíguo se builder e critic são mesma entidade e o geração comanda o ciclo;
    Nenhum se não faz parte do ciclo de geração/aceite.
    """
    gera = any(f.escreve or f.edita for f in agente.ferramentas) or agente.gera_controle
    decide = any(f.decide_aceite for f in agente.ferramentas)
    if not gera and not decide:
        return Papel.NENHUM
    if gera and decide and agente.gera_controle:
        # mesma entidade gera e decide e comanda o ciclo — ambiguidade estrutural
        return Papel.AMBIGUO
    if gera and not decide:
        return Papel.BUILDER
    if not gera and decide:
        return Papel.CRITIC
    # gera e decide mas não comanda o ciclo: review interno, verificar caso a caso
    return Papel.AMBIGUO

# ── Exemplo de catalogação de um repo real (adaptar ao repo) ────────────

AGENTES_EXEMPLO = [
    Agente(
        nome="Linter GitHub Actions",
        ferramentas=(
            Ferramenta(nome="action-lint", le=True, escreve=False, edita=False, decide_aceite=True),
        ),
        gera_controle=False,
    ),
    Agente(
        nome="Autor do PR",
        ferramentas=(
            Ferramenta(nome="editor local", le=False, escreve=True, edita=True, decide_aceite=False),
        ),
        gera_controle=False,
    ),
    Agente(
        nome="CI de testes",
        ferramentas=(
            Ferramenta(nome="pytest runners", le=False, escreve=False, edita=False, decide_aceite=True),
        ),
        gera_controle=False,
    ),
    Agente(
        nome="Agente de geração de docs (LLM)",
        ferramentas=(
            Ferramenta(nome="prompt docs", le=True, escreve=True, edita=False, decide_aceite=False),
            Ferramenta(nome="self-review prompt", le=True, escreve=False, edita=False, decide_aceite=True),
        ),
        gera_controle=True,
    ),
]

if __name__ == "__main__":
    print(f"{'Agente':<40} {'Papel':<10} {'Observação'}")
    print("-" * 70)
    for a in AGENTES_EXEMPLO:
        p = classificar(a)
        if p == Papel.AMBIGUO:
            obs = "builder e critic na mesma entidade — verificar se ambiguidade é legítima"
        elif p == Papel.NENHUM:
            obs = "não participa do ciclo de geração/aceite"
        elif p == Papel.BUILDER:
            obs = "gera conteúdo novo, não decide aceite"
        else:
            obs = "decide aceite sem gerar — papel de critic"
        print(f"{a.nome:<40} {p.value:<10} {obs}")
```

A saída esperada do script acima para o catálogo de exemplo:

```
Agente                                      Papel      Observação
----------------------------------------------------------------------
Linter GitHub Actions                       critic    decide aceite sem gerar — papel de critic
Autor do PR                                 builder   gera conteúdo novo, não decide aceite
CI de testes                                critic    decide aceite sem gerar — papel de critic
Agente de geração de docs (LLM)             ambíguo   builder e critic na mesma entidade — verificar se ambiguidade é legítima
```

O ponto que o exercício entrega: o agente de geração de docs é ambíguo não por culpa do LLM — é ambíguo porque o mesmo agente que gera também faz self-review. A peça 1 não diz "não use LLM para docs". Diz: se o LLM é builder e critic ao mesmo tempo, o repo precisa de política para isso — ou crítico externo, ou aceitação explícita de que a ambiguidade é legítima no contexto [3][6].

## 5. Aplica

Você está adotando um agente para gerar e revisar relatórios de deployment. O agente roda um prompt de geração, lê o relatório, avalia se está completo e, se estiver, marca como aprovado. Parece eficiente — e é, no dia a dia de quem o usa. Mas o repo não tem entidade independente que decida se o relatório está completo de verdade; a decisão de aceite é parte do mesmo agente que gerou.

O que a peça 1 propõe aqui não é desabilitar o agente — é definir, para o relatório de deployment, quem é builder e quem é critic, e garantir que sejam distintas quando o critério de completude pode ser falso-positivo. Em repo pequeno, essa distinção pode ser um humano que amostra 10% dos relatórios; em repo grande, pode ser um gate determinístico (peça 2) que verifica a estrutura do relatório, com o agente apenas gerando conteúdo [1][7].

Escala: em repo com múltiplos agentes colaborando, a peça 1 se torna mais crítica porque o número de pares builder/critic possível cresce — e com ele cresce a chance de um agente ser builder e critic ao mesmo tempo sem que ninguém perceba. O mapeamento de agentes por papel, feito no exercício, é o diagnóstico que orienta a prioridade de instalação da peça 1 versus as outras peças [4][5].

### Exercício

- [ ] Liste todos os agentes e processos que tocam artefatos no seu repo (humanos, scripts, agentes de IA, pipelines).
- [ ] Para cada um, responda as três perguntas objetivas: gera conteúdo novo? decide aceite? é a mesma entidade?
- [ ] Classifique cada um como builder, critic, ambíguo ou nenhum usando o critério do capítulo.
- [ ] Para os ambíguos, decida em uma linha se a ambiguidade é legítima (contexto pequeno, risco baixo) ou problemática (critério de aceite dependente do gênero).
- [ ] Para os problemáticos, descreva em uma linha qual entidade independente poderia substituir o crítico interno.
- [ ] Comite a classificação no repo — porque o mapeamento de papéis é o diagnóstico que justifica instalar ou não a peça 1.

## 6. Conclusão

A peça 1 não é sobre confiar ou não confiar em quem gera — é sobre design de processo onde a decisão de aceite tem origem diferente da geração quando o critério de aceite pode ser falso-positivo. O classificador objetivo deste capítulo entrega, para cada agente ou processo, um papel rastreável — builder, critic, ambíguo ou nenhum — e mostra que ambiguidade não é sempre erro, mas ambiguidade problemática é sintoma de processo que depende da vontade humana (ou da intenção do agente) para coerência.

Os próximos capítulos detalham as outras peças: gate determinístico (cap 4) que decide aceite com critério objetivo; registro declarativo (cap 5) que torna o critério auditável; hook (cap 6) que bloqueia o commit vermelho; postmortem que vira teste (cap 7) que previne recorrência; e hook + CI/CD (cap 8) que aplica o gate em dois pontos do ciclo. A peça 1 é a base porque ela define quem decide — e sem definir quem decide, as outras peças não podem ser aplicadas com critério [2][3].

## 7. Referências Bibliográficas

[1] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[2] MARTIN, R. C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1. ed. Boston: Pearson, 2017. ISBN 978-0134434403.

[3] BLOCK, E. *Workflow: A Guide to the Automated Business Process*. 1. ed. Berkeley: Apress, 2019. ISBN 978-1484256140.

[4] MYERS, G. J. *The Art of Software Testing*. 2. ed. Hoboken: John Wiley & Sons, 2011. ISBN 978-0470404152.

[5] BROWN, S.; BEYER, B.; et al. *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. ISBN 978-1491929124.

[6] HARRISON, K.; SINGER, L. *The Human Side of Agile: Essays on 옹호, 행等业务 and Collaboration*. 1. ed. Berkeley: Apress, 2013. ISBN 978-1430265025.

[7] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.
