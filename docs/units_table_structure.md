# Estrutura da Tabela `units`

## Schema do Banco de Dados

```sql
CREATE TABLE public.units (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text,
  address text,
  type text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone,
  CONSTRAINT units_pkey PRIMARY KEY (id)
);
```

## Campos

| Campo | Tipo | Descrição | Constraints |
|-------|------|-----------|-------------|
| `id` | `uuid` | Identificador único da unidade | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() |
| `name` | `text` | Nome da unidade | NULL |
| `address` | `text` | Endereço da unidade | NULL |
| `type` | `text` | Tipo da unidade (ex: 'CCA', 'CEI') | NULL |
| `created_at` | `timestamptz` | Data de criação | NOT NULL, DEFAULT now() |
| `updated_at` | `timestamptz` | Data de atualização | NULL |

## Relacionamentos

- A tabela `storage` tem uma foreign key `unit_id` que referencia `units.id`
- A tabela `orders` tem uma foreign key `unit_id` que referencia `units.id`
- A tabela `unit_users` tem uma foreign key `unit_id` que referencia `units.id`

## Observações

1. **Primary Key**: O campo `id` é do tipo UUID e é gerado automaticamente
2. **Foreign Key Constraint**: Qualquer `unit_id` usado em outras tabelas deve existir na tabela `units`
3. **Campos Opcionais**: `name`, `address`, `type` e `updated_at` podem ser NULL
4. **Timestamp**: `created_at` é preenchido automaticamente na criação

## Uso no Código

Atualmente, o backend não possui um modelo `Unit` definido, mas a tabela é referenciada através de:
- `Storage.unit_id` - referencia `units.id`
- Validação de foreign key constraint no `StorageRepository`

## Recomendações

Para melhorar a integridade e facilitar o desenvolvimento, seria recomendado:
1. Criar um modelo `Unit` em `entities/models/unit.py`
2. Criar um `UnitRepository` para operações CRUD
3. Validar a existência do `unit_id` antes de criar registros em `storage`

