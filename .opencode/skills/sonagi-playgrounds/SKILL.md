# Sonagi Playgrounds - Example Runtime Agent Skill

이 문서는 `sonagi-playgrounds` 저장소에서 작업할 때 AI 에이전트(Opencode 등)가 준수해야 할 가이드라인입니다.

## 1. 프로젝트 정체성

- `sonagi-playgrounds`는 Sonagi 생태계의 **실행 가능한 예제 코드 단일 진실의 원천(SSOT)**입니다.
- 모든 예제는 `examples/` 하위에 있으며, 블로그(`llm-wiki`)와 디스코드 봇(`sonagi-bots`)이 이 저장소를 참조합니다.
- **예제 코드를 다른 저장소로 복사하지 마십시오.** 소비처는 항상 이 저장소를 URL로 참조합니다.

## 2. 런타임 라우팅 규칙 (가장 중요)

예제의 종류에 따라 실행 환경이 **고정되어 있습니다.** 임의로 바꾸지 마십시오.

| 예제 종류 | 실행 환경 | 근거 |
|---|---|---|
| React / Vanilla JS / UI 컴포넌트 | CodeSandbox, Sandpack | 브라우저 네이티브, 즉시 렌더링 |
| Python / 데이터 분석 (`*.ipynb`) | **JupyterLite** (GitHub Pages) | 서버 비용 0원, iframe 임베드 제약 없음 |
| 단순 텍스트 입출력 스크립트 | Piston (봇 `/play run`) | 시각적 결과물이 없을 때만 |

### Python 예제에 CodeSandbox를 쓰지 마십시오

과거에 시도했다가 실패한 경로입니다. 반복하지 마십시오. 상세 경위는
`llm-wiki/20_Wiki/Projects/Sonagi-Playgrounds-Sandbox-Architecture.md` 참조.

- CodeSandbox 브라우저 모드(Nodebox)에는 Python 커널이 없어 `.ipynb`가 JSON 텍스트로 표시됩니다.
- 하위 폴더에 `.devcontainer/` 또는 `sandbox.config.json`을 주입하면 `422 Unknown error`가 발생합니다.
- 저장소 전체를 Devbox로 여는 기능(`/p/github/...`)은 CodeSandbox에서 제거되었습니다.
- Google Colab은 `X-Frame-Options` 때문에 iframe 임베드가 불가능합니다. 링크 공유용으로만 쓰십시오.

## 3. JupyterLite 빌드 제약 (하드 룰)

`.github/workflows/deploy-jupyterlite.yml`이 `examples/`를 JupyterLite 사이트로 빌드합니다.
아래를 어기면 **빌드가 실패합니다.**

1. **의존성**: `jupyterlite-core`, `jupyterlite-pyodide-kernel`, `jupyter_server` 3개가 모두 필요합니다.
   `jupyter_server`가 없으면 `--contents` 처리 단계에서 `RuntimeError`로 죽습니다.
   (패키지명은 `jupyterlite-pyodide`가 아니라 `jupyterlite-pyodide-kernel`입니다.)
2. **빌드 명령**: 반드시 `--lite-dir .`를 명시하십시오. 생략하면 CI 러너가 상위 경로를
   기준으로 잡아 `FileNotFoundError`가 발생합니다.
   ```bash
   jupyter lite build --lite-dir . --contents examples --output-dir dist
   ```
3. **숨김 파일 금지**: `examples/` 하위에 `.vscode/`, `.codesandbox/` 같은 점(`.`)으로 시작하는
   폴더를 두지 마십시오. JupyterLite가 인덱싱을 거부하며 404로 빌드가 실패합니다.
   불가피할 경우 루트의 `jupyter_lite_config.json`에 `"allow_hidden": true`가 설정되어 있어야 합니다.

## 4. 경로 규약 (소비처 연동 시)

소비처(봇, 블로그)에 전달하는 경로에는 **`examples/` 접두사를 붙이지 않습니다.**

- GitHub API 트리는 `examples/python-test/test_notebook.ipynb`를 반환합니다.
- Cloudflare Worker API와 JupyterLite는 내부적으로 `examples/`를 이미 붙입니다.
- 접두사를 제거하지 않으면 `examples/examples/...`가 되어 404가 납니다.

```text
올바름:  python-test/test_notebook.ipynb
잘못됨:  examples/python-test/test_notebook.ipynb
```

## 5. 예제 폴더 표준 스펙

새 예제를 추가할 때:

- **프론트엔드**: 폴더에 독립적인 `package.json`과 `index.html`이 있어야 합니다.
  `npm install && npm run dev`가 그대로 동작해야 합니다.
- **Python**: `.ipynb` 파일과 `requirements.txt`를 같은 폴더에 둡니다.
  브라우저(Pyodide)에서 도는 순수 패키지만 쓰십시오. GPU/딥러닝 라이브러리는 동작하지 않습니다.

## 6. 소비처

| 소비처 | 연동 방식 |
|---|---|
| `llm-wiki` (블로그) | iframe 임베드 (JupyterLite) / Sandpack (프론트엔드) |
| `sonagi-bots` (디스코드) | `/play sandbox` 커맨드. 자동완성이 이 저장소 트리를 읽어갑니다 |
| 로컬 개발 | `git clone` 후 예제 폴더에서 `npm run dev` |

**디스코드는 iframe 임베드가 불가능합니다.** 봇은 링크 버튼 제공까지만 담당하고,
인터랙티브한 실행 화면은 블로그가 책임집니다.
