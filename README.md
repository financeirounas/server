# Documentação de Features - Sistema de Gestão de Segurança Alimentar e Logística Social

## Visão Geral

Este documento descreve todas as features implementadas no frontend e suas respectivas rotas de API no backend. O sistema é composto por um frontend Next.js que se comunica com um backend FastAPI através de rotas intermediárias (API Routes do Next.js).

### Arquitetura

-**Frontend**: Next.js (React) com API Routes intermediárias

-**Backend**: FastAPI (Python)

-**Autenticação**: JWT (JSON Web Tokens)

-**Comunicação**: Frontend → Next.js API Routes → Backend FastAPI

---

## Autenticação e Autorização

### 1. Login

**Página**: `/auth/login`

**Componente**: `login-desktop.jsx` / `login-mobile.jsx`

**Fluxo**:

1. Usuário insere email e senha
2. Frontend chama `/api/auth/login` (POST)
3. API Route valida e chama backend `POST /auth/login`
4. Backend retorna token JWT e dados do usuário
5. Token é armazenado em cookie HTTP-only
6. Redireciona para dashboard se role = "gestor"

**Rotas**:

-**Frontend API**: `POST /api/auth/login`

-**Backend**: `POST /auth/login`

-**Body**: `{ email: string, password: string }`

-**Response**: `{ ok: true }` (token salvo em cookie)

---

### 2. Logout

**Página**: Qualquer página autenticada

**Componente**: `dashboard-layout.jsx`

**Fluxo**:

1. Usuário clica em "Sair"
2. Frontend chama `/api/auth/logout` (POST)
3. API Route remove cookie do token
4. Redireciona para login

**Rotas**:

-**Frontend API**: `POST /api/auth/logout`

-**Backend**: Não utilizado (logout é apenas no frontend)

---

### 3. Recuperação de Senha

**Página**: `/auth/forgot-password`

**Componente**: `forgot-password-desktop.jsx` / `forgot-password-mobile.jsx`

**Fluxo**:

1. Usuário insere email
2. Frontend chama `/api/auth/send-code` (POST)
3. Backend envia código por email
4. Usuário insere código recebido
5. Frontend chama `/api/auth/validate-code` (POST)
6. Backend valida código e retorna token de reset
7. Usuário insere nova senha
8. Frontend chama `/api/auth/reset-password` (POST) com token

**Rotas**:

-**Frontend API**:

  -`POST /api/auth/send-code`

  -`POST /api/auth/validate-code`

  -`POST /api/auth/reset-password`

-**Backend**:

  -`POST /auth/send-code`

  -`POST /auth/validate-code`

  -`POST /auth/reset-password`

---

### 4. Verificação de Email

**Página**: `/auth/verify-email`

**Componente**: `verify-email-desktop.jsx` / `verify-email-mobile.jsx`

**Fluxo**:

1. Usuário solicita novo código
2. Frontend chama `/api/auth/send-verify-email-code` (POST)
3. Backend envia código por email
4. Usuário insere código
5. Frontend chama `/api/auth/verify-email` (POST)
6. Backend valida e marca email como verificado

**Rotas**:

-**Frontend API**:

  -`POST /api/auth/send-verify-email-code`

  -`POST /api/auth/verify-email`

-**Backend**:

  -`POST /auth/send-code-verify-email`

  -`POST /auth/verify-email`

---

## Dashboard Principal

### Página Inicial

**Página**: `/` (index.jsx)

**Componente**: `home-dashboard.jsx`

**Features**:

- Exibe métricas principais (refeições por dia, gasto mensal, custo per capita, frequência atual)
- Lista itens em estoque com quantidade atual
- Mostra nome da unidade associada

**Rotas Utilizadas**:

-**Frontend API**:

  -`GET /api/storage/my-storage` - Busca estoque e unidade

  -`GET /api/reports/my-report` - Busca métricas do relatório

-**Backend**:

  -`GET /user-unit/{user_id}/units` - Busca unidades do usuário

  -`GET /storage?unit_id={unit_id}` - Busca estoque da unidade

  -`GET /reports/me` - Busca relatório do usuário (mês atual)

**Dados Exibidos**:

