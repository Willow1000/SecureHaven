# Importing necessary libraries
import os 
import shutil
import subprocess
import json
import pyzipper
import requests
import random as rd
import re
import getpass as pa
from time import sleep
import pyperclip
from getpass import getpass
from datetime import datetime
import platform
from pathlib import Path
from nacl.secret import SecretBox
from nacl.pwhash import argon2id
from nacl.utils import random


FOLDER_NAME = 'production'

if os.path.exists(FOLDER_NAME):
    os.chdir(FOLDER_NAME)
else:
    os.mkdir(FOLDER_NAME)
    os.chdir(FOLDER_NAME) 
# CONSTANTS

# File name constants
PASSWORD_STORAGE_FILE = Path(os.getcwd()+"/"+'passengers.json')
SECRETS_STORAGE_FILE = Path(os.getcwd()+"/"+'essentials.json')
USER_INFO_FILE = Path(os.getcwd()+'/'+'itenerary.json')
WALLET_STORAGE_FILE = Path(os.getcwd()+'/'+'locus.json')
PROJECT_STORAGE_FILE = Path(os.getcwd()+'/'+'memento.json')
# Backup constants

BACKUP_FOLDER_PATH = Path(os.getcwd()+"/"+'Backup')
REPOSITORY_PATH = Path(os.getcwd()+"/"+"..")
BACKUP_ZIP_FILE_PATH = "Backup.zip"
SECURE_VAULT_ZIP_PATH = 'Vault.zip'
EXTRACTION_FOLDER_PATH = "Here"

PASSWORD_FILE_NAME = 'passengers.json'
SECRETS_FILE_NAME = 'essentials.json'
WALLET_FILE_NAME = "locus.json"
PROJECT_FILE_NAME = "memento.json"
USER_INFO_FILE_NAME = 'itenerary.json'

# Github constants

COMMIT_MESSAGE = "Made some changes"
BRANCH = 'main'
FILES_TO_TRACK = FOLDER_NAME

# OS
windows = 'windows' in platform.platform().lower()
linux = 'linux' in platform.platform().lower()

# OS BASED VARIABLES
if windows:
    os.makedirs(f"c:/Users/{pa.getuser()}/.backup",exist_ok=True)
    BACKUP_DIR = f'c:/Users/{pa.getuser()}/.backup'
elif linux:
    if not os.path.exists(f"/home/{pa.getuser()}/.backup"):
        subprocess.run(["sudo","mkdir",f"/home/{pa.getuser()}/.backup"])
    BACKUP_DIR = f"/home/{pa.getuser()}/.backup"
# ENCRYPTION CONSTANTS
SALT_SIZE = 16
NONCE_SIZE = SecretBox.NONCE_SIZE
KEY_SIZE = SecretBox.KEY_SIZE
OPS_LIMIT = argon2id.OPSLIMIT_MODERATE
MEM_LIMIT = argon2id.MEMLIMIT_MODERATE

PASSWORD = '' #replace with secure password 
# Setting font color to green
if windows:
    os.system('color 2')
    
# FILE OPERATION FUNCTIONS

# Decrypting function


def derive_key(password: str,salt: bytes) -> bytes:
    return argon2id.kdf(KEY_SIZE,password.encode(),salt,opslimit = OPS_LIMIT,memlimit=MEM_LIMIT)

def encrypt_file(data_dict,password,file_path):
    content=json.dumps(data_dict).encode('utf-8')
    salt = random(SALT_SIZE)
    nonce = random(NONCE_SIZE)
    key = derive_key(password,salt)
    box = SecretBox(key)
    encrypted_data = box.encrypt(content,nonce)

    with open(file_path,'wb') as f:
        f.write(salt+encrypted_data)


def decrypt_file(password,file_path):
    with open(file_path,'rb') as f:
        blob = f.read()

    salt = blob[:SALT_SIZE]
    encrypted_data = blob[SALT_SIZE:]
    key = derive_key(password,salt)
    box = SecretBox(key)
    decrypted_data = box.decrypt(encrypted_data)       

    return json.loads(decrypted_data.decode("utf-8"))     

                     

# USER PERSONAL INFO FUNCTIONS

