# 🌩️ Sonagi Playgrounds

**Sonagi Playgrounds**는 프론트엔드 UI 컴포넌트, 인터랙션 패턴, 바닐라 JS 로직 등 다양한 예제와 보일러플레이트를 모아둔 **단일 진실의 원천(SSOT, Single Source of Truth)** 저장소입니다.

단순한 코드 조각 보관소를 넘어, **어떤 플랫폼에서든 1초 만에 실행을 보장**하도록 모든 예제가 표준화(Normalization)되어 있습니다.

---

## 🎯 비전 및 소비처 (The Vision & Consumers)

모든 예제 폴더는 독립적인 `package.json`과 `index.html`을 갖춘 표준 규격으로 정규화되어 있어, 특정 플랫폼이나 브릿지(Bridge) 서버에 종속되지 않고 다양한 채널에서 즉시 소비될 수 있습니다.

1. **블로그 (LLM-Wiki)**
   - `Sandpack` 라이브러리를 통해 마크다운 문서 내에 '살아있는 문서(Living Docs)' 형태로 즉시 임베드(Embed)됩니다.
   - 독자는 위키를 읽으며 별도의 새 창 없이 바로 코드를 수정하고 결과를 확인할 수 있습니다.
2. **디스코드 & 협업 플랫폼 (Discord/Slack)**
   - CodeSandbox의 GitHub 연동 URL을 통해 디스코드 채팅창에 던지면, 썸네일과 함께 즉시 구동 가능한 Rich Embed 형태로 제공됩니다.
3. **AI 코딩 에이전트 (Cursor, OpenCode 등)**
   - 에이전트가 새로운 UI나 기능을 구현할 때, 이 저장소의 특정 폴더를 템플릿으로 복사(Scaffold)하여 0에서부터 설정하는 시간을 단축합니다.
4. **로컬 개발 환경 (Local Dev)**
   - 팀원이 `git clone` 후 원하는 예제 폴더에서 `npm run dev`만 입력하면 1초 만에 로컬 테스트 환경이 구축됩니다.

---

## 🏗️ 아키텍처 및 정규화 스펙 (Architecture & Normalization)

과거에는 불완전한 코드 스니펫을 실행하기 위해 별도의 서버리스 브릿지(Cloudflare Worker)가 `package.json`을 동적 주입하는 우회 방식을 사용했습니다. 
현재는 **모든 예제 폴더가 독립 실행 가능한 표준 규격으로 완전 정규화(CEO-1073)** 되었습니다.

* **표준 스펙:**
  - 모든 디렉토리는 고유의 `package.json`을 가집니다.
  - 최상단 진입점인 `index.html` (및 `vite.config.js`)이 존재합니다.
  - `npm install && npm run dev` 호환성을 100% 보장합니다.

## 🚀 사용 방법 (Usage)

### CodeSandbox (GitHub Import)를 통한 즉시 실행
원하는 예제의 GitHub 경로를 CodeSandbox URL 규칙에 맞춰 호출하면 서버 없이 즉시 브라우저 상에서 빌드 및 실행됩니다.

**URL 구조:**
`https://codesandbox.io/s/github/mindulle/sonagi-playgrounds/tree/main/examples/{분류}/{예제명}`

**Preview 전용 모드 (UI 없는 클린 렌더링):**
URL 끝에 `?view=preview` 파라미터를 추가하여 무거운 에디터 UI 없이 순수 결과물만 Iframe으로 임베드할 수 있습니다.
