#!/usr/bin/env python3
"""content.toml -> index.html (웹판), --pdf 면 전화번호를 넣은 인쇄판을 헤드리스 Chrome으로 PDF로 뽑는다.

  python build.py [content.toml]
  RESUME_PHONE=010-0000-0000 python build.py --pdf [--out ../resume.pdf]
"""
import argparse, os, re, subprocess, sys, tomllib
from html import escape as e
from pathlib import Path

import markdown  # pip install markdown

HERE = Path(__file__).resolve().parent
CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


# 기간(2023.07 ~ 2024.06)과 「1년 차」는 줄 끝에서 갈라지지 않게 붙인다
NOBREAK = re.compile(r"\d{4}\.\d{2} ~ (?:\d{4}\.\d{2}|현재)|\d+년 차")


def nobreak(html):
    return NOBREAK.sub(lambda m: m.group(0).replace(" ", "\u00a0"), html)


def md(text):
    return nobreak(markdown.markdown((text or "").strip()))


def item_html(it, default_layout):
    lay = it.get("layout", default_layout)
    top = lay.startswith("top")
    dcol = "col-xs-12 col-print-12" if top else "col-xs-12 col-sm-4 col-md-3 col-print-12"
    ccol = "col-xs-12 col-print-12" if top else "col-xs-12 col-sm-8 col-md-9 col-print-12"
    d = ""
    for k in ("name", "company"):
        if it.get(k):
            d += f"<h4>{e(it[k])}</h4>"
    if it.get("link"):
        d += f'<a href="{e(it["link"])}" target="_blank" class="link">{e(it.get("link_text", it["link"]))}</a>'
    for k in ("job_title", "qualification"):
        if it.get(k):
            d += f"<p><b>{e(it[k])}</b></p>"
    if it.get("dates"):
        d += "<p>" + "<br/>".join(nobreak(e(x)) for x in str(it['dates']).split("\n")) + "</p>"
    c = f'<p class="quote">{e(it["quote"])}</p>' if it.get("quote") else ""
    c += md(it.get("description"))
    return (f'<div class="row clearfix layout layout-{e(lay)}">\n'
            f'  <div class="{dcol} details">{d}</div>\n'
            f'  <div class="{ccol}">{c}</div>\n</div>\n')


def section_html(s):
    out = f'<div class="container">\n  <h3>{e(s["title"])}</h3>\n'
    if s.get("quote"):
        out += f'  <p class="quote">{e(s["quote"])}</p>\n'
    if s.get("content"):
        out += f'  <div class="row clearfix"><div class="col-md-12">{md(s["content"])}</div></div>\n'
    for it in s.get("items", []):
        out += item_html(it, s.get("layout", "left"))
    return out + "</div>\n"


def render(c, phone=None):
    icons = "".join(
        f'<li><a target="_blank" href="{e(i["url"])}" class="button button--sacnite button--round-l">'
        f'<i class="fab fa-{e(i["icon"])}" title="{e(i["icon"])}"></i></a></li>'
        for i in c.get("icons", []))
    contact = f'<p>Email: <a href="mailto:{e(c["email"])}" target="_blank">{e(c["email"])}</a></p>'
    for label, url in c.get("links", {}).items():
        contact += f'<p>{e(label)}: <a href="{e(url)}" target="_blank">{e(url)}</a></p>'
    if phone:
        contact += f'<p>Phone: <a href="tel:{e(phone.replace("-", ""))}">{e(phone)}</a></p>'  # 링크로 둬서 다른 연락처 값과 같은 굵기

    about = c.get("about", {})
    img = about.get("profile_image")
    about_html = ""
    if about:
        pic = (f'<div class="col-xs-12 col-sm-4 col-md-3 no-print"><span class="profile-img" '
               f'style="background-image: url({e(img)})"></span></div>') if img else ""
        col = "col-xs-12 col-sm-8 col-md-9 col-print-12" if img else "col-xs-12 col-print-12"
        about_html = (f'<div class="container intro-container">\n  <h3>{e(about.get("title", "About Me"))}</h3>\n'
                      f'  <div class="row clearfix">{pic}<div class="{col}">{md(about.get("content"))}</div></div>\n</div>\n')

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(c["name"])} | {e(c["title"])}</title>
  <meta name="description" content="{e(c.get("description", c["title"]))}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <link rel="stylesheet" href="assets/main.css">
  <link rel="stylesheet" href="assets/ko.css">
</head>
<body>
<div class="container header-container">
  <div class="row">
    <div class="col-xs-12 col-sm-6 col-md-6 col-lg-8 header-left">
      <h1>{e(c["name"])}</h1>
      <h2>{e(c["title"])}</h2>
    </div>
    <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4 header-right">
      <ul class="icons no-print">{icons}</ul>
      {contact}
    </div>
  </div>
</div>
<main class="page-content" aria-label="Content"><div class="wrapper">
{about_html}{"".join(section_html(s) for s in c.get("sections", []))}</div></main>
<div class="container footer-container">
  <p>{e(c["name"])} - <a href="mailto:{e(c["email"])}" target="_blank">{e(c["email"])}</a></p>
  <p class="no-print"><small>Template: <a href="https://github.com/jojoldu/jojoldu.github.io">jojoldu/jojoldu.github.io</a> (GPL-3.0),
    <a href="https://github.com/sproogen/modern-resume-theme">sproogen/modern-resume-theme</a> (MIT)</small></p>
</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content", nargs="?", default=HERE / "content.toml", type=Path)
    ap.add_argument("--pdf", action="store_true", help="전화번호를 넣은 인쇄판 PDF도 만든다")
    ap.add_argument("--phone", default=os.environ.get("RESUME_PHONE"), help="기본값: 환경변수 RESUME_PHONE")
    ap.add_argument("--out", type=Path, default=HERE.parent / "resume.pdf", help="PDF 경로 (사이트 폴더 밖 권장)")
    a = ap.parse_args()

    c = tomllib.loads(a.content.read_text(encoding="utf-8"))
    (HERE / "index.html").write_text(render(c), encoding="utf-8")
    print("index.html")
    if not a.pdf:
        return
    if not a.phone:
        sys.exit("--pdf 에는 --phone 또는 RESUME_PHONE 이 필요하다")
    chrome = next((p for p in CHROMES if Path(p).exists()), None)
    if not chrome:
        sys.exit("Chrome/Chromium/Edge 를 찾지 못했다")
    tmp = HERE / ".print.html"  # 전화번호가 든 파일. 출력 뒤 바로 지운다
    tmp.write_text(render(c, a.phone), encoding="utf-8")
    try:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=10000", f"--print-to-pdf={a.out.resolve()}",
                        tmp.as_uri()], check=True, capture_output=True)
    finally:
        tmp.unlink(missing_ok=True)
    print(a.out)


if __name__ == "__main__":
    main()
