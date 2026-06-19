/**
storage.js
Drop-in async shim that replaces localStorage with server-backed persistence.
Exposes: store.get(key), store.set(key, value), store.remove(key)
All return Promises. A tiny in-memory cache avoids redundant network hits.
*/
(function () {
  const cache = {};
  window.store = {
    _cache: cache,
    async get(key) {
      if (key in cache) return cache[key];
      try {
        // Relative path: automatically uses the current origin (host + port)
        const res = await fetch(`/data?key=${encodeURIComponent(key)}`);
        const json = await res.json();
        const val = json.value ?? null;
        cache[key] = val;
        return val;
      } catch (e) {
        console.warn('[store] GET failed for', key, e);
        return null;
      }
    },

    async set(key, value) {
      cache[key] = value;
      try {
        await fetch('/data', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key, value })
        });
      } catch (e) {
        console.warn('[store] SET failed for', key, e);
      }
    },

    async remove(key) {
      delete cache[key];
      try {
        await fetch('/data', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key, delete: true })
        });
      } catch (e) {
        console.warn('[store] REMOVE failed for', key, e);
      }
    }
  };
})();