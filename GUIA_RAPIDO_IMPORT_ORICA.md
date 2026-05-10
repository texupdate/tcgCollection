# 🎨 Guia Rápido: Importar Cartas Orica

## ⚡ Começando Rápido

### 1. Use o Template
Abra o arquivo **`template_import_orica.csv`** no Excel, LibreOffice ou editor de texto.

### 2. Preencha suas Oricas
```csv
collection_name;card_number;card_name;tipoOrigem;quantity
Minhas Oricas;1;Dark Magician Custom;Orica;2
Minhas Oricas;2;Blue-Eyes Alt Art;Orica;1
Minhas Oricas;3;Red-Eyes Custom;Orica;1
```

### 3. Salve como CSV UTF-8

**Excel:**
- Arquivo → Salvar Como
- Tipo: "CSV UTF-8 (separado por vírgulas)"

**LibreOffice Calc:**
- Arquivo → Salvar Como
- Tipo: "Texto CSV (.csv)"
- Codificação: "Unicode (UTF-8)"

**Google Sheets:**
- Arquivo → Fazer download → CSV (.csv)

### 4. Execute a Importação
```bash
python import_cards.py minhas_oricas.csv
```

## 📊 Colunas do CSV

### Obrigatórias
- **collection_name**: Nome da coleção (ex: "Orica Yu-Gi-Oh")
- **card_number**: Número sequencial (1, 2, 3...)
- **card_name**: Nome da carta

### Importantes para Orica
- **tipoOrigem**: Coloque `Orica` (se deixar vazio, assume `Konami`)
- **quantity**: Quantas você tem
- **image_url**: Link da imagem (opcional)

### Opcionais
- rarity, set_name, condition, language, notes

## 🎯 Exemplo Completo

Crie um arquivo `minhas_oricas.csv`:

```csv
collection_name;card_number;card_name;tipoOrigem;image_url;quantity;notes
Orica LOB;1;Blue-Eyes White Dragon Custom;Orica;https://i.imgur.com/abc123.jpg;1;Arte por @artista
Orica LOB;2;Dark Magician Alternate;Orica;https://i.imgur.com/def456.jpg;2;Proxy para jogo
Orica LOB;3;Red-Eyes B. Dragon Alt;Orica;;1;Sem imagem ainda
```

Depois execute:
```bash
python import_cards.py minhas_oricas.csv
```

Você verá:
```
🎨 Carta #001 - Blue-Eyes White Dragon Custom [Orica]
🎨 Carta #002 - Dark Magician Alternate [Orica]
🎨 Carta #003 - Red-Eyes B. Dragon Alt [Orica]
```

## 💡 Dicas

### Misturar Originais e Oricas
```csv
collection_name;card_number;card_name;tipoOrigem;quantity
Minha Coleção;1;Carta Original;Konami;3
Minha Coleção;2;Carta Orica;Orica;1
Minha Coleção;3;Outra Original;Konami;2
```

### Múltiplas Coleções no Mesmo CSV
```csv
collection_name;card_number;card_name;tipoOrigem;quantity
Oricas Set 1;1;Carta A;Orica;1
Oricas Set 1;2;Carta B;Orica;1
Oricas Set 2;1;Carta C;Orica;2
Oricas Set 2;2;Carta D;Orica;1
```

### Adicionar Mais Tarde
Você pode importar o CSV quantas vezes quiser. Novas cartas serão adicionadas, cartas duplicadas serão ignoradas.

## ⚠️ Erros Comuns

### "Número duplicado"
- Já existe carta com esse número na coleção
- Use número diferente ou delete a carta antiga

### "Encoding error"
- Salve o CSV como UTF-8
- No Excel: use "CSV UTF-8"

### "Servidor não rodando"
```bash
python app.py
```

## 📚 Documentação Completa

Para mais detalhes, veja: [README_IMPORT_ORICA.md](README_IMPORT_ORICA.md)

---

**Pronto! Agora é só preencher o CSV e importar suas Oricas! 🎨**
