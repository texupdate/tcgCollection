from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Collection(db.Model):
    """Modelo para representar uma coleção de cartas"""
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    total_cards = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com cartas
    cards = db.relationship('Card', backref='collection', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'total_cards': self.total_cards,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Collection {self.name}>'


class Card(db.Model):
    """Modelo para representar uma carta da coleção"""
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=False)
    collection_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    set_name = db.Column(db.String(100))
    card_number = db.Column(db.String(50))
    rarity = db.Column(db.String(50))
    card_type = db.Column(db.String(50))
    tipoOrigem = db.Column(db.String(20), default='Konami')  # 'Konami' ou 'Orica'
    quantity = db.Column(db.Integer, default=0)
    condition = db.Column(db.String(50))
    language = db.Column(db.String(50), default='Português')
    notes = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    purchase_price = db.Column(db.Float)
    current_value = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint para garantir numeração única por coleção
    __table_args__ = (db.UniqueConstraint('collection_id', 'collection_number', name='unique_card_number_per_collection'),)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'collection_number': self.collection_number,
            'name': self.name,
            'set_name': self.set_name,
            'card_number': self.card_number,
            'rarity': self.rarity,
            'card_type': self.card_type,
            'tipoOrigem': self.tipoOrigem,
            'quantity': self.quantity,
            'condition': self.condition,
            'language': self.language,
            'notes': self.notes,
            'image_url': self.image_url,
            'purchase_price': self.purchase_price,
            'current_value': self.current_value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Card #{self.collection_number} {self.name}>'
