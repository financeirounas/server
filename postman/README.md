# Postman Collection - Storage API

Esta pasta contém a coleção do Postman para testar as rotas de estoque (storage) da API UNAS.

## Como usar

1. **Importar a coleção no Postman:**
   - Abra o Postman
   - Clique em "Import"
   - Selecione o arquivo `Storage_API.postman_collection.json`

2. **Configurar variáveis de ambiente:**
   - A coleção já inclui variáveis padrão:
     - `base_url`: `http://localhost:8000` (ajuste se necessário)
     - `unit_id`: **IMPORTANTE**: Substitua pelo ID real de uma unidade que existe na tabela `units` do seu banco de dados. 
       - O valor padrão `00000000-0000-0000-0000-000000000000` é apenas um placeholder e causará erro de foreign key constraint.
       - Para obter um `unit_id` válido, você pode:
         - Consultar diretamente no banco: `SELECT id FROM units LIMIT 1;`
         - Ou criar uma unidade primeiro através da interface do sistema

3. **Testar os endpoints:**

   ### GET /storage
   - Lista todos os itens de estoque de uma unidade
   - Requer: `unit_id` como query parameter

   ### POST /storage/entry
   - Registra entrada de estoque
   - Se o item já existe (mesmo `name` + `unit_id`), incrementa a quantidade
   - Caso contrário, cria um novo registro
   - Exemplos incluídos:
     - Entrada comprada (com nota fiscal)
     - Entrada doada (sem nota fiscal)
     - Novo item

   ### POST /storage/exit
   - Registra saída de estoque
   - Valida disponibilidade antes de decrementar
   - Suporta múltiplos itens em uma única requisição
   - Exemplos incluídos:
     - Saída com múltiplos itens
     - Saída com item único
     - Teste de erro (quantidade insuficiente)

## Estrutura das Requisições

### Entrada (Entry)
```json
{
    "name": "Arroz integral",
    "amount": 100.0,
    "unit_id": "uuid-da-unidade",
    "type": "comprado",  // ou "doado"
    "supplier": "Nome do fornecedor/doador",
    "invoice": "NF-12345",  // opcional
    "responsible": "Nome do responsável",
    "date": "2024-01-15"
}
```

### Saída (Exit)
```json
{
    "items": [
        {
            "name": "Arroz integral",
            "amount": 25.0
        }
    ],
    "purpose": "Almoço",
    "responsible": "Nome do responsável",
    "date": "2024-01-17",
    "notes": "Observações opcionais",
    "unit_id": "uuid-da-unidade"
}
```

## Notas

- A API roda na porta 8000 por padrão
- Não há autenticação implementada (conforme especificado)
- O campo `type` deve ser "comprado" ou "doado"
- O campo `amount` deve ser maior que 0
- A data deve estar no formato ISO (YYYY-MM-DD)

