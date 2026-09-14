# Manual OmniRoute — 15 Provedores de IA Gratuitos

## 📚 Conteúdo Disponível

Este livro está estruturado em 5 capítulos EITA (Introdução, Explica, Ilustra, Técnica, Aplica):

### Capítulos

1. **01-introducao.md** — OmniRoute: Seu Agregador de Modelos de IA
   - Introdução ao conceito
   - Arquitetura do proxy
   - Setup mínimo (3 passos)
   - Tempo de leitura: ~20 min

2. **02-dashboard.md** — Acessando e Navegando o Dashboard
   - Como acessar o painel
   - Menu e navegação
   - Gerenciamento de usuários
   - Tempo de leitura: ~18 min

3. **03-provedores.md** — 15 Provedores Gratuitos: Seleção, Setup e Comparação
   - Tabela dos 15 provedores
   - 5 passos idênticos de setup
   - Top 3 recomendados
   - Tempo de leitura: ~35 min

4. **04-claude-code.md** — Integrando OmniRoute com Claude Code
   - Configuração em Claude Code Web
   - Setup em Cursor (desktop)
   - Seleção de modelos
   - Testes com curl
   - Tempo de leitura: ~18 min

5. **05-troubleshooting.md** — Troubleshooting: Resolvendo Problemas Comuns
   - Diagnóstico em camadas
   - 5 problemas comuns e soluções
   - Árvore de decisão
   - Tempo de leitura: ~22 min

---

## 📋 Resumo Executivo

OmniRoute é um **proxy OpenAI-compatível** que centraliza credenciais de múltiplos provedores de IA (Vertex AI, Claude, GPT-4, Groq, etc.) e faz load balancing automático.

- **Para startups**: Reduz custos em 70% + garante 99.99% uptime
- **Para DevOps**: Elimina fricção de múltiplas credenciais
- **Para desenvolvedores**: Uma API única para 15+ modelos

---

## 🎯 Como Ler

**Caminho rápido (1 hora):**
1. Leia Cap 1 (Introdução + Conceito)
2. Pule Cap 2 (se já conhece dashboard)
3. Leia Cap 3 (Provedores) — foco no "Top 3 Recomendados"
4. Pule para Cap 4 (Claude Code) direto

**Caminho completo (2h 30min):**
Leia tudo na ordem: 1 → 2 → 3 → 4 → 5

**Se você tem problema:**
Pule direto para Cap 5 (Troubleshooting) — árvore de decisão resolve 99% dos casos

---

## 🚀 Setup Rápido (3 Passos)

```
1. Acesse: http://81.17.103.186:20127
   Usuário: admin
   Senha: omniroute_2026

2. Gere API Key em: Settings → API Keys

3. Use em código:
   curl http://81.17.103.186:20127/v1/chat/completions \
     -H "Authorization: Bearer sk-omniroute-..." \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Olá!"}]}'
```

---

## 📊 Informações do Livro

| Aspecto | Valor |
|---------|-------|
| **Versão** | 1.0 |
| **Data** | 24 de agosto de 2026 |
| **Autor** | Marketing Conexão |
| **Público** | Desenvolvedores, DevOps, Startups |
| **Nível** | Intermediário |
| **Tempo total** | 2h 30min |
| **Capítulos** | 5 (EITA structure) |
| **Palavras** | ~18.000 |

---

## 🏷️ Tags

`OmniRoute` `IA` `API` `LLM` `Provedores Gratuitos` `Claude Code` `DevOps` `Integração` `Load Balancing`

---

**Editora Agêntica — Agosto 2026**
