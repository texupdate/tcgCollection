#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
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

def fix_all_as_cards():
    """Corrige todas as cartas com '(as ...)' no nome sem imagem"""
    with app.app_context():
        # Buscar cartas com "(as " no nome e sem imagem
        cards_with_as = Card.query.filter(
            Card.name.like('% (as %'),
            Card.image_url.is_(None)
        ).all()
        
        total = len(cards_with_as)
        print(f"📊 Total de cartas para corrigir: {total}\n")
        
        success = 0
        failed = 0
        
        for i, card in enumerate(cards_with_as, 1):
            print(f"[{i}/{total}] 🔍 {card.name}")
            print(f"          Coleção: {card.collection.name} #{card.collection_number}")
            
            # Limpar nome
            clean_name = clean_card_name(card.name)
            print(f"          Nome limpo: {clean_name}")
            
            # Buscar na API
            try:
                api_url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={clean_name}"
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
                            
                            print(f"          ✅ Imagem atualizada")
                            success += 1
                        else:
                            print(f"          ⚠️ Sem imagens disponíveis")
                            failed += 1
                    else:
                        print(f"          ⚠️ Carta não encontrada na API")
                        failed += 1
                else:
                    print(f"          ❌ Erro HTTP {response.status_code}")
                    failed += 1
                    
            except Exception as e:
                print(f"          ❌ Erro: {e}")
                failed += 1
            
            # Rate limiting (respeitar a API)
            if i < total:
                time.sleep(0.5)
            
            print()
        
        print("\n" + "="*60)
        print(f"✅ Sucesso: {success}")
        print(f"❌ Falhas: {failed}")
        print(f"📊 Total: {total}")
        print("="*60)

if __name__ == "__main__":
    fix_all_as_cards()
