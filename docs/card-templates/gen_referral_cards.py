#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YiYi 微信裂变 & 转介绍卡片生成器（自写HTML·Chrome渲染·零成本）
产出：
  推荐有礼裂变海报 3 款（配色变体：雾霾蓝 / 豆沙粉 / 淡橄榄）
  朋友圈学员成果/晒卡模板 3 款（款A进步对比 / 款B测评晒卡 / 款C好评截图）
全部 1080x1440 竖版。莫兰迪低饱和 · 证书/成绩单质感 · 无微信号无二维码 · 留文字链接。
用法：python3 gen_referral_cards.py
"""
import os, subprocess, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "生成", "微信裂变转介绍")
os.makedirs(OUTDIR, exist_ok=True)
FONT = '"PingFang SC","Microsoft YaHei",sans-serif'
LINK = "mylumee.cn/yiyi-ceping"

def render(html, out, w=1080, h=1440):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8>" + html)
        tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=2", f"--window-size={w},{h}",
        f"--screenshot={out}", f"file://{tmp}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)


# ========== 1. 推荐有礼裂变海报（证书质感·莫兰迪） ==========
# 配色变体：每套 3 色封顶（底/主色/强调）
PALETTES = {
    "雾霾蓝": dict(bg="#eef2f4", card="#ffffff", ink="#2f3d47", main="#5b7d94",
                  accent="#c58a4e", soft="#e7edf1", line="#dfe6ea", faint="#8a9aa6"),
    "豆沙粉": dict(bg="#f5eeec", card="#ffffff", ink="#3f3230", main="#a56b64",
                  accent="#8a9a6b", soft="#f0e6e3", line="#ece1de", faint="#a08d88"),
    "淡橄榄": dict(bg="#f0f1e9", card="#ffffff", ink="#33372b", main="#6e7a54",
                  accent="#b07d4a", soft="#e8 eae0".replace(" ", ""), line="#e2e5d8", faint="#8d937d"),
}

def referral_poster(c, parent_ph="[家长名]"):
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}
body{{width:1080px;height:1440px;background:{c["bg"]};position:relative;overflow:hidden}}
.frame{{position:absolute;inset:44px;background:{c["card"]};border-radius:34px;
  box-shadow:0 24px 60px rgba(70,80,90,.10);border:1px solid {c["line"]};padding:64px 68px}}
/* 顶部品牌 + 报告小字 */
.brandrow{{display:flex;align-items:center;justify-content:space-between;
  border-bottom:2px solid {c["soft"]};padding-bottom:26px}}
.brand{{font-size:40px;font-weight:900;color:{c["ink"]};letter-spacing:1px}}
.brand small{{font-size:24px;font-weight:700;color:{c["main"]};margin-left:8px;letter-spacing:0}}
.doct{{font-size:24px;color:{c["faint"]};font-weight:700;letter-spacing:2px}}
/* 专属邀请位 */
.invite{{margin-top:34px;font-size:33px;color:{c["ink"]};font-weight:800}}
.invite b{{color:{c["main"]}}}
/* 主标题：核心利益+数字（严格 2 行） */
.title{{margin-top:22px;font-size:70px;font-weight:900;color:{c["ink"]};line-height:1.22}}
.title .hl{{color:{c["accent"]}}}
.title .amt{{color:{c["main"]}}}
.sub{{margin-top:18px;font-size:31px;color:{c["faint"]};font-weight:700;line-height:1.5}}
/* 双方福利：两枚证书章 */
.rewards{{margin-top:38px;display:flex;gap:26px}}
.rw{{flex:1;background:{c["soft"]};border:2px solid {c["line"]};border-radius:24px;
  padding:28px 28px;text-align:center}}
.rw .who{{font-size:28px;color:{c["faint"]};font-weight:800;letter-spacing:1px}}
.rw .big{{font-size:66px;font-weight:900;color:{c["main"]};margin:10px 0 4px;line-height:1}}
.rw.b .big{{color:{c["accent"]}}}
.rw .u{{font-size:30px;font-weight:800;color:{c["ink"]}}}
.rw .d{{font-size:25px;color:{c["faint"]};font-weight:700;margin-top:8px}}
/* 三步 */
.steps{{margin-top:36px}}
.stephd{{font-size:26px;color:{c["faint"]};font-weight:800;letter-spacing:3px;margin-bottom:16px}}
.step{{display:flex;align-items:center;margin-bottom:16px}}
.sn{{flex:none;width:54px;height:54px;border-radius:50%;background:{c["main"]};color:#fff;
  font-size:29px;font-weight:900;display:flex;align-items:center;justify-content:center;margin-right:22px}}
.st{{font-size:32px;font-weight:800;color:{c["ink"]}}}
/* 信任背书行 */
.trust{{position:absolute;left:68px;right:68px;bottom:160px;
  border-top:2px solid {c["soft"]};padding-top:24px;
  font-size:27px;color:{c["main"]};font-weight:800;text-align:center;letter-spacing:1px}}
.trust span{{color:{c["faint"]};margin:0 6px}}
/* 底部文字链接（无二维码/无微信号） */
.cta{{position:absolute;left:44px;right:44px;bottom:44px;height:96px;
  background:{c["ink"]};border-radius:0 0 34px 34px;color:#fff;
  display:flex;align-items:center;justify-content:center;gap:14px}}
.cta .k{{font-size:30px;font-weight:700;opacity:.85}}
.cta .l{{font-size:34px;font-weight:900;color:#fff;
  background:{c["accent"]};padding:8px 22px;border-radius:14px;letter-spacing:.5px}}
.corner{{position:absolute;width:26px;height:26px;border-color:{c["accent"]}}}
</style>
<div class=frame>
  <div class=brandrow>
    <div class=brand>YiYi <small>少儿英语</small></div>
    <div class=doct>推 荐 有 礼</div>
  </div>
  <div class=invite><b>{parent_ph}</b> 邀请你，一起给孩子测测英语</div>
  <div class=title>推荐1位朋友，各得<span class=amt>¥500</span><br><span class=amt>课程金</span> + 好友<span class=hl>首课8折</span></div>
  <div class=sub>推荐无上限 · 推得越多，攒得越多</div>
  <div class=rewards>
    <div class="rw a">
      <div class=who>推 荐 人 得</div>
      <div class=big>¥500</div>
      <div class=u>课程抵扣券</div>
      <div class=d>朋友报名后到账</div>
    </div>
    <div class="rw b">
      <div class=who>好 友 得</div>
      <div class=big>8折</div>
      <div class=u>首课优惠</div>
      <div class=d>新家庭专属</div>
    </div>
  </div>
  <div class=steps>
    <div class=stephd>三 步 领 取</div>
    <div class=step><div class=sn>1</div><div class=st>把这张卡 / 测评链接分享给朋友</div></div>
    <div class=step><div class=sn>2</div><div class=st>朋友给孩子报名体验课</div></div>
    <div class=step><div class=sn>3</div><div class=st>你和朋友，各得一份福利</div></div>
  </div>
  <div class=trust>欧美外教 <span>·</span> TESOL 认证 <span>·</span> 已服务 3000+ 家庭</div>
  <div class=cta><span class=k>了解 / 给娃测评　</span><span class=l>{LINK}</span></div>
</div>'''


# ========== 2. 朋友圈学员成果/晒卡模板（含占位·学管填空即用） ==========
NOTE_BG = "#fff6e6"; NOTE_INK = "#9a6a1a"; NOTE_BORDER = "#f0d9a8"

def _ops_note(text):
    # 顶部给运营看的红字提示（发布前删/替换真实内容）
    return f'''<div class=opsnote>⚠️ {text}</div>'''

# 款A：进步对比卡
def tmpl_A():
    P = PALETTES["雾霾蓝"]
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}
body{{width:1080px;height:1440px;background:{P["bg"]};position:relative;overflow:hidden}}
.opsnote{{position:absolute;top:0;left:0;right:0;background:{NOTE_BG};color:{NOTE_INK};
  font-size:24px;font-weight:800;text-align:center;padding:16px 30px;border-bottom:2px dashed {NOTE_BORDER};z-index:5;line-height:1.4}}
.frame{{position:absolute;top:96px;left:44px;right:44px;bottom:44px;background:#fff;border-radius:34px;
  box-shadow:0 24px 60px rgba(70,80,90,.10);border:1px solid {P["line"]};padding:56px 60px}}
.hd{{display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid {P["soft"]};padding-bottom:22px}}
.brand{{font-size:34px;font-weight:900;color:{P["ink"]}}}.brand small{{font-size:22px;color:{P["main"]};margin-left:6px}}
.badge{{font-size:23px;color:{P["faint"]};font-weight:800;letter-spacing:2px}}
.who{{margin-top:34px;font-size:52px;font-weight:900;color:{P["ink"]}}}
.who .ph{{color:{P["main"]}}}
.meta{{margin-top:12px;font-size:30px;color:{P["faint"]};font-weight:700}}
.cmp{{margin-top:44px;display:flex;align-items:stretch;gap:20px}}
.side{{flex:1;border-radius:22px;padding:34px 28px;position:relative}}
.before{{background:{P["soft"]};border:2px solid {P["line"]}}}
.after{{background:#f2efe6;border:2px solid #e6dcc4}}
.lab{{font-size:26px;font-weight:900;letter-spacing:2px;margin-bottom:16px}}
.before .lab{{color:{P["faint"]}}}.after .lab{{color:{P["accent"]}}}
.txt{{font-size:36px;font-weight:800;color:{P["ink"]};line-height:1.45}}
.arrow{{flex:none;align-self:center;font-size:52px;color:{P["accent"]};font-weight:900}}
.fb{{margin-top:40px;background:{P["soft"]};border-left:8px solid {P["main"]};border-radius:16px;
  padding:30px 32px;font-size:33px;color:{P["ink"]};font-weight:700;line-height:1.5}}
.fb .q{{color:{P["main"]};font-weight:900}}
.foot{{position:absolute;left:60px;right:60px;bottom:52px;border-top:2px solid {P["soft"]};padding-top:24px}}
.trust{{font-size:26px;color:{P["main"]};font-weight:800;text-align:center;letter-spacing:1px}}
.trust span{{color:{P["faint"]};margin:0 6px}}
.disc{{font-size:22px;color:{P["faint"]};text-align:center;margin-top:12px;font-weight:600}}
</style>
{_ops_note("真实案例需家长授权 · 不编造 · 替换[占位]为真实内容后再发")}
<div class=frame>
  <div class=hd><div class=brand>YiYi <small>少儿英语</small></div><div class=badge>学 员 成 长 记 录</div></div>
  <div class=who><span class=ph>[学员昵称]</span> · [几年级]</div>
  <div class=meta>在 YiYi 学习 [X] 个月</div>
  <div class=cmp>
    <div class="side before"><div class=lab>刚 来 时</div><div class=txt>[例：不敢开口<br>只会背单词]</div></div>
    <div class=arrow>→</div>
    <div class="side after"><div class=lab>现 在</div><div class=txt>[例：能和外教<br>日常对话]</div></div>
  </div>
  <div class=fb><span class=q>“</span>[粘家长真实反馈一句·如：孩子现在主动开口，敢说了]<span class=q>”</span></div>
  <div class=foot>
    <div class=trust>欧美外教 <span>·</span> TESOL 认证 <span>·</span> 已服务 3000+ 家庭</div>
    <div class=disc>真实学员成长 · 个体情况不同 · 仅供参考，不代表提分承诺</div>
  </div>
</div>'''

# 款B：测评晒卡引导
def tmpl_B():
    P = PALETTES["豆沙粉"]
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}
body{{width:1080px;height:1440px;background:{P["bg"]};position:relative;overflow:hidden}}
.opsnote{{position:absolute;top:0;left:0;right:0;background:{NOTE_BG};color:{NOTE_INK};
  font-size:24px;font-weight:800;text-align:center;padding:16px 30px;border-bottom:2px dashed {NOTE_BORDER};z-index:5;line-height:1.4}}
.frame{{position:absolute;top:96px;left:44px;right:44px;bottom:44px;background:#fff;border-radius:34px;
  box-shadow:0 24px 60px rgba(90,70,70,.10);border:1px solid {P["line"]};padding:60px 62px}}
.hd{{display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid {P["soft"]};padding-bottom:22px}}
.brand{{font-size:34px;font-weight:900;color:{P["ink"]}}}.brand small{{font-size:22px;color:{P["main"]};margin-left:6px}}
.badge{{font-size:23px;color:{P["faint"]};font-weight:800;letter-spacing:2px}}
.title{{margin-top:48px;font-size:64px;font-weight:900;color:{P["ink"]};line-height:1.3}}
.title .hl{{color:{P["main"]}}}
.sub{{margin-top:18px;font-size:30px;color:{P["faint"]};font-weight:700}}
/* 段位阶梯示意（占位） */
.ladder{{margin-top:50px}}
.tier{{display:flex;align-items:center;background:{P["soft"]};border-radius:18px;
  padding:22px 28px;margin-bottom:16px;border:2px solid transparent}}
.tier.on{{background:#f2efe3;border-color:{P["accent"]}}}
.tn{{flex:none;width:64px;height:64px;border-radius:16px;background:#fff;color:{P["faint"]};
  font-size:30px;font-weight:900;display:flex;align-items:center;justify-content:center;margin-right:24px;border:2px solid {P["line"]}}}
.tier.on .tn{{background:{P["accent"]};color:#fff;border-color:{P["accent"]}}}
.td{{font-size:34px;font-weight:800;color:{P["ink"]}}}
.tier .mark{{margin-left:auto;font-size:26px;color:{P["accent"]};font-weight:900}}
.cta{{position:absolute;left:44px;right:44px;bottom:44px;height:120px;
  background:{P["ink"]};border-radius:0 0 34px 34px;color:#fff;
  display:flex;flex-direction:column;align-items:center;justify-content:center}}
.cta .k{{font-size:30px;font-weight:700;opacity:.9;margin-bottom:8px}}
.cta .l{{font-size:36px;font-weight:900;color:#fff;background:{P["main"]};padding:8px 24px;border-radius:14px}}
</style>
{_ops_note("段位/结果替换为孩子真实测评结果后再发 · 需家长同意 · 不编造")}
<div class=frame>
  <div class=hd><div class=brand>YiYi <small>少儿英语</small></div><div class=badge>英 语 段 位 测 评</div></div>
  <div class=title>今天带娃测了<br><span class=hl>英语段位</span></div>
  <div class=sub>3 分钟 · 6 大能力维度 · 对标 CEFR</div>
  <div class=ladder>
    <div class=tier><div class=tn>1</div><div class=td>入门 · 认读单词</div></div>
    <div class="tier on"><div class=tn>3</div><div class=td>[娃所在段位·如：能日常对话]</div><div class=mark>孩子在这</div></div>
    <div class=tier><div class=tn>5</div><div class=td>进阶 · 流利表达</div></div>
  </div>
  <div class=cta><span class=k>你也带娃测测看 →</span><span class=l>{LINK}</span></div>
</div>'''

# 款C：好评截图卡
def tmpl_C():
    P = PALETTES["淡橄榄"]
    return f'''<style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}
body{{width:1080px;height:1440px;background:{P["bg"]};position:relative;overflow:hidden}}
.opsnote{{position:absolute;top:0;left:0;right:0;background:{NOTE_BG};color:{NOTE_INK};
  font-size:24px;font-weight:800;text-align:center;padding:16px 30px;border-bottom:2px dashed {NOTE_BORDER};z-index:5;line-height:1.4}}
.frame{{position:absolute;top:96px;left:44px;right:44px;bottom:44px;background:#fff;border-radius:34px;
  box-shadow:0 24px 60px rgba(70,80,60,.10);border:1px solid {P["line"]};padding:56px 58px}}
.hd{{display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid {P["soft"]};padding-bottom:22px}}
.brand{{font-size:34px;font-weight:900;color:{P["ink"]}}}.brand small{{font-size:22px;color:{P["main"]};margin-left:6px}}
.badge{{font-size:23px;color:{P["faint"]};font-weight:800;letter-spacing:2px}}
.htitle{{margin-top:40px;font-size:56px;font-weight:900;color:{P["ink"]}}}
.htitle .hl{{color:{P["main"]}}}
.qmark{{font-size:130px;color:{P["soft"]};font-weight:900;line-height:.6;margin:24px 0 -30px}}
.bubbles{{margin-top:30px}}
.bub{{background:{P["soft"]};border-radius:24px;padding:30px 34px;margin-bottom:22px;position:relative}}
.bub .avatar{{position:absolute;top:-14px;left:26px;background:{P["main"]};color:#fff;
  font-size:22px;font-weight:800;padding:6px 18px;border-radius:16px}}
.bub p{{font-size:34px;color:{P["ink"]};font-weight:700;line-height:1.5;margin-top:10px}}
.stars{{color:{P["accent"]};font-size:32px;margin-top:12px;letter-spacing:4px}}
.foot{{position:absolute;left:58px;right:58px;bottom:52px;border-top:2px solid {P["soft"]};padding-top:24px}}
.trust{{font-size:27px;color:{P["main"]};font-weight:800;text-align:center;letter-spacing:1px}}
.trust span{{color:{P["faint"]};margin:0 6px}}
.link{{text-align:center;margin-top:14px;font-size:26px;color:{P["faint"]};font-weight:700}}
.link b{{color:{P["ink"]}}}
</style>
{_ops_note("粘贴家长真实好评截图或原话 · 需家长授权 · 不编造 · 替换[占位]后发")}
<div class=frame>
  <div class=hd><div class=brand>YiYi <small>少儿英语</small></div><div class=badge>家 长 真 实 反 馈</div></div>
  <div class=htitle>家长们<span class=hl>怎么说</span></div>
  <div class=qmark>“</div>
  <div class=bubbles>
    <div class=bub><div class=avatar>[家长A]</div><p>[粘家长好评原话·如：外教很有耐心，孩子每次上课都很期待]</p><div class=stars>★★★★★</div></div>
    <div class=bub><div class=avatar>[家长B]</div><p>[粘家长好评原话·如：学了几个月，孩子敢开口说了]</p><div class=stars>★★★★★</div></div>
  </div>
  <div class=foot>
    <div class=trust>欧美外教 <span>·</span> TESOL 认证 <span>·</span> 已服务 3000+ 家庭</div>
    <div class=link>了解 / 给娃测评　<b>{LINK}</b></div>
  </div>
</div>'''


def main():
    jobs = []
    # 3 款推荐海报配色变体
    for name, pal in PALETTES.items():
        jobs.append((referral_poster(pal), f"推荐有礼海报_{name}.png"))
    # 3 款朋友圈模板
    jobs.append((tmpl_A(), "朋友圈_款A_进步对比.png"))
    jobs.append((tmpl_B(), "朋友圈_款B_测评晒卡.png"))
    jobs.append((tmpl_C(), "朋友圈_款C_好评截图.png"))

    for html, fn in jobs:
        out = os.path.join(OUTDIR, fn)
        render(html, out)
        print(f"✅ {fn}")
    print(f"\n全部 → {OUTDIR}")

if __name__ == "__main__":
    main()