- Métricas calculadas a partir do relatório mensal
- Lista de itens de estoque com tipo (Comprado/Doação)
- Capacidade e frequência da unidade

---

## Gestão de Frequência

### Tela de Frequência

**Página**: `/frequencia`

**Componente**: `attendance-dashboard.jsx`

**Features**:

1.**Registro de Frequência**

- Campo para data (DD/MM/YYYY)
- Campo para número de presentes
- Validação de capacidade máxima
- Botão "Registrar Frequência"

2.**Histórico de Frequências**

- Lista todas as frequências registradas
- Exibe data formatada e quantidade de pessoas
- Botão de edição (ícone de lápis) em cada registro

3.**Edição de Frequência**

- Modal para editar data e quantidade
- Validação de campos
- Atualização em tempo real

**Rotas Utilizadas**:

-**Frontend API**:

  -`GET /api/frequency/my-frequencies` - Lista frequências do usuário

  -`POST /api/frequency/create` - Cria nova frequência

  -`PUT /api/frequency/update?frequency_id={id}` - Atualiza frequência

-**Backend**:

  -`GET /user-unit/{user_id}/units` - Busca unidades do usuário

  -`GET /units/{unit_id}` - Busca detalhes da unidade (capacidade)

  -`GET /frequency?unit_id={unit_id}` - Lista frequências da unidade

  -`POST /frequency` - Cria nova frequência

  -`PUT /frequency/{frequency_id}` - Atualiza frequência

**Payload de Criação**:

```json

{

  "unit_id": "uuid",

  "amount": 120,

  "date": "2025-12-15"

}

```

**Payload de Atualização**:

```json

{

  "amount": 125,

  "date": "2025-12-15"

}

```

---

## Gestão de Estoque

### Tela de Estoque

**Página**: `/estoque`

**Componente**: `estoque.jsx`

**Features**:

1.**Listagem de Itens**

- Tabela com todos os itens em estoque
- Filtro de busca por nome
- Exibe: nome, tipo, quantidade inicial, quantidade usada, quantidade atual

2.**Registro de Entrada**

- Formulário completo para entrada de itens
- Campos: nome, quantidade inicial, preço unitário, tipo (Comprado/Doação), fornecedor, data, nota fiscal, responsável
- Validação de campos obrigatórios

3.**Registro de Saída**

- Seleção de item do estoque
- Quantidade a retirar (validação de disponibilidade)
- Finalidade (Consumo/Descarte)
- Data, responsável, observações

**Rotas Utilizadas**:

-**Frontend API**:

  -`GET /api/storage/my-storage` - Busca estoque completo

  -`POST /api/storage/entry` - Registra entrada

  -`POST /api/storage/exit` - Registra saída

-**Backend**:

  -`GET /user-unit/{user_id}/units` - Busca unidades do usuário

  -`GET /storage?unit_id={unit_id}` - Lista estoque da unidade

  -`POST /storage/entry` - Registra entrada de estoque

  -`POST /storage/exit` - Registra saída de estoque

**Payload de Entrada**:

```json

{

  "name": "Arroz integral",

  "amount": 5.50,

  "unit_id": "uuid",

  "type": "comprado",

  "supplier": "Distribuidora ABC",

  "invoice": "NF-12345",

  "responsible": "João Silva",

  "date": "2025-12-15",

  "initial_quantity": 100,

  "used_quantity": 0

}

```

**Payload de Saída**:

```json

{

  "items": [

    {

      "name": "Arroz integral",

      "used_quantity": 20

    }

  ],

  "purpose": "Consumo",

  "responsible": "Maria Santos",

  "date": "2025-12-15",

  "notes": "Consumo diário",

  "unit_id": "uuid"

}

```

---

## Pedidos de Alimentos

### Tela de Pedidos

**Página**: `/pedidos`

**Componente**: `orders-dashboard.jsx`

**Features**:

- Lista todos os pedidos da unidade
- Exibe: ID do pedido, data de criação, valor total, itens do pedido
- Botão "Novo Pedido" (funcionalidade futura)

**Rotas Utilizadas**:

-**Frontend API**:

  -`GET /api/storage/my-storage` - Busca unidade do usuário

  -`GET /api/orders/unit/{unit_id}` - Lista pedidos da unidade (não implementado no frontend)

