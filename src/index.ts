/**
 * Sonagi Playgrounds - Code Execution Sandbox
 * Cloudflare Worker Entrypoint (Powered by CodeSandbox API - 100% Free & Serverless)
 */

export interface Env {
  GITHUB_TOKEN?: string;
}

interface SandboxResponse {
  sandbox_id: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
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
        if (env.GITHUB_TOKEN) {
          githubHeaders['Authorization'] = `token ${env.GITHUB_TOKEN}`;
        }

        const encodedPath = examplePath.split('/').map(encodeURIComponent).join('/');
        const contentsUrl = `https://api.github.com/repos/mindulle/sonagi-playgrounds/contents/examples/${encodedPath}`;
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

        const contents = await contentsResponse.json();
        if (!Array.isArray(contents)) {
          return Response.json(
            { error: 'Provided path must point to a directory, not a file.' },
            { status: 400 }
          );
        }

        // Fetch all files in the directory
        const filesToFetch = contents.filter(
          (item: any) => item.type === 'file' && item.download_url
        );
        const fetchedFiles = await Promise.all(
          filesToFetch.map(async (file: any) => {
            const fileRes = await fetch(file.download_url as string);
            if (!fileRes.ok) throw new Error(`Failed to fetch file ${file.name}`);
            const content = await fileRes.text();
            return { name: file.name, content };
          })
        );

        // Build Payload for CodeSandbox
        const payload: { files: Record<string, { content: string }> } = { files: {} };
        fetchedFiles.forEach((file) => {
          payload.files[file.name] = { content: file.content };
        });

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

        // Return Artifact-ready URLs
        return Response.json({
          status: 'success',
          sandbox_id: data.sandbox_id,
          // 1. 순수 웹사이트 미리보기 주소 (최상단 새 창용)
          preview_url: `https://${data.sandbox_id}.csb.app`,
          // 2. 아티팩트 Iframe 임베드 주소 (에디터/메뉴바 숨김, 결과물만 표시)
          embed_url: `https://codesandbox.io/embed/${data.sandbox_id}?view=preview&hidenavigation=1&moduleview=1`,
          // 3. 전체 IDE 주소 (코드를 직접 고치고 싶을 때)
          ide_url: `https://codesandbox.io/s/${data.sandbox_id}`,
        });
      } catch (_error: any) {
        return Response.json({ status: 'error', message: _error.message }, { status: 500 });
      }
    }

    return new Response('Sonagi Playgrounds Sandbox API (CodeSandbox Edition)', { status: 200 });
  },
};
