from colorama import init, Fore, Back, Style
import bcrypt

init(autoreset=True)

class Colors:
    RED = Style.BRIGHT + Fore.RED
    BLUE = Style.BRIGHT + Fore.BLUE
    YELLOW = Style.BRIGHT + Fore.YELLOW
    GREEN = Style.BRIGHT + Fore.GREEN

def hash_passwords(password:str)->bytes:
    enc_pass = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashedpw = bcrypt.hashpw(enc_pass, salt)
    return hashedpw

def check_pass(password:str, hashed_pw:bytes)->bool:
    enc_pass = password.encode("utf-8")
    return bcrypt.checkpw(enc_pass, hashed_pw)