from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hash:
    def __init__(self):
        pass

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
