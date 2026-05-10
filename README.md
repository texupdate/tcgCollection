# TCG Collection Manager

Sistema de gerenciamento de coleção de cartas TCG (Trading Card Game) com servidor local.

## 📋 Descrição

Aplicação web localhost para gerenciar sua coleção de cartas TCG, permitindo:
- Cadastro e organização de cartas
- Controle de inventário
- Busca e filtros
- Estatísticas da coleção

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
