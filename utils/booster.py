import os

def booster_fps():
    os.system("powercfg -setactive SCHEME_MIN")
    os.system("ipconfig /flushdns")

def limpar_registro():
    os.system("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU /f")

def limpar_event_logs():
    os.system('for /F "tokens=*" %1 in (\'wevtutil.exe el\') DO wevtutil.exe cl "%1"')

def limpar_journal():
    os.system("fsutil usn deletejournal /D C:")

def limpar_shadow():
    os.system("vssadmin delete shadows /all /quiet")