# Sistema Original vs Orica

## 🎨 O Que São Oricas?

**Orica** = Original Card Art (arte original customizada)  
São cartas **não oficiais** criadas por fãs ou artistas, incluindo:
- Cartas com arte alternativa/customizada
- Réplicas/proxies
- Cartas de teste/protótipo
- Fan-made cards

**Original** = Cartas oficiais produzidas pela Konami/fabricante oficial

## 🗄️ Banco de Dados

### Campo Adicionado: `is_orica`
- **Tipo**: Boolean
- **Padrão**: `False` (Original)
- **Valores**:
  - `False` ou `0` = Carta Original ✨
  - `True` ou `1` = Carta Orica 🎨

### Migração Executada
```bash
python migrate_add_orica.py
```

Todas as 2514 cartas foram marcadas como **Original** por padrão.

## 🌐 Interface Web

### Filtros Disponíveis

Na visualização do livro, você verá 3 botões:

```
📋 Todas    ✨ Originais    🎨 Oricas
```

- **Todas**: Mostra todas as cartas (originais e oricas)
- **Originais**: Mostra apenas cartas oficiais
- **Oricas**: Mostra apenas cartas customizadas

### Badge Visual

Cartas marcadas como **Orica** exibem um badge vermelho:

```
┌─────────────┐
│ 🎨 ORICA   │ ← Badge no canto superior direito
│             │
│   [Imagem]  │
│             │
│  Carta #5   │
└─────────────┘
```

## 🔧 Como Marcar Cartas como Orica

### Método 1: Script de Linha de Comando (Recomendado)

```bash
# Marcar cartas individuais
python mark_as_orica.py "AST" 1,5,10

# Marcar intervalo
python mark_as_orica.py "AST" 10-20

# Marcar mix (individual + intervalo)
python mark_as_orica.py "AST" 1,5,10-15,20,25-30

# Reverter para Original
python mark_as_orica.py "AST" 5,10 --original
```

**Sintaxe:**
```
python mark_as_orica.py <nome_coleção> <números> [--original]
```

**Exemplos práticos:**

```bash
# Todas as cartas de 1 a 10 da coleção LOB são oricas
python mark_as_orica.py "LOB" 1-10

# Cartas específicas da coleção AST
python mark_as_orica.py "AST" 0,5,15,25,35

# Desfazer: marcar como original novamente
python mark_as_orica.py "AST" 0,5 --original
```

### Método 2: API REST

#### Marcar como Orica
```bash
curl -X PUT http://localhost:5000/api/cards/123 \
  -H "Content-Type: application/json" \
  -d '{"is_orica": true}'
```

#### Marcar como Original
```bash
curl -X PUT http://localhost:5000/api/cards/123 \
  -H "Content-Type: application/json" \
  -d '{"is_orica": false}'
```

### Método 3: Interface de Gerenciamento

_(A implementar)_  
Futuramente, você poderá marcar/desmarcar diretamente na página `/manage`.

## 📊 Consultas no Banco

### SQLite - Contar Oricas por Coleção
```sql
SELECT 
    c.name AS collection_name,
    COUNT(*) FILTER (WHERE ca.is_orica = 1) AS oricas,
    COUNT(*) FILTER (WHERE ca.is_orica = 0) AS originais,
    COUNT(*) AS total
FROM cards ca
JOIN collections c ON ca.collection_id = c.id
GROUP BY c.name;
```

### Listar Todas as Oricas
```sql
SELECT 
    c.name AS collection,
    ca.collection_number,
    ca.name AS card_name,
    ca.quantity
FROM cards ca
JOIN collections c ON ca.collection_id = c.id
WHERE ca.is_orica = 1
ORDER BY c.name, ca.collection_number;
```

## 🎯 Casos de Uso

### Cenário 1: Colecionador Purista
```
Filtro: ✨ Originais
```
Mostra apenas cartas oficiais, esconde todas as oricas.

### Cenário 2: Jogador Casual (Usa Proxies)
```
Filtro: 📋 Todas
```
Vê tanto cartas originais quanto proxies/oricas.

### Cenário 3: Artista/Customizador
```
Filtro: 🎨 Oricas
```
Foco apenas nas cartas customizadas.

### Cenário 4: Organização de Inventário
```
# Marcar cartas falsas/suspeitas
python mark_as_orica.py "LOB" 50-60

# Depois filtrar para ver apenas essas
Filtro: 🎨 Oricas
```

## 📝 CSV Import

Ao importar cartas via CSV, adicione coluna `is_orica`:

```csv
collection_name,r_numr,card_name,image_url,is_orica
AST,0,The End of Anubis,https://...,0
AST,1,Custom Dark Magician,https://...,1
AST,2,Gogiga Gagagigo,https://...,0
```

Valores aceitos:
- `0`, `false`, `False`, vazio = Original
- `1`, `true`, `True` = Orica

## 🔄 Atualização em Massa

Para marcar muitas cartas de uma vez, use Python:

```python
import requests

# Marcar cartas 1-50 da coleção ID 5 como Orica
for card_num in range(1, 51):
    response = requests.get('http://localhost:5000/api/collections/5/cards')
    cards = response.json()
    
    for card in cards:
        if card['collection_number'] == card_num:
            requests.put(
                f'http://localhost:5000/api/cards/{card["id"]}',
                json={'is_orica': True}
            )
            print(f"Marcado: #{card_num}")
```

## ⚠️ Notas Importantes

1. **Padrão**: Todas as cartas são **Original** por padrão
2. **Reversível**: Você pode mudar entre Original ↔ Orica a qualquer momento
3. **Filtros**: Os filtros afetam apenas a visualização, não os dados
4. **Quantidade**: Oricas e Originais compartilham o mesmo contador de quantidade
5. **Backup**: Faça backup do banco antes de operações em massa

## 🚀 Próximas Melhorias

- [ ] Checkbox na página `/manage` para marcar/desmarcar
- [ ] Filtro na página de gerenciamento
- [ ] Estatísticas: "X originais, Y oricas"
- [ ] Exportar CSV separando originais e oricas
- [ ] Contador duplo (quantidade original + quantidade orica)

## 📞 Suporte

Dúvidas? Abra uma issue no GitHub!