# Security questions function
def collect_security_questions():
    city = getpass('in which city were you born? '.upper()).strip().lower()
    color = getpass('what is your favorite colour? '.upper()).strip().lower()
    nick_name = getpass('what was your childhood nickname? '.upper()).strip().lower()
    retrival_pass = getpass("enter password you'll use for retrieval: ".upper()).strip()
    conf_retrieval_pass = getpass("confirm the password you'll use for retrieval: ".upper()).strip()
    attempts_remaining = 3
    while conf_retrieval_pass != retrival_pass:
        print(f'passwords do not match,please try again {attempts_remaining} more attempts remaining'.upper())
        retrival_pass = getpass("enter password you'll use for retrieval: ".upper()).strip()
        conf_retrieval_pass = getpass("confirm the password you'll use for retrieval: ".upper()).strip()
        attempts_remaining -= 1
        if attempts_remaining == 0:
            print('maximum number of attempts exceeded,kindly try again later'.upper())
            quit()
    securityQuizDict = {'city': city, 'color': color, 'nick_name': nick_name, "retrival_pass": retrival_pass}
    return securityQuizDict

def collect_git_credentials():
    gitUsername = getpass('Enter your github username: '.upper()).strip()
    gitEmail = getpass('enter the email linked to your github account: '.upper()).strip()
    gitRepoLink = getpass('enter the link to the repository that will store your files: '.upper()).strip()
    githubnInfoDict = {"gitUsername": gitUsername, "gitEmail": gitEmail, "gitRepoLink": gitRepoLink}
    return githubnInfoDict 



# BACKUP FUNCTIONS

# Local Backup function   

