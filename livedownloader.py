import os
import subprocess
from datetime import datetime
from colorama import init, Fore, Style
import threading
import sys
import time
import ctypes

# Configuração para permitir caracteres acentuados no console
init(autoreset=True)
os.system("chcp 65001")  # Define o código de página para UTF-8

def set_console_title(title):
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except Exception as e:
            print(f"Erro ao definir o título da janela: {e}")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_header():
    python_version = sys.version.split(' ')[0]
    title = f'"Python {python_version} | Livestream Downloader by S0ar3s"'
    set_console_title(title)
    header = r"""
     _     _                _                            
    | |   (_)_   _____  ___| |_ _ __ ___  __ _ _ __ ___  
    | |   | \ \ / / _ \/ __| __| '__/ _ \/ _` | '_ ` _ \ 
    | |___| |\ V /  __/\__ \ |_| | |  __/ (_| | | | | | |
    |_____|_| \_/ \___||___/\__|_|  \___|\__,_|_| |_| |_|    
    |  _ \  _____      _| | ___   __ _  __| | ___ _ __   
    | | | |/ _ \ \ /\ / / |/ _ \ / _` |/ _` |/ _ \ '__|  
    | |_| | (_) \ V  V /| | (_) | (_| | (_| |  __/ |     
    |____/ \___/ \_/\_/ |_|\___/ \__,_|\__,_|\___|_|     
    """
    print(Style.BRIGHT + Fore.LIGHTWHITE_EX + header)

def run_ffmpeg(ffmpeg_command):
    subprocess.run(ffmpeg_command)

def download_live_stream():
    clear_screen()
    print_header()

    print(Fore.YELLOW + "+------------------------------------------------------------------------+")
    print(Fore.YELLOW + "+ Para sair do script a qualquer momento, feche a janela do prompt.      +")
    print(Fore.YELLOW + "+------------------------------------------------------------------------+")
    print()

    # Permitir entrada de caracteres acentuados
    stream_url = input("Cole aqui seu link m3u8/flv: ").encode('utf-8').decode('cp65001')

    valid_extensions = [".m3u8", ".flv"]
    valid_link = any(ext in stream_url for ext in valid_extensions)

    if valid_link:
        print(Fore.GREEN + f"[ * ] {datetime.now().strftime('%d/%m/%Y %H:%M')} Link válido! [ * ]")
    else:
        print(Fore.RED + f"[ * ] {datetime.now().strftime('%d/%m/%Y %H:%M')} Link inválido! Por favor, insira um link que termine em .m3u8 ou .flv. [ * ]")
        input(Fore.YELLOW + "Aperte ENTER para voltar ao início do script e cole seu link novamente.")
        return

    nome = input("Digite um nome para a pasta onde ficará a live: ").encode('utf-8').decode('cp65001')

    # Obtenha o horário de início
    hora_inicio = datetime.now()

    if not os.path.exists("Lives"):
        os.makedirs("Lives")

    live_folder = os.path.join("Lives", nome)
    os.makedirs(live_folder, exist_ok=True)

    data = hora_inicio.strftime("%d-%m-%Y")
    hora = hora_inicio.strftime("%H-%M")

    # Substitua as barras por hífens no nome do arquivo
    output_file = os.path.join(live_folder, f"live_{data}_{hora}_{nome.replace('/', '-')}.mp4")

    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-loglevel", "warning",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "copy",
        "-reconnect", "1",
        output_file
    ]

    print(Fore.GREEN + f"[*] {hora} O download da live foi iniciado!")

    download_thread = threading.Thread(target=run_ffmpeg, args=(ffmpeg_command,))
    download_thread.start()

    download_text = "Download iniciado, aguarde..."
    while download_thread.is_alive():
        for _ in range(3):
            print(download_text, end='', flush=True)
            time.sleep(1)
            print('\b' * len(download_text), end='', flush=True)

    hora_termino = datetime.now()

    size = os.path.getsize(output_file)
    size_MB = size / (1024 ** 2)
    size_GB = size / (1024 ** 3)

    print("\n--------------------")
    print(Fore.GREEN + f" Live finalizada!")
    print("--------------------\n")
    print(Fore.GREEN + f"[ * ] {hora} - {hora_termino.strftime('%d/%m/%Y %H:%M')} O arquivo foi salvo com sucesso na pasta: {nome}")
    print(Fore.GREEN + f"[ * ] {hora} - {hora_termino.strftime('%d/%m/%Y %H:%M')} Nome do arquivo: live_{data}_{hora}_{nome.replace('/', '-')}.mp4")

    if size_GB > 0:
        print(Fore.GREEN + f"[ * ] {hora} - {hora_termino.strftime('%d/%m/%Y %H:%M')} Tamanho do arquivo: {size_GB:.2f} GB")
    else:
        print(Fore.GREEN + f"[ * ] {hora} - {hora_termino.strftime('%d/%m/%Y %H:%M')} Tamanho do arquivo: {size_MB:.2f} MB")

    print("\n-----------------------------------------------------------------------------------------")
    input(Fore.YELLOW + f"\nPressione ENTER para voltar ao início e salvar outra live.")
    print("-----------------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    while True:
        try:
            download_live_stream()
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro: {e}")
            input("Pressione ENTER para encerrar o script.")
