#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_INI="${SCRIPT_DIR}/drone/config/client.ini"
SET_HOST="${SCRIPT_DIR}/set_host.py"
SERVICE="technic-show.service"

# Запасной путь к стандартной директории на Orange Pi
if [[ ! -f "$CLIENT_INI" && -f "/home/orangepi/technic-show/drone/config/client.ini" ]]; then
    CLIENT_INI="/home/orangepi/technic-show/drone/config/client.ini"
fi
if [[ ! -f "$SET_HOST" && -f "/home/orangepi/technic-show/set_host.py" ]]; then
    SET_HOST="/home/orangepi/technic-show/set_host.py"
fi

if [[ $EUID -ne 0 ]]; then
   echo "Запускайте с правами root (sudo)."
   exit 1
fi

if [[ -n "${1:-}" ]]; then
    SERVER_IP="$1"
else
    read -p "Введите IP-адрес сервера: " SERVER_IP
fi

if [[ ! -f "$SET_HOST" ]]; then
    echo "Ошибка: $SET_HOST не найден. Убедитесь, что скрипт set_host.py находится в папке проекта."
    exit 2
fi

echo ">>> Устанавливаю IP сервера: $SERVER_IP"
python3 "$SET_HOST" "$CLIENT_INI" "$SERVER_IP"

echo ">>> Исправляю права доступа к client.ini..."
chown -R orangepi:orangepi "$(dirname "$CLIENT_INI")" 2>/dev/null || true
chmod 644 "$CLIENT_INI" 2>/dev/null || true

echo ">>> Запускаю сервис $SERVICE..."
systemctl unmask "$SERVICE" 2>/dev/null || true
systemctl enable "$SERVICE"
systemctl restart "$SERVICE"

echo ">>> Статус сервиса:"
systemctl status "$SERVICE" --no-pager -l

echo ">>> Последние строки лога:"
journalctl -u "$SERVICE" -n 20 --no-pager
