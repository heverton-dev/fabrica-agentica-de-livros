#!/usr/bin/env python3
"""
Política de aplicação INVIOLÁVEL da regra HUB POR COLEÇÃO.

Proposta de integração em 5 pontos de validação + hardening de dir_obra():

1. dir_obra() — adiciona modo 'escrita' que força hub (nunca retorna plano)
2. parametros_obra.py — valida que config vem de hub
3. auditar-obra.py — gate pré-compilação testa estrutura
4. pre-commit hook — valida antes de aceitar commit
5. empacotar-colecao.py — rejeita estrutura não conforme

Uso:
    python scripts/aplicar-politica-hub.py --diagrama       # gera diagrama de integração
    python scripts/aplicar-politica-hub.py --codigo         # exibe código das mudanças
"""

import argparse
import sys

# ──────────────────────────────────────────────────────────────────────────
# DIAGNÓSTICO DAS RAÍZES
# ──────────────────────────────────────────────────────────────────────────

RAIZ_PROBLEMA = """
RAIZ DO PROBLEMA: dir_obra() foi desenhada para SUPORTAR layout plano como fallback

Linha 576 de tipos_obra.py:
    '''Quando nada existe, devolve o caminho plano (fallback de escrita).'''

Código (linhas 584-621):
    direto = base / slug
    if direto.exists():
        return direto
    # ... procura em hubs ...
    return direto  # ← FALLBACK PLANO (lines 612, 621)

CONSEQUÊNCIA:
- Qualquer script que chama dir_obra(slug) e depois grava um arquivo
  pode SILENCIOSAMENTE criar estrutura plana se o slug não existir no hub.
- Exemplo: esbocar.py cria config_obra.json via dir_obra("tema");
  se "tema" não existe, cria output/livros/tema/ (plano).
"""

# ──────────────────────────────────────────────────────────────────────────
# PROVEDORES (SCRIPTS QUE USAM dir_obra())
# ──────────────────────────────────────────────────────────────────────────

PROVEDORES = """
176 chamadas para dir_obra() em scripts/:

RISCO ALTO (criam caminhos de escrita):
  - auditar-obra.py:686 — lê/escreve em dir_livro
  - parametros_obra.py:127 — lê config_obra.json via dir_obra()
  - campanha.py:372-526 — lê/escreve manifesto e config
  - compilar-referencias.py:133 — escreve referencias_compiladas.md
  - fatiar-obra.py — escreve arquivos de derivado
  - minerar-fontes-academicas.py — escreve dossie de pesquisa

RISCO MÉDIO (leem da escrita anterior):
  - colecao.py:194-222 — lê config/sumario de dir_obra()
  - gerar-capa.py — lê config_obra.json
  - validar-*.py — leem de dir_obra()

INTENÇÃO ORIGINAL (plano estava documentado):
  - Ambos os layouts (plano e hub) foram deliberadamente suportados
  - CLAUDE.md V5 MUDOU A REGRA para "HUB POR COLEÇÃO" (layout plano agora proibido)
  - Mas dir_obra() não foi reescrito para impor a nova regra
"""

# ──────────────────────────────────────────────────────────────────────────
# CÓDIGO DAS MUDANÇAS PROPOSTAS
# ──────────────────────────────────────────────────────────────────────────

