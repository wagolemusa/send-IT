from passlib.hash import pbkdf2_sha256 as sha256

class PassModel():
    ...

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)