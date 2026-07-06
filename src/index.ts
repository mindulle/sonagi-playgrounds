/**
 * Sonagi Playgrounds - Code Execution Sandbox
 * Cloudflare Worker Entrypoint
 */

// eslint-disable-next-line @typescript-eslint/no-empty-interface, @typescript-eslint/no-empty-object-type
export interface Env {
  GITHUB_TOKEN?: string;
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
        const githubHeaders: Record<string, string> = {
          'User-Agent': 'Sonagi-Playgrounds-Worker',
          Accept: 'application/vnd.github.v3+json',
        };
        if (_env.GITHUB_TOKEN) {
          githubHeaders['Authorization'] = `token ${_env.GITHUB_TOKEN}`;
        }

        const contentsUrl = `https://api.github.com/repos/mindulle/sonagi-playgrounds/contents/examples/${examplePath}`;
        const contentsResponse = await fetch(contentsUrl, { headers: githubHeaders });

        if (contentsResponse.status === 404) {
          return Response.json(
            { error: `Example not found at examples/${examplePath}` },
            { status: 404 }
          );
        }

        if (!contentsResponse.ok) {
          return Response.json(
            { error: `Failed to fetch from GitHub: ${contentsResponse.statusText}` },
            { status: 502 }
          );
        }

        const contents = (await contentsResponse.json()) as Array<{
          name: string;
          type: string;
          download_url: string | null;
        }>;

        const filesToFetch = contents.filter((item) => item.type === 'file' && item.download_url);

        const fetchedFiles = await Promise.all(
          filesToFetch.map(async (file) => {
            const fileRes = await fetch(file.download_url as string);
            const content = await fileRes.text();
            return { name: file.name, content };
          })
        );

        const payload: { files: Record<string, { content: string }> } = { files: {} };
        let hasPackageJson = false;
        let hasIndexHtml = false;
        let hasCss = false;

        fetchedFiles.forEach((file) => {
          payload.files[file.name] = { content: file.content };
          if (file.name === 'package.json') hasPackageJson = true;
          if (file.name === 'index.html') hasIndexHtml = true;
          if (file.name.endsWith('.css')) hasCss = true;
        });

        // 1. Fallback for package.json
        if (!hasPackageJson) {
          const safePackageName = `sonagi-sandbox-${examplePath.replace(/\//g, '-')}`.toLowerCase();
          const packageJson = {
            name: safePackageName,
            version: '1.0.0',
            description: 'Auto-generated sandbox by Sonagi Playgrounds',
            main: payload.files['index.js'] ? 'index.js' : 'script.js',
            dependencies: {},
          };
          payload.files['package.json'] = { content: JSON.stringify(packageJson, null, 2) };
        }

        // 2. Fallback for index.html (Vanilla JS backward compatibility)
        if (!hasIndexHtml && (payload.files['index.js'] || payload.files['script.js'])) {
          const mainScript = payload.files['index.js'] ? 'index.js' : 'script.js';
          const cssLink = hasCss ? '\n  <link rel="stylesheet" href="style.css">' : '';
          const fallbackHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sonagi Sandbox</title>${cssLink}
</head>
<body>
  <div id="app"></div>
  <script src="${mainScript}"></script>
</body>
</html>`;
          payload.files['index.html'] = { content: fallbackHtml };
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