MUDANCA_TIPO_OBRA = """
MUDANÇA 1: tipos_obra.py — adicionar modo 'escrita' ao dir_obra()

Assinatura nova:
    def dir_obra(slug, base=None, modo='leitura'):
        '''
        modo='leitura'  — compatível com código atual (busca em hubs, fallback plano OK)
        modo='escrita'  — INVIOLÁVEL (rejeita plano, força hub ou levanta erro)
        '''

Implementação (pseudocódigo):

def dir_obra(slug, base=None, modo='leitura'):
    base = Path(base) if base is not None else DIR_OUTPUT
    slug = str(slug).replace("\\\\", "/")
    direto = base / slug

    # ... procurar em hubs (código existente) ...

    # ANTES DE RETORNAR O FALLBACK PLANO:
    if modo == 'escrita':
        tipo, sep, resto = slug.partition("/")
        if tipo in _raizes_tipo():  # se está tentando criar em output/<tipo>/<slug>
            raise ValueError(
                f"Modo escrita rejeita raiz plana. "
                f"Slug '{slug}' tentaria criar em '{direto}' (proibido). "
                f"Use: (1) dir_obra(..., modo='leitura') para ler, ou "
                f"(2) criar um hub para acomodar a nova obra. Ver CLAUDE.md § Estrutura."
            )

    return direto  # OK em modo leitura; modo escrita foi bloqueado acima

ONDE INTEGRAR modo='escrita':
  1. parametros_obra.carregar_config() — lê, mode='leitura' (OK leitura plana)
  2. esbocar.py agent — escreve config, mode='escrita' (FORÇA hub)
  3. fatiar-obra.py — escreve derivado, mode='escrita' (FORÇA hub)
  4. minerar-fontes-academicas.py — escreve pesquisa, mode='escrita' (FORÇA hub)
"""

MUDANCA_PARAMETROS = """
MUDANÇA 2: parametros_obra.py — validar que config vem de hub (optativo)

Adicionar função:

def validar_config_em_hub(slug):
    '''Se config existe, certifica que está em um hub, não em raiz plana.
    Aviso apenas (não quebra código antigo).'''
    caminho = caminho_config(slug)

    # Verificar se está em raiz plana
    TIPOS_PLANOS = {"livros", "tccs", "artigos", "ebooks",
                    "playbooks", "lead-magnets", "decks", "emails"}

    partes = caminho.relative_to(DIR_OUTPUT).parts
    if len(partes) > 0 and partes[0] in TIPOS_PLANOS:
        import warnings
        warnings.warn(
            f"Config em raiz plana: {caminho}. "
            f"Mude para output/<hub>/{'/'.join(partes)}.",
            DeprecationWarning,
            stacklevel=2
        )

Integração:
  - carregar_config() chama validar_config_em_hub() como aviso
  - Não quebra codigo antigo, mas alerta sobre problemas
"""

MUDANCA_AUDITORIA = """
MUDANÇA 3: auditar-obra.py — gate pré-compilação (CRÍTICO)

Adicionar gate que falha antes de compilar se estrutura é inválida:

def gate_estrutura_hub(slug):
    '''Gate R-STR-1: estrutura deve estar em hub, nunca em raiz plana.'''
    from validar_estrutura_hub import validar_estrutura_output

    resultado = validar_estrutura_output()

    if resultado['violacoes']:
        # Filtrar apenas violações relacionadas a `slug`
        violacoes_slug = [v for v in resultado['violacoes']
                         if slug in v.get('caminho', '')]
        if violacoes_slug:
            raise ValueError(
                f"Gate R-STR-1 FALHOU: Estrutura hub inválida para {slug}.\\n"
                + "\\n".join(v['mensagem'] for v in violacoes_slug)
            )

Integração em auditar-obra.py:
  - linha ~150 (após carregar_config, antes dos gates de conteúdo):
    gate_estrutura_hub(args.slug)
"""

MUDANCA_PRECOMMIT = """
MUDANÇA 4: pre-commit hook — valida antes de aceitar commit

Adicionar ao .git/hooks/pre-commit (depois dos testes):

# Gate de estrutura hub
echo "[pre-commit] Validando estrutura HUB por coleção..."
python scripts/validar-estrutura-hub.py --estrito
if [ $? -ne 0 ]; then
    echo "✗ COMMIT BLOQUEADO: Violações da regra HUB encontradas."
    echo "Corrija com: python scripts/validar-estrutura-hub.py --relatorio"
    exit 1
fi

Benefício: nenhum commit com estrutura plana pode entrar no repo
"""

MUDANCA_EMPACOTAR = """
MUDANÇA 5: empacotar-colecao.py — rejeita estrutura não conforme

Adicionar validação antes de empacotar:

from validar_estrutura_hub import validar_estrutura_output

def empacotar_colecao(slug_colecao, destino):
    # Validar que tudo está em hub antes de empacotar
    resultado = validar_estrutura_output()
    if resultado['violacoes']:
        raise ValueError(
            f"Não posso empacotar {slug_colecao}: estrutura hub inválida.\\n"
            f"Erros: {resultado['resumo']}\\n"
            f"Execute: python scripts/validar-estrutura-hub.py --relatorio"
        )

    # ... resto do empacotamento ...

Benefício: evita distribuir pacotes com artefatos órfãos
"""

