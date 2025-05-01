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
from cryptography.fernet import Fernet
import pyperclip
from getpass import getpass
from datetime import datetime
import platform



FOLDER_NAME = 'production'

if os.path.exists(FOLDER_NAME):
    os.chdir(FOLDER_NAME)
else:
    os.mkdir(FOLDER_NAME)
    os.chdir(FOLDER_NAME) 
# CONSTANTS

# File name constants
PASSWD_FILE = os.getcwd()+"\\"+'passengers.json'
SECRETS_FILE=os.getcwd()+"\\"+'essentials.json'
CARS_FILE = os.getcwd()+"\\"+'cars.txt'
PERSONAL_INFO_FILE = os.getcwd()+'\\'+'itenerary.json'
WALL_FILE = os.getcwd()+'\\'+'locus.json'
PROJ_FILE= os.getcwd()+'\\'+'memento.json'
# Backup constants
BASE_DIR = 'C:\\Users'



FOLDER_PATH = os.getcwd()+"\\"+'Backup'
REPO_PATH = os.getcwd()+"\\"+"../"
ZIP_FILE_PATH = "Backup.zip"
FILE_VAULT_PATH = 'Vault.zip'
FILE_EXTRACT_FOLDER_PATH = "Here"

PASSWD_FILE_NAME = 'passengers.json'
SECRETS_FILE_NAME='essentials.json'
CARS_FILE_NAME = 'cars.txt'
WALL_FILE_NAME = "locus.json"
PROJ_FILE_NAME = "memento.json"
PERSONAL_INFO_FILE_NAME='itenerary.json'

# Github constants

COMMIT_MESSAGE = "Made some changes"
BRANCH = 'main'
FILES_TO_TRACK = FOLDER_NAME

# OS BASED VARIABLES
if 'windows' in platform.platform().lower():
    os.makedirs(f"c:/Users/{pa.getuser()}/.backup",exist_ok=True)
    BACKUP_DIR=f'c:/Users/{pa.getuser()}/.backup'
elif 'linux' in platform.platform().lower():
    if not os.path.exists(f"/home/{pa.getuser()}/.backup"):
        subprocess.run(["sudo","mkdir",f"/home/{pa.getuser()}/.backup"])
    BACKUP_DIR=f"/home/{pa.getuser()}/.backup"

# Setting font color to green
if 'windows' in platform.platform().lower():
    os.system('color 2')
    


# FILE OPERATION FUNCTIONS

# Decrypting fuction
def unlock(file):
    if os.path.exists(file): 
        with open(CARS_FILE,'rb') as f:
            key=f.read()
        with open(file,'rb') as f:
            cont=f.read()
        cont_decr=json.loads(Fernet(key).decrypt(cont).decode())
        return cont_decr 
    else:
        raise FileNotFoundError
    
# Encrypting function    
def lock(dictionary,file):
    if not os.path.exists(CARS_FILE):
        with open(CARS_FILE,'wb') as f:
            key = Fernet.generate_key()
            f.write(key)
        cont=json.dumps(dictionary).encode('utf-8')
        cont_encr=Fernet(key).encrypt(cont)
        with open(file,'wb') as f:
            f.write(cont_encr)
     
    else:
        with open(CARS_FILE,'rb') as f:
            key=f.read()
        cont=json.dumps(dictionary).encode('utf-8')
        cont_encr=Fernet(key).encrypt(cont)
        with open(file,'wb') as f:
            f.write(cont_encr)

                     

# USER PERSONAL INFO FUNCTIONS

# Security questions function
def securityQuiz():
    city=getpass('in which city were you born? '.upper()).strip().lower()
    color=getpass('what is your favorite colour? '.upper()).strip().lower()
    nick_name=getpass('what was your childhood nickname? '.upper()).strip().lower()
    retrival_pass = getpass("enter password you'll use for retrieval: ".upper()).strip()
    conf_retrieval_pass = getpass("confirm the password you'll use for retrieval: ".upper()).strip()
    count=3
    while conf_retrieval_pass !=retrival_pass:
        print(f'passwords do not match,please try again {count} more attempts remaining'.upper())
        retrival_pass = getpass("enter password you'll use for retrieval: ".upper()).strip()
        conf_retrieval_pass = getpass("confirm the password you'll use for retrieval: ".upper()).strip()
        count-=1
        if count==0:
            print('maximum number of attempts exceeded,kindly try again later'.upper())
            quit()
    securityQuizDict = {'city':city,'color':color,'nick_name':nick_name,"retrival_pass":retrival_pass}
    return securityQuizDict

