# 🔐 SecureHaven Password Vault

A comprehensive, military-grade encrypted password management system designed for security professionals, cryptocurrency enthusiasts, and privacy-conscious users. Features advanced encryption, Web3 wallet management, and intelligent backup systems.

## ✨ Key Features

• **🛡️ Military-Grade Security** - XSalsa20Poly1305 encryption with Argon2id key derivation
• **💰 Web3 Integration** - Cryptocurrency wallet management with OCR seed phrase extraction
• **🔄 Intelligent Backup** - Automated local and Git-based cloud synchronization
• **📁 File Vault** - Encrypt and store sensitive documents and folders
• **🔍 Universal Search** - Quick access to email, account, and wallet credentials
• **🤫 Secret Management** - Timestamped personal secret storage with additional protection
• **🌐 Cross-Platform** - Full Windows and Linux support with mobile-ready architecture

## 🎯 Perfect For

- Security professionals managing multiple client credentials
- Cryptocurrency traders with multiple wallets and seed phrases
- Developers needing secure storage for API keys and certificates
- Privacy enthusiasts requiring offline-first password management
- Teams needing secure credential sharing with audit trails

## 🔒 Security Architecture

Built on proven cryptographic primitives with a zero-trust security model. All data is encrypted locally before storage, ensuring your secrets remain private even if storage is compromised.

**Encryption Stack:**
- XSalsa20 stream cipher for data encryption
- Poly1305 for authenticated encryption
- Argon2id for password-based key derivation
- Cryptographically secure random number generation

## 🚀 Quick Start

```bash
# Install dependencies
pip install pyzipper requests pyperclip pynacl paddleocr

# Run the vault
python password_vault.py
See Installation Guide for detailed setup instructions.

📊 Project Stats
PythonEncryptionPlatformLicense

# 🔐 Secure Password Vault

A comprehensive, military-grade encrypted password management system with advanced security features, backup capabilities, and multi-platform support. Built with Python and designed for maximum security and usability.

## 🚀 Features

### Core Security Features
- **🔒 AES-256 Encryption**: All data protected with industry-standard encryption
- **🛡️ Argon2id Key Derivation**: Memory-hard password hashing resistant to attacks
- **🔑 Master Password Protection**: Single password secures entire vault
- **❓ Security Questions**: Multi-factor account recovery system
- **👁️ Secure Input**: Hidden password entry prevents shoulder surfing
- **🎲 Cryptographically Secure RNG**: High-entropy random number generation

### Password Management
- **📧 Email Account Storage**: Dedicated email credential management
- **👤 General Account Management**: Universal account/service credential storage
- **🔐 Secure Password Generation**: Customizable strong password creation
- **📋 Clipboard Integration**: Automatic credential copying with security
- **🔍 Quick Search & Retrieval**: Fast access to stored credentials
- **📊 Password Strength Analysis**: Built-in password validation

### Cryptocurrency & Web3
- **💰 Wallet Management**: Secure cryptocurrency wallet credential storage
- **🌱 Seed Phrase Protection**: OCR extraction and encrypted seed phrase storage
- **🔗 Project-Wallet Linking**: Connect Web3 projects to associated wallets
- **📱 Multi-Wallet Support**: Organize multiple wallets per application
- **🎯 Smart Contract Integration**: Store contract addresses and credentials

### Advanced Features
- **🤫 Secret Storage**: Timestamped personal secret management
- **📁 File Vault**: Encrypt and store sensitive files and folders
- **🔄 Automatic Backup**: Intelligent local and remote backup system
- **🌐 Git Integration**: Seamless GitHub synchronization
- **🖥️ Cross-Platform**: Full Windows and Linux support
- **📱 Mobile-Ready**: Platform-agnostic design for future mobile support

## 🔐 Security Architecture

### Encryption Stack
┌─────────────────────────────────────┐ │ User Interface Layer │ ├─────────────────────────────────────┤ │ Application Logic Layer │ ├─────────────────────────────────────┤ │ 🔐 XSalsa20Poly1305 Encryption │ │ 🔑 Argon2id Key Derivation │ │ 🎲 Cryptographically Secure RNG │ ├─────────────────────────────────────┤ │ Encrypted File Storage │ ├─────────────────────────────────────┤ │ 🛡️ Operating System Security │ └─────────────────────────────────────┘


### Cryptographic Specifications
- **Symmetric Encryption**: XSalsa20 stream cipher with Poly1305 MAC
- **Key Derivation**: Argon2id with moderate memory/CPU parameters
- **Salt Generation**: 16-byte cryptographically secure random salt per file
- **Nonce Management**: 24-byte unique nonce per encryption operation
- **Key Size**: 256-bit encryption keys
- **Authentication**: Authenticated encryption prevents tampering

## 📦 Installation

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows 10+ or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 512MB available (for Argon2id operations)
- **Storage**: 100MB for application + storage for encrypted data
- **Network**: Internet connection for Git backup functionality

### Dependencies Installation

```bash
# Core dependencies
pip install pyzipper requests pyperclip pynacl