# ──────────────────────────────────────────────────────────────────────────
# DIAGRAMA DE INTEGRAÇÃO
# ──────────────────────────────────────────────────────────────────────────

DIAGRAMA_INTEGRACAO = """
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUXO DE VALIDAÇÃO HUB                                │
└─────────────────────────────────────────────────────────────────────────┘

1. ESCRITA (agente/script cria obra/derivado)
   ├─ esbocar.py → dir_obra(slug, modo='escrita') → ✓ força hub
   ├─ fatiar-obra.py → dir_obra(..., modo='escrita') → ✓ força hub
   └─ minerar-fontes.py → dir_obra(..., modo='escrita') → ✓ força hub
                                    ↓
2. LEITURA (script lê config/sumario existente)
   ├─ parametros_obra.py → dir_obra(slug) + validar_config_em_hub()
   ├─ colecao.py → dir_obra() para listar
   └─ gerar-capa.py → dir_obra() para ler config
                                    ↓
3. AUDITORIA (pré-compilação)
   ├─ auditar-obra.py → gate_estrutura_hub() → validar-estrutura-hub.py
   └─ compile/empacotar ← falha se violações
                                    ↓
4. GIT (pré-commit)
   └─ .git/hooks/pre-commit → validar-estrutura-hub.py --estrito
                                    ↓
5. DISTRIBUIÇÃO (empacotar)
   └─ empacotar-colecao.py → validar-estrutura-hub.py
                                    ↓
   Resultado: ESTRUTURA HUB INVIOLÁVEL ✓
"""

TABELA_RESUMO = """
┌────────────────────┬─────────────────────┬──────────────────────┬─────────┐
│ Ponto de Integração│ Script/Arquivo      │ Ação                 │ Severidade
├────────────────────┼─────────────────────┼──────────────────────┼─────────┤
│ 1. Escrita         │ tipos_obra.py       │ dir_obra(m='escrita')│ CRÍTICA │
│                    │ esbocar.py          │ modo='escrita'       │         │
│                    │ fatiar-obra.py      │ modo='escrita'       │         │
├────────────────────┼─────────────────────┼──────────────────────┼─────────┤
│ 2. Leitura         │ parametros_obra.py  │ validar_config_...() │ AVISO   │
│                    │ colecao.py          │ deprecation warning  │         │
├────────────────────┼─────────────────────┼──────────────────────┼─────────┤
│ 3. Auditoria       │ auditar-obra.py     │ gate_estrutura_hub() │ CRÍTICA │
│                    │ validar-...-.py     │ falha se inválida    │         │
├────────────────────┼─────────────────────┼──────────────────────┼─────────┤
│ 4. Pré-commit      │ .git/hooks/         │ validar --estrito    │ CRÍTICA │
│                    │ pre-commit          │ bloqueia commit      │         │
├────────────────────┼─────────────────────┼──────────────────────┼─────────┤
│ 5. Distribuição    │ empacotar-colecao   │ validar antes de emb │ CRÍTICA │
└────────────────────┴─────────────────────┴──────────────────────┴─────────┘
"""

# ──────────────────────────────────────────────────────────────────────────
# TESTE DE INVIOLABILIDADE
# ──────────────────────────────────────────────────────────────────────────