def create_encrypted_backup(zip_file_path, folder_path, target_directory=''):
    zip_pass = bytes(decrypt_file(file_path=USER_INFO_FILE,password=PASSWORD).get("retrival_pass"), encoding="utf8")
    
    if not os.path.exists(target_directory+"\\"+zip_file_path) or check_for_changes():
        with pyzipper.AESZipFile(zip_file_path, 'a', compression=pyzipper.ZIP_DEFLATED) as zip_file:
            zip_file.setpassword(zip_pass)
            zip_file.setencryption(pyzipper.WZ_AES, nbits=128) 
            if os.path.isdir(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Add file to zip if it's a regular file (not a directory)
                        if os.path.isfile(file_path):
                            zip_file.write(file_path, os.path.relpath(file_path, folder_path)) 
            else:
                zip_file.write(folder_path)
        if "Backup" in zip_file_path and not os.path.exists(target_directory+"/"+zip_file_path):
            if windows:
                shutil.move(zip_file_path, target_directory) 
            elif linux:
                subprocess.run(f"sudo mv {zip_file_path} {target_directory}", shell=True)
                
        elif "Backup" in zip_file_path and os.path.exists(target_directory+"/"+zip_file_path):
            
            if windows:
                os.remove(target_directory+"/"+zip_file_path) 
                shutil.move(zip_file_path, target_directory) 
            elif linux:
                subprocess.run(f"sudo rm -rf {target_directory}/{zip_file_path}", shell=True)
                subprocess.run(f"sudo mv {zip_file_path} {target_directory}", shell=True)
                
                
        shutil.rmtree(folder_path)  
    
            
def backup_all_files():

    if os.path.exists(BACKUP_FOLDER_PATH):
        if os.path.exists(PASSWORD_STORAGE_FILE):
            shutil.copy(PASSWORD_STORAGE_FILE, os.path.join(BACKUP_FOLDER_PATH, PASSWORD_FILE_NAME))


        if os.path.exists(USER_INFO_FILE):
            shutil.copy(USER_INFO_FILE, os.path.join(BACKUP_FOLDER_PATH, USER_INFO_FILE_NAME))    
        if os.path.exists(SECRETS_STORAGE_FILE):
            shutil.copy(SECRETS_STORAGE_FILE, os.path.join(BACKUP_FOLDER_PATH, SECRETS_FILE_NAME))
        if os.path.exists(WALLET_STORAGE_FILE):
            shutil.copy(WALLET_STORAGE_FILE, os.path.join(BACKUP_FOLDER_PATH, WALLET_FILE_NAME))
        if os.path.exists(PROJECT_STORAGE_FILE):    
            shutil.copy(PROJECT_STORAGE_FILE, os.path.join(BACKUP_FOLDER_PATH, PROJECT_FILE_NAME))
        if os.path.exists(SECURE_VAULT_ZIP_PATH):    
            shutil.copy(SECURE_VAULT_ZIP_PATH, os.path.join(BACKUP_FOLDER_PATH, SECURE_VAULT_ZIP_PATH))    

        if "window" in platform.platform().lower():
            subprocess.run(f"attrib +h +s +r {BACKUP_DIR}", shell=True, check=True)    
    else:
        os.makedirs(BACKUP_FOLDER_PATH, exist_ok=True)
        if os.path.exists(USER_INFO_FILE):
            shutil.copy(USER_INFO_FILE, BACKUP_FOLDER_PATH)
        if os.path.exists(PASSWORD_STORAGE_FILE):
            shutil.copy(PASSWORD_STORAGE_FILE, BACKUP_FOLDER_PATH)
        if os.path.exists(SECRETS_STORAGE_FILE):
            shutil.copy(SECRETS_STORAGE_FILE, BACKUP_FOLDER_PATH)
        if os.path.exists(WALLET_STORAGE_FILE):
            shutil.copy(WALLET_STORAGE_FILE, BACKUP_FOLDER_PATH)
        if os.path.exists(PROJECT_STORAGE_FILE):    
            shutil.copy(PROJECT_STORAGE_FILE, BACKUP_FOLDER_PATH)
        if os.path.exists(SECURE_VAULT_ZIP_PATH):    
            shutil.copy(SECURE_VAULT_ZIP_PATH, BACKUP_FOLDER_PATH)    
        create_encrypted_backup(zip_file_path=BACKUP_ZIP_FILE_PATH, folder_path=BACKUP_FOLDER_PATH, target_directory=BACKUP_DIR)
        if windows:
            try:
                import win32api, win32con
                win32api.SetFileAttributes(BACKUP_DIR, 
                                          win32con.FILE_ATTRIBUTE_HIDDEN | 
                                          win32con.FILE_ATTRIBUTE_SYSTEM | 
                                          win32con.FILE_ATTRIBUTE_READONLY)
            except ImportError:
                subprocess.run(f"attrib +h +s +r {BACKUP_DIR}", shell=True, check=True)


# Github Backup function 
def push_to_github(commit_message=COMMIT_MESSAGE, branch=BRANCH, folder_name=FOLDER_NAME):
    user_info_dictionary = decrypt_file(file_path=USER_INFO_FILE,password = PASSWORD)
    email = user_info_dictionary.get('gitEmail')
    username = user_info_dictionary.get('gitUsername')
    repo_link = user_info_dictionary.get('gitRepoLink')
    """
    Automatically stages, commits, and pushes files to GitHub.

    Args:
        repo_path (str): The local repository path.
        commit_message (str): The commit message.
        branch (str): The branch to push changes to.
        email (str): The Git user email.
        username (str): The Git username.
        repo_link (str): The remote repository URL.
        files_to_track (str): Files to track (default: "a" for all).
    """
    try:
        # Ensure repo_path exists
        # os.chdir(REPOSITORY_PATH)
        # Check if this is already a Git repository
        is_git_repo = os.path.exists(os.path.join(REPOSITORY_PATH, ".git"))

        if not is_git_repo:
            try:
                print("Initializing a new Git repository...")
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'config', 'init.defaultBranch', branch], check=True)
                subprocess.run(['git', 'remote', 'add', 'origin', repo_link], check=True)
                # Mark the repo as safe
                subprocess.run(["git", "config", "--add", "safe.directory", REPOSITORY_PATH], check=True)
                # Configure Git user information (local, not global)
                subprocess.run(['git', 'config', 'user.name', username], check=True)
                subprocess.run(['git', 'config', 'user.email', email], check=True)

                
                subprocess.run(['git', 'add', folder_name], check=True)
                # Commit changes
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)

                # Push changes
                subprocess.run(['git', 'push', '-u', 'origin', branch], check=True)

                print("✅ Changes pushed to GitHub successfully.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Git command failed: {e}")
                print("⚠️ Removing .git directory to reset the repository...")
                # subprocess.run(["rmdir", "/s", "/q", ".git"], check=True, shell=True)
                print("🗑️ .git directory removed successfully")
        else:
            try:
                # Mark the repo as safe
                subprocess.run(["git", "config", "--add", "safe.directory", REPOSITORY_PATH], check=True)
                #Stage Files
                subprocess.run(['git', 'add', folder_name], check=True)
                # Commit changes
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                #Push Changes
                subprocess.run(['git', 'push', '-u', 'origin', branch], check=True)
                print("✅ Changes pushed to GitHub successfully.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Git command failed: {e}")
                print("⚠️ Removing .git directory to reset the repository...")
                # subprocess.run(["rmdir", "/s", "/q", ".git"], check=True)
                print("🗑️ .git directory removed successfully")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        # subprocess.run(["rmdir", "/s", "/q", ".git"], check=True, shell=True)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # subprocess.run(["rmdir", "/s", "/q", ".git"], check=True, shell=True)

# USER INPUT FUNCTIONS

# PASSWORD FUNCTIONS
def generate_secure_password():
    lower = 'abcdefghijklmnopqrstuvwxyz '
    upper = lower.upper()
    number = '0123456789 '
    symbols = '!@#$%^&*,? '

    character_set = lower + upper + number + symbols
    length = int(input('How many characters would you like your password to have? '.upper()))
    while True:
        password = ''.join(rd.sample(character_set, length))
        if (re.search(r"[0-9]", password) and re.search(r"[a-z]", password) and re.search(r"[A-Z]", password) and re.search(r"[!@#$%^&*,?]", password)):
            break
        else:
            continue    

    return password

