#!/usr/bin/env python3
"""Script para limpar todas as coleções via API."""

import requests
import sys

API_BASE_URL = "http://127.0.0.1:5000/api"

def clear_via_api():
    """Remove todas as coleções via API."""
    try:
        # Buscar todas as coleções
        response = requests.get(f"{API_BASE_URL}/collections")
        response.raise_for_status()
        collections = response.json()
        
        print(f"📊 Encontradas {len(collections)} coleções")
        print("=" * 60)
        
        # Deletar cada coleção
        for collection in collections:
            col_id = collection['id']
            col_name = collection['name']
            
            try:
                delete_response = requests.delete(f"{API_BASE_URL}/collections/{col_id}")
                delete_response.raise_for_status()
                print(f"✓ Coleção deletada: {col_name} (ID: {col_id})")
            except Exception as e:
                print(f"✗ Erro ao deletar {col_name}: {e}")
        
        print("=" * 60)
        print("✓ Limpeza concluída!")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro: Servidor Flask não está rodando ou inacessível")
        print(f"  {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🗑️  TCG Collection Manager - Limpeza via API")
    print("=" * 60)
    resposta = input("⚠️  ATENÇÃO: Isso vai DELETAR TODAS as coleções e cartas! Confirma? (s/N): ")
    if resposta.lower() == 's':
        clear_via_api()
    else:
        print("❌ Operação cancelada.")
