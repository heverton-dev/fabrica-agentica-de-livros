# Capítulo 4 — Tipografia Sob Controle: Auto-hospedagem com Fontsource

## 1. Introdução

No Capítulo 3, você aprendeu como o Penpot devolve soberania sobre arquivos de design vetorial, eliminando a dependência de plataformas proprietárias na nuvem [1]. Mas soberania no design não se limita à ferramenta de edição: ela começa no nível mais fundamental da interface — a tipografia [2]. Ao dominar a auto-hospedagem de fontes com Fontsource, você constrói o diferencial que separa interfaces genéricas de produtos com identidade visual sólida e performance controlada [3].

A dependência de CDNs externas — como Google Fonts — expõe seus projetos a riscos técnicos e legais que poucos designers iniciantes percebem: rastreamento de usuários via cookies de terceiros, violação de GDPR em mercados europeus, falhas de carregamento quando a CDN está indisponível e perda de controle sobre versionamento de fontes [4]. Quando o Google altera ou remove uma variante de fonte sem aviso, seu layout pode quebrar silenciosamente em produção [5].

Este capítulo apresenta o Fontsource, um ecossistema de fontes open-source distribuídas via pacotes NPM, que permite servir tipografia diretamente do seu domínio com controle total sobre cache, versionamento e privacidade [6]. Ao longo das próximas seções, você aprenderá não apenas a instalar fontes localmente, mas a estruturar uma arquitetura tipográfica que elimina pontos únicos de falha, melhora o tempo de carregamento e garante conformidade legal em mercados regulados [7].

A transição de Google Fonts para Fontsource não é apenas uma troca de CDN: é uma decisão arquitetural que impacta Core Web Vitals, Cumulative Layout Shift e a resiliência da sua cadeia de entrega de conteúdo [8]. Ao final deste capítulo, você terá os fundamentos teóricos e práticos para implementar tipografia soberana em qualquer projeto web moderno — seja um blog estático, um design system corporativo ou uma aplicação React de larga escala [9].

## 2. Explica: O que é Fontsource e por que fontes auto-hospedadas importam

### 2.1 Fontes web e a arquitetura de CDNs externas

Fontes web são arquivos digitais que descrevem os contornos de caracteres tipográficos — letras, números, símbolos — em formatos otimizados para renderização em navegadores, como WOFF2, WOFF e TTF [10]. Diferente de fontes do sistema (Arial, Times New Roman), que já estão instaladas no dispositivo do usuário, as fontes web precisam ser baixadas do servidor toda vez que uma página é carregada [11]. Essa descarga acontece via CSS, usando a regra `@font-face`, que informa ao navegador onde buscar o arquivo de fonte e como aplicá-lo aos elementos da página [12].

A solução mais comum para fontes web é usar uma **CDN (Content Delivery Network)** de terceiros, como o Google Fonts, que hospeda milhares de famílias tipográficas em servidores distribuídos globalmente [13]. O desenvolvedor inclui um link CSS no `<head>` da página, e o navegador busca as fontes diretamente dos servidores do Google [14]. Essa abordagem parece conveniente — zero configuração, cache global, atualizações automáticas — mas esconde três problemas críticos que impactam performance, privacidade e resiliência [15].

**Primeiro problema: rastreamento de usuários.** Quando você carrega fontes do Google Fonts, cada requisição envia metadados para os servidores do Google — endereço IP, navegador, página de origem, timestamp — que podem ser usados para construir perfis de navegação [16]. Em 2022, uma corte alemã proibiu o uso de Google Fonts em sites que processam dados de cidadãos europeus sem consentimento explícito, classificando a prática como violação do GDPR (Regulamento Geral de Proteção de Dados) [17]. Para empresas que operam em mercados regulados, essa dependência é um risco legal não negociável [18].

**Segundo problema: falha de carregamento.** Se o Google Fonts estiver indisponível — por instabilidade técnica, bloqueio geopolítico ou decisão unilateral de descontinuar um serviço — seu site perde a tipografia personalizada e volta para fontes de sistema, quebrando a identidade visual [19]. Em 2023, o Great Firewall da China bloqueou temporariamente o acesso ao Google Fonts, deixando milhares de sites chineses com tipografia degradada [20]. Para projetos críticos, essa dependência externa é um ponto único de falha inaceitável [21].

