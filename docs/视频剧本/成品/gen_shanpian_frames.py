#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""片单对标·启蒙动画 pilot 竖版帧生成 (1080x1920, 纯文字片名, 零IP形象)"""
import os, subprocess, tempfile, html as _H

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.dirname(os.path.abspath(__file__)) + "/frames"
os.makedirs(OUT, exist_ok=True)
FONT = '"PingFang SC","Microsoft YaHei",sans-serif'
W, H = 1080, 1920
def e(s): return _H.escape(str(s))

BG = "linear-gradient(165deg,#fff2f7 0%,#ffe4ec 55%,#ffd6e2 100%)"
BASE = f'''*{{margin:0;box-sizing:border-box;font-family:{FONT}}}
body{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{BG}}}
.brand{{position:absolute;top:60px;left:60px;background:#ff7a3d;color:#fff;font-size:34px;font-weight:800;padding:12px 30px;border-radius:30px}}
.safe{{position:absolute;bottom:44px;left:0;right:0;text-align:center;font-size:24px;color:#c99;font-weight:600}}'''

def cover():
    return f'''<style>{BASE}
.hook{{position:absolute;top:388px;left:60px;right:60px;text-align:center;font-size:112px;font-weight:900;color:#3a2330;line-height:1.24}}
.hl{{color:#e83e6e;font-size:150px;display:inline-block;margin:6px 0}}
.agetag{{position:absolute;top:836px;left:0;right:0;text-align:center;font-size:68px;font-weight:900;color:#ff7a3d}}
.sub{{position:absolute;top:964px;left:80px;right:80px;text-align:center;font-size:56px;font-weight:900;color:#fff;background:#e83e6e;border-radius:26px;padding:32px 24px;line-height:1.36;box-shadow:0 12px 30px rgba(232,62,110,.30)}}
.hand{{position:absolute;top:1226px;left:0;right:0;text-align:center;font-size:140px}}
.tip{{position:absolute;top:1436px;left:70px;right:70px;text-align:center;font-size:44px;font-weight:800;color:#b06}}
</style>
<div class=brand>YiYi英语</div>
<div class=hook>英语启蒙动画<br><span class=hl>别乱刷！</span><br>12部按难度排好</div>
<div class=agetag>2-10岁 · 分4档</div>
<div class=sub>刷错动画=白刷<br>越刷越听不懂</div>
<div class=hand>👇</div>
<div class=tip>存下来 · 照着给娃排</div>
<div class=safe>动画按公开信息中立分类 · 不打优劣分 · 仅供参考</div>'''

def tier(level, color, sub, items, idx):
    # items: list of (英文名, 中文名, 适龄, 一句话)
    dots = ""
    for d in range(1, 5):
        cls = "on" if d <= idx else "off"
        dots += f'<span class="dot {cls}"></span>'
    rows = ""
    for en, cn, age, note in items:
        rows += f'''<div class=item>
<div class=nm><span class=en>{e(en)}</span> <span class=cn>{e(cn)}</span></div>
<div class=meta><span class=age>{e(age)}</span><span class=note>{e(note)}</span></div></div>'''
    return f'''<style>{BASE}
.step{{position:absolute;top:150px;left:60px;background:{color};color:#fff;font-size:74px;font-weight:900;padding:22px 46px;border-radius:26px;box-shadow:0 10px 26px rgba(0,0,0,.14)}}
.dots{{position:absolute;top:196px;right:70px;display:flex;gap:22px}}
.dot{{width:34px;height:34px;border-radius:50%}}
.dot.on{{background:{color}}}
.dot.off{{background:{color};opacity:.22}}
.ssub{{position:absolute;top:310px;left:66px;right:66px;font-size:48px;font-weight:800;color:#96566e}}
.list{{position:absolute;top:440px;left:60px;right:60px}}
.item{{background:#fff;border-left:16px solid {color};border-radius:22px;padding:34px 40px;margin-bottom:34px;box-shadow:0 10px 26px rgba(200,120,150,.15)}}
.nm{{font-size:60px;font-weight:900;color:#2f1f2a;line-height:1.2}}
.en{{color:{color}}}.cn{{font-size:46px;color:#5a4550}}
.meta{{margin-top:18px;display:flex;align-items:center;gap:20px}}
.age{{flex:none;background:{color}22;color:{color};font-size:38px;font-weight:900;padding:8px 22px;border-radius:16px}}
.note{{font-size:40px;color:#7a5f6c;font-weight:700}}
</style>
<div class=brand>YiYi英语</div>
<div class=step>{e(level)}</div><div class=dots>{dots}</div>
<div class=ssub>{e(sub)}</div>
<div class=list>{rows}</div>
<div class=safe>片名均为真实存在的公开作品 · 中立分类不打优劣分</div>'''

