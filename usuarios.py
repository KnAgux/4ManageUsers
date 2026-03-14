import requests
import os
import sys
import json

# ================= CONFIGURAÇÃO =================
REPO = "KnAgux/4ManageUsers"
ARQUIVO = "config/usuarios.json"  # Caminho relativo dentro do repositório
BRANCH = "reorganizacao-pastas"   # Branch onde o arquivo está

# ================= FUNÇÃO CAMINHO RELATIVO =================
def caminho_relativo(caminho):
    """
    Retorna o caminho correto quando rodando .exe com PyInstaller
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, caminho)

LOCAL_USUARIOS = caminho_relativo(ARQUIVO)

# ================= FUNÇÃO PARA BAIXAR DO GITHUB =================
def baixar_usuarios():
    """
    Baixa o usuarios.json do repositório GitHub.
    Se falhar, tenta ler o arquivo local.
    Retorna lista de dicionários.
    """
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{ARQUIVO}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"Erro ao baixar usuários do GitHub: {e}")
        # Tenta ler arquivo local como fallback
        try:
            with open(LOCAL_USUARIOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as ex:
            print(f"Erro ao ler arquivo local de usuários: {ex}")
            return []