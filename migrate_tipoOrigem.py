#!/usr/bin/env python3
"""
Migração: Substituir campo is_orica por tipoOrigem

Este script:
1. Remove o campo is_orica (boolean)
2. Adiciona o campo tipoOrigem (string: 'Konami' ou 'Orica')
3. Migra dados: is_orica=0 -> tipoOrigem='Konami', is_orica=1 -> tipoOrigem='Orica'
"""

import sqlite3
import os

DB_PATH = "instance/tcg_collection.db"

def migrate():
    """Migra is_orica -> tipoOrigem"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return False
    
    print("🔄 Iniciando migração...")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar estrutura atual
        cursor.execute("PRAGMA table_info(cards)")
        columns = {column[1]: column for column in cursor.fetchall()}
        
        if 'tipoOrigem' in columns:
            print("⚠️  Campo 'tipoOrigem' já existe!")
            print("   Nenhuma alteração necessária.")
            conn.close()
            return True
        
        print("📝 Passo 1: Adicionando coluna 'tipoOrigem'...")
        cursor.execute("""
            ALTER TABLE cards 
            ADD COLUMN tipoOrigem TEXT DEFAULT 'Konami'
        """)
        
        # Se is_orica existe, migrar os dados
        if 'is_orica' in columns:
            print("📝 Passo 2: Migrando dados de is_orica para tipoOrigem...")
            cursor.execute("""
                UPDATE cards 
                SET tipoOrigem = CASE 
                    WHEN is_orica = 1 THEN 'Orica'
                    ELSE 'Konami'
                END
            """)
            
            # Contar cartas migradas
            cursor.execute("SELECT COUNT(*) FROM cards WHERE tipoOrigem = 'Konami'")
            konami_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM cards WHERE tipoOrigem = 'Orica'")
            orica_count = cursor.fetchone()[0]
            
            print(f"   ✓ Konami: {konami_count} cartas")
            print(f"   ✓ Orica: {orica_count} cartas")
            
            print("\n📝 Passo 3: Removendo coluna antiga 'is_orica'...")
            # SQLite não suporta DROP COLUMN diretamente, precisa recriar tabela
            print("   ⚠️  SQLite não suporta DROP COLUMN - coluna is_orica permanecerá no banco")
            print("   (Será ignorada pelo código)")
        
        # Commit
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migração concluída com sucesso!")
        print("\n💡 Próximos passos:")
        print("   1. Reinicie o servidor Flask")
        print("   2. A interface agora mostrará 'Konami' ou 'Orica'")
        
        conn.close()
        return True
            
    except sqlite3.Error as e:
        print(f"❌ Erro ao executar migração: {e}")
        return False

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    print("🎴 TCG Collection Manager - Migração is_orica → tipoOrigem")
    print("=" * 60)
    
    resposta = input("\n⚠️  Deseja fazer backup do banco antes? (S/n): ")
    
    if resposta.lower() != 'n':
        import shutil
        
        backup_name = f"instance/tcg_collection_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_PATH, backup_name)
        print(f"✓ Backup criado: {backup_name}")
    
    print("\n🚀 Executando migração...")
    success = migrate()
    
    if not success:
        sys.exit(1)
