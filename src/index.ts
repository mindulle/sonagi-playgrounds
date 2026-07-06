/**
 * Sonagi Playgrounds - Code Execution Sandbox
 * Cloudflare Worker Entrypoint
 */

// eslint-disable-next-line @typescript-eslint/no-empty-interface, @typescript-eslint/no-empty-object-type
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

      // Path traversal validation
      if (examplePath.includes('../') || examplePath.includes('..\\')) {
        return Response.json({ error: 'Invalid path parameter.' }, { status: 400 });
      }

      try {
        const githubRawUrl = `https://raw.githubusercontent.com/mindulle/sonagi-playgrounds/main/examples/${examplePath}/index.js`;
        const codeResponse = await fetch(githubRawUrl);

        let codeContent = '';
        if (codeResponse.ok) {
          codeContent = await codeResponse.text();
        } else if (codeResponse.status === 404) {
          // Fallback to script.js only if index.js is strictly 404 Not Found
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
        } else {
          // GitHub returned a non-404 error (e.g., 500)
          return Response.json(
            { error: `Failed to fetch from GitHub: ${codeResponse.statusText}` },
            { status: 502 }
          );
        }

        // Fetch index.html and style.css in parallel
        const htmlUrl = `https://raw.githubusercontent.com/mindulle/sonagi-playgrounds/main/examples/${examplePath}/index.html`;
        const cssUrl = `https://raw.githubusercontent.com/mindulle/sonagi-playgrounds/main/examples/${examplePath}/style.css`;

        const [htmlResponse, cssResponse] = await Promise.all([fetch(htmlUrl), fetch(cssUrl)]);

        let htmlContent = null;
        if (htmlResponse.ok) {
          htmlContent = await htmlResponse.text();
        }

        let cssContent = null;
        if (cssResponse.ok) {
          cssContent = await cssResponse.text();
        }

        // Construct dynamic boilerplate for CodeSandbox
        const safePackageName = `sonagi-sandbox-${examplePath.replace(/\//g, '-')}`.toLowerCase();
        const packageJson = {
          name: safePackageName,
          version: '1.0.0',
          description: 'Auto-generated sandbox by Sonagi Playgrounds',
          main: 'index.js',
          dependencies: {},
        };

        let finalHtml = htmlContent;
        if (!finalHtml) {
          finalHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sonagi Sandbox</title>${cssContent ? '\n  <link rel="stylesheet" href="style.css">' : ''}
</head>
<body>
  <div id="app"></div>
  <script src="index.js"></script>
</body>
</html>`;
        }

        const payload: { files: Record<string, { content: string }> } = {
          files: {
            'package.json': { content: JSON.stringify(packageJson, null, 2) },
            'index.html': { content: finalHtml },
            'index.js': { content: codeContent },
          },
        };

        if (cssContent) {
          payload.files['style.css'] = { content: cssContent };
        }

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
      } catch (_error: unknown) {
        const message = _error instanceof Error ? _error.message : String(_error);
        return Response.json({ status: 'error', message }, { status: 500 });
      }
    }

    return new Response('Sonagi Playgrounds Sandbox API', { status: 200 });
  },
};
