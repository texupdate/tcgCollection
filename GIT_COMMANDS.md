# Comandos Git - tcgCollection

## ✅ Já executado
```bash
# Repositório Git já foi inicializado e primeiro commit já foi feito!
git init
git add .
git commit -m "Initial commit: TCG Collection Manager setup"
```

## 📤 Próximos passos para publicar no GitHub

### 1. Criar repositório no GitHub
Acesse: https://github.com/new
- Nome do repositório: **tcgCollection**
- Descrição: Sistema de gerenciamento de coleção de cartas TCG
- Público ou Privado (sua escolha)
- **NÃO** marque "Initialize with README" (já temos um)

### 2. Conectar ao repositório remoto
```bash
# Substitua 'seu-usuario' pelo seu usuário do GitHub
git remote add origin https://github.com/seu-usuario/tcgCollection.git

# Verificar se o remote foi adicionado
git remote -v
```

### 3. Enviar código para o GitHub
```bash
# Primeira vez (cria a branch main e faz push)
git branch -M main
git push -u origin main
```

### 4. Comandos úteis para o dia a dia

```bash
# Ver status dos arquivos
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push

# Puxar mudanças do GitHub
git pull

# Ver histórico de commits
git log --oneline

# Criar nova branch
git checkout -b nome-da-branch

# Voltar para branch main
git checkout main
```

## 🚀 Comandos para rodar o projeto

```bash
# Entrar na pasta do projeto
cd c:\Documentos\GitHub\Git_tex\tcgCollection

# Criar ambiente virtual (primeira vez)
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Rodar o servidor
python app.py

# Acessar no navegador
# http://localhost:5000
```

## 📝 Dicas

- Sempre ative o ambiente virtual antes de rodar o projeto
- Faça commits regulares com mensagens descritivas
- Use branches para desenvolver novas funcionalidades
- Mantenha o .gitignore atualizado para não commitar arquivos desnecessários