def gitInfo():
    gitUsername = getpass('Enter your github username: '.upper()).strip()
    gitEmail = getpass('enter the email linked to your github account: '.upper()).strip()
    gitRepoLink = getpass('enter the link to the repository that will store your files: '.upper()).strip()
    githubnInfoDict = {"gitUsername":gitUsername,"gitEmail":gitEmail,"gitRepoLink":gitRepoLink}
    return githubnInfoDict 



# BACKUP FUNCTIONS

# Local Backup function   

def zip_file_func(zip_file_path,folder_path,target_dir=''):
    zip_pass = bytes(unlock(PERSONAL_INFO_FILE).get("retrival_pass"),encoding="utf8")
    
    if not os.path.exists(target_dir+"\\"+zip_file_path) or conf_changes():
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
        if "Backup" in zip_file_path and not os.path.exists(target_dir+"\\"+zip_file_path):
            shutil.move(zip_file_path,target_dir) 

        elif "Backup" in zip_file_path:
            os.remove(target_dir+"\\"+zip_file_path) 
            shutil.move(zip_file_path,target_dir)
                
        shutil.rmtree(folder_path)  
    
            
def backup():

    if os.path.exists(FOLDER_PATH):
        if os.path.exists(PASSWD_FILE):
            shutil.copy(PASSWD_FILE, os.path.join(FOLDER_PATH, PASSWD_FILE_NAME))

        if os.path.exists(CARS_FILE):
            shutil.copy(CARS_FILE, os.path.join(FOLDER_PATH, CARS_FILE_NAME))

        if os.path.exists(PERSONAL_INFO_FILE):
            shutil.copy(PERSONAL_INFO_FILE, os.path.join(FOLDER_PATH, PERSONAL_INFO_FILE_NAME))    
        if os.path.exists(SECRETS_FILE):
            shutil.copy(SECRETS_FILE, os.path.join(FOLDER_PATH, SECRETS_FILE_NAME))
        if os.path.exists(WALL_FILE):
            shutil.copy(WALL_FILE, os.path.join(FOLDER_PATH, WALL_FILE_NAME))
        if os.path.exists(PROJ_FILE):    
            shutil.copy(PROJ_FILE, os.path.join(FOLDER_PATH, PROJ_FILE_NAME))
    else:
        os.makedirs(FOLDER_PATH, exist_ok=True)
        if os.path.exists(PERSONAL_INFO_FILE):
            shutil.copy(PERSONAL_INFO_FILE, FOLDER_PATH)
        if os.path.exists(CARS_FILE):
            shutil.copy(CARS_FILE, FOLDER_PATH)
        if os.path.exists(PASSWD_FILE):
            shutil.copy(PASSWD_FILE, FOLDER_PATH)
        if os.path.exists(SECRETS_FILE):
            shutil.copy(SECRETS_FILE, FOLDER_PATH)
        if os.path.exists(WALL_FILE):
            shutil.copy(WALL_FILE, FOLDER_PATH)
        if os.path.exists(PROJ_FILE):    
            shutil.copy(PROJ_FILE, FOLDER_PATH)
        zip_file_func(zip_file_path=ZIP_FILE_PATH,folder_path=FOLDER_PATH,target_dir=BACKUP_DIR)
        subprocess.run(f"attrib +h +s +r {BACKUP_DIR}",shell=True,check=True)