-**Backend**:

  -`GET /user-unit/{user_id}/units` - Busca unidades do usuário

  -`GET /orders/unit/{unit_id}` - Lista pedidos de uma unidade

**Nota**: A rota de pedidos no frontend ainda não está completamente implementada. O componente busca a unidade mas não faz a chamada para listar pedidos.

---

## Relatórios

### Tela de Relatórios

**Página**: `/relatorios`

**Componente**: `reports-dashboard.jsx`

**Features**:

1.**Métricas Principais**

- Capacidade total
- Frequência média (com tendência comparativa ao mês anterior)
- Custo per capita
- Gasto total e orçamento disponível

2.**Origem dos Recursos**

- Verba Normal (pacotes e percentual)
- Doações (pacotes e percentual)
- Total Geral

3.**Detalhamento de Alimentos**

- Tabela com alimentos (comprado vs doado)
- Gráfico de barras empilhadas (StackedBarChart)

4.**Análise de Desempenho Mensal**

- Comparativo dos últimos 3 meses
- Tabela com: mês, gasto total, frequência média, custo per capita
- Gráfico de barras verticais (VerticalBarChart)

5.**Exportação em PDF**

- Botão "Exportar" gera PDF completo
- Inclui todas as métricas, tabelas e gráficos
- Formatação profissional em preto e tons de cinza
- Nome do arquivo: `relatorio-gestao-{unidade}-{mes}.pdf`

**Rotas Utilizadas**:

-**Frontend API**:

  -`GET /api/reports/my-report` - Busca relatório do mês atual

  -`GET /api/reports/my-report?month={YYYY-MM}` - Busca relatório de mês específico

-**Backend**:

  -`GET /reports/me` - Relatório do usuário (mês atual)

  -`GET /reports/me?month={YYYY-MM}` - Relatório de mês específico

**Estrutura do Relatório**:

```json

{

  "unit_name": "Unidade Alpha",

  "metrics": {

    "capacity": 150,

    "frequency_pct": 92.5,

    "cost_per_capita": 450.75,

    "total_spending": 67612.50

  },

  "totals": {

    "packs_budget": 120,

    "packs_donations": 30,

    "total_packs": 150

  },

  "storage_summary": [

    {

      "food": "Arroz",

      "bought_amount": 500,

      "donated_amount": 100

    }

  ],

  "monthly_comparison": [

    {

      "month": "2025-09",

      "spent": 65000,

      "budget": 75000

    }

  ],

  "frequencies": [

    {

      "date": "01/11/2025 10:00",

      "amount": 140

    }

  ]

}

```

**Bibliotecas de PDF**:

-`jsPDF` - Geração de PDF

-`jspdf-autotable` - Tabelas no PDF

-`html2canvas` - Captura de gráficos como imagens

---

## Upload de Arquivos

### Upload para Google Drive

**Rota**: `/api/files/upload`

**Componente**: Utilizado em formulários que requerem upload de arquivos

**Features**:

- Upload de arquivos via multipart/form-data
- Integração com Google Drive
- Retorna URLs de visualização e download

**Rotas**:

-**Frontend API**: `POST /api/files/upload`

-**Backend**: Não utilizado (upload é feito diretamente no frontend via Google Drive API)

**Response**:

```json

{

  "success": true,

  "driveFileId": "file_id",

  "viewUrl": "https://drive.google.com/...",

  "downloadUrl": "https://drive.google.com/...",

  "fileName": "documento.pdf",

  "mimeType": "application/pdf"

}

```

---

## Mapeamento de Rotas Frontend ↔ Backend

### Tabela Completa de Rotas

| Feature | Frontend API Route | Método | Backend Route | Método | Descrição |

|---------|-------------------|--------|---------------|--------|-----------|

| **Autenticação** |

| Login | `/api/auth/login` | POST | `/auth/login` | POST | Autentica usuário |

| Logout | `/api/auth/logout` | POST | - | - | Remove token (frontend only) |

| Enviar código reset | `/api/auth/send-code` | POST | `/auth/send-code` | POST | Envia código de recuperação |

