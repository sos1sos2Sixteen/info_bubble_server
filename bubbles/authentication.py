import hashlib

def gen_auth(acct):
    return hashlib.md5((acct.account_num + acct.password_plain + "ohoho").encode("utf-8")).hexdigest()

def validate_auth(acct,auth):
    return gen_auth(acct) == auth