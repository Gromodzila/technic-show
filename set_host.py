#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
from config import ConfigManager

def set_host(file_path, new_host):
    cfg = ConfigManager()
    cfg.load_config_and_spec(file_path)  
    cfg.set('SERVER', 'host', new_host)   
    cfg.write()                          
    print(f"✓ IP сервера изменён на {new_host}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Использование: python3 set_host.py <путь к client.ini> <новый IP>")
        sys.exit(1)
    set_host(sys.argv[1], sys.argv[2])