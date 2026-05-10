# 📥 Importação em Massa de Cartas

Script para importar cartas de coleção em massa a partir de arquivos CSV.

## 🚀 Como Usar

### 1. Preparar o arquivo CSV

Crie um arquivo CSV com os seguintes campos:

**Campos Obrigatórios:**
- `collection_name` - Nome da coleção
- `card_number` - Número da carta na coleção (1, 2, 3...)
- `card_name` - Nome da carta

**Campos Opcionais:**
- `image_url` - URL da imagem da carta
- `rarity` - Raridade (Common, Rare, Ultra Rare, etc)
- `quantity` - Quantidade inicial (padrão: 0)
- `set_name` - Nome do set/expansão
- `set_card_number` - Número oficial da carta no set
- `condition` - Condição (Mint, Near Mint, etc)
- `language` - Idioma (padrão: Português)
- `notes` - Observações

### 2. Exemplo de CSV

Veja o arquivo `exemplo_import.csv` incluído no projeto:

```csv
collection_name,card_number,card_name,image_url,rarity,quantity
Pokémon Base Set,1,Alakazam,https://images.pokemontcg.io/base1/1_hires.png,Rare,0
Pokémon Base Set,2,Blastoise,https://images.pokemontcg.io/base1/2_hires.png,Rare,1
Pokémon Base Set,4,Charizard,https://images.pokemontcg.io/base1/4_hires.png,Rare,2
Yu-Gi-Oh! LOB,1,Blue-Eyes White Dragon,https://images.ygoprodeck.com/images/cards/89631139.jpg,Ultra Rare,1
```

### 3. Executar a Importação

**Importante:** O servidor Flask deve estar rodando!

```bash
# Terminal 1: Inicie o servidor
python app.py

# Terminal 2: Execute a importação
python import_cards.py exemplo_import.csv
```

### 4. Saída Esperada

```
🎴 TCG Collection Manager - Importador CSV
============================================================
✓ Servidor Flask está online

📁 Lendo arquivo: exemplo_import.csv
============================================================

📚 Processando coleção: Pokémon Base Set
------------------------------------------------------------
✓ Coleção 'Pokémon Base Set' criada (ID: 1)
  ✓ Carta #001 - Alakazam
  ✓ Carta #002 - Blastoise
  ✓ Carta #004 - Charizard

📚 Processando coleção: Yu-Gi-Oh! LOB
------------------------------------------------------------
✓ Coleção 'Yu-Gi-Oh! LOB' criada (ID: 2)
  ✓ Carta #001 - Blue-Eyes White Dragon

============================================================
📊 RESUMO DA IMPORTAÇÃO
============================================================
✓ Coleções criadas: 2
✓ Cartas adicionadas: 4
✗ Erros: 0
============================================================
```

## 💡 Dicas

### Criar CSV no Excel/Google Sheets

1. Crie uma planilha com as colunas
2. Preencha os dados
3. Salve como CSV (UTF-8)

### Exportar de um site TCG

Muitos sites permitem exportar listas de cartas. Você pode:

1. Exportar a lista
2. Abrir no Excel
3. Ajustar as colunas para o formato correto
4. Salvar como CSV

### URLs de Imagens

#### Pokémon TCG
```
https://images.pokemontcg.io/base1/4_hires.png
```
Formato: `base1` = set, `4` = número da carta

#### Yu-Gi-Oh!
```
https://images.ygoprodeck.com/images/cards/89631139.jpg
```
Use o ID da carta do banco de dados YGOPro

#### Magic: The Gathering
```
https://cards.scryfall.io/large/front/0/0/001.jpg
```
Use a API do Scryfall

### Importação Incremental

O script é seguro para executar múltiplas vezes:
- ✅ Coleções existentes são reutilizadas
- ✅ Cartas duplicadas geram erro mas não quebram o processo
- ✅ Você pode adicionar mais cartas depois

### Atualizar Total de Cartas na Coleção

Se você sabe quantas cartas tem no total na coleção, atualize depois:

1. Acesse `/manage`
2. Veja a coleção criada
3. Ou edite diretamente o total no banco

## 🐛 Solução de Problemas

### Erro: Servidor Flask não está rodando
```bash
python app.py
```

### Erro: Carta duplicada
O número da carta já existe na coleção. Verifique o CSV.

### Erro: Arquivo não encontrado
Verifique o caminho do arquivo CSV.

### Erro de encoding (caracteres estranhos)
Salve o CSV como UTF-8:
- Excel: "Salvar Como" → "CSV UTF-8"
- Google Sheets: Download → "CSV"

### Imagens não aparecem
- Verifique se as URLs estão corretas
- Teste as URLs no navegador
- Use HTTPS sempre que possível

## 📊 Formato Completo do CSV

Para todos os campos disponíveis:

```csv
collection_name,card_number,card_name,image_url,rarity,quantity,set_name,set_card_number,condition,language,notes
Pokémon Base Set,4,Charizard,https://images.pokemontcg.io/base1/4_hires.png,Rare,2,Base Set,4/102,Near Mint,Português,Carta favorita
```

## ⚙️ Script Python

O script `import_cards.py` faz:

1. ✅ Lê o arquivo CSV
2. ✅ Agrupa cartas por coleção
3. ✅ Cria coleções automaticamente
4. ✅ Calcula o total de cartas por coleção
5. ✅ Adiciona cada carta via API
6. ✅ Mostra progresso em tempo real
7. ✅ Exibe estatísticas no final

## 🔧 Personalização

Você pode modificar o script para:
- Adicionar validações personalizadas
- Conectar com APIs externas
- Fazer backup antes de importar
- Gerar relatórios detalhados

## 📝 Exemplo Prático

Vamos importar uma coleção completa do Pokémon Base Set (102 cartas):

1. Baixe a lista de cartas
2. Crie um CSV com todas as 102 cartas
3. Execute: `python import_cards.py pokemon_base_set.csv`
4. Acesse a visualização do livro
5. Veja todas as cartas organizadas!

## 🎯 Próximos Passos

Depois de importar:
1. Acesse http://localhost:5000
2. Selecione a coleção
3. Use os botões +/- para gerenciar seu estoque
4. Aproveite a visualização em formato de livro!
