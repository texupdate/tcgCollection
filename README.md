# TCG Collection Manager

Sistema de gerenciamento de coleção de cartas TCG (Trading Card Game) com visualização em formato de livro aberto.

## 📋 Descrição

Aplicação web localhost para gerenciar sua coleção de cartas TCG com visualização interativa em formato de livro, permitindo:
- 📚 Múltiplas coleções com numeração própria
- 📖 Visualização em formato de livro aberto (18 cartas por página)
- ➕➖ Controle de estoque com botões + e - 
- 🖼️ Imagens das cartas via URL
- 📊 Efeito visual para cartas com quantidade zero
- 🔍 Busca e filtros
- 📈 Estatísticas da coleção

## ✨ Funcionalidades Principais

### Visualização de Livro
- Layout em formato de livro aberto
- Página esquerda: cartas 1-9
- Página direita: cartas 10-18
- Navegação entre páginas
- Transparência cinza para cartas com quantidade 0

### Gerenciamento
- Criar múltiplas coleções
- Cadastrar cartas com número específico por coleção
- Incrementar/decrementar quantidade diretamente no livro
- Editar e remover cartas e coleções

## 🛠️ Tecnologias

- **Backend**: Python + Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML/CSS/JavaScript

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/tcgCollection.git
cd tcgCollection

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

## ▶️ Como Usar

```bash
# Execute o servidor
python app.py

# Acesse no navegador
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
tcgCollection/
├── app.py              # Servidor principal
├── database.py         # Configuração do banco de dados
├── models.py           # Modelos de dados
├── requirements.txt    # Dependências
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── templates/         # Templates HTML
└── instance/          # Banco de dados (gerado automaticamente)
```

## 📝 Licença

MIT License

## 👤 Autor

Seu Nome
