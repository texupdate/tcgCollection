#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, db
from models import Card
import sys

sys.stdout.reconfigure(encoding='utf-8')

with app.app_context():
    # Buscar cartas com "(as " no nome e sem imagem
    cards_with_as = Card.query.filter(
        Card.name.like('% (as %'),
        Card.image_url.is_(None)
    ).all()
    
    print(f"📊 Cartas com '(as ...)' no nome e sem imagem: {len(cards_with_as)}\n")
    
    if cards_with_as:
        for card in cards_with_as:
            print(f"ID {card.id}: {card.name} (Coleção: {card.collection.name} #{card.collection_number})")
    else:
        print("✅ Nenhuma carta encontrada com esse problema!")
