"""Build the Korean pages (/ko/...) from the English ones.

Each English page holds both languages; the Korean copy only differs in
<html lang>, and in the <head> block between the head:start / head:end
markers (title, description and link-preview tags in Korean).

Run after editing work/index.html, jev/index.html or scpc/index.html:
    python tools/make_ko.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://sweet-butters.github.io"

PAGES = {
    "work/index.html": {
        "out": "ko/work/index.html",
        "path": "/work/",
        "title": "정회광 · CRUD 노선",
        "description": "만든 것(C), 관심 있게 보는 것(R), 참여한 것(U), 없앤 불편함(D). 제 작업을 하나의 노선도로 정리했어요.",
        "og_title": "정회광 · AI로 만들고, 매일 돌아가게 합니다",
        "og_description": "매일 실제로 돌아가는 AI 서비스와 그 뒤의 판단, 대회와 강의를 CRUD 노선도로 정리한 작업 기록.",
        "og_image": f"{SITE}/work/img/radar.jpg",
    },
    "jev/index.html": {
        "out": "ko/jev/index.html",
        "path": "/jev/",
        "title": "Jev 실사용 기록 · 정회광",
        "description": "새로 나온 AI 모델 TypeSafe Jev를 AI 공모전 수집 서비스의 판정기로 실제 운영에 붙여 본 기록.",
        "og_title": "새로 나온 AI 모델 Jev를 실제 서비스의 판정기로 붙여 보다",
        "og_description": "공고 3,728건 판정, 규칙과 95% 같은 판단, 전체 비용 약 $0.11. 된 것과 안 된 것을 기록했어요.",
        "og_image": f"{SITE}/work/img/jev-results.jpg",
    },
    "scpc/index.html": {
        "out": "ko/scpc/index.html",
        "path": "/scpc/",
        "title": "SCPC AI 챌린지 · 정회광",
        "description": "2026 SCPC AI 챌린지 세 라운드에서 무엇을 만들었고 어떤 판단을 했는지, 제 말로 정리한 기록.",
        "og_title": "SCPC AI 챌린지: 예선 두 번을 넘어 본선 발표까지",
        "og_description": "언어모델 없는 규칙 엔진(비공개 채점 35위 / 127), 작업이 바뀌어도 기억을 이어 가는 안드로이드 비서, 그리고 본선 발표.",
        "og_image": f"{SITE}/work/img/scpc.jpg",
    },
}


def korean_head(page):
    url_en, url_ko = SITE + page["path"], SITE + "/ko" + page["path"]
    return f"""<!-- head:start (generated Korean head) -->
<title>{page['title']}</title>
<meta name="description" content="{page['description']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{page['og_title']}">
<meta property="og:description" content="{page['og_description']}">
<meta property="og:url" content="{url_ko}">
<meta property="og:image" content="{page['og_image']}">
<meta property="og:locale" content="ko_KR">
<link rel="canonical" href="{url_ko}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="ko" href="{url_ko}">
<!-- head:end -->"""


def build(src_name, page):
    src = (ROOT / src_name).read_text(encoding="utf-8")
    assert '<html lang="en"' in src, f"{src_name}: expected <html lang=\"en\""
    out = src.replace('<html lang="en"', '<html lang="ko"', 1)
    out = out.replace('data-default-lang="en"', 'data-default-lang="ko"', 1)
    out, n = re.subn(r"<!-- head:start.*?<!-- head:end -->", lambda _: korean_head(page), out, count=1, flags=re.S)
    assert n == 1, f"{src_name}: head markers not found"
    out = out.replace("<!doctype html>", f"<!doctype html>\n<!-- GENERATED from {src_name} by tools/make_ko.py. Edit that file, not this one. -->", 1)
    dest = ROOT / page["out"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    print(f"{src_name} -> {page['out']}")


if __name__ == "__main__":
    for name, page in PAGES.items():
        build(name, page)