# OCR functionality (optional, for seed phrase extraction)
pip install paddleocr

# Windows-specific enhancements (optional)
pip install pywin32
Alternative Installation Methods
Using requirements.txt

pip install -r requirements.txt
Using Conda

conda install -c conda-forge pynacl pyzipper requests pyperclip
Development Installation

git clone <repository-url>
cd secure-password-vault
pip install -e .
🚀 Quick Start
First-Time Setup (5 minutes)
Download and Run


python password_vault.py
Create Your Vault

Choose a strong master password (12+ characters)
Set up security questions for recovery
Configure GitHub credentials for backup
Your First Password

Select "Email Management" from main menu
Add your first email account credentials
Test retrieval to confirm everything works
Daily Workflow

# Start the vault
python password_vault.py

# Quick access pattern:
# 1. Enter master password
# 2. Navigate to desired section
# 3. Retrieve/add/modify credentials
# 4. Automatic backup on changes
📖 Detailed Usage
🔐 Initial Vault Setup
Master Password Creation
Your master password is the key to your entire vault. Choose wisely:

Minimum 12 characters (20+ recommended)
Mix of uppercase, lowercase, numbers, symbols
Avoid personal information (names, dates, addresses)
Use passphrase method: "Coffee$Makes@Me#Happy2024!"
Security Questions Configuration
Set up 3 security questions for account recovery:

Birth City: City where you were born
Favorite Color: Your favorite color
Childhood Nickname: What you were called as a child
Important: Remember these answers exactly as entered (case-sensitive)

GitHub Backup Setup
Configure automatic cloud backup:

Create Private Repository: On GitHub, create a private repository
Generate Personal Access Token: GitHub Settings > Developer settings > Personal access tokens
Configure Credentials: Enter username, email, and repository URL
📧 Email Management
Store and manage email account credentials securely.

Adding Email Accounts
Main Menu > Email Management > Add New Email
Information Stored:

Email address
Password
Account provider (Gmail, Outlook, etc.)
Recovery information
Two-factor authentication backup codes
Password Generation
The vault includes a secure password generator:

Length: 8-128 characters
Character Sets: Uppercase, lowercase, numbers, symbols
Exclusions: Ambiguous characters (0, O, l, 1)
Patterns: Pronounceable or completely random
👤 Account Management
Universal credential storage for any service or application.

Account Categories
Social Media: Facebook, Twitter, Instagram, etc.
Financial: Banking, investment, credit card portals
Work: Corporate accounts, VPNs, development tools
Entertainment: Streaming services, gaming platforms
Shopping: E-commerce sites, loyalty programs
Organizational Features
Service Name: Platform or application name
Username/Email: Login identifier
Password: Encrypted password storage
URL: Direct link to login page
Notes: Additional context or instructions
💰 Cryptocurrency & Web3 Management
Wallet Storage
Securely manage cryptocurrency wallet credentials:

Wallet Information:

Application: MetaMask, Trust Wallet, Ledger, etc.
Wallet Name: Custom identifier
Email: Associated email address
Password: Wallet access password
Seed Phrase: 12/24-word recovery phrase (encrypted)
OCR Seed Phrase Extraction
Extract seed phrases from images automatically:

Capture Image: Photo of handwritten or printed seed phrase
OCR Processing: Automatic text extraction using PaddleOCR
Verification: Manual review and correction
Encryption: Secure storage with wallet credentials
Web3 Project Management
Link projects to their associated wallets:

Project Details:

Project Name: DeFi protocol, NFT collection, etc.
Website URL: Official project website
Connected Wallet: Associated wallet from vault
Contract Addresses: Smart contract information
Notes: Project-specific information
🤫 Secret Management
Store personal secrets with timestamp tracking.

