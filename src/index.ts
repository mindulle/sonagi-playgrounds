/**
 * Sonagi Playgrounds - Code Execution Sandbox
 * Cloudflare Worker Entrypoint
 */

// eslint-disable-next-line @typescript-eslint/no-empty-interface, @typescript-eslint/no-empty-object-type
export interface Env {
  // Bindings go here
}

export default {
  async fetch(request: Request, _env: Env, _ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Simple health check endpoint
    if (url.pathname === '/healthz') {
      return new Response('OK', { status: 200 });
    }

    // TODO: Implement Sandbox execution endpoint (e.g., /execute)
    if (request.method === 'POST' && url.pathname === '/execute') {
      try {
        const body = await request.json();

        // Mock Sandbox execution response
        return Response.json({
          status: 'success',
          result: `Mock execution of code: ${JSON.stringify(body)}`,
        });
      } catch (_error) {
        return Response.json({ status: 'error', message: 'Invalid request' }, { status: 400 });
      }
    }

    return new Response('Sonagi Playgrounds Sandbox API', { status: 200 });
  },
};
