#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from app import app, db
from models import Card
import sys

sys.stdout.reconfigure(encoding='utf-8')

def try_alternative_names(card_id, alternatives):
    """Tenta buscar a carta com nomes alternativos"""
    with app.app_context():
        card = Card.query.get(card_id)
        if not card:
            return False
        
        print(f"\n🔍 {card.name}")
        
        for alt_name in alternatives:
            print(f"   Tentando: {alt_name}")
            try:
                api_url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={alt_name}"
                response = requests.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and len(data['data']) > 0:
                        card_info = data['data'][0]
                        
                        if 'card_images' in card_info and len(card_info['card_images']) > 0:
                            image_url = card_info['card_images'][0]['image_url']
                            card.image_url = image_url
                            db.session.commit()
                            
                            print(f"   ✅ Sucesso! Imagem atualizada")
                            return True
            except:
                pass
        
        print(f"   ❌ Nenhum nome alternativo funcionou")
        return False

# Tentar corrigir as 2 que falharam
print("="*60)
print("Tentando corrigir cartas que falharam...")
print("="*60)

# Judgment of Pharaoh (JUMP #8) - ID 662
try_alternative_names(662, [
    "Judgment of the Pharaoh",
    "Pharaoh's Judgment",
    "Judgment of Anubis"
])

# Luster Dragon #2 (LOD #50) - ID 1125
try_alternative_names(1125, [
    "Luster Dragon",
    "Luster Dragon 2",
    "Sapphire Dragon"
])

print("\n" + "="*60)
print("Processo concluído!")
print("="*60)