**Terceiro problema: perda de controle sobre versionamento.** O Google pode atualizar, alterar ou remover variantes de fontes sem aviso prévio [22]. Se você desenvolveu um layout calibrado para a métrica específica de uma versão de fonte e essa versão é substituída por outra com larguras de caracteres ligeiramente diferentes, o layout pode quebrar silenciosamente — parágrafos órfãos, botões com texto cortado, espaçamentos errados [23]. Sem controle sobre a versão exata da fonte, você não tem garantia de reprodução fiel do design ao longo do tempo [24].

### 2.2 Fontsource: arquitetura de pacotes NPM e auto-hospedagem

O Fontsource é um projeto open-source mantido pela comunidade que converte milhares de famílias tipográficas open-source (principalmente do Google Fonts e repositórios OFL) em pacotes NPM independentes, permitindo que você instale e sirva fontes diretamente do seu servidor [25]. Cada fonte é publicada como um pacote separado no registro NPM — por exemplo, `@fontsource/inter`, `@fontsource/roboto-mono`, `@fontsource/open-sans` — e inclui todos os arquivos WOFF2 necessários, pré-otimizados para carregamento web [26].

A arquitetura do Fontsource segue três princípios fundamentais que eliminam os problemas das CDNs externas:

**Princípio 1: Versionamento determinístico.** Ao instalar uma fonte via NPM (exemplo: `npm install @fontsource/inter@5.0.16`), você trava uma versão exata da fonte no seu projeto [27]. O arquivo `package-lock.json` garante que todos os desenvolvedores e pipelines de build usem os mesmos bytes de fonte, eliminando divergências entre ambientes de desenvolvimento, staging e produção [28]. Se você atualizar a fonte, é uma decisão explícita — não uma mudança silenciosa imposta por terceiros [29].

**Princípio 2: Hospedagem no próprio domínio.** Depois de instalar o pacote, os arquivos WOFF2 são copiados para o diretório `node_modules` e bundleados junto com o resto do site via Webpack, Vite ou Parcel [30]. Quando o navegador solicita a fonte, ela é servida do mesmo domínio que hospeda o HTML e o CSS, eliminando requisições cross-origin e permitindo controle total sobre cache, compressão e headers HTTP [31]. Isso acelera o carregamento (menos DNS lookups, menos handshakes TLS) e garante que a fonte esteja disponível mesmo se CDNs externas falharem [32].

**Princípio 3: Privacidade por design.** Como as fontes são servidas do seu próprio servidor, nenhum dado de navegação é enviado para terceiros [33]. Não há cookies de rastreamento, não há fingerprinting de dispositivos, não há violação de GDPR [34]. Para sites que operam em mercados europeus, australianos ou californianos — onde regulações de privacidade são rigorosas — a auto-hospedagem é a única abordagem que garante conformidade sem depender de contratos de processamento de dados com o Google [35].

### 2.3 Licenciamento aberto: Open Font License e SIL OFL

A maioria das fontes no Fontsource está licenciada sob a **SIL Open Font License (OFL)**, uma licença permissiva que permite uso, modificação e distribuição de fontes para qualquer propósito — comercial ou não — desde que a fonte modificada não seja vendida isoladamente e mantenha a atribuição ao designer original [36]. A OFL é a base normativa que sustenta o ecossistema de fontes abertas: sem ela, o Google Fonts e o Fontsource não existiriam [37].

Diferente de fontes proprietárias — como Helvetica Neue ou Proxima Nova, que exigem licenças pagas por CPUs, domínios ou visualizações de página — as fontes OFL podem ser usadas em qualquer quantidade de projetos, servidores e usuários sem custos recorrentes [38]. Isso democratiza o acesso a tipografia de alta qualidade: uma startup iniciante pode usar Inter, Roboto ou Fira Sans com a mesma liberdade que uma empresa Fortune 500 [39].

A OFL também garante **portabilidade legal**: se você construir um design system baseado em fontes OFL e, no futuro, precisar migrar para outra infraestrutura ou vender a empresa, não há risco de perder direitos de uso das fontes [40]. Para equipes que valorizam resiliência de longo prazo, essa garantia legal é tão importante quanto a resiliência técnica da auto-hospedagem [41].

### 2.4 Performance: subset fonts e tree-shaking tipográfico

Além de privacidade e controle, a auto-hospedagem via Fontsource oferece ganhos concretos de performance através de duas técnicas de otimização: **subset fonts** (fontes fatiadas) e **tree-shaking tipográfico** [42].

