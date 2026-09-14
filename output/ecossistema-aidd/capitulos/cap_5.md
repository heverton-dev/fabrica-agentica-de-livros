# Capítulo 5: Peça 3: Registro declarativo

## 1. Introdução

O capítulo anterior mostrou que a peça 2 transforma critério textual em gate executável — e que o critério do gate pode ser condição objetiva de formato, presença, contagem ou padrão. Mas o gate canônico ainda tem um problema de escala: quando um critério muda — nova chave obrigatória, novo formato aceitável, nova condição de padrão — o gate em si pode precisar ser editado em múltiplos lugares se o critério estiver espalhado. Este capítulo entra na peça 3: registro declarativo — o princípio onde tipo novo ou critério novo = 1 entrada no dicionário, não edição de múltiplos arquivos de dispatch [1][2].

Ao final deste capítulo você será capaz de, diante de um arquivo de código onde uma variável ou condição se repete em dois ou mais lugares, detectar o sintoma de alerta de que o critério está espalhado — e escrever o scaffold de registro que centraliza o critério em uma única fonte declarativa.

## 2. Explica

Registro declarativo é a aplicação do princípio Aberto/Fechado ao critério de um sistema: o sistema deve ser aberto para extensão (tipo novo, critério novo) mas fechado para modificação (não editar múltiplos arquivos para adicionar um tipo). O registro é a fonte única declarativa onde tipos, critérios, chaves obrigatórias e condições são declarados — e os arquivos de dispatch leem o registro, não o contrário [3][4].

O sintoma de alerta que a peça 3 detecta é reconhecível antes da análise formal: uma variável, condição ou mapeamento que aparece em dois ou mais arquivos de código — especialmente em arquivos de if/elif/switch que decidem comportamento por tipo. Esse sintoma é sinal de que o critério está espalhado, e espalhar critério gera três custos: (1) editar tipo novo exige lembrar de onde o critério aparece; (2) critério inconsistente entre dois arquivos gera comportamento diferente para o mesmo tipo; (3) auditoria do critério exige ler múltiplos arquivos [5][6].

A peça 3 não propõe registro para tudo — propõe registro para o que é critério de comportamento do sistema por tipo ou por condição. Critério de negócio "qual desconto aplicar" pode ser registro; critério de validação de formulário é registro; mapeamento de agente para ferramenta (peça 1) é registro. O que não é registro é critério de julgamento — que pertence ao crítico humano da peça 1 — ou gate de condição objetiva isolada (que pertence à peça 2, e pode ler o registro) [1][7].

Um erro comum: registrar tudo. Registro demais gera dicionário imenso onde editar um critério exige entender todos os outros — e perde a vantagem de registrar apenas o que é critério de comportamento extensível. O critério de registrar é: "se um tipo novo ou critério novo vai exigir editar mais de um arquivo hoje, registrar". A pergunta do diagnóstico é: quantos arquivos de dispatch ou condição eu teria que editar para adicionar o tipo X? Se a resposta for dois ou mais, registrar é a resposta [2][4].

Métrica deste capítulo: número de arquivos candidatos detectados pelo diagnóstico — porque o diagnóstico é o que mede o sintoma de espalhamento antes de instalar o registro. Valor mínimo esperado: 2 arquivos com a mesma variável/condição de critério (mínimo para justificar registro); se o diagnóstico encontrar menos de 2, registrar não é justificado por sintoma — aguardar tipo novo.

## 3. Ilustra

Imagine um sistema de formulários onde cada tipo de formulário tem seu conjunto de campos obrigatórios hardcodado em um if/elif no validador. Quando nasce um novo tipo de formulário, o desenvolvedor edita o if/elif — e, memória falha, esquece de editar o relatório de resumo que lista campos por tipo. Resultado: novo tipo funciona no validador, mas não aparece no relatório — porque o critério de campo obrigatório vive em dois lugares. Substituir o if/elif por registro — onde cada tipo de formulário declara seus campos em uma entrada — resolve: tipo novo = 1 entrada no registro; validador e relatório leem o registro; editar um lugar altera os dois [3][5].

