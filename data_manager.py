import os, hashlib
import data
from flask import session


def random_api_key():
    """
    :return: salt in secret key
    """
    return os.urandom(100)


def is_logged_in():
    if 'logged_in' in session:
        return True
    return False


def check_login(username, typed_password):
    if username in data.users and encrypt_password(typed_password) == data.users[username]:
        return True
    return False


def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()

