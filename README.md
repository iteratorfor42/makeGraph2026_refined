# makeGraph2026_refined

한국학중앙연구원 디지털인문학연구소의 `makeGraph2022.exe`를 현대 Python 환경에서
사용할 수 있도록 재구현하는 프로젝트이다.

기존 MakeGraph2022는 온톨로지 설계 스크립트(`.lst`)를 읽어 Vis.js 기반 네트워크
그래프 HTML을 생성하는 교육용 도구이다.

이 프로젝트는 기존 프로그램의 실행 환경에 대한 의존성을 줄이고, 현재 Python
환경에서 동일한 `.lst` 데이터를 활용할 수 있도록 하는 것을 목표로 한다.

> 본 재구현은 공개된 사용 설명서(매뉴얼)에 기술된 입력 문법과 동작 규칙만을
> 근거로 한 클린룸(clean-room) 구현이다. 
> `original/makeGraph2022.exe`는 비교 검증을 위한 참고 자료로만 보관하며,
> 내부 코드를 역컴파일하거나 그대로 이식하지 않는다.

---

## 1. 프로젝트 구조

```text
makeGraph2026_refined/
│
├─ README.md
│
├─ original/
│  └─ makeGraph2022.exe          # 원본 보관 (수정하지 않음)
│
├─ phase1-compatible/            # 1차: 실용적 현대화
│  ├─ makegraph.py
│  ├─ samples/
│  │  ├─ example.lst             # 매뉴얼 "전체 예제"
│  │  ├─ example-icons.lst       # 아이콘/시퀀스/표시옵션 예제
│  │  └─ example-error.lst       # 오류 검증 테스트
│  └─ output/
│
└─ phase2-reproduction/          # 2차: 원본과의 동작 재현 검증
   ├─ makegraph.py               # (phase1 기반, 원본 비교 후 조정)
   ├─ tests/
   ├─ samples/
   ├─ output/
   └─ comparison/                # 원본 vs 재구현 결과 비교 자료
```

### 왜 1차/2차를 분리하는가

- **1차 (`phase1-compatible`)**: 실용성·호환성 우선. "Python에서 기존 `.lst`를
  읽어 그래프를 생성한다"가 목표.
- **2차 (`phase2-reproduction`)**: 원본과의 동작 일치성 우선. 같은 `.lst`를
  원본 EXE와 재구현판에 각각 입력해 레이아웃/스타일/오류 처리를 비교한다.

`original/`은 절대 수정하지 않는 원본 보관 영역이다.

---

## 2. 원본 프로그램 개요

* 온톨로지 설계 방식의 네트워크 그래프 작성 도구
* Vis.js Network Library 사용
* `.lst` 형식의 온톨로지 스크립트 입력 (UTF-8)
* HTML 네트워크 그래프 생성
* Class별 노드 스타일, Relation별 화살표 지정
* Node hyperlink / icon 지원
* Normal / Horizontal / Vertical 레이아웃 지원

바이너리 분석 결과 Python 3.6 + PyInstaller로 패키징된 프로그램으로 확인되었다.
최신 Windows 환경에서 이 레거시 실행 구조와의 호환성 문제가 발생할 수 있어
재구현이 필요하다.

---

## 3. 개발 환경

```text
Python : 3.12+ (표준 라이브러리만 사용, 외부 패키지 불필요, 개발 검증 환경 : Python 3.14.6)
출력   : HTML + Vis.js (CDN 기본, --vis-js로 오프라인 사용 가능)
```

---

## 4. 1차 구현 — 지원 기능

* `#Project` / `#Class` / `#Relation` / `#Nodes` / `#Links` / `#End`
* UTF-8 입력, 홑따옴표(`'`) 금지 검증
* Class 색상 / node shape (`box`, `circle`, `ellipse`, `star`, `triangle`,
  `square`, `dot`, `text`)
* Relation 설명(다른 이름) / 화살표 모양
  (`arrow`, `inverse`, `both`, `moving-arrows`, `line`, `sequence`)
