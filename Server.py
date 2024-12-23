from flask import Flask
from flask import request

import random
import os
import subprocess
import base64

alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

app = Flask(__name__)

@app.route('/decompile', methods=['POST'])
def decompile():
    bytecode = request.get_data()
    filename = 'temp_'

    for _ in range(32):
        filename += random.choice(alphanumeric)

    filename += '.bin'

    try:
        bytecode = base64.b64decode(bytecode)
    except:
        print('Invalid data! @ ' + filename)
        return 'Invalid data! Bytecode:\n' + str(bytecode)

    with open(filename, 'wb') as file:
        file.write(bytecode)

    result = subprocess.run(['luau-lifter.exe', filename, '-e'], stdout=subprocess.PIPE)

    if result.returncode != 0:
        print('Error decompiling bytecode! @ ' + filename)
        os.remove(filename)
        return 'Error decompiling bytecode! Bytecode:\n' + str(bytecode)
    else:
        print('Decompiled bytecode successfully!')
    
    os.remove(filename)

    return result.stdout

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
