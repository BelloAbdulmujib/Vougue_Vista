from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    print(generate_password_hash(password))

if __name__ == "__main__":
    password = "12345678"
    hash_password(password)