* Relation 표시 옵션 `0/1/2/3` (이름 숨김 / 이름 / 설명 / 이름+설명)
* Node hyperlink, icon, 표시 옵션 `0/1/2` (hover 아이콘 / 아이콘 / 원형 아이콘)
* Normal / Horizontal / Vertical 레이아웃 전환 버튼
* 섹션 미정의, Class/Relation/Node 참조 무결성, 인코딩 오류 검증 →
  오류를 네트워크 그래프 형태로 표시

---

## 5. 실행 방법

```powershell
cd phase1-compatible
python makegraph.py samples/example.lst
```

결과: `samples/example.html` (입력 파일과 동일한 이름, 확장자만 `.html`)

출력 경로 지정:

```powershell
python makegraph.py samples/example.lst -o output/result.html
```

오프라인 사용 (로컬 vis-network.min.js 사용):

```powershell
python makegraph.py samples/example.lst --vis-js vis-network.min.js
```

---

## 6. MakeGraph 온톨로지 스크립트 문법 요약

```text
#Project
h1 그래프 제목

#Class
사람 blue circle
동물 red box

#Relation
likes 좋아한다 arrow
isPreviousTo ~보다_먼저이다 sequence

#Nodes
철수 사람 철수 files/sample1.htm#Cheol-su files/Cheol.png 1

#Links
철수 영이 likes

#End
```

* 모든 이름(범주/관계성/노드 식별자/레이블)에는 공백 대신 `_`를 사용한다.
* 홑따옴표(`'`)는 어디에서도 사용할 수 없다.
* Node/Link는 반드시 먼저 정의된 Class/Relation/Node를 참조해야 한다.

자세한 필드 구조는 `phase1-compatible/samples/*.lst` 예제를 참고한다.

---

## 7. 2차 구현 (원본 재현 검증)

`phase2-reproduction/`에서는 다음을 비교·검증한다.

1. Normal / Horizontal / Vertical layout
2. Node shape / color / icon / circular icon / hyperlink
3. Relation arrow, moving-arrows, sequence, label/description 표시
4. 오류 처리 방식과 오류 메시지
5. HTML 구조 및 Vis.js 옵션

같은 `.lst`를 원본 EXE(Windows 환경 필요)와 재구현판에 각각 입력한 뒤
`comparison/`에 스크린샷·결과 HTML을 나란히 저장해 차이를 기록한다.
Windows 환경이 없는 경우, `phase2-reproduction/tests/`의 자동화 테스트로
재구현판 자체의 회귀를 검증한다.

---

## 8. 원본과의 차이 (알려진 한계)

* Vis.js 버전 차이로 인한 물리 엔진/레이아웃 미세 차이
* `moving-arrows`는 원본의 애니메이션 대신 점선(dashed) 화살표로 근사 구현
  (2차에서 애니메이션 재현 여부 검토)
* HTML/CSS 마크업 구조는 원본과 동일하지 않음
* 오류 메시지 문구는 원본과 다를 수 있음 (기능적으로는 동일한 4가지 오류
  유형을 검증: 잘못된 섹션명 / 미정의 Class / 미정의 Relation / 미정의 Node)

이러한 차이는 2차 구현에서 원본과 나란히 비교하며 좁혀 나간다.

---

## 9. 라이선스 및 출처

본 프로젝트는 MakeGraph2022의 공개된 사용법과 입력 형식을 참고한 호환 구현이다.
원본 MakeGraph2022는 한국학중앙연구원 디지털인문학연구소에서 개발되었으며,
원본 안내에 따라 이 도구로 제작한 그래프를 사용할 경우 
Vis.js 및 디지털인문학연구소의 온톨로지 스크립트 변환기 출처를 표시할 것을 권장한다. 
원본 프로그램 및 Vis.js의 라이선스·저작권 조건을 확인한 후 배포 범위를 결정해야 한다.
