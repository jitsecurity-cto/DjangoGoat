"""Cryptographic vulnerability examples for scanner detection."""

import hashlib
import base64
from Crypto.Cipher import DES, AES, Blowfish


# CWE-327: Use of broken/weak cryptographic algorithms
def encrypt_with_des(plaintext, key):
    """DES encryption - broken algorithm."""
    cipher = DES.new(key[:8], DES.MODE_ECB)
    padded = plaintext + (8 - len(plaintext) % 8) * ' '
    return cipher.encrypt(padded.encode())


def encrypt_with_ecb(plaintext, key):
    """AES-ECB mode - insecure block cipher mode."""
    cipher = AES.new(key.encode()[:16], AES.MODE_ECB)
    padded = plaintext + (16 - len(plaintext) % 16) * ' '
    return cipher.encrypt(padded.encode())


def hash_password_md5(password):
    """MD5 for password hashing - CWE-328."""
    return hashlib.md5(password.encode()).hexdigest()


def hash_password_sha1(password):
    """SHA1 for password hashing - CWE-328."""
    return hashlib.sha1(password.encode()).hexdigest()


def weak_encryption_key():
    """Hardcoded weak encryption key - CWE-321."""
    key = "0123456789abcdef"
    iv = "abcdef9876543210"
    return key, iv


# CWE-329: Not using a random IV
def encrypt_static_iv(plaintext):
    """Static IV reuse vulnerability."""
    key = b'Sixteen byte key'
    iv = b'\x00' * 16  # Static zero IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = plaintext + (16 - len(plaintext) % 16) * ' '
    return cipher.encrypt(padded.encode())


# CWE-916: Insufficient password hashing
def hash_no_salt(password):
    """Password hashing without salt."""
    return hashlib.sha256(password.encode()).hexdigest()


def xor_encrypt(data, key="secret"):
    """XOR cipher - trivially breakable."""
    return bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data.encode())])


def encode_not_encrypt(sensitive_data):
    """Base64 encoding mistaken for encryption - CWE-311."""
    return base64.b64encode(sensitive_data.encode()).decode()
