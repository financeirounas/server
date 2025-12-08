# Análise de Rotas Faltantes - Sistema de Gestão Alimentar

## Resumo Executivo

Este documento apresenta uma análise completa das rotas de API que precisam ser implementadas no backend para suportar todas as funcionalidades do frontend do Sistema de Gestão Alimentar.

**Status Atual:**
- Autenticação: 8 rotas implementadas
- Estoque: 3 rotas implementadas
- Unidades: 9 rotas implementadas (CRUD completo)
- Pedidos: 9 rotas implementadas (CRUD completo com approve/reject)
- Orçamentos (Budgets): 0 rotas (CRÍTICO - necessário para orders)
- Financeiro/Despesas: Integração com API externa (a ser desenvolvida por outro time)
- Frequência/Atendimento: Integração com API externa (a ser desenvolvida por outro time)
- Usuários/Permissões (Unit Users): 0 rotas (IMPORTANTE)
- Alimentos (Foods): 0 rotas (OPCIONAL)
- Relatórios: 0 rotas (OPCIONAL - depende de expenses e attendance)

---

## 1. Rotas Já Implementadas

### 1.1 Autenticação (`/auth`)

**Arquivo:** `router/auth.py`

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/login` | Login de usuário |
| POST | `/auth/logout` | Logout de usuário |
| POST | `/auth/send-code` | Envia código de redefinição de senha |
| POST | `/auth/validate-code` | Valida código de redefinição |
| POST | `/auth/verify-email` | Verifica código de e-mail |
| POST | `/auth/send-code-verify-email` | Envia código de verificação de e-mail |
| POST | `/auth/reset-password` | Redefine senha com token |
| POST | `/auth/validate-token` | Valida token JWT |

### 1.2 Estoque (`/storage`)

**Arquivo:** `router/storage.py`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/storage?unit_id={id}` | Lista todos os itens de estoque de uma unidade |
| POST | `/storage/entry` | Registra entrada de estoque |
| POST | `/storage/exit` | Registra saída de estoque |

### 1.3 Unidades (`/units`)

**Arquivo:** `router/units.py`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/units` | Lista todas as unidades |
| GET | `/units?type={type}` | Lista unidades filtradas por tipo |
| GET | `/units/{id}` | Busca unidade por ID |
| POST | `/units` | Cria nova unidade |
| PUT | `/units/{id}` | Atualiza unidade |
| DELETE | `/units/{id}` | Deleta unidade |
| GET | `/units/name/{name}` | Busca unidade por nome |
| GET | `/units/address/{address}` | Busca unidade por endereço |
| GET | `/units/type/{type}` | Busca unidades por tipo |

### 1.4 Pedidos (`/orders`)

**Arquivo:** `router/orders.py`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/orders` | Lista todos os pedidos |
| GET | `/orders?unit_id={id}` | Lista pedidos filtrados por unidade |
| GET | `/orders?budget_id={id}` | Lista pedidos filtrados por orçamento |
| GET | `/orders/{id}` | Busca pedido por ID (inclui itens) |
| POST | `/orders` | Cria novo pedido (com ou sem itens) |
| PUT | `/orders/{id}` | Atualiza pedido |
| DELETE | `/orders/{id}` | Deleta pedido e seus itens |
| GET | `/orders/unit/{unit_id}` | Busca pedidos de uma unidade |
| GET | `/orders/budget/{budget_id}` | Busca pedidos de um orçamento |
| PUT | `/orders/{id}/approve` | Aprova pedido |
| PUT | `/orders/{id}/reject` | Rejeita pedido |

---

## 2. Rotas Faltantes

### 2.1 Orçamentos (`/budgets`) - **CRÍTICO**

**Prioridade:** ALTA  
**Dependências:** Nenhuma (mas orders depende de budgets)

#### Arquivos Necessários

```
entities/
  models/
    budget.py                   # Modelo Budget
  dtos/
    budget_dto.py               # DTOs para orçamentos
repositories/
    budget_repository.py        # Repository para orçamentos
services/
    budget_service.py           # Service para orçamentos
router/
    budgets.py                  # Rotas de orçamentos
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/budgets` | Lista todos os orçamentos | `?initial_date={date}`, `?final_date={date}` (opcional) |
| GET | `/budgets/{id}` | Busca orçamento por ID | `id` (path) |
| POST | `/budgets` | Cria novo orçamento | Body: BudgetCreateDTO |
| PUT | `/budgets/{id}` | Atualiza orçamento | `id` (path), Body: BudgetUpdateDTO |
| DELETE | `/budgets/{id}` | Deleta orçamento | `id` (path) |

#### Modelo de Dados

**Budget Model:**
```python
{
  "id": "uuid",
  "description": "string?",
  "initial_date": "date?",
  "final_date": "date?",
  "amount": "float?",
  "created_at": "datetime",
  "updated_at": "datetime?"
}
```

#### DTOs Necessários

