import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    'Brick \\u0e04\\u0e37\\u0e2d\\u0e2d\\u0e30\\u0e44\\u0e23.pdf',
    '\\u0e42\\u0e21\\u0e40\\u0e14\\u0e25\\u0e1b\\u0e31\\u0e0d\\u0e0d\\u0e32\\u0e1b\\u0e23\\u0e30\\u0e14\\u0e34\\u0e29\\u0e10\\u0e4c.pdf',
    '\\u0e15\\u0e31\\u0e27\\u0e2d\\u0e22\\u0e48\\u0e32\\u0e07\\u0e17\\u0e35\\u0e48\\u0e21\\u0e35\\u0e21\\u0e32\\u0e43\\u0e2b\\u0e49\\u0e1e\\u0e23\\u0e49\\u0e2d\\u0e21\\u0e43\\u0e0a\\u0e49\\u0e07\\u0e32\\u0e19.pdf',
    'ABX00162-ABX00173-datasheet.pdf',
    'App \\u0e04\\u0e37\\u0e2d\\u0e2d\\u0e30\\u0e44\\u0e23.pdf',
    '\\u0e01\\u0e32\\u0e23\\u0e42\\u0e1b\\u0e23\\u0e41\\u0e01\\u0e23\\u0e21\\u0e1a\\u0e2d\\u0e23\\u0e4c\\u0e14 Arduino UNO Q \\u0e14\\u0e49\\u0e27\\u0e22\\u0e42\\u0e2b\\u0e21\\u0e14\\u0e40\\u0e19\\u0e47\\u0e15\\u0e40\\u0e27\\u0e34\\u0e23\\u0e4c\\u0e04.pdf',
    '\\u0e25\\u0e07\\u0e25\\u0e35\\u0e19\\u0e38\\u0e01\\u0e2a\\u0e4c\\u0e43\\u0e2b\\u0e21\\u0e48.pdf',
    'Introduction to App Lab.pdf'
]

for f in files:
    decoded = json.loads(f'"{f}"')
    print("-", decoded)