# Github Backup function 
def git_push(commit_message=COMMIT_MESSAGE, branch=BRANCH,folder_name = FOLDER_NAME):
    personalinfodict = unlock(PERSONAL_INFO_FILE)
    email = personalinfodict.get('gitEmail')
    username = personalinfodict.get('gitUsername')
    repo_link = personalinfodict.get('gitRepoLink')
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
        # os.chdir(REPO_PATH)
        # Check if this is already a Git repository
        is_git_repo = os.path.exists(os.path.join(REPO_PATH, ".git"))

        if not is_git_repo:
            try:
                print("Initializing a new Git repository...")
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'config', 'init.defaultBranch', branch], check=True)
                subprocess.run(['git', 'remote', 'add', 'origin', repo_link], check=True)
                # Mark the repo as safe
                subprocess.run(["git", "config", "--add", "safe.directory", REPO_PATH], check=True)
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
                subprocess.run(["git", "config", "--add", "safe.directory", REPO_PATH], check=True)
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
def password_generator():
    lower='abcdefghijklmnopqrstuvwxyz'
    upper=lower.upper()
    number='0123456789'
    symbols='!@#$%^&*,?'

    al=lower+upper+number+symbols
    length=int(input('How many characters would you like your password to have? '.upper()))
    while True:
        password=''.join(rd.sample(al,length))
        if (re.search(r"[0-9]",password) and re.search(r"[a-z]",password) and re.search(r"[A-Z]",password) and re.search(r"[!@#$%^&*,?]",password)):
            break
        else:
            continue    

    return password

def create_own_pass():
    password=getpass('enter the password: '.upper())
    conf_pass=getpass('confirm your password: '.upper())
    count=3
    while conf_pass !=password:
        print(f'passwords do not match,please try again {count} more attempts remaining'.upper())
        password=getpass('enter the password: '.upper()).strip()
        conf_pass=getpass('confirm your password: '.upper()).strip()
        count-=1
        if count==0:
            print('maximum number of attempts exceeded,kindly try again later'.upper())
    return password        


# OCR FUNCTION
def seedphrase_ocr(image_path):
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
                word_list.append(line[1][0].replace(line[1][0][0:3]," ").strip())
            elif line[1][0][0].isnumeric() and line[1][0][1] == '.' and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:2]," ").strip())    
            elif " " in line[1][0]:
                word_list.append(line[1][0].split(' ')[1])
         
            elif line[1][0][0:2].isnumeric() and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:2]," ").strip())
            elif line[1][0][0].isnumeric() and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0]," ").strip())
            elif line[1][0].isnumeric() or (line[1][0][0:2].isnumeric() and len(line[1][0]) == 3) or (line[1][0][0].isnumeric() and len(line[1][0]) == 2):
                pass
            else:
                word_list.append(line[1][0])     
        except IndexError:
            pass  
          
    os.remove(image_path)
    return {i+1:value for i,value in enumerate(word_list)} 
    

# UTILITY FUNCTIONS

# Clearing console function
def clear_console():
    if 'windows' in platform.platform().lower():
        subprocess.run("cls",shell=True)
    elif 'linux' in platform.platform().lower() or "mac" in platform.platform().lower() :
        subprocess.run("clear",shell=True)
    else:
        print("Dang what Os is that?")