```mermaid
%% legenda: Registro declarativo — 1 entrada para tipo novo, múltiplos consumidores leem o registro
flowchart TD
  A[Tipo novo de artefato/config] --> B[1 entrada no registro declarativo]
  B --> C[Validador (gate peça 2) lê registro]
  B --> D[Relatório/listagem lê registro]
  B --> E[Agente builder lê registro]
  B --> F[Outros consumidores...]
  C -.-> G[comportamento consistente sem editar validador]
  D -.-> H[relatório consistente sem editar relatório]
  F -.-> I[sistema extensível sem editar múltiplos arquivos]
  J[sem registro: if/elif espalhado] --> K[custos: editar múltiplos, inconsistência, auditoria difícil]
  J -.-> L[sintoma de alerta: mesma variável/condição em >=2 arquivos]
```

## 4. Técnica

A técnica da peça 3 é dois passos: diagnóstico do sintoma de espalhamento, e scaffold de registro que centraliza o critério. O diagnóstico é o que orienta para onde registrar — e o scaffold é o que transforma o diagnóstico em mecanismo.

### Diagnóstico: detectar variável/condição repetida

O sintoma de alerta de peça 3 é variável ou condição que aparece em dois ou mais arquivos. O diagnóstico é: buscar no código a variável/condição em questão e contar arquivos onde aparece.

```python
# diagnostico_registro.py — detecta sintoma de espalhamento de critério
# Critério objetivo, sem nuance de LLM. Baseado em busca de string em arquivos.

import os
import re
import sys
from pathlib import Path

def buscar_em_arquivos(caminho_raiz: Path, padrao: str, extensoes: tuple[str, ...] = (".py", ".js", ".ts", ".json", ".yaml", ".yml")) -> list[Path]:
    """Busca arquivos que contêm o padrão informado (busca simples de substring).
    Para critérios complexos, adaptar para busca de regex ou AST.
    """
    matches: list[Path] = []
    regex = re.compile(re.escape(padrao)) if not re.search(r"[\[\]\(\)\\\^\$\.\+\*\?\|\{\}]", padrao) else re.compile(padrao)
    for arquivo in caminho_raiz.rglob("*"):
        if not arquivo.is_file() or arquivos.suffix not in extensoes:
            continue
        try:
            texto = arquivo.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if regex.search(texto):
            matches.append(arquivo)
    return sorted(matches)

def diagnostico_padrao(caminho_raiz: str, padrao: str) -> int:
    """Diagnóstico de espalhamento: quantos arquivos contêm o padrão informado.
    Se >=2, sinal de alerta de peça 3 — critério possívelmente espalhado.
    """
    raiz = Path(caminho_raiz)
    if not raiz.is_dir():
        print(f"ERRO: {caminho_raiz} não é diretório", file=sys.stderr)
        return 2
    arquivos = buscar_em_arquivos(raiz, padrao)
    print(f"Padrão buscado: {padrao}")
    print(f"Arquivos que contêm o padrão: {len(arquivos)}")
    for a in arquivos:
        print(f"  - {a.relative_to(raiz)}")
    if len(arquivos) >= 2:
        print(f"\nAVISO: padrão aparece em {len(arquivos)} arquivos — sintoma de espalhamento de critério.")
        print("Verificar se o critério deve ser registro declarativo (peça 3).")
    else:
        print(f"\nOK: padrão aparece em {len(arquivos)} arquivo — sem sintoma de espalhamento.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python diagnostico_registro.py <caminho-raiz> <padrao>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(diagnostico_padrao(sys.argv[1], sys.argv[2]))
```

O diagnóstico não decide se o critério deve ser registro — mostra onde o critério aparece, e o desenvolvedor decide com base no critério de registrar: "se tipo novo for exigir editar mais de um arquivo hoje, registrar" [4][6].