Secret Categories
Personal Information: SSN, passport numbers, etc.
Recovery Codes: Backup codes for important accounts
Family Information: Important family details
Legal Documents: Reference numbers, legal information
Medical Information: Insurance numbers, medical IDs
Access Control
Secret Phrase: Additional password for secret access
Timestamp Tracking: When secrets were added/accessed
Reveal Protection: Confirms intent before displaying secrets
📁 File Vault
Encrypt and store sensitive files and folders.

Supported Operations
Folder Encryption: Encrypt entire directories
File Extraction: Decrypt and access stored files
Secure Deletion: Remove files after access
Password Protection: Separate password for file vault
Use Cases
Tax Documents: Annual tax returns and supporting documents
Legal Papers: Contracts, wills, important agreements
Personal Photos: Sensitive or private photographs
Identity Documents: Scanned copies of ID, passport, etc.
Financial Records: Bank statements, investment documents
📁 File Structure
password-vault/
├── password_vault.py          # Main application
├── backup_recovery.py         # Emergency recovery utility
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── production/                # Main vault directory
│   ├── passengers.json        # Email credentials (encrypted)
│   ├── essentials.json        # Personal secrets (encrypted)
│   ├── itenerary.json         # User settings (encrypted)
│   ├── locus.json            # Wallet information (encrypted)
│   ├── memento.json          # Project credentials (encrypted)
│   ├── Vault.zip             # Encrypted file storage
│   └── Backup/               # Local backup staging
├── .git/                     # Git repository (if enabled)
└── docs/                     # Additional documentation
    ├── SECURITY.md           # Security best practices
    ├── CHANGELOG.md          # Version history
    └── TROUBLESHOOTING.md    # Common issues and solutions
Hidden System Directories
Windows
C:/Users/[username]/.backup/   # Encrypted backup storage
Linux
/home/[username]/.backup/      # Encrypted backup storage
🔄 Backup & Recovery
Automatic Backup System
The vault implements a multi-layered backup strategy:

Local Backup
Trigger: Automatic on any data change
Location: Hidden system directory
Encryption: AES-256 with retrieval password
Frequency: Real-time change detection
Git Backup
Trigger: After successful local backup
Location: Private GitHub repository
Disclaimer: repo should be private and account should have 2FA authentication coupled with Authenticator App
Security: Repository isolation, safe directory configuration
Frequency: Synchronized with local backup
Recovery Procedures
Using Backup Recovery Script

python backup_recovery.py
Locate Backup: Automatically finds encrypted backup
Enter Retrieval Password: Password from security questions setup
Extract Files: Restores to production1/ directory
Verify Integrity: Check extracted files before use
Manual Recovery Steps
Clone Repository: git clone [your-repo-url]
Navigate to Directory: cd [repository-name]/production
Run Main Application: python password_vault.py
Enter Credentials: Use master password and security questions
Emergency Recovery
If all else fails:

Answer Security Questions: Recreate access using security questions
GitHub Repository: Clone from last known good backup
Local Backup Search: Check system backup directories manually
⚠️ Security Considerations
Critical Security Settings
Change Default Master Password
⚠️ CRITICAL: The script contains a hardcoded password PASSWORD = "SOME"

Before first use, change this to a secure value:


PASSWORD = "YourSecureMasterPasswordHere123!"
GitHub Repository Security
Use Private Repositories Only: Never use public repositories
Enable Two-Factor Authentication: Protect your GitHub account
Use Personal Access Tokens: Instead of passwords for Git operations
Regular Token Rotation: Change access tokens periodically
System Security
Full Disk Encryption: Enable BitLocker (Windows) or LUKS (Linux)
Antivirus Software: Keep real-time protection enabled
System Updates: Maintain current OS security patches
User Account Control: Don't run as administrator unless necessary
Best Practices
Password Management
Unique Master Password: Never reuse your vault master password
Regular Password Changes: Update critical account passwords regularly
Password Strength: Use vault's password generator for new accounts
Backup Security Questions: Store answers securely offline
Operational Security
Private Environment: Only access vault on trusted, private devices
Network Security: Avoid public WiFi for vault operations
Screen Privacy: Be aware of shoulder surfing
Session Management: Always exit vault completely when finished
Backup Security
Test Recoveries: Regularly test backup restoration procedures
Multiple Locations: Consider additional backup locations
Access Control: Limit who knows about backup locations/passwords
Retention Policy: Keep multiple backup generations
🐛 Troubleshooting
Common Issues and Solutions
Installation Problems
"Module not found" errors


