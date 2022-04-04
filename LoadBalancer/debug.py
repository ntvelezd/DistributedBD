from colorama import Fore

def printWarning(text):
    print(Fore.LIGHTRED_EX+ text + Fore.WHITE)

def printError(text):
    print(Fore.RED + text + Fore.WHITE)

def printSuccess(text):
    print(Fore.YELLOW + text + Fore.WHITE)