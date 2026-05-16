# 🤝 Handover: hotssi/sandbox Migration Project

이 문서는 `hotssi/sandbox` 저장소를 **CodeSandbox**로 완벽하게 이관하기 위한 다음 단계 지침서입니다.

## 1. 현재 상황 (Current State)
- **자산 발굴**: GitHub `hotssi/sandbox`에서 Vanilla JS, React, Design Patterns 예제들을 발굴함.
- **위키 등록**: `20_Wiki/_references/Code_Examples.md`에 모든 예제와 CodeSandbox 실행 링크를 등록함.
- **이슈 발생**: 현재 링크 클릭 시 CodeSandbox에서 `Something went wrong` 에러 발생. (원인: Stackblitz 전용 구조 혹은 서브디렉토리 설정 미비)

## 2. 해결 과제 (To-Do)
- **설정 보완**: 각 예제 폴더가 독립적으로 실행될 수 있도록 필요한 설정 파일(`package.json`, `index.html`)을 점검하고 보완하십시오.
- **링크 검증**: 위키 문서의 `[Run in Sandbox]` 링크가 실제로 브라우저에서 동작하는지 확인하십시오.
- **Trello 업데이트**: 작업 진행 상황을 `🏗️ Active Projects` 보드의 관련 카드에 기록하십시오.

## 3. 기술적 참고 사항
- CodeSandbox GitHub Import 규칙: `https://codesandbox.io/s/github/[USER]/[REPO]/tree/[BRANCH]/[PATH]`
- 서브디렉토리에 `package.json`이 없으면 CodeSandbox가 프로젝트 유형을 판단하지 못할 수 있습니다.

---
*Created by Gemini Agent on 2026-05-16*
