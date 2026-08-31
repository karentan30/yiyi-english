#!/usr/bin/env python3
"""
guizang v3 — 小红书米白系
- 奶油白背景 + 每张独立口音色
- 配真图（传图路径进来）
- 每张都不一样
"""
import os, html, subprocess, time, re

CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 每个系列的口音色（不同的，轻柔的）
# (accent_dark, accent_light_bg, accent_text)
PALETTES = {
    "AI干货":    ("#2952CC", "#EEF3FF", "#2952CC"),  # 蓝
    "朗诵演讲":  ("#B03030", "#FFF0F0", "#B03030"),  # 暖红
    "片单":      ("#1E6B4A", "#EEF8F3", "#1E6B4A"),  # 绿
    "考试":      ("#5B3FA0", "#F2EEFF", "#5B3FA0"),  # 紫
    "文化":      ("#A06020", "#FFF8EE", "#A06020"),  # 琥珀
    "每日":      ("#C05080", "#FFF0F5", "#C05080"),  # 玫
    "夏令营":    ("#2A7A8A", "#EDFAFC", "#2A7A8A"),  # 青
    "戏剧":      ("#7A3060", "#FBF0FF", "#7A3060"),  # 紫红
}

CSS_TMPL = """
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px;background:#FAF8F3}}
.card{{
  width:1080px;height:1440px;
  background:#FAF8F3;
  display:flex;flex-direction:column;
  font-family:"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;
  position:relative;overflow:hidden;
}}

/* 顶部图片区 */
.img-zone{{
  height:{img_h}px;flex-shrink:0;position:relative;overflow:hidden;
}}
.img-zone img{{
  width:100%;height:100%;object-fit:cover;
  filter:brightness(0.92);
}}
.img-zone .no-img{{
  width:100%;height:100%;
  background:linear-gradient(135deg, {accent_light} 0%, #FAF8F3 100%);
  display:flex;align-items:center;justify-content:center;
}}
.img-zone .icon-placeholder{{
  font-size:200px;opacity:0.18;
}}

/* 顶部标签栏 */
.top-bar{{
  position:absolute;top:0;left:0;right:0;
  padding:40px 56px;
  display:flex;align-items:center;justify-content:space-between;
  z-index:10;
}}
.tag-pill{{
  background:{accent_dark};color:#fff;
  padding:8px 20px;border-radius:20px;
  font-size:13px;letter-spacing:2px;font-weight:700;
}}
.pg-num{{
  font-size:12px;letter-spacing:2px;color:rgba(0,0,0,0.3);font-weight:500;
}}

/* 文字区 */
.text-zone{{
  flex:1;padding:44px 56px 0;display:flex;flex-direction:column;
}}
.kicker{{
  font-size:14px;letter-spacing:4px;color:{accent_dark};
  font-weight:700;text-transform:uppercase;margin-bottom:16px;
  display:flex;align-items:center;gap:10px;
}}
.kicker::before{{content:'';display:block;width:28px;height:2px;background:{accent_dark};}}
h1{{
  font-size:{h1_size}px;font-weight:800;line-height:1.1;
  color:#0a0a0a;letter-spacing:-1px;margin-bottom:20px;
}}
h1 b{{color:{accent_dark};}}
.sub{{
  font-size:30px;color:#555;line-height:1.6;font-weight:400;
  max-width:860px;margin-bottom:32px;
}}
.sub .en{{color:{accent_dark};font-weight:600;}}

/* 内容标签 */
.accent-box{{
  background:{accent_light};border-radius:12px;
  padding:24px 32px;margin-top:auto;margin-bottom:36px;
  border-left:4px solid {accent_dark};
}}
.accent-box p{{font-size:28px;color:#1a1a1a;line-height:1.6;}}
.accent-box p .en{{color:{accent_dark};font-weight:700;}}

/* 底部 */
.bottom-strip{{
  padding:24px 56px;
  display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid rgba(0,0,0,0.06);
}}
.brand{{font-size:11px;color:rgba(0,0,0,0.2);letter-spacing:3px;font-weight:500;}}
.hint{{font-size:14px;color:rgba(0,0,0,0.25);}}

/* 大数字装饰 */
.bignum{{
  position:absolute;right:-10px;bottom:50px;
  font-size:380px;font-weight:900;
  color:rgba(0,0,0,0.03);line-height:1;
  pointer-events:none;z-index:0;
}}
"""

def make_css(palette_key, img_h=480, h1_size=82):
    ad, al, at = PALETTES[palette_key]
    return CSS_TMPL.format(
        accent_dark=ad, accent_light=al, accent_text=at,
        img_h=img_h, h1_size=h1_size
    )