TESTE_INVIOLABILIDADE = """
Verificação pós-implementação (checklist):

□ 1. dir_obra(slug, modo='escrita') rejeita raiz plana?
     python -c "from scripts.tipos_obra import dir_obra; dir_obra('livros/test', modo='escrita')"
     ✓ Levanta ValueError

□ 2. Gate de auditoria falha em estrutura inválida?
     python scripts/auditar-obra.py deepseek-harness-do-zero-ao-phd
     ✓ Gate R-STR-1 falha com mensagem clara

□ 3. Pre-commit bloqueia commit com estrutura plana?
     touch output/livros/teste/config_obra.json
     git add -A
     git commit -m "test"
     ✓ Commit bloqueado, saída clara

□ 4. Empacotar-colecao rejeita estrutura inválida?
     python scripts/empacotar-colecao.py deepseek-harness
     ✓ Levanta ValueError

□ 5. Leitura (parametros_obra) ainda funciona com raiz plana (retrocompat)?
     python scripts/parametros_obra.py deepseek-harness-do-zero-ao-phd
     ✓ Funciona, mas com DeprecationWarning

□ 6. Suite de testes passa 100%?
     python -m pytest -q scripts/tests/
     ✓ 100%

□ 7. Nenhuma raiz plana foi criada nos últimos N commits?
     python scripts/validar-estrutura-hub.py --relatorio
     ✓ {"valido": true, "violacoes": []}
"""

# ──────────────────────────────────────────────────────────────────────────
# MIGRAÇÃO DE ESTRUTURA PLANA EXISTENTE
# ──────────────────────────────────────────────────────────────────────────

MIGRACAO = """
Para RESOLVER as 4 violações atuais:

Opção A (LIMPA — recomendada):
--------
1. Criar novo hub 'deepseek' para acomodar a coleção:
   mkdir -p output/deepseek/{livros,playbooks,colecoes}

2. Mover artefatos:
   mv output/livros/deepseek-harness-do-zero-ao-phd/* output/deepseek/livros/
   mv output/playbooks/deepseek-harness/* output/deepseek/playbooks/
   mv output/colecoes/deepseek-harness-do-zero-ao-phd.json output/deepseek/colecoes/

3. Remover raízes planas vazias:
   rmdir output/livros output/playbooks

4. Validar:
   python scripts/validar-estrutura-hub.py
   ✓ Deve estar valido=true

5. Commitar:
   git add relatorios/
   git commit -m "refactor: migrar deepseek para hub (estrutura conforme HUB POR COLEÇÃO)"

Opção B (CONSERVADORA):
--------
Deixar estrutura plana como está mas:
  1. Bloquear novas estruturas planas via dir_obra(mode='escrita')
  2. Avisar via DeprecationWarning sobre raizes existentes
  3. Migrar gradualmente conforme trabalha-se nas obras
"""

# ──────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Diagnóstico e proposta de endurecimento da regra HUB"
    )
    ap.add_argument("--diagrama", action="store_true",
                    help="Mostrar diagrama de integração")
    ap.add_argument("--codigo", action="store_true",
                    help="Mostrar código das 5 mudanças")
    ap.add_argument("--teste", action="store_true",
                    help="Mostrar checklist de inviolabilidade")
    ap.add_argument("--migracao", action="store_true",
                    help="Mostrar estratégia de migração")
    ap.add_argument("--completo", action="store_true",
                    help="Mostrar tudo")

    args = ap.parse_args()

    if not any([args.diagrama, args.codigo, args.teste, args.migracao, args.completo]):
        args.completo = True

    print("=" * 79)

    if args.completo or args.codigo:
        print("\n📋 RAIZ DO PROBLEMA")
        print(RAIZ_PROBLEMA)

        print("\n📋 PROVEDORES (176 chamadas a dir_obra)")
        print(PROVEDORES)

        print("\n📋 MUDANÇAS PROPOSTAS (5 PONTOS)")
        print(MUDANCA_TIPO_OBRA)
        print(MUDANCA_PARAMETROS)
        print(MUDANCA_AUDITORIA)
        print(MUDANCA_PRECOMMIT)
        print(MUDANCA_EMPACOTAR)

    if args.completo or args.diagrama:
        print("\n📊 DIAGRAMA DE INTEGRAÇÃO")
        print(DIAGRAMA_INTEGRACAO)
        print(TABELA_RESUMO)

    if args.completo or args.teste:
        print("\n✓ CHECKLIST DE INVIOLABILIDADE")
        print(TESTE_INVIOLABILIDADE)

    if args.completo or args.migracao:
        print("\n🔄 ESTRATÉGIA DE MIGRAÇÃO")
        print(MIGRACAO)

    print("\n" + "=" * 79)


if __name__ == "__main__":
    main()
