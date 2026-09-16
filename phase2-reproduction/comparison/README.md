# 원본 vs 재구현 비교 검증

검증 과정을 클로드 Linux 환경에서 진행하고자 했으나, 
아래 절차대로 직접 검증.
참고> Linux 환경에서는 `makeGraph2022.exe`(Windows PE32+ 실행파일)를 직접 실행할 수 없다. 
따라서 아래 절차는 **Windows 환경에서 사용자가 직접 수행**해야 한다.

## 절차

1. `original/makeGraph2022.exe`와 `phase1-compatible/samples/*.lst`를
   Windows PC로 복사한다.
2. 각 `.lst` 파일을 원본 EXE에 드래그&드롭하여 `.htm`을 생성한다.
   - 생성 파일을 `comparison/original/예제1.htm` 형태로 저장.
3. 동일한 `.lst`를 재구현판으로 변환한다.
   ```powershell
   python phase2-reproduction/makegraph.py samples/example.lst -o comparison/reimpl/example.html
   ```
4. 두 HTML을 같은 브라우저에서 열어 다음 항목을 비교하고 기록한다.

| 항목 | 원본 | 재구현 | 일치 여부 | 비고 |
|---|---|---|---|---|
| Normal layout 초기 배치 | | | | |
| Horizontal layout | | | | |
| Vertical layout | | | | |
| Node shape/color | | | | |
| Node icon 표시 (0/1/2) | | | | |
| Hyperlink 클릭 동작 | | | | |
| Relation arrow 스타일 | | | | |
| moving-arrows 애니메이션 | | | | 재구현은 점선으로 근사 |
| sequence 색상/굵기 | | | | |
| Relation label 표시 옵션 (0/1/2/3) | | | | |
| 오류 발생 시 화면 | | | | |

5. 차이가 발견되면 `phase2-reproduction/makegraph.py`를 수정하고
   `phase2-reproduction/tests/`에 회귀/검증 테스트를 추가한다.
   (`phase1-compatible/makegraph.py`는 건드리지 않는다 — 1차 안정 버전 보존.)

