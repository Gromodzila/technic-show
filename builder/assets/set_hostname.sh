#!/bin/bash
# Скрипт для смены hostname дрона
# Использование: sudo ./set-hostname.sh new-hostname
set -euo pipefail

HOSTS_FILE="/etc/hosts"

if [[ $EUID -ne 0 ]]; then
   echo "Запускайте с правами root (sudo)."
   exit 1
fi

if [[ -z "${1:-}" ]]; then
    echo "Укажите новый hostname. Пример: sudo $0 technic-1"
    exit 2
fi

NEW_HOSTNAME="$1"

echo ">>> Устанавливаю hostname: $NEW_HOSTNAME"
hostnamectl set-hostname "$NEW_HOSTNAME"

echo ">>> Обновляю $HOSTS_FILE"
# Находим строку с 127.0.1.1 и заменяем её, либо добавляем новую, если её нет
if grep -q '^127\.0\.1\.1[[:space:]]' "$HOSTS_FILE"; then
    sed -i "s/^127\.0\.1\.1[[:space:]].*/127.0.1.1       $NEW_HOSTNAME $NEW_HOSTNAME.local/" "$HOSTS_FILE"
else
    echo "127.0.1.1       $NEW_HOSTNAME $NEW_HOSTNAME.local" >> "$HOSTS_FILE"
fi

echo "Готово. Новый hostname: $NEW_HOSTNAME"
echo "Чтобы изменения полностью вступили в силу, рекомендуется перезагрузить дрон (sudo reboot)."