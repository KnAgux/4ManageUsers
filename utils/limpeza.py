import os
import shutil
import tempfile

def limpar_pasta(pasta):
    erro = False
    if not os.path.exists(pasta):
        return
    for root, dirs, files in os.walk(pasta, topdown=False):
        for name in files:
            try: os.remove(os.path.join(root, name))
            except: erro = True
        for name in dirs:
            try: shutil.rmtree(os.path.join(root, name), ignore_errors=True)
            except: erro = True
    return not erro

def limpar_temp(): limpar_pasta(tempfile.gettempdir())
def limpar_windows_temp(): limpar_pasta(os.path.expanduser(r"~\AppData\Local\Temp"))
def limpar_prefetch(): limpar_pasta(r"C:\Windows\Prefetch")
def limpar_recent(): limpar_pasta(os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Recent"))
def limpar_crash(): limpar_pasta(os.path.expanduser(r"~\AppData\Local\CrashDumps"))
def limpar_shader():
    limpar_pasta(os.path.expanduser(r"~\AppData\Local\NVIDIA\DXCache"))
    limpar_pasta(os.path.expanduser(r"~\AppData\Local\AMD\DXCache"))
def limpar_directx(): limpar_pasta(os.path.expanduser(r"~\AppData\Local\D3DSCache"))
def limpar_logs(): limpar_pasta(r"C:\Windows\Logs")
def limpar_windows_update(): limpar_pasta(r"C:\Windows\SoftwareDistribution\Download")
def limpar_fivem_cache(fivem_path): limpar_pasta(os.path.join(fivem_path,"data","cache"))
def limpar_lixeira(): os.system("powershell.exe Clear-RecycleBin -Confirm:$false")
def limpar_downloads(): limpar_pasta(os.path.expanduser(r"~\Downloads"))