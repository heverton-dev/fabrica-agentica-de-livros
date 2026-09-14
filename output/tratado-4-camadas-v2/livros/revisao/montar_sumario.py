#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grava o sumario_macro.json da reescrita GG (bancada pratica).

Cada capitulo declara: titulo, objetivo, 3 pilares, ancora visual, entrega
tecnica, aplicacao no projeto do leitor e o que acontece no caso ancora.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DESTINO = Path(__file__).resolve().parent.parent / "sumario_macro.json"

C = lambda n, t, o, p, av, et, ap, ca: {
    "capitulo": str(n), "titulo": t, "objetivo": o, "pilares_previstos": p,
    "ancora_visual": av, "entrega_tecnica": et,
    "aplicacao_no_projeto": ap, "caso_ancora": ca,
}

PARTES = [
    ("I", "A Bancada Antes da Primeira Peça", [
        C(1, "A conta que ninguém quer pagar",
          "Mostrar com números por que projetos construídos no improviso com IA travam, e apresentar o mapa das quatro camadas que resolve cada uma das dores.",
          ["As quatro dores que param um projeto de IA: contexto esquecido, casca sem função, paralelismo cego e prisão de fornecedor",
           "A diferença entre conversar com a IA e operar uma bancada de trabalho",
           "O mapa da obra: as quatro camadas, o projeto que entra na bancada e o que estará pronto no fim"],
          "Linha do tempo comparada: o projeto improvisado travando no terceiro dia contra o projeto de bancada entregando a mesma tarefa com conferência",
          "Diagnóstico escrito das quatro dores aplicado ao próprio projeto e a escolha do alvo que entrará na bancada",
          "Listar as tarefas repetitivas que você faz à mão hoje e escolher uma única para ser o alvo da obra",
          "Apresentação do Painel de Pedidos: o que faz, quanto consome hoje em trabalho manual e por que é o alvo escolhido"),
        C(2, "O dicionário de bancada",
          "Fixar sem jargão os termos que aparecem do começo ao fim da obra, cada um com analogia de bancada e um exemplo tirado do caso âncora.",
          ["Termos de IA e contexto: agente, janela de contexto, alucinação, contexto canônico",
           "Termos de engenharia: harness, portão de qualidade, exit code, stub, worktree",
           "Termos de operação: protocolo de ferramentas, persistência, idempotência, ambiente reversível"],
          "O quadro de parede da oficina: cada termo em uma etiqueta com sua analogia física",
          "Glossário pessoal em arquivo próprio dentro do repositório",
          "Escrever o glossário do seu domínio, traduzindo cada termo técnico para o vocabulário da sua área",
          "Tradução dos termos aplicada ao Painel de Pedidos: o que significa portão quando o assunto é pedido duplicado"),
        C(3, "O seu projeto na bancada",
          "Preparar o alvo real: escolher o projeto, fotografar o estado atual em números, medir o custo do trabalho manual e criar a base mínima de trabalho.",
          ["Escolher um alvo do tamanho certo: pequeno, real, com dor que dá para medir",
           "Fotografar antes: linha de base, tempo gasto, erros por semana, retrabalho",
           "Criar a base mínima: repositório, caderno de bancada e uma verificação que já roda"],
          "A fotografia do antes pregada na parede, ao lado do espaço onde ficará a do depois",
          "Linha de base documentada em números e repositório inicial com uma verificação executável",
          "Medir em minutos o custo atual de uma tarefa sua e gravar essa linha de base antes de mudar qualquer coisa",
          "Medição do Painel de Pedidos: minutos por dia gastos à mão, erros de digitação por semana e pedidos perdidos por mês"),
        C(4, "A Constituição da bancada",
          "Apresentar as leis que impedem retrabalho e ensinar a escrever as regras do próprio projeto em um arquivo único que a IA lê antes de agir.",
          ["As leis inegociáveis da bancada e o preço de cada uma quando ignorada",
           "Regra escrita contra regra executável: quem fiscaliza a regra que ninguém lembra",
           "Como escrever o arquivo de regras do seu projeto e o que nunca deve entrar nele"],
          "A constituição pregada na parede da oficina, com as leis numeradas e o responsável por fiscalizar cada uma",
          "Arquivo de regras do projeto com itens curtos, verificáveis e sem ambiguidade",
          "Escrever as primeiras regras do seu projeto e marcar quais delas um comando consegue verificar",
          "A constituição do Painel de Pedidos: nenhum pedido entra sem identificador externo, nenhum relatório sai sem totais conferidos"),
    ]),
    ("II", "As Quatro Peças", [
        C(5, "Peça 1 — Contexto: o que a IA lê antes de agir",
          "Montar a camada de contexto: definir o que entra na mesa de trabalho da IA, em que formato e em que ordem, para que ela obedeça hoje e continue obedecendo depois.",
          ["O que a IA precisa ler antes de escrever a primeira linha: objetivo, contrato, exemplo e prova",
           "Densidade e localidade: por que contexto grande atrapalha e contexto certo acelera",
           "Arquivos canônicos que sobrevivem à troca de modelo, de ferramenta e de pessoa"],
          "A mesa de trabalho da bancada: o que fica sobre ela e o que vai para a gaveta",
          "Especificação curta e contrato de dados do projeto, com o exemplo mínimo que orienta o trabalho",
          "Escrever, em uma página, a especificação de uma tarefa sua com entrada, saída e critério de pronto",
          "A especificação do Painel de Pedidos: formato do arquivo de entrada, campos obrigatórios do pedido e regra de duplicidade"),
        C(6, "Peça 2 — Harness: o ciclo de vida e os disjuntores",
          "Instalar o ciclo de vida do trabalho com portões que devolvem sim ou não e proteções que impedem ações destrutivas antes que elas aconteçam.",
          ["O ciclo de quatro passos e por que quem verifica não pode ser a mesma voz que executa",
           "Portões binários: aprovação e bloqueio, sem estado intermediário de quase aprovado",
           "Proteções e ambiente reversível: como errar sem perder o trabalho do dia"],
          "O quadro de disjuntores da oficina: qual circuito abre em cada situação de risco",
          "Verificação do projeto que devolve código de aprovação ou bloqueio e regra de proteção das pastas críticas",
          "Transformar em comando uma conferência que hoje você faz de olho",
          "O portão do Painel de Pedidos: todo arquivo passa por conferência de colunas, valores e duplicidades antes de entrar no banco"),
        C(7, "Peça 3 — Motor: roteamento, contratos e custo",
          "Decidir quem executa cada tarefa, travar as respostas em formatos previsíveis e entender como o custo cresce junto com o contexto.",
          ["Roteamento: tarefa pequena não precisa de agente caro nem de modelo maior",
           "Contratos: obrigar a resposta a chegar na forma que o resto do sistema entende",
           "Economia de operação: o que encarece a conta e o efeito do reaproveitamento de prefixo estável"],
          "O roteador de serviço da oficina: cada serviço entra pela porta certa, com o formulário certo",
          "Tabela de decisão do projeto e contrato de resposta em formato de dados",
          "Classificar as tarefas do seu dia em três portas de entrada e escolher o recurso adequado para cada uma",
          "Roteamento no Painel de Pedidos: leitura de arquivo é script, pedido ambíguo é agente e fechamento do dia é script"),
        C(8, "Peça 4 — Ferramentas e persistência: a usina determinística",
          "Montar as mãos da operação: ferramentas reexecutáveis, padronização de conexão com o mundo externo e um registro durável do que foi feito.",
          ["Ferramentas reexecutáveis: rodar duas vezes não pode estragar nada",
           "Padronização de ferramentas e os riscos reais de confiar sem verificar",
           "Persistência: onde vive o estado do trabalho e onde ele nunca deve viver"],
          "A prateleira da usina, cada ferramenta com etiqueta de uso, limite e dono",
          "Conjunto de ferramentas do projeto e registro durável das execuções",
          "Transformar em ferramenta reexecutável as duas ações que você mais repete à mão",
          "As ferramentas do Painel de Pedidos: importar, conferir e gerar relatório, todas reexecutáveis sem duplicar pedido"),
    ]),
    ("III", "Montagem: O Projeto Real de Ponta a Ponta", [
        C(9, "Primeiro encaixe: do script solto ao repositório governado",
          "Juntar as quatro peças em um projeto pequeno e real, partindo do que já existe, e fechar o primeiro ciclo completo com aprovação.",
          ["Inventário do que existe: o que aproveitar, o que cercar e o que precisa nascer",
           "A ordem de instalação das quatro peças e por que essa ordem importa",
           "O primeiro ciclo completo: uma tarefa do pedido ao portão aprovado"],
          "A bancada montada: as quatro peças no lugar e a primeira lâmpada de teste acesa",
          "Repositório do projeto com as quatro camadas mínimas instaladas e um ciclo completo aprovado",
          "Rodar um ciclo completo em uma tarefa pequena do seu projeto, do pedido até a verificação aprovada",
          "O Painel de Pedidos deixa de ser um script solto e passa a ser projeto governado, sem perder o que já funcionava"),
        C(10, "O caso âncora completo: o Painel de Pedidos, da ideia ao ar",
          "Percorrer a construção completa do caso âncora, com as decisões, os erros e as correções que aparecem em um projeto de verdade.",
          ["Modelagem: o que é um pedido, o que é um lote e o que é uma conferência",
           "Construção guiada: importação, painel, relatório, teste e publicação",
           "Registro de decisões: o que ficou de fora, por quê e o que isso custa depois"],
          "A vista explodida do projeto: cada peça com seu encaixe, sua função e sua etiqueta",
          "Caso âncora funcionando de ponta a ponta com registro de decisões",
          "Construir a primeira versão utilizável do seu projeto seguindo o mesmo roteiro do caso âncora",
          "Painel de Pedidos em uso local: importa o arquivo, mostra o painel, gera o relatório e registra cada execução"),
        C(11, "Trabalho em paralelo: subagentes, worktrees e integração sem colisão",
          "Dividir trabalho entre vários agentes sem que um apague o outro, com isolamento físico, fila de tarefas, revisão e integração controlada.",
          ["Isolamento físico: cada agente no seu diretório de trabalho, sem disputa por arquivo",
           "Fila e lotes: quantos agentes ao mesmo tempo e por que passar disso piora o resultado",
           "Integração e revisão: quem aceita o que entra e como o conflito se resolve"],
          "Várias bancadas iguais lado a lado, cada uma com o seu projeto e uma esteira de entrada e saída",
          "Duas frentes independentes rodando em paralelo com regra de integração e revisão definida",
          "Escolher duas tarefas independentes do seu projeto e executá-las em paralelo com isolamento",
          "O Painel de Pedidos ganha duas frentes simultâneas: relatório por período e conferência automática de divergências"),
        C(12, "Os portões finais: teste, auditoria e entrega",
          "Fechar o trabalho com verificação séria: testes que provam comportamento, auditoria que aponta o que ficou frouxo e uma entrega que outra pessoa consegue usar.",
          ["Teste que prova comportamento, não teste que apenas repete a implementação",
           "Auditoria guiada por evidência: descobrir o que faltou sem reler tudo a cada mudança",
           "Entrega utilizável: o que acompanha o artefato, quem pode operar e o que fica de fora"],
          "A esteira de saída: a peça atravessa os portões e sai com a etiqueta de conferida",
          "Suíte de testes do projeto, relatório de auditoria e pacote de entrega com instruções de uso",
          "Escrever um teste que falha antes da correção e passa depois, e montar o pacote de entrega",
          "O Painel de Pedidos entra em uso rotineiro com relatório conferido e divergências históricas corrigidas"),
    ]),
    ("IV", "Escala, Custo e Soberania", [
        C(13, "Fazer mais gastando menos: a economia da bancada",
          "Medir e reduzir o custo da operação sem perder qualidade, usando contexto reaproveitado, tarefas no lugar certo e limites claros de uso.",
          ["Medir antes de cortar: de onde vem o custo de uma operação com IA",
           "Reaproveitamento de prefixo estável e o efeito dele no custo e no tempo de resposta",
           "Limites: quando economizar degrada a qualidade e como perceber isso a tempo"],
          "O medidor de consumo da oficina: quanto cada painel gasta por tarefa executada",
          "Registro de custo por tarefa do projeto e dois cortes aplicados com ganho medido",
          "Medir uma semana de uso e aplicar dois cortes de custo no seu projeto",
          "O custo por relatório do Painel de Pedidos é medido antes e depois da reorganização do contexto"),
        C(14, "O certificado de bancada: provar que funciona",
          "Construir evidência de confiabilidade, distinguir prova de opinião e escrever um certificado honesto sobre o que a solução faz e o que não faz.",
          ["Evidência contra opinião: o que conta como prova em uma entrega de software",
           "Reprodutibilidade: a mesma entrada precisa produzir a mesma saída",
           "Declarar limites: o que a solução não faz, onde não deve ser usada e quem responde por ela"],
          "O certificado afixado na parede, com números, data, responsável e limites declarados",
          "Certificado do projeto com escopo, números, limites e responsável",
          "Produzir a evidência de uma entrega sua: números, procedimento de conferência e o que ficou de fora",
          "O Painel de Pedidos passa a ser operado por outra pessoa, com instruções, limites e procedimento de conferência"),
        C(15, "Levando a bancada para o time (e para o código que já existe)",
          "Adotar a bancada em equipe e em sistemas herdados: por onde começar, como convencer com evidência e como conviver com código antigo.",
          ["Adoção sem revolução: uma tarefa, um portão e um responsável por vez",
           "Código herdado: cercar antes de reescrever, medir antes de julgar",
           "Acordo de time: quem decide, quem revisa, quem assina a entrega"],
          "A oficina grande: várias bancadas compartilhando a mesma prateleira de ferramentas e o mesmo manual",
          "Plano de adoção em etapas com responsável e prazo, mais a cerca de proteção do módulo herdado",
          "Escolher uma tarefa de time, um responsável e um portão, e rodar assim por duas semanas",
          "O Painel de Pedidos vira rotina do time: quem opera, quem conserta e o que acontece quando o processo falha"),
        C(16, "Soberania: não ficar preso a fornecedor, modelo ou plataforma",
          "Proteger o que foi construído, garantindo que dados, regras e histórico continuem seus e que a troca de fornecedor seja uma decisão e não uma emergência.",
          ["O que precisa ser seu: dados, regras, portões e histórico do trabalho",
           "Trocar de modelo ou de ferramenta sem reescrever o processo inteiro",
           "Decidir por evidência: quando ficar, quando sair e como conduzir a mudança"],
          "A mesa de ferramentas intercambiáveis: a peça troca de lugar e o projeto continua funcionando",
          "Contrato de portabilidade do projeto: o que troca, o que permanece e o que precisa de teste antes da troca",
          "Testar a troca de um fornecedor ou modelo no seu projeto e registrar o custo real da mudança",
          "O Painel de Pedidos roda em dois ambientes diferentes sem que as regras de negócio sejam tocadas"),
    ]),
]