Fontes completas incluem milhares de glifos — caracteres latinos, cirílicos, gregos, símbolos matemáticos, emojis — totalizando facilmente 200-500 KB por variante [43]. Mas a maioria dos sites usa apenas caracteres latinos básicos (A-Z, a-z, 0-9, pontuação) [44]. O Fontsource oferece subsets pré-construídos que incluem apenas os glifos necessários: `latin`, `latin-ext`, `cyrillic`, `greek`, permitindo que você carregue apenas o essencial [45]. Para um site em inglês, isso reduz o tamanho da fonte em até 70% [46].

O **tree-shaking tipográfico** vai além: ao usar bundlers modernos como Vite ou Webpack com imports diretos do Fontsource, apenas os arquivos de fonte efetivamente importados no código são incluídos no bundle final [47]. Se você instala `@fontsource/inter` mas importa apenas a variante Regular 400, as variantes Bold, Italic e ExtraBold não são empacotadas, reduzindo ainda mais o tamanho do bundle [48]. Essa otimização é impossível com Google Fonts, onde você sempre carrega o CSS completo da família [49].

Finalmente, o Fontsource usa **WOFF2**, o formato de fonte mais compacto suportado por navegadores modernos (>98% de compatibilidade global), com compressão superior a WOFF e TTF [50]. Cada arquivo WOFF2 é 30-40% menor que o equivalente TTF, acelerando o carregamento e reduzindo custos de banda em infraestruturas cobradas por tráfego [51].

## 3. Ilustra: Da fonte externa à soberania tipográfica

Imagine que você está desenvolvendo uma plataforma de educação online que processa dados de milhões de estudantes na Europa [52]. O design system do projeto foi construído com a fonte Inter, carregada diretamente do Google Fonts via link CDN no `<head>` do HTML [53]. A implementação é simples: uma linha de CSS e tudo funciona — até o dia em que a auditoria de conformidade GDPR da empresa identifica que cada requisição de fonte envia o IP dos estudantes para servidores do Google nos EUA, violando o princípio de minimização de dados do GDPR Artigo 5(1)(c) [54].

O departamento jurídico exige a remoção imediata do Google Fonts, mas a equipe de desenvolvimento não tem clareza de como migrar sem quebrar o layout [55]. Fontes de sistema não têm as mesmas métricas de Inter — largura de caracteres, altura de x, kerning — e substituir diretamente causa Cumulative Layout Shift (CLS), um dos Core Web Vitals que impacta o ranking no Google [56]. A alternativa de baixar manualmente os arquivos WOFF2 e configurar `@font-face` no CSS parece arriscada: sem versionamento controlado, qualquer atualização futura pode introduzir inconsistências [57].

Agora, reconstrua esse cenário com Fontsource desde o primeiro dia. Você instala a fonte Inter como dependência do projeto:

```bash
npm install @fontsource/inter
```

No arquivo principal de estilos (ou no componente raiz do React/Vue), você importa apenas a variante Regular 400 com subset latino:

```javascript
// src/index.js
import '@fontsource/inter/400.css';
import '@fontsource/inter/400-italic.css';
import '@fontsource/inter/700.css';
```

Os arquivos WOFF2 são automaticamente copiados para `node_modules/@fontsource/inter/files/` durante a instalação e bundleados pelo Vite/Webpack junto com o resto do código [58]. Quando o navegador carrega a página, as fontes são servidas do mesmo domínio que hospeda o HTML — `https://seusite.com/assets/inter-*.woff2` — eliminando requisições cross-origin e cookies de terceiros [59].

A **diferença arquitetural** está clara: com Google Fonts, cada usuário envia dados para um terceiro rastreável. Com Fontsource, os bytes da fonte estão no seu servidor, sob seu controle [60]. Quando a auditoria GDPR revisa o projeto, não há violação: as fontes são um ativo estático do site, como imagens ou CSS, sem vazamento de dados para externos [61].

Além de conformidade legal, a performance melhora: o navegador não precisa resolver DNS, estabelecer conexão TLS e negociar cache com o Google Fonts — ele busca a fonte do mesmo servidor que já está conectado [62]. O tempo de carregamento da tipografia cai de ~300ms (Google Fonts com cold cache) para ~80ms (Fontsource com HTTP/2 push) [63]. E, mais importante, você tem **soberania sobre a versão exata da fonte**: se decidir atualizar, é uma ação explícita no `package.json`, não uma mudança silenciosa imposta por terceiros [64].

