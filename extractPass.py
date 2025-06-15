#!/usr/bin/env python3
"""
SECURE BACKUP RETRIEVAL UTILITY
===============================
Companion script for the Secure Password Vault system.
Used to decrypt and extract local encrypted backups when the main vault is inaccessible.

This script locates and decrypts the encrypted backup file created by the main
password vault application, allowing data recovery in emergency situations.

Author: Password Vault System
Dependencies: pyzipper, getpass (built-in), platform (built-in), os (built-in)
"""

import os
import pyzipper      # For handling password-protected AES encrypted ZIP files
import getpass       # For getting current system username
import platform      # For operating system detection

# ============================================================================
# PLATFORM-SPECIFIC BACKUP LOCATION DETECTION
# ============================================================================
# Automatically detect the backup file location based on the operating system
# These paths must match the backup directory structure used by the main vault

if 'windows' in platform.platform().lower():
    # Windows backup location in user's hidden .backup directory
    zip_file_path = f'c:/Users/{getpass.getuser()}/.backup/Backup.zip'
elif 'linux' in platform.platform().lower():
    # Linux backup location in user's home hidden .backup directory  
    zip_file_path = f'/home/{getpass.getuser()}/.backup/Backup.zip'

# Target extraction directory (will be created if it doesn't exist)
extract_folder = "production1"

# ============================================================================
# BACKUP EXTRACTION FUNCTION
# ============================================================================

def extract_zip_with_password(zip_file_path, extract_folder, password):
    """
    Extract encrypted backup ZIP file using the retrieval password.
    
    This function:
    1. Verifies the backup file exists
    2. Creates extraction directory if needed
    3. Attempts to decrypt and extract the backup
    4. Provides user feedback on success/failure
    
    Args:
        zip_file_path (str): Full path to the encrypted backup ZIP file
        extract_folder (str): Directory where backup contents will be extracted
        password (bytes): Retrieval password in bytes format for decryption
        
    Returns:
        None: Function prints status messages and exits on failure
    """
    
    # Verify backup file exists before attempting extraction
    if not os.path.exists(zip_file_path):
        print('Backup does not exist!'.capitalize())
        print(f'Expected location: {zip_file_path}')
        exit()
    
    # Create extraction directory if it doesn't exist
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
        print(f'Created extraction directory: {extract_folder}')
    
    # Attempt to decrypt and extract the backup
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
            # Set the decryption password
            zip_file.setpassword(password)
            
            # Extract all contents to the target folder
            zip_file.extractall(extract_folder)
            
            print("✅ Backup successfully extracted to production1")
            print("📁 Your vault data has been restored and is ready to use")
            
    except RuntimeError as e:
        # Handle incorrect password errors
        if "Bad password" in str(e) or "password" in str(e).lower():
            print("❌ Incorrect retrieval password. Please check your password and try again.")
        else:
            print(f"❌ Decryption error: {e}")
            
    except Exception as e:
        # Handle any other extraction errors
        print(f'❌ An error occurred during extraction: {e}')
        print("💡 Possible causes:")
        print("   - Corrupted backup file")
        print("   - Insufficient disk space") 
        print("   - Permission issues")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🔓 SECURE BACKUP RETRIEVAL UTILITY")
    print("=" * 40)
    print(f"📍 Backup location: {zip_file_path}")
    print(f"📂 Extraction target: {extract_folder}")
    print()
    
    # Prompt for retrieval password (this should be the same password set 
    # during the security questions setup in the main vault application)
    password = input('🔑 Enter retrieval password to unlock backup: ').encode('utf-8')
    
    print("\n🔄 Processing backup extraction...")
    extract_zip_with_password(zip_file_path, extract_folder, password)
