# Dossiê Técnico: Fundamentos, Práticas e Arquitetura em DevOps

## 1. Contextualização e Visão Geral
O termo **DevOps** (uma junção de *Development* e *Operations*) representa uma mudança cultural, filosófica e de engenharia focada na unificação do desenvolvimento de software e das operações de TI. O objetivo principal é encurtar o ciclo de vida do desenvolvimento de sistemas e fornecer entrega contínua com alta qualidade de software (EBERT et al., 2016; BASS et al., 2015).

### 1.1 Objetivos Centrais
- **Quebra de Silos:** Alinhamento de incentivos entre equipes de desenvolvimento, testes, segurança e operações.
- **Automação de Processos:** Eliminação de tarefas manuais repetitivas por meio de pipelines de CI/CD e infraestrutura como código.
- **Feedback Rápido:** Monitoramento contínuo e telemetria para detecção precoce de falhas em produção.

---

## 2. Pilares Fundamentais (Cultura CALMS)
O modelo CALMS sumariza os pilares essenciais do DevOps:
1. **Cultura (Culture):** Foco em colaboração, responsabilidade compartilhada e cultura de aprendizado com falhas (*blameless postmortems*).
2. **Automação (Automation):** Automatizar o build, teste, provisionamento e deploy.
3. **Lean (Lean):** Reduzir desperdícios, fluxo contínuo e lotes de entrega menores.
4. **Medição (Measurement):** Coleta de métricas de desempenho e engenharia (DORA metrics: *Deployment Frequency*, *Lead Time for Changes*, *Mean Time to Recovery - MTTR*, e *Change Failure Rate*).
5. **Compartilhamento (Sharing):** Transparência de conhecimento e ferramentas entre os times.

---

## 3. Práticas e Engenharia de CI/CD
A Integração Contínua (CI) e a Entrega/Implantação Contínua (CD) constituem a espinha dorsal técnica do DevOps.
- **Integração Contínua:** Desenvolvedores integram código em um repositório central frequentemente (várias vezes ao dia). Cada integração é verificada por um build automatizado e testes unitários/integração (DHAWAN & DHAWAN, 2026).
- **Entrega Contínua:** O código validado pelo pipeline é automaticamente preparado para release em ambientes de homologação ou produção, exigindo aprovação manual ou automática (BILDIRICI & AKDEMIR, 2023).
- **Ferramentas de Referência:** Jenkins, GitLab CI, GitHub Actions, Argo CD.

---

## 4. Infraestrutura como Código (IaC) e Contêineres
- **Infraestrutura como Código (IaC):** Provisionamento e gerenciamento de infraestrutura (servidores, redes, balanceadores) por meio de arquivos de configuração versionados (Terraform, Ansible). Garante imutabilidade e reproducibilidade de ambientes.
- **Contêineres e Orquestração:** O Docker padroniza o empacotamento da aplicação e suas dependências (DOCKER, 2026). O Kubernetes gerencia o ciclo de vida, escalabilidade e resiliência de contêineres em larga escala (KUBERNETES, 2026).

---

## 5. Segurança, Monitoramento e Observabilidade (DevSecOps)
- **DevSecOps:** Integração de práticas de segurança (*Shift-Left*) desde as etapas iniciais do desenvolvimento (análise estática de código - SAST, análise de dependências, escaneamento de contêineres).
- **Observabilidade:** Monitoramento baseado em Três Pilares:
  1. **Métricas:** Séries temporais (Prometheus, Grafana).
  2. **Logs:** Agregação e indexação de eventos (ELK Stack, Fluentd).
  3. **Traces:** Rastreamento distribuído de requisições em microsserviços (Jaeger, OpenTelemetry).

---

## 6. Fontes Brutas

- EBERT, Christof et al. *DevOps*. In: IEEE Software. 2016. Disponível em: https://doi.org/10.1109/ms.2016.68. Acesso em: 26 ago. 2026. (A)
- BASS, Len; WEBER, Ingo; ZHU, Liming. *Devops: A Software Architect's Perspective*. In: CERN Document Server. 2015. Disponível em: http://cds.cern.ch/record/2034028. Acesso em: 26 ago. 2026. (A)
- LEITE, Leonardo et al. *A Survey of DevOps Concepts and Challenges*. In: ACM Computing Surveys. 2019. Disponível em: https://doi.org/10.1145/3359981. Acesso em: 26 ago. 2026. (A)
- DHAWAN, R.; DHAWAN, M. *AI-augmented reliability in CI/CD: a framework for predictive, adaptive, and self-correcting pipelines*. In: Frontiers in artificial intelligence. 2026. Disponível em: https://pubmed.ncbi.nlm.nih.gov/41994557/. Acesso em: 26 ago. 2026. (A)
- BILDIRICI, Fatih; AKDEMIR, Ömür. *From Agile to DevOps, Holistic Approach for Faster and Efficient Software Product Release Management*. In: arXiv. 2023. Disponível em: http://arxiv.org/abs/2301.09429v1. Acesso em: 26 ago. 2026. (A)
- DOCKER. *What is Docker?*. Disponível em: https://docs.docker.com/get-started/overview/. Acesso em: 26 ago. 2026. (B)
- KUBERNETES. *Kubernetes Components*. Disponível em: https://kubernetes.io/docs/concepts/overview/components/. Acesso em: 26 ago. 2026. (B)
- JENKINS. *Pipeline*. Disponível em: https://www.jenkins.io/doc/book/pipeline/. Acesso em: 26 ago. 2026. (B)
