from flask import Flask, render_template, request, jsonify
from models import db, Card
import os

app = Flask(__name__)

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'tcg_collection.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Inicializa o banco de dados
db.init_app(app)

# Cria as tabelas se não existirem
with app.app_context():
    os.makedirs('instance', exist_ok=True)
    db.create_all()

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    """Retorna todas as cartas da coleção"""
    cards = Card.query.all()
    return jsonify([card.to_dict() for card in cards])

@app.route('/api/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    """Retorna uma carta específica"""
    card = Card.query.get_or_404(card_id)
    return jsonify(card.to_dict())

@app.route('/api/cards', methods=['POST'])
def add_card():
    """Adiciona uma nova carta à coleção"""
    data = request.get_json()
    
    new_card = Card(
        name=data.get('name'),
        set_name=data.get('set_name'),
        card_number=data.get('card_number'),
        rarity=data.get('rarity'),
        card_type=data.get('card_type'),
        quantity=data.get('quantity', 1),
        condition=data.get('condition'),
        language=data.get('language', 'Português'),
        notes=data.get('notes'),
        image_url=data.get('image_url'),
        purchase_price=data.get('purchase_price'),
        current_value=data.get('current_value')
    )
    
    db.session.add(new_card)
    db.session.commit()
    
    return jsonify(new_card.to_dict()), 201

@app.route('/api/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    """Atualiza uma carta existente"""
    card = Card.query.get_or_404(card_id)
    data = request.get_json()
    
    card.name = data.get('name', card.name)
    card.set_name = data.get('set_name', card.set_name)
    card.card_number = data.get('card_number', card.card_number)
    card.rarity = data.get('rarity', card.rarity)
    card.card_type = data.get('card_type', card.card_type)
    card.quantity = data.get('quantity', card.quantity)
    card.condition = data.get('condition', card.condition)
    card.language = data.get('language', card.language)
    card.notes = data.get('notes', card.notes)
    card.image_url = data.get('image_url', card.image_url)
    card.purchase_price = data.get('purchase_price', card.purchase_price)
    card.current_value = data.get('current_value', card.current_value)
    
    db.session.commit()
    
    return jsonify(card.to_dict())

@app.route('/api/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Remove uma carta da coleção"""
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    
    return jsonify({'message': 'Card deleted successfully'}), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas da coleção"""
    total_cards = db.session.query(db.func.sum(Card.quantity)).scalar() or 0
    unique_cards = Card.query.count()
    total_value = db.session.query(db.func.sum(Card.current_value * Card.quantity)).scalar() or 0
    
    return jsonify({
        'total_cards': int(total_cards),
        'unique_cards': unique_cards,
        'total_value': float(total_value)
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
