#!/usr/bin/env python3
# 把 docs 下所有 .md 转成黑底护眼 HTML（同名 .html），浏览器打开即可。
import os, glob, sys, re, html as _html

DOCDIR = os.path.dirname(os.path.abspath(__file__))

CSS = """
<style>
  :root { color-scheme: dark; }
  body { background:#121212; color:#e0e0e0; font-family:-apple-system,"PingFang SC","Microsoft YaHei",Segoe UI,sans-serif;
         line-height:1.75; max-width:860px; margin:0 auto; padding:40px 28px; font-size:16px; }
  h1,h2,h3,h4 { color:#fff; line-height:1.35; margin-top:1.6em; }
  h1 { border-bottom:2px solid #333; padding-bottom:.3em; }
  h2 { border-bottom:1px solid #2a2a2a; padding-bottom:.25em; }
  a { color:#5db0ff; }
  code { background:#1e1e1e; color:#ff9d6c; padding:2px 6px; border-radius:4px; font-size:.9em; }
  pre { background:#1a1a1a; border:1px solid #2a2a2a; padding:14px 16px; border-radius:8px; overflow:auto; }
  pre code { background:none; color:#c8e1c8; padding:0; }
  blockquote { border-left:4px solid #4a4a4a; margin:0; padding:.3em 1em; color:#b0b0b0; background:#171717; }
  table { border-collapse:collapse; width:100%; margin:1em 0; }
  th,td { border:1px solid #333; padding:8px 12px; text-align:left; }
  th { background:#1f1f1f; color:#fff; }
  tr:nth-child(even) td { background:#181818; }
  hr { border:none; border-top:1px solid #2a2a2a; margin:2em 0; }
  strong { color:#fff; }
  li { margin:.25em 0; }
</style>
"""

def convert(md_text):
    try:
        import markdown
        return markdown.markdown(md_text, extensions=['tables','fenced_code','sane_lists','nl2br'])
    except Exception:
        # 极简兜底（无 markdown 库时）：转义后处理标题/粗体/换行
        t = _html.escape(md_text)
        t = re.sub(r'^### (.*)$', r'<h3>\1</h3>', t, flags=re.M)
        t = re.sub(r'^## (.*)$', r'<h2>\1</h2>', t, flags=re.M)
        t = re.sub(r'^# (.*)$', r'<h1>\1</h1>', t, flags=re.M)
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        return '<p>' + t.replace('\n\n','</p><p>').replace('\n','<br>') + '</p>'

def main():
    files = [f for f in glob.glob(os.path.join(DOCDIR,'*.md'))]
    n = 0
    for f in files:
        with open(f, encoding='utf-8') as fh:
            md = fh.read()
        title = _html.escape(os.path.basename(f)[:-3])
        body = convert(md)
        out = f'<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>{title}</title>{CSS}</head><body>{body}</body></html>'
        with open(f[:-3]+'.html','w',encoding='utf-8') as oh:
            oh.write(out)
        n += 1
    print(f'转换完成 {n} 个文件 -> .html（黑底）')

if __name__ == '__main__':
    main()
