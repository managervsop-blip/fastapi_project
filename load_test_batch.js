import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // разогрев до 20 VU
    { duration: '1m', target: 50 },    // до 50 VU
    { duration: '30s', target: 0 },    // спад
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<3000'], // 3 сек (с batch и rate limiter)
  },
};

export default function () {
  const uniqueKey = `batch-load-${__VU}-${__ITER}-${randomString(6)}`;
  const url = `http://127.0.0.1:8000/test/enqueue?key=${uniqueKey}`;
  const res = http.post(url);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'status is pending': (r) => r.json().status === 'pending',
  });

  sleep(0.5); // пауза, чтобы не перегружать
}
