import os
import sys
import json
import customtkinter as ctk
from utils import limpeza, hardware, booster
import requests

# ================= CONFIGURAÇÕES =================
ctk.set_appearance_mode("dark")
AZUL = "#2da8ff"
tentativas = 0
deep_aberto = False
fivem = os.path.expanduser(r"~\AppData\Local\FiveM\FiveM.app")

# ================= FUNÇÃO CAMINHO RELATIVO =================
def caminho_relativo(caminho):
    """Retorna o caminho correto quando rodando .exe com PyInstaller"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, caminho)

USUARIOS_JSON = caminho_relativo("config/usuarios.json")

# ================= FUNÇÃO BAIXAR USUÁRIOS GITHUB =================
REPO = "KnAgux/4ManageUsers"

def baixar_usuarios_github():
    url = f"https://raw.githubusercontent.com/{REPO}/main/usuarios.json"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erro ao baixar usuários do GitHub: {e}")
        return []

# ================= LOGIN =================
def login():
    global tentativas
    tela = ctk.CTk()
    tela.geometry("350x220")
    tela.title("4Manage Login")

    def verificar():
        global tentativas
        usuario_input = usuario.get()
        senha_input = senha.get()

        # Primeiro tenta GitHub, depois arquivo local
        lista_usuarios = baixar_usuarios_github()
        if not lista_usuarios:
            try:
                with open(USUARIOS_JSON, "r", encoding="utf-8") as f:
                    lista_usuarios = json.load(f)
            except Exception as e:
                print(f"Erro ao ler arquivo local: {e}")
                lista_usuarios = []

        valido = any(u["usuario"] == usuario_input and u["senha"] == senha_input for u in lista_usuarios)

        if valido:
            tela.destroy()
        else:
            tentativas += 1
            erro.configure(
                text="ACESSO NEGADO",
                text_color="red",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            if tentativas >= 3:
                tela.destroy()
                sys.exit()

    ctk.CTkLabel(tela, text="4Manage", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=5)
    usuario = ctk.CTkEntry(tela, placeholder_text="Email/Usuário", width=200)
    usuario.pack(pady=5)
    senha = ctk.CTkEntry(tela, show="*", width=200, placeholder_text="Senha")
    senha.pack(pady=5)
    ctk.CTkButton(tela, text="Entrar", command=verificar).pack(pady=10)
    erro = ctk.CTkLabel(tela, text="")
    erro.pack()
    tela.protocol("WM_DELETE_WINDOW", sys.exit)
    tela.mainloop()

login()

# ================= FUNÇÃO DE LOG =================
def log(msg):
    log_box.insert("end", msg + "\n")
    log_box.see("end")

# ================= FUNÇÃO ATUALIZAR HARDWARE =================
def atualizar():
    info.configure(text=hardware.detectar_hardware())
    janela.after(1000, atualizar)

# ================= INTERFACE PRINCIPAL =================
janela = ctk.CTk()
janela.geometry("960x540")
janela.title("4Manage")

tabs = ctk.CTkTabview(janela)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

tabs.add("Dashboard")
tabs.add("Limpeza")
tabs.add("Privado")

aba_home = tabs.tab("Dashboard")
aba_limpeza = tabs.tab("Limpeza")
aba_privado = tabs.tab("Privado")

# --- Dashboard ---
titulo = ctk.CTkLabel(aba_home, text="4MANAGE", font=ctk.CTkFont(size=32, weight="bold"))
titulo.pack(pady=20)

info = ctk.CTkLabel(aba_home, text="Detectando hardware...")
info.pack()

log_box = ctk.CTkTextbox(aba_home, width=500, height=150)
log_box.pack(pady=10)

progress = ctk.CTkProgressBar(aba_home, width=400)
progress.pack(pady=10)
progress.set(0)

ctk.CTkButton(
    aba_home,
    text="Limpeza Completa",
    fg_color=AZUL,
    command=lambda: iniciar_limpeza()
).pack(pady=10)

# --- Funções de Limpeza ---
def iniciar_limpeza():
    progress.set(0)
    tarefas = [
        limpeza.limpar_temp,
        limpeza.limpar_windows_temp,
        limpeza.limpar_prefetch,
        limpeza.limpar_recent,
        limpeza.limpar_crash,
        limpeza.limpar_shader,
        limpeza.limpar_directx,
        limpeza.limpar_logs,
        limpeza.limpar_windows_update,
        lambda: limpeza.limpar_fivem_cache(fivem)
    ]
    total = len(tarefas)
    for i, tarefa in enumerate(tarefas):
        try:
            tarefa()
        except Exception as e:
            log(f"Erro na tarefa {tarefa.__name__ if hasattr(tarefa,'__name__') else str(tarefa)}: {e}")
        progress.set((i+1)/total)
    log("Limpeza completa")

# --- Deep Clean (Ctrl+Shift+D) ---
def abrir_deep(event=None):
    global deep_aberto
    if not deep_aberto:
        tabs.add("Deep Clean")
        aba_deep = tabs.tab("Deep Clean")
        ctk.CTkLabel(aba_deep, text="DEEP SYSTEM CLEAN", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)
        ctk.CTkButton(aba_deep, text="Limpar Registro", command=booster.limpar_registro).pack(pady=8)
        ctk.CTkButton(aba_deep, text="Limpar Event Logs", command=booster.limpar_event_logs).pack(pady=8)
        ctk.CTkButton(aba_deep, text="Limpar JournalTrace", command=booster.limpar_journal).pack(pady=8)
        ctk.CTkButton(aba_deep, text="Limpar Shadow Cache", command=booster.limpar_shadow).pack(pady=8)
        tabs.set("Deep Clean")
        deep_aberto = True
    else:
        tabs.delete("Deep Clean")
        deep_aberto = False

janela.bind("<Control-Shift-D>", abrir_deep)

# --- Limpeza separada ---
frame_esq = ctk.CTkFrame(aba_limpeza)
frame_esq.pack(side="left", expand=True, padx=40, pady=20)
frame_dir = ctk.CTkFrame(aba_limpeza)
frame_dir.pack(side="right", expand=True, padx=40, pady=20)

def botao(frame, texto, cmd):
    ctk.CTkButton(frame, text=texto, width=180, height=40, fg_color=AZUL, command=cmd).pack(pady=8)

# Esquerda
botao(frame_esq, "Temp", limpeza.limpar_temp)
botao(frame_esq, "Windows Temp", limpeza.limpar_windows_temp)
botao(frame_esq, "Prefetch", limpeza.limpar_prefetch)
botao(frame_esq, "Recent", limpeza.limpar_recent)
botao(frame_esq, "Crash Dumps", limpeza.limpar_crash)
botao(frame_esq, "Lixeira", limpeza.limpar_lixeira)
botao(frame_esq, "Downloads", limpeza.limpar_downloads)

# Direita
botao(frame_dir, "Shader Cache", limpeza.limpar_shader)
botao(frame_dir, "DirectX Cache", limpeza.limpar_directx)
botao(frame_dir, "Logs Windows", limpeza.limpar_logs)
botao(frame_dir, "Windows Update", limpeza.limpar_windows_update)
botao(frame_dir, "FiveM Cache", lambda: limpeza.limpar_fivem_cache(fivem))

# --- Privado ---
painel_privado = ctk.CTkFrame(aba_privado)

def verificar_privado():
    if senha_priv.get() == "Booster4Manage":
        login_priv.pack_forget()
        painel_privado.pack(pady=20)

login_priv = ctk.CTkFrame(aba_privado)
login_priv.pack(pady=40)
senha_priv = ctk.CTkEntry(login_priv, show="*")
senha_priv.pack(pady=10)
ctk.CTkButton(login_priv, text="Entrar", command=verificar_privado).pack()

ctk.CTkButton(
    painel_privado,
    text="Booster FPS FiveM",
    fg_color="#00ff9c",
    command=booster.booster_fps
).pack(pady=10)

# Atualizar hardware
janela.after(1000, atualizar)
janela.protocol("WM_DELETE_WINDOW", sys.exit)
janela.mainloop()