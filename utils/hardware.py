import psutil
try:
    import wmi
except:
    wmi = None

def detectar_hardware():
    if wmi:
        computador = wmi.WMI()
        cpu = computador.Win32_Processor()[0].Name
        gpu = computador.Win32_VideoController()[0].Name
    else:
        cpu = "CPU não detectada"
        gpu = "GPU não detectada"
    ram = round(psutil.virtual_memory().total / (1024**3), 2)
    return f"CPU: {cpu}\nGPU: {gpu}\nRAM: {ram} GB"