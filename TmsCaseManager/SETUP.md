# TMS-CaseManager API Project Setup Guide

## Prerequisites
- Python 3.8 or higher
- Git
- Allure CLI (for test reporting)

## Step 1: Install Python Packages
```bash
# Clone the repository
git clone <your-repo-url>
cd TMS-CaseManager

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

## Step 2: Install Allure CLI (Required for Reports)

### Windows (using scoop):
```bash
# Install scoop first (if not installed)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

### macOS:
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Allure
brew install allure
```

### Linux:
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

## Step 3: Verify Installation
```bash
# Check Python packages
behave --version
python -c "import allure_behave; print('Allure Behave installed')"

# Check Allure CLI
allure --version
```

## Step 4: Run Tests
```bash
# Run CaseManager tests
behave features/case_manager.feature

# Run TMS tests
behave features/tms.feature

# Generate Allure report
behave features/case_manager.feature --format allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## Troubleshooting
- If `allure` command not found: Make sure Allure CLI is installed separately
- If `behave` command not found: Make sure virtual environment is activated
- If import errors: Run `pip install -r requirements.txt` again
