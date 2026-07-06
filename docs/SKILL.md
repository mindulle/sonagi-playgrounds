# Skill: sonagi-playgrounds

## 1. 개요 (Overview)

`sonagi-playgrounds`는 Cloudflare Workers 환경에서 구동되는 동적 샌드박스 백엔드(API) 서비스입니다. GitHub에 등록된 바닐라 예제 코드를 CodeSandbox, 혹은 자체 Sandbox 환경으로 동적 변환하여 제공하는 역할을 담당합니다.

## 2. 테스트 환경 (Testing)

이 프로젝트는 **Vitest**와 **@cloudflare/vitest-pool-workers**를 사용하여 Cloudflare Workers 환경을 에뮬레이션합니다.

- **테스트 실행 명령어**: `npm run test` (단발성) / `npm run test:watch` (실시간 반영)
- **테스트 파일 작성 규칙**: `*.test.ts` 네이밍을 따르며, `import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test'` 구문을 사용해 가상 환경을 셋업합니다. API 수정 시 반드시 E2E 형식의 Worker 테스트 코드를 함께 보강해야 합니다.

## 3. Git Hooks (Husky & Lint-staged)

사전 설정된 Husky Hook이 작동 중입니다.

- **Pre-commit Hook**: 커밋 생성 전 `npx lint-staged`가 실행되어 코드 포맷팅(Prettier)과 린트(ESLint)를 강제로 체크합니다. 추가로 테스트 스위트가 통과하는지 검증하는 구문을 추가해 두었습니다.

## 4. 아키텍처 가이드라인 (Architecture Guidelines)

- **현재 샌드박스 연동 (CodeSandbox)**
  - `/sandbox` 엔드포인트는 `examples` 디렉토리 하위의 파일들을 스캔하여 페이로드를 생성합니다.
  - **제약사항**: 과거 로직은 `index.js`, `index.html`, `style.css` 3가지만 하드코딩으로 패치했습니다.
  - **향후 고도화 목표 (CEO-289 연장선)**: GitHub REST API (또는 Repository 스캔)를 통해 `package.json`, 다중 컴포넌트, 훅(Hooks) 등 다양한 형태의 폴더를 스캔하여 동적으로 페이로드를 조립하도록 확장해야 합니다.
