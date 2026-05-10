# Guia de Uso - TCG Collection Manager

## 🎯 Visão Geral

Sistema completo para gerenciar sua coleção de cartas TCG com visualização em formato de livro aberto.

## 📖 Como Usar

### 1. Iniciar o Servidor

```bash
cd c:\Documentos\GitHub\Git_tex\tcgCollection
python app.py
```

Acesse: **http://localhost:5000**

### 2. Criar uma Coleção

1. Acesse o menu **"⚙️ Gerenciar Coleção"**
2. Clique em **"➕ Nova Coleção"**
3. Preencha:
   - **Nome da Coleção**: Ex: "Pokémon Base Set"
   - **Descrição**: Ex: "Primeira coleção de Pokémon TCG"
   - **Total de Cartas**: Ex: 102 (número total de cartas que existem nessa coleção)
4. Clique em **"Salvar"**

### 3. Adicionar Cartas

1. Ainda na página de gerenciamento
2. Clique em **"➕ Nova Carta"**
3. Preencha:
   - **Coleção**: Selecione a coleção criada
   - **Número na Coleção**: Ex: 1 (posição da carta na coleção)
   - **Nome da Carta**: Ex: "Charizard"
   - **URL da Imagem**: Cole a URL da imagem da carta
   - **Quantidade Inicial**: Ex: 0 (você ajusta depois no livro)
4. Clique em **"Salvar"**

💡 **Dica**: Cadastre todas as cartas da coleção, mesmo que você não tenha nenhuma cópia. Deixe quantidade = 0.

### 4. Visualizar no Formato Livro

1. Volte para a página inicial (⬅️ Voltar para Visualização)
2. Selecione a coleção no dropdown
3. Visualize suas cartas em formato de livro:
   - **Página Esquerda**: Cartas 1-9
   - **Página Direita**: Cartas 10-18
4. Use os botões de navegação para ver outras páginas

### 5. Gerenciar Quantidade

Diretamente na visualização do livro:
- **Botão ➕**: Adiciona 1 carta ao estoque
- **Botão ➖**: Remove 1 carta do estoque
- **Quantidade 0**: Carta fica com transparência cinza

⚡ **As mudanças são salvas automaticamente no banco de dados!**

## 🎨 Layout do Livro

```
┌─────────────────────────────────────────────────────┐
│                    Minha Coleção TCG                 │
│     [Selecione Coleção ▼]  [⚙️ Gerenciar]          │
└─────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────┐
│   Página Esquerda    │   Página Direita     │
│   Cartas 0-8 ou 1-9  │   Cartas 9-17 ou 10-18│
├──────────────────────┼──────────────────────┤
│  ┌────┐ ┌────┐ ┌────┐│ ┌────┐ ┌────┐ ┌────┐│
│  │ #0 │ │ #1 │ │ #2 ││ │ #9 │ │#10 │ │#11 ││
│  └────┘ └────┘ └────┘│ └────┘ └────┘ └────┘│
│  ┌────┐ ┌────┐ ┌────┐│ ┌────┐ ┌────┐ ┌────┐│
│  │ #3 │ │ #4 │ │ #5 ││ │#12 │ │#13 │ │#14 ││
│  └────┘ └────┘ └────┘│ └────┘ └────┘ └────┘│
│  ┌────┐ ┌────┐ ┌────┐│ ┌────┐ ┌────┐ ┌────┐│
│  │ #6 │ │ #7 │ │ #8 ││ │#15 │ │#16 │ │#17 ││
│  └────┘ └────┘ └────┘│ └────┘ └────┘ └────┘│
└──────────────────────┴──────────────────────┘

    [⬅️ Anterior] Cartas 0-17 de 102 [Próximo ➡️]
```

**💡 Detecção Automática:**
- Se a coleção começa do **0**: mostra 0-17, depois 18-35, etc.
- Se a coleção começa do **1**: mostra 1-18, depois 19-36, etc.
- O sistema detecta automaticamente o menor número da coleção!

## 📝 Exemplo de Fluxo Completo

### Cenário: Criar coleção de Yu-Gi-Oh!

1. **Criar Coleção**
   - Nome: "Legend of Blue Eyes White Dragon"
   - Total: 126 cartas

2. **Adicionar Cartas**
   ```
   Carta #1: Blue-Eyes White Dragon
   URL: https://images.ygoprodeck.com/images/cards/89631139.jpg
   Quantidade: 0
   
   Carta #2: Dark Magician
   URL: https://images.ygoprodeck.com/images/cards/46986414.jpg
   Quantidade: 1
   
   ...continue até carta #126
   ```

3. **Visualizar e Atualizar**
   - Selecione a coleção
   - Navegue pelas páginas
   - Clique em ➕ quando comprar uma carta
   - Clique em ➖ quando vender/trocar uma carta

## 🔍 Onde Encontrar Imagens

### Pokémon TCG
- https://pokemontcg.io/
- https://www.pokemon.com/us/pokemon-tcg/

### Yu-Gi-Oh!
- https://ygoprodeck.com/api-guide/
- https://db.ygoprodeck.com/

### Magic: The Gathering
- https://scryfall.com/
- https://gatherer.wizards.com/

### One Piece Card Game
- https://asia-en.onepiece-cardgame.com/cardlist/

## 🛠️ Recursos Técnicos

### Banco de Dados
- SQLite (arquivo: `instance/tcg_collection.db`)
- Backup automático não implementado (copie o arquivo manualmente)

### API REST
- `GET /api/collections` - Lista coleções
- `GET /api/collections/{id}/cards` - Lista cartas de uma coleção
- `POST /api/cards/{id}/increment` - Adiciona +1 à quantidade
- `POST /api/cards/{id}/decrement` - Remove -1 da quantidade

Ver [API_DOCS.md](API_DOCS.md) para documentação completa.

## ⚠️ Limitações Atuais

- ❌ Sem upload de imagens (apenas URL)
- ❌ Sem busca/filtro na visualização do livro
- ❌ Sem edição de cartas no livro (apenas no gerenciamento)
- ❌ Sem backup automático
- ❌ Sem autenticação/múltiplos usuários

## 💡 Dicas

1. **URLs de Imagem**: Use sempre HTTPS para evitar problemas
2. **Numeração**: Mantenha a numeração oficial da coleção
3. **Backup**: Copie regularmente o arquivo `instance/tcg_collection.db`
4. **Performance**: Coleções muito grandes (>500 cartas) podem ficar lentas

## 🐛 Problemas Comuns

### Carta não aparece
- Verifique se o número está correto
- Verifique se a coleção está selecionada
- Atualize a página

### Imagem não carrega
- Verifique se a URL está correta
- Verifique se a URL é HTTPS
- Teste a URL no navegador

### Botões não funcionam
- Verifique o console do navegador (F12)
- Reinicie o servidor
- Limpe o cache do navegador

## 📞 Suporte

Problemas ou sugestões? Abra uma issue no GitHub!