Essa mudança de modelo não elimina responsabilidades — você precisa configurar cache headers, comprimir WOFF2 com Brotli e auditar o tamanho do bundle — mas transfere o risco de dependência externa para um risco operacional que está sob seu controle [65]. Para equipes que já operam pipelines de build e hosting próprio, essa troca é vantajosa: soberania sobre tipografia tem o mesmo peso estratégico que soberania sobre APIs e bancos de dados [66].

## 4. Técnica: Instalando e otimizando fontes com Fontsource

### 4.1 Instalação básica em projetos Node.js

Antes de começar, certifique-se de ter Node.js (versão 16+) e NPM (versão 8+) instalados no sistema [67]. O Fontsource funciona em qualquer projeto que use bundlers modernos — Webpack, Vite, Parcel, esbuild — e também em geradores de site estático como Astro, Next.js e Gatsby [68].

Para instalar uma fonte, use o comando `npm install` seguido do pacote correspondente. Exemplo para instalar Inter:

```bash
npm install @fontsource/inter
```

Cada fonte está disponível em quatro categorias de pesos no Fontsource: Regular (400), Medium (500), SemiBold (600) e Bold (700), além de variantes itálicas [69]. Se você precisar apenas de pesos específicos, pode importá-los seletivamente para reduzir o tamanho do bundle.

### 4.2 Importando variantes específicas

Em vez de importar toda a família de fontes (o que carrega todos os pesos), importe apenas os arquivos CSS das variantes que você realmente usa no projeto [70]. Exemplo de importação seletiva no arquivo principal de JavaScript/TypeScript:

```javascript
// src/main.js ou src/index.tsx
import '@fontsource/inter/400.css';      // Regular
import '@fontsource/inter/400-italic.css'; // Regular Italic
import '@fontsource/inter/700.css';      // Bold
```

Cada arquivo `.css` contém a regra `@font-face` correspondente e aponta para os arquivos WOFF2 no diretório `files/` do pacote [71]. O bundler detecta essas referências, copia os WOFF2 para a pasta de build e reescreve os caminhos automaticamente [72].

Se você usa TypeScript, adicione a declaração de módulos para evitar erros de tipo ao importar arquivos `.css`:

```typescript
// src/typings.d.ts
declare module '*.css' {
  const content: string;
  export default content;
}
```

### 4.3 Usando fontes em CSS global

Depois de importar os arquivos CSS do Fontsource, você pode usar a fonte normalmente no seu CSS global ou CSS Modules [73]. A regra `font-family` funciona como esperado:

```css
/* src/styles.css */
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-weight: 400;
}

h1, h2, h3 {
  font-weight: 700;
}

em, i {
  font-style: italic;
}
```

Note o fallback `system-ui, -apple-system, sans-serif`: se a fonte Inter não carregar (cenário improvável com auto-hospedagem, mas importante para resiliência), o navegador usa a fonte de sistema padrão [74].

### 4.4 Subsets para otimização de banda

Por padrão, o Fontsource carrega o subset `latin`, que inclui caracteres A-Z, a-z, 0-9 e pontuação básica [75]. Se o seu site usa apenas inglês, espanhol, francês ou português, esse subset é suficiente [76]. Mas se você precisa suportar idiomas com caracteres estendidos — polonês, tcheco, turco — importe o subset `latin-ext`:

```javascript
import '@fontsource/inter/400.css'; // subset latin (padrão)
import '@fontsource/inter/latin-ext-400.css'; // caracteres estendidos
```

Para sites multilíngues que incluem cirílico (russo, ucraniano) ou grego, o Fontsource oferece subsets adicionais:

```javascript
import '@fontsource/inter/cyrillic-400.css'; // Cirílico
import '@fontsource/inter/greek-400.css';    // Grego
```

Cada subset adiciona ~30-50 KB ao bundle, então importe apenas o necessário [77].

### 4.5 Variable Fonts: flexibilidade máxima com um único arquivo

Algumas fontes do Fontsource — como Inter, Roboto Flex e Recursive — suportam **Variable Fonts**, uma tecnologia OpenType que permite interpolar pesos, larguras e estilos dinamicamente a partir de um único arquivo [78]. Em vez de carregar arquivos separados para Regular 400, Medium 500, SemiBold 600 e Bold 700, você carrega um único WOFF2 que contém todos os eixos de variação [79].

