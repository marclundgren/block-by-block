#!/usr/bin/env python3
"""Flatten the single-page book (index.html) into one linear, print-styled
HTML document at dist/block-by-block.html. That file is the source for the
EPUB and PDF builds (see build-bundle.sh)."""
import re, html, pathlib

SRC = pathlib.Path("index.html").read_text()
OUT = pathlib.Path("dist"); OUT.mkdir(exist_ok=True)

# --- parse the curriculum manifest out of the page's JS ---
parts = []
for pid, title, sub, body in re.findall(
        r'\{ id:"(\d+)", title:"([^"]+)", sub:"([^"]+)", lessons:\[(.*?)\]\}', SRC, re.S):
    lessons = re.findall(r'\["([^"]+)","([^"]+)"\]', body)
    parts.append((pid, title, sub, lessons))

def template(tid):
    m = re.search(r'<template data-id="%s">(.*?)</template>' % re.escape(tid), SRC, re.S)
    return m.group(1) if m else "<div class='content'><p>(missing)</p></div>"

# --- assemble the linear body ---
chunks = []
# title page
chunks.append('''<section class="titlepage">
  <div class="logo">▦</div>
  <h1 class="booktitle">Block by Block</h1>
  <p class="booksub">Python &middot; Minecraft &middot; Full-Stack</p>
  <p class="bookby">A hands-on path from your first line of code to your own AI-powered Minecraft server.</p>
</section>''')

# table of contents
toc = ['<section class="toc"><h1>Contents</h1>']
n = 0
for pid, title, sub, lessons in parts:
    toc.append(f'<div class="toc-part">Part {pid}. {html.escape(title)}</div>')
    for lid, ltitle in lessons:
        n += 1
        toc.append(f'<div class="toc-row"><span>{pid}.{lessons.index((lid,ltitle))+1} {html.escape(ltitle)}</span></div>')
toc.append('<div class="toc-part">★ Secret Chapter. The AI Admin Console</div>')
toc.append('</section>')
chunks.append("\n".join(toc))

# parts + lessons
for pid, title, sub, lessons in parts:
    chunks.append(f'<section class="partpage"><div class="pnum">Part {pid}</div>'
                  f'<h1>{html.escape(title)}</h1><p>{html.escape(sub)}</p></section>')
    for i, (lid, ltitle) in enumerate(lessons, 1):
        chunks.append(f'<article class="lesson"><div class="kicker">Part {pid} &middot; {html.escape(title)}</div>'
                      f'<h1>{pid}.{i} &nbsp;{html.escape(ltitle)}</h1>{template(lid)}</article>')

# bonus chapter
chunks.append('<section class="partpage gold"><div class="pnum">★ Secret Chapter</div>'
              '<h1>The AI Admin Console</h1><p>Unlocked by finishing every lesson.</p></section>')
chunks.append(f'<article class="lesson"><div class="kicker">★ Secret Chapter</div>'
              f'<h1>The AI Admin Console</h1>{template("bonus")}</article>')

BODY = "\n".join(chunks)

CSS = '''
@page { margin: 22mm 18mm; }
:root{ --ink:#1f2328; --muted:#59636e; --line:#d1d9e0; --grass:#1f883d; --link:#0969da;
  --code-bg:#f6f8fa; --gold:#9a6700; --purple:#8250df; --amber:#9a6700; }
*{box-sizing:border-box}
body{font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:var(--ink);
  font-size:11pt;line-height:1.55;margin:0}
h1,h2,h3{font-weight:600;line-height:1.2}
a{color:var(--link);text-decoration:none}
code{font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:.85em;
  background:#eaeef2;padding:.1em .35em;border-radius:4px}
kbd{font-family:ui-monospace,monospace;font-size:.78em;background:#f6f8fa;border:1px solid var(--line);
  border-bottom-width:2px;border-radius:4px;padding:.05em .4em}
.titlepage{height:88vh;display:flex;flex-direction:column;justify-content:center;align-items:center;
  text-align:center;page-break-after:always}
.titlepage .logo{font-size:64pt;color:var(--grass);line-height:1}
.booktitle{font-size:40pt;margin:16px 0 6px;letter-spacing:-.02em}
.booksub{font-family:ui-monospace,monospace;color:var(--grass);font-size:13pt;margin:0}
.bookby{color:var(--muted);max-width:380px;margin:24px auto 0;font-size:12pt}
.toc{page-break-after:always}
.toc h1{font-size:22pt;border-bottom:2px solid var(--line);padding-bottom:8px}
.toc-part{font-weight:700;margin:16px 0 4px;color:var(--grass)}
.toc-row{display:flex;justify-content:space-between;color:var(--muted);font-size:10.5pt;padding:2px 0 2px 14px}
.partpage{page-break-before:always;padding-top:40mm}
.partpage .pnum{font-family:ui-monospace,monospace;color:var(--grass);font-weight:700;font-size:13pt}
.partpage h1{font-size:32pt;margin:6px 0;letter-spacing:-.02em}
.partpage.gold .pnum,.partpage.gold h1{color:var(--gold)}
.lesson{page-break-before:always}
.lesson>.kicker{font-family:ui-monospace,monospace;font-size:8.5pt;letter-spacing:.08em;
  text-transform:uppercase;color:var(--grass)}
.lesson>h1{font-size:20pt;margin:4px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line);letter-spacing:-.01em}
.content h2{font-size:15pt;margin:20px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line)}
.content h3{font-size:12.5pt;margin:16px 0 6px}
.content p{margin:9px 0;color:#3d444d}
.content ul,.content ol{color:#3d444d;padding-left:22px}
.content li{margin:4px 0}
.content strong{color:var(--ink)}
pre{background:var(--code-bg);border:1px solid var(--line);border-radius:6px;padding:10px 12px;
  overflow:hidden;white-space:pre-wrap;word-break:break-word;page-break-inside:avoid;margin:12px 0}
pre code{display:block;background:none;padding:0;font-size:9pt;line-height:1.5;color:#1f2328}
pre .bar{display:none}
code .c{color:#6e7781;font-style:italic} code .k{color:#cf222e} code .s{color:#0a3069}
code .f{color:#8250df} code .n{color:#0550ae} code .o{color:#cf222e} code .nd{color:#6639ba}
.box{border:1px solid var(--line);border-left:4px solid var(--muted);border-radius:6px;
  padding:10px 14px;margin:12px 0;font-size:10pt;page-break-inside:avoid}
.box .h{font-weight:700;font-size:9pt;display:block;margin-bottom:3px}
.box.note{border-left-color:var(--link)} .box.note .h{color:var(--link)}
.box.tip{border-left-color:var(--grass)} .box.tip .h{color:var(--grass)}
.box.warn{border-left-color:var(--amber);background:#fff8c5} .box.warn .h{color:var(--amber)}
.box.try{border-left-color:var(--purple)} .box.try .h{color:var(--purple)}
.box.try .h::before{content:"\\26CF  QUEST"}
.box .h:empty{margin:0}
'''

DOC = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Block by Block: Python, Minecraft, Full-Stack</title>
<style>{CSS}</style></head><body>{BODY}</body></html>'''

(OUT / "block-by-block.html").write_text(DOC)
print("wrote dist/block-by-block.html  (%d lessons + bonus)" % n)