SUMARIO = {
    "titulo_obra": "As Quatro Camadas da Fábrica Agêntica",
    "titulo_capa": "As 4 Camadas da Fábrica Agêntica",
    "subtitulo": "Guia Prático Para Automatizar Um Projeto Real",
    "edition_tag": "v4.0 — Edição Prática",
    "tipo_obra": "livro",
    "tamanho_obra": "GG",
    "min_referencias_por_capitulo": 20,
    "senioridade_obra": "iniciante",
    "estilo_tecnica": "hibrido",
    "motivo_condutor": {
        "nome": "A Bancada do Projeto Vivo",
        "descricao": (
            "Você não lê este livro: você monta uma bancada. O mesmo projeto real "
            "fica sobre a mesa do capítulo 1 ao 16, e cada capítulo instala uma peça "
            "que continua no lugar até o fim. Nada de exemplo descartável: o que "
            "entra na bancada é usado de novo, todo capítulo, e é isso que faz o "
            "aprendizado grudar."
        ),
        "vocabulario": [
            "bancada", "projeto vivo", "peça instalada", "encaixe",
            "caderno de bancada", "lâmpada de teste", "disjuntor de bancada",
            "roteador de serviço", "usina de ferramentas", "certificado de bancada",
        ],
        "persona_leitor": "Engenheiro de Bancada",
    },
    "introducao": (
        "Mostrar a conta que o improviso com IA cobra de quem constrói de verdade, "
        "apresentar o Painel de Pedidos como caso âncora que atravessa a obra "
        "inteira e fixar a promessa concreta: ao final, o leitor tem um projeto real "
        "funcionando com as quatro camadas instaladas e evidência de resultado."
    ),
    "partes": [
        {"parte": p, "titulo_parte": tp, "capitulos": caps} for p, tp, caps in PARTES
    ],
    "metricas_obrigatorias": {
        "1": [{"metrica": "repositórios públicos que declararam uso de kits de desenvolvimento com modelos de linguagem", "valor": "1,1 milhão"}],
        "2": [{"metrica": "economia de custo de token de entrada com reaproveitamento de prefixo", "valor": "90%"}],
        "3": [{"metrica": "desenvolvedores que desconfiam da exatidão da saída gerada por IA", "valor": "46%"}],
        "4": [{"metrica": "desenvolvedores que usam ferramentas de IA no trabalho", "valor": "84%"}],
        "5": [{"metrica": "redução de latência com reaproveitamento de prefixo estável", "valor": "85%"}],
        "6": [{"metrica": "saturação do teste público de tarefas de programação", "valor": "93,9%"}],
        "7": [{"metrica": "resolução do mesmo modelo no teste privado após a suíte pública", "valor": "17,8%"}],
        "8": [{"metrica": "dependências referenciadas por código gerado que não existem", "valor": "20%"}],
        "9": [{"metrica": "amostras de código gerado por IA com vulnerabilidade conhecida", "valor": "45%"}],
        "10": [{"metrica": "taxa de aprovação de segurança do código gerado por IA", "valor": "56%"}],
        "11": [{"metrica": "adoção de engenharia de plataforma nos times pesquisados", "valor": "90%"}],
        "12": [{"metrica": "correções aceitas como corretas que não resolviam a tarefa", "valor": "7,2%"}],
        "13": [{"metrica": "confiança declarada na exatidão da saída de IA entre 2024 e 2025", "valor": "43% para 33%"}],
        "14": [{"metrica": "repositórios públicos que passaram a usar notebooks", "valor": "2,4 milhões"}],
        "15": [{"metrica": "desenvolvedores que usam ferramentas de IA no dia a dia", "valor": "84% dos desenvolvedores"}],
        "16": [{"metrica": "riscos específicos de IA generativa catalogados pelo perfil do NIST", "valor": "12 riscos"}],
    },
    "conclusao": (
        "Fechar o ciclo da bancada: o leitor termina com um projeto real funcionando, "
        "as quatro camadas instaladas, evidência de resultado e um caminho claro de "
        "manutenção para os próximos projetos."
    ),
}

DESTINO.write_text(json.dumps(SUMARIO, ensure_ascii=False, indent=2), encoding="utf-8")
total = sum(len(p["capitulos"]) for p in SUMARIO["partes"])
print(f"[ok] {DESTINO.name}: {len(SUMARIO['partes'])} partes, {total} capitulos")
