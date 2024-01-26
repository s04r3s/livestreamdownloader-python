import os
from colorama import init, Fore, Style

# Inicializar colorama
init()

# Função para exibir o cabeçalho colorido
def exibir_cabecalho():
    print(Fore.CYAN + Style.BRIGHT + r"""
 _____ _____ ____  _        _ __   __                          
|  ___|  ___|  _ \| |      / \\ \ / /                          
| |_  | |_  | |_) | |     / _ \\ V /                           
|  _| |  _| |  __/| |___ / ___ \| |                            
|_|   |_|___|_|  _|_____/_/__ \_\_| ____  _____    _    __  __ 
| |   |_ _\ \   / / ____/ ___|_   _|  _ \| ____|  / \  |  \/  |
| |    | | \ \ / /|  _| \___ \ | | | |_) |  _|   / _ \ | |\/| |
| |___ | |  \ V / | |___ ___) || | |  _ <| |___ / ___ \| |  | |
|_____|___|  \_/  |_____|____/ |_| |_| \_\_____/_/   \_\_|  |_|

""" + Style.RESET_ALL)

# Função principal
def reproduzir_live():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar o console
    exibir_cabecalho()

    link = input(Fore.YELLOW + "Cole aqui seu link m3u8/flv: " + Style.RESET_ALL)

    command = f'ffplay -i "{link}" -x 315 -y 540 -volume 25 -autoexit'
    os.system(command)

    print("\n\nLive finalizada!")
    input("Pressione qualquer tecla para voltar ao início e assistir outra live.")

# Loop principal
while True:
    reproduzir_live()
