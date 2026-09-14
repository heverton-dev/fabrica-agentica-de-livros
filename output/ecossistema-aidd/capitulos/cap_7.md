# Capítulo 7: Peça 5: Postmortem que vira teste

## 1. Introdução

O capítulo anterior mostrou que a peça 4 bloqueia o commit vermelho local — e que o hook é a primeira linha de defesa antes do commit. Mas há um tipo de risco que o hook não previne: incidente que já aconteceu, foi documentado em postmortem, e pode acontecer de novo porque o repo não tem teste que detecte a recorrência. Este capítulo entra na peça 5: postmortem que vira teste — cada linha de "Prevenção" nasce com um stub de teste de regressão, não só anotação arquivada [1][2].

Ao final deste capítulo você será capaz de, diante de um postmortem existente, transformar a linha de Prevenção em stub de teste executável — e saber quando o postmortem não deve virar teste (porque a causa não é detectável por teste automatizado).

## 2. Explica

Postmortem é o artefato que documenta o que aconteceu, por que aconteceu, e o que fazer para que não aconteça de novo. O problema não é que o postmortem seja inútil — é que, quando a "prevenção" vive apenas como texto arquivado, o repo não tem memória mecânica da prevenção. Memória textual é memória que depende de alguém ler e recordar — e recordar é o que falha sob pressão e rotatividade [3][4].

A peça 5 transforma a prevenção textual em prevenção mecânica: cada linha de "Prevenção" do postmortem é traduzida em um stub de teste de regressão que o repo pode executar. O stub não precisa ser teste completo — precisa ser teste que falhe se a condição de recorrência for detectável. Se a causa do incidente é detectável por teste, o stub é a prevenção mecânica; se a causa não é detectável por teste, o postmortem "prevenção" vira critério de crítico humano (peça 1) ou critério de gate (peça 2) [5][6].

Um erro comum: postmortem com prevenção genérica ("melhorar monitoramento", "revisar processo") sem condição objetiva. A prevenção genérica não pode virar stub de teste — porque não tem condição que o teste possa verificar. O critério de peça 5 é: prevenção com condição objetiva detectável = stub de teste; prevenção sem condição objetiva = prevenção textual (que deve ser critério de crítico humano ou gate, não só anotação) [1][7].

A ciclo de peça 5 é: incidente → postmortem → análise de prevenção → stub de teste → suíte detecta recorrência → postmortem é memória mecânica, não só textual. Quando o stub detecta recorrência, o incidente não volta a acontecer silenciosamente — o repo avisa que o mesmo problema voltou [2][3].

Métrica deste capítulo: número de stubs gerados no exercício — porque o número de stubs é o que mede a adoção real da peça 5, não a existência de postmortem arquivados.

## 3. Ilustra

Imagine um hospital onde cada incidente de qualidade é documentado em relatório arquivado — e a prevenção é "melhorar handoff de turno". O relatório existe, a prevenção está escrita, e o incidente pode acontecer de novo porque ninguém verificou se o handoff melhorou. Substituir a prevenção textual por checklist de handoff que o sistema registra — e teste que verifica se o checklist foi preenchido corretamente — transforma a prevenção em memória mecânica. Em repo, o stub de teste é o checklist: verifica se a condição de recorrência ainda é possível [4][5].

```mermaid
%% legenda: Postmortem que vira teste — prevenção textual vira stub de teste de regressão
flowchart TD
  A[Incidente] --> B[Postmortem: o que, por que, prevenção]
  B --> C{Análise: prevenção tem condição objetiva detectável?}
  C -->|sim| D[Stub de teste de regressão: falha se condição de recorrência]
  D --> E[Stub entra na suíte — repo executa]
  E --> F 스텁 detects recorrência?]
  F -->|sim| G[Repositório avisa que o mesmo problema voltou\npostmortem é memória mecânica]
  F -->|não| H[Recorrência não detectável pelo stub — prévia textual ou critério de gate/crítico]
  C -->|não| H
  D -.-> I[prevenção textual sem stub = memória que depende de recordação]
  H -.-> I
```

## 4. Técnica

A técnica da peça 5 é três passos: analisar o postmortem para identificar prevenção com condição objetiva; escrever o stub de teste que falha se a condição de recorrência for detectável; integrar o stub na suíte para que o repo execute. O conversor de postmortem para stub é o que acelera o processo — e o diagnóstico é o que decide se a prevenção deve virar stub ou permanecer textual [1][6].

### Molde de postmortem

