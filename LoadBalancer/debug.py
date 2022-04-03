from colorama import Fore

def printWarning(text):
    print(Fore.YELLOW + text + Fore.WHITE)

def printError(text):
    print(Fore.RED + text + Fore.WHITE)

def printSuccess(text):
    print(Fore.GREEN + text + Fore.WHITE)