import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  stages: [
    { duration: '1m', target: 100 },   // разогрев до 100
    { duration: '2m', target: 300 },   // до 300
    { duration: '2m', target: 500 },   // до 500 (пик)
    { duration: '1m', target: 0 },     // резкий спад
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],       // допускаем 5% ошибок на пике
    http_req_duration: ['p(95)<3000'],    // p95 < 3 сек
  },
};

export default function () {
  // Уникальный ключ, чтобы каждая задача создавалась (имитация вебхука)
  const uniqueKey = `max-load-${__VU}-${__ITER}-${randomString(6)}`;
  const url = `http://127.0.0.1:8000/test/enqueue?key=${uniqueKey}`;
  
  const res = http.post(url);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'status is pending': (r) => r.json().status === 'pending',
  });

  sleep(0.1); // минимальная пауза (чтобы VU не «долбили» без перерыва)
}
