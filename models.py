from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Card(db.Model):
    """Modelo para representar uma carta da coleção"""
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    set_name = db.Column(db.String(100))
    card_number = db.Column(db.String(50))
    rarity = db.Column(db.String(50))
    card_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=1)
    condition = db.Column(db.String(50))
    language = db.Column(db.String(50), default='Português')
    notes = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    purchase_price = db.Column(db.Float)
    current_value = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'set_name': self.set_name,
            'card_number': self.card_number,
            'rarity': self.rarity,
            'card_type': self.card_type,
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
        return f'<Card {self.name} - {self.set_name}>'
