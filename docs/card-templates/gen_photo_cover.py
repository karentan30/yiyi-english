#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成照片叠文字主视觉封面 · D1 磨耳朵歌单
"""
import os, sys

# 导入 render 函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_cards import render

IMG_PATH = "/Users/karen/projects/yiyi-english/docs/card-templates/生成/一诺妈/素材-唱歌小孩/唱歌小孩_02.png"
OUT_PATH = "/Users/karen/projects/yiyi-english/docs/card-templates/生成/一诺妈/D1_周一2100_磨耳朵歌单/封面-照片版.png"

FONT = '"PingFang SC","Microsoft YaHei",sans-serif'

html = f'''<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; font-family: {FONT}; }}
body {{
  width: 1080px;
  height: 1440px;
  position: relative;
  overflow: hidden;
  background: #0a0a1a;
}}

/* 全幅背景女孩照 */
.bg-photo {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
}}

/* 底部渐变遮罩：透明→深色，覆盖底部 2/3 */
.gradient-mask {{
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    transparent 15%,
    rgba(10, 10, 26, 0.35) 38%,
    rgba(10, 10, 26, 0.72) 55%,
    rgba(10, 10, 26, 0.92) 72%,
    rgba(10, 10, 26, 0.97) 85%,
    rgba(10, 10, 26, 1.0) 100%
  );
}}

/* 顶部标签胶囊 */
.top-tag {{
  position: absolute;
  top: 64px;
  left: 64px;
  background: rgba(20, 20, 40, 0.78);
  color: #fff;
  font-size: 26px;
  font-weight: 700;
  padding: 10px 26px;
  border-radius: 50px;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,0.18);
}}

/* 主文字区 */
.text-area {{
  position: absolute;
  bottom: 130px;
  left: 64px;
  right: 64px;
}}

.main-line {{
  font-size: 88px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.18;
  text-shadow: 0 2px 8px rgba(0,0,0,0.8), 0 4px 24px rgba(0,0,0,0.6);
  display: block;
}}

.highlight-line {{
  font-size: 88px;
  font-weight: 900;
  color: #FF8C42;
  line-height: 1.18;
  text-shadow: 0 2px 8px rgba(0,0,0,0.8), 0 4px 24px rgba(0,0,0,0.6);
  display: block;
}}

.sub-line {{
  font-size: 36px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.5;
  margin-top: 18px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  display: block;
}}

/* 底部栏 */
.bottom-bar {{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  padding: 0 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(10, 10, 26, 0.88);
  backdrop-filter: blur(8px);
}}

.account-name {{
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.6);
}}

.aigc-label {{
  font-size: 24px;
  font-weight: 400;
  color: rgba(180, 180, 200, 0.75);
}}
</style>

<!-- 背景照片 -->
<img class="bg-photo" src="file://{IMG_PATH}" alt="">

<!-- 渐变遮罩 -->
<div class="gradient-mask"></div>

<!-- 顶部标签 -->
<div class="top-tag">🎵 磨耳朵</div>

<!-- 中下文字区 -->
<div class="text-area">
  <span class="main-line">磨耳朵别乱放</span>
  <span class="highlight-line">这8首唱熟</span>
  <span class="main-line">= 200个词</span>
  <span class="sub-line">节奏慢 · 重复多 · 日常词密</span>
</div>

<!-- 底部栏 -->
<div class="bottom-bar">
  <span class="account-name">@一诺妈说启蒙</span>
  <span class="aigc-label">AI生成图 · AIGC</span>
</div>
'''

render(html, OUT_PATH, 1080, 1440)
print(f"✅ 已输出 → {OUT_PATH}")
