# 🌩️ Sonagi Playgrounds (Sandbox Bridge)

**Sonagi Playgrounds**는 GitHub 저장소 내의 개별 예제(Subdirectory) 코드들을 즉석에서 **CodeSandbox** 환경으로 변환하여 실행할 수 있게 해주는 **서버리스 중개자(Bridge)**입니다. [Cloudflare Workers](https://workers.cloudflare.com/) 위에서 동작합니다.

---

## 🎯 도입 배경 (The Problem)

과거 `hotssi/sandbox` 등의 예제 코드를 관리할 때, GitHub의 서브디렉토리를 CodeSandbox로 직접 연결(`codesandbox.io/s/github/...`)하려 했으나 잦은 에러가 발생했습니다.
가장 큰 원인은 순수 바닐라(Vanilla JS) 예제나 단순 스니펫 폴더에 **`package.json`이나 `index.html`이 누락되어 있어 CodeSandbox 엔진이 빌드 환경을 인식하지 못하기 때문**이었습니다.

## 🌉 중개자(Bridge) 아키텍처 (The Solution)

이 문제를 해결하기 위해, 단순한 정적 파일 서빙을 넘어 실시간으로 환경을 패키징해주는 **Cloudflare Worker 기반의 Bridge API**를 구축했습니다.

1. **Request:** 사용자가 `/sandbox?path=Vanilla/counter` API를 호출합니다.
2. **Fetch:** Worker가 GitHub API를 통해 `sonagi-playgrounds/examples/Vanilla/counter` 폴더 내의 파일들을 긁어옵니다.
3. **Fallback Injection (핵심):**
   - 긁어온 파일 중 `package.json`이 없다면 가상의 패키지 설정을 동적으로 주입합니다.
   - `index.html`이 없다면 스크립트와 스타일시트를 연결한 기본 HTML 뼈대를 생성하여 주입합니다.
4. **Deploy:** 패키징된 JSON 페이로드를 **CodeSandbox Define API**로 전송합니다.
5. **Response:** 즉시 실행 가능한 고유의 Sandbox ID와 URL(`https://codesandbox.io/s/{id}`)을 반환합니다.

이를 통해 위키나 외부 문서에서 링크 클릭 한 번만으로, 불완전한 코드 조각들도 완벽한 브라우저 샌드박스 환경에서 구동됩니다.

---

## 🚀 API 엔드포인트 (Usage)

### `GET /sandbox?path={example_path}`

저장소의 `examples/` 폴더 하위에 있는 경로를 파라미터로 전달합니다.

**Request Example:**

```http
GET https://playgrounds.sonagi.space/sandbox?path=Vanilla/counter
```

**Response Example:**

```json
{
  "status": "success",
  "sandbox_url": "https://codesandbox.io/s/a1b2c3d4",
  "preview_url": "https://a1b2c3d4.csb.app",
  "sandbox_id": "a1b2c3d4"
}
```

---

## 🛠️ 개발 및 배포 (Development)

이 프로젝트는 `Wrangler`를 사용하여 로컬 테스트 및 배포를 진행합니다.

```bash
# 의존성 설치
npm install

# 로컬 개발 서버 실행
npm run dev

# Cloudflare 에 배포
npm run deploy
```

> **Note:** GitHub API의 Rate Limit 확장을 위해 `wrangler.toml` 또는 Cloudflare 대시보드에 `GITHUB_TOKEN` 환경변수를 세팅하는 것을 권장합니다.
