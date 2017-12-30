import base64
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings


def generate_uuid():
    list_uuid = uuid.uuid4()
    return list_uuid

def generate_masterkey(domain):
    domain = str(uuid.uuid5(uuid.NAMESPACE_DNS, domain))
    domain = domain.encode('utf-8')
    globalkey = settings.MASTER_SALT
    salt = globalkey.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    masterkey = base64.urlsafe_b64encode(kdf.derive(domain))
    return masterkey

def generate_personalkey(user_uuid, user_password):
    password = user_password.encode('utf-8')
    salt = str(user_uuid)
    salt = salt.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    personalkey = base64.urlsafe_b64encode(kdf.derive(password))
    return personalkey

def encrypt_password(masterkey, personalkey, password):

    ## encrypt using master key
    f = Fernet(masterkey)
    pwbin = password.encode('utf-8')
    pwenc = f.encrypt(pwbin)
    pw = pwenc.decode('utf-8')

    ## encrypt using personal key
    fn = Fernet(personalkey)
    finpwbin = pw.encode('utf-8')
    finpwenc = fn.encrypt(finpwbin)

    ## return encrypted password
    return finpwenc.decode('utf-8')

def decrypt_password(masterkey, personalkey, password):

    ## decrypt using personal key
    f = Fernet(personalkey)
    pw1 = password.encode('utf-8')
    pw = f.decrypt(pw1)

    ## decrypt using master key
    f = Fernet(masterkey)
    pw = f.decrypt(pw)
    try:
        pw = pw.decode('utf-8')
    except:
        pass
    return pw
