from jupyterhub.crypto import CryptKeeper


def encrypt(string):
    return CryptKeeper.instance()._encrypt(string).decode('utf-8')


def decrypt(string):
    return CryptKeeper.instance()._decrypt(string.encode('utf-8'))
