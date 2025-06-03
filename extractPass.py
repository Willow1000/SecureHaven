import os
import pyzipper
import getpass
import platform

if 'windows' in platform.platform().lower():
    zip_file_path = f'c:Users/{getpass.getuser()}/Favorites/.backup/Backup.zip'
elif 'linux' in platform.platform().lower():
    zip_file_path =  f'/home/{getpass.getuser()}/.backup/Backup.zip'



extract_folder = "production1"


def extract_zip_with_password(zip_file_path, extract_folder, password):
    if not os.path.exists(zip_file_path):
        print('Backup does not exist!'.capitalize())
        exit()
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
        try:
            zip_file.setpassword(password)
            zip_file.extractall(extract_folder)
            print("Backup successfully extracted to production1")
        except Exception as e:
            print(f'An error occured: {e}')    

if __name__ == "__main__":
    password = input('Enter password to Unlock file: '.capitalize()).encode('utf-8')
    extract_zip_with_password(zip_file_path, extract_folder, password)
