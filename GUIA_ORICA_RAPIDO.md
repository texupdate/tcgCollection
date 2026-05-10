# 🎨 Sistema Original vs Orica - Guia Rápido

## ✅ O Que Foi Implementado

### 1. Banco de Dados
- ✅ Campo `is_orica` adicionado à tabela `cards`
- ✅ Migração executada: 2514 cartas marcadas como Original (padrão)
- ✅ API atualizada para aceitar/retornar `is_orica`

### 2. Interface Web
- ✅ **Filtros**: 📋 Todas | ✨ Originais | 🎨 Oricas
- ✅ **Badge Visual**: Cartas Orica exibem badge vermelho "🎨 ORICA"
- ✅ Filtros funcionais em tempo real

### 3. Ferramentas
- ✅ Script `mark_as_orica.py` para marcação em massa
- ✅ Documentação completa em `README_ORICA.md`

---

## 🚀 Como Usar

### Ver na Interface Web

1. Acesse http://127.0.0.1:5000
2. Selecione uma coleção
3. Use os botões de filtro:
   - **📋 Todas**: Mostra todas as cartas
   - **✨ Originais**: Só cartas oficiais
   - **🎨 Oricas**: Só cartas customizadas

### Marcar Cartas como Orica

```bash
# Cartas individuais
python mark_as_orica.py "AST" 1,5,10

# Intervalos
python mark_as_orica.py "AST" 10-20

# Misturado
python mark_as_orica.py "AST" 1,5,10-15,20-25

# Reverter para Original
python mark_as_orica.py "AST" 5,10 --original
```

### Via API

```bash
# Marcar como Orica
curl -X PUT http://localhost:5000/api/cards/123 \
  -H "Content-Type: application/json" \
  -d '{"is_orica": true}'

# Marcar como Original
curl -X PUT http://localhost:5000/api/cards/123 \
  -H "Content-Type: application/json" \
  -d '{"is_orica": false}'
```

---

## 📊 Exemplos Práticos

### Cenário: Yu-Gi-Oh com Proxies

Você tem cartas originais caras e usa proxies para jogar:

```bash
# Marcar suas proxies (cartas 50-70 da coleção LOB)
python mark_as_orica.py "LOB" 50-70

# Visualizar
# Use filtro "Originais" para ver sua coleção real
# Use filtro "Oricas" para ver seus proxies
```

### Cenário: Artista de Custom Cards

```bash
# Todas as suas customs estão nas posições 1-30
python mark_as_orica.py "My Custom Set" 1-30

# Visualizar só suas customs
# Use filtro "Oricas"
```

---

## 🎯 Recursos Visuais

### Antes (sem filtro):
```
[Original] [Original] [Orica] [Original] [Orica]
```

### Depois (filtro "Originais"):
```
[Original] [Original] [     ] [Original] [     ]
```

### Depois (filtro "Oricas"):
```
[     ] [     ] [Orica] [     ] [Orica]
```

---

## 📝 Notas

- **Padrão**: Todas as cartas são Original
- **Reversível**: Pode mudar de Original ↔ Orica a qualquer momento
- **Quantidade**: Oricas e Originais compartilham o mesmo contador
- **Badge**: Aparece automaticamente em cartas marcadas como Orica

---

## 🔗 Links Úteis

- Documentação completa: [README_ORICA.md](README_ORICA.md)
- Repositório: https://github.com/texupdate/tcgCollection
- Servidor: http://127.0.0.1:5000

---

## ✅ Teste Rápido

```bash
# 1. Marcar uma carta de teste
python mark_as_orica.py "AST" 1

# 2. Abrir navegador
# http://127.0.0.1:5000

# 3. Selecionar coleção "AST"

# 4. Ver badge vermelho na carta #1

# 5. Testar filtros:
#    - Clicar "Oricas" → Ver só a carta #1
#    - Clicar "Originais" → Carta #1 desaparece
#    - Clicar "Todas" → Carta #1 aparece novamente

# 6. Reverter
python mark_as_orica.py "AST" 1 --original
```

Pronto! 🎉
