# Fail2ban vs. Unprotected Nginx — HTTP Flood Demo

Three containers on an isolated network (172.29.0.0/24), all serving/attacking a
simple "Hello World" `index.html`:

| Container               | IP           | Role                                             |
|--------------------------|--------------|---------------------------------------------------|
| http-victim-protected    | 172.29.0.10  | nginx + fail2ban (`http-flood` jail)              |
| http-victim-unprotected  | 172.29.0.11  | nginx only, no defenses                           |
| http-attacker            | 172.29.0.20  | `flood.py`: bounded, fixed-duration HTTP test       |

## Run (Docker Desktop on macOS / Linux)

Run these commands from this directory, the one containing `docker-compose.yml`.
On macOS, start Docker Desktop first; the protected container needs the
`NET_ADMIN` capability to install its firewall rule inside its own network
namespace. No host `iptables` commands or host-side firewall changes are needed.

Recommended (waits for services and checks Fail2ban before starting the test):

```sh
bash run_demo.sh
```

Or run manually:

```sh
docker compose up -d --build
docker compose ps
docker compose exec -T attacker curl -i http://victim-protected/
docker compose exec -T attacker curl -i http://victim-unprotected/
docker compose exec -T victim-protected fail2ban-client status http-flood
docker compose exec -T attacker python /flood.py
docker compose exec -T victim-protected fail2ban-client status http-flood
docker compose logs --tail=50 victim-protected
```

To follow the Fail2ban log live, use a separate terminal and press Ctrl-C to
stop following it:

```sh
docker compose exec victim-protected tail -f /var/log/fail2ban.log
```

Stop and remove the lab containers/network when finished:

```sh
docker compose down
```

## What happens

1. `flood.py` runs `CONCURRENCY` parallel workers sending `GET /` for
   `DURATION` seconds to each target in turn. `REQUESTS_PER_SECOND` caps the
   aggregate request-start rate per target. Compose sets these to 150 workers,
   150 requests/second, and 45 seconds (about 90 seconds total); standalone
   defaults are 40 workers, 50 requests/second, and 20 seconds. The Python
   standard library handles requests; the container installs `curl` for manual
   connectivity checks.
2. Every request Nginx serves is written to the real file
   `/var/log/nginx/access.log` (the protected image replaces the official Nginx
   image's default stdout symlink so Fail2ban can monitor it).
3. On `victim-protected`, Fail2ban's `http-flood` filter/jail (see
   `victim-protected/jail.local`) watches that log. At 60 matching HTTP requests
   from one IP within 10 seconds, Fail2ban bans that source for 10 minutes.
   Repeat bans increase in duration, up to one day. The `iptables-allports`
   action blocks that IP from all ports on the protected container only; it
   does not affect the host or unprotected container. The flood output counts
   non-200 results as failed; these can include connection errors/timeouts as
   well as bans.
4. `victim-unprotected` has no Fail2ban and does not install a ban, but under
   heavy load it is not guaranteed to return `200` to every request.

This is a bounded, fixed-duration comparison for these lab containers only: the
flood script runs for the configured duration against each target, then stops
and prints a summary. It does not guarantee that either target will fall over.

## Reviewing the two images

Everything below assumes the stack is up (`docker compose up -d --build`).

### 1. Compare what's actually different between them

```bash
diff -u victim-unprotected/Dockerfile victim-protected/Dockerfile
diff -u victim-unprotected/nginx.conf victim-protected/nginx.conf
```

`nginx.conf` and the site content are identical — the only real difference is
that `victim-protected` also installs and runs Fail2ban and writes its access
log to a file that the jail can monitor.

### 2. Inspect the built images directly

```bash
docker image ls | grep victim
docker image inspect http-victim-protected -f '{{json .Config.ExposedPorts}}'
docker history http-victim-protected     # layer-by-layer build steps
docker history http-victim-unprotected
```

### 3. Look inside each running container

```bash
# Unprotected: just nginx, nothing watching the logs
docker exec http-victim-unprotected ps aux
docker exec http-victim-unprotected ls /etc/ | grep -i fail2ban   # -> not found

# Protected: nginx + fail2ban both running
docker exec http-victim-protected ps aux
docker exec http-victim-protected cat /etc/fail2ban/jail.local
docker exec http-victim-protected cat /etc/fail2ban/filter.d/http-flood.conf
docker exec http-victim-protected fail2ban-client status
docker exec http-victim-protected fail2ban-client status http-flood
```

### 4. Watch each one live during/after a flood

```bash
# Protected access log is a regular file monitored by Fail2ban
docker compose exec victim-protected tail -f /var/log/nginx/access.log

# The unprotected image uses the official Nginx stdout log symlink
docker compose logs -f victim-unprotected

# Only the protected one has a fail2ban log, and it shows the ban happen
docker compose exec victim-protected tail -f /var/log/fail2ban.log

# Only the protected one should get Fail2ban iptables rules
docker compose exec -T victim-protected iptables -S | grep -i f2b
docker compose exec -T victim-unprotected sh -c 'command -v iptables || echo "iptables not installed"'
```

### 5. Compare behavior from the attacker's side

```bash
# During/after a flood, hit both directly and compare
docker exec http-attacker curl -s -o /dev/null -w "protected:   %{http_code} in %{time_total}s\n"   http://victim-protected/
docker exec http-attacker curl -s -o /dev/null -w "unprotected: %{http_code} in %{time_total}s\n" http://victim-unprotected/
```

While the attacker's IP is banned, the protected target will refuse/time out
(`000`) on this check; the unprotected target has no ban and should normally
answer `200` when it is not overloaded.

## Tuning

- `DURATION`, `CONCURRENCY`, `REQUESTS_PER_SECOND` — set in `docker-compose.yml`
   under the `attacker` service's `environment`. `flood.py` accepts durations up
   to 300 seconds, concurrency up to 500 workers, and a request rate up to 500
   per second; it rejects values outside those bounds.
- `maxretry`, `findtime`, `bantime`, `bantime.factor`, and `bantime.maxtime` —
   set in `victim-protected/jail.local`. The defaults detect 60 requests per IP
   in 10 seconds, start bans at 10 minutes, and escalate repeat bans up to one
   day. Tune cautiously: logs do not distinguish abusive clients from legitimate
   users behind a shared IP, so an overly low threshold can block many users.

