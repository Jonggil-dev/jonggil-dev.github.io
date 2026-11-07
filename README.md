# 웹 이력서 (정종길)

이동욱 님 이력서 템플릿(jojoldu.github.io)과 같은 모양의 정적 사이트. Jekyll 없이 `index.html` 하나로 열리고, GitHub Pages에 그대로 올리면 된다.

## 파일
- `content.toml`: 이력서 내용(직접 만든다). 형식과 칸 설명은 `content.example.toml` 주석에 있다.
- `build.py`: `content.toml` → `index.html`. `--pdf` 를 주면 전화번호를 넣은 인쇄판 PDF도 만든다.
- `assets/main.css`: 템플릿이 쓰는 CSS 원본(https://jojoldu.github.io/assets/main.css). 바꾼 곳은 bootstrap 불러오는 주소 하나(CDN → 같은 폴더 `bootstrap.min.css`).
- `assets/ko.css`: 한글 글꼴, 낱말 단위 줄바꿈, A4 인쇄와 쪽 나눔 규칙. 모양을 고칠 때는 이 파일만 고친다.

## 사용법
```bash
python3 -m venv .venv && .venv/bin/pip install markdown   # 처음 한 번
cp content.example.toml content.toml                      # 내용 채우기
.venv/bin/python build.py                                  # 웹판 index.html
RESUME_PHONE=010-0000-0000 .venv/bin/python build.py --pdf --out ~/Desktop/정종길_이력서.pdf
```
- 웹판과 PDF판의 차이는 머리말 오른쪽 `Phone:` 한 줄뿐이다. 전화번호는 내용 파일에 쓰지 않고 `--phone` 이나 `RESUME_PHONE` 으로만 넣는다. 전화번호가 든 임시 HTML(`.print.html`)은 출력 뒤 지운다.
- PDF 기본 경로는 사이트 폴더 밖(`../resume.pdf`)이다. 폴더 안에 두면 사이트와 함께 공개될 수 있다.
- PDF는 설치된 Chrome(없으면 Chromium, Edge)의 헤드리스 `--print-to-pdf` 로 뽑는다. A4, 여백 14mm x 12mm.
- 확인: `pdffonts 이력서.pdf` 에 Pretendard 계열만 보이면 정상이다(영문도 Pretendard로 통일).

## 글꼴
- 템플릿은 Roboto만 지정해서 한글은 OS 기본 글꼴(맥 Apple SD Gothic Neo, 윈도 맑은 고딕)로 나온다.
- 여기서는 `Roboto, Pretendard, Noto Sans KR, ...` 순서로 둔다. 영문은 Roboto, 한글은 Pretendard.
- 웹판은 Pretendard를 jsDelivr CDN으로 불러온다. CDN CSS가 `local()` 을 먼저 보므로 Pretendard가 설치된 맥에서는 PDF도 설치 글꼴로 나온다.

## 원본 템플릿과 다른 점
- 뺀 것: Google Analytics, utterances 댓글, Fork me 리본, 다크 모드 스크립트, 「References on request」.
- 인쇄판: 회사 칸과 내용 칸을 1:3으로 고정(원본은 반반으로 눌림), 양쪽 맞춤 대신 왼쪽 맞춤, `<mark>` 강조 유지(원본은 bootstrap 인쇄 규칙 때문에 사라짐), 섹션 제목 뒤 쪽 나눔 금지, 불릿 한 줄 중간 잘림 금지(항목 블록은 쪽을 넘어갈 수 있음).
- 섹션은 고정 목록이 아니라 `[[sections]]` 를 적은 순서대로 나온다.

## 출처와 라이선스
- 이 사이트는 https://github.com/jojoldu/jojoldu.github.io (GPL-3.0, 이동욱)의 레이아웃과 CSS를 가져와 고친 것이라 GPL-3.0을 따른다. 전문은 `LICENSE`.
- 그 템플릿의 테마는 https://github.com/sproogen/modern-resume-theme (MIT, James Grant).
- `assets/bootstrap.min.css`: Bootstrap 3.3.5 (MIT, Twitter). 글꼴: Roboto(Google Fonts, Apache-2.0), Pretendard(OFL-1.1). 아이콘: Font Awesome 5 (CDN).
- 페이지 맨 아래(화면에서만)에 템플릿 출처 링크를 둔다.

## 알려진 한계
- Roboto, Font Awesome, Pretendard(미설치 환경)는 CDN에서 받는다. 오프라인이면 영문도 Pretendard나 OS 글꼴로 바뀌고 아이콘이 빠진다.
- 한글 기울임(quote 줄)은 Pretendard에 이탤릭이 없어 브라우저가 기울여 그린다(원본도 같음).
- 왼쪽 칸(인쇄 때 25%)에 긴 URL을 넣으면 중간에서 접힌다. `link_text` 로 짧게 보이게 할 수 있다.
- 쪽 나눔은 항목 단위로만 막는다. 항목 하나가 한 쪽보다 길면 그 안에서 잘린다.
- 마크다운은 Python-Markdown 기준이라 Jekyll(kramdown)과 미세하게 다를 수 있다. 문단 바로 뒤 목록은 빈 줄을 하나 둬야 목록이 된다.
