
import os 
import random
import json
import hashlib

USERS_FILE = "Users.json"
def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

def generate_iban():
    country_code = "FR"
    control_key = f"{random.randint(0,99):02d}"
    bank_code = "12345"
    branch_code = "67890"
    account_number = f"{random.randint(0, 99999999999):011d}"
    return f"{country_code}{control_key}{bank_code}{branch_code}{account_number}"

def hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode()).hexdigest()