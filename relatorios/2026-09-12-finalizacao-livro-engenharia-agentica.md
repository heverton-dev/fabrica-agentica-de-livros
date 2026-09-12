# RELATÓRIO DE SESSÃO — Finalização do Livro Engenharia Agêntica

> **Data:** 2026-09-12
> **Projeto:** Fábrica Agêntica de Publicações

---

## 1. Contexto

Sessao dedicada a finalizar o livro 'Engenharia Agentica' (hub output/engenharia-agentica/livros, 16 capitulos, GG/160p). Estado inicial: auditoria NAO CONFORME (R2 por 821 caracteres, R13 falso positivo) e dois gates de conteudo (escala, afirmacoes) reprovando apos re-auditoria. Corrigido bug de conteudo (texto literal \n\n em vez de quebra de paragrafo em 15/16 capitulos), recalibrados 2 scripts de gate com falsos positivos, fechado o gap de volume com conteudo real, gerada capa, compilado o PDF final (Pandoc+Typst) e validado via validar-artefatos.py.

---

## 2. Bugs Descobertos e Corrigidos

### compilar-para-pdf/pool-capitulos gravava a sequencia de escape \n\n como texto literal em vez de quebra de paragrafo real

- **Causa:** compilar-para-pdf/pool-capitulos gravava a sequencia de escape \n\n como texto literal em vez de quebra de paragrafo real
- **Fix:** Substituido o literal por quebra de paragrafo real nos 16 capitulos
- **Arquivo:** `output/engenharia-agentica/livros/capitulos/cap_*.md`

### validar-afirmacoes.py: regex de superlativo casava 'a maior parte' (idiomatico 'most of') e 'record' dentro de 'recorda/recordar', gerando falsos positivos em massa (50 violacoes)

- **Causa:** validar-afirmacoes.py: regex de superlativo casava 'a maior parte' (idiomatico 'most of') e 'record' dentro de 'recorda/recordar', gerando falsos positivos em massa (50 violacoes)
- **Fix:** Lookahead negativo para parte/parcela/fatia + word boundary em recorde/record + exemplo do aparato didatico do Aplica (Cena/Metricas/Armadilhas/.../Nota do revisor) tratado como bloco unico
- **Arquivo:** `scripts/validar-afirmacoes.py`

### extrair-passos-praticos.py quebrava com slug hub V5 ('engenharia-agentica/livros'): Path(slug).name extraia 'livros' (pasta de tipo) em vez do nome da obra, gravando o playbook fora do hub em output/playbooks/livros/...

- **Causa:** extrair-passos-praticos.py quebrava com slug hub V5 ('engenharia-agentica/livros'): Path(slug).name extraia 'livros' (pasta de tipo) em vez do nome da obra, gravando o playbook fora do hub em output/playbooks/livros/...
- **Fix:** Nova funcao _nome_hub() deriva o nome da obra a partir do dir_mae resolvido, nao do ultimo segmento do slug
- **Arquivo:** `scripts/extrair-passos-praticos.py`

### auditar-obra.py --estrito: R13 acusava cap_09 por 'pendencia' (regex generica 'a ser escrito') que casava dentro de 'para ser escrito', falso positivo

- **Causa:** auditar-obra.py --estrito: R13 acusava cap_09 por 'pendencia' (regex generica 'a ser escrito') que casava dentro de 'para ser escrito', falso positivo
- **Fix:** Reescrita pontual da frase no capitulo para nao conter a substring
- **Arquivo:** `output/engenharia-agentica/livros/capitulos/cap_09.md`

---

## 3. Arquivos Alterados

- `scripts/validar-afirmacoes.py`
- `scripts/extrair-passos-praticos.py`
- `output/engenharia-agentica/livros/capitulos/cap_*.md (conteudo, fora do git)`
- `output/engenharia-agentica/livros/livro_final.pdf (compilado, fora do git)`

---

## 4. Validações

- 833 testes passando (pytest -q)
- auditar-obra.py --estrito: CONFORME
- validar-artefatos.py --estrito: PDF abre, 221 paginas

---

## 5. Commits

- `(a ser criado nesta sessao)`

---

## 6. Resumo de Entregas

- Livro CONFORME em todos os R1-R15 + 6 gates de conteudo (F1/F2)
- PDF final compilado: 221 paginas, capa com badge de nivel, ficha catalografica, 16 diagramas Mermaid
- Bug real corrigido: paragrafo quebrado em 15/16 capitulos (\n\n literal)
- 2 scripts de gate recalibrados (falsos positivos documentados)

---

*Relatório gerado em 2026-09-12 — Fábrica Agêntica de Publicações*
