import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // разогрев до 50 VU
    { duration: '1m', target: 100 },   // поднимаем до 100
    { duration: '1m', target: 200 },   // до 200
    { duration: '30s', target: 300 },  // пик 300
    { duration: '30s', target: 0 },    // спад
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],      // ошибок < 1%
    http_req_duration: ['p(95)<1000'],   // 95% запросов быстрее 1 сек
  },
};

export default function () {
  // Уникальный ключ, чтобы каждая задача создавалась заново
  const uniqueKey = `load-${__VU}-${__ITER}-${randomString(6)}`;
  
  const url = `http://127.0.0.1:8000/test/enqueue?key=${uniqueKey}`;
  const res = http.post(url);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'status is pending': (r) => r.json().status === 'pending',
  });

  sleep(0.1); // небольшая пауза, чтобы VU не долбили сервер без передышки
}
