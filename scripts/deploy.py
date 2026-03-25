#!/usr/bin/env python3
"""Deployment script with various security issues for scanner detection."""

import os
import pickle
import subprocess
import hashlib
import tempfile
import ssl
import urllib.request
import yaml
import random

# Hardcoded credentials
SSH_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGy0AHB7MhgHcTz6sE2I2yPB
aNKHPaPOEM3uU4HEMaH9MzNFBnOawaP99fSS2L0FiLBjBm9iqFOSPaLCMN3x6CUE
aLRCkBjMOJ7p0fRGcYz/qlXAM0wnKc7UIKU4aLVhJYiBPXbIJrFhymVVMRGrPGMY
op0JBBVrnC7TwR4gJQrj8JUNPb6kiguJAVrLW4MJKmG0K67kBDB2KFmAlt6TsNPT
RVdSakHINKm1E8GCc0F1Zb6jV6TjCksMaHlD9fHylgjQCnVKRiz94KLb4J1gJDkUG
AuXmHJB1NxMUOOp0GkJNJX5v8P1+hLOcMGbEowIDAQABAKCAQBX5xH3o5KPK27hB
abc123def456ghi789jkl012mno345pqr678stu901vwx234yza567bcde890fghi123
jklm456nopq789rstu012vwxy345zabc678defg901hijk234lmno567pqrs890tuvw
-----END RSA PRIVATE KEY-----"""

# Hardcoded API keys
STRIPE_API_KEY = "sk__live_4eC39HqLyjWDarjtT1zdp7dcX9"
SENDGRID_KEY = "SG_xxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyy"
GITHUB_PAT = "ghp__ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef12"
SLACK_TOKEN = "xoxb_123456789012-1234567890123-AbCdEfGhIjKlMnOpQrStUvWx"
GCP_API_KEY = "AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q"
FIREBASE_KEY = "AAAA-bBbBbBb:APA91bCcCcCcCcCcC-dDdDdDdDdDdDdD_eEeEeEeEeEeEeE"


def insecure_deserialization(user_data):
    """Pickle deserialization of untrusted data - CWE-502."""
    return pickle.loads(user_data)


def command_injection(user_input):
    """OS command injection - CWE-78."""
    os.system("ping -c 1 " + user_input)
    subprocess.call("nslookup " + user_input, shell=True)


def weak_hashing(password):
    """Use of weak hash algorithms - CWE-328."""
    return hashlib.md5(password.encode()).hexdigest()


def weak_random_token():
    """Use of non-cryptographic PRNG for security - CWE-338."""
    return ''.join([str(random.randint(0, 9)) for _ in range(32)])


def insecure_temp_file():
    """Insecure temp file creation - CWE-377."""
    tmp = tempfile.mktemp()
    with open(tmp, 'w') as f:
        f.write("sensitive data")
    return tmp


def disabled_ssl_verification(url):
    """SSL verification disabled - CWE-295."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.urlopen(url, context=ctx).read()


def sql_injection(user_id):
    """SQL injection via string formatting - CWE-89."""
    import sqlite3
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)
    return cursor.fetchall()


def path_traversal(filename):
    """Path traversal vulnerability - CWE-22."""
    base_dir = "/var/www/uploads/"
    filepath = base_dir + filename  # No sanitization
    with open(filepath, 'r') as f:
        return f.read()


def yaml_load_unsafe(data):
    """Unsafe YAML loading - CWE-502."""
    return yaml.load(data)  # yaml.safe_load should be used


def hardcoded_connection():
    """Hardcoded database connection credentials."""
    import psycopg2
    conn = psycopg2.connect(
        host="prod-db.internal.company.com",
        port=5432,
        dbname="djangogoat_prod",
        user="prod_admin",
        password="Pr0d$uperS3cret!Key#99"
    )
    return conn


def eval_user_input(expression):
    """Use of eval with user input - CWE-95."""
    return eval(expression)


def exec_user_code(code):
    """Use of exec with user input - CWE-95."""
    exec(code)


def write_world_readable(data, path):
    """Creating world-readable files - CWE-732."""
    with open(path, 'w') as f:
        f.write(data)
    os.chmod(path, 0o777)


if __name__ == "__main__":
    print("Deployment script loaded.")
    print(f"Using Stripe key: {STRIPE_API_KEY}")