def hi(t, accent_dark):
    escaped = html.escape(str(t))
    return re.sub(r'([A-Za-z][A-Za-z0-9\-\'\.\/]+)',
                  f'<span class="en" style="color:{accent_dark};font-weight:700">\\1</span>',
                  escaped)

def render(slug, content_html, css, out_path):
    D = "/tmp/gz_v3/"
    os.makedirs(D, exist_ok=True)
    fn = slug + ".html"
    with open(D + fn, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{content_html}</body></html>")
    p = subprocess.Popen([CH,
        "--headless=new","--disable-gpu","--no-sandbox",
        f"--user-data-dir=/tmp/cs_v3_{slug}","--force-device-scale-factor=2",
        "--window-size=1080,1440","--hide-scrollbars","--virtual-time-budget=4000",
        f"--screenshot={out_path}", f"file://{D}{fn}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(0.5)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            time.sleep(0.3); break
    try: p.terminate(); p.wait(timeout=3)
    except: p.kill()

def make_cover(out_dir, slug, palette_key, kicker, title, sub, tag_label,
               img_path=None, accent_box_text=None, pg_num="01", bignum="1"):
    ad, al, at = PALETTES[palette_key]
    css = make_css(palette_key, img_h=460 if img_path else 300)

    if img_path and os.path.exists(img_path):
        img_tag = f"<img src='file://{img_path}'>"
    else:
        img_tag = f"<div class='no-img'><div class='icon-placeholder'>📚</div></div>"

    accent_html = ""
    if accent_box_text:
        accent_html = f"""<div class='accent-box'><p>{hi(accent_box_text, ad)}</p></div>"""

    body = f"""
<div class="card">
  <div class="img-zone">
    {img_tag}
    <div class="top-bar">
      <span class="tag-pill">{html.escape(tag_label)}</span>
      <span class="pg-num">{pg_num}</span>
    </div>
  </div>
  <div class="text-zone">
    <div class="kicker">{html.escape(kicker)}</div>
    <h1>{hi(title, ad)}</h1>
    <div class="sub">{hi(sub, ad)}</div>
    {accent_html}
  </div>
  <div class="bottom-strip">
    <span class="brand">YIYI 英语</span>
    <span class="hint">滑动查看 →</span>
  </div>
  <div class="bignum">{bignum}</div>
</div>"""

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"01_封面.png")
    render(slug, body, css, out)
    return out


# ===== 出4个不同颜色样本 =====
if __name__ == "__main__":
    base = os.path.expanduser("~/projects/yiyi-english/docs/视频剧本/主题色样本v3/")
    os.makedirs(base, exist_ok=True)

    samples = [
        # (文件夹, slug, 主题, kicker, 标题, 副标, 标签, img_path, accent_box)
        ("A_AI干货",   "sA", "AI干货",
         "AI vs 真外教",
         "AI越强，\n真人越贵",
         "ChatGPT、豆包、多邻国都能练了——外教还有啥用？",
         "干货",
         None,
         "AI = 工具；真外教 = 纠音+语感+真实对话场景。缺一不可。"),

        ("B_朗诵演讲",  "sB", "朗诵演讲",
         "英语朗诵 · 演讲",
         "会背了\n才会说",
         "给孩子攒一首演讲稿，比刷100道题管用",
         "朗诵",
         None,
         "从 My Dream 到 My Motherland——3分钟上台，模板在这"),

        ("C_片单",     "sC", "片单",
         "分级动画片单",
         "Peppa 之后\n看什么？",
         "帮你排好了：从 aa 级到章节书，照这个顺序看",
         "片单",
         None,
         "Peppa → Bluey → Octonauts → Magic School Bus → Horrible Histories"),

        ("D_考试",     "sD", "考试",
         "KET · PET 真实数据",
         "KET 报名\n避坑指南",
         "报名通过率、认可学校、费用——一次看清",
         "考试",
         None,
         "KET 通过 = A2 级 · PET 通过 = B1 级 · 认可院校 800+"),
    ]

    outputs = []
    for folder, slug, palette, kicker, title, sub, tag, img, box in samples:
        out_d = os.path.join(base, folder)
        print(f"渲染 {folder}...", end=" ", flush=True)
        out = make_cover(out_d, slug, palette, kicker, title, sub, tag,
                         img_path=img, accent_box_text=box)
        outputs.append(out)
        print("✅")

    subprocess.run(["open", base])
    print("完成 → 打开文件夹")