def get_user_password():
    password = getpass('enter the password: '.upper())
    conf_pass = getpass('confirm your password: '.upper())
    attempts_remaining = 3
    while conf_pass != password:
        print(f'passwords do not match,please try again {attempts_remaining} more attempts remaining'.upper())
        password = getpass('enter the password: '.upper()).strip()
        conf_pass = getpass('confirm your password: '.upper()).strip()
        attempts_remaining -= 1
        if attempts_remaining == 0:
            print('maximum number of attempts exceeded,kindly try again later'.upper())
    return password        


# OCR FUNCTION
def extract_seedphrase_from_image(image_path):
    if os.path.exists(image_path):
         pass
    else:
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    from paddleocr import PaddleOCR
    import logging
    logging.getLogger('PaddleOCR').setLevel(logging.CRITICAL)
    ocr = PaddleOCR(use_angle_cls=True, lang='en', gpu=True)  # need to run only once to download the model and load it into memory
    result = ocr.ocr(image_path, cls=True)
    word_list = []
    for line in result[0]:
        try:
            if line[1][0][0:2].isnumeric() and line[1][0][2] == '.' and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:3], " ").strip())
            elif line[1][0][0].isnumeric() and line[1][0][1] == '.' and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:2], " ").strip())    
            elif " " in line[1][0]:
                word_list.append(line[1][0].split(' ')[1])
         
            elif line[1][0][0:2].isnumeric() and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:2], " ").strip())
            elif line[1][0][0].isnumeric() and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0], " ").strip())
            elif line[1][0].isnumeric() or (line[1][0][0:2].isnumeric() and len(line[1][0]) == 3) or (line[1][0][0].isnumeric() and len(line[1][0]) == 2):
                pass
            else:
                word_list.append(line[1][0])     
        except IndexError:
            pass  
          
    os.remove(image_path)
    return {i+1: value for i, value in enumerate(word_list)} 
    

# UTILITY FUNCTIONS

# Clearing console function
def clear_screen():
    if windows:
        subprocess.run("cls", shell=True)
    elif linux or "mac" in platform.platform().lower():
        subprocess.run("clear", shell=True)
    else:
        print("Dang what Os is that?")

