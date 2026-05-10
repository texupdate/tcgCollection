# Guia: Atualizar Imagens das Cartas

## 🖼️ Como Funciona

Se você importou cartas com URLs da Yugipedia (páginas wiki) ao invés de URLs diretas de imagens, use este script para buscar automaticamente as imagens reais.

## 📝 Padrão de URL da Yugipedia

O padrão usado no CSV é:
```
https://yugipedia.com/wiki/Nome_da_Carta
```

Onde os espaços são substituídos por `_` (underscore).

**Exemplo:**
- Nome: `Warrior of Zera`
- URL: `https://yugipedia.com/wiki/Warrior_of_Zera`

## 🚀 Como Usar

### 1. Certifique-se de que o Flask está rodando

```bash
python app.py
```

### 2. Execute o script de atualização

```bash
python fetch_card_images.py
```

### 3. Confirme a operação

```
Deseja continuar? (s/N): s
```

## ⚙️ O Que o Script Faz

1. **Busca todas as coleções** do banco de dados
2. **Para cada carta** com URL da Yugipedia:
   - Acessa a página da carta
   - Faz scraping do HTML
   - Extrai a URL da imagem real
   - Atualiza o banco de dados via API
3. **Aguarda 0.5s entre requisições** para não sobrecarregar o servidor
4. **Mostra progresso em tempo real**

## 📊 Exemplo de Saída

```
🖼️  TCG Collection Manager - Atualização de Imagens
============================================================
📚 Encontradas 41 coleções
============================================================

📖 Processando: AST
------------------------------------------------------------
  🔍 Buscando imagem: The End of Anubis
     Wiki: https://yugipedia.com/wiki/The_End_of_Anubis
     ✓ Imagem atualizada: https://ms.yugipedia.com/8/8f/TheEndofAnubis-AST-EN...
     
  🔍 Buscando imagem: Warrior of Zera
     Wiki: https://yugipedia.com/wiki/Warrior_of_Zera
     ✓ Imagem atualizada: https://ms.yugipedia.com/1/1e/WarriorofZera-AST-EN...

...

============================================================
📊 RESUMO
============================================================
✓ Imagens atualizadas: 2450
✗ Falhas: 64
============================================================
```

## ⏱️ Tempo de Execução

- **~0.5-1 segundo por carta** (com delay)
- Para 2500 cartas: **~20-40 minutos**
- É normal demorar! O script faz scraping de cada página

## ⚠️ Possíveis Problemas

### Imagem não encontrada
- Algumas páginas da Yugipedia podem ter estrutura diferente
- Cartas muito antigas podem não ter imagens de boa qualidade
- Cards promocionais podem estar em páginas especiais

### Erros de conexão
- Se houver muitos erros 429 (Too Many Requests):
  - Aumente o delay no script (linha com `time.sleep(0.5)`)
  - Tente novamente mais tarde

### Timeout
- Se a Yugipedia estiver lenta:
  - Aumente o timeout na função `get_image_url_from_yugipedia`
  - Atualmente está em 10 segundos

## 🔧 Personalizações

### Aumentar o delay entre requisições

Edite `fetch_card_images.py`:

```python
# Linha ~137
time.sleep(1.0)  # Era 0.5, agora 1 segundo
```

### Processar apenas uma coleção

Modifique o código para filtrar:

```python
collections = [c for c in collections if c['name'] == 'AST']
```

### Atualizar apenas cartas sem imagem

Adicione verificação antes do scraping:

```python
if card.get('image_url') and 'placeholder' in card['image_url']:
    # Só atualiza se for placeholder
```

## 🎯 Alternativa: API do YGOProDeck

Se preferir usar a API oficial do YGOProDeck ao invés de scraping:

```bash
# Criar script alternativo usando
# https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Nome+da+Carta
```

Vantagens:
- ✅ Mais rápido
- ✅ Mais confiável
- ✅ Imagens de melhor qualidade

Desvantagens:
- ❌ Precisa do nome exato da carta em inglês
- ❌ Não tem todas as versões/printings

## 📞 Suporte

Se tiver problemas, verifique:
1. Flask está rodando? ✓
2. BeautifulSoup4 instalado? `pip install beautifulsoup4` ✓
3. Conexão com internet ativa? ✓
4. URLs no banco estão corretas? ✓
