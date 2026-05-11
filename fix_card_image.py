#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from app import app, db
from models import Card
import sys

sys.stdout.reconfigure(encoding='utf-8')

def clean_card_name(name):
    """Limpa o nome da carta removendo sufixos problemáticos"""
    clean_name = name.strip()
    
    # Remover sufixo (as ...)
    if ' (as ' in clean_name:
        clean_name = clean_name.split(' (as ')[0].strip()
    
    return clean_name

def fetch_image_for_card(card_id):
    """Busca imagem para uma carta específica"""
    with app.app_context():
        card = Card.query.get(card_id)
        if not card:
            print(f"❌ Carta ID {card_id} não encontrada")
            return
        
        print(f"\n🔍 Processando: {card.name}")
        
        # Limpar nome
        clean_name = clean_card_name(card.name)
        print(f"   Nome limpo: {clean_name}")
        
        # Buscar na API
        try:
            api_url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={clean_name}"
            print(f"   🌐 Buscando API: {api_url}")
            
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    card_info = data['data'][0]
                    
                    # Pegar URL da imagem
                    if 'card_images' in card_info and len(card_info['card_images']) > 0:
                        image_url = card_info['card_images'][0]['image_url']
                        
                        # Atualizar no banco
                        card.image_url = image_url
                        db.session.commit()
                        
                        print(f"   ✅ Imagem atualizada: {image_url}")
                        return True
                    else:
                        print(f"   ⚠️ Sem imagens disponíveis")
                else:
                    print(f"   ⚠️ Carta não encontrada na API")
            else:
                print(f"   ❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        return False

if __name__ == "__main__":
    # ID da carta CRV #14
    card_id = 126
    fetch_image_for_card(card_id)
