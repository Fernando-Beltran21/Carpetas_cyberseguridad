// The browser never holds the API key. nginx adds it server-side.
const btn = document.getElementById('callBtn');
const statusEl = document.getElementById('status');
const outputEl = document.getElementById('output');

btn.addEventListener('click', async () => {
  btn.disabled = true;
  statusEl.className = 'status';
  statusEl.textContent = 'Sending request...';
  outputEl.textContent = '—';

  try {
    const res = await fetch('/api/secure-data', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    const body = await res.json().catch(() => ({}));

    if (res.ok) {
      statusEl.className = 'status ok';
      statusEl.textContent = `${res.status} OK`;
    } else {
      statusEl.className = 'status err';
      statusEl.textContent = `${res.status} ${res.statusText}`;
    }
    outputEl.textContent = JSON.stringify(body, null, 2);
  } catch (err) {
    statusEl.className = 'status err';
    statusEl.textContent = 'Request failed';
    outputEl.textContent = String(err);
  } finally {
    btn.disabled = false;
  }
});