def cta():
    return f'''<style>{BASE}
.big{{position:absolute;top:360px;left:70px;right:70px;text-align:center;font-size:96px;font-weight:900;color:#3a2330;line-height:1.3}}
.hl{{color:#e83e6e}}
.card{{position:absolute;top:820px;left:80px;right:80px;background:#fff;border-radius:30px;padding:56px 44px;box-shadow:0 16px 40px rgba(200,120,150,.2);text-align:center}}
.card .lbl{{font-size:46px;font-weight:800;color:#96566e}}
.card .link{{margin-top:24px;font-size:64px;font-weight:900;color:#ff7a3d;letter-spacing:1px}}
.free{{margin-top:20px;display:inline-block;background:#ffe0ea;color:#e83e6e;font-size:40px;font-weight:900;padding:12px 30px;border-radius:20px}}
.collect{{position:absolute;top:1430px;left:70px;right:70px;text-align:center;font-size:52px;font-weight:900;color:#b06}}
</style>
<div class=brand>YiYi英语</div>
<div class=big>不知道娃<br>适合<span class=hl>哪一级？</span></div>
<div class=card>
<div class=lbl>主页免费测 · 一测就知道该从哪部看</div>
<div class=link>mylumee.cn/yiyi-ceping</div>
<div class=free>0元 · 免费测评</div>
</div>
<div class=collect>⭐ 存下来 · 关注不迷路</div>
<div class=safe>测评仅供启蒙参考 · 不承诺学习效果</div>'''

FRAMES = [
    ("01_cover.png", cover()),
    ("02_L1.png", tier("入门·磨耳朵", "#ff8fab", "0基础先磨耳朵 · 重复多语速慢",
        [("Super Simple Songs","超级简单儿歌","2-4岁","短句重复 · 边唱边指物"),
         ("Cocomelon","可可melon儿歌","2-4岁","日常场景儿歌 · 画面直白"),
         ("Maisy","小鼠波波","3-5岁","慢节奏日常 · 词汇少")], 1)),
    ("03_L2.png", tier("初级·日常", "#ff6f91", "有点听力基础 · 生活场景",
        [("Peppa Pig","小猪佩奇","3-6岁","家庭日常 · 语速慢句子短"),
         ("Bluey","布鲁伊","4-7岁","亲子生活 · 地道口语"),
         ("Little Bear","小熊布迷","4-6岁","温和叙事 · 情节简单")], 2)),
    ("04_L3.png", tier("进阶·情节", "#e8567a", "能听懂简单对话 · 情节变长",
        [("Paw Patrol","汪汪队立大功","5-8岁","任务情节 · 对白变多"),
         ("Dora the Explorer","爱探险的朵拉","4-7岁","互动问答 · 边看边说"),
         ("Octonauts","海底小纵队","5-8岁","科普情节 · 词汇拓展")], 3)),
    ("05_L4.png", tier("挑战·近原速", "#c9366a", "有积累冲刺 · 语速接近原声",
        [("Magic School Bus","神奇校车","6-10岁","科普长句 · 语速接近原速"),
         ("Wild Kratts","动物兄弟","6-10岁","科学词汇多 · 信息量大"),
         ("Ben & Holly","本和霍利","5-8岁","情节丰富 · 语速偏快")], 4)),
    ("06_cta.png", cta()),
]

def render(html, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8>" + html); tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", f"--window-size={W},{H}",
        f"--screenshot={out}", f"file://{tmp}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)

if __name__ == "__main__":
    for name, html in FRAMES:
        render(html, os.path.join(OUT, name))
        print("✅", name)
    print("→", OUT)
