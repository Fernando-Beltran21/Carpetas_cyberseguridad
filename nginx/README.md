# Nginx X-API-Key proxy

This project runs a single nginx container. Nginx serves the static page and
proxies `/api/` requests to the URL configured in `API_UPSTREAM`.

The browser never receives or sends the secret. At startup, nginx reads
`API_KEY` from the container environment and adds it to proxied requests with
`proxy_set_header X-API-Key`. The generated nginx configuration remains inside
the container; it is not part of the static files served to the browser.

## Files

```text
.
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── nginx.conf.template
├── index.html
└── app.js
```

## Run with Docker Compose

Copy the example environment file and set a real secret and the URL of the
protected API:

```bash
cp .env.example .env
# edit .env and set API_KEY and API_UPSTREAM
docker compose up --build
```

Open <http://localhost:8080>. The page calls `/api/secure-data`; nginx forwards
that request to `API_UPSTREAM` and adds the hidden header.

`API_UPSTREAM` defaults to `http://host.docker.internal:8000`, which is useful
when the protected API is running on the host. The `/api/` prefix is removed
before forwarding, so `/api/secure-data` reaches `/secure-data` in `files2`.
For an API available elsewhere, set its base URL in `.env`, for example:

```dotenv
API_KEY=replace-with-a-long-random-secret
API_UPSTREAM=http://api.example.test:8000
```

Only nginx publishes a host port:

```text
browser -> nginx:8080 -> API_UPSTREAM
```

## Verify that the browser cannot see the key

The static files contain no real secret and `app.js` does not set an
`X-API-Key` header. Check the served JavaScript with:

```bash
curl -s http://localhost:8080/app.js | grep -Ei 'API_KEY|X-API-Key' \
  && echo "Unexpected secret reference" \
  || echo "No API key in browser JavaScript"
```

To inspect the request sent by the browser, use the browser network panel or
the following command without adding credentials:

```bash
curl -i http://localhost:8080/api/secure-data
```

The request to nginx has no `X-API-Key` header. Nginx adds that header only on
the server-side hop to `API_UPSTREAM`.

## Security notes

- Never commit `.env` or place a real key in `index.html` or `app.js`.
- Keep `API_KEY` only in the runtime environment of nginx.
- Use HTTPS in production so the browser-to-nginx connection is encrypted.
- The proxy secret identifies nginx to the protected API; it does not provide
  user authentication. Add sessions or tokens if requests need per-user
  authorization.