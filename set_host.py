#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
from config import ConfigManager

def configure_chrony(server_host, chrony_conf="/etc/chrony/chrony.conf"):
    if not os.path.exists(chrony_conf):
        return False
    try:
        with open(chrony_conf, 'r') as f:
            lines = f.readlines()
        new_lines = []
        replaced = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("server ") or stripped.startswith("pool "):
                if not replaced:
                    new_lines.append(f"server {server_host} iburst minpoll 2 maxpoll 4\n")
                    replaced = True
            else:
                new_lines.append(line)
        if not replaced:
            new_lines.insert(0, f"server {server_host} iburst minpoll 2 maxpoll 4\n")
        with open(chrony_conf, 'w') as f:
            f.writelines(new_lines)
        os.system("systemctl restart chrony 2>/dev/null || true")
        print(f"✓ Chrony NTP настроен на {server_host}")
        return True
    except Exception as e:
        print(f"⚠ Не удалось обновить Chrony: {e}")
        return False

def set_host(file_path, new_host, port=None, broadcast=None, sync_chrony=False):
    if not os.path.exists(file_path):
        print(f"✗ Файл конфигурации не найден: {file_path}")
        sys.exit(1)
        
    cfg = ConfigManager()
    cfg.load_config_and_spec(file_path)
    cfg.set('SERVER', 'host', new_host)
    if port is not None:
        cfg.set('SERVER', 'port', int(port))
    if broadcast is not None:
        cfg.set('BROADCAST', 'use', bool(broadcast))
    cfg.write()
    
    status_str = f"✓ Сервер установлен: {new_host}"
    if port:
        status_str += f":{port}"
    if broadcast is not None:
        status_str += f" | Broadcast: {'ВКЛ' if broadcast else 'ВЫКЛ'}"
    print(status_str)
    
    if sync_chrony and os.geteuid() == 0:
        configure_chrony(new_host)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Настройка IP сервера и параметров связи")
    parser.add_argument("config_file", help="Путь к client.ini")
    parser.add_argument("new_host", help="Новый IP-адрес или hostname сервера")
    parser.add_argument("--port", "-p", type=int, default=None, help="Порт сервера (по умолчанию 25000)")
    parser.add_argument("--enable-broadcast", action="store_true", help="Включить UDP broadcast поиск")
    parser.add_argument("--disable-broadcast", action="store_true", help="Отключить UDP broadcast поиск (рекомендуется)")
    parser.add_argument("--sync-chrony", action="store_true", help="Синхронизировать адрес в /etc/chrony/chrony.conf")
    
    args = parser.parse_args()
    
    broadcast = None
    if args.enable_broadcast:
        broadcast = True
    elif args.disable_broadcast:
        broadcast = False
        
    set_host(args.config_file, args.new_host, port=args.port, broadcast=broadcast, sync_chrony=args.sync_chrony)
