from utils import common_util
import jwt

def generate_jwt(password):
    try:
        util=common_util.common_utilities()
        config=util.read_config_file()
        key=config['shared_key_jwt']
        dict_pass={'password':password}
        return jwt.encode(dict_pass, key, algorithm='HS256')
    except Exception as e:
        raise Exception(f"Error generating JWT: {e}")
    
print(generate_jwt("tarmak007"))

