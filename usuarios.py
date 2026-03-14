import requests
import json
import os
import sys

# Configurações
REPO = "KnAgux/4ManageUsers"
ARQUIVO = "config/usuarios.json"
BRANCH = "reorganizacao-pastas"


def baixar_usuarios():
    """
    Tenta baixar usuarios.json do GitHub.
    Se falhar, lê o arquivo local.
    Retorna lista de usuários.
    """
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{ARQUIVO}"

    # Primeiro: tentar baixar do GitHub
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erro ao baixar usuários do GitHub: {e}")

    # Fallback: usar arquivo local
    try:
        if getattr(sys, 'frozen', False):  # se for .exe
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        caminho_local = os.path.join(base_path, ARQUIVO)
        if os.path.exists(caminho_local):
            with open(caminho_local, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao ler arquivo local: {e}")

    # Se tudo falhar, retorna lista vazia
    return []