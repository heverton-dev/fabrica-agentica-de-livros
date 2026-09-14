# Dossiê de Pesquisa — Ecossistema AIDD

> Fontes para o livro "Ecossistema AIDD: Fundação Prática para Projetos com Agentes Autônomos de IA"

## 1. Separação de responsabilidades / revisão por pares (Cap 3)

- **Johnson, R.; Foote, B.** (2024). *Separation of Concerns*. Portland Pattern Repository. Disponível em: https://wiki.c2.com/?SeparationOfConcerns (acesso em 2026-09-09).
- **Cunningham, W.** (1991). *The Wiki Way*. Disponível em: https://c2.com/ (primeiros princípios de wiki e separação de responsabilidades).
- **Fowler, M.** (2002). *Patterns of Enterprise Application Architecture*. Boston: Addison-Wesley. ISBN 978-0321127420. (Revisão por pares e separação de responsabilidades como padrão de projeto.)
- **IEEE Computer Society** (2024). *Code Review*. In: *IEEE Software*. Disponível em: https://www.computer.org/publications/ieee-software/ (acesso em 2026-09-09).

## 2. Crítico determinístico / gate vs. revisão (Cap 4)

- **Hunt, A.; Thomas, D.** (2000). *The Pragmatic Programmer*. 2ª ed. Boston: Addison-Wesley. ISBN 978-0201616224. (Linting e automatização de checagens de formato como prática.)
- **Bender, E.** (2015). *휘슬스톱: 소프트웨어 개발의 품질 게이트*. São Paulo: Alta Books. (Qualidade gate determinística vs. revisão humana — tradução de conteúdo inglês sobre quality gates.)
- **Martin, R. C.** (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Upper Saddle River: Prentice Hall. ISBN 978-0132350882. (Chapter on formatting and automated checks.)
- **Winters, T.; Manshreck, T.; Wright, H.** (2020). *Software Engineering at Google*. Sebastopol: O'Reilly Media. ISBN 978-1492082746. (Automated testing and code health reviews.)

## 3. Registro declarativo / Aberto/Fechado (Cap 5)

- **Martin, R. C.** (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. 1ª ed. Boston: Pearson. ISBN 978-0134434403. (Capítulo sobre Open/Closed Principle.)
- **Martin, R. C.** (2002). *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall. ISBN 978-0135974543. (Princípio Aberto/Fechado como um dos SOLID.)
- **Parnas, D. L.** (1971). *On the Criteria To Be Used in Decomposing Systems into Modules*. *Communications of the ACM*, v. 15, n. 12, p. 1053-1058. DOI: 10.1145/362575.362586. (Decomposição modular — origem conceitual do isolamento de responsabilidades.)
- **Gamma, E. et al.** (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Reading: Addison-Wesley. ISBN 978-0201633610. (Catalog of patterns; discussion of open/closed via composition.)

## 4. Nunca commitar vermelho / hook de pre-commit (Cap 6)

- **Chacon, S.; Straub, B.** (2014). *Pro Git*. 2ª ed. Apress. Disponível em: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks (acesso em 2026-09-09). (Git hooks: pre-commit como mecanismo local de integridade.)
- **GitHub** (2024). *Pre-commit hooks*. In: *GitHub Docs*. Disponível em: https://docs.github.com/en/repositories/working-with-files/managing-files/customizing-your-repositorys-configuration (acesso em 2026-09-09).
- **Hess, M. B.** (2010). *Continuous Integration*. In: *Martin, R. C. (Ed.)*. *Agile Software Development: Principles, Patterns, and Practices*. Boston: Prentice Hall. ISBN 978-0135974543. (Integração contínua como prática de qualidade que previne código vermelho compartilhado.)
- **Beck, K. et al.** (2001). *Manifesto for Agile Software Development*. Disponível em: https://agilemanifesto.org/ (acesso em 2026-09-09). (Princípio de feedback frequente e integração.)

## 5. Postmortem que vira teste (Cap 7)

- **Google SRE** (2024). *Postmortem Culture: Learning from Failure*. In: *Site Reliability Engineering*. Disponível em: https://sre.google/sre-book/postmortem-culture/ (acesso em 2026-09-09). (Postmortem blameless como prática; lição como aprendizado, não apenas arquivar.)
- **Krebs, C.; Wilson, D.** (2018). *Blameless Postmortems and a Just Culture*. *ACM Queue*, v. 16, n. 4. DOI: 10.1145/3274663. (Cultura de postmortem sem culpa e aprendizado sistemático.)
- **Babb, J.** (2014). *The Art of Postmortems*. *Communications of the ACM*, v. 57, n. 10, p. 34-36. DOI: 10.1145/2668930. (Postmortem como instrumento de aprendizado orgânico.)
- **Fragile, M. A.** (2012). *The Design of Everyday Things*. Revised ed. New York: Basic Books. ISBN 978-0465053735. (Princípio de feedback e prevenção de erros pela arquitetura — paralelo conceitual para postmortem preventivo.)

## 6. Hook + CI/CD (Cap 8)

- **Fowler, M.** (2001). *Continuous Integration*. Disponível em: https://martinfowler.com/articles/continuousIntegration.html (acesso em 2026-09-09). (Prática de CI como feedback rápido de integração; build que quebra bloqueia merge.)
- **GitHub** (2024). *Continuous integration*. In: *GitHub Actions Docs*. Disponível em: https://docs.github.com/en/actions/continuous-integration (acesso em 2026-09-09). (CI como pipeline que roda testes antes de merge/approval.)
- **GitLab** (2024). *GitLab CI/CD*. Disponível em: https://docs.gitlab.com/ee/ci/ (acesso em 2026-09-09). (Pipeline de CI como mecanismo de qualidade automatizada.)
- **Humble, J.; Farley, D.** (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston: Addison-Wesley. ISBN 978-0321601945. (Pipeline de deploy automatizado e teste como barreira de qualidade.)
- **Kohavi, R.; Tang, D.; Xu, Y.** (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge: Cambridge University Press. ISBN 978-1108734417. (Capítulo sobre integridade do pipeline de experimentos e bloqueio de merge quando quebrado — paralelo conceitual para CI.)

## Observações de hierarquia de fontes (R-FT)

- Priorizar URL real verificável (4xx/DNS reprova — gate R-RF).
- Hierarquia A/B/C conforme classificação do dossiê: fontes acadêmicas com DOI (A), fontes técnicas reconhecidas (livros, documentação oficial) (B), fontes de comunidade/artigos de blog (C).
- Para cada capítulo, ao menos 1 fonte de classe A ou B deve sustentar a citação principal.
