#!/usr/bin/env python3
"""4种颜色主题封面样本"""
import os, html, subprocess, time, re

CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 6种主题色（每个系列用不同的）
THEMES = {
    "navy":   {"bg":"#001a4a", "bg2":"#002F7F", "accent":"#5db0ff", "tag":"#002FA7"},   # 干货/AI
    "crimson":{"bg":"#5c0a0a", "bg2":"#8B1a1a", "accent":"#ffb3b3", "tag":"#C0392B"},  # 朗诵/爱国
    "forest": {"bg":"#0a2e1a", "bg2":"#1a5233", "accent":"#7fdfb0", "tag":"#1a8a50"},  # 片单/资源
    "purple": {"bg":"#1a0a3a", "bg2":"#2D1B6E", "accent":"#c4a0ff", "tag":"#5c35c0"},  # 考试/戏剧
    "amber":  {"bg":"#2e1a00", "bg2":"#5c3800", "accent":"#ffd080", "tag":"#c07800"},  # 文化/讲中国
    "teal":   {"bg":"#002a2e", "bg2":"#004a52", "accent":"#80dfe0", "tag":"#007b85"},  # 课本同步
}

def make_css(t):
    return f"""*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1440px}}
.cover{{
  width:1080px;height:1440px;
  background:linear-gradient(135deg, {t['bg']} 0%, {t['bg2']} 60%, {t['bg']} 100%);
  display:flex;flex-direction:column;
  position:relative;overflow:hidden;
  font-family:"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;
}}
/* 装饰圆 */
.deco-circle{{
  position:absolute;top:-180px;right:-180px;
  width:600px;height:600px;
  border-radius:50%;
  background:rgba(255,255,255,0.04);
  pointer-events:none;
}}
.deco-circle2{{
  position:absolute;bottom:-100px;left:-150px;
  width:500px;height:500px;
  border-radius:50%;
  background:rgba(255,255,255,0.03);
  pointer-events:none;
}}
/* 图片区 */
.img-well{{
  height:460px;overflow:hidden;position:relative;flex-shrink:0;
}}
.img-well img{{width:100%;height:100%;object-fit:cover;opacity:0.5;}}
.img-well .img-overlay{{
  position:absolute;inset:0;
  background:linear-gradient(to bottom, transparent 30%, {t['bg']} 100%);
}}
.img-well .no-img{{
  width:100%;height:100%;
  background:repeating-linear-gradient(
    -45deg,
    rgba(255,255,255,0.02) 0px,rgba(255,255,255,0.02) 1px,
    transparent 1px,transparent 20px
  );
}}
.top-bar{{
  position:absolute;top:0;left:0;right:0;
  padding:44px 60px;
  display:flex;align-items:center;justify-content:space-between;
  z-index:10;
}}
.series-num{{font-size:12px;letter-spacing:3px;color:rgba(255,255,255,0.4);font-weight:600;}}
.tag-pill{{
  background:{t['tag']};color:#fff;padding:7px 18px;border-radius:20px;
  font-size:12px;letter-spacing:2px;font-weight:700;
}}
.text-block{{
  flex:1;display:flex;flex-direction:column;justify-content:flex-end;
  padding:0 60px 20px;position:relative;z-index:5;
}}
.kicker{{font-size:14px;letter-spacing:4px;color:{t['accent']};font-weight:600;margin-bottom:18px;}}
h1{{
  font-size:88px;font-weight:800;line-height:1.08;color:#fff;
  letter-spacing:-2px;margin-bottom:22px;
}}
h1 b{{color:{t['accent']};}}
.sub{{font-size:26px;color:rgba(255,255,255,0.65);line-height:1.5;font-weight:300;max-width:840px;}}
.bottom-rule{{
  border-top:1px solid rgba(255,255,255,0.12);
  padding:26px 60px;
  display:flex;align-items:center;justify-content:space-between;
  position:relative;z-index:5;
}}
.brand-tiny{{font-size:11px;color:rgba(255,255,255,0.25);letter-spacing:2px;}}
.swipe-hint{{font-size:14px;color:rgba(255,255,255,0.35);}}
.bignum{{
  position:absolute;right:-15px;bottom:60px;
  font-size:500px;font-weight:900;
  color:rgba(255,255,255,0.04);line-height:1;z-index:0;
  pointer-events:none;
}}
"""

def hi(t):
    escaped = html.escape(str(t))
    return re.sub(r'([A-Za-z][A-Za-z0-9\-\'\.]+)', r'<span style="font-weight:700">\1</span>', escaped)

def render(slug, content_html, css, out_path):
    D = "/tmp/gz_themes/"
    os.makedirs(D, exist_ok=True)
    fn = slug + ".html"
    with open(D + fn, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{content_html}</body></html>")
    p = subprocess.Popen([CH,
        "--headless=new","--disable-gpu","--no-sandbox",
        f"--user-data-dir=/tmp/cs_th_{slug}","--force-device-scale-factor=2",
        "--window-size=1080,1440","--hide-scrollbars","--virtual-time-budget=4000",
        f"--screenshot={out_path}", f"file://{D}{fn}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(0.5)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            time.sleep(0.3); break
    try: p.terminate(); p.wait(timeout=3)
    except: p.kill()

SAMPLES = [
    ("navy",    "01",  "AI vs 真人外教",    "哪个贵不代表哪个好",        "AI vs 真外教 · 干货"),
    ("crimson", "02",  "爱国英语朗诵",       "会背了，再会说，才叫学会",   "英语朗诵 · 演讲"),
    ("forest",  "03",  "分级动画片单",       "从 Peppa 到 Harry Potter 怎么升级", "分级片单 · 3.9万赞同款"),
    ("purple",  "04",  "KET / PET 真实数据", "报名通过率、认可学校一次看清", "KET·PET · 考试系列"),
]

out_dir = os.path.expanduser("~/projects/yiyi-english/docs/视频剧本/主题色样本/")
os.makedirs(out_dir, exist_ok=True)

for theme_key, num, title, sub, kicker in SAMPLES:
    t = THEMES[theme_key]
    css = make_css(t)
    body = f"""
<div class="cover">
  <div class="deco-circle"></div>
  <div class="deco-circle2"></div>
  <div class="img-well">
    <div class="no-img"></div>
    <div class="img-overlay"></div>
  </div>
  <div class="top-bar">
    <span class="series-num">SERIES · {num}</span>
    <span class="tag-pill">干货</span>
  </div>
  <div class="text-block">
    <div class="kicker">{html.escape(kicker)}</div>
    <h1>{hi(title)}</h1>
    <div class="sub">{html.escape(sub)}</div>
  </div>
  <div class="bottom-rule">
    <span class="brand-tiny">YIYI 英语</span>
    <span class="swipe-hint">滑动查看 →</span>
  </div>
  <div class="bignum">{num}</div>
</div>"""
    out = os.path.join(out_dir, f"{num}_{theme_key}_封面.png")
    print(f"渲染 {theme_key}...", end=" ", flush=True)
    render(f"th_{theme_key}", body, css, out)
    print("✅")

print("打开文件夹...")
subprocess.run(["open", out_dir])