```markdown
# Postmortem: [nome do incidente]

**Data do incidente:** DD/MM/AAAA
**Severidade:** [baixa / média / alta — definir critério do repo]
**Owner:** [quem conduziu o postmortem]

## O que aconteceu

[Descrição do incidente em texto — o que o usuário/observador viu]

## Por que aconteceu

[Causa raiz — rastreável. Se múltiplas causas, listar em ordem de impacto]

## O que foi feito imediatamente

[Ação de contenção ou correção imediata]

## Prevenção

- [ ] [condição objetiva] — stub: [descrição da condição que o teste deve verificar]
- [ ] [condição objetiva] — stub: [descrição]
- [ ] [prevenção textual — sem condição objetiva — critério de crítico humano ou gate]
```

O molde entrega, para cada prevenção, a pergunta de condição objetiva: "isso pode ser verificado por teste automatizado?" Se sim, stub; se não, textual com critério de crítico ou gate. O checkbox é o que torna a prevenção auditável — porque uma prevenção sem checkbox é prevenção que ninguém verificou se foi feita [3][7].

### Código: conversor de postmortem para stub de teste

```python
# postmortem_para_stub.py — converte postmortem em stub de teste de regressão
# Le postmortem (markdown) e gera stub de teste Python baseado nas prevenções com condição objetiva.
# Critério objetivo: prevenção com "stub:" gera stub; prevenção textual sem stub vira marcador de item manual.

import re
import sys
from pathlib import Path
from typing import TextIO

POSTMORTEM_STUB_HEADER = """\
# Stubs de teste gerados a partir de postmortem
# Gerado automaticamente por postmortem_para_stub.py
# Cada stub corresponde a uma prevenção com condição objetiva do postmortem.
# Stubs são ponto de partida — a completar com condição real de verificação.
"""

def parsear_prevenções(texto: str) -> list[dict]:
    """Parseia seções de prevenção de postmortem markdown.
    Espera formato: "- [ ] <descrição> — stub: <condição objetiva>"
    ou "- [ ] <descrição>" (prevenção textual sem stub).
    """
    prevenções: list[dict] = []
    # busca blocos de prevenção: lista com checkbox
    for m in re.finditer(r"^- \[ \] (.+?)(?: — stub: (.+))?$", texto, re.MULTILINE):
        descricao = m.group(1).strip()
        stub_condicao = m.group(2)
        if stub_condicao:
            prevenções.append({"tipo": "stub", "descricao": descricao, "condicao": stub_condicao})
        else:
            prevenções.append({"tipo": "textual", "descricao": descricao})
    return prevenções

def gerar_stub_python(nome_postmortem: str, prevenções: list[dict]) -> str:
    """Gera código Python de stub de teste (pytest) a partir das prevenções com stub.
    """
    linhas: list[str] = []
    linhas.append(f"def test_prevenção_{nome_postmortem}():")
    linhas.append('    """Stub de teste de regressão gerado a partir de postmortem."""')
    linhas.append("    # TODO: completar com condição real de verificação")
    linhas.append("    # Cada assert abaixo corresponde a uma prevenção do postmortem.")
    linhas.append("")
    for i, p in enumerate(prevenções, 1):
        if p["tipo"] == "stub":
            linhas.append(f"    # Prevenção {i}: {p['descricao']}")
            linhas.append(f"    # Condição objetiva: {p['condicao']}")
            linhas.append(f"    # assert <condição real>, \"Prevenção {i} não verificada\"")
            linhas.append("")
    if not any(p["tipo"] == "stub" for p in prevenções):
        linhas.append("    pass  # nenhuma prevenção com condição objetiva no postmortem")
    else:
        linhas.append("    # Stubs acima: completar antes de mergear")
    return "\n".join(linhas)

def gerar_marcadores_textuais(nome_postmortem: str, prevenções: list[dict]) -> str:
    """Gera lista de marcadores de prevenção textual para rastreamento manual.
    """
    linhas: list[str] = []
    linhas.append("# Prevenções textuais (sem condição objetiva) — rastrear manualmente")
    for i, p in enumerate(prevenções, 1):
        if p["tipo"] == "textual":
            linhas.append(f"# - [?] {p['descrição']} — critério de crítico humano ou gate")
    return "\n".join(linhas)

def processar_postmortem(caminho: Path, saida: TextIO | None = None) -> int:
    """Processa um arquivo de postmortem markdown e gera stub + marcadores.
    """
    if not caminho.exists():
        print(f"ERRO: {caminho} não existe", file=sys.stderr)
        return 2
    texto = caminho.read_text(encoding="utf-8")
    nome = caminho.stem
    prevenções = parsear_prevenções(texto)
    if not prevenções:
        print(f"AVISO: {caminho} não tem prevenções no formato esperado — verificar molde", file=sys.stderr)
        return 1
    stubs = [p for p in prevenções if p["tipo"] == "stub"]
    textuais = [p for p in prevenções if p["tipo"] == "textual"]
    print(f"Postmortem: {nome}")
    print(f"Prevenções totais: {len(prevenções)}")
    print(f"Prevenções com stub (gerar teste): {len(stubs)}")
    print(f"Prevenções textuais (rastrear manual): {len(textuais)}")
    saida = saida or sys.stdout
    saida.write(POSTMORTEM_STUB_HEADER)
    saida.write(f"# Postmortem: {nome}\n\n")
    saida.write(gerar_stub_python(nome, prevenções))
    saida.write("\n\n")
    if textuais:
        saida.write(gerar_marcadores_textuais(nome, prevenções))
        saida.write("\n")
    return 0

def main(caminhos: list[str]) -> int:
    if not caminhos:
        print("Uso: python postmortem_para_stub.py <caminho-do-postmortem.md> [saída.py]", file=sys.stderr)
        return 2
    saida: TextIO | None = None
    primeiro = True
    for cp in caminhos:
        caminho = Path(cp)
        if caminho.suffix == ".py":
            if saida is not None:
                print("AVISO: segunda saída .py ignorada — concatenando no mesmo arquivo", file=sys.stderr)
            continue
        saida = open(caminho.with_suffix("") + "_stubs.py", "w", encoding="utf-8") if primeiro else saida
        if not primeiro:
            # reabre para concatenar se houver múltiplos
            saida = open(caminho.with_suffix("") + "_stubs.py", "a", encoding="utf-8")
        codigo = processar_postmortem(caminho, saida)
        saida.flush()
        if codigo not in (0, 1):
            return codigo
        primeiro = False
    if saida and not caminhos[0].endswith(".py"):
        saida.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

O conversor entrega, para um postmortem com prevenções com stub, um arquivo `_stubs.py` com teste de regressão que o desenvolvedor completa com a condição real. O conversor também lista as prevenções textuais para rastreamento manual — porque a peça 5 não ignora prevenção textual, ela decide onde ela pertence: manual (crítico humano ou gate) ou stub [2][5].

### Exemplo de postmortem fictício e stub gerado

Postmortem fictício (simplificado):

```markdown
# Postmortem: Configuração de agente sem chave ambiente

