#!/usr/bin/env python3
"""
Script para buscar URLs reais de imagens a partir de links da Yugipedia.

Uso: python fetch_card_images.py
"""

import requests
import time
import sys
from bs4 import BeautifulSoup

API_BASE_URL = "http://127.0.0.1:5000/api"

def get_image_url_from_yugipedia(wiki_url: str) -> str:
    """
    Extrai a URL da imagem principal de uma página da Yugipedia.
    
    Args:
        wiki_url: URL da página da carta na Yugipedia
    
    Returns:
        URL da imagem ou None se não encontrar
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(wiki_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Procurar pela imagem principal da carta
        # Na Yugipedia, geralmente está em <div class="cardtable-cardimage">
        cardimage = soup.find('div', class_='cardtable-cardimage')
        if cardimage:
            img = cardimage.find('img')
            if img and img.get('src'):
                img_url = img['src']
                # Converter para URL absoluta se necessário
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif img_url.startswith('/'):
                    img_url = 'https://yugipedia.com' + img_url
                return img_url
        
        # Fallback: procurar qualquer imagem grande
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if 'card' in src.lower() and any(ext in src for ext in ['.jpg', '.png']):
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://yugipedia.com' + src
                return src
        
        return None
        
    except Exception as e:
        print(f"    ✗ Erro ao buscar imagem: {e}")
        return None

def update_card_images():
    """Atualiza as imagens de todas as cartas que têm URL da Yugipedia."""
    print("🖼️  TCG Collection Manager - Atualização de Imagens")
    print("=" * 60)
    
    try:
        # Buscar todas as coleções
        response = requests.get(f"{API_BASE_URL}/collections")
        response.raise_for_status()
        collections = response.json()
        
        print(f"📚 Encontradas {len(collections)} coleções")
        print("=" * 60)
        
        total_updated = 0
        total_failed = 0
        
        for collection in collections:
            col_id = collection['id']
            col_name = collection['name']
            
            print(f"\n📖 Processando: {col_name}")
            print("-" * 60)
            
            # Buscar cartas da coleção
            cards_response = requests.get(f"{API_BASE_URL}/collections/{col_id}/cards")
            cards_response.raise_for_status()
            cards = cards_response.json()
            
            for card in cards:
                # Verificar se tem URL da Yugipedia
                if not card.get('image_url'):
                    continue
                    
                wiki_url = card['image_url']
                if 'yugipedia.com' not in wiki_url:
                    continue
                
                print(f"  🔍 Buscando imagem: {card['name']}")
                print(f"     Wiki: {wiki_url}")
                
                # Buscar URL da imagem real
                image_url = get_image_url_from_yugipedia(wiki_url)
                
                if image_url:
                    # Atualizar no banco
                    try:
                        update_data = {
                            'image_url': image_url
                        }
                        update_response = requests.put(
                            f"{API_BASE_URL}/cards/{card['id']}", 
                            json=update_data
                        )
                        update_response.raise_for_status()
                        
                        print(f"     ✓ Imagem atualizada: {image_url[:60]}...")
                        total_updated += 1
                        
                    except Exception as e:
                        print(f"     ✗ Erro ao atualizar: {e}")
                        total_failed += 1
                else:
                    print(f"     ✗ Imagem não encontrada")
                    total_failed += 1
                
                # Delay para não sobrecarregar o servidor
                time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print("📊 RESUMO")
        print("=" * 60)
        print(f"✓ Imagens atualizadas: {total_updated}")
        print(f"✗ Falhas: {total_failed}")
        print("=" * 60)
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro: Servidor Flask não está rodando ou inacessível")
        print(f"  {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("\n⚠️  Este processo pode demorar vários minutos...")
    print("    Aguarde enquanto buscamos as imagens das cartas.\n")
    
    resposta = input("Deseja continuar? (s/N): ")
    if resposta.lower() == 's':
        update_card_images()
    else:
        print("❌ Operação cancelada.")