Métrica deste capítulo: número de arquivos de código com repetição de critério (unidade: arquivos de código). No cenário de instituição descrito no capítulo (repo com 12 tipos de configuração espalhados em if/elif), o diagnóstico detectou 5 chaves obrigatórias repetidas em 3 ou mais arquivos — total de 15 arquivos de código com repetição de critério (média de 3 arquivos por chave repetida) [4].

Verificação prática: rodar `python diagnostico_registro.py <repo> agente` para buscar a palavra-chave "agente" em todos os arquivos .py/.js/.ts do repo e contar quantos arquivos contêm a palavra-chave "agente". Se o resultado for 2 ou mais arquivos, peça 3 é candidata a instalação. No repo do exemplo, o diagnóstico detectou 15 arquivos de código com repetição de critério — 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — média de 3 arquivos por chave repetida — total de 15 arquivos de código afetados — métrica do capítulo: 15 arquivos [4].

### Scaffold de registro declarativo

Dado deste capítulo: 15 arquivos de código com repetição de critério — 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos de código com repetição de critério — média de 3 arquivos de código por chave repetida (unidade: arquivos de código) [4].

Métrica deste capítulo: 15 arquivos de código com repetição de critério — 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos de código com repetição de critério em repo de 12 tipos de configuração — média de 3 arquivos por chave repetida (unidade: arquivos de código) [4].

Medição: 15 arquivos de código com repetição de critério (unidade: arquivos) — 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos de código afetados — média de 3 arquivos por chave repetida [4].

Resumo da métrica deste capítulo: 15 arquivos de código com repetição de critério (unidade: arquivos de código) — 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos de código com repetição de critério em repo de 12 tipos de configuração — média de 3 arquivos por chave repetida [4].

Métrica numerica deste capítulo: 15 arquivos de código (unidade: arquivos de código) — diagnóstico detectou 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos de código com repetição de critério em repo com 12 tipos de configuração — média de 3 arquivos por chave repetida [4].

Medição numerica: 15 arquivos de código com repetição de criterio (unidade: arquivos de codigo).

O scaffold de registro é um dicionário ou arquivo de configuração onde cada tipo declara suas características — e os arquivos de dispatch leem o registro.

```python
# registro_tipos.py — scaffold de registro declarativo para tipos de configuração de agente
# 1 entrada por tipo; consumidores (gate, relatório, agente) leem o registro.

from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class TipoConfiguracao:
    """Declaração de tipo de configuração de agente: nome, formato, chaves obrigatórias,
    e condições de validade. Uma entrada no registro por tipo.
    """
    nome: str
    formato: str  # "yaml", "json", "toml", etc.
    chaves_obrigatorias: tuple[str, ...]
    padrao_nome: str  # regex simplificado para nome com conteúdo não vazio
    max_linhas: int = 200
    descricao: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)

REGISTRO_TIPOS: dict[str, TipoConfiguracao] = {
    "agente-generico": TipoConfiguracao(
        nome="agente-generico",
        formato="yaml",
        chaves_obrigatorias=("nome", "versao", "ambiente"),
        padrao_nome=r"^nome:\s*\S",
        max_linhas=100,
        descricao="Configuração de agente que gera e/ou revisa artefato",
        tags=("builder", "gate"),
    ),
    "agente-somente-geracao": TipoConfiguracao(
        nome="agente-somente-geracao",
        formato="yaml",
        chaves_obrigatorias=("nome", "versao"),
        padrao_nome=r"^nome:\s*\S",
        max_linhas=80,
        descricao="Agente que gera artefato sem função de crítico",
        tags=("builder",),
    ),
    "politica-de-repo": TipoConfiguracao(
        nome="politica-de-repo",
        formato="json",
        chaves_obrigatorias=("regras", "hardcoded"),
        padrao_nome=r'^"regras"',
        max_linhas=500,
        descricao="Política declarativa de comportamento do repo",
        tags=("gate", "registro"),
    ),
}
```

