import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  scenarios: {
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '3m', target: 100 },
        { duration: '4m', target: 300 },
        { duration: '6m', target: 500 },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
      exec: 'loadTest',
    },
    e2e_check: {
      executor: 'constant-vus',
      vus: 5,
      duration: '3m',
      startTime: '15m30s',
      exec: 'e2eCheck',
    },
  },
  thresholds: {
    'http_req_duration{name:enqueue}': ['p(95)<3000'],
    'http_req_failed{name:enqueue}': ['rate<0.05'],
    'checks{check:queue_progressing}': ['rate>0.9'],
    'checks{check:no_processing_leak}': ['rate>0.9'],
  },
};

export function loadTest() {
  const uniqueKey = `long-load-${__VU}-${__ITER}-${randomString(6)}`;
  const res = http.post(
    'http://127.0.0.1:8000/test/enqueue',
    JSON.stringify({ key: uniqueKey }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'enqueue' },
    }
  );

  if (res.status !== 200) {
    console.error(`HTTP ${res.status}: ${res.body ? res.body.substring(0, 200) : 'no body'}`);
    return;
  }

  let body;
  try {
    body = res.json();
  } catch (e) {
    console.error(`Invalid JSON: ${res.body ? res.body.substring(0, 200) : 'no body'}`);
    return;
  }

  check(res, {
    'status is 200': (r) => r.status === 200,
    'status is pending': () => body.status === 'pending',
  });

  sleep(Math.random() * 0.5);
}

export function e2eCheck() {
  const res = http.get('http://127.0.0.1:8000/metrics/queue', {
    tags: { name: 'queue_metrics' },
  });

  if (res.status !== 200) {
    console.error(`Metrics error: ${res.status}`);
    return;
  }

  const text = res.body;
  const done = parseInt(text.match(/tasks_outbox_count\{status="done"\} (\d+)/)?.[1] || 0);
  const pending = parseInt(text.match(/tasks_outbox_count\{status="pending"\} (\d+)/)?.[1] || 0);
  const processing = parseInt(text.match(/tasks_outbox_count\{status="processing"\} (\d+)/)?.[1] || 0);
  const failed = parseInt(text.match(/tasks_outbox_count\{status="failed"\} (\d+)/)?.[1] || 0);

  console.log(`Queue: done=${done} pending=${pending} processing=${processing} failed=${failed}`);

  check(null, {
    'queue_progressing': () => pending < 100000,
    'no_processing_leak': () => processing < 1000,
  });

  sleep(5);
}
