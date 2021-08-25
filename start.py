logo = '''
█▀█ █▀█ █   █ █▄▄ █▀█ ▀█▀
█▀▀ █▄█ █▄▄ █ █▄█ █▄█  █ 
'''
ask_for_this = {'db_password':None}
projects_paths = ['fastapi/app', 'streamlit/app']

if __name__ == "__main__":
    print(logo)
    for k,v in ask_for_this.items():
        answer = input('{}: '.format(k))
        ask_for_this[k] = answer
    
    for project_path in projects_paths:
        with open('{}/.env'.format(project_path), 'w') as env_file:
            for k,v in ask_for_this.items():
                env_file.write('{}={}'.format(k, v))
    print("\nProject is ready!\nStart it with : docker-compose up")