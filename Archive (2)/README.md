# Fail2ban Docker Lab

Two containers on an isolated network (172.28.0.0/24):

| Container      | IP           | Role                                             |
|----------------|--------------|--------------------------------------------------|
| f2b-victim     | 172.28.0.10  | sshd + rsyslog + fail2ban (`sshd` jail)          |
| f2b-attacker   | 172.28.0.20  | simulates SSH brute force with `attack.sh`       |

## Run
    ./run_demo.sh

or manually:

    docker compose up -d --build
    docker exec f2b-attacker /attack.sh
    docker exec f2b-victim fail2ban-client status sshd
    docker exec f2b-victim tail -f /var/log/fail2ban.log

## What happens
1. The attacker tries wrong passwords for `testuser` via SSH.
2. sshd logs `Failed password ...` to /var/log/auth.log.
3. After 3 failures in 60s (see `victim/jail.local`), fail2ban bans 172.28.0.20 for 120s
   with an iptables rule; further attempts are refused.
4. The ban expires automatically, or unban with:
   `docker exec f2b-victim fail2ban-client set sshd unbanip 172.28.0.20`

## Tuning
- Change `ATTEMPTS`, `DELAY` in docker-compose.yml (attacker env).
- Change `maxretry`, `findtime`, `bantime` in victim/jail.local.

## Troubleshooting
- If fail2ban logs iptables/nft errors, your host kernel may lack the nft backend. In
  victim/Dockerfile add:
  `RUN update-alternatives --set iptables /usr/sbin/iptables-legacy`
- Only run this against the lab containers. Never point attack.sh at systems you don't own.