**Data do incidente:** 12/08/2026
**Severidade:** média
**Owner:** time-qa

## O que aconteceu

Um agente de geração subiu configuração sem a chave de ambiente obrigatória. O agente não detectou a ausência porque o gate de configuração (peça 2) não verificava presença de chave ambiente para tipo "agente-generico" — critério ausente do registro (peça 3).

## Por que aconteceu

Causa raiz: chave "ambiente" não estava na lista de chaves obrigatórias do registro para tipo "agente-generico" — o gate (peça 2) lê o registro e não verificou porque o registro não declarava a chave.

## O que foi feito imediatamente

Adicionado chave "ambiente" ao registro para tipo "agente-generico" e rodado gate em modo dry-run — 8 configurações sem chave ambiente detectadas, corrigidas.

## Prevenção

- [ ] chave "ambiente" presente no registro para todo tipo que o agente pode gerar — stub: validar que todo tipo no registro tem "ambiente" em chaves_obrigatorias
- [ ] gate lê registro e verifica chaves obrigatórias — stub: validar que gate está verificando as chaves declaradas no registro
- [ ] revisão de configuração por crítico humano antes de merge em tipos novos — critério de crítico humano (peça 1)
```

Stub gerado pelo conversor:

```python
# Stubs de teste gerados a partir de postmortem
# Gerado automaticamente por postmortem_para_stub.py
# Cada stub corresponde a uma prevenção com condição objetiva do postmortem.
# Stubs são ponto de partida — a completar com condição real de verificação.

def test_prevenção_configuracao_sem_chave_ambiente():
    """Stub de teste de regressão gerado a partir de postmortem."""
    # TODO: completar com condição real de verificação
    # Cada assert abaixo corresponde a uma prevenção do postmortem.

    # Prevenção 1: chave "ambiente" presente no registro para todo tipo que o agente pode gerar
    # Condição objetiva: validar que todo tipo no registro tem "ambiente" em chaves_obrigatorias
    # assert <condição real>, "Prevenção 1 não verificada"

    # Prevenção 2: gate lê registro e verifica chaves obrigatórias
    # Condição objetiva: validar que gate está verificando as chaves declaradas no registro
    # assert <condição real>, "Prevenção 2 não verificada"

    # Stubs acima: completar antes de mergear
