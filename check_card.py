#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, db
from models import Collection, Card
import sys

sys.stdout.reconfigure(encoding='utf-8')

with app.app_context():
    crv = Collection.query.filter_by(name='CRV').first()
    if crv:
        card = Card.query.filter_by(collection_id=crv.id, collection_number=14).first()
        if card:
            print(f"✅ Carta encontrada:")
            print(f"  ID: {card.id}")
            print(f"  Nome: {card.name}")
            print(f"  Collection Number: {card.collection_number}")
            print(f"  Image URL: {card.image_url}")
            print(f"  Tipo Origem: {card.tipoOrigem}")
        else:
            print("❌ Carta #14 não encontrada na coleção CRV")
    else:
        print("❌ Coleção CRV não encontrada")
