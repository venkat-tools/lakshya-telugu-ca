// Lakshya PWA Service Worker (Stale-While-Revalidate & Offline Kit)
const CACHE_NAME = 'lakshya-pwa-v4';
const OFFLINE_URL = '/';

const CORE_PRECACHE = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/manifest.json',
  '/icon.svg',
  '/lakshya_logo.jpg',
  '/map_pointing_atlas',
  '/sc_judgments_hub',
  '/group2_paper2_master',
  '/static_gk_pocketbook',
  '/mains_descriptive_portal',
  '/student_analytics',
  '/audio_revision',
  '/agri_irrigation_hub',
  '/awards_sports_hub',
  '/group1_prelims_master',
  '/tribal_heritage_hub',
  '/api/sc_judgments',
  '/api/group2_paper2',
  '/api/static_gk',
  '/api/agri_irrigation',
  '/api/awards_sports',
  '/api/group1_prelims',
  '/api/tribal_heritage'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Lakshya PWA] Precaching offline study resources...');
      return cache.addAll(CORE_PRECACHE).catch(err => console.warn('[PWA] Precache warning:', err));
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) {
            console.log('[Lakshya PWA] Clearing legacy cache:', k);
            return caches.delete(k);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // For API and HTML pages: Network first, fallback to cache
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Cache successful GET responses
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(async () => {
        const cached = await caches.match(event.request);
        if (cached) return cached;
        // If requesting an HTML navigation, fallback to root
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
        return new Response('ఆఫ్‌లైన్‌లో ఉన్నారు. దయచేసి నెట్‌వర్క్ కనెక్షన్ సరిచూసుకోండి.', {
          status: 503,
          statusText: 'Offline',
          headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
      })
  );
});
