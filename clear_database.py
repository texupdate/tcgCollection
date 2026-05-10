#!/usr/bin/env python3
"""Script para limpar o banco de dados."""

import os
import sys

# Caminho do banco
DB_PATH = "instance/tcg_collection.db"

def clear_database():
    """Remove o banco de dados para recriá-lo do zero."""
    if os.path.exists(DB_PATH):
        print(f"🗑️  Removendo banco de dados: {DB_PATH}")
        os.remove(DB_PATH)
        print("✓ Banco removido com sucesso!")
        print("\n💡 Reinicie o servidor Flask para criar um banco limpo.")
        print("   python app.py")
    else:
        print(f"⚠️  Banco não encontrado: {DB_PATH}")

if __name__ == "__main__":
    resposta = input("⚠️  ATENÇÃO: Isso vai DELETAR TODAS as coleções e cartas! Confirma? (s/N): ")
    if resposta.lower() == 's':
        clear_database()
    else:
        print("❌ Operação cancelada.")