```

A propriedade que o stub entrega: se alguém remove "ambiente" do registro para um tipo, o stub pode ser completado para falhar — e o repo detecta a recorrência do incidente antes que alcance produção [1][7].

## 5. Aplica

Você tem um postmortem arquivado de um incidente de configuração sem chave obrigatória — e o postmortem tem prevenção textual "melhorar gate de configuração". A peça 5 não ignora a prevenção textual — analisa se ela tem condição objetiva detectável. Se a condição é "todo tipo no registro tem chaves obrigatórias", o stub é verificar isso. Se a condição é "crítico humano revisa", o stub não aplica — e a prevenção vira critério de peça 1 (crítico humano com papel definido) [3][6].

Um cenário real de instituição: time com 5 postmortems arquivados, nenhum com stub. O exercício deste capítulo gera, para cada postmortem, a análise de prevenção — quantas prevenções têm condição objetiva, quantas são textuais. O resultado orienta a prioridade de stub: prevenções com condição objetiva primeiro, porque são as que o repo pode executar; textuais viram critério de crítico ou gate, com papel definido pela peça 1 e gate da peça 2 [2][4].

Escala: em repo com múltiplos incidentes e múltiplos agentes, o postmortem vira teste é o que transforma o repositório em memória mecânica de incidentes — e o repo avisa quando o mesmo problema tenta voltar. Sem stub, o postmortem é memória que depende de recordação — e recordação é o que falha sob pressão e rotatividade [1][7].

### Exercício

- [ ] Liste todos os postmortems arquivados do seu repo (ou incidentes documentados em qualquer formato).
- [ ] Defina o limite de stub: gerar stub apenas para prevenções com condição objetiva detectável em até 3 condições por postmortem — prevenções com mais de 3 condições podem exigir módulo de teste dedicado, não stub simples (limite prático do conversor).
- [ ] Defina o contorno de stub: stub não substitui teste completo de regressão — é ponto de partida para ser completado com a condição real de verificação antes de mergear; stub não testado não previne recorrência.
- [ ] Para cada postmortem, aplique o molde de prevenção: converter cada prevenção em condição objetiva (stub) ou textual (sem stub).
- [ ] Para as prevenções com condição objetiva, gere o stub de teste com o conversor de postmortem para stub.
- [ ] Para as prevenções textuais, decida em uma linha: critério de crítico humano (peça 1) ou critério de gate (peça 2) — e descreva a condição.
- [ ] Comite os stubs gerados na suíte do repo — porque o stub é a memória mecânica do postmortem, e a suíte que executa é o que detecta recorrência.
- [ ] Comite o relatório de análise de prevenção — porque o relatório é o que justifica quais prevenções viraram stub e quais permaneceram textuais.

## 6. Conclusão

A peça 5 é postmortem que vira teste — cada linha de prevenção com condição objetiva nasce com stub de teste de regressão, não só anotação arquivada. A peça não propõe stub para toda prevenção — propõe stub para prevenção com condição objetiva detectável, e deixa prevenção textual para critério de crítico humano (peça 1) ou gate (peça 2), com papel definido pelas peças anteriores. O conversor de postmortem para stub é o que acelera o processo — e o diagnóstico de prevenção é o que decide a classificação. Os próximos capítulos detalham as outras peças: hook + CI/CD (cap 8). A peça 5 é a memória mecânica do repo — sem ela, o postmortem é memória que depende de recordação [3][5].

## 7. Referências Bibliográficas

[1] BROWN, S.; BEYER, B.; et al. *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol: O'Reilly Media, 2016. ISBN 978-1491929124.

[2] GOOGLE SRE. *Postmortem Culture: Learning from Failure*. In: *Site Reliability Engineering*. Disponível em: https://sre.google/sre-book/postmortem-culture/. Acesso em: 09 set. 2026.

[3] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[4] MYERS, G. J. *The Art of Software Testing*. 2. ed. Hoboken: John Wiley & Sons, 2011. ISBN 978-0470404152.

[5] FOWLER, M. *Continuous Integration*. 2001. Disponível em: https://martinfowler.com/articles/continuousIntegration.html. Acesso em: 09 set. 2026.

[6] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.

[7] BLOCK, E. *Workflow: A Guide to the Automated Business Process*. 1. ed. Berkeley: Apress, 2019. ISBN 978-1484256140.
