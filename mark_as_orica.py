#!/usr/bin/env python3
"""
Script para marcar cartas como Orica (custom/réplica).

Uso:
  python mark_as_orica.py <collection_name> <card_numbers>
  
Exemplos:
  python mark_as_orica.py "AST" 1,5,10-15,20
  python mark_as_orica.py "LOB" 1-10
"""

import requests
import sys

API_BASE_URL = "http://127.0.0.1:5000/api"

def parse_card_numbers(numbers_str):
    """
    Parse string de números (ex: "1,5,10-15,20") para lista.
    
    Retorna: [1, 5, 10, 11, 12, 13, 14, 15, 20]
    """
    numbers = []
    parts = numbers_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range: 10-15
            start, end = part.split('-')
            numbers.extend(range(int(start), int(end) + 1))
        else:
            # Número único
            numbers.append(int(part))
    
    return sorted(set(numbers))

def get_collection_by_name(name):
    """Busca coleção por nome."""
    try:
        response = requests.get(f"{API_BASE_URL}/collections")
        response.raise_for_status()
        collections = response.json()
        
        for col in collections:
            if col['name'].lower() == name.lower():
                return col
        
        return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro ao buscar coleções: {e}")
        return None

def mark_cards_as_orica(collection_id, card_numbers, is_orica=True):
    """Marca cartas específicas como Orica ou Original."""
    try:
        # Buscar todas as cartas da coleção
        response = requests.get(f"{API_BASE_URL}/collections/{collection_id}/cards")
        response.raise_for_status()
        cards = response.json()
        
        updated = 0
        failed = 0
        
        for card in cards:
            if card['collection_number'] in card_numbers:
                # Atualizar o card
                try:
                    update_response = requests.put(
                        f"{API_BASE_URL}/cards/{card['id']}",
                        json={'is_orica': is_orica}
                    )
                    update_response.raise_for_status()
                    
                    status = "ORICA 🎨" if is_orica else "Original ✨"
                    print(f"  ✓ Carta #{card['collection_number']:03d} {card['name']} → {status}")
                    updated += 1
                    
                except Exception as e:
                    print(f"  ✗ Erro na carta #{card['collection_number']:03d}: {e}")
                    failed += 1
        
        return updated, failed
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro ao buscar cartas: {e}")
        return 0, 0

def main():
    if len(sys.argv) < 3:
        print("Uso: python mark_as_orica.py <collection_name> <card_numbers> [--original]")
        print("\nExemplos:")
        print("  python mark_as_orica.py \"AST\" 1,5,10-15,20")
        print("  python mark_as_orica.py \"LOB\" 1-10")
        print("  python mark_as_orica.py \"AST\" 5,10 --original  (marca como original)")
        sys.exit(1)
    
    collection_name = sys.argv[1]
    card_numbers_str = sys.argv[2]
    is_orica = '--original' not in sys.argv
    
    print("🎴 TCG Collection Manager - Marcador de Oricas")
    print("=" * 60)
    
    # Verificar servidor
    try:
        requests.get(f"{API_BASE_URL}/stats")
    except:
        print("✗ Erro: Servidor Flask não está rodando!")
        print("  Execute: python app.py")
        sys.exit(1)
    
    # Buscar coleção
    print(f"🔍 Buscando coleção: {collection_name}")
    collection = get_collection_by_name(collection_name)
    
    if not collection:
        print(f"✗ Coleção '{collection_name}' não encontrada!")
        sys.exit(1)
    
    print(f"✓ Coleção encontrada: {collection['name']} (ID: {collection['id']})")
    
    # Parse números das cartas
    try:
        card_numbers = parse_card_numbers(card_numbers_str)
        print(f"\n📝 Números das cartas: {card_numbers}")
        print(f"   Total: {len(card_numbers)} cartas")
    except Exception as e:
        print(f"✗ Erro ao processar números: {e}")
        sys.exit(1)
    
    # Confirmar
    action = "ORICA 🎨" if is_orica else "ORIGINAL ✨"
    print(f"\n⚠️  Marcar {len(card_numbers)} cartas como {action}?")
    resposta = input("Digite 's' para confirmar: ")
    
    if resposta.lower() != 's':
        print("❌ Operação cancelada")
        sys.exit(0)
    
    # Executar
    print(f"\n🚀 Atualizando cartas...")
    print("-" * 60)
    
    updated, failed = mark_cards_as_orica(collection['id'], card_numbers, is_orica)
    
    print("-" * 60)
    print(f"\n📊 RESUMO:")
    print(f"  ✓ Atualizadas: {updated}")
    print(f"  ✗ Falhas: {failed}")
    print("\n✅ Concluído! Recarregue a página do navegador para ver as mudanças.")

if __name__ == "__main__":
    main()
