# 🎨 Importação de Cartas Orica via CSV

## 📋 Template CSV

Use o arquivo **`template_import_orica.csv`** como base para importar suas cartas Orica.

## 📊 Formato do CSV

```csv
collection_name;card_number;card_name;tipoOrigem;image_url;rarity;quantity;set_name;condition;language;notes
```

### Delimitador
- **Ponto e vírgula (;)** - Recomendado para evitar conflitos com vírgulas nos nomes
- **Vírgula (,)** - Também suportado, detectado automaticamente

### Encoding
- UTF-8 (recomendado)
- Latin-1, CP1252, ISO-8859-1 (fallback automático)

## 📝 Campos Detalhados

### Obrigatórios

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `collection_name` | Nome da coleção | `Orica Yu-Gi-Oh` |
| `card_number` | Número da carta na coleção | `1`, `2`, `3` |
| `card_name` | Nome da carta | `Dark Magician Girl Custom` |

### Opcionais

| Campo | Descrição | Valores | Padrão |
|-------|-----------|---------|--------|
| `tipoOrigem` | Tipo de origem | `Konami`, `Orica` | `Konami` |
| `image_url` | URL da imagem | URL completa | `null` |
| `rarity` | Raridade | `Common`, `Rare`, `Custom`, etc | `null` |
| `quantity` | Quantidade | Número inteiro | `0` |
| `set_name` | Nome do set | Texto livre | `null` |
| `condition` | Condição física | `Mint`, `Near Mint`, `Played` | `null` |
| `language` | Idioma | `Português`, `Inglês`, etc | `Português` |
| `notes` | Observações | Texto livre | `null` |

## 🎯 Exemplos Práticos

### Exemplo 1: Cartas Orica Simples
```csv
collection_name;card_number;card_name;tipoOrigem;quantity
Minhas Oricas;1;Custom Dragon;Orica;2
Minhas Oricas;2;Alternate Art Mage;Orica;1
Minhas Oricas;3;Fan Made Warrior;Orica;1
```

### Exemplo 2: Oricas com Imagens
```csv
collection_name;card_number;card_name;tipoOrigem;image_url;rarity;quantity
Orica Collection;1;Dark Magician Alt;Orica;https://imgur.com/abc123.jpg;Custom;1
Orica Collection;2;Blue-Eyes Custom;Orica;https://imgur.com/def456.jpg;Custom;2
```

### Exemplo 3: Misturando Originais e Oricas
```csv
collection_name;card_number;card_name;tipoOrigem;quantity;notes
LOB Expandido;1;Blue-Eyes White Dragon;Konami;1;Carta original
LOB Expandido;2;Blue-Eyes Alt Art;Orica;1;Arte customizada
LOB Expandido;3;Dark Magician;Konami;2;Carta original
LOB Expandido;4;Dark Magician Orica;Orica;1;Proxy para torneio casual
```

## 🚀 Como Usar

### 1. Prepare seu CSV
```bash
# Use o template como base
cp template_import_orica.csv minhas_oricas.csv

# Edite com Excel, LibreOffice, ou editor de texto
# IMPORTANTE: Salve como CSV com encoding UTF-8
```

### 2. Execute o script de importação
```bash
python import_cards.py minhas_oricas.csv
```

### 3. Acompanhe o progresso
O script mostrará:
- 🎨 = Carta Orica importada
- ✨ = Carta Konami importada
- ✓ = Sucesso
- ✗ = Erro

Exemplo de saída:
```
📁 Lendo arquivo: minhas_oricas.csv
============================================================
✓ Arquivo lido com encoding: utf-8-sig, delimitador: ';'

📚 Processando coleção: Orica Yu-Gi-Oh
------------------------------------------------------------
✓ Coleção 'Orica Yu-Gi-Oh' criada (ID: 42)
  🎨 Carta #001 - Dark Magician Girl Custom [Orica]
  🎨 Carta #002 - Blue-Eyes White Dragon Alt Art [Orica]
  🎨 Carta #003 - Red-Eyes Black Dragon Alternate [Orica]

============================================================
📊 RESUMO DA IMPORTAÇÃO
============================================================
✓ Coleções criadas: 1
✓ Cartas adicionadas: 3
✗ Erros: 0
============================================================
```

## ⚠️ Observações Importantes

### Numeração
- Cada coleção tem sua própria sequência de números
- Números devem ser únicos dentro da mesma coleção
- Cartas duplicadas (mesmo número) serão ignoradas

### Campo tipoOrigem
- **Konami**: Cartas oficiais (mostra logo Konami na interface)
- **Orica**: Cartas customizadas/proxies (mostra texto "ORICA" em vermelho)
- Se omitido, assume **Konami** por padrão

### Imagens
- URLs devem ser completas (incluir `http://` ou `https://`)
- Se não tiver imagem, deixe vazio ou use placeholder
- Sistema de busca automática de imagens funciona apenas para cartas oficiais

### Encoding no Excel
Se usar Excel:
1. Abra o CSV no Excel
2. Salvar Como → CSV (separado por vírgulas)
3. Ferramentas → Opções Web → Encoding → UTF-8

Se tiver problemas com acentos, salve como:
- **CSV UTF-8 (separado por vírgulas)** - Excel 2016+
- **CSV Delimitado por Ponto e Vírgula** + UTF-8

## 🔄 Atualizando Cartas Existentes

Para atualizar cartas já importadas:
1. Use a interface `/manage` para edição individual
2. Ou use a API REST para atualizações em massa

Exemplo API:
```bash
curl -X PUT http://localhost:5000/api/cards/123 \
  -H "Content-Type: application/json" \
  -d '{"tipoOrigem": "Orica", "quantity": 2}'
```

## 📖 Documentação Relacionada

- [README_IMPORT.md](README_IMPORT.md) - Documentação completa de importação
- [README_ORICA.md](README_ORICA.md) - Sistema Original vs Orica (detalhado)
- [API_DOCS.md](API_DOCS.md) - Documentação da API REST

## 🆘 Problemas Comuns

### Erro: "Número duplicado"
- A carta já existe na coleção com esse número
- Verifique se não há duplicatas no CSV
- Use números diferentes ou atualize via API

### Erro: "Encoding"
- Salve o CSV como UTF-8
- O script tenta automaticamente vários encodings
- Se falhar, converta manualmente: `iconv -f latin1 -t utf-8 input.csv > output.csv`

### Erro: "Servidor não está rodando"
- Inicie o servidor: `python app.py`
- Verifique se está rodando em http://127.0.0.1:5000

### Cartas não aparecem na interface
- Recarregue a página (Ctrl + Shift + R)
- Verifique o console do navegador (F12)
- Confirme que a coleção foi criada

## ✅ Checklist Antes de Importar

- [ ] CSV salvo com encoding UTF-8
- [ ] Delimitador consistente (`;` ou `,`)
- [ ] Coluna `tipoOrigem` com valores "Konami" ou "Orica"
- [ ] Números de cartas únicos por coleção
- [ ] Servidor Flask rodando (`python app.py`)
- [ ] Backup do banco de dados feito (opcional)

---

**Pronto!** Agora você pode importar suas cartas Orica em massa! 🎨🃏
