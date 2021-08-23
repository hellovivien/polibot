import uvicorn

logo = '''
█▀█ █▀█ █   █ █▄▄ █▀█ ▀█▀   ▄▀█ █▀█ █
█▀▀ █▄█ █▄▄ █ █▄█ █▄█  █    █▀█ █▀▀ █
'''

if __name__ == "__main__":
    print(logo)
    print("------------------------------------\nopen http://localhost:8080\n------------------------------------\n")
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)        