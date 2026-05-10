from flask import Flask, render_template, request, jsonify
from models import db, Card, Collection
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
    """Página inicial - visualização de livro"""
    return render_template('index.html')

@app.route('/manage')
def manage():
    """Página de gerenciamento de cartas"""
    return render_template('manage.html')

# ============= COLLECTIONS ENDPOINTS =============

@app.route('/api/collections', methods=['GET'])
def get_collections():
    """Retorna todas as coleções"""
    collections = Collection.query.all()
    return jsonify([c.to_dict() for c in collections])

@app.route('/api/collections/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    """Retorna uma coleção específica"""
    collection = Collection.query.get_or_404(collection_id)
    return jsonify(collection.to_dict())

@app.route('/api/collections', methods=['POST'])
def add_collection():
    """Adiciona uma nova coleção"""
    data = request.get_json()
    
    new_collection = Collection(
        name=data.get('name'),
        description=data.get('description'),
        total_cards=data.get('total_cards', 0)
    )
    
    db.session.add(new_collection)
    db.session.commit()
    
    return jsonify(new_collection.to_dict()), 201

@app.route('/api/collections/<int:collection_id>', methods=['PUT'])
def update_collection(collection_id):
    """Atualiza uma coleção"""
    collection = Collection.query.get_or_404(collection_id)
    data = request.get_json()
    
    collection.name = data.get('name', collection.name)
    collection.description = data.get('description', collection.description)
    collection.total_cards = data.get('total_cards', collection.total_cards)
    
    db.session.commit()
    
    return jsonify(collection.to_dict())

@app.route('/api/collections/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    """Remove uma coleção"""
    collection = Collection.query.get_or_404(collection_id)
    db.session.delete(collection)
    db.session.commit()
    
    return jsonify({'message': 'Collection deleted successfully'}), 200

# ============= CARDS ENDPOINTS =============

@app.route('/api/collections/<int:collection_id>/cards', methods=['GET'])
def get_collection_cards(collection_id):
    """Retorna todas as cartas de uma coleção ordenadas por número"""
    page = request.args.get('page', 1, type=int)
    cards = Card.query.filter_by(collection_id=collection_id).order_by(Card.collection_number).all()
    
    # Retorna todas as cartas sem paginação (faremos no frontend)
    return jsonify([card.to_dict() for card in cards])

@app.route('/api/cards', methods=['GET'])
def get_cards():
    """Retorna todas as cartas"""
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
        collection_id=data.get('collection_id'),
        collection_number=data.get('collection_number'),
        name=data.get('name'),
        set_name=data.get('set_name'),
        card_number=data.get('card_number'),
        rarity=data.get('rarity'),
        card_type=data.get('card_type'),
        tipoOrigem=data.get('tipoOrigem', 'Konami'),
        quantity=data.get('quantity', 0),
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
    card.collection_number = data.get('collection_number', card.collection_number)
    card.set_name = data.get('set_name', card.set_name)
    card.card_number = data.get('card_number', card.card_number)
    card.rarity = data.get('rarity', card.rarity)
    card.card_type = data.get('card_type', card.card_type)
    card.tipoOrigem = data.get('tipoOrigem', card.tipoOrigem)
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

@app.route('/api/cards/<int:card_id>/increment', methods=['POST'])
def increment_card_quantity(card_id):
    """Incrementa a quantidade de uma carta"""
    card = Card.query.get_or_404(card_id)
    card.quantity += 1
    db.session.commit()
    
    return jsonify(card.to_dict())

@app.route('/api/cards/<int:card_id>/decrement', methods=['POST'])
def decrement_card_quantity(card_id):
    """Decrementa a quantidade de uma carta"""
    card = Card.query.get_or_404(card_id)
    if card.quantity > 0:
        card.quantity -= 1
    db.session.commit()
    
    return jsonify(card.to_dict())

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas da coleção"""
    total_cards = db.session.query(db.func.sum(Card.quantity)).scalar() or 0
    unique_cards = Card.query.count()
    total_value = db.session.query(db.func.sum(Card.current_value * Card.quantity)).scalar() or 0
    total_collections = Collection.query.count()
    
    return jsonify({
        'total_cards': int(total_cards),
        'unique_cards': unique_cards,
        'total_value': float(total_value),
        'total_collections': total_collections
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
