# API Documentation - tcgCollection

## 📊 Endpoints da API

### Cards (Cartas)

#### GET /api/cards
Retorna todas as cartas da coleção

**Response:**
```json
[
  {
    "id": 1,
    "name": "Carta Exemplo",
    "set_name": "Set Base",
    "card_number": "001",
    "rarity": "Rare",
    "card_type": "Monster",
    "quantity": 3,
    "condition": "Near Mint",
    "language": "Português",
    "notes": "Observações sobre a carta",
    "image_url": null,
    "purchase_price": 10.50,
    "current_value": 15.00,
    "created_at": "2026-05-09T12:00:00",
    "updated_at": "2026-05-09T12:00:00"
  }
]
```

#### GET /api/cards/{id}
Retorna uma carta específica

**Parâmetros:**
- `id` (int): ID da carta

#### POST /api/cards
Adiciona uma nova carta à coleção

**Body:**
```json
{
  "name": "Nome da Carta",
  "set_name": "Nome do Set",
  "card_number": "001",
  "rarity": "Rare",
  "card_type": "Monster",
  "quantity": 1,
  "condition": "Near Mint",
  "language": "Português",
  "notes": "Notas opcionais",
  "image_url": "url_da_imagem",
  "purchase_price": 10.50,
  "current_value": 15.00
}
```

#### PUT /api/cards/{id}
Atualiza uma carta existente

**Parâmetros:**
- `id` (int): ID da carta

**Body:** Mesmos campos do POST

#### DELETE /api/cards/{id}
Remove uma carta da coleção

**Parâmetros:**
- `id` (int): ID da carta

**Response:**
```json
{
  "message": "Card deleted successfully"
}
```

### Stats (Estatísticas)

#### GET /api/stats
Retorna estatísticas da coleção

**Response:**
```json
{
  "total_cards": 150,
  "unique_cards": 50,
  "total_value": 1250.50
}
```

## 🗄️ Modelo de Dados

### Card (Carta)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | Integer | Auto | ID único da carta |
| name | String(200) | Sim | Nome da carta |
| set_name | String(100) | Não | Nome do set/expansão |
| card_number | String(50) | Não | Número da carta no set |
| rarity | String(50) | Não | Raridade (Common, Rare, etc) |
| card_type | String(50) | Não | Tipo da carta |
| quantity | Integer | Não | Quantidade (padrão: 1) |
| condition | String(50) | Não | Condição física da carta |
| language | String(50) | Não | Idioma (padrão: Português) |
| notes | Text | Não | Notas adicionais |
| image_url | String(500) | Não | URL da imagem da carta |
| purchase_price | Float | Não | Preço de compra |
| current_value | Float | Não | Valor atual de mercado |
| created_at | DateTime | Auto | Data de criação |
| updated_at | DateTime | Auto | Data da última atualização |

## 🎯 Próximas Funcionalidades Sugeridas

- [ ] Busca e filtros por nome, set, raridade
- [ ] Upload de imagens das cartas
- [ ] Importação/Exportação de coleção (CSV, JSON)
- [ ] Gráficos de estatísticas
- [ ] Integração com APIs de preços (TCGPlayer, etc)
- [ ] Sistema de autenticação
- [ ] Múltiplas coleções/decks
- [ ] Histórico de preços
- [ ] Wishlist (cartas desejadas)
- [ ] Trading system (registro de trocas)
