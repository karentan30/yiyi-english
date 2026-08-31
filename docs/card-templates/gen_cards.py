#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡片生成引擎 · 喂数据→批量出图（中文完美·免费·边际token≈0）
用法：python3 gen_cards.py cards.json
cards.json 是一个数组，每项：{"type":"金句","out":"号A_01.png","h":1440,"data":{...}}
支持模板：金句 / 数字 / 清单 / 对比 / 路线 / 排行 / 痛点问句
换数据就出新卡，不用改脚本。
"""
import json, os, subprocess, sys, tempfile, html as _H

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "生成")
os.makedirs(OUTDIR, exist_ok=True)
FONT = '"PingFang SC","Microsoft YaHei",sans-serif'
def e(s): return _H.escape(str(s))

# 每个模板返回完整 HTML；配色可在 data.color 里覆盖，默认给一套好看的
def t_金句(d):  # data: tag, lines[], hl, sub, foot, color{bg,tagbg,accent,sub,foot,glow}
    c=d.get("color",{})
    bg=c.get("bg","linear-gradient(155deg,#1f2d3d,#2b3f57 60%,#39536f)")
    tagbg=c.get("tagbg","#e8552d"); acc=c.get("accent","#ffd05e")
    subc=c.get("sub","#c7d6e6"); footc=c.get("foot","#9fb3c8")
    glow=c.get("glow","rgba(255,190,120,.22)")
    lines = "<br>".join(f'<span class=y>{e(x)}</span>' if x==d.get("hl") else e(x) for x in d["lines"])
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;height:1440px;position:relative;overflow:hidden;background:{bg};color:#fff}}
.tex{{position:absolute;inset:0;background:radial-gradient(circle at 80% 20%,{glow},transparent 42%)}}
.tag{{position:absolute;top:88px;left:70px;background:{tagbg};padding:12px 30px;border-radius:30px;font-size:28px;font-weight:800}}
.q{{position:absolute;top:150px;left:52px;font-size:170px;color:rgba(255,255,255,.07);font-weight:900}}
.t{{position:absolute;top:360px;left:66px;right:66px;font-size:104px;font-weight:900;line-height:1.24}}
.y{{color:{acc}}}.s{{position:absolute;top:940px;left:66px;right:66px;font-size:50px;color:{subc};font-weight:700;line-height:1.5}}
.f{{position:absolute;bottom:90px;left:70px;font-size:32px;color:{footc}}}</style>
<div class=tex></div><div class=q>"</div><div class=tag>{e(d.get("tag",""))}</div>
<div class=t>{lines}</div><div class=s>{e(d.get("sub",""))}</div><div class=f>{e(d.get("foot",""))}</div>'''

def t_数字(d):  # data: tag, num, unit, desc, preview(emoji串), cta
    pv=f'<div class=pv>{e(d.get("preview",""))}</div>' if d.get("preview") else ''
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;height:1440px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 32%,#fff5e6 0%,#fde0bd 100%);text-align:center}}
.tag{{position:absolute;top:100px;left:50%;transform:translateX(-50%);background:#2a1e14;color:#ffd98a;font-size:30px;font-weight:800;padding:12px 34px;border-radius:30px}}
.wrap{{position:absolute;top:290px;left:0;right:0}}
.num{{display:inline-block;font-size:280px;font-weight:900;color:#e8552d;line-height:1;letter-spacing:-8px;text-shadow:0 8px 22px rgba(232,85,42,.22);position:relative}}
.num:after{{content:"";position:absolute;left:-20px;right:-20px;bottom:34px;height:32px;background:rgba(255,208,63,.45);z-index:-1;border-radius:6px}}
.unit{{font-size:56px;font-weight:800;color:#b56a2a;margin-left:6px}}
.desc{{margin:44px 60px 0;font-size:54px;font-weight:800;color:#2a1e14;line-height:1.4;background:rgba(255,255,255,.55);border-radius:22px;padding:26px 24px}}
.pv{{margin-top:34px;font-size:66px;letter-spacing:10px}}
.cta{{position:absolute;bottom:0;left:0;right:0;height:118px;background:linear-gradient(90deg,#2a1e14,#3a2a1a);color:#ffd98a;display:flex;align-items:center;justify-content:center;font-size:42px;font-weight:900}}</style>
<div class=tag>{e(d.get("tag",""))}</div><div class=wrap><span class=num>{e(d["num"])}</span><span class=unit>{e(d.get("unit",""))}</span>
<div class=desc>{e(d.get("desc",""))}</div>{pv}</div><div class=cta>{e(d.get("cta",""))}</div>'''

def t_痛点(d):  # 痛点问句大字 data: tag, lines[], hl, sub, foot, color{bg,ink,accent,tagbg,tagink,sub}
    c=d.get("color",{})
    bg=c.get("bg","linear-gradient(160deg,#fff0e6,#ffd9bf)"); ink=c.get("ink","#3a2318")
    acc=c.get("accent","#e8552d"); accline=c.get("accline","#ffb03a")
    tagbg=c.get("tagbg","#2a2320"); tagink=c.get("tagink","#ffd98a")
    subc=c.get("sub","#8a6a55"); footc=c.get("foot","#b09a8a")
    lines="<br>".join(f'<span class=h>{e(x)}</span>' if x==d.get("hl") else e(x) for x in d["lines"])
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;height:1440px;position:relative;overflow:hidden;background:{bg};color:{ink}}}
.tag{{position:absolute;top:90px;left:70px;background:{tagbg};color:{tagink};padding:12px 30px;border-radius:30px;font-size:28px;font-weight:800}}
.t{{position:absolute;top:360px;left:70px;right:70px;font-size:100px;font-weight:900;line-height:1.3}}.h{{color:{acc};text-decoration:underline;text-decoration-color:{accline};text-decoration-thickness:10px}}
.s{{position:absolute;top:960px;left:70px;right:70px;font-size:48px;color:{subc};font-weight:700;line-height:1.5}}
.f{{position:absolute;bottom:80px;left:70px;font-size:32px;color:{footc};font-weight:700}}</style>
<div class=tag>{e(d.get("tag",""))}</div><div class=t>{lines}</div><div class=s>{e(d.get("sub",""))}</div><div class=f>{e(d.get("foot",""))}</div>'''

def t_清单(d):  # data: title, hl, sub, items[{n,name,note,color}], cta
    cols=["#ff8c42","#5aa9e6","#7bc47f","#ef8ca0","#f0a952","#9b7fd0","#4bb3b0"]
    rows="".join(f'<div class=it style="border-left:8px solid {i.get("color",cols[k%len(cols)])}"><div class=n style="background:linear-gradient(135deg,{i.get("color",cols[k%len(cols)])},{i.get("color",cols[k%len(cols)])}cc)">{e(i.get("n",""))}</div><div class=s><b>{e(i["name"])}</b><small>{e(i.get("note",""))}</small></div></div>' for k,i in enumerate(d["items"]))
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;min-height:1440px;position:relative;background:linear-gradient(160deg,#fff6ec,#ffe9d2);padding:56px 48px 130px}}
.t{{font-size:78px;font-weight:900;color:#2a1e14;text-align:center;line-height:1.2}}.hl{{color:#e8552d;background:linear-gradient(transparent 58%,#ffd23f 58%);padding:0 8px}}.sub{{text-align:center;font-size:30px;color:#a8815e;margin:14px 0 36px;font-weight:700}}
.it{{display:flex;align-items:center;background:#fff;border-radius:22px;padding:24px 28px;margin-bottom:18px;box-shadow:0 10px 26px rgba(180,120,60,.13)}}
.n{{flex:none;width:78px;height:78px;color:#fff;border-radius:50%;font-size:30px;font-weight:900;display:flex;align-items:center;justify-content:center;margin-right:24px;box-shadow:0 6px 14px rgba(0,0,0,.14)}}
.s{{font-size:38px;font-weight:800;color:#3a2a1a}}.s small{{display:block;font-size:25px;color:#9a8776;font-weight:500;margin-top:5px}}
.cta{{position:fixed;bottom:0;left:0;right:0;height:110px;background:linear-gradient(90deg,#2b2b2b,#3a332e);color:#ffd98a;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:900}}</style>
<div class=t>{e(d["title"]).replace(e(d.get("hl","\x00")),f'<span class=hl>{e(d.get("hl",""))}</span>') if d.get("hl") else e(d["title"])}</div>
<div class=sub>{e(d.get("sub",""))}</div>{rows}<div class=cta>{e(d.get("cta",""))}</div>'''

def t_对比(d):  # data: title, sub, a{name,rows[]}, b{name,rows[]}, verdict, cta
    def col(x,c): return f'<div class=col><div class="h" style="background:{c}">{e(x["name"])}</div>'+"".join(f'<div class=row><b>{e(r.split("：")[0])}</b>{"："+e("：".join(r.split("：")[1:])) if "：" in r else ""}</div>' for r in x["rows"])+'</div>'
    vd=f'<div class=verdict>💡 {e(d["verdict"])}</div>' if d.get("verdict") else ''
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;height:1440px;position:relative;background:linear-gradient(160deg,#fef0e2,#fbe0cc);padding:50px 46px}}
.t{{font-size:68px;font-weight:900;text-align:center;color:#2a1e14;margin-bottom:8px;line-height:1.2}}.o{{color:#e8552d}}
.sub{{text-align:center;font-size:30px;color:#a8815e;font-weight:700;margin-bottom:30px}}
.cols{{display:flex;gap:22px}}.col{{flex:1;background:#fff;border-radius:24px;padding:28px 24px;box-shadow:0 12px 28px rgba(180,120,60,.14)}}
.h{{font-size:44px;font-weight:900;text-align:center;padding:16px;border-radius:16px;margin-bottom:20px;color:#fff}}
.row{{font-size:27px;line-height:1.45;padding:18px 4px;border-bottom:1px solid #f0e6d8;color:#5a4a3a}}.row b{{color:#2a1e14}}
.vs{{position:absolute;top:410px;left:50%;transform:translate(-50%,-50%);background:linear-gradient(135deg,#e8552d,#c73e1a);color:#fff;font-size:38px;font-weight:900;width:96px;height:96px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:2;box-shadow:0 6px 16px rgba(0,0,0,.25)}}
.verdict{{margin-top:32px;background:#2a1e14;color:#ffd98a;border-radius:22px;padding:30px 32px;font-size:36px;font-weight:800;text-align:center;line-height:1.4}}
.cta{{position:absolute;bottom:0;left:0;right:0;height:110px;background:#3a2a1a;color:#ffd83b;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:900}}</style>
<div class=t>{e(d["title"])}</div>{f'<div class=sub>{e(d.get("sub",""))}</div>' if d.get("sub") else ''}<div class=cols>{col(d["a"],"#5a96d6")}{col(d["b"],"#e89440")}</div><div class=vs>VS</div>{vd}<div class=cta>{e(d.get("cta",""))}</div>'''

def t_路线(d):  # data: kicker, title, hl, sub, steps[{n,color,name,age,note}], cta
    steps="".join(f'''<div class=step><div class=num style="background:{s.get("color","#7bd389")}">{e(s.get("n",""))}</div>
<div class=box><b>{e(s["name"])}<span class=age>{e(s.get("age",""))}</span></b><small>{e(s.get("note",""))}</small></div></div>'''+('<div class=arrow>↓</div>' if s is not d["steps"][-1] else '') for s in d["steps"])
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;height:1440px;position:relative;overflow:hidden;background:linear-gradient(160deg,#fef6ee,#f7e4d6)}}
.kicker{{position:absolute;top:70px;left:60px;background:#2b2b2b;color:#ffd98a;font-size:26px;font-weight:800;padding:10px 26px;border-radius:30px}}
.title{{position:absolute;top:150px;left:60px;right:60px;font-size:84px;font-weight:900;color:#2a2320;line-height:1.15}}.mk{{color:#e8552d}}
.sub{{position:absolute;top:340px;left:60px;right:60px;font-size:30px;color:#9a8a7d;font-weight:600}}
.steps{{position:absolute;top:430px;left:56px;right:56px}}.step{{display:flex;align-items:center;background:rgba(255,255,255,.92);border-radius:26px;padding:24px 30px;box-shadow:0 12px 26px rgba(180,120,80,.15)}}
.num{{flex:none;width:92px;height:92px;border-radius:24px;color:#fff;font-size:42px;font-weight:900;display:flex;align-items:center;justify-content:center;margin-right:26px}}
.box b{{font-size:38px;color:#2a2320}}.age{{font-size:22px;color:#b09a8a;margin-left:12px;background:#f4ebe2;padding:3px 14px;border-radius:20px}}.box small{{display:block;font-size:25px;color:#8a7a6d;margin-top:6px}}
.arrow{{text-align:center;font-size:32px;color:#d9a066;margin:8px 0 8px 44px}}
.cta{{position:absolute;bottom:0;left:0;right:0;height:120px;background:#2b2b2b;color:#ffd98a;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:900}}</style>
<div class=kicker>{e(d.get("kicker",""))}</div><div class=title>{e(d["title"])}</div><div class=sub>{e(d.get("sub",""))}</div>
<div class=steps>{steps}</div><div class=cta>{e(d.get("cta",""))}</div>'''

def t_排行(d):  # data: title_a, title_b, tiers[{name,color,rows[[名,...,学费]]}], cta
    sec=""
    for tier in d["tiers"]:
        rows=""
        for r in tier["rows"]:
            mid=" · ".join(e(c) for c in r[1:-1])
            rows+=f'<div class=row><div class=nm>{e(r[0])}</div><div class=mid>{mid}</div><div class=fee>{e(r[-1])}</div></div>'
        sec+=f'<div class=sec><div class=tier style="background:{tier["color"]}">{e(tier["name"])}</div>{rows}</div>'
    cta=f'<div class=cta>{e(d.get("cta",""))}</div>' if d.get("cta") else ''
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;background:linear-gradient(160deg,#fdf7ee,#f7ebd9);padding:40px 30px 44px}}
.t{{text-align:center;margin-bottom:26px}}.a{{font-size:72px;font-weight:900;color:#b0473c;line-height:1.15}}.b{{font-size:58px;font-weight:900;color:#2a5a8c}}
.sec{{margin-bottom:26px;border-radius:20px;overflow:hidden;box-shadow:0 8px 22px rgba(160,100,60,.12)}}
.tier{{font-size:38px;font-weight:900;color:#fff;text-align:center;padding:16px}}
.row{{display:flex;align-items:center;background:#fff;padding:20px 24px;border-bottom:1px solid #f2e8da;font-size:30px}}
.row:nth-child(even){{background:#fdf6ec}}
.nm{{flex:none;width:340px;font-weight:800;color:#3a2a1a}}.mid{{flex:1;font-size:24px;color:#9a8776}}.fee{{flex:none;font-weight:900;color:#b0473c;font-size:32px}}
.cta{{background:#2a1e14;color:#ffd98a;border-radius:18px;text-align:center;padding:24px;font-size:38px;font-weight:900}}</style>
<div class=t><div class=a>{e(d["title_a"])}</div><div class=b>{e(d["title_b"])}</div></div>{sec}{cta}'''

def t_片单(d):  # data: title_a, title_b, stages[{name,sub,color,items[{img?,name,note}]}], badge
    sec=""
    for st in d["stages"]:
        cells=""
        for it in st["items"]:
            thumb=f'<img src="{it["img"]}" class=th>' if it.get("img") else f'<div class=th style="background:linear-gradient(135deg,{st["color"]},{st["color"]}bb);display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:800;text-align:center;padding:6px">{e(it["name"])}</div>'
            cells+=f'<div class=cell>{thumb}<div class=cn>{e(it["name"])}</div>{f"<div class=note>{e(it.get("note",""))}</div>" if it.get("note") else ""}</div>'
        sec+=f'<div class=stage><div class=stg style="background:{st["color"]}"><div class=sn>{e(st["name"])}</div><div class=ss>{e(st.get("sub",""))}</div></div><div class=grid>{cells}</div></div>'
    badge=f'<div class=badge>⚠️ {e(d.get("badge","可能含AI生成内容"))}</div>'
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:1080px;background:linear-gradient(160deg,#fff0f5,#ffe8ee);padding:70px 26px 40px;position:relative}}
.badge{{position:absolute;top:20px;left:26px;font-size:20px;color:#888;background:rgba(255,255,255,.7);padding:6px 14px;border-radius:14px}}
.t{{text-align:center;margin-bottom:26px}}.a{{font-size:76px;font-weight:900;color:#e8302f;line-height:1.1;-webkit-text-stroke:1px #fff}}.b{{font-size:64px;font-weight:900;color:#1a3a8c}}
.stage{{display:flex;background:rgba(255,255,255,.85);border-radius:22px;padding:16px;margin-bottom:18px;box-shadow:0 8px 22px rgba(200,120,140,.14)}}
.stg{{flex:none;width:150px;border-radius:16px;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px}}
.sn{{font-size:36px;font-weight:900}}.ss{{font-size:22px;font-weight:700;margin-top:6px;opacity:.95;text-align:center}}
.grid{{flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-left:14px}}
.cell{{text-align:center}}.th{{width:100%;height:150px;border-radius:10px;object-fit:cover;box-shadow:0 3px 8px rgba(0,0,0,.12)}}
.cn{{font-size:20px;font-weight:700;color:#333;margin-top:6px;line-height:1.2}}.note{{font-size:16px;color:#999}}</style>
{badge}<div class=t><div class=a>{e(d["title_a"])}</div><div class=b>{e(d["title_b"])}</div></div>{sec}'''

TEMPLATES={"金句":t_金句,"数字":t_数字,"痛点":t_痛点,"清单":t_清单,"对比":t_对比,"路线":t_路线,"排行":t_排行,"片单":t_片单}

def render(html, out, w=1080, h=1440):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.NamedTemporaryFile("w",suffix=".html",delete=False,encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8>"+html); tmp=f.name
    subprocess.run([CHROME,"--headless=new","--disable-gpu","--hide-scrollbars",
        "--force-device-scale-factor=2",f"--window-size={w},{h}",f"--screenshot={out}",f"file://{tmp}"],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    os.remove(tmp)

def main():
    spec=json.load(open(sys.argv[1],encoding="utf-8"))
    ok=0
    for i,card in enumerate(spec):
        try:
            html=TEMPLATES[card["type"]](card["data"])
            out=os.path.join(OUTDIR,card.get("out",f"card_{i:03d}.png"))
            render(html,out,card.get("w",1080),card.get("h",1440)); ok+=1
        except Exception as ex:
            print(f"[跳过 #{i}] {ex}")
    print(f"✅ 生成 {ok}/{len(spec)} 张 → {OUTDIR}")

if __name__=="__main__": main()
