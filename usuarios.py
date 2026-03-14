import requests

# ================= CONFIGURAÇÃO =================
REPO = "KnAgux/4ManageUsers"
ARQUIVO = "usuarios.json"

def baixar_usuarios():
    """
    Baixa o usuarios.json do repositório GitHub e retorna como lista de dicionários
    """
    url = f"https://raw.githubusercontent.com/{REPO}/main/{ARQUIVO}"

    r = requests.get(url)
    r.raise_for_status()  # se der erro, lança exceção

    return r.json()