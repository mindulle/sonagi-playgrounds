---
title: "인터랙티브 디자인 랩 (Interactive Design Labs)"
category: Design
tags: [labs, tools, interactive, html, scripts]
description: "로고 작도, 뼈대 뷰어, 그리드 팩토리를 자동화하는 HTML/Python 도구 모음"
---

# 🧪 인터랙티브 디자인 랩 (Interactive Labs)

이곳은 정적인 마크다운 문서를 넘어, 브라우저에서 직접 로고와 그리드, 컴포넌트의 변이를 눈으로 보고 통제할 수 있는 **HTML 기반의 인터랙티브 도구 모음**입니다.

과거 `10_Sources/assets/`에 흩어져 있던 방대한 Python 생성 스크립트와 HTML 대시보드들을 PARA 구조에 맞게 완벽하게 통합했습니다. 

---

## 📺 라이브 대시보드 (Live Preview)

위키 안에서 직접 HTML 랩실을 시각적으로 구동할 수 있습니다. (※ 옵시디언 환경에 따라 렌더링에 시간이 걸릴 수 있습니다.)

### 1. Sonagi V4.0 Brand Kit (Matrix Edition)
<iframe src="./branding/v4.0_matrix/brand_presentation_v4.html" width="100%" height="500px" style="border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 20px;"></iframe>

### 2. Grid Arsenal Dashboard
<iframe src="./grids/grid_arsenal.html" width="100%" height="500px" style="border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 20px;"></iframe>

---

## 🏢 1. 브랜딩 팩토리 (Branding Labs)
로고, 워드마크, 타이포그래피의 비율과 배열을 실험하는 곳입니다.
*   **V4 Matrix 버전 (가장 최신)**
    *   [Brand Presentation V4](./branding/v4.0_matrix/brand_presentation_v4.html): V4 브랜드 에셋 마스터 프레젠테이션
    *   [Ultimate Matrix Lab](./branding/v4.0_matrix/ultimate_matrix_lab.html): 그리드 매트릭스 변이 실험실
    *   [True Grid Variations](./branding/v4.0_matrix/true_grid_variations_lab.html): 엄격한 그리드 기반 로고 변주 테스트
*   **V3 이전 버전**
    *   [Ultimate Fusion Logo](./branding/v3.0/ultimate_fusion_logo.html)
    *   [Typography Grid Proof](./branding/v3.0/typography_grid_proof.html)

---

## 📐 2. 기하학 그리드 도구 (Grids Labs)
마스터 그리드 도감(`LOGO_00_Master_Grid_Arsenal`)을 살아 움직이게 만드는 뷰어 및 생성기입니다.
*   [Grid Arsenal Dashboard](./grids/grid_arsenal.html): 바우하우스, 피보나치, 방사형 등 블루프린트 그리드 SVG 뷰어
*   [Bento Dashboard](./grids/bento_dashboard.html): 벤토(Bento) 스타일의 UI 매크로 레이아웃 테스트
*   [Spectacular Variations Lab](./grids/spectacular_variations_lab.html)

> 💡 **참고**: `grids` 폴더 안에는 `blueprint-grid-bauhaus.svg`, `blueprint-grid-fibonacci.svg` 등 **고해상도 투명 SVG 그리드 원본 파일**들이 10개 이상 들어 있습니다! 언제든 ComfyUI에 던져넣고 사용할 수 있습니다.

---

## 🔣 3. 아이콘 및 심볼 랩 (Icons Labs)
소나기(Sonagi) 전용 아이콘 세트와 기하학적 뼈대를 실험하는 랩실입니다.
*   [Sonagi Master Board](./icons/sonagi_master_board.html): 코어 아이콘 전체 마스터 보드
*   [Sonagi Sticker Sheet V2](./icons/sonagi_sticker_sheet_v2.html): 아이콘 스티커 시트 (웹용)
*   [Commercial Benchmark](./icons/sonagi_vs_commercial_benchmark.html): 상용 아이콘(Material, Apple 등)과의 시각적 밸런스 벤치마크 테스트
*   [Logo Grid Analysis](./icons/test_logo_grid_analysis.html): 로고 뼈대와 회전(Rotation) 분석 도구

---
**관련 문서**
- [[LOGO_00_Master_Grid_Arsenal]] (로고 마스터 그리드 이론)
- [[Core-Color-Palette]] (소나기 코어 컬러 팔레트)