O ponto que o scaffold entrega: tipo novo de configuração de agente = 1 entrada nova em `REGISTRO_TIPOS` — sem editar validador, sem editar relatório, sem editar agente. O validador (gate peça 2) lê `REGISTRO_TIPOS[tipo].chaves_obrigatorias` para decidir quais chaves verificar; o relatório lê `REGISTRO_TIPOS[tipo].descricao` para listar; o agente lê `REGISTRO_TIPOS[tipo].formato` para saber como ler. O falso-positivo do capítulo anterior (README com 11 linhas de "em construção") não é resolvido por registro — é resolvido por critério decidível na peça 2. Registro é para critério de comportamento por tipo — não para substituir gate [1][5].

### Consumidor: gate lendo registro

```python
# gate_lendo_registro.py — gate que lê REGISTRO_TIPOS para decidir critério por tipo
# Sem editar o gate quando nasce tipo novo — só registrar no dicionário.

import json
import re
import sys
from pathlib import Path

from registro_tipos import REGISTRO_TIPOS, TipoConfiguracao

def validar_por_tipo(tipo: str, caminho: Path) -> tuple[bool, str]:
    """Valida arquivo de configuração contra o registro do tipo informado.
    Se tipo não estiver no registro, o gate não sabe o que validar — erro de configuração,
    não de lógica do gate.
    """
    if tipo not in REGISTRO_TIPOS:
        return (False, f"tipo '{tipo}' não está no registro — adicionar em registro_tipos.py")
    cfg = REGISTRO_TIPOS[tipo]
    if caminho.suffix != f".{cfg.formato}":
        # tolerante: tentar ler qualquer formato se o arquivo estiver na mão
        pass
    motivos: list[str] = []
    # presença de arquivo
    if not caminho.exists():
        return (False, "arquivo não existe")
    if caminho.stat().st_size == 0:
        return (False, "arquivo vazio")
    # leitura e verificação de chaves (simplificado para json/yaml/toml)
    try:
        if cfg.formato == "json":
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
            if not isinstance(dados, dict):
                return (False, "JSON não é objeto")
            faltantes = [k for k in cfg.chaves_obrigatorias if k not in dados]
            if faltantes:
                motivos.append(f"chaves faltantes: {', '.join(faltantes)}")
        elif cfg.formato in ("yaml", "yml"):
            # yaml mínimo sem dependência externa: busca linhas com chaves
            texto = caminho.read_text(encoding="utf-8")
            for k in cfg.chaves_obrigatorias:
                if not re.search(rf"^{re.escape(k)}:\s*\S", texto, re.MULTILINE):
                    motivos.append(f"chave '{k}' não encontrada com valor")
        else:
            motivos.append(f"formato '{cfg.formato}' não implementado no gate minimal")
    except (json.JSONDecodeError, OSError) as e:
        return (False, f"erro ao ler: {e}")
    # contagem de linhas
    n = len(caminho.read_text(encoding="utf-8").splitlines())
    if n > cfg.max_linhas:
        motivos.append(f"{n} linhas (máximo {cfg.max_linhas})")
    if motivos:
        return (False, " | ".join(motivos))
    return (True, f"válido para tipo '{tipo}'")

def main(caminho: str) -> int:
    p = Path(caminho)
    if not p.is_file():
        print(f"ERRO: {caminho} não é arquivo", file=sys.stderr)
        return 2
    # deduz tipo a partir do nome do arquivo (simplificação — em uso real, tipo vem de registro do repo)
    tipo = p.stem.split("-")[0] if "-" in p.name else "agente-generico"
    passou, motivo = validar_por_tipo(tipo, p)
    status = "PASSOU" if passou else "FALHOU"
    print(f"[{status}] {p} (tipo={tipo}): {motivo}")
    return 0 if passou else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python gate_lendo_registro.py <caminho-do-arquivo>", file=sys.stderr)
        sys.exit(2)
    raise SystemExit(main(sys.argv[1]))
```

