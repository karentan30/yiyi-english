# ComfyUI 出图 prompt 批次 · 外教课（2026-08-28）

> 本机跑：`venv/bin/python main.py`（port 8188）｜模型：RealVisXL_V5（写实）｜零成本
> ⚠️ SD 渲染中文字是糊的——**这里只出"底图/人像/图标"，中文大标题一律用 Canva/HTML 叠**。
> 尺寸：小红书 3:4 竖版 = **1080×1440**（头像 1:1 = 1024×1024）
> 通用负面词（所有图都加）：`(worst quality, low quality:1.4), blurry, deformed, disfigured, bad anatomy, extra fingers, watermark, signature, text, letters, chinese characters, logo, jpeg artifacts`

---

## 0. 图从哪来（优先级·别啥都AI出）
1. **信息图卡（教材指南/清单/对比/路线图）→ HTML模板渲染**（中文完美·免费·对标爆款）。
   模板在 `docs/card-templates/`（已有`教材指南卡.html`+渲染好的png）。改内容→Chrome无头渲染出PNG：
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --window-size=1080,1440 --screenshot=out.png file://路径.html`
   **这是对标@PA千柚那种绿底教材卡的正确方法——不是AI，SD渲染中文会糊。**
2. **场景/氛围/实拍底图 → 免费无版权图库**（Unsplash/Pexels/Pixabay/Mixkit·直接用·免费商用）。搜 `kids learning`/`study desk`/`mother child reading`/`english book`。多数封面底图从这拿。
3. **定制场景 → ComfyUI 本机**（图库找不到的：AI vs真人对比构图等）。prompt 见下。一键启动：`cd ~/ComfyUI && venv/bin/python main.py --port 8188`。
4. **真外教/真娃 → 真实授权素材**（不用图库不用AI，必须授权）。
5. **简单封面中文大字 → Canva 叠字**。

## A. 封面底图 ComfyUI prompt（图库找不到时才用·留白给中文标题）

**A1 · 暖色书桌氛围（宝妈日常/教材/启蒙类）**
```
soft warm beige background, minimalist study desk corner, open English textbook,
a few colorful sticky notes, a cup, cozy morning sunlight, clean flat lay,
pastel tones, lots of negative space at top for text, cozy lifestyle photography,
high detail, 3:4 vertical
```

**A2 · AI vs 真人对比（AI外教对冲母题）**
```
split composition, left side a child looking at a glowing smartphone with blue AI light,
right side the same child happily talking face to face with an adult, warm vs cool contrast,
soft cinematic lighting, conceptual, clean minimal background, space for text overlay,
high detail, 3:4 vertical
```

**A3 · 绿底极简信息图底（清单/路线图/对比表类）**
```
solid soft green background (mint/sage), minimal flat design, subtle rounded panels,
a few small education icons (book, pencil, speech bubble) in corners, lots of empty center space,
clean modern infographic style, pastel, no text, 3:4 vertical
```

**A4 · 亲子学习场景（启蒙/低龄类）**
```
warm cozy home scene, an Asian mother and a young child (age 6) reading an English picture book together on a sofa, natural window light, soft focus background, heartwarming lifestyle photography, empty space at top for text, high detail, 3:4 vertical
```

**A5 · 外教上课场景（外教/领读/纠音类）**
```
online English lesson scene on a laptop screen, a friendly western foreign teacher smiling and gesturing, warm inviting home study setup, soft bokeh background, lifestyle photography, space for text at bottom, high detail, 3:4 vertical
```

---

## A+. 情绪/真人/对比封面底图（v2新封面策略·转化款首选）
> 专家结论：绿底思维导图点击率低已烂大街。**涨粉款用情绪大字报/数字冲击；转化款用真人脸/before-after**（人脸封面点击率天然高）。中文大字仍用Canva叠，这里只出"人/场景/对比"底图。

**A+1 · 真娃"憋红脸 vs 手机蓝光"（AI对冲款）**
```
split composition, left: an Asian child (age 8) looking anxious and shy, blushing, holding a smartphone glowing cold blue light; right: the same child looking frustrated trying to speak to a real adult, warm light; emotional contrast, cinematic, clean space for text, photorealistic, high detail, 3:4 vertical
```