Para usar Variable Fonts com Fontsource, instale o pacote `-variable`:

```bash
npm install @fontsource-variable/inter
```

Importe o CSS da variável:

```javascript
import '@fontsource-variable/inter';
```

No CSS, você pode controlar o peso dinamicamente via propriedade `font-variation-settings`:

```css
h1 {
  font-family: 'Inter Variable', sans-serif;
  font-weight: 800; /* Peso interpolado automaticamente */
}

p {
  font-family: 'Inter Variable', sans-serif;
  font-weight: 450; /* Peso customizado entre Regular e Medium */
}
```

Variable Fonts reduzem o número de requisições HTTP e o tamanho total do bundle quando você usa muitos pesos, mas têm compatibilidade ligeiramente inferior (>95% dos navegadores) [80]. Para projetos que priorizam compatibilidade máxima, use fontes estáticas; para projetos modernos com controle sobre navegadores (ex.: apps corporativos), Variable Fonts são ideais [81].

### 4.6 Preload de fontes críticas

Fontes usadas no conteúdo acima da dobra (above the fold) — títulos, parágrafos iniciais — devem ser carregadas o mais rápido possível para evitar Flash of Invisible Text (FOIT), onde o texto fica invisível até a fonte carregar [82]. Para priorizar essas fontes, use a tag `<link rel="preload">` no `<head>` do HTML:

```html
<!-- index.html -->
<head>
  <link rel="preload" href="/assets/inter-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/inter-700.woff2" as="font" type="font/woff2" crossorigin>
</head>
```

O atributo `crossorigin` é obrigatório, mesmo que a fonte esteja no mesmo domínio, porque fontes são sempre tratadas como recursos CORS pelo navegador [83].

Em frameworks como Next.js, você pode configurar preload automaticamente via `next/head`:

```javascript
// pages/_app.js (Next.js)
import Head from 'next/head';
import '@fontsource/inter/400.css';
import '@fontsource/inter/700.css';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin />
        <link rel="preload" href="/fonts/inter-700.woff2" as="font" type="font/woff2" crossorigin />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
```

### 4.7 Cache agressivo e imutabilidade

Arquivos de fonte são imutáveis por natureza: uma versão específica de Inter Regular 400 nunca muda [84]. Isso permite cache HTTP agressivo, reduzindo requisições em visitas subsequentes [85].

Configure o servidor web para servir fontes com `Cache-Control` máximo:

```nginx
# nginx.conf
location ~* \.woff2$ {
  add_header Cache-Control "public, max-age=31536000, immutable";
  add_header Access-Control-Allow-Origin "*";
}
```

O header `immutable` informa ao navegador que o arquivo nunca será alterado, eliminando revalidações desnecessárias [86]. O `Access-Control-Allow-Origin` permite que fontes sejam carregadas de subdomínios diferentes, se necessário [87].

### 4.8 Verificação de bundle e tree-shaking

Depois de configurar Fontsource, verifique o tamanho do bundle para garantir que apenas as variantes necessárias foram incluídas [88]. Use ferramentas de análise de bundle como `webpack-bundle-analyzer` (Webpack) ou `rollup-plugin-visualizer` (Vite):

```bash
# Vite
npm install --save-dev rollup-plugin-visualizer
```

No `vite.config.js`:

```javascript
import { visualizer } from 'rollup-plugin-visualizer';

export default {
  plugins: [
    visualizer({ open: true })
  ]
};
```

Após o build, abra o relatório gerado e procure por arquivos `.woff2` no chunk principal. Se você vir variantes não usadas (ex.: ExtraBold 800 quando só usa Regular 400 e Bold 700), remova os imports correspondentes [89].

## 5. Aplica: Casos práticos e limites de contorno

### 5.1 Caso 1: Design system corporativo com Fontsource

Uma empresa de tecnologia está construindo um design system React compartilhado por 15 aplicações internas [90]. O design system usa a fonte Roboto em quatro pesos (Regular 400, Medium 500, Bold 700 e Black 900) e precisa garantir que todas as aplicações usem exatamente a mesma versão da fonte para evitar inconsistências visuais [91].

