#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朗诵演讲类·双语稿图文卡引擎（复用card-templates/gen_cards.py的Chrome无头截图零成本管线）
用法：python3 gen_recitation_cards.py <topic_key>
topic_key 取 TOPICS 里的键；换数据就出新系列，不用改脚本。
"""
import os, subprocess, tempfile, html as _H, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '"PingFang SC","Microsoft YaHei",sans-serif'
W, H = 1080, 1440

def e(s): return _H.escape(str(s))

def render(html_body, out, w=W, h=H):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = f"<!doctype html><meta charset=utf-8><style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:{w}px;height:{h}px;overflow:hidden}}</style>{html_body}"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(doc); tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=2", f"--window-size={w},{h}", f"--screenshot={out}", f"file://{tmp}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)

DISCLAIMER = "原创双语朗诵稿 · 仅供亲子跟读练习参考"

def cover(theme, title_en, title_cn, hook_cn, series_tag):
    bg = theme["cover_bg"]; acc = theme["accent"]; gold = theme["gold"]
    return f'''<div style="position:relative;width:{W}px;height:{H}px;background:{bg};overflow:hidden;color:#fff">
<div style="position:absolute;top:64px;left:64px;background:{acc};padding:12px 30px;border-radius:30px;font-size:26px;font-weight:800">YiYi英语 · {e(series_tag)}</div>
<div style="position:absolute;top:0;left:0;right:0;height:520px;display:flex;align-items:center;justify-content:center">
  <div style="font-size:260px;line-height:1">🇨🇳</div>
</div>
<div style="position:absolute;top:560px;left:70px;right:70px;text-align:center">
  <div style="font-size:64px;font-weight:900;color:{gold};line-height:1.25">{e(hook_cn)}</div>
</div>
<div style="position:absolute;top:820px;left:60px;right:60px;text-align:center">
  <div style="font-size:92px;font-weight:900;line-height:1.2">{e(title_en)}</div>
  <div style="font-size:52px;font-weight:800;color:{gold};margin-top:18px">{e(title_cn)}</div>
</div>
<div style="position:absolute;top:1200px;left:80px;right:80px;text-align:center;font-size:40px;font-weight:800;background:rgba(255,255,255,.12);border-radius:24px;padding:26px">双语朗诵稿 · 逐句对照 · 可收藏可打印</div>
<div style="position:absolute;bottom:36px;left:0;right:0;text-align:center;font-size:24px;color:rgba(255,255,255,.7)">{DISCLAIMER}</div>
</div>'''

def lines_card(theme, idx, total, pairs):
    bg = theme["card_bg"]; acc = theme["accent"]; ink = theme["ink"]
    rows = ""
    for en, cn in pairs:
        rows += f'''<div style="background:#fff;border-left:14px solid {acc};border-radius:22px;padding:44px 44px;margin-bottom:36px;box-shadow:0 10px 26px rgba(0,0,0,.08)">
<div style="font-size:58px;font-weight:900;color:{ink};line-height:1.35">{e(en)}</div>
<div style="font-size:42px;color:#8a6a55;font-weight:700;margin-top:18px">{e(cn)}</div>
</div>'''
    return f'''<div style="position:relative;width:{W}px;height:{H}px;background:{bg};overflow:hidden;display:flex;flex-direction:column">
<div style="padding:70px 56px 0;flex:none">
<div style="position:absolute;top:60px;right:56px;background:{acc};color:#fff;font-size:28px;font-weight:800;padding:10px 26px;border-radius:24px">{idx}/{total}</div>
<div style="font-size:44px;font-weight:900;color:{ink};margin-bottom:0">My Motherland 我的祖国</div>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:0 56px">{rows}</div>
<div style="flex:none;padding-bottom:44px;text-align:center;font-size:24px;color:#a8815e">{DISCLAIMER}</div>
</div>'''

def cta_card(theme, cta_text, sub_text):
    bg = theme["cta_bg"]; gold = theme["gold"]
    return f'''<div style="position:relative;width:{W}px;height:{H}px;background:{bg};color:#fff;overflow:hidden;display:flex;flex-direction:column">
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0 64px;text-align:center">
<div style="font-size:76px;font-weight:900;line-height:1.3;margin-bottom:56px">想要这份<br><span style="color:{gold}">《我的祖国》</span>全文？</div>
<div style="background:rgba(255,255,255,.14);border-radius:28px;padding:48px 40px;font-size:46px;font-weight:800;line-height:1.6;width:100%">{e(cta_text)}</div>
<div style="margin-top:56px;font-size:38px;color:rgba(255,255,255,.9);font-weight:700;line-height:1.6">{e(sub_text)}</div>
</div>
<div style="flex:none;padding:0 64px 60px;text-align:center;font-size:26px;color:rgba(255,255,255,.6)">发音练手/示范/参考 · 不承诺效果 · 全程无微信号，口令仅在群内公开发放</div>
</div>'''

THEMES = {
    "aiguo": {  # 爱国红金
        "cover_bg": "linear-gradient(165deg,#8c1a1a 0%,#a3221f 55%,#c0392b 100%)",
        "card_bg": "linear-gradient(160deg,#fff6ec,#ffe9d2)",
        "cta_bg": "linear-gradient(165deg,#7a1414,#a3221f)",
        "accent": "#c0392b", "gold": "#f4c542", "ink": "#2a1e14",
    },
}

POEM = [
    ("I live in China, a country I love.", "我住在中国，我爱这片土地。"),
    ("Our flag is red, with five golden stars.", "我们的国旗是红色的，上面有五颗金星。"),
    ("Beijing is our capital, old and new.", "北京是我们的首都，古老又崭新。"),
    ("The Great Wall winds across the hills.", "长城蜿蜒在群山之上。"),
    ("The Yellow River flows through our land.", "黄河奔流过我们的土地。"),
    ("I have black hair and bright black eyes.", "我有黑色的头发，明亮的黑眼睛。"),
    ("I speak Chinese, and I say it with pride.", "我说中文，我骄傲地说出它。"),
    ("I am Chinese. This is my home.", "我是中国人，这里是我的家。"),
    ("I love you, China.", "我爱你，中国。"),
]

def build_woguozuguo(outdir):
    theme = THEMES["aiguo"]
    render(cover(theme, "My Motherland", "我的祖国", "I am Chinese 我是中国人", "爱国朗诵·第1集"),
           os.path.join(outdir, "01_封面.png"))
    chunks = [POEM[0:3], POEM[3:6], POEM[6:9]]
    n = len(chunks)
    for i, pairs in enumerate(chunks, start=1):
        render(lines_card(theme, i, n, pairs), os.path.join(outdir, f"{i+1:02d}_稿{i}.png"))
    render(cta_card(theme,
        "评论区扣【朗诵稿】，我发全文",
        "娃念完想知道发音对不对？进群外教帮你过一遍"),
        os.path.join(outdir, f"{n+2:02d}_CTA.png"))
    print(f"✅ 我的祖国 卡片系列生成完毕 → {outdir}")

TOPICS = {"woguozuguo": build_woguozuguo}

def main():
    key = sys.argv[1] if len(sys.argv) > 1 else "woguozuguo"
    if key not in TOPICS:
        print(f"未知topic: {key}，可选：{list(TOPICS)}"); return
    outdir = os.path.join(HERE, "我的祖国" if key == "woguozuguo" else key)
    TOPICS[key](outdir)

if __name__ == "__main__":
    main()
