#!/usr/bin/env python3
"""
Script para importar cartas em massa de um arquivo CSV para o TCG Collection Manager.

Formato do CSV (com cabeçalho):
collection_name,card_number,card_name,image_url,rarity,quantity

Exemplo:
Pokémon Base Set,1,Alakazam,https://example.com/alakazam.jpg,Rare,2
Pokémon Base Set,2,Blastoise,https://example.com/blastoise.jpg,Rare,1
Yu-Gi-Oh LOB,1,Blue-Eyes White Dragon,https://example.com/bewd.jpg,Ultra Rare,0
"""

import csv
import requests
import sys
from typing import Dict, List

# Configuração da API
API_BASE_URL = "http://127.0.0.1:5000/api"

class TCGImporter:
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url
        self.collections_cache: Dict[str, int] = {}
        self.stats = {
            'collections_created': 0,
            'cards_added': 0,
            'errors': 0
        }
    
    def get_or_create_collection(self, collection_name: str, total_cards: int = 0) -> int:
        """Obtém o ID de uma coleção existente ou cria uma nova."""
        
        # Verifica se já está no cache
        if collection_name in self.collections_cache:
            return self.collections_cache[collection_name]
        
        # Busca coleções existentes
        try:
            response = requests.get(f"{self.api_url}/collections")
            response.raise_for_status()
            collections = response.json()
            
            for collection in collections:
                if collection['name'] == collection_name:
                    self.collections_cache[collection_name] = collection['id']
                    print(f"✓ Coleção '{collection_name}' já existe (ID: {collection['id']})")
                    return collection['id']
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao buscar coleções: {e}")
            self.stats['errors'] += 1
            return None
        
        # Cria nova coleção
        try:
            data = {
                'name': collection_name,
                'description': f'Importado via CSV',
                'total_cards': total_cards
            }
            response = requests.post(f"{self.api_url}/collections", json=data)
            response.raise_for_status()
            collection = response.json()
            
            self.collections_cache[collection_name] = collection['id']
            self.stats['collections_created'] += 1
            print(f"✓ Coleção '{collection_name}' criada (ID: {collection['id']})")
            return collection['id']
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao criar coleção '{collection_name}': {e}")
            self.stats['errors'] += 1
            return None
    
    def add_card(self, collection_id: int, card_data: dict) -> bool:
        """Adiciona uma carta à coleção."""
        try:
            card_data['collection_id'] = collection_id
            response = requests.post(f"{self.api_url}/cards", json=card_data)
            response.raise_for_status()
            self.stats['cards_added'] += 1
            return True
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            try:
                if response.status_code == 500:
                    print(f"✗ Erro ao adicionar carta #{card_data['collection_number']} - {card_data['name']}: Número duplicado?")
                else:
                    print(f"✗ Erro ao adicionar carta #{card_data['collection_number']} - {card_data['name']}: {error_msg}")
            except:
                print(f"✗ Erro ao adicionar carta #{card_data['collection_number']} - {card_data['name']}: {error_msg}")
            self.stats['errors'] += 1
            return False
    
    def import_from_csv(self, csv_file: str, encoding: str = 'utf-8-sig'):
        """Importa cartas de um arquivo CSV."""
        print(f"\n📁 Lendo arquivo: {csv_file}")
        print("=" * 60)
        
        try:
            # Tentar diferentes encodings
            encodings_to_try = [encoding, 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            success = False
            
            for enc in encodings_to_try:
                try:
                    with open(csv_file, 'r', encoding=enc) as file:
                        # Detectar delimitador automaticamente
                        sample = file.read(1024)
                        file.seek(0)
                        delimiter = ';' if sample.count(';') > sample.count(',') else ','
                        reader = csv.DictReader(file, delimiter=delimiter)
                        
                        # Validar cabeçalhos (aceitar variações)
                        fieldnames = [f.strip().lower() for f in reader.fieldnames]
                        
                        # Mapear variações de nomes de colunas
                        field_mapping = {}
                        for original in reader.fieldnames:
                            lower = original.strip().lower()
                            if 'collection' in lower and 'name' in lower:
                                field_mapping['collection_name'] = original
                            elif lower in ['card_number', 'r_numr', 'number', 'num']:
                                field_mapping['card_number'] = original
                            elif 'card' in lower and 'name' in lower:
                                field_mapping['card_name'] = original
                        
                        required_fields = ['collection_name', 'card_number', 'card_name']
                        if not all(field in field_mapping for field in required_fields):
                            print(f"✗ Erro: O CSV deve ter campos equivalentes a: {', '.join(required_fields)}")
                            print(f"  Campos encontrados: {', '.join(reader.fieldnames)}")
                            return
                        
                        # Agrupar por coleção para calcular total_cards
                        collections_data = {}
                        rows = list(reader)
                        
                        print(f"✓ Arquivo lido com encoding: {enc}, delimitador: '{delimiter}'")
                        
                        for row in rows:
                            col_name = row[field_mapping['collection_name']].strip()
                            if col_name not in collections_data:
                                collections_data[col_name] = []
                            collections_data[col_name].append(row)
                    
                    # Processar cada coleção
                    for collection_name, cards in collections_data.items():
                        print(f"\n📚 Processando coleção: {collection_name}")
                        print("-" * 60)
                        
                        # Calcular total de cartas da coleção
                        max_card_number = max(int(card[field_mapping['card_number']]) for card in cards)
                        
                        # Criar ou obter coleção
                        collection_id = self.get_or_create_collection(collection_name, max_card_number)
                        if not collection_id:
                            print(f"⚠️  Pulando coleção '{collection_name}' devido a erro")
                            continue
                        
                        # Adicionar cartas
                        for row in cards:
                            card_data = {
                                'collection_number': int(row[field_mapping['card_number']]),
                                'name': row[field_mapping['card_name']].strip(),
                                'image_url': row.get('image_url', '').strip() or None,
                                'rarity': row.get('rarity', '').strip() or None,
                                'quantity': int(row.get('quantity', 0)) if row.get('quantity', '').strip() else 0,
                                'set_name': row.get('set_name', '').strip() or None,
                                'card_number': row.get('set_card_number', '').strip() or None,
                                'condition': row.get('condition', '').strip() or None,
                                'language': row.get('language', 'Português').strip() if row.get('language', '').strip() else 'Português',
                                'notes': row.get('notes', '').strip() or None
                            }
                            
                            if self.add_card(collection_id, card_data):
                                print(f"  ✓ Carta #{card_data['collection_number']:03d} - {card_data['name']}")
                    
                    # Sucesso - sair do loop de encodings
                    success = True
                    break
                        
                except UnicodeDecodeError:
                    if enc == encodings_to_try[-1]:
                        print(f"✗ Erro: Não foi possível ler o arquivo com nenhum encoding testado")
                        self.stats['errors'] += 1
                        return
                    continue
            
            if not success:
                print(f"✗ Erro ao processar arquivo")
                self.stats['errors'] += 1
                
        except FileNotFoundError:
            print(f"✗ Erro: Arquivo '{csv_file}' não encontrado")
            self.stats['errors'] += 1
        except Exception as e:
            print(f"✗ Erro ao processar CSV: {e}")
            self.stats['errors'] += 1
        
        # Estatísticas finais
        print("\n" + "=" * 60)
        print("📊 RESUMO DA IMPORTAÇÃO")
        print("=" * 60)
        print(f"✓ Coleções criadas: {self.stats['collections_created']}")
        print(f"✓ Cartas adicionadas: {self.stats['cards_added']}")
        print(f"✗ Erros: {self.stats['errors']}")
        print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Uso: python import_cards.py <arquivo.csv>")
        print("\nFormato do CSV:")
        print("collection_name,card_number,card_name,image_url,rarity,quantity")
        print("\nCampos obrigatórios:")
        print("  - collection_name: Nome da coleção")
        print("  - card_number: Número da carta na coleção (1, 2, 3...)")
        print("  - card_name: Nome da carta")
        print("\nCampos opcionais:")
        print("  - image_url: URL da imagem da carta")
        print("  - rarity: Raridade (Common, Rare, etc)")
        print("  - quantity: Quantidade inicial (padrão: 0)")
        print("  - set_name: Nome do set/expansão")
        print("  - set_card_number: Número da carta no set oficial")
        print("  - condition: Condição (Mint, Near Mint, etc)")
        print("  - language: Idioma (padrão: Português)")
        print("  - notes: Observações")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    print("🎴 TCG Collection Manager - Importador CSV")
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
    
    # Iniciar importação
    importer = TCGImporter()
    importer.import_from_csv(csv_file)


if __name__ == "__main__":
    main()
