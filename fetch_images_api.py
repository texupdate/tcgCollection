#!/usr/bin/env python3
"""
Script para buscar URLs de imagens usando a API oficial do YGOPRODeck.

A API retorna diretamente as URLs das imagens das cartas!
Muito mais rápido e confiável que scraping.

API: https://db.ygoprodeck.com/api/v7/cardinfo.php
"""

import requests
import time
import sys
import urllib.parse

API_BASE_URL = "http://127.0.0.1:5000/api"
YGOPRODECK_API = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

def get_image_from_ygoprodeck_api(card_name: str) -> str:
    """
    Busca a URL da imagem usando a API do YGOPRODeck.
    
    Args:
        card_name: Nome da carta em inglês
    
    Returns:
        URL da imagem ou None se não encontrar
    """
    try:
        # Limpar o nome da carta (remover sufixos como "(as Nome Alternativo)")
        clean_name = card_name
        if ' (as ' in clean_name:
            clean_name = clean_name.split(' (as ')[0].strip()
        
        # Fazer requisição à API
        params = {'name': clean_name}
        response = requests.get(YGOPRODECK_API, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Verificar se encontrou a carta
        if 'data' in data and len(data['data']) > 0:
            card_data = data['data'][0]
            
            # Pegar a primeira imagem (artwork padrão)
            if 'card_images' in card_data and len(card_data['card_images']) > 0:
                image_url = card_data['card_images'][0]['image_url']
                return image_url
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"    ✗ Erro na API: {e}")
        return None
    except Exception as e:
        print(f"    ✗ Erro ao processar resposta: {e}")
        return None

def update_card_images():
    """Atualiza as imagens de todas as cartas."""
    print("🖼️  TCG Collection Manager - Atualização de Imagens via API")
    print("=" * 60)
    print("📡 Usando API oficial do YGOPRODeck")
    print("=" * 60)
    
    try:
        # Buscar todas as coleções
        response = requests.get(f"{API_BASE_URL}/collections")
        response.raise_for_status()
        collections = response.json()
        
        print(f"\n📚 Encontradas {len(collections)} coleções")
        print("=" * 60)
        
        total_updated = 0
        total_failed = 0
        total_skipped = 0
        request_count = 0
        start_time = time.time()
        
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
                card_name = card['name']
                
                # Verificar se já tem URL de imagem válida (não Yugipedia)
                current_url = card.get('image_url', '')
                if current_url and 'yugipedia.com' not in current_url and 'images.ygoprodeck.com' in current_url:
                    print(f"  ⏭️  Pulando: {card_name} (já tem imagem)")
                    total_skipped += 1
                    continue
                
                print(f"  🔍 Buscando: {card_name}")
                
                # Rate limiting: máximo 20 requisições por segundo
                request_count += 1
                if request_count >= 18:  # Deixar margem de segurança
                    elapsed = time.time() - start_time
                    if elapsed < 1.0:
                        sleep_time = 1.0 - elapsed
                        print(f"     ⏸️  Aguardando {sleep_time:.2f}s (rate limit)...")
                        time.sleep(sleep_time)
                    request_count = 0
                    start_time = time.time()
                
                # Buscar imagem na API
                image_url = get_image_from_ygoprodeck_api(card_name)
                
                if image_url:
                    # Atualizar no banco
                    try:
                        update_data = {'image_url': image_url}
                        update_response = requests.put(
                            f"{API_BASE_URL}/cards/{card['id']}", 
                            json=update_data
                        )
                        update_response.raise_for_status()
                        
                        print(f"     ✓ Imagem atualizada!")
                        print(f"       {image_url}")
                        total_updated += 1
                        
                    except Exception as e:
                        print(f"     ✗ Erro ao atualizar banco: {e}")
                        total_failed += 1
                else:
                    print(f"     ✗ Carta não encontrada na API")
                    print(f"       Tente: nome exato em inglês")
                    total_failed += 1
                
                # Pequeno delay entre cartas
                time.sleep(0.1)
        
        print("\n" + "=" * 60)
        print("📊 RESUMO")
        print("=" * 60)
        print(f"✓ Imagens atualizadas: {total_updated}")
        print(f"⏭️  Puladas (já tinham): {total_skipped}")
        print(f"✗ Falhas: {total_failed}")
        print("=" * 60)
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro: Servidor Flask não está rodando ou inacessível")
        print(f"  {e}")
        sys.exit(1)

def test_single_card(card_name: str):
    """Testa busca de uma única carta."""
    print(f"\n🧪 Teste: Buscando '{card_name}'")
    print("=" * 60)
    
    image_url = get_image_from_ygoprodeck_api(card_name)
    
    if image_url:
        print(f"✓ Imagem encontrada:")
        print(f"  {image_url}")
    else:
        print(f"✗ Carta não encontrada")
        print(f"  Verifique se o nome está correto (em inglês)")

if __name__ == "__main__":
    print("🎴 TCG Collection Manager - Buscador de Imagens")
    print("=" * 60)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        response.raise_for_status()
        print("✓ Servidor Flask está online")
    except requests.exceptions.RequestException:
        print("✗ Erro: Servidor Flask não está rodando!")
        print("  Execute: python app.py")
        sys.exit(1)
    
    # Modo de teste ou atualização completa
    if len(sys.argv) > 1:
        # Teste com uma carta específica
        card_name = ' '.join(sys.argv[1:])
        test_single_card(card_name)
    else:
        # Atualização completa
        print("\n⚠️  Este processo vai buscar imagens para todas as cartas.")
        print("    Taxa limite: ~18 cartas por segundo")
        print("    Tempo estimado: ~2-5 minutos para 2500 cartas\n")
        
        resposta = input("Deseja continuar? (s/N): ")
        if resposta.lower() == 's':
            update_card_images()
        else:
            print("❌ Operação cancelada.")
            print("\n💡 Para testar uma carta específica:")
            print("   python fetch_images_api.py \"Dark Magician\"")