- `BudgetCreateDTO`: description?, initial_date?, final_date?, amount?
- `BudgetUpdateDTO`: description?, initial_date?, final_date?, amount?
- `BudgetResponseDTO`: Todos os campos do modelo

#### Observações

- Validar que `final_date` seja posterior a `initial_date` (se ambos fornecidos)
- `amount` deve ser positivo (se fornecido)
- Validar existência de `budget_id` em `orders` antes de deletar
- Orçamentos são referenciados por `orders.budget_id`

---

### 2.2 Unidades (`/units`) - **IMPLEMENTADO**

**Prioridade:** ALTA  
**Dependências:** Nenhuma (base para outras funcionalidades)

#### Arquivos Necessários

```
entities/
  models/
    unit.py                    # Modelo Unit
  dtos/
    unit_dto.py                # DTOs para unidades
repositories/
    unit_repository.py         # Repository para unidades
services/
    unit_service.py            # Service para unidades
router/
    units.py                   # Rotas de unidades
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/units` | Lista todas as unidades | `?type={CCA\|CEI}` (opcional) |
| GET | `/units/{id}` | Busca unidade por ID | `id` (path) |
| POST | `/units` | Cria nova unidade | Body: UnitCreateDTO |
| PUT | `/units/{id}` | Atualiza unidade | `id` (path), Body: UnitUpdateDTO |
| DELETE | `/units/{id}` | Deleta unidade | `id` (path) |

#### Modelo de Dados

**Unit Model:**
```python
{
  "id": "uuid",
  "name": "string",
  "type": "CCA" | "CEI",
  "address": "string",
  "capacity": "number",
  "responsibles": ["string"],  # Array de nomes ou user_ids
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### DTOs Necessários

- `UnitCreateDTO`: name, type, address, capacity, responsibles[]
- `UnitUpdateDTO`: name?, type?, address?, capacity?, responsibles[]?
- `UnitResponseDTO`: Todos os campos do modelo

#### Observações

- Validar que `type` seja apenas 'CCA' ou 'CEI'
- `capacity` deve ser um número positivo
- Soft delete recomendado (campo `deleted_at`)
- Validar existência de `unit_id` em outras tabelas antes de deletar

---

### 2.3 Pedidos (`/orders`) - **IMPLEMENTADO**

**Prioridade:** ALTA  
**Dependências:** Unidades (`/units`)

#### Arquivos Necessários

```
entities/
  models/
    order.py                   # Modelo Order
    order_item.py              # Modelo OrderItem
  dtos/
    order_dto.py               # DTOs para pedidos
repositories/
    order_repository.py        # Repository para pedidos
services/
    order_service.py           # Service para pedidos