# Confirms if changes were made on files
def conf_changes():
    if os.path.exists('.git'):
        results = subprocess.run(['git',"status","--porcelain"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True)
        tracked_changes = [line for line in results.stdout.splitlines() if (line.strip() and not line.startswith("??") or line.startswith("?? production"))]
        if tracked_changes:
            return True
        else:
            return False
        
    return True 

# MAIN CLASS
class essentials():   
    if os.path.exists(PASSWD_FILE):
        passwd_dict=unlock(PASSWD_FILE)
    else:
        passwd_dict={}
    if os.path.exists(SECRETS_FILE):    
        secretdict = unlock(SECRETS_FILE)
    else:
        secretdict={}
    if os.path.exists(PERSONAL_INFO_FILE):    
        personalinfodict = unlock(PERSONAL_INFO_FILE)
    else:
        personalinfodict = {}
    if os.path.exists(WALL_FILE):    
        walletinfodict = unlock(WALL_FILE)
    else:
        walletinfodict = {}
    if os.path.exists(PROJ_FILE):    
        projectsinfodict= unlock(PROJ_FILE)
    else:
        projectsinfodict = {}
    @classmethod  
    def memb(cls):
        if os.path.exists(PERSONAL_INFO_FILE): 
            username=input('enter your vault username: '.upper())
            usernamecount=3
            while username not in cls.personalinfodict.keys() and usernamecount>0:
                print(f'incorrect username {usernamecount} more attempts remaining'.upper())
                username=input('enter your vault username: '.upper())
                usernamecount-=1
                if usernamecount==0:
                    print('maximum number of attempts reached'.upper())
                    return False
            vault_password=getpass('enter your vault password: '.upper()).strip()
            passwdcount=3
           
            while vault_password!=cls.personalinfodict.get(username) and passwdcount>0:
                print(f'incorrect password {passwdcount} more attempts remaining')
                vault_password=getpass('enter your vault password: '.upper())
                passwdcount-=1
                if passwdcount ==0:
                    print('answer the following security questions to reset your password'.upper())
                    [city,color,nick_name] = securityQuiz().values()
                    values = cls.personalinfodict.values()
                    if color in values and city in values and nick_name in values:
                        new_passwd=getpass('enter your new password: '.upper())
                        new_passwd_conf=getpass('confirm your new password: '.upper())
                        count=0
                        while new_passwd != new_passwd_conf:
                            print('The password you entered do not match')
                            new_passwd=getpass('enter your new password: '.upper())
                            new_passwd_conf=getpass('confirm your new password: '.upper())
                            count+=1
                            if count==3:
                                print('maximum number of attempts reached'.upper())
                                return False
                        else:
                            cls.personalinfodict.pop(username)
                            cls.personalinfodict.update({username:new_passwd})
                            print('password was reset succssefuly!!'.upper())
                            cls.username = username
                            return True
                    else:
                        print('wrong details!! please try again later'.upper())
                        return False
            else:
                cls.username  = username
                clear_console()
                return True
    @classmethod            
    def new(cls):
        vault_user_name=input('enter your vault username: '.upper())
        cls.username = vault_user_name
        vault_pass = getpass('set your vault password: '.upper()).strip()
        conf_vault_pass=getpass('confirm your vault password: '.upper()).strip()
        count=3
        while conf_vault_pass!=vault_pass:
            print(f'password doesnt match please try again you have {count} more attempts'.upper())
            conf_vault_pass=getpass('confirm your vault password: '.upper()).strip()
            count-=1
            if count==0:
                print('too many attempts try again later'.upper())
                exit()
        secretPhrase = getpass('set your secret phrase: '.upper()).strip()
        conf_secretPhrase=getpass('confirm your secret phrase: '.upper()).strip()
        count=3
        while conf_secretPhrase!=secretPhrase:
            print(f'secret phrase doesnt match please try again you have {count} more attempts'.upper())
            conf_secretPhrase=getpass('confirm your secret phrase: '.upper()).strip()
            count-=1
            if count==0:
                print('too many attempts try again later'.upper())
                break 
        else:
            print('answer the following emergency questions'.upper())
            security_info_dict=securityQuiz()
            security_info_dict.update({'secretPhrase':secretPhrase})
            security_info_dict.update({vault_user_name:vault_pass})
            git_info_dict = gitInfo()
            security_info_dict.update(git_info_dict)
            cls.personalinfodict.update(security_info_dict)
            lock(cls.personalinfodict,PERSONAL_INFO_FILE)
            print('account succssefully created!'.upper()) 
        return True 

    @classmethod
    def act(cls):
        print(f'olaa, {cls.username} welcome to your vault'.upper())
        while True:
            action_choices = ['create','retrieve','list',"exit","clear"]
            activity_choices = ['email','account',"exit","clear",cls.personalinfodict.get("secretPhrase"),"web3","file"]
            activity_choice=input("email | account | web3 | file | clear | exit'? ".upper()).lower()
            while activity_choice not in activity_choices:
                print('invalid input'.upper())
                
                activity_choice=input("email | account | web3 | file | clear | exit'? ".upper()).lower()
            if activity_choice == 'email':
                while True:

                    action_choice = input('Would you like to create | retrieve | list emails | exit? '.upper()).lower()
                    
                    while action_choice not in action_choices:
                        print('invalid input'.upper())
                        action_choice = input('Would you like to create | retrieve | list emails? '.upper()).lower()
                    if action_choice =='retrieve':
                        mail_address = input('Enter the e-mail address: '.upper())
                        value=cls.passwd_dict.get(mail_address,'invalid account or username')
                        if value == 'invalid account or username':
                            print(value.upper())
                        else:
                            pyperclip.copy(value)    
                            print(f'Your "{mail_address}" password has been copied to clipboard')    

                    elif action_choice == "create":
                        email_address = input('Enter the e-mail address: '.upper()).strip()
                        password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        while password_choice not in ['a','g']:
                            print('invalid input'.upper())
                            password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        if password_choice=='g':
                            password = password_generator()
                        elif password_choice == 'a':
                            password = create_own_pass()    
                        cls.passwd_dict.update({email_address:password})  
                        pyperclip.copy(password)       
                        print('your password has been copied to clipboard'.upper())   
                        lock(cls.passwd_dict,PASSWD_FILE)
                    elif action_choice == "list":
                        email_list=[i for i in cls.passwd_dict.keys() if " " not in i]
                        if email_list:
                            print(*email_list,sep="\n")
                        else:
                            print("No emails available")    
                    elif action_choice == "exit":
                        clear_console()
                        break
            elif activity_choice == "account":
                while True:
                    action_choice = input('Would you like to create | retrieve | list accounts | exit? '.upper()).lower()
                    while action_choice not in action_choices:
                        print('invalid input'.upper())
                        action_choice = input('Would you like to create | retrieve | list accounts? '.upper()).lower()
                    if action_choice == "retrieve":
                        acc=input('Enter the a/c: '.upper())
                        username=input('enter your username: '.upper())
                        bio=acc+' '+username
                        value=cls.passwd_dict.get(bio,'invalid account or username')
                        if value == 'invalid account or username':
                            print(value.upper())
                        else:
                            pyperclip.copy(value)    
                            print(f'Your "{acc}" password for "{username}" has been copied to clipboard')
                    elif action_choice == "create":
                        acc=input('Enter the a/c: '.upper()).strip()
                        username=input('enter your username: '.upper()).strip()
                        bio=acc+' '+username

                        password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        while password_choice not in ['a','g']:
                            print('invalid input'.upper())
                            password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                        if password_choice=='g':
                            password = password_generator()
                        elif password_choice == 'a':
                            password = create_own_pass()    
                        cls.passwd_dict.update({bio:password})  
                        pyperclip.copy(password)       
                        print('your password has been copied to clipboard'.upper())   
                        lock(cls.passwd_dict,PASSWD_FILE)
                    elif action_choice == "list":
                        accounts_list=[i for i in cls.passwd_dict.keys() if " " in i]
                        if accounts_list:
                            print(*accounts_list,sep="\n")
                        else:
                            print("No accounts available")   
                    elif action_choice == "exit":
                        clear_console()
                        break         
            elif activity_choice == "web3":
                file_action_choices = ['wallet',"project"]
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
                               
                            bio=app_name+' '+wallet_name + ' ' +wallet_email
                            value=cls.walletinfodict.get(bio,'invalid account or username')
                            if value == 'invalid account or username':
                                print(value.upper())
                            else:
                                pyperclip.copy(value)    
                                print(f'Your "{app_name}" "{wallet_name}" details for "{wallet_email}" have been copied to clipboard')
                        elif action_choice == "create":
                            app_name = input("enter app name: ".upper()).strip()
                            wallet_name = input("enter name of the wallet: ".upper()).strip()
                            wallet_email = input("enter email associated with wallet: ".upper()).strip()
                            bio=app_name+' '+wallet_name + " " + wallet_email

                            password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            while password_choice not in ['a','g']:
                                print('invalid input'.upper())
                                password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            if password_choice=='g':
                                password = password_generator()
                            elif password_choice == 'a':
                                password = create_own_pass() 

                            seedphrase_input_choices = ['manual','image']
                            seedphrase_input_choice = input("enter seedphrase manual | image: ".upper()).lower()
                            while seedphrase_input_choice not in seedphrase_input_choices:
                                print('invalid input'.upper())
                                seedphrase_input_choice = input("enter seedphrase manual | image: ".upper()).lower()
                            if seedphrase_input_choice == 'manual':
                                seedphrase = input('enter your seedphrases separated by "," (no spaces): '.upper()).strip()
                                seedphrase_dict = {i+1:value for i,value in enumerate(seedphrase.split(','))}
                            elif seedphrase_input_choice == 'image':
                                image_path = input('enter the path to the image: '.upper()).strip()
                                seedphrase_dict = seedphrase_ocr(image_path)

                            cls.walletinfodict.update({bio:{"password":password,"seedphrase":seedphrase_dict}})  
                            pyperclip.copy(password)       
                            print(f'your password for"{app_name}" "{wallet_name}" for email "{wallet_email}" havebeen copied to clipboard'.upper()) 
                            lock(cls.walletinfodict,WALL_FILE)  
                        elif action_choice == "list":
                            accounts_list={i.split(' ')[0] for i in cls.walletinfodict.keys()}
                            if accounts_list:
                                print(*accounts_list,sep="\n")
                            else:
                                print("No Wallets available") 

                        elif action_choice == "exit":
                            print("you web3 info has been secured".capitalize())
                            clear_console()
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
                            bio=project_name+' '+project_username + ' ' + project_email
                            value=cls.projectsinfodict.get(bio,'invalid account or username')
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
                            bio=project_name+' '+project_username + " " + project_email
                            password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            while password_choice not in ['a','g']:
                                print('invalid input'.upper())
                                password_choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                            if password_choice=='g':
                                password = password_generator()
                            elif password_choice == 'a':
                                password = create_own_pass() 

                            cls.projectsinfodict.update({bio:{"password":password,"wallet":connected_wallet}})  
                            pyperclip.copy(password)       
                            print(f'your "{project_name}" for {project_username} has been copied to clipboard'.upper()) 
                            lock(cls.projectsinfodict,PROJ_FILE)  
                        elif action_choice == "list":
                            accounts_list={i.split(' ')[0] for i in cls.projectsinfodict.keys()}
                            if accounts_list:
                                print(*accounts_list,sep="\n")
                            else:
                                print("No projects available") 
                        elif action_choice == "exit":
                            print("you web3 info has been secured".capitalize())
                            clear_console()
                            break     

            elif activity_choice == cls.personalinfodict.get("secretPhrase"):
                clear_console() 
                print('Welcome...Your secret is safe with me')
                choices = ['share','reveal','quit']
                choice=''
                while choice!='quit':
                    choice=input('would you like to share || reveal a secret(s) || quit: '.upper()).lower()
                    if choice == 'share':
                        secret = input('enter your secret: '.upper())
                        now = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                        cls.secretdict.update({now:secret})
                        lock(cls.secretdict,SECRETS_FILE)
                    elif choice == 'reveal':
                        if cls.secretdict:
                            print(cls.secretdict)  
                        else:
                            print("You have no secrets")       
                        
                    elif choice not in choices:
                        print('invalid input'.upper())    
                print('Your secerts have been secured!!'.upper())
                sleep(2.2)
                clear_console()


            # SECURING FILE FUNCTIONALITY

            elif activity_choice == 'file':
                file_action_choices = ['secure','retrieve',"list","exit",'clear',"empty"]
                zip_pass = bytes(unlock(PERSONAL_INFO_FILE).get("retrival_pass"),encoding="utf8")
                zip_file_path=FILE_VAULT_PATH
                while True:
                    file_action_choice=input("would you like to secure | retrieve | clear | empty vault | list secured files | exit: ".upper()).strip().lower()
                    while file_action_choice not in file_action_choices:
                        print("invalid input".upper())
                        file_action_choice = input("would you like to secure | retrieve | clear | list secured files | exit: ".upper()).strip().lower()
                   
                    if file_action_choice == "retrieve":
                        if os.path.exists(zip_file_path):
                            extract_folder = REPO_PATH+"\\"+FILE_EXTRACT_FOLDER_PATH
                            path_file = input("enter the name of thefile you would like to retrieve: ".upper()).strip()
                            back_to_zip = input("would you like to delete the file after accessing it? y(yes) | n(no): ".upper()).strip().lower()
                            while back_to_zip not in ['y','n']:
                                print("invalid choice")
                                back_to_zip = input("would you like to secure the file after accessing it? y(yes) | n(no): ".upper()).strip().lower()
                            if not os.path.exists(extract_folder):    
                                os.makedirs(extract_folder)
                                
                            with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
                                zip_file.setpassword(zip_pass)
                                zip_file.extract(path_file,path=extract_folder)
                                print(f"You can access the file here {extract_folder}")
                            if back_to_zip == 'y':
                                done = input("press enter to delete the file: ".upper()).strip()
                                if done == "" or done:
                                    shutil.rmtree(extract_folder)
                                    print("The file has been deleted".upper())
                        else:
                            print("the vault is empty!".upper())
                    elif file_action_choice == "secure":
                        consent_choices = ["y",'n']
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
                                        zip_file_func(folder_path= path_file,zip_file_path=zip_file_path)
                                        print(f"{os.path.basename(path_file)} has been secured".upper())
                                    except FileNotFoundError as e:
                                        print(f"an error occured: {e}")    
                                else:
                                    print("You cancelled the securing file process")
                                    clear_console()
                                    continue
                        except Exception as e:
                            print(f"an error occured: {e}")    
                            continue

                    elif file_action_choice == "list":
                        if os.path.exists(zip_file_path):
                            with pyzipper.AESZipFile(zip_file_path, 'r', compression=pyzipper.ZIP_DEFLATED) as zip_file:
                                zip_file.setpassword(zip_pass)
                                zip_file.setencryption(pyzipper.WZ_AES, nbits=128)
                                print(*[file.filename for file in zip_file.filelist],sep="\n")
                        else:
                            print("the vault is empty".upper())        

                    elif file_action_choice == "exit":
                        print("you files are secured".capitalize())
                        clear_console()
                        break

                    elif file_action_choice == 'clear':
                        clear_console()

                    elif file_action_choice == "empty":
                        if os.path.exists(zip_file_path):
                            empty_choice = input("kindly confirm your action y(yes) | n(no): ").strip().lower()
                            while empty_choice not in ['y','n']:
                                print("invalid choice")
                                empty_choice = input("kindly confirm your action y(yes) | n(no): ").strip().lower()
                            if empty_choice == 'y':
                                os.remove(zip_file_path)
                                print("the vault has been cleared!".upper())
                            else:
                                print("action cancelled!".upper())   
                        else:
                            print("Nothing to be emptied")         


            elif activity_choice == 'clear':
                clear_console()
            elif activity_choice == 'exit':
                print('Your vault has been locked'.upper())
                sleep(2.2)
                clear_console()
                break
            else:
                print('invalid input'.upper())
# Logic
def vault():
    memb = essentials.memb()
    try:
        if memb:
            essentials.act()
        elif memb==None:
            essentials.new()
            essentials.act()
    except Exception as error:
        print(f'an error occurred: {error.args}'.upper())
        return 
    finally:
        if conf_changes():
            backup()
        else:
            pass   
 
# Running
if __name__ == '__main__':
    vault()
    os.chdir(REPO_PATH)
    
    try:
        
        response = requests.get('https://www.google.com',timeout=5)
        if response.status_code == 200:
                        
            if conf_changes():
                git_push()
            else:
                print("No changes to push to GitHub.")
                            
        else:
            print('Internet access is not available'.upper())
            sleep(2.5)
    except requests.ConnectionError:
        print('No internet Connection'.upper())
        sleep(2.5)