# Confirms if changes were made on files
def check_for_changes():
    if os.path.exists('.git'):
        results = subprocess.run(['git', "status", "--porcelain"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        tracked_changes = [line for line in results.stdout.splitlines() if (line.strip().startswith("?? production")) or (line.strip().startswith("M production"))]
        if tracked_changes:
            return True
        else:
            return False
        
    return True 

# MAIN CLASS
class PasswordManager():   
    if os.path.exists(PASSWORD_STORAGE_FILE):
        password_dictionary = decrypt_file(file_path=PASSWORD_STORAGE_FILE,password = PASSWORD)
    else:
        password_dictionary = {}
    if os.path.exists(SECRETS_STORAGE_FILE):    
        secrets_dictionary = decrypt_file(file_path=SECRETS_STORAGE_FILE,password = PASSWORD)
    else:
        secrets_dictionary = {}
    if os.path.exists(USER_INFO_FILE):    
        user_info_dictionary = decrypt_file(file_path=USER_INFO_FILE,password=PASSWORD)
    else:
        user_info_dictionary = {}
    if os.path.exists(WALLET_STORAGE_FILE):    
        wallet_dictionary = decrypt_file(file_path=WALLET_STORAGE_FILE,password = PASSWORD)
    else:
        wallet_dictionary = {}
    if os.path.exists(PROJECT_STORAGE_FILE):    
        projects_dictionary = decrypt_file(file_path=PROJECT_STORAGE_FILE,password = PASSWORD)
    else:
        projects_dictionary = {}
    @classmethod  
    def authenticate_user(cls):
        if os.path.exists(USER_INFO_FILE): 
            username = input('enter your vault username: '.upper())
            username_attempts_remaining = 3
            while username not in cls.user_info_dictionary.keys() and username_attempts_remaining > 0:
                print(f'incorrect username {username_attempts_remaining} more attempts remaining'.upper())
                username = input('enter your vault username: '.upper())
                username_attempts_remaining -= 1
                if username_attempts_remaining == 0:
                    print('maximum number of attempts reached'.upper())
                    return False
            vault_password = getpass('enter your vault password: '.upper()).strip()
            password_attempts_remaining = 3
           
            while vault_password != cls.user_info_dictionary.get(username) and password_attempts_remaining > 0:
                print(f'incorrect password {password_attempts_remaining} more attempts remaining')
                vault_password = getpass('enter your vault password: '.upper())
                password_attempts_remaining -= 1
                if password_attempts_remaining == 0:
                    print('answer the following security questions to reset your password'.upper())
                    [city, color, nick_name] = collect_security_questions().values()
                    values = cls.user_info_dictionary.values()
                    if color in values and city in values and nick_name in values:
                        new_passwd = getpass('enter your new password: '.upper())
                        new_passwd_conf = getpass('confirm your new password: '.upper())
                        count = 0
                        while new_passwd != new_passwd_conf:
                            print('The password you entered do not match')
                            new_passwd = getpass('enter your new password: '.upper())
                            new_passwd_conf = getpass('confirm your new password: '.upper())
                            count += 1
                            if count == 3:
                                print('maximum number of attempts reached'.upper())
                                return False
                        else:
                            cls.user_info_dictionary.pop(username)
                            cls.user_info_dictionary.update({username: new_passwd})
                            print('password was reset succssefuly!!'.upper())
                            cls.username = username
                            return True
                    else:
                        print('wrong details!! please try again later'.upper())
                        return False
            else:
                cls.username = username
                cls.password = vault_password
                clear_screen()
                return True
    @classmethod            
    def create_new_user(cls):
        vault_user_name = input('enter your vault username: '.upper())
        cls.username = vault_user_name
        vault_pass = getpass('set your vault password: '.upper()).strip()
        conf_vault_pass = getpass('confirm your vault password: '.upper()).strip()
        attempts_remaining = 3
        while conf_vault_pass != vault_pass:
            print(f'password doesnt match please try again you have {attempts_remaining} more attempts'.upper())
            conf_vault_pass = getpass('confirm your vault password: '.upper()).strip()
            attempts_remaining -= 1
            if attempts_remaining == 0:
                print('too many attempts try again later'.upper())
                exit()
        secretPhrase = getpass('set your secret phrase: '.upper()).strip()
        conf_secretPhrase = getpass('confirm your secret phrase: '.upper()).strip()
        attempts_remaining = 3
        while conf_secretPhrase != secretPhrase:
            print(f'secret phrase doesnt match please try again you have {attempts_remaining} more attempts'.upper())
            conf_secretPhrase = getpass('confirm your secret phrase: '.upper()).strip()
            attempts_remaining -= 1
            if attempts_remaining == 0:
                print('too many attempts try again later'.upper())
                quit()
        else:
            print('answer the following emergency questions'.upper())
            security_info_dict = collect_security_questions()
            security_info_dict.update({'secretPhrase': secretPhrase})
            security_info_dict.update({vault_user_name: vault_pass})
            git_info_dict = collect_git_credentials()
            security_info_dict.update(git_info_dict)
            cls.user_info_dictionary.update(security_info_dict)
            encrypt_file(data_dict = cls.user_info_dictionary, file_path = USER_INFO_FILE,password = PASSWORD)
            print('account succssefully created!'.upper()) 
            clear_screen()
        return True 

    @classmethod
    def manage_vault_actions(cls):
        print(f'olaa, {cls.username} welcome to your vault'.upper())
        while True:
            action_choices = ['create', 'retrieve', 'list', "exit", "clear"]
            activity_choices = ['email', 'account', "exit", "clear", cls.user_info_dictionary.get("secretPhrase"), "web3", "file"]
            activity_choice = input("email | account | web3 | file | clear | exit'? ".upper()).lower()
            while activity_choice not in activity_choices:
                print('invalid input'.upper())
                
                activity_choice = input("email | account | web3 | file | clear | exit'? ".upper()).lower()
            if activity_choice == 'email':
                while True:

                    action_choice = input('Would you like to create | retrieve | list emails | exit? '.upper()).lower()
                    
                    while action_choice not in action_choices:
                        print('invalid input'.upper())
                        action_choice = input('Would you like to create | retrieve | list emails | exit? '.upper()).lower()
                    if action_choice == 'retrieve':
                        mail_address = input('Enter the e-mail address: '.upper())
                        value = cls.password_dictionary.get(mail_address, 'invalid account or username')
                        if value == 'invalid account or username':
                            print(value.upper())
                        else:
                            pyperclip.copy(value)    
                            print(f'Your "{mail_address}" password has been copied to clipboard')    

                    elif action_choice == "create":
                        email_address = input('Enter the e-mail address: '.upper()).strip()
                        password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        while password_choice not in ['a', 'g']:
                            print('invalid input'.upper())
                            password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        if password_choice == 'g':
                            password = generate_secure_password()
                        elif password_choice == 'a':
                            password = get_user_password()    
                        cls.password_dictionary.update({email_address: password})  
                        pyperclip.copy(password)       
                        print('your password has been copied to clipboard'.upper())   
                        encrypt_file(data_dict=cls.password_dictionary, file_path=PASSWORD_STORAGE_FILE,password = PASSWORD)
                    elif action_choice == "list":
                        email_list = [i for i in cls.password_dictionary.keys() if " " not in i]
                        if email_list:
                            print(*email_list, sep="\n")
                        else:
                            print("No emails available")    
                    elif action_choice == "exit":
                        clear_screen()
                        break
            elif activity_choice == "account":
                while True:
                    action_choice = input('Would you like to create | retrieve | list accounts | exit? '.upper()).lower()
                    while action_choice not in action_choices:
                        print('invalid input'.upper())
                        action_choice = input('Would you like to create | retrieve | list accounts | exit? '.upper()).lower()
                    if action_choice == "retrieve":
                        acc = input('Enter the a/c: '.upper())
                        username = input('enter your username: '.upper())
                        account_identifier = acc + ' ' + username
                        value = cls.password_dictionary.get(account_identifier, 'invalid account or username')
                        if value == 'invalid account or username':
                            print(value.upper())
                        else:
                            pyperclip.copy(value)    
                            print(f'Your "{acc}" password for "{username}" has been copied to clipboard')
                    elif action_choice == "create":
                        acc = input('Enter the a/c: '.upper()).strip()
                        username = input('enter your username: '.upper()).strip()
                        account_identifier = acc + ' ' + username

                        password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        while password_choice not in ['a', 'g']:
                            print('invalid input'.upper())
                            password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        if password_choice == 'g':
                            password = generate_secure_password()
                        elif password_choice == 'a':
                            password = get_user_password()    
                        cls.password_dictionary.update({account_identifier: password})  
                        pyperclip.copy(password)       
                        print('your password has been copied to clipboard'.upper())   
                        encrypt_file(data_dict=cls.password_dictionary, file_path=PASSWORD_STORAGE_FILE,password=PASSWORD)
                    elif action_choice == "list":
                        accounts_list = [i for i in cls.password_dictionary.keys() if " " in i]
                        if accounts_list:
                            print(*accounts_list, sep="\n")
                        else:
                            print("No accounts available")   
                    elif action_choice == "exit":
                        clear_screen()
                        break         
            elif activity_choice == "web3":
                file_action_choices = ['wallet', "project"]
                file_action_choice = input("wallet | project: ".upper()).strip().lower()
                while True:
                    while file_action_choice not in file_action_choices:
                        print("invalid input".upper())
                        file_action_choice = input("wallet | project: ".upper()).strip().lower()
                    if file_action_choice == "wallet":
                        action_choice = input('Would you like to create | retrieve | list wallets | exit? '.upper()).lower()
                        while action_choice not in action_choices:
                            print('invalid input'.upper())
                            action_choice = input('Would you like to create | retrieve | list wallets | exit? '.upper()).lower()
                        if action_choice == "retrieve":
                            app_name = input("enter app name: ".upper()).strip()
                            wallet_name = input("enter name of the wallet: ".upper()).strip()
                            wallet_email = input("enter email associated with wallet: ".upper()).strip()
                               
                            account_identifier = app_name + ' ' + wallet_name + ' ' + wallet_email
                            value = cls.wallet_dictionary.get(account_identifier, 'invalid account or username')
                            if value == 'invalid account or username':
                                print(value.upper())
                            else:
                                pyperclip.copy(value)    
                                print(f'Your "{app_name}" "{wallet_name}" details for "{wallet_email}" have been copied to clipboard')
                        elif action_choice == "create":
                            app_name = input("enter app name: ".upper()).strip()
                            wallet_name = input("enter name of the wallet: ".upper()).strip()
                            wallet_email = input("enter email associated with wallet: ".upper()).strip()
                            account_identifier = app_name + ' ' + wallet_name + " " + wallet_email

                            password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            while password_choice not in ['a', 'g']:
                                print('invalid input'.upper())
                                password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            if password_choice == 'g':
                                password = generate_secure_password()
                            elif password_choice == 'a':
                                password = get_user_password() 

                            seedphrase_input_choices = ['manual', 'image']
                            seedphrase_input_choice = input("enter seedphrase manual | image: ".upper()).lower()
                            while seedphrase_input_choice not in seedphrase_input_choices:
                                print('invalid input'.upper())
                                seedphrase_input_choice = input("enter seedphrase manual | image: ".upper()).lower()
                            if seedphrase_input_choice == 'manual':
                                seedphrase = input('enter your seedphrases separated by "," (no spaces): '.upper()).strip()
                                seedphrase_dict = {i+1: value for i, value in enumerate(seedphrase.split(','))}
                            elif seedphrase_input_choice == 'image':
                                image_path = input('enter the path to the image: '.upper()).strip()
                                seedphrase_dict = extract_seedphrase_from_image(image_path)

                            cls.wallet_dictionary.update({account_identifier: {"password": password, "seedphrase": seedphrase_dict}})  
                            pyperclip.copy(password)       
                            print(f'your password for"{app_name}" "{wallet_name}" for email "{wallet_email}" havebeen copied to clipboard'.upper()) 
                            encrypt_file(data_dict=cls.wallet_dictionary, file_path=WALLET_STORAGE_FILE,password = PASSWORD)  
                        elif action_choice == "list":
                            accounts_list = {i.split(' ')[0] for i in cls.wallet_dictionary.keys()}
                            if accounts_list:
                                print(*accounts_list, sep="\n")
                            else:
                                print("No Wallets available") 

                        elif action_choice == "exit":
                            print("you web3 info has been secured".capitalize())
                            clear_screen()
                            break
                    elif file_action_choice == "project":
                        action_choice = input('Would you like to create | retrieve | list projects | exit? '.upper()).lower()
                        while action_choice not in action_choices:
                            print('invalid input'.upper())
                            action_choice = input('Would you like to create | retrieve | list projects | exit? '.upper()).lower()
                        if action_choice == "retrieve":
                            project_name = input("enter project name: ".upper()).strip().strip()
                            project_username = input("enter name of the wallet: ".upper()).strip().strip()
                            project_email = input("enter email associated with wallet: ".upper()).strip().strip()
                            account_identifier = project_name + ' ' + project_username + ' ' + project_email
                            value = cls.projects_dictionary.get(account_identifier, 'invalid account or username')
                            if value == 'invalid account or username':
                                print(value.upper())
                            else:
                                pyperclip.copy(value)    
                                print(f'Your "{project_name}" details for "{project_username}" have been copied to clipboard')
                        elif action_choice == "create":
                            project_name = input("enter project name: ".upper()).strip()
                            project_username = input("enter username: ".upper()).strip()
                            project_email = input("enter email associated with wallet: ".upper()).strip()
                            connected_wallet = input("enter the name of the wallet connected to this project: ".upper()).strip()
                            account_identifier = project_name + ' ' + project_username + " " + project_email
                            password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            while password_choice not in ['a', 'g']:
                                print('invalid input'.upper())
                                password_choice = input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            if password_choice == 'g':
                                password = generate_secure_password()
                            elif password_choice == 'a':
                                password = get_user_password() 

                            cls.projects_dictionary.update({account_identifier: {"password": password, "wallet": connected_wallet}})  
                            pyperclip.copy(password)       
                            print(f'your "{project_name}" for {project_username} has been copied to clipboard'.upper()) 
                            encrypt_file(data_dict=cls.projects_dictionary, file_path=PROJECT_STORAGE_FILE,password=PASSWORD)  
                        elif action_choice == "list":
                            accounts_list = {i.split(' ')[0] for i in cls.projects_dictionary.keys()}
                            if accounts_list:
                                print(*accounts_list, sep="\n")
                            else:
                                print("No projects available") 
                        elif action_choice == "exit":
                            print("you web3 info has been secured".capitalize())
                            clear_screen()
                            break     

            elif activity_choice == cls.user_info_dictionary.get("secretPhrase"):
                clear_screen() 
                print('Welcome...Your secret is safe with me')
                choices = ['share', 'reveal', 'quit']
                choice = ''
                while choice != 'quit':
                    choice = input('would you like to share || reveal a secret(s) || quit: '.upper()).lower()
                    if choice == 'share':
                        secret = input('enter your secret: '.upper())
                        now = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                        cls.secrets_dictionary.update({now: secret})
                        encrypt_file(data_dict=cls.secrets_dictionary, file_path=SECRETS_STORAGE_FILE,password = PASSWORD)
                    elif choice == 'reveal':
                        if cls.secrets_dictionary:
                            print(cls.secrets_dictionary)  
                        else:
                            print("You have no secrets")       
                        
                    elif choice not in choices:
                        print('invalid input'.upper())    
                print('Your secerts have been secured!!'.upper())
                sleep(2.2)
                clear_screen()


            # SECURING FILE FUNCTIONALITY

            elif activity_choice == 'file':
                file_action_choices = ['secure', 'retrieve', "list", "exit", 'clear', "empty"]
                zip_pass = bytes(decrypt_file(file_path=USER_INFO_FILE,password = PASSWORD).get("retrival_pass"), encoding="utf8")
                zip_file_path = SECURE_VAULT_ZIP_PATH
                while True:
                    file_action_choice = input("would you like to secure | retrieve | clear | empty vault | list secured files | exit: ".upper()).strip().lower()
                    while file_action_choice not in file_action_choices:
                        print("invalid input".upper())
                        file_action_choice = input("would you like to secure | retrieve | clear | list secured files | exit: ".upper()).strip().lower()
                   
                    if file_action_choice == "retrieve":
                        if os.path.exists(zip_file_path):
                            extract_folder = str(REPOSITORY_PATH) + "/" + EXTRACTION_FOLDER_PATH
                            path_file = input("enter the name of the file you would like to retrieve: ".upper()).strip()
                            if not os.path.exists(extract_folder):    
                                os.makedirs(extract_folder)
                                
                            with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
                                zip_file.setpassword(zip_pass)
                                if path_file in zip_file.namelist():
                                    zip_file.extract(path_file, path=extract_folder)
                                    print(f"You can access the file here {extract_folder}")
                                    back_to_zip = input("would you like to delete the file after accessing it? y(yes) | n(no): ".upper()).strip().lower()
                                    while back_to_zip not in ['y', 'n']:
                                        print("invalid choice")
                                        back_to_zip = input("would you like to secure the file after accessing it? y(yes) | n(no): ".upper()).strip().lower()
                                    if back_to_zip == 'y':
                                        done = input("press enter to delete the file: ".upper()).strip()
                                        if done == "" or done:
                                            shutil.rmtree(extract_folder)
                                            print("The file has been deleted".upper())
                                else:
                                    print("That file is not in the vault".upper())
                                   
                           
                        else:
                            print("the vault is empty!".upper())
                    elif file_action_choice == "secure":
                        consent_choices = ["y", 'n']
                        try:

                        # if 
                            path_file = input("enter the path to the file you would like to secure: ".upper()).strip()
                            if not os.path.exists(path_file):
                                raise FileNotFoundError(f"The file {path_file} does not exist.")
                            if not os.path.isdir(path_file):
                                print("File path is not a directory".upper())
                                continue
                            else:

                                consent_choice = input("proceeding with this actions means that the file will only exist in the vault and can only be accessed using the retrieval password, would you like to proceed? y(yes) | n(no): ".capitalize()).strip().lower()
                                while consent_choice not in consent_choices:
                                    print("invalid input")
                                    consent_choice = input("y(yes) | n(no): ".upper()).strip().lower()
                                if consent_choice == "y":
                                    try:
                                        create_encrypted_backup(folder_path=path_file, zip_file_path=zip_file_path)
                                        print(f"{os.path.basename(path_file)} has been secured".upper())
                                    except FileNotFoundError as e:
                                        print(f"an error occured: {e}")    
                                else:
                                    print("You cancelled the securing file process")
                                    clear_screen()
                                    continue
                        except Exception as e:
                            print(f"an error occured: {e}")    
                            continue

                    elif file_action_choice == "list":
                        if os.path.exists(zip_file_path):
                            with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
                                zip_file.setpassword(zip_pass)
                                file_list = zip_file.namelist()
                                if file_list:
                                    print(*file_list, sep="\n")
                                else:
                                    print("No files in vault")    
                        else:
                            print("the vault is empty!".upper())
                    elif file_action_choice == "empty":
                        if os.path.exists(zip_file_path):
                            os.remove(zip_file_path)
                            print("vault emptied successfully".upper())
                        else:
                            print("the vault is already empty!".upper())
                    elif file_action_choice == "clear":
                        clear_screen()
                    elif file_action_choice == "exit":
                        clear_screen()
                        break
            elif activity_choice == 'clear':
                clear_screen()
            elif activity_choice == 'exit':
                print('Your vault has been locked'.upper())
                sleep(2.2)
                clear_screen()
                break
            else:
                print('invalid input'.upper())
# Logic
def run_password_vault():
    membership_verified = PasswordManager.authenticate_user()
    try:
        if membership_verified:
            PasswordManager.manage_vault_actions()
        elif membership_verified == None:
            PasswordManager.create_new_user()
            PasswordManager.manage_vault_actions()
    except Exception as error:
        print(f'an error occurred: {error.args}'.upper())
        return 
    finally:
        if check_for_changes():
            backup_all_files()
        else:
            pass   
 
# Running
if __name__ == '__main__':
    run_password_vault()
    os.chdir(REPOSITORY_PATH)
    
    try:
        
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
                        
            if check_for_changes():
                push_to_github()
            else:
                print("No changes to push to GitHub.")
                            
        else:
            print('Internet access is not available'.upper())
            sleep(2.5)
    except requests.ConnectionError:
        print('No internet Connection'.upper())
        sleep(2.5)