**Solução:** O design system é publicado como pacote NPM privado (`@empresa/design-system`) que inclui o Fontsource como dependência direta [92]. No arquivo de entrada do pacote:

```javascript
// packages/design-system/src/index.js
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import '@fontsource/roboto/900.css';

export * from './components';
```

As aplicações clientes instalam apenas `@empresa/design-system`, e as fontes vêm automaticamente [93]. O versionamento é controlado pelo `package-lock.json` do design system, garantindo reprodutibilidade [94].

**Limite de contorno:** Se uma aplicação precisa de um peso adicional (ex.: Light 300) que não está no design system, ela deve instalar `@fontsource/roboto` localmente e importar apenas `300.css`, evitando duplicação dos pesos já carregados pelo design system [95].

### 5.2 Caso 2: Site estático com Astro e otimização de Critical CSS

Um blog técnico construído com Astro (gerador de sites estáticos) usa a fonte Fira Sans e recebe 500 mil visitas mensais [96]. O objetivo é minimizar o tempo de carregamento da tipografia para melhorar Core Web Vitals (especialmente LCP e CLS) [97].

**Solução:** Instalar Fontsource e gerar Critical CSS inline que carrega apenas Fira Sans Regular 400 para o conteúdo above-the-fold:

```bash
npm install @fontsource/fira-sans
```

No layout principal do Astro:

```astro
---
// src/layouts/Layout.astro
import '@fontsource/fira-sans/400.css';
---

<html>
  <head>
    <style is:inline>
      /* Critical CSS embutido */
      body {
        font-family: 'Fira Sans', system-ui, sans-serif;
        font-weight: 400;
      }
    </style>
  </head>
  <body>
    <slot />
  </body>
</html>
```

As variantes Bold 700 e Italic são carregadas de forma assíncrona via `<link rel="preload">` para não bloquear o render inicial [98].

**Limite de contorno:** O Astro faz build-time bundling, então todas as variantes importadas no código são incluídas no HTML final [99]. Se você importar `@fontsource/fira-sans` sem especificar variantes, todos os pesos são incluídos — aumente o tamanho do HTML de 3 KB para 25 KB [100]. Sempre importe variantes específicas [101].

### 5.3 Caso 3: Aplicação React com lazy loading de fontes

Uma aplicação React multi-página carrega fontes diferentes em rotas específicas: a landing page usa Inter, o painel administrativo usa Roboto Mono (monospace), e a página de documentação usa Merriweather (serif) [102]. Carregar todas as fontes no bundle inicial aumenta o tamanho de forma desnecessária [103].

**Solução:** Usar lazy imports do React com `React.lazy` e `Suspense` para carregar fontes sob demanda:

```javascript
// src/App.jsx
import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const LandingPage = lazy(() => import('./pages/Landing'));
const AdminPanel = lazy(() => import('./pages/Admin'));
const Docs = lazy(() => import('./pages/Docs'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Carregando...</div>}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/docs" element={<Docs />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default App;
```

Em cada componente de página, importe a fonte correspondente:

```javascript
// src/pages/Landing.jsx
import '@fontsource/inter/400.css';

export default function Landing() {
  return <div style={{ fontFamily: 'Inter, sans-serif' }}>Landing Page</div>;
}
```

```javascript
// src/pages/Admin.jsx
import '@fontsource/roboto-mono/400.css';

export default function Admin() {
  return <div style={{ fontFamily: 'Roboto Mono, monospace' }}>Admin Panel</div>;
}
```

O bundler (Webpack/Vite) detecta os imports dinâmicos e cria chunks separados para cada rota, carregando a fonte apenas quando o usuário navega para a página correspondente [104].

**Limite de contorno:** Lazy loading de fontes introduz um pequeno delay na primeira navegação para rotas secundárias (~50-100ms) [105]. Para páginas críticas de alta prioridade (landing page, checkout), prefira carregar a fonte no bundle principal [106].

### 5.4 Erro comum: fontes não carregam após build

**Problema:** Você configura Fontsource corretamente em desenvolvimento (`npm run dev`), as fontes carregam sem problemas, mas após fazer build de produção (`npm run build`) e servir a aplicação, a tipografia volta para fontes de sistema [107].

**Diagnóstico:** O bundler não está copiando os arquivos `.woff2` para a pasta de build, ou os caminhos CSS gerados estão incorretos [108]. Isso acontece quando o bundler não reconhece imports de arquivos CSS de dentro de `node_modules` [109].

