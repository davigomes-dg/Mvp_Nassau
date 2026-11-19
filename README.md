# Mvp_Nassau
# Notaê

> [A plataforma analisa as notas do Enem e a localização do usuário para indicar instituições de ensino superior nas quais ele pode concorrer a uma vaga.]

## Participantes

- **Integrante 1:** [Nome completo]
- **Integrante 2:** [Nome completo]
- **Integrante 3:** [Nome completo]
- **Integrante 4:** [Nome completo]

---

## 1. Visão Geral

### 1.1 Descrição do Projeto

[A proposta do projeto consiste no desenvolvimento de uma plataforma digital que utiliza as notas obtidas pelo usuário no Enem e sua localização para identificar as instituições de ensino superior nas quais ele poderá concorrer a uma vaga.]

### 1.2 Objetivo

[Descrever o principal resultado que o MVP pretende alcançar.]

### 1.3 Proposta de Valor

[A aplicação pode facilitar o acesso ao ensino superior ao ajudar estudantes a identificar instituições nas quais possam concorrer com base na nota do Enem e em sua localização, economizando tempo e apoiando escolhas mais informadas. Seu diferencial está em oferecer recomendações personalizadas que consideram esses dois fatores, reunindo opções relevantes de forma prática e acessível. As indicações devem ser entendidas como estimativas, pois os critérios de seleção e as notas de corte podem variar.]

---

## 2. Problema

### 2.1 Contexto

[A principal motivação para desenvolver a aplicação é ajudar estudantes a compreender e acompanhar suas possibilidades de ingresso no ensino superior. Com base na nota do Enem e na localização, a plataforma poderá indicar instituições nas quais tenham chances de concorrer a uma vaga, facilitando o planejamento e a escolha de onde se candidatar.]

### 2.2 Problema Identificado

[Estudantes que realizaram o Enem podem ter dificuldade para identificar quais instituições de ensino superior oferecem opções compatíveis com seu desempenho e sua localização. Comparar cursos, vagas, notas de corte e critérios de seleção pode exigir consultas a diferentes fontes e tornar mais difícil visualizar as possibilidades de ingresso.]

### 2.3 Soluções Existentes

[O aplicativo oficial do SiSU permite pesquisar vagas por curso, cidade e instituição, simular notas e consultar informações como vagas, pesos e modalidades de concorrência. Também existem simuladores, como o da Bernoulli, que comparam a nota do Enem com cursos e permitem filtrar resultados por cidade e modalidade. Aplicativo oficial do SiSU · Simulador Bernoulli

Essas soluções ajudam os estudantes a pesquisar oportunidades, mas seu alcance depende das instituições e dos dados disponíveis em cada processo seletivo. Por exemplo, o SiSU contempla instituições públicas participantes, e suas notas de corte servem como referência, sem garantir a aprovação. Informações do MEC sobre o SiSU · Orientações do Inep sobre notas de corte

Um possível diferencial da aplicação é combinar a nota do Enem e a localização para apresentar, em uma busca personalizada, opções relevantes ao estudante.]

### 2.4 Hipótese do MVP

[A hipótese do MVP é que, ao informar sua nota do Enem e sua localização, o estudante conseguirá visualizar com mais facilidade instituições e cursos que podem ser opções para concorrer a uma vaga. Isso poderá reduzir o tempo de pesquisa e apoiar a escolha de onde se candidatar. As indicações serão estimativas, não garantias de aprovação.]

---

## 3. Público-Alvo

### 3.1 Perfil dos Usuários

[O público-alvo principal são estudantes que realizaram o Enem e pretendem ingressar no ensino superior. A aplicação atende especialmente quem deseja descobrir opções de instituições próximas e compreender em quais delas seu desempenho pode ser competitivo]

### 3.2 Necessidades

[Os estudantes precisam compreender quais instituições e cursos podem ser opções de ingresso considerando seu desempenho no Enem e sua localização. Também precisam consultar e comparar as notas de corte disponíveis, que podem variar conforme o curso, a instituição e o processo seletivo. A aplicação deve apresentar essas informações de forma clara e indicar que os resultados são estimativas, não garantias de aprovação.]

