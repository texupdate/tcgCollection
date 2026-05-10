#!/usr/bin/env python3
"""
Script para restaurar image_urls das cartas Orica que perderam suas URLs
"""

import requests
import time
from app import app
from models import db, Card

def clean_card_name(name):
    """Remove caracteres especiais e formata o nome para a API"""
    # Remover sufixos como (as Alternate Name)
    if ' (as ' in name:
        name = name.split(' (as ')[0].strip()
    return name

def fetch_card_image(card_name):
    """Busca a imagem da carta na API YGOPRODeck"""
    try:
        clean_name = clean_card_name(card_name)
        url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={clean_name}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('data') and len(data['data']) > 0:
            # Pegar a primeira carta encontrada
            card_data = data['data'][0]
            
            # Pegar a imagem (tentar small primeiro, depois normal)
            if 'card_images' in card_data and len(card_data['card_images']) > 0:
                image_url = card_data['card_images'][0].get('image_url')
                return image_url
        
        return None
    except Exception as e:
        print(f"  ⚠️  Erro ao buscar {card_name}: {e}")
        return None

def restore_orica_images():
    """Restaura URLs de imagens para cartas Orica sem image_url"""
    
    with app.app_context():
        # Buscar todas as Oricas sem image_url
        oricas_sem_url = Card.query.filter_by(tipoOrigem='Orica').filter(
            (Card.image_url == None) | (Card.image_url == '')
        ).all()
        
        total = len(oricas_sem_url)
        print(f"\n🎨 Encontradas {total} cartas Orica sem image_url")
        print("=" * 60)
        
        if total == 0:
            print("✓ Todas as Oricas já têm URLs!")
            return
        
        success = 0
        failed = 0
        
        for i, card in enumerate(oricas_sem_url, 1):
            print(f"\n[{i}/{total}] Processando: {card.name} (#{card.collection_number})")
            
            image_url = fetch_card_image(card.name)
            
            if image_url:
                card.image_url = image_url
                db.session.commit()
                print(f"  ✓ URL atualizada: {image_url}")
                success += 1
            else:
                print(f"  ✗ Não encontrada na API")
                failed += 1
            
            # Rate limiting - aguardar 0.2s entre requisições
            if i < total:
                time.sleep(0.2)
        
        print("\n" + "=" * 60)
        print("📊 RESUMO")
        print("=" * 60)
        print(f"✓ URLs restauradas: {success}/{total}")
        print(f"✗ Não encontradas: {failed}/{total}")
        print(f"Taxa de sucesso: {(success/total*100):.1f}%")
        print("=" * 60)

if __name__ == '__main__':
    restore_orica_images()