**A+2 · before-after 真娃开口（前后对比款）**
```
before-after split, left: shy Asian child (age 7) covering mouth, hesitant, muted cool tones; right: same child confidently speaking on a small stage, bright warm light, happy; emotional transformation, photorealistic, space for center label, high detail, 3:4 vertical
```

**A+3 · 真娃对着课本发愁（痛点款"考高分不敢开口"）**
```
an Asian child (age 9) sitting at desk with a high-score English test paper, looking down frustrated and unable to speak, speech bubble empty, warm indoor light, emotional lifestyle photography, space for top text, photorealistic, high detail, 3:4 vertical
```

**A+4 · 外教带读真实上课（外教出镜款）**
```
warm screenshot-style online lesson, a friendly western foreign teacher pointing at an English textbook, encouraging expression, a child's small video window in corner, cozy home study, authentic candid feel, space for bottom subtitle text, photorealistic, high detail, 3:4 vertical
```

**A+5 · 情绪大字报底（涨粉款·数字冲击）**
```
bold minimal poster background, bright energetic solid color (coral/yellow), dynamic geometric shapes, big empty center for large number text, playful education vibe, high contrast, clean, no text, 3:4 vertical
```

> ⚠️ 真娃底图仅作**版式参考/示意**；正式发布必须用**自己学员真实素材（家长授权）**，AI生成的假娃别当"真实成果"发（信任红线）。

## B. 头像（1024×1024）

> ⚠️ **红线**：外教号(#8/#9)头像**别用 AI 假外教脸**——号称真外教却用假脸=欺骗+砸招牌。**必须用真实外教授权照片**。下面只给宝妈号/图标类的 AI prompt。

**B1 · 宝妈号头像（#1-5，各改年龄/发型/表情做差异化，别雷同）**
基础模板（填入变量）：
```
portrait of a Chinese woman, age {32/35/38}, {long straight hair / shoulder-length wavy hair / hair in a bun}, gentle warm smile, soft natural makeup, casual cozy sweater, warm indoor lighting, friendly approachable mom vibe, photorealistic, shallow depth of field, high detail, 1:1
```
- #1 团团妈：age 34, long straight hair, warm smile
- #2 朵朵妈：age 36, shoulder-length wavy hair, gentle look
- #3 果冻妈：age 32, hair in a bun, cheerful bright smile
- #4 一诺妈：age 35, long hair, soft calm smile
- #5 小柚子妈：age 33, short bob, energetic smile

**B2 · 教研老师号头像（#6）**
```
portrait of a professional Chinese female teacher, age 35, neat shoulder-length hair, confident warm smile, smart casual blazer, clean bright background, professional approachable, photorealistic, high detail, 1:1
```

**B3 · 图标类头像（#7 干货/#10 避坑/#11 测评/#13 牛娃 — 用图标不用人脸）**
```
flat vector icon logo, {open book / magnifying glass / balance scale / trophy}, minimal modern design, soft green and cream colors, rounded shapes, centered, clean white background, no text, 1:1
```
- #7 英语启蒙研究所：open book
- #10 英语课避坑指南：magnifying glass
- #11 少儿英语测评室：balance scale
- #13 牛娃养成笔记：trophy / rising star

**B4 · 垂类号 #12 校内教材配外教（课本+对话气泡插画）**
```
flat illustration icon, a school textbook with two speech bubbles above it (one Chinese, one English style), minimal cute design, soft green and warm colors, clean background, no text, 1:1
```

> #8/#9 外教号 → 真实外教授权照｜#14 官方号 → 品牌 LOGO（设计，非 AI 生成）

---

## C. 出图工作流（团队）
1. ComfyUI 跑上面 prompt 出底图/头像（每个 prompt 出 4 张选最好，自评≥8 才用）
2. 封面：底图导入 **Canva**（或 HTML 模板）→ 叠中文大标题（标题公式：数字/权威+无痛利益+锚点）
3. 内页轮播图：绿底 A3 底图 + Canva 排单词卡/对比表/清单（6-9 张）
4. 多号差异化：同母题换底图配色/换标题/换封面文案，别 14 号同一张

## D. 迭代
- 人像出废图先查：是否缺 age/发型/表情/负面词
- 中文字永远别指望 SD 出，全部 Canva/HTML 叠
- 出图前把 prompt 发群确认（省 GPU 时间），自评<8 自己重跑再交