router/
    orders.py                  # Rotas de pedidos
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/orders` | Lista pedidos | `?unit_id={id}` (opcional), `?status={status}` (opcional) |
| GET | `/orders/{id}` | Busca pedido por ID | `id` (path) |
| POST | `/orders` | Cria novo pedido | Body: OrderCreateDTO |
| PUT | `/orders/{id}` | Atualiza pedido | `id` (path), Body: OrderUpdateDTO |
| PUT | `/orders/{id}/approve` | Aprova pedido | `id` (path) |
| PUT | `/orders/{id}/reject` | Rejeita pedido | `id` (path) |
| DELETE | `/orders/{id}` | Cancela/deleta pedido | `id` (path) |

#### Modelo de Dados

**Order Model:**
```python
{
  "id": "uuid",
  "unit_id": "uuid",
  "date": "date",
  "requested_by": "uuid",      # user_id
  "status": "pending" | "approved" | "rejected" | "completed",
  "total": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**OrderItem Model:**
```python
{
  "id": "uuid",
  "order_id": "uuid",
  "name": "string",
  "quantity": "number",
  "unit": "kg" | "pacotes",
  "price_per_unit": "number",
  "weight_per_package": "number?",  # Apenas se unit = "pacotes"
  "subtotal": "number"
}
```

#### DTOs Necessários

- `OrderCreateDTO`: unit_id, date, requested_by, items[]
- `OrderItemDTO`: name, quantity, unit, price_per_unit, weight_per_package?
- `OrderUpdateDTO`: status?, items[]?
- `OrderResponseDTO`: Todos os campos + items[]

#### Observações

- CRUD completo implementado
- Validação de `unit_id` e `budget_id` implementada
- Criação de pedidos com itens implementada
- Rotas de aprovação/rejeição (`PUT /orders/{id}/approve`, `PUT /orders/{id}/reject`) implementadas
- Cálculo automático de total implementado (soma dos itens se amount não fornecido)
- Campo `status` adicionado ao model e DTOs (opcional)
- Campo `status` precisa ser adicionado ao schema do banco de dados se ainda não existir
- Campo `requested_by` não existe no schema atual (pode ser adicionado no futuro)
- Schema atual não tem campos `date`, `requested_by` - podem ser adicionados no futuro se necessário

---

### 2.3 Financeiro/Despesas (`/expenses`) - **INTEGRAÇÃO COM API EXTERNA**

**Prioridade:** ALTA  
**Dependências:** Unidades (`/units`)  
**Status:** Será integrado com API externa desenvolvida por outro time

#### Arquivos Necessários

**Nota:** Esta funcionalidade será integrada com API externa. Os arquivos abaixo podem ser necessários apenas para adaptadores/proxies se necessário.

```
router/
    expenses.py                # Rotas proxy/adaptador para API externa (se necessário)
services/
    expense_integration_service.py  # Service para integração com API externa
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/expenses` | Lista despesas | `?unit_id={id}`, `?month={YYYY-MM}`, `?type={verba\|doado}` |
| GET | `/expenses/{id}` | Busca despesa por ID | `id` (path) |
| POST | `/expenses` | Registra nova despesa | Body: ExpenseCreateDTO |
| PUT | `/expenses/{id}` | Atualiza despesa | `id` (path), Body: ExpenseUpdateDTO |
| DELETE | `/expenses/{id}` | Remove despesa | `id` (path) |
| GET | `/expenses/summary` | Resumo financeiro | `?unit_id={id}`, `?month={YYYY-MM}` |

#### Modelo de Dados

**Expense Model:**
```python
{
  "id": "uuid",
  "unit_id": "uuid",
  "item": "string",
  "supplier": "string",
  "date": "date",
  "amount": "number",
  "responsible": "uuid",       # user_id
  "invoice": "string?",        # Número da nota fiscal
  "type": "verba" | "doado",   # Fonte do recurso
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### DTOs Necessários

- `ExpenseCreateDTO`: unit_id, item, supplier, date, amount, responsible, invoice?, type
- `ExpenseUpdateDTO`: item?, supplier?, date?, amount?, responsible?, invoice?, type?
- `ExpenseResponseDTO`: Todos os campos do modelo
- `ExpenseSummaryDTO`: verba_total, doacao_total, total, unit_id?, month?

#### Observações

- Esta funcionalidade será consumida de API externa
- Pode ser necessário criar rotas proxy/adaptador se a API externa tiver estrutura diferente
- Definir contrato de integração com o time responsável pela API externa
- Considerar tratamento de erros e fallbacks caso a API externa esteja indisponível
- Documentar endpoints da API externa quando disponíveis

---

### 2.4 Frequência/Atendimento (`/attendance`) - **INTEGRAÇÃO COM API EXTERNA**

**Prioridade:** MÉDIA  
**Dependências:** Unidades (`/units`)  
**Status:** Será integrado com API externa desenvolvida por outro time

#### Arquivos Necessários

**Nota:** Esta funcionalidade será integrada com API externa. Os arquivos abaixo podem ser necessários apenas para adaptadores/proxies se necessário.

```
router/
    attendance.py               # Rotas proxy/adaptador para API externa (se necessário)
services/
    attendance_integration_service.py  # Service para integração com API externa
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/attendance` | Busca frequência | `?unit_id={id}`, `?date={YYYY-MM-DD}` |
| GET | `/attendance/history` | Histórico de frequência | `?unit_id={id}`, `?start_date={YYYY-MM-DD}`, `?end_date={YYYY-MM-DD}` |
| POST | `/attendance` | Registra frequência do dia | Body: AttendanceCreateDTO |
| PUT | `/attendance/{id}` | Atualiza registro de frequência | `id` (path), Body: AttendanceUpdateDTO |
| GET | `/attendance/consumption` | Calcula consumo estimado | `?unit_id={id}`, `?date={YYYY-MM-DD}` |

#### Modelo de Dados

**Attendance Model:**
```python
{
  "id": "uuid",
  "unit_id": "uuid",
  "date": "date",
  "present": "number",         # Número de presentes
  "total": "number",           # Capacidade total da unidade
  "percentage": "number",      # Calculado: (present / total) * 100
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### DTOs Necessários

- `AttendanceCreateDTO`: unit_id, date, present
- `AttendanceUpdateDTO`: present?
- `AttendanceResponseDTO`: Todos os campos do modelo
- `ConsumptionEstimateDTO`: rice, beans, protein (em kg)

#### Observações

- Esta funcionalidade será consumida de API externa
- Pode ser necessário criar rotas proxy/adaptador se a API externa tiver estrutura diferente
- Definir contrato de integração com o time responsável pela API externa
- Considerar tratamento de erros e fallbacks caso a API externa esteja indisponível
- Documentar endpoints da API externa quando disponíveis

---

### 2.5 Usuários e Permissões (`/users` e `/unit-users`) - **IMPORTANTE**

**Prioridade:** MÉDIA  
**Dependências:** Nenhuma (mas relaciona com unidades)

#### Arquivos Necessários

```
entities/
  models/
    unit_user.py               # Modelo UnitUser (relação)
  dtos/
    user_dto.py                # DTOs estendidos para usuários
repositories/
    unit_user_repository.py    # Repository para relações
services/
    (estender user_service.py) # Extensão do service existente
router/
    users.py                   # Rotas de usuários
```

#### Rotas a Implementar

**Usuários (`/users`):**
| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/users` | Lista todos os usuários | `?role={role}`, `?active={true\|false}` |
| GET | `/users/{id}` | Busca usuário por ID | `id` (path) |
| PUT | `/users/{id}` | Atualiza usuário | `id` (path), Body: UserUpdateDTO |
| DELETE | `/users/{id}` | Desativa usuário | `id` (path) |

**Relação Usuário-Unidade (`/unit-users`):**
| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/unit-users` | Lista todas as associações | `?unit_id={id}`, `?user_id={id}` |
| GET | `/unit-users/{id}` | Busca associação por ID | `id` (path) |
| POST | `/unit-users` | Cria associação usuário-unidade | Body: UnitUserCreateDTO |
| PUT | `/unit-users/{id}` | Atualiza associação | `id` (path), Body: UnitUserUpdateDTO |
| DELETE | `/unit-users/{id}` | Remove associação | `id` (path) |
| GET | `/users/{id}/units` | Lista unidades do usuário | `id` (path) |
| GET | `/units/{id}/users` | Lista usuários da unidade | `id` (path) |

#### Modelo de Dados

**UnitUser Model (Relação N:N):**
```python
{
  "id": "uuid",
  "user_id": "uuid",
  "unit_id": "uuid",
  "role": "admin" | "manager" | "kitchen" | "financial",
  "active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**User Model (estendido):**
```python
{
  "id": "uuid",
  "email": "string",
  "username": "string",
  "type": "string",
  "active": "boolean",         # Novo campo
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### DTOs Necessários

- `UserUpdateDTO`: username?, type?, active?
- `UnitUserCreateDTO`: user_id, unit_id, role
- `UserResponseDTO`: Todos os campos + units[] (opcional)

#### Observações

- Validar que `user_id` e `unit_id` existem
- `role` deve ser um dos valores permitidos
- Um usuário pode ter múltiplas associações (múltiplas unidades)
- Soft delete recomendado (campo `active`)
- Apenas admins podem gerenciar usuários

---

### 2.6 Alimentos (`/foods`) - **OPCIONAL**

**Prioridade:** BAIXA  
**Dependências:** Nenhuma

#### Arquivos Necessários

```
entities/
  models/
    food.py                      # Modelo Food
  dtos/
    food_dto.py                  # DTOs para alimentos
repositories/
    food_repository.py           # Repository para alimentos
services/
    food_service.py              # Service para alimentos
router/
    foods.py                     # Rotas de alimentos
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/foods` | Lista todos os alimentos | `?type={type}` (opcional) |
| GET | `/foods/{id}` | Busca alimento por ID | `id` (path) |
| POST | `/foods` | Cria novo alimento | Body: FoodCreateDTO |
| PUT | `/foods/{id}` | Atualiza alimento | `id` (path), Body: FoodUpdateDTO |
| DELETE | `/foods/{id}` | Deleta alimento | `id` (path) |

#### Modelo de Dados

**Food Model:**
```python
{
  "id": "uuid",
  "type": "string?",
  "created_at": "datetime",
  "updated_at": "datetime?"
}
```

#### DTOs Necessários

- `FoodCreateDTO`: type?
- `FoodUpdateDTO`: type?
- `FoodResponseDTO`: Todos os campos do modelo

#### Observações

- Tabela parece ser um catálogo/referência de tipos de alimentos
- Não há foreign keys diretas no schema atual
- Pode ser usado como referência para outros módulos

---

### 2.7 Relatórios (`/reports`) - **OPCIONAL**

**Prioridade:** BAIXA  
**Dependências:** Pedidos, Despesas, Frequência

#### Arquivos Necessários

```
router/
    reports.py                 # Rotas de relatórios (agregação)
```

#### Rotas a Implementar

| Método | Rota | Descrição | Parâmetros |
|--------|------|-----------|------------|
| GET | `/reports/consolidated` | Relatório consolidado | `?month={YYYY-MM}` |
| GET | `/reports/unit/{unit_id}` | Relatório por unidade | `unit_id` (path), `?month={YYYY-MM}` |
| GET | `/reports/comparison` | Comparação entre unidades | `?month={YYYY-MM}` |

#### Dados Retornados

**Consolidated Report:**
```python
{
  "total_units": "number",
  "total_capacity": "number",
  "total_spending": "number",
  "total_verba": "number",
  "total_donation": "number",
  "total_consumption": "number",
  "average_attendance": "number",
  "month": "YYYY-MM"
}
```

**Unit Report:**
```python
{
  "unit_id": "uuid",
  "unit_name": "string",
  "verba": "number",
  "donation": "number",
  "total": "number",
  "consumption": "number",
  "per_capita": "number",
  "attendance": "number",
  "month": "YYYY-MM"
}
```

**Comparison Report:**
```python
{
  "units": [
    {
      "unit_id": "uuid",
      "unit_name": "string",
      "verba": "number",
      "donation": "number",
      "consumption": "number",
      "per_capita": "number",
      "attendance": "number"
    }
  ],
  "month": "YYYY-MM"
}
```

#### Observações

- Essas rotas agregam dados das outras rotas (expenses, attendance, orders)
- Não precisam de novos modelos, apenas agregação
- Otimizar queries para performance
- Considerar cache para relatórios consolidados

---

## 3. Priorização de Implementação

### Fase 1 - Base (Crítico)
1. **Unidades (`/units`)** - Base para todas as outras funcionalidades - IMPLEMENTADO
2. **Pedidos (`/orders`)** - Funcionalidade principal do sistema - IMPLEMENTADO (básico)
3. **Orçamentos (`/budgets`)** - Necessário para orders funcionarem completamente - PENDENTE
4. **Financeiro (`/expenses`)** - Integração com API externa - AGUARDANDO API EXTERNA

### Fase 2 - Funcionalidades Essenciais
5. **Frequência (`/attendance`)** - Integração com API externa - AGUARDANDO API EXTERNA
6. **Usuários/Permissões (`/users` e `/unit-users`)** - Necessário para controle de acesso - PENDENTE

### Fase 3 - Melhorias
7. **Alimentos (`/foods`)** - Catálogo/referência - PENDENTE
8. **Relatórios (`/reports`)** - Depende de expenses e attendance (APIs externas) - AGUARDANDO APIS EXTERNAS

---

## 4. Considerações Técnicas

### 4.1 Autenticação e Autorização

- **Todas as rotas** (exceto `/auth/login`) devem validar JWT token
- Implementar middleware de autenticação
- Verificar roles/permissões:
  - `admin`: Acesso total
  - `manager`: Acesso à unidade específica
  - `kitchen`: Acesso limitado (estoque, frequência)
  - `financial`: Acesso financeiro (expenses, orders, reports)

### 4.2 Validações

- Validar foreign keys (ex: `unit_id` deve existir em `units`)
- Validar tipos de dados (ex: `type` deve ser 'CCA' ou 'CEI')
- Validar ranges (ex: `amount` deve ser positivo)
- Validar unicidade quando necessário (ex: attendance por unit_id + date)

### 4.3 Soft Delete

- Implementar soft delete para:
  - Unidades (campo `deleted_at`)
  - Usuários (campo `active` ou `deleted_at`)
  - Pedidos (campo `status = 'cancelled'`)

### 4.4 Paginação

- Implementar paginação nas rotas GET que listam múltiplos itens:
  - `?page={number}&limit={number}`
  - Retornar: `{ "data": [], "total": number, "page": number, "limit": number }`

### 4.5 Filtros e Busca

- Suportar filtros comuns:
  - Por data/período: `?start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}`
  - Por unidade: `?unit_id={id}`
  - Por status: `?status={status}`
  - Por tipo: `?type={type}`

### 4.6 Tratamento de Erros

- Retornar códigos HTTP apropriados:
  - `200`: Sucesso
  - `201`: Criado com sucesso
  - `400`: Erro de validação
  - `401`: Não autenticado
  - `403`: Sem permissão
  - `404`: Não encontrado
  - `500`: Erro interno

- Mensagens de erro consistentes:
```json
{
  "detail": "Mensagem de erro descritiva",
  "code": "ERROR_CODE",
  "field": "campo_com_erro" // quando aplicável
}
```

---

## 5. Estrutura de Arquivos

### Arquivos Já Criados

```
entities/
  models/
    unit.py
    orders.py
    order_item.py
    user.py
    security_code.py
    storage.py
  dtos/
    unit_dto.py
    orders_dto.py
    auth_dto.py
    storage_dto.py

repositories/
    unit_repository.py
    order_repository.py
    user_repository.py
    code_repository.py
    storage_repository.py

services/
    unit_service.py
    order_service.py
    user_service.py
    auth_service.py
    code_service.py
    storage_service.py

router/
    units.py
    orders.py
    auth.py
    storage.py
```

### Arquivos a Criar

```
entities/
  models/
    budget.py
    unit_user.py
    food.py
  dtos/
    budget_dto.py
    unit_user_dto.py
    user_dto.py (extensão)
    food_dto.py

repositories/
    budget_repository.py
    unit_user_repository.py
    food_repository.py

services/
    budget_service.py
    unit_user_service.py
    food_service.py

router/
    budgets.py
    users.py
    unit-users.py
    foods.py
    reports.py
```

### Arquivos para Integração com APIs Externas (se necessário)

```
services/
    expense_integration_service.py    # Integração com API externa de expenses
    attendance_integration_service.py # Integração com API externa de attendance

router/
    expenses.py                        # Rotas proxy/adaptador (se necessário)
    attendance.py                      # Rotas proxy/adaptador (se necessário)
```

---

## 6. Integração no main.py

### Rotas Já Registradas

```python
from router import auth, storage, units, orders

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(storage.router, prefix="/storage", tags=["storage"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
```

### Rotas a Adicionar

```python
from router import budgets, users, unit_users, foods, reports

app.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(unit_users.router, prefix="/unit-users", tags=["unit-users"])
app.include_router(foods.router, prefix="/foods", tags=["foods"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
```

### Rotas para Integração com APIs Externas (se necessário)

```python
# Apenas se for necessário criar rotas proxy/adaptador
from router import expenses, attendance

app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
```

---

## 7. Checklist de Implementação

### Unidades
- [x] Criar modelo `Unit`
- [x] Criar DTOs (`UnitCreateDTO`, `UnitUpdateDTO`, `UnitResponseDTO`)
- [x] Criar `UnitRepository`
- [x] Criar `UnitService`
- [x] Criar rotas em `router/units.py`
- [x] Adicionar rotas no `main.py`
- [x] Testar CRUD completo
- [x] Validar foreign keys em outras tabelas

### Pedidos
- [x] Criar modelos `Order` e `OrderItem`
- [x] Criar DTOs
- [x] Criar `OrderRepository`
- [x] Criar `OrderService`
- [x] Criar rotas em `router/orders.py`
- [x] Adicionar rotas no `main.py`
- [x] Implementar cálculo automático de total
- [x] Implementar aprovação/rejeição (`PUT /orders/{id}/approve`, `PUT /orders/{id}/reject`)
- [x] Adicionar campo `status` ao model e DTOs

### Orçamentos
- [ ] Criar modelo `Budget`
- [ ] Criar DTOs (`BudgetCreateDTO`, `BudgetUpdateDTO`, `BudgetResponseDTO`)
- [ ] Criar `BudgetRepository`
- [ ] Criar `BudgetService`
- [ ] Criar rotas em `router/budgets.py`
- [ ] Adicionar rotas no `main.py`
- [ ] Validar foreign keys em orders

### Financeiro (Integração com API Externa)
- [ ] Definir contrato de integração com time responsável
- [ ] Documentar endpoints da API externa
- [ ] Criar service de integração (`expense_integration_service.py`)
- [ ] Criar rotas proxy/adaptador em `router/expenses.py` (se necessário)
- [ ] Implementar tratamento de erros e fallbacks
- [ ] Adicionar rotas no `main.py` (se necessário)
- [ ] Testar integração com API externa

### Frequência (Integração com API Externa)
- [ ] Definir contrato de integração com time responsável
- [ ] Documentar endpoints da API externa
- [ ] Criar service de integração (`attendance_integration_service.py`)
- [ ] Criar rotas proxy/adaptador em `router/attendance.py` (se necessário)
- [ ] Implementar tratamento de erros e fallbacks
- [ ] Adicionar rotas no `main.py` (se necessário)
- [ ] Testar integração com API externa

### Usuários/Permissões
- [ ] Criar modelo `UnitUser`
- [ ] Criar DTOs
- [ ] Criar `UnitUserRepository`
- [ ] Estender `UserService`
- [ ] Criar rotas em `router/users.py` (CRUD de usuários)
- [ ] Criar rotas em `router/unit-users.py` (relação N:N)
- [ ] Adicionar rotas no `main.py`
- [ ] Implementar associação usuário-unidade
- [ ] Validar permissões

### Alimentos
- [ ] Criar modelo `Food`
- [ ] Criar DTOs (`FoodCreateDTO`, `FoodUpdateDTO`, `FoodResponseDTO`)
- [ ] Criar `FoodRepository`
- [ ] Criar `FoodService`
- [ ] Criar rotas em `router/foods.py`
- [ ] Adicionar rotas no `main.py`

### Relatórios
- [ ] Aguardar disponibilidade das APIs externas (expenses e attendance)
- [ ] Criar rotas em `router/reports.py`
- [ ] Adicionar rotas no `main.py`
- [ ] Implementar agregação de dados (incluindo dados de APIs externas)
- [ ] Otimizar queries e chamadas a APIs externas
- [ ] Considerar cache para dados de APIs externas

---

## 8. Referências

- **Frontend Components:**
  - `Sistema de Gestão Alimentar/src/components/unit-management.tsx`
  - `Sistema de Gestão Alimentar/src/components/orders.tsx`
  - `Sistema de Gestão Alimentar/src/components/financial.tsx`
  - `Sistema de Gestão Alimentar/src/components/attendance.tsx`
  - `Sistema de Gestão Alimentar/src/components/users-permissions.tsx`
  - `Sistema de Gestão Alimentar/src/components/reports.tsx`

- **Documentação Existente:**
  - `docs/units_table_structure.md` - Estrutura da tabela `units`
  - `router/auth.py` - Exemplo de implementação de rotas
  - `router/storage.py` - Exemplo de implementação de rotas

---

## 9. Como Testar as Rotas Implementadas

### 9.1 Pré-requisitos

1. **Ambiente Python configurado:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou
   venv\Scripts\activate  # Windows
   ```

2. **Dependências instaladas:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Variáveis de ambiente configuradas:**
   - Criar arquivo `.env` na raiz do projeto
   - Configurar variáveis necessárias (Supabase, JWT, etc.)

4. **Banco de dados:**
   - Supabase configurado e acessível
   - Tabelas criadas conforme schema

### 9.2 Iniciando o Servidor

**Opção 1: Script de desenvolvimento (recomendado)**
```bash
# Linux/macOS
./run_dev.sh

# Windows
run_dev.bat
```

**Opção 2: Comando direto**
```bash
uvicorn cmd.main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: `http://127.0.0.1:8000`

**Documentação interativa:**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 9.3 Testando com Postman

**Importar Collection:**
1. Abrir Postman
2. Importar arquivo: `postman/UNAS-API.postman_collection.json`
3. Configurar variável `base_url`:
   - Valor: `http://127.0.0.1:8000`
   - Ou a URL do ambiente de produção/staging

**Collection inclui:**
- Autenticação (login, logout, etc.)
- Estoque (entrada, saída, listagem)
- Unidades (CRUD completo)
- Pedidos (CRUD completo + approve/reject)

### 9.4 Testando com cURL

#### 9.4.1 Autenticação

**Login:**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@unas.org.br",
    "password": "123456"
  }'
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Salvar token para uso posterior:**
```bash
TOKEN="seu_token_aqui"
```

#### 9.4.2 Unidades

**Listar todas as unidades:**
```bash
curl -X GET "http://127.0.0.1:8000/units" \
  -H "Authorization: Bearer $TOKEN"
```

**Criar unidade:**
```bash
curl -X POST "http://127.0.0.1:8000/units" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "CCA Heliópolis I",
    "type": "CCA",
    "address": "Rua da Mina, 123 - Heliópolis",
    "capacity": 100,
    "responsibles": ["Maria Silva", "João Santos"]
  }'
```

**Buscar unidade por ID:**
```bash
curl -X GET "http://127.0.0.1:8000/units/{unit_id}" \
  -H "Authorization: Bearer $TOKEN"
```

**Atualizar unidade:**
```bash
curl -X PUT "http://127.0.0.1:8000/units/{unit_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "CCA Heliópolis I - Atualizado",
    "capacity": 120
  }'
```

**Deletar unidade:**
```bash
curl -X DELETE "http://127.0.0.1:8000/units/{unit_id}" \
  -H "Authorization: Bearer $TOKEN"
```

#### 9.4.3 Pedidos

**Listar todos os pedidos:**
```bash
curl -X GET "http://127.0.0.1:8000/orders" \
  -H "Authorization: Bearer $TOKEN"
```

**Listar pedidos filtrados:**
```bash
# Por unidade
curl -X GET "http://127.0.0.1:8000/orders?unit_id={unit_id}" \
  -H "Authorization: Bearer $TOKEN"

# Por orçamento
curl -X GET "http://127.0.0.1:8000/orders?budget_id={budget_id}" \
  -H "Authorization: Bearer $TOKEN"
```

**Criar pedido (sem itens):**
```bash
curl -X POST "http://127.0.0.1:8000/orders" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "description": "Pedido mensal de alimentos",
    "amount": 1500.0,
    "unit_id": "{unit_id}",
    "budget_id": "{budget_id}"
  }'
```

**Criar pedido (com itens):**
```bash
curl -X POST "http://127.0.0.1:8000/orders" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "description": "Pedido mensal de alimentos para CCA",
    "unit_id": "{unit_id}",
    "budget_id": "{budget_id}",
    "items": [
      {
        "description": "Arroz integral",
        "amount": 100.0,
        "measure_unit": "kg",
        "received": false
      },
      {
        "description": "Feijão preto",
        "amount": 50.0,
        "measure_unit": "kg",
        "received": true
      }
    ]
  }'
```

**Buscar pedido por ID:**
```bash
curl -X GET "http://127.0.0.1:8000/orders/{order_id}" \
  -H "Authorization: Bearer $TOKEN"
```

**Atualizar pedido:**
```bash
curl -X PUT "http://127.0.0.1:8000/orders/{order_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "description": "Pedido atualizado",
    "amount": 2000.0
  }'
```

**Aprovar pedido:**
```bash
curl -X PUT "http://127.0.0.1:8000/orders/{order_id}/approve" \
  -H "Authorization: Bearer $TOKEN"
```

**Rejeitar pedido:**
```bash
curl -X PUT "http://127.0.0.1:8000/orders/{order_id}/reject" \
  -H "Authorization: Bearer $TOKEN"
```

**Deletar pedido:**
```bash
curl -X DELETE "http://127.0.0.1:8000/orders/{order_id}" \
  -H "Authorization: Bearer $TOKEN"
```

**Buscar pedidos por unidade:**
```bash
curl -X GET "http://127.0.0.1:8000/orders/unit/{unit_id}" \
  -H "Authorization: Bearer $TOKEN"
```

**Buscar pedidos por orçamento:**
```bash
curl -X GET "http://127.0.0.1:8000/orders/budget/{budget_id}" \
  -H "Authorization: Bearer $TOKEN"
```

#### 9.4.4 Estoque

**Listar estoque de uma unidade:**
```bash
curl -X GET "http://127.0.0.1:8000/storage?unit_id={unit_id}" \
  -H "Authorization: Bearer $TOKEN"
```

**Registrar entrada de estoque:**
```bash
curl -X POST "http://127.0.0.1:8000/storage/entry" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "unit_id": "{unit_id}",
    "name": "Arroz",
    "amount": 50.0,
    "type": "comprado",
    "date": "2025-11-29"
  }'
```

**Registrar saída de estoque:**
```bash
curl -X POST "http://127.0.0.1:8000/storage/exit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "unit_id": "{unit_id}",
    "name": "Arroz",
    "amount": 10.0,
    "date": "2025-11-29"
  }'
```

### 9.5 Testando com Swagger UI

1. Acessar `http://127.0.0.1:8000/docs`
2. Expandir a seção desejada (auth, storage, units, orders)
3. Clicar em "Try it out" no endpoint desejado
4. Preencher os parâmetros necessários
5. Clicar em "Execute"
6. Verificar a resposta

**Vantagens:**
- Interface visual e intuitiva
- Documentação integrada
- Não requer ferramentas externas
- Testa diretamente no navegador

### 9.6 Códigos de Status HTTP Esperados

- `200 OK`: Requisição bem-sucedida (GET, PUT)
- `201 Created`: Recurso criado com sucesso (POST)
- `204 No Content`: Recurso deletado com sucesso (DELETE)
- `400 Bad Request`: Erro de validação nos dados enviados
- `401 Unauthorized`: Token ausente ou inválido
- `403 Forbidden`: Sem permissão para acessar o recurso
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

### 9.7 Tratamento de Erros

**Exemplo de resposta de erro:**
```json
{
  "detail": "Pedido não encontrado"
}
```

**Exemplo de erro de validação:**
```json
{
  "detail": [
    {
      "loc": ["body", "unit_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 9.8 Checklist de Testes

**Autenticação:**
- [ ] Login com credenciais válidas
- [ ] Login com credenciais inválidas
- [ ] Validação de token

**Unidades:**
- [ ] Listar todas as unidades
- [ ] Criar unidade
- [ ] Buscar unidade por ID
- [ ] Atualizar unidade
- [ ] Deletar unidade
- [ ] Buscar por nome
- [ ] Buscar por tipo
- [ ] Buscar por endereço

**Pedidos:**
- [ ] Listar todos os pedidos
- [ ] Listar pedidos filtrados por unidade
- [ ] Listar pedidos filtrados por orçamento
- [ ] Criar pedido sem itens
- [ ] Criar pedido com itens
- [ ] Buscar pedido por ID
- [ ] Atualizar pedido
- [ ] Aprovar pedido
- [ ] Rejeitar pedido
- [ ] Deletar pedido
- [ ] Verificar cálculo automático de total

**Estoque:**
- [ ] Listar estoque de uma unidade
- [ ] Registrar entrada
- [ ] Registrar saída
- [ ] Validar atualização de quantidade

### 9.9 Troubleshooting

**Erro: "Connection refused"**
- Verificar se o servidor está rodando
- Verificar se a porta 8000 está disponível

**Erro: "401 Unauthorized"**
- Verificar se o token está sendo enviado no header
- Verificar se o token não expirou
- Fazer login novamente para obter novo token

**Erro: "404 Not Found"**
- Verificar se o ID do recurso existe no banco
- Verificar se a rota está correta

**Erro: "500 Internal Server Error"**
- Verificar logs do servidor
- Verificar conexão com Supabase
- Verificar variáveis de ambiente

**Erro: "Foreign key constraint"**
- Verificar se os IDs referenciados existem (unit_id, budget_id, etc.)
- Criar os recursos dependentes primeiro

---

**Última atualização:** 2025-11-29  
**Versão:** 2.0

## 10. Tabelas do Schema do Banco de Dados

### Tabelas com API Implementada
- `users` - Autenticação implementada
- `security_codes` - Usado em auth
- `storage` - CRUD implementado
- `units` - CRUD implementado
- `orders` - CRUD básico implementado
- `order_items` - Incluído em orders

### Tabelas sem API
- `budgets` - CRÍTICO (orders depende)
- `unit_users` - IMPORTANTE (permissões)
- `foods` - OPCIONAL (catálogo)

### Funcionalidades com Integração Externa
- `expenses` - Será consumido de API externa (desenvolvida por outro time)
- `attendance` - Será consumido de API externa (desenvolvida por outro time)

### Observações sobre Integrações Externas
- Definir contratos de API com os times responsáveis
- Documentar endpoints e estruturas de dados das APIs externas
- Implementar tratamento de erros e timeouts
- Considerar cache para reduzir chamadas às APIs externas
- Implementar fallbacks quando possível

