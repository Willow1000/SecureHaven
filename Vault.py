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


FOLDER_NAME = 'production'

if os.path.exists(FOLDER_NAME):
    os.chdir(FOLDER_NAME)
else:
    os.mkdir(FOLDER_NAME)
    os.chdir(FOLDER_NAME) 
# Defining constants

# File name constants
PASSWD_FILE = os.getcwd()+"\\"+'passengers.json'
SECRETS_FILE=os.getcwd()+"\\"+'essentials.json'
CARS_FILE = os.getcwd()+"\\"+'cars.txt'
PERSONAL_INFO_FILE = os.getcwd()+'\\'+'itenerary.json'
# Backup constants
BASE_DIR = 'C:\\Users'

BACKUP_DIR=f'c:/Users/{pa.getuser()}/Favorites'
FOLDER_PATH = "Backup"
REPO_PATH = os.getcwd()+"\\"+"../"
ZIP_FILE_PATH = "Backup.zip"
ZIP_PASS = b"i'll never forget"

PASSWD_FILE_NAME = 'passengers.json'
SECRETS_FILE_NAME='essentials.json'
CARS_FILE_NAME = 'cars.txt'
PERSONAL_INFO_FILE_NAME='itenerary.json'

# Github constants

COMMIT_MESSAGE = "Made some changes"
BRANCH = 'main'
FILES_TO_TRACK = 'production'


# Setting font color to green
os.system('color 2')


# Subordinate Functions  
def conf(file=None, directory=None, target_dir='./'):
    if file:
        return os.path.exists(os.path.join(target_dir, file))
    elif directory:
        return os.path.exists(os.path.join(target_dir, directory))
    return False
def unlock(file):
    json_list=[]
    if conf(file=PASSWD_FILE):
        json_list.append(PASSWD_FILE)
    if PASSWD_FILE in json_list: 
        with open(CARS_FILE,'rb') as f:
            key=f.read()
        with open(file,'rb') as f:
            cont=f.read()
        cont_decr=json.loads(Fernet(key).decrypt(cont).decode())
        return cont_decr
    else:
        return 
def lock(dictionary,file):
    if conf(file=CARS_FILE) == False:
        with open(CARS_FILE,'wb') as f:
            key = Fernet.generate_key()
            f.write(key)
        cont=json.dumps(dictionary).encode('utf-8')
        cont_encr=Fernet(key).encrypt(cont)
        with open(file,'wb') as f:
            f.write(cont_encr)
     
    elif conf(file=CARS_FILE):
        with open(CARS_FILE,'rb') as f:
            key=f.read()
        cont=json.dumps(dictionary).encode('utf-8')
        cont_encr=Fernet(key).encrypt(cont)
        with open(file,'wb') as f:
            f.write(cont_encr)
            
    else:
        return        

