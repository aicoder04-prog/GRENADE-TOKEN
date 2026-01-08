import random
import string
import json
import time
import requests
import uuid
import base64
import io
import struct
import sys
from colorama import Fore, Style, init

# Initialize Colorama for styling
init(autoreset=True)

# Crypto libraries check
try:
    from Crypto.Cipher import AES, PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
except ImportError:
    print(Fore.RED + "Error: 'pycryptodome' module not found.")
    print(Fore.YELLOW + "Run: pip install pycryptodome")
    exit()

# --- PREMIUM UI & ANIMATION ---

def nadeem_logo():
    logo = f"""
{Fore.CYAN}███╗   ██╗ █████╗ ██████╗ ███████╗███████╗███╗   ███╗
{Fore.CYAN}████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝████╗ ████║
{Fore.WHITE}██╔██╗ ██║███████║██║  ██║█████╗  █████╗  ██╔████╔██║
{Fore.WHITE}██║╚██╗██║██╔══██║██║  ██║██╔══╝  ██╔══╝  ██║╚██╔╝██║
{Fore.CYAN}██║ ╚████║██║  ██║██████╔╝███████╗███████╗██║ ╚═╝ ██║
{Fore.CYAN}╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝
{Fore.YELLOW}__________________________________________________________
{Fore.MAGENTA}          PREMIUM FACEBOOK TOOL BY NADEEM
{Fore.YELLOW}__________________________________________________________
    """
    print(logo)

def animated_print(text, color=Fore.WHITE, delay=0.03):
    """Prints text with animation and underlines it."""
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    print(color + "—" * (len(text) + 2))

# --- CORE LOGIC (NO CHANGES TO ORIGINAL FUNCTIONALITY) ---

class FacebookPasswordEncryptor:
    @staticmethod
    def get_public_key():
        try:
            url = 'https://b-graph.facebook.com/pwd_key_fetch'
            params = {
                'version': '2',
                'flow': 'CONTROLLER_INITIALIZATION',
                'method': 'GET',
                'fb_api_req_friendly_name': 'pwdKeyFetch',
                'fb_api_caller_class': 'com.facebook.auth.login.AuthOperations',
                'access_token': '438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28'
            }
            response = requests.post(url, params=params).json()
            return response.get('public_key'), str(response.get('key_id', '25'))
        except Exception as e:
            raise Exception(f"Public key fetch error: {e}")

    @staticmethod
    def encrypt(password, public_key=None, key_id="25"):
        if public_key is None:
            public_key, key_id = FacebookPasswordEncryptor.get_public_key()

        try:
            rand_key = get_random_bytes(32)
            iv = get_random_bytes(12)
            
            pubkey = RSA.import_key(public_key)
            cipher_rsa = PKCS1_v1_5.new(pubkey)
            encrypted_rand_key = cipher_rsa.encrypt(rand_key)
            
            cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
            current_time = int(time.time())
            cipher_aes.update(str(current_time).encode("utf-8"))
            encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(password.encode("utf-8"))
            
            buf = io.BytesIO()
            buf.write(bytes([1, int(key_id)]))
            buf.write(iv)
            buf.write(struct.pack("<h", len(encrypted_rand_key)))
            buf.write(encrypted_rand_key)
            buf.write(auth_tag)
            buf.write(encrypted_passwd)
            
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            # Result formatting
            return f"#PWD_FB4A:2:{current_time}:{encoded}"
        except Exception as e:
            raise Exception(f"Encryption error: {e}")

class FacebookAppTokens:
    APPS = {
        'FB_ANDROID': {'name': 'Facebook For Android', 'app_id': '350685531728'},
        'MESSENGER_ANDROID': {'name': 'Facebook Messenger For Android', 'app_id': '256002347743983'},
        'FB_LITE': {'name': 'Facebook For Lite', 'app_id': '275254692598279'},
        'MESSENGER_LITE': {'name': 'Facebook Messenger For Lite', 'app_id': '200424423651082'},
        'ADS_MANAGER_ANDROID': {'name': 'Ads Manager App For Android', 'app_id': '438142079694454'},
        'PAGES_MANAGER_ANDROID': {'name': 'Pages Manager For Android', 'app_id': '121876164619130'}
    }
    
    @staticmethod
    def get_app_id(app_key):
        app = FacebookAppTokens.APPS.get(app_key)
        return app['app_id'] if app else None
    
    @staticmethod
    def get_all_app_keys():
        return list(FacebookAppTokens.APPS.keys())

class FacebookLogin:
    def __init__(self, uid_phone_mail, password):
        self.uid_phone_mail = uid_phone_mail
        
        animated_print(f"[*] Starting process for User: {self.uid_phone_mail}", Fore.CYAN)
        
        if password.startswith("#PWD_FB4A"):
            self.password = password
            animated_print("[!] Password already encrypted.", Fore.YELLOW)
        else:
            animated_print("[*] Generating Secure Encrypted Token...", Fore.YELLOW)
            self.password = FacebookPasswordEncryptor.encrypt(password)
            
            # CONVO TOKEN IN GREEN COLOUR
            print(f"{Fore.GREEN}[SUCCESS_TOKEN]: {self.password}")
            print(Fore.GREEN + "—" * 60)

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    nadeem_logo()
    
    # User Input
    user_input = input(f"{Fore.WHITE}Enter Email/UID/Phone: ")
    pass_input = input(f"{Fore.WHITE}Enter Password: ")
    print("\n")
    
    try:
        # Running the login logic
        session = FacebookLogin(user_input, pass_input)
        animated_print("[+] All tasks completed successfully!", Fore.MAGENTA)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {e}")
