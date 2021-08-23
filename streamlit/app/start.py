from dotenv import dotenv_values
from streamlit import cli as stcli
import sys

def ask_for_params(env_keys):
    with open('.env', 'w') as env_file:
        for key in env_keys:
            val = input('{}: '.format(key))
            if val:
                env_file.write('{}={}'.format(key, val))
    return dotenv_values()


env_dict = dotenv_values()
env_keys = ['db_password']
logo = '''
█▀█ █▀█ █   █ █▄▄ █▀█ ▀█▀
█▀▀ █▄█ █▄▄ █ █▄█ █▄█  █
'''

print(logo)
while list(env_dict.keys()) != env_keys:
    env_dict = ask_for_params(env_keys)
sys.argv = ["streamlit", "run", "streamlit/app/app.py"]
sys.exit(stcli.main())