| Validar código | `/api/auth/validate-code` | POST | `/auth/validate-code` | POST | Valida código de reset |

| Reset senha | `/api/auth/reset-password` | POST | `/auth/reset-password` | POST | Redefine senha |

| Enviar código verificação | `/api/auth/send-verify-email-code` | POST | `/auth/send-code-verify-email` | POST | Envia código de verificação |

| Verificar email | `/api/auth/verify-email` | POST | `/auth/verify-email` | POST | Verifica email do usuário |

| **Unidades** |

| Minhas unidades | `/api/units/my-units` | GET | `/user-unit/{user_id}/units` | GET | Lista unidades do usuário |

| **Frequência** |

| Minhas frequências | `/api/frequency/my-frequencies` | GET | `/frequency?unit_id={id}` | GET | Lista frequências da unidade |

| Criar frequência | `/api/frequency/create` | POST | `/frequency` | POST | Registra nova frequência |

| Atualizar frequência | `/api/frequency/update` | PUT | `/frequency/{id}` | PUT | Edita frequência existente |

| **Estoque** |

| Meu estoque | `/api/storage/my-storage` | GET | `/storage?unit_id={id}` | GET | Lista estoque da unidade |

| Registrar entrada | `/api/storage/entry` | POST | `/storage/entry` | POST | Adiciona item ao estoque |

| Registrar saída | `/api/storage/exit` | POST | `/storage/exit` | POST | Remove item do estoque |

| **Relatórios** |

| Meu relatório | `/api/reports/my-report` | GET | `/reports/me` | GET | Relatório do mês atual |

| Meu relatório (mês) | `/api/reports/my-report?month={YYYY-MM}` | GET | `/reports/me?month={YYYY-MM}` | GET | Relatório de mês específico |

| **Pedidos** |

| Pedidos da unidade | `/api/orders/unit/{unit_id}` | GET | `/orders/unit/{unit_id}` | GET | Lista pedidos (não implementado) |

| **Arquivos** |

| Upload arquivo | `/api/files/upload` | POST | - | - | Upload para Google Drive |

---

## Autenticação

Todas as rotas (exceto login e recuperação de senha) requerem autenticação via JWT token. O token é enviado no header:

```

Authorization: Bearer {token}

```

O token é obtido durante o login e armazenado em cookie HTTP-only pelo frontend.

---

## Tratamento de Erros

### Padrão de Resposta de Erro

**Frontend API Routes**:

```json

{

  "error": "Mensagem de erro",

  "details": "Detalhes adicionais (opcional)"

}

```

**Backend FastAPI**:

```json

{

  "detail": "Mensagem de erro"

}

```

### Códigos de Status HTTP

-`200` - Sucesso

-`201` - Criado com sucesso

-`400` - Erro de validação

-`401` - Não autenticado

-`403` - Não autorizado

-`404` - Não encontrado

-`405` - Método não permitido

-`500` - Erro interno do servidor

---

## Observações Importantes

1.**Unidade do Usuário**: A maioria das operações assume que o usuário possui uma única unidade associada. O sistema sempre busca a primeira unidade do usuário.

2.**Validação de Role**: Apenas usuários com role "gestor" podem acessar o sistema.

3.**Formato de Datas**:

- Frontend exibe: `DD/MM/YYYY`
- API recebe/envia: `YYYY-MM-DD`

4.**Formato de Moeda**:

- Backend: números decimais
- Frontend: formatação brasileira (R$ 1.234,56)

5.**PDF Export**: A exportação de PDF é feita completamente no frontend usando bibliotecas JavaScript. Os gráficos são capturados como imagens usando `html2canvas`.

---

## Dependências Principais

### Frontend

-`next` - Framework React

-`react` - Biblioteca UI

-`lucide-react` - Ícones

-`jspdf` - Geração de PDF

-`jspdf-autotable` - Tabelas em PDF

-`html2canvas` - Captura de elementos HTML

### Backend

-`fastapi` - Framework Python

-`pydantic` - Validação de dados

-`supabase` - Banco de dados

-`python-jose` - JWT tokens

---

## Versão

**Documento**: v1.0.0

**Data**: Dezembro 2025

**Sistema**: Segurança Alimentar e Logística Social - UNAS