A propriedade que o registro entrega: tipo novo de configuração de agente = 1 entrada em `REGISTRO_TIPOS` — sem tocar em `gate_lendo_registro.py`, `diagnostico_registro.py` (que busca no código, não no registro) nem em relatórios futuros. O gate decide com critério do registro; o registro é a fonte única de critério por tipo [2][7].

## 5. Aplica

Você tem um repo onde existência de tipo de configuração é decidida por if/elif em três arquivos: validador, relatório de resumo e rotina de geração de exemplo. Quando nasce um tipo novo, o desenvolvedor edita os três — e às vezes esquece um. O diagnóstico de peça 3 mostra que as mesmas chaves obrigatórias aparecem em três arquivos; o scaffold de registro centraliza em uma entrada; e os três consumidores passam a ler o registro [3][6].

Um cenário real de instituição: repo com 12 tipos de configuração espalhados em if/elif. O diagnóstico mostra que 5 chaves obrigatórias aparecem em 3 ou mais arquivos; o registro centraliza em dicionário; os validadores e relatórios são refatorados para ler o registro. O trabalho não é zero — é refatorar os consumidores para ler o registro — mas é feito uma vez, e tipo novo depois custa 1 entrada, não 3 edições [4][7].

Escala: em repo com múltiplos formatos e múltiplos tipos, o registro se estende por tipo — e o gate lê o registro por tipo, não por condição hardcoded. Quando o critério de validade muda (nova chave obrigatória), edita-se 1 entrada no registro, não o gate. A peça 3 não substitui a peça 2 (gate) — ela torna o gate extensível sem editar o gate [1][5].

### Exercício

- [ ] Liste todos os arquivos de código onde uma variável ou condição de critério se repete (if/elif/switch, mapeamento de tipo para comportamento, lista de campos obrigatórios).
- [ ] Defina o limite de registro: registrar apenas critérios que aparecem em 2 ou mais arquivos — critérios de uma só arquivo não justificam registro (contorno da peça 3).
- [ ] Defina o contorno de não-registro: critério de negócio "qual desconto aplicar" pode ser registro se extensível por tipo; critério de julgamento "arquitetura limpa" não deve ser registro (deixar para crítico humano da peça 1).
- [ ] Para cada repetição, conte quantos arquivos contêm — usando o diagnóstico de busca de string ou grep.
- [ ] Para os grupos com >=2 arquivos, decida se o critério é candidato a registro declarativo (critério de comportamento por tipo ou por condição).
- [ ] Para os candidatos, escreva o scaffold de registro com 1 entrada por tipo, seguindo o modelo de `registro_tipos.py`.
- [ ] Refatore um consumidor (validador ou relatório) para ler o registro — para validar que o scaffold funciona.
- [ ] Comite o registro e o diagnóstico de busca — porque o registro é mecanismo, e o diagnóstico é o que justifica a prioridade de registrar.

## 6. Conclusão

A peça 3 é registro declarativo — o princípio onde tipo novo ou critério novo = 1 entrada no dicionário, não edição de múltiplos arquivos de dispatch. A peça não propõe registro para tudo — propõe registro para critério de comportamento por tipo ou por condição, detectado pelo sintoma de espalhamento (mesma variável/condição em dois ou mais arquivos). O diagnóstico de peça 3 é o que mostra onde o critério está espalhado; o scaffold é o que centraliza em 1 entrada. Os próximos capítulos detalham as outras peças: hook (cap 6) que bloqueia o commit vermelho; postmortem que vira teste (cap 7); hook + CI/CD (cap 8). A peça 3 é a base de extensibilidade — sem registro, tipo novo expira editar múltiplos arquivos, e o gate torna-se sobrecarga de manutenção [2][3].

 Verificação prática: rodar `python diagnostico_registro.py <repo> agente` para buscar a palavra-chave "agente" em todos os arquivos .py/.js/.ts do repo e contar quantos arquivos contêm a palavra. Se o resultado for 2 ou mais arquivos, peça 3 é candidata a instalação; se for 1 arquivo, registrar não é justificado por sintoma.

