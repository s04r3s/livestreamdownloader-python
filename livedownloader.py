import os
import subprocess
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_header():
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
    print(Fore.CYAN + header)

def download_live_stream():
    clear_screen()
    print_header()

    print(Fore.YELLOW + "+------------------------------------------------------------------------+")
    print(Fore.YELLOW + "+ Para sair do script a qualquer momento, feche a janela do prompt.      +")
    print(Fore.YELLOW + "+------------------------------------------------------------------------+")
    print()

    stream_url = input("Cole aqui seu link m3u8/flv: ")

    valid_extensions = [".m3u8", ".flv"]
    valid_link = any(ext in stream_url for ext in valid_extensions)

    if valid_link:
        print(Fore.GREEN + f"[*] {datetime.now().strftime('%H-%M-%S')} Link válido! [*]")
    else:
        print(Fore.RED + f"[*] {datetime.now().strftime('%H-%M-%S')} Link inválido! Por favor, insira um link que termine em .m3u8 ou .flv. [*]")
        input(Fore.YELLOW + "Aperte ENTER para voltar ao início do script e cole seu link novamente.")
        return

    nome = input("Digite um nome para a pasta onde ficará a live: ")

    data = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H-%M-%S")

    # Cria a pasta Lives se ela ainda não existir
    if not os.path.exists("Lives"):
        os.makedirs("Lives")

    live_folder = os.path.join("Lives", nome)
    os.makedirs(live_folder, exist_ok=True)

    output_file = os.path.join(live_folder, f"live_{nome}_{data}_{hora}.mp4")

    ffmpeg_command = [
        "ffmpeg",
        "-i", stream_url,
        "-loglevel", "info",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "copy",
        output_file
    ]

    subprocess.run(ffmpeg_command)

    # Calcula o tamanho do arquivo em bytes
    size = os.path.getsize(output_file)

    # Converte o tamanho do arquivo para MB ou GB
    size_MB = size / (1024 ** 2)
    size_GB = size / (1024 ** 3)

    print("\n--------------------")
    print(Fore.GREEN + f"[*] Live finalizada! [*]")
    print("--------------------\n")
    print(Fore.GREEN + f"[*] {hora} O arquivo foi salvo com sucesso na pasta: {nome}")
    print(Fore.GREEN + f"[*] {hora} Nome do arquivo: live_{nome}_{data}_{hora}.mp4")

    if size_GB > 0:
        print(Fore.GREEN + f"[*] {hora} Tamanho do arquivo: {size_GB:.2f} GB")
    else:
        print(Fore.GREEN + f"[*] {hora} Tamanho do arquivo: {size_MB:.2f} MB")

    print(f"-----------------------------------------------------------------------------------------")
    input(Fore.YELLOW + f"\n[*] Pressione ENTER para voltar ao início e salvar outra live. [*]")
    print(f"-----------------------------------------------------------------------------------------")
if __name__ == "__main__":
    while True:
        try:
            download_live_stream()
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro: {e}")
