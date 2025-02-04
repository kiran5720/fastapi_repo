from passlib.context import CryptContext

pwd_contaxt = CryptContext(schemes=["bcrypt"],deprecated = "auto")


def hash(password:str):
    return pwd_contaxt.hash(password)


def verify(plain_password,hashed_password):
    return pwd_contaxt.verify(plain_password,hashed_password)