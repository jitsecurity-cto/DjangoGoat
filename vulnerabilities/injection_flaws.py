"""Injection vulnerability examples for SAST scanner detection."""

import os
import subprocess
import sqlite3
import xml.etree.ElementTree as ET
from lxml import etree


# ============================================================
# SQL Injection - CWE-89
# ============================================================

def get_user_by_name(username):
    """SQL injection via string concatenation."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return cursor.fetchall()


def get_user_by_id(user_id):
    """SQL injection via format string."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()


def search_users(search_term):
    """SQL injection via % formatting."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE '%%%s%%'" % search_term)
    return cursor.fetchall()


# ============================================================
# Command Injection - CWE-78
# ============================================================

def ping_host(hostname):
    """OS command injection via os.system."""
    os.system("ping -c 4 " + hostname)


def lookup_dns(domain):
    """Command injection via subprocess with shell=True."""
    result = subprocess.check_output("nslookup " + domain, shell=True)
    return result.decode()


def process_file(filename):
    """Command injection in file processing."""
    os.popen("cat /var/data/" + filename)


# ============================================================
# Code Injection - CWE-94/95
# ============================================================

def calculate(expression):
    """Code injection via eval."""
    return eval(expression)


def run_dynamic_code(code_string):
    """Code injection via exec."""
    exec(code_string)


def dynamic_import(module_name):
    """Arbitrary module import."""
    return __import__(module_name)


# ============================================================
# XXE - CWE-611
# ============================================================

def parse_xml_unsafe(xml_string):
    """XXE via lxml without disabling external entities."""
    parser = etree.XMLParser(resolve_entities=True)
    return etree.fromstring(xml_string.encode(), parser)


def parse_xml_file(filepath):
    """XXE via ElementTree (less severe but still flagged)."""
    tree = ET.parse(filepath)
    return tree.getroot()


# ============================================================
# SSRF - CWE-918
# ============================================================

def fetch_url(user_url):
    """Server-side request forgery."""
    import urllib.request
    return urllib.request.urlopen(user_url).read()


def proxy_request(target_host, target_path):
    """SSRF via user-controlled host."""
    import requests
    url = f"http://{target_host}/{target_path}"
    return requests.get(url).text


# ============================================================
# LDAP Injection - CWE-90
# ============================================================

def find_user_ldap(username):
    """LDAP injection via string concatenation."""
    import ldap
    conn = ldap.initialize("ldap://ldap.example.com")
    search_filter = "(uid=" + username + ")"
    return conn.search_s("dc=example,dc=com", ldap.SCOPE_SUBTREE, search_filter)


# ============================================================
# XPath Injection - CWE-643
# ============================================================

def xpath_login(username, password):
    """XPath injection."""
    tree = ET.parse("users.xml")
    query = f"//user[@name='{username}' and @password='{password}']"
    return tree.getroot().findall(query)
