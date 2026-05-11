#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migração: Adicionar campo 'notes' à tabela collections
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

def migrate():
    conn = sqlite3.connect('instance/tcg_collection.db')
    cursor = conn.cursor()
    
    try:
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(collections)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'notes' in columns:
            print("✅ Campo 'notes' já existe na tabela collections")
            return
        
        # Adicionar coluna notes
        print("📝 Adicionando campo 'notes' à tabela collections...")
        cursor.execute("ALTER TABLE collections ADD COLUMN notes TEXT DEFAULT ''")
        conn.commit()
        
        print("✅ Migração concluída com sucesso!")
        print(f"   Campo 'notes' adicionado à tabela collections")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
