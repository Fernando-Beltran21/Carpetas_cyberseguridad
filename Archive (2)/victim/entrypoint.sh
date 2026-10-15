#!/bin/bash
set -e
mkdir -p /run/sshd /var/run/fail2ban
touch /var/log/auth.log /var/log/fail2ban.log
rm -f /var/run/fail2ban/fail2ban.sock /var/run/fail2ban/fail2ban.pid

rsyslogd            # writes sshd auth events to /var/log/auth.log
sleep 1
/usr/sbin/sshd      # SSH server (logs via syslog)
fail2ban-client -x start

echo "[victim] sshd + fail2ban running. Following fail2ban log..."
exec tail -F /var/log/fail2ban.log
