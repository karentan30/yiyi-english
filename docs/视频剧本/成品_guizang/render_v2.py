#!/usr/bin/env python3
"""guizang v2 — 有颜色+有图版本"""
import os, sys, json, html, subprocess, time, textwrap, re

CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#0a0a0a;--blue:#002FA7;--navy:#001a4a;--paper:#fafaf8;--mid:#f0f0ee}
html,body{width:1080px;height:1440px}

/* ===== COVER ===== */
.cover{
  width:1080px;height:1440px;
  background:var(--navy);
  display:flex;flex-direction:column;
  position:relative;overflow:hidden;
  font-family:"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;
}
.cover .bg-img{
  position:absolute;top:0;left:0;width:100%;height:55%;
  object-fit:cover;opacity:0.45;
}
.cover .bg-grad{
  position:absolute;top:0;left:0;width:100%;height:55%;
  background:linear-gradient(to bottom, rgba(0,26,74,0.3) 0%, rgba(0,26,74,0.95) 100%);
}
.cover .top-bar{
  position:relative;z-index:5;
  padding:52px 64px 0;
  display:flex;align-items:center;justify-content:space-between;
}
.cover .series-num{
  font-size:13px;letter-spacing:3px;color:rgba(255,255,255,0.55);font-weight:600;text-transform:uppercase;
}
.cover .tag-pill{
  background:#002FA7;color:#fff;padding:7px 18px;border-radius:20px;
  font-size:12px;letter-spacing:2px;font-weight:700;text-transform:uppercase;
}
.cover .center-block{
  position:relative;z-index:5;
  flex:1;display:flex;flex-direction:column;justify-content:flex-end;
  padding:0 64px 60px;
}
.cover .kicker{
  font-size:15px;letter-spacing:4px;color:#5db0ff;font-weight:600;
  text-transform:uppercase;margin-bottom:20px;
}
.cover h1{
  font-size:96px;font-weight:800;line-height:1.05;color:#fff;
  letter-spacing:-2px;margin-bottom:24px;
}
.cover h1 b{color:#5db0ff;}
.cover .sub{
  font-size:28px;color:rgba(255,255,255,0.7);line-height:1.5;font-weight:300;
  max-width:820px;
}
.cover .bottom-rule{
  position:relative;z-index:5;
  border-top:1px solid rgba(255,255,255,0.15);
  padding:28px 64px;
  display:flex;align-items:center;justify-content:space-between;
}
.cover .brand-tiny{font-size:12px;color:rgba(255,255,255,0.3);letter-spacing:2px;}
.cover .swipe-hint{font-size:14px;color:rgba(255,255,255,0.4);}
/* deco number */
.cover .bignum{
  position:absolute;right:-20px;bottom:80px;
  font-size:520px;font-weight:900;
  color:rgba(255,255,255,0.04);line-height:1;z-index:2;
  pointer-events:none;user-select:none;
}

/* ===== INNER PAGE ===== */
.inner{
  width:1080px;height:1440px;
  background:var(--paper);
  display:flex;flex-direction:column;
  font-family:"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;
  position:relative;overflow:hidden;
}
.inner .head-band{
  background:var(--blue);
  padding:52px 64px 44px;
  position:relative;overflow:hidden;
}
.inner .head-band::after{
  content:'';position:absolute;bottom:-1px;left:0;right:0;height:2px;
  background:rgba(0,0,0,0.15);
}
.inner .pg-num{
  font-size:12px;letter-spacing:3px;color:rgba(255,255,255,0.45);
  font-weight:600;text-transform:uppercase;margin-bottom:20px;
}
.inner .pt-label{
  font-size:13px;letter-spacing:3px;color:rgba(255,255,255,0.6);
  font-weight:700;text-transform:uppercase;margin-bottom:14px;
}
.inner h2{
  font-size:68px;font-weight:800;line-height:1.1;color:#fff;
  letter-spacing:-1px;
}
.inner h2 b{color:#a8c8ff;}
.inner .content-area{
  flex:1;padding:52px 64px;display:flex;flex-direction:column;justify-content:center;
}
.inner .body-text{
  font-size:40px;line-height:1.75;color:#1a1a1a;font-weight:400;
}
.inner .body-text .en{color:var(--blue);font-weight:700;}
.inner .example-box{
  margin-top:36px;background:var(--mid);border-left:5px solid var(--blue);
  padding:28px 32px;border-radius:0 12px 12px 0;
}
.inner .example-box .label{
  font-size:11px;letter-spacing:3px;color:#999;font-weight:700;
  text-transform:uppercase;margin-bottom:10px;
}
.inner .example-box .text{
  font-size:36px;font-weight:500;color:#1a1a1a;line-height:1.5;
}
.inner .example-box .text .en{color:var(--blue);font-weight:700;}
.inner .bignum{
  position:absolute;right:40px;bottom:10px;
  font-size:340px;font-weight:900;
  color:rgba(0,47,167,0.05);line-height:1;z-index:0;
  pointer-events:none;user-select:none;
}

/* ===== CTA ===== */
.cta{
  width:1080px;height:1440px;
  background:var(--navy);
  display:flex;flex-direction:column;justify-content:center;align-items:center;
  font-family:"Helvetica Neue","PingFang SC","Noto Sans SC",sans-serif;
  position:relative;overflow:hidden;
}
.cta .bignum{
  position:absolute;right:-30px;bottom:40px;
  font-size:600px;font-weight:900;
  color:rgba(255,255,255,0.03);line-height:1;
}
.cta .center{position:relative;z-index:5;text-align:center;padding:0 80px;}
.cta h2{font-size:72px;font-weight:800;color:#fff;line-height:1.2;margin-bottom:32px;}
.cta h2 b{color:#5db0ff;}
.cta .divider{width:60px;height:3px;background:#002FA7;margin:0 auto 40px;}
.cta .body{font-size:34px;color:rgba(255,255,255,0.7);line-height:1.6;font-weight:300;}
.cta .cta-pill{
  margin-top:60px;
  background:#002FA7;color:#fff;
  padding:22px 48px;border-radius:40px;
  font-size:26px;font-weight:700;letter-spacing:1px;
  display:inline-block;
}
.cta .brand-tiny{
  position:absolute;bottom:32px;width:100%;text-align:center;
  font-size:12px;color:rgba(255,255,255,0.2);letter-spacing:2px;
}
"""

def hi(t):
    """highlight English words in blue"""
    escaped = html.escape(str(t))
    return re.sub(r'([A-Za-z][A-Za-z0-9\-\'\.]+)', r'<span class="en">\1</span>', escaped)

def render(slug, content_html, out_path, css=CSS):
    D = "/tmp/gz_render/"
    os.makedirs(D, exist_ok=True)
    fn = slug + ".html"
    with open(D + fn, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{content_html}</body></html>")

    p = subprocess.Popen([CH,
        "--headless=new","--disable-gpu","--no-sandbox",
        f"--user-data-dir=/tmp/cs_v2_{slug}","--force-device-scale-factor=2",
        "--window-size=1080,1440","--hide-scrollbars","--virtual-time-budget=4000",
        f"--screenshot={out_path}", f"file://{D}{fn}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(0.5)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            time.sleep(0.3)
            break
    try:
        p.terminate(); p.wait(timeout=3)
    except:
        p.kill()

def make_cover(out_dir, cover_title, sub, kicker="AI vs 真外教", img_path=None, num="01"):
    """Dark navy cover with optional background image"""
    img_tag = f"<img class='bg-img' src='file://{img_path}'>" if img_path and os.path.exists(img_path) else ""
    grad_tag = "<div class='bg-grad'></div>" if img_path else ""
    # If no image, add a subtle geometric pattern via CSS gradient
    no_img_style = "" if img_path else "background:linear-gradient(135deg, #001a4a 0%, #002F7F 40%, #001a4a 100%);"

    h = hi(cover_title)
    html_content = f"""
<div class="cover" style="{no_img_style}">
  {img_tag}
  {grad_tag}
  <div class="top-bar">
    <span class="series-num">SERIES · {num}</span>
    <span class="tag-pill">干货</span>
  </div>
  <div class="center-block">
    <div class="kicker">{html.escape(kicker)}</div>
    <h1>{h}</h1>
    <div class="sub">{hi(sub)}</div>
  </div>
  <div class="bottom-rule">
    <span class="brand-tiny">YIYI 英语</span>
    <span class="swipe-hint">滑动查看 →</span>
  </div>
  <div class="bignum">1</div>
</div>"""
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "01_封面.png")
    render("cover_" + os.path.basename(out_dir), html_content, out)
    return out

def make_inner(out_dir, pg_num, total, pt_label, h2_text, body_text, example=None, idx=1):
    """Blue-band top + white content inner page"""
    h2h = hi(h2_text)
    bodyh = hi(body_text)
    ex_html = ""
    if example:
        ex_html = f"""<div class="example-box">
          <div class="label">例子</div>
          <div class="text">{hi(example)}</div>
        </div>"""
    html_content = f"""
<div class="inner">
  <div class="head-band">
    <div class="pg-num">{pg_num:02d} / {total:02d}</div>
    <div class="pt-label">POINT {idx:02d}</div>
    <h2>{h2h}</h2>
  </div>
  <div class="content-area">
    <div class="body-text">{bodyh}</div>
    {ex_html}
  </div>
  <div class="bignum">{idx:02d}</div>
</div>"""
    out = os.path.join(out_dir, f"{pg_num:02d}.png")
    render(f"inner_{os.path.basename(out_dir)}_{pg_num}", html_content, out)
    return out

def make_cta(out_dir, pg_num, h2_text, body_text, cta_text="评论区聊聊你怎么看"):
    h2h = hi(h2_text)
    html_content = f"""
<div class="cta">
  <div class="center">
    <h2>{h2h}</h2>
    <div class="divider"></div>
    <div class="body">{hi(body_text)}</div>
    <div class="cta-pill">👇 {html.escape(cta_text)}</div>
  </div>
  <div class="brand-tiny">YIYI 英语 · 真外教 · 真人练习</div>
  <div class="bignum">6</div>
</div>"""
    out = os.path.join(out_dir, f"{pg_num:02d}_CTA.png")
    render(f"cta_{os.path.basename(out_dir)}_{pg_num}", html_content, out)
    return out

# ===== TEST: render just the cover =====
if __name__ == "__main__":
    out_dir = os.path.expanduser(
        "~/projects/yiyi-english/docs/视频剧本/成品_guizang/guandian_4_v2/"
    )
    os.makedirs(out_dir, exist_ok=True)

    print("渲染封面...")
    out = make_cover(
        out_dir=out_dir,
        cover_title="AI越强，真人越贵",
        sub="ChatGPT、豆包、多邻国都能陪娃练了——还花钱上课干嘛？",
        kicker="AI vs 真外教 · 干货篇",
        img_path=None,  # no image yet, using CSS gradient
        num="01"
    )
    print(f"✅ 封面 → {out}")
    subprocess.run(["open", out])
