#!/bin/bash
set -e
cd "$(dirname "$0")"

echo ">>> Building and starting containers..."
docker compose up -d --build
sleep 4

echo; echo ">>> Fail2ban status BEFORE attack"
docker exec f2b-victim fail2ban-client status sshd

echo; echo ">>> Launching attack from attacker container"
docker exec f2b-attacker /attack.sh || true

sleep 2
echo; echo ">>> Fail2ban status AFTER attack"
docker exec f2b-victim fail2ban-client status sshd

echo; echo ">>> iptables rules created by fail2ban"
docker exec f2b-victim iptables -S | grep -i f2b || true

echo; echo ">>> Fail2ban log (last lines)"
docker exec f2b-victim tail -n 15 /var/log/fail2ban.log

cat <<MSG

Useful next steps:
  docker exec f2b-victim fail2ban-client set sshd unbanip 172.28.0.20   # manual unban
  docker exec f2b-attacker /attack.sh                                    # attack again
  docker compose down                                                    # cleanup
MSG
