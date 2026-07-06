import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';
import { describe, it, expect } from 'vitest';
import worker from './index';

describe('Sonagi Playgrounds Sandbox API', () => {
  it('responds with OK on /healthz', async () => {
    const request = new Request('http://localhost/healthz');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);

    expect(response.status).toBe(200);
    expect(await response.text()).toBe('OK');
  });

  it('responds with 400 when path parameter is missing on /sandbox', async () => {
    const request = new Request('http://localhost/sandbox');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);

    expect(response.status).toBe(400);
    const json = (await response.json()) as { error: string };
    expect(json).toHaveProperty('error');
    expect(json.error).toContain('Missing path parameter');
  });

  it('responds with 400 on path traversal attempts', async () => {
    const request = new Request('http://localhost/sandbox?path=../etc/passwd');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);

    expect(response.status).toBe(400);
    const json = (await response.json()) as { error: string };
    expect(json).toHaveProperty('error');
    expect(json.error).toContain('Invalid path parameter');
  });
});