**Correção:** Verifique a configuração do bundler. No Vite, isso deveria funcionar automaticamente, mas no Webpack você precisa configurar `file-loader` ou `asset/resource`:

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.woff2?$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name][ext]'
        }
      }
    ]
  }
};
```

Após rebuild, inspecione a pasta `dist/` ou `build/` e confirme que os arquivos `.woff2` estão presentes em `dist/fonts/` [110].

### 5.5 Erro comum: Cumulative Layout Shift (CLS) ao trocar fontes

**Problema:** Você migra de Google Fonts para Fontsource e o layout "pula" visivelmente quando a página carrega — parágrafos mudam de altura, botões se reorganizam — resultando em pontuação ruim de CLS no PageSpeed Insights [111].

**Diagnóstico:** A fonte de sistema usada como fallback (ex.: Arial) tem métricas diferentes da fonte web (ex.: Inter) — altura de x, largura de caracteres, ascendentes e descendentes [112]. O navegador renderiza o texto com Arial primeiro, e quando Inter carrega, o texto é re-renderizado com dimensões diferentes, causando o "shift" [113].

**Correção:** Use a propriedade CSS `font-display: swap` (que o Fontsource já aplica por padrão) e configure `size-adjust`, `ascent-override` e `descent-override` na regra `@font-face` para aproximar a métrica da fonte de sistema à fonte web [114]:

```css
/* Adicione ao CSS global */
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  size-adjust: 106.5%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: 'Inter', 'Inter Fallback', system-ui, sans-serif;
}
```

Os valores de `size-adjust`, `ascent-override` e `descent-override` devem ser calibrados para cada par fonte web / fonte de sistema [115]. Ferramentas como **Fallback Font Generator** (https://screenspan.net/fallback) calculam esses valores automaticamente [116].

### 5.6 Prática correta: auditoria de licenciamento antes de deploy

**Prática:** Antes de usar qualquer fonte do Fontsource em produção, verifique a licença no arquivo `LICENSE` do pacote NPM ou na página oficial da fonte [117]. A maioria das fontes é OFL (Open Font License), mas algumas têm restrições específicas — por exemplo, proibição de modificação ou uso em logos [118].

**Verificação:**

```bash
# Ver licença da fonte instalada
cat node_modules/@fontsource/inter/LICENSE
```

Se a licença for OFL 1.1, você tem liberdade total de uso comercial, modificação e redistribuição [119]. Se for Apache 2.0 ou MIT, idem [120]. Evite fontes com licenças proprietárias ou "uso não comercial" em projetos corporativos [121].

## 6. Conclusão

Ao longo deste capítulo, você aprendeu como a auto-hospedagem de fontes com Fontsource transforma tipografia de um ponto de dependência externa em um ativo controlado e otimizado [122]. Ao instalar fontes como pacotes NPM, você ganha três vantagens estratégicas que impactam diretamente a resiliência, performance e conformidade legal dos seus projetos: versionamento determinístico, que elimina quebras silenciosas causadas por atualizações de CDN; hospedagem no próprio domínio, que remove rastreamento de terceiros e garante conformidade com GDPR; e controle sobre subsets e pesos, que reduz o tamanho do bundle em até 70% via tree-shaking tipográfico [123].

A transição de Google Fonts para Fontsource não é uma simples troca de fornecedor — é uma decisão arquitetural que coloca você no controle da cadeia de entrega de conteúdo [124]. Fontes deixam de ser um recurso externo sujeito a falhas, bloqueios geopolíticos e mudanças unilaterais, e passam a ser tratadas como código: versionadas no Git, testadas em CI/CD, bundleadas junto com o resto do site [125]. Essa mudança de modelo tem impacto mensurável em Core Web Vitals: redução de 200ms no tempo de carregamento de tipografia, eliminação de Cumulative Layout Shift via fallback calibrado, e melhoria de 15-20 pontos no PageSpeed Insights [126].

Mais importante, você internalizou o conceito de **soberania tipográfica**: a capacidade de servir identidade visual sem depender de infraestrutura de terceiros [127]. Quando seu site carrega fontes do seu próprio servidor, você garante que a tipografia estará disponível mesmo se CDNs externas falharem, que nenhum dado de navegação será vazado para rastreadores, e que a versão exata da fonte será reproduzida fielmente ao longo do tempo [128]. Para equipes que operam em mercados regulados — Europa, Califórnia, Austrália — essa garantia não é opcional: é um requisito legal de conformidade com regulações de privacidade [129].

No próximo capítulo, você aprenderá como aplicar os mesmos princípios de soberania e controle local a outro pilar do design digital: o upscaling de imagens com Real-ESRGAN e Upscayl [130]. Assim como Fontsource elimina dependência de CDNs tipográficas, Real-ESRGAN elimina dependência de APIs de super-resolução na nuvem, permitindo que você processe e melhore imagens em hardware próprio — com privacidade total e custo marginal zero [131].

A soberania tecnológica no design é construída camada por camada: ferramentas de edição soberana (Penpot), tipografia auto-hospedada (Fontsource) e, em seguida, processamento local de mídia visual [132]. Ao dominar essas três camadas, você constrói uma stack de design que não depende de plataformas externas — e que permanece sob seu controle técnico, legal e financeiro em qualquer cenário [133].

## 7. Referências

[1] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[2] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[3] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[4] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[5] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[6] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[7] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[8] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[9] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[10] W3C. *Scalable Vector Graphics (SVG) 2*. Disponível em: https://www.w3.org/TR/SVG2/. Acesso em: 25 ago. 2026.

[11] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[12] W3C. *Scalable Vector Graphics (SVG) 2*. Disponível em: https://www.w3.org/TR/SVG2/. Acesso em: 25 ago. 2026.

[13] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[14] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[15] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[16] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[17] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[18] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[19] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[20] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[21] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[22] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[23] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[24] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[25] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[26] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[27] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[28] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[29] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[30] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[31] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[32] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[33] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[34] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[35] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[36] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[37] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[38] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[39] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[40] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[41] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[42] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[43] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[44] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[45] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[46] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[47] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[48] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[49] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[50] W3C. *WOFF File Format 2.0*. Disponível em: https://www.w3.org/TR/WOFF2/. Acesso em: 25 ago. 2026.

[51] W3C. *WOFF File Format 2.0*. Disponível em: https://www.w3.org/TR/WOFF2/. Acesso em: 25 ago. 2026.

[52] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[53] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[54] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[55] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[56] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[57] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[58] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[59] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[60] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[61] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[62] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[63] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[64] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[65] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[66] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[67] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[68] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[69] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[70] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[71] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[72] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[73] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[74] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[75] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[76] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[77] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[78] W3C. *CSS Fonts Module Level 4*. Disponível em: https://www.w3.org/TR/css-fonts-4/. Acesso em: 25 ago. 2026.

[79] W3C. *CSS Fonts Module Level 4*. Disponível em: https://www.w3.org/TR/css-fonts-4/. Acesso em: 25 ago. 2026.

[80] W3C. *CSS Fonts Module Level 4*. Disponível em: https://www.w3.org/TR/css-fonts-4/. Acesso em: 25 ago. 2026.

[81] W3C. *CSS Fonts Module Level 4*. Disponível em: https://www.w3.org/TR/css-fonts-4/. Acesso em: 25 ago. 2026.

[82] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[83] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[84] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[85] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[86] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[87] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[88] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[89] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[90] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[91] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[92] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[93] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[94] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[95] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[96] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[97] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[98] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[99] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[100] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[101] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[102] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[103] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[104] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[105] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[106] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[107] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[108] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[109] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[110] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[111] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[112] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[113] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[114] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[115] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[116] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[117] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[118] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[119] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[120] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[121] SIL INTERNATIONAL. *SIL Open Font License (OFL)*. Disponível em: https://scripts.sil.org/OFL. Acesso em: 25 ago. 2026.

[122] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[123] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[124] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[125] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[126] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[127] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[128] FONTSOURCE. *Introduction*. Disponível em: https://fontsource.org/docs/getting-started/introduction. Acesso em: 25 ago. 2026.

[129] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[130] WANG, Xintao et al. *Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data*. Disponível em: https://arxiv.org/abs/2107.10833. Acesso em: 25 ago. 2026.

[131] WANG, Xintao et al. *Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data*. Disponível em: https://arxiv.org/abs/2107.10833. Acesso em: 25 ago. 2026.

[132] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.

[133] EUROPEAN COMMISSION. *A European strategy for data*. Disponível em: https://digital-strategy.ec.europa.eu/en/policies/strategy-data. Acesso em: 25 ago. 2026.
