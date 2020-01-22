import string
import secrets


def generate_unique_id():
    length = 8
    initial = "unique_id_"
    secret_key = secrets.token_hex(16)[0:length]
    generated_id =  initial + str(secret_key)
    return generated_id


def generate_unique_id_field():
    length = 20
    initial = "id_"
    secret_key = secrets.token_hex(16)[0:length]
    generated_id =  initial + str(secret_key)
    return generated_id

def generate_unique_id_file():
    length = 9
    initial = "file_id_"
    secret_key = secrets.token_hex(16)[0:length]
    generated_id =  initial + str(secret_key)
    return generated_id

def generate_unique_id_link():
    length = 25
    secret_key = secrets.token_hex(16)[0:length]
    generated_id =  str(secret_key)
    return generated_id

def generate_session_id():
    length = 32
    secret_key = secrets.token_hex(16)[0:length]
    generated_id =  str(secret_key)
    return generated_id

def update_unique_id():
    length = 7
    initial = "update_id_"
    secret_key = secrets.token_hex(16)[0:length]
    generated_id =  str(secret_key)
    return generated_id



