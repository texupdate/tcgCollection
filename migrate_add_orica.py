#!/usr/bin/env python3
"""
Migração: Adicionar campo is_orica à tabela cards

Este script adiciona o campo 'is_orica' (Boolean) à tabela de cartas
para diferenciar cartas originais de Oricas (custom/réplica).
"""

import sqlite3
import os

DB_PATH = "instance/tcg_collection.db"

def migrate():
    """Adiciona o campo is_orica à tabela cards"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return False
    
    print("🔄 Iniciando migração...")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(cards)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_orica' in columns:
            print("⚠️  Campo 'is_orica' já existe no banco!")
            print("   Nenhuma alteração necessária.")
            conn.close()
            return True
        
        # Adicionar a nova coluna
        print("📝 Adicionando coluna 'is_orica' à tabela 'cards'...")
        cursor.execute("""
            ALTER TABLE cards 
            ADD COLUMN is_orica BOOLEAN DEFAULT 0
        """)
        
        # Commit das mudanças
        conn.commit()
        
        # Verificar se foi adicionada
        cursor.execute("PRAGMA table_info(cards)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_orica' in columns:
            print("✓ Coluna 'is_orica' adicionada com sucesso!")
            print("\n📊 Estatísticas:")
            
            # Contar total de cartas
            cursor.execute("SELECT COUNT(*) FROM cards")
            total = cursor.fetchone()[0]
            print(f"   Total de cartas: {total}")
            print(f"   Todas marcadas como: Original (is_orica = False)")
            
            print("\n" + "=" * 60)
            print("✅ Migração concluída com sucesso!")
            print("\n💡 Próximos passos:")
            print("   1. Reinicie o servidor Flask")
            print("   2. Use a interface web para marcar cartas como Orica")
            print("   3. Ou atualize via API: PUT /api/cards/{id} {'is_orica': true}")
            
            conn.close()
            return True
        else:
            print("❌ Erro: Coluna não foi adicionada")
            conn.close()
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Erro ao executar migração: {e}")
        return False

def rollback():
    """Remove o campo is_orica (não suportado diretamente no SQLite)"""
    print("⚠️  SQLite não suporta DROP COLUMN diretamente.")
    print("   Para reverter, você precisaria:")
    print("   1. Criar nova tabela sem a coluna")
    print("   2. Copiar todos os dados")
    print("   3. Deletar tabela antiga")
    print("   4. Renomear nova tabela")
    print("\n   Ou simplesmente restaurar o backup do banco de dados.")

if __name__ == "__main__":
    import sys
    
    print("🎴 TCG Collection Manager - Migração de Banco")
    print("=" * 60)
    print("📋 Operação: Adicionar campo 'is_orica' (Original vs Orica)")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback()
    else:
        resposta = input("\n⚠️  Deseja fazer backup do banco antes? (S/n): ")
        
        if resposta.lower() != 'n':
            import shutil
            from datetime import datetime
            
            backup_name = f"instance/tcg_collection_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(DB_PATH, backup_name)
            print(f"✓ Backup criado: {backup_name}")
        
        print("\n🚀 Executando migração...")
        success = migrate()
        
        if not success:
            sys.exit(1)