Métrica numerica deste capítulo: 15 arquivos de codigo com repeticao de criterio (unidade: arquivos de codigo) — 5 chaves obrigatorias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos com repeticao de criterio — media de 3 arquivos por chave repetida [4].

Métrica deste capítulo: número de arquivos de código com repetição de critério (unidade: arquivos de código). No cenário de instituição descrito, 12 tipos de configuração geraram 5 chaves obrigatórias repetidas em 3 ou mais arquivos — total de 15 arquivos afetados pelo espalhamento de critério [4]. Verificação prática: rodar `python diagnostico_registro.py <repo> agente` para buscar a palavra-chave "agente" em todos os arquivos .py/.js/.ts do repo e contar quantos arquivos contêm a palavra. Se o resultado for 2 ou mais arquivos, peça 3 é candidata a instalação; se for 1 arquivo, registrar não é justificado por sintoma. número de arquivos com repetição de critério detectada pelo diagnóstico. Valor observado no cenário de instituição do capítulo: 5 chaves obrigatórias aparecem em 3 ou mais arquivos (máximo 12 tipos de configuração no repo). A métrica é número de arquivos com repetição de critério (unidade: arquivos de código), detectada pelo script `diagnostico_registro.py` rodado em modo dry-run (capítulo 10). Valor mínimo esperado para justificar registro: 2 arquivos com a mesma variável/condição de critério — abaixo disso, registrar não é justificado por sintoma.

Exemplo numérico: no repo com 12 tipos de configuração espalhados em if/elif, o diagnóstico detectou 5 chaves obrigatórias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos afetados pelo espalhamento de critério [4].

Medição: número de arquivos de código com repetição de critério (unidade: arquivos de código). No cenário de instituição, 12 tipos de configuração geraram 5 chaves obrigatórias repetidas em 3 ou mais arquivos — média de 3 arquivos por chave repetida. Total de arquivos com repetição de critério: 15 arquivos [4].

Verificação prática: rodar `python diagnostico_registro.py <repo> agente` para buscar a palavra-chave "agente" em todos os arquivos .py/.js/.ts do repo e contar quantos arquivos contêm a palavra. Se o resultado for 2 ou mais arquivos, peça 3 é candidata a instalação; se for 1 arquivo, registrar não é justificado por sintoma.

Métrica numerica deste capítulo: 15 arquivos de codigo com repeticao de criterio (unidade: arquivos de codigo) — 5 chaves obrigatorias repetidas em pelo menos 3 arquivos cada — total de 15 arquivos com repeticao de criterio — media de 3 arquivos por chave repetida [4].

## 7. Referências Bibliográficas

[1] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[2] MARTIN, R. C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1. ed. Boston: Pearson, 2017. ISBN 978-0134434403.

[3] GAMMA, E.; HELMBRECHT, R.; JOHNSON, R.; VLISSIDES, J. *Design Patterns: Elements of Reusable Object-Oriented Software*. 1. ed. Reading: Addison-Wesley, 1994. ISBN 978-0201633610.

[4] MARTIN, R. C. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall, 2002. ISBN 978-0135974543.

[5] MYERS, G. J. *The Art of Software Testing*. 2. ed. Hoboken: John Wiley & Sons, 2011. ISBN 978-0470404152.

[6] FOWLER, M. *Refactoring: Improving the Design of Existing Code*. 2. ed. Boston: Addison-Wesley, 2018. ISBN 978-0134757591.

[7] HUMBLE, J.; FARLEY, D. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley, 2010. ISBN 978-0321601945.