# Install missing dependencies
pip install --upgrade pip
pip install pyzipper requests pyperclip pynacl
Permission denied errors (Linux)


# Install with user permissions
pip install --user [package-name]
# Or use sudo for system-wide installation
sudo pip install [package-name]
Runtime Issues
"Backup does not exist" error

Cause: No backup has been created yet
Solution: Create initial backup by making changes to vault
Prevention: Run vault at least once before attempting recovery
"Incorrect password" errors

Master Password: Verify caps lock, special characters
Retrieval Password: Use exact password from security questions setup
Git Credentials: Check GitHub username/token combination
OCR extraction failures

Image Quality: Ensure clear, high-contrast seed phrase images
Lighting: Use good lighting conditions for photography
Text Size: Ensure seed phrase text is large enough for OCR
Language: OCR optimized for English text
Git Integration Issues
"Repository not found" errors


# Verify repository URL and access permissions
git ls-remote [repository-url]
"Authentication failed" errors

Personal Access Token: Verify token is valid and has repo permissions
Username: Ensure correct GitHub username
Repository Access: Confirm you have write access to repository
"Safe directory" warnings


# Add directory to Git safe directories
git config --global --add safe.directory [vault-directory]
Performance Optimization
Large Vault Performance
File Organization: Keep vault files under 100MB each
Backup Frequency: Adjust backup triggers for large datasets
Memory Usage: Monitor system memory during Argon2id operations
Network Optimization
Git Operations: Use SSH keys instead of HTTPS for better performance
Backup Timing: Schedule backups during off-peak hours
Connection Stability: Ensure stable internet for Git operations
Getting Help
Documentation Resources
Security Guide: See docs/SECURITY.md for advanced security topics
Change Log: Check docs/CHANGELOG.md for version-specific issues
Troubleshooting: Detailed solutions in docs/TROUBLESHOOTING.md
Community Support
GitHub Issues: Report bugs and feature requests
Security Concerns: Contact maintainers directly for security issues
Feature Requests: Submit enhancement ideas through issues
🔮 Roadmap & Future Features
Planned Enhancements
Version 2.0 - Multi-User Support
Family Vaults: Shared credential management
Permission Systems: Role-based access control
Audit Logging: Track access and modifications
Version 2.1 - Enhanced Security
Hardware Security Keys: FIDO2/WebAuthn integration
Biometric Authentication: Fingerprint and face recognition
Zero-Knowledge Architecture: Client-side encryption only
Version 2.2 - Platform Expansion
Mobile Applications: iOS and Android native apps
Browser Extensions: Chrome, Firefox, Safari integration
API Access: RESTful API for third-party integration
Version 3.0 - Enterprise Features
Team Management: Organization credential sharing
Compliance Tools: SOX, HIPAA, GDPR compliance features
Advanced Reporting: Security analytics and insights
Contributing Guidelines
Development Setup

# Clone repository
git clone [repository-url]
cd secure-password-vault

# Create virtual environment
python -m venv vault-env
source vault-env/bin/activate  # Linux/Mac
vault-env\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
Code Contribution Process
Fork Repository: Create personal fork on GitHub
Create Branch: Feature-specific branch from main
Implement Changes: Follow existing code style
Add Tests: Ensure test coverage for new features
Submit Pull Request: Detailed description of changes
Security Review Process
Security-Critical Changes: Require additional review
Cryptographic Modifications: Expert cryptographer review
Dependency Updates: Security impact assessment
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Third-Party Licenses
PyNaCl: Apache License 2.0
PyZipper: MIT License
Requests: Apache License 2.0
PaddleOCR: Apache License 2.0
⚠️ Disclaimer
This software is provided "as-is" without any express or implied warranties. Users are responsible for:

Security: Properly securing master passwords and backup materials
Compliance: Ensuring compliance with local laws and regulations
Data Protection: Maintaining independent backups of critical information
Risk Assessment: Understanding and accepting security risks
Important Notices
Beta Software: This is beta software; test thoroughly with non-critical data first
Backup Responsibility: Users are solely responsible for backup and recovery
Security Updates: Keep software updated with latest security patches
Legal Compliance: Ensure compliance with applicable laws and regulations
🔐 Secure Password Vault - Protecting Your Digital Life

Built with security, designed for usability, trusted by professionals.
