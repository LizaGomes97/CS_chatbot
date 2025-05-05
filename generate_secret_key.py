#!/usr/bin/env python
"""
Utilitário para gerar uma SECRET_KEY Django segura.
Execute este script para gerar uma nova chave secreta que você pode usar no arquivo .env.
"""

import random
import string

# Caracteres que podem fazer parte da SECRET_KEY
chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'

# Gerar SECRET_KEY de 50 caracteres
SECRET_KEY = ''.join(random.choice(chars) for _ in range(50))

print('Copie a chave abaixo e adicione ao seu arquivo .env:')
print(f"SECRET_KEY={SECRET_KEY}")

# Opcionalmente, tentar atualizar o arquivo .env
try:
    import os
    from dotenv import load_dotenv, set_key
    
    # Verificar se .env existe
    if os.path.exists('.env'):
        load_dotenv()
        
        print("\nDeseja atualizar automaticamente seu arquivo .env? (s/n)")
        choice = input().lower()
        
        if choice == 's' or choice == 'sim':
            set_key('.env', 'SECRET_KEY', SECRET_KEY)
            print("Arquivo .env atualizado com sucesso!")
        else:
            print("O arquivo .env não foi modificado.")
    else:
        print("\nO arquivo .env não foi encontrado no diretório atual.")
        print("Se quiser criar um arquivo .env, execute:")
        print("echo SECRET_KEY=", SECRET_KEY, "> .env")
except ImportError:
    # python-dotenv pode não estar instalado
    pass