def backup():

    if conf(directory=FOLDER_PATH):
        shutil.copy(PASSWD_FILE, os.path.join(FOLDER_PATH, PASSWD_FILE_NAME))
        shutil.copy(CARS_FILE, os.path.join(FOLDER_PATH, CARS_FILE_NAME))
        shutil.copy(SECRETS_FILE, os.path.join(FOLDER_PATH, SECRETS_FILE_NAME))
        shutil.copy(PERSONAL_INFO_FILE, os.path.join(FOLDER_PATH, PERSONAL_INFO_FILE_NAME))
    else:
        os.makedirs(FOLDER_PATH, exist_ok=True)
        shutil.copy(PASSWD_FILE, FOLDER_PATH)
        shutil.copy(CARS_FILE, FOLDER_PATH)
        shutil.copy(SECRETS_FILE, FOLDER_PATH)
        shutil.copy(PASSWD_FILE, FOLDER_PATH)
    with pyzipper.AESZipFile(ZIP_FILE_PATH, 'w', compression=pyzipper.ZIP_DEFLATED) as zip_file:
        zip_file.setpassword(ZIP_PASS)
        zip_file.setencryption(pyzipper.WZ_AES, nbits=128)  
        for root, dirs, files in os.walk(FOLDER_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip if it's a regular file (not a directory)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, os.path.relpath(file_path, FOLDER_PATH))   
    shutil.rmtree(FOLDER_PATH)                
    if os.path.exists(BACKUP_DIR+"\\"+ZIP_FILE_PATH):
        os.remove(BACKUP_DIR+"\\"+ZIP_FILE_PATH)     
        shutil.move(ZIP_FILE_PATH,BACKUP_DIR)
    else:
        shutil.move(ZIP_FILE_PATH,BACKUP_DIR)
                     


def securityQuiz():
    city=getpass('in which city were you born? '.upper()).lower()
    color=getpass('what is your favorite colour? '.upper()).lower()
    nick_name=getpass('what was your childhood nickname? '.upper()).lower()
    securityQuizDict = {'city':city,'color':color,'nick_name':nick_name}
    return securityQuizDict

def gitInfo():
    gitUsername = getpass('Enter your github username: '.upper())
    gitEmail = getpass('enter the email linked to your github account: '.upper())
    gitRepoLink = getpass('enter the link to the repository that will store your files: '.upper())
    githubnInfoDict = {"gitUsername":gitUsername,"gitEmail":gitEmail,"gitRepoLink":gitRepoLink}
    return githubnInfoDict 

personalinfodict = unlock(PERSONAL_INFO_FILE)
EMAIL = personalinfodict.get('gitEmail')
USERNAME = personalinfodict.get('gitUsername')
REPO_LINK = personalinfodict.get('gitRepoLink')
def git_push(commit_message=COMMIT_MESSAGE, branch=BRANCH, email = EMAIL, username=USERNAME, repo_link = REPO_LINK, files_to_track=FILES_TO_TRACK,folder_name = FOLDER_NAME):
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

        os.chdir(REPO_PATH)

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
                subprocess.run(["rmdir", "/s", "/q", ".git"], check=True, shell=True)
                print("🗑️ .git directory removed successfully")
        else:
            try:
                # Mark the repo as safe
                subprocess.run(["git", "config", "--add", "safe.directory", REPO_PATH], check=True)
                #Stage Files
                subprocess.run(['git', 'commit', '-am', commit_message], check=True)
                #Push Changes
                subprocess.run(['git', 'push', '-u', 'origin', branch], check=True)
                print("✅ Changes pushed to GitHub successfully.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Git command failed: {e}")
                print("⚠️ Removing .git directory to reset the repository...")
                subprocess.run(["rmdir", "/s", "/q", ".git"], check=True)
                print("🗑️ .git directory removed successfully")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        subprocess.run(["rmdir", "/s", "/q", ".git"], check=True, shell=True)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        subprocess.run(["rmdir", "/s", "/q", ".git"], check=True, shell=True)

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

# Main 
class essentials():   
    json_list=[]
    if conf(file=PASSWD_FILE_NAME):
        json_list.append(PASSWD_FILE_NAME)
    if PASSWD_FILE_NAME in json_list:
        passwd_dict=unlock(PASSWD_FILE)
        secretdict = unlock(SECRETS_FILE)
        personalinfodict = unlock(PERSONAL_INFO_FILE)
    else:
        passwd_dict={}
        secretdict={}
        personalinfodict = {}
    username=''    
   
    @classmethod  
    def memb(cls):
        passwd_dict=cls.passwd_dict
        personalinfodict = cls.personalinfodict
        json_list=cls.json_list
        if conf(file=PASSWD_FILE_NAME):
            json_list.append(PASSWD_FILE_NAME)
        if PASSWD_FILE_NAME in json_list: 
            username=input('enter your vault username: '.upper())
            usernamecount=3
            while username not in personalinfodict.keys() and usernamecount>0:
                print(f'incorrect username {usernamecount} more attempts remaining'.upper())
                username=input('enter your vault username: '.upper())
                usernamecount-=1
                if usernamecount==0:
                    print('maximum number of attempts reached'.upper())
                    return False
            vault_password=getpass('enter your vault password: '.upper())
            passwdcount=3
           
            while vault_password!=personalinfodict.get(username) and passwdcount>0:
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
                            personalinfodict.pop(username)
                            personalinfodict.update({username:new_passwd})
                            print('password was reset succssefuly!!'.upper())
                            return True
                    else:
                        print('wrong details!! please try again later'.upper())
                        return False
            else:
                return True
    @classmethod            
    def new(cls):
        personalinfodict=cls.personalinfodict
        vault_user_name=input('enter your vault username: '.upper())
        cls.username = vault_user_name
        vault_pass = getpass('set your vault password: '.upper())
        conf_vault_pass=getpass('confirm your vault password: '.upper())
        count=3
        while conf_vault_pass!=vault_pass:
            print(f'password doesnt match please try again you have {count} more attempts'.upper())
            conf_vault_pass=getpass('confirm your vault password: '.upper())
            count-=1
            if count==0:
                print('too many attempts try again later'.upper())
                break 
        secretPhrase = getpass('set your secret phrase: '.upper())
        conf_secretPhrase=getpass('confirm your secret phrase: '.upper())
        count=3
        while conf_secretPhrase!=secretPhrase:
            print(f'secret phrase doesnt match please try again you have {count} more attempts'.upper())
            conf_secretPhrase=getpass('confirm your secret phrase: '.upper())
            count-=1
            if count==0:
                print('too many attempts try again later'.upper())
                break 
        else:
            print('answer the following emergency questions'.upper())
            [city,color,nick_name]=securityQuiz().values()
            [gitUsername,gitEmail,gitRepoLink] = gitInfo().values()

            personalinfodict.update({vault_user_name:vault_pass,'nickname':nick_name,'city':city,'color':color,"secretPhrase":secretPhrase,'gitUsername':gitUsername,'gitEmail':gitEmail,'gitRepoLink':gitRepoLink})
            lock(personalinfodict,PERSONAL_INFO_FILE)
            print('account succssefully created!'.upper()) 
        return True 

    @classmethod
    def act(cls):
        passwd_dict=cls.passwd_dict
        secretdict=cls.secretdict
        print(f'olaa, {cls.username} welcome to your vault'.upper())
        choice = ''
        while True:
            choice=input("would you like to 'retrieve' a password? ||'create' a new one? || 'exit' ? ".upper()).upper()
            if choice =='retrieve'.upper():
                acc_choices=['ACCOUNT','EMAIL']
                account_type = input("'Email' address or 'account?' ".upper()).upper()
                while account_type not in acc_choices:
                    print('invalid input'.upper())
                    account_type = input("'Email' address or 'account?' ".upper()).upper()
                if account_type == 'account'.upper():
                    acc=input('Enter the a/c: '.upper())
                    username=input('enter your username: '.upper())
                    bio=acc+' '+username
                    value=passwd_dict.get(bio,'invalid account or username')
                    if value == 'invalid account or username':
                        print(value.upper())
                    else:
                        pyperclip.copy(value)    
                        print(f'Your "{acc}" password for "{username}" has been copied to clipboard')
                elif account_type == 'Email address'.upper() or account_type=='email'.upper():
                    mail_address = input('Enter the e-mail address: '.upper())
                    bio = mail_address
                    value=passwd_dict.get(bio,'invalid account or username')
                    if value == 'invalid account or username':
                        print(value.upper())
                    else:
                        pyperclip.copy(value)    
                        print(f'Your "{bio}" password has been copied to clipboard')        
            elif choice=='create'.upper():
                choice=input("enter 'a' if you already have a password in mind or 'g' for us to generate one for you: ".upper()).lower()
                if choice=='g':
                    password = password_generator()
                elif choice == 'a':
                    password=getpass('enter the password: '.upper())
                    conf_pass=getpass('confirm your password: '.upper())
                    count=3
                    while conf_pass !=password:
                        print(f'passwords do not match,please try again {count} more attempts remaining'.upper())
                        password=getpass('enter the password: '.upper())
                        conf_pass=getpass('confirm your password: '.upper())
                        count-=1
                        if count==0:
                            print('maximum number of attempts exceeded,kindly try again later'.upper())
                            break  
                acc_choices=['ACCOUNT','EMAIL']
                    
                account_type = input("'Email' address or 'account'? ".upper()).upper()
                while account_type not in acc_choices:
                    print('invalid input'.upper())
                    account_type = input("'Email' address or 'account'? ".upper()).upper()   
                if account_type == 'account'.upper():
                    account=input('enter name of a/c: '.upper())
                    username=input('enter your username: '.upper())
                    bio=account+' '+username
                elif account_type == 'email address'.upper() or account_type=='email'.upper():
                    bio = input('Enter the e-mail address: '.upper())

                passwd_dict.update({bio:password})     
                pyperclip.copy(password)       
                print('your password has been copied to clipboard'.upper())    
            elif choice == passwd_dict.get("secretPhrase",'coffee').upper():
                subprocess.run(["cls"],shell=True)
                print('Welcome...Your secret is safe with me')
                choices = ['share','reveal','quit']
                while choice!='quit':
                    choice=input('would you like to share || reveal a secret(s) || quit: '.upper()).lower()
                    if choice == 'share':
                        secret = input('enter your secret: '.upper())
                        now = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                        secretdict.update({now:secret})
                    elif choice == 'reveal':
                        secretdict = unlock(SECRETS_FILE)   
                        print(secretdict)     
                        
                    elif choice not in choices:
                        print('invalid input'.upper())    
                print('Your secerts have been secured!!'.upper())
                sleep(2.2)
                os.system('cls')
                  
            elif choice == 'exit'.upper():
                lock(secretdict,SECRETS_FILE)
                lock(passwd_dict,PASSWD_FILE)
                print('Your vault has been locked'.upper())
                sleep(2.2)
                os.system('cls')
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
        backup()
# Running
if __name__ == '__main__':
    vault()
    try:
        response = requests.get('https://www.google.com',timeout=5)
        if response.status_code == 200:
                git_push()
        else:
            print('Internet access is not available'.upper())
            sleep(2.5)
    except requests.ConnectionError:
        print('No internet Connection'.upper())
        sleep(2.5)