### 3.3 Cenário de Utilização

[Após realizar o Enem, o estudante acessa a aplicação pelo computador ou celular e cria uma conta ou faz login. Em seguida, informa suas notas e localização. O sistema consulta os dados cadastrados sobre instituições, cursos e notas de corte, compara as informações e apresenta opções que podem ser compatíveis com o perfil do estudante. Ele pode usar os resultados para orientar sua busca e decidir onde se candidatar.]

---

## 4. Escopo do MVP

### 4.1 Funcionalidades Principais

- Cadastro e login: permitir que o usuário crie uma conta e acesse a aplicação.

- Entrada de dados: permitir que o usuário informe suas notas do Enem e sua localização.

- Consulta e comparação: comparar os dados informados com as notas de corte cadastradas para cursos e instituições.

- Apresentação dos resultados: exibir instituições e cursos que possam ser opções para o usuário, junto às informações usadas na comparação.

---

## 5. Arquitetura da Solução

### 5.1 Visão Arquitetural

[A aplicação será organizada em três componentes principais:

Front-end: apresenta as telas de cadastro e login, recebe as notas e a localização informadas pelo usuário e exibe os resultados.

Back-end: processa as solicitações do front-end, autentica o usuário, valida os dados recebidos, consulta o banco de dados e prepara as informações que serão enviadas à aplicação.

Banco de dados: armazena os dados dos usuários e suas notas, além das instituições, dos cursos e das respectivas notas de corte. Quando disponíveis, os dados podem incluir o ano do processo seletivo e a modalidade de concorrência.]

### 5.2 Fluxo Principal

[1 - O usuário cria uma conta ou faz login.

2 - Informa suas notas do Enem e sua localização.

3 - O back-end valida a solicitação e consulta no banco de dados as instituições, os cursos e as notas de corte correspondentes.

4 - A aplicação compara as informações e apresenta ao usuário as opções identificadas como possíveis.]

## 5.2 Fluxo Principal

1 - Cadastro ou login: o usuário cria uma conta ou informa suas credenciais. O front-end envia os dados ao back-end, que realiza a autenticação.

2 - Entrada de dados: o usuário informa suas notas do Enem e sua localização.

3 - Consulta e análise: o back-end valida os dados, consulta no banco as instituições, os cursos e as notas de corte correspondentes e compara essas informações.

4 - Exibição dos resultados: o front-end apresenta as opções encontradas, indicando que são estimativas de compatibilidade e não garantias de aprovação.

---

## 6. Tecnologias Utilizadas

| Categoria | Tecnologia | Finalidade |
|-----------|------------|------------|
| Linguagem de Programação | Python | Processar as informações da aplicação. |
| Front-end | HTML, CSS e JavaScript | Criar as páginas, definir sua aparência e permitir interações com o usuário. |
| Back-end | Python com Flask | Receber os dados, realizar o login e consultar o banco de dados. |
| Banco de Dados | SQLite | Armazenar usuários, notas do Enem, instituições, cursos e notas de corte. |
| Ferramentas | VS Code, GitHub e Figma | Escrever o código, guardar o projeto e planejar as telas. |

---

## 7. Requisitos

### 7.1 Requisitos Funcionais

- **RF01:** O sistema deve permitir que o usuário crie uma conta e faça login.
- **RF02:** O sistema deve permitir que o usuário informe suas notas do Enem e sua localização.
- **RF03:** O sistema deve comparar os dados informados com as notas de corte cadastradas e apresentar instituições e cursos que possam ser opções para o usuário.

### 7.2 Requisitos Não Funcionais

- **RNF01:** A busca por instituições e cursos deve apresentar os resultados em até cinco segundos, em condições normais de uso.
- **RNF02:** O sistema deve proteger as senhas e permitir que cada usuário acesse somente os próprios dados.
- **RNF03:** A interface deve usar linguagem clara, orientar o preenchimento dos dados e funcionar em computadores e celulares.
