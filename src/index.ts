/**
 * Sonagi Playgrounds - Code Execution Sandbox
 * Cloudflare Worker Entrypoint
 */

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export interface Env {
  // Bindings go here
}

interface SandboxResponse {
  sandbox_id: string;
}

export default {
  async fetch(request: Request, _env: Env, _ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Simple health check endpoint
    if (url.pathname === '/healthz') {
      return new Response('OK', { status: 200 });
    }

    // Dynamic Sandbox Generation Endpoint
    if (request.method === 'GET' && url.pathname === '/sandbox') {
      const examplePath = url.searchParams.get('path');

      if (!examplePath) {
        return Response.json(
          { error: 'Missing path parameter. Usage: /sandbox?path=Vanilla/counter' },
          { status: 400 }
        );
      }

      try {
        // Fetch the raw code from GitHub
        // NOTE: If there are multiple files (HTML, CSS), we might need to fetch them individually
        // or rely on a generic index.js for this boilerplate.
        const githubRawUrl = `https://raw.githubusercontent.com/mindulle/sonagi-playgrounds/main/examples/${examplePath}/index.js`;
        const codeResponse = await fetch(githubRawUrl);

        let codeContent = '';
        if (codeResponse.ok) {
          codeContent = await codeResponse.text();
        } else {
          // If index.js is not found, fallback to trying script.js (common in legacy)
          const fallbackUrl = `https://raw.githubusercontent.com/mindulle/sonagi-playgrounds/main/examples/${examplePath}/script.js`;
          const fallbackResponse = await fetch(fallbackUrl);
          if (fallbackResponse.ok) {
            codeContent = await fallbackResponse.text();
          } else {
            return Response.json(
              { error: `Example not found at examples/${examplePath}` },
              { status: 404 }
            );
          }
        }

        // Construct dynamic boilerplate for CodeSandbox
        const packageJson = {
          name: `sonagi-sandbox-${examplePath.replace(/\//g, '-')}`,
          version: '1.0.0',
          description: 'Auto-generated sandbox by Sonagi Playgrounds',
          main: 'index.js',
          dependencies: {}, // Can dynamically inject React etc. if path includes 'react'
        };

        const htmlTemplate = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sonagi Sandbox</title>
</head>
<body>
  <div id="app"></div>
  <script src="index.js"></script>
</body>
</html>`;

        const payload = {
          files: {
            'package.json': { content: JSON.stringify(packageJson, null, 2) },
            'index.html': { content: htmlTemplate },
            'index.js': { content: codeContent },
          },
        };

        // Send to CodeSandbox Define API
        const csbResponse = await fetch('https://codesandbox.io/api/v1/sandboxes/define?json=1', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify(payload),
        });

        if (!csbResponse.ok) {
          throw new Error(`CodeSandbox API returned ${csbResponse.status}`);
        }

        const data = (await csbResponse.json()) as SandboxResponse;

        return Response.json({
          status: 'success',
          sandbox_url: `https://codesandbox.io/s/${data.sandbox_id}`,
          preview_url: `https://${data.sandbox_id}.csb.app`,
          sandbox_id: data.sandbox_id,
        });
      } catch (error: unknown) {
        return Response.json(
          { status: 'error', message: (error as Error).message },
          { status: 500 }
        );
      }
    }

    return new Response('Sonagi Playgrounds Sandbox API', { status: 200 });
  },
};
