import os
import pyzipper
import getpass

zip_file_path=f'c:/Users/{getpass.getuser()}/Favorites/Backup.zip'
extract_folder = os.getcwd()+"\\"+"production"


def extract_zip_with_password(zip_file_path, extract_folder, password):
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
        zip_file.setpassword(password)
        zip_file.extractall(extract_folder)

if __name__ == "__main__":
    password = input('Enter password to Unlock file (Hint: cuzz + favorite band): '.capitalize()).encode('utf-8')
    extract_zip_with_password(zip_file_path, extract_folder, password)
