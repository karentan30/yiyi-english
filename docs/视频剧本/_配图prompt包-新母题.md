# 配图 Prompt 包 · 新母题（朗诵/夏令营）

> 用途：交出图窗口直接跑。**铁律**：
> ① AI只出**背景/插画，不出任何文字**（模型渲中英文必糊）；双语稿+标题用卡引擎/剪映叠上去。
> ② 尺寸小红书竖版 **1080×1440（3:4）**，构图顶部/中部留空给标题。
> ③ 人物必含：年龄+华人(Chinese)+发型+情绪+风格+负面词。禁西方脸、禁乱指、禁鬼脸。
> ④ 工具：文字卡底图/确定性→ComfyUI免费；叙事插画(如囊萤夜读)→ComfyUI RealVisXL 或 GPT-image(海报级更好·付费)。
> ⑤ 出图前须经Karen确认prompt+出图工具+成本。

---

## 一、朗诵演讲类

### 稿1《我的祖国》封面/卡片底图（爱国红金）
- **用途**：封面 + 双语朗诵卡背景
- **Prompt(EN)**：`A bright warm children's-book illustration of Tiananmen Gate at golden sunrise, a red Chinese national flag with five golden stars waving against a clear blue sky, soft red-and-gold palette, majestic and hopeful mood, clean symmetrical composition with generous empty space at the top and center for a title, warm cinematic morning light, high detail, flat illustration style, no text, no words, no letters`
- **Negative**：`text, words, letters, watermark, logo, dark, gloomy, cluttered, low quality, distorted, extra limbs, realistic photo`
- **排版**：顶部大字「My Motherland 我的祖国」+ 角标「第X集·英语朗诵」，中部双语稿逐句。

### 稿2《囊萤夜读》封面+内页插画（中国故事·叙事插画）
- **用途**：封面 + 内页插画（建议GPT-image出海报级）
- **Prompt(EN)**：`A 10-year-old Chinese boy in simple ancient Han-dynasty robe, short black hair, calm focused studious expression, sitting at a low wooden desk deep at night reading bamboo scrolls, a small translucent silk pouch filled with glowing fireflies casting soft warm golden light on the pages, the rest of the room in gentle darkness, traditional Chinese ink-and-color storybook illustration, magical peaceful diligent mood, warm firefly glow as the only light source, empty space at top for a title, no text, no words`
- **Negative**：`text, words, letters, modern clothing, western facial features, extra fingers, deformed hands, blurry, low quality, scary, horror, glasses`
- **排版**：顶部「用英语讲中国故事《囊萤夜读》Reading by Firefly Light」，插画配双语故事。

### 稿3《教师节》封面（节日暖橙）
- **用途**：封面 + 节日双语卡背景
- **Prompt(EN)**：`A warm cozy flat illustration of a teacher's wooden desk, a shiny red apple, a fresh bouquet of flowers, a green chalkboard softly blurred in the background, autumn warm orange tones, gratitude and warmth mood, children's book illustration style, clean composition with empty space at the top for a title, soft daylight, no text, no words, no letters`
- **Negative**：`text, words, letters, watermark, people faces, dark, cluttered, low quality, distorted`
- **排版**：顶部「Happy Teachers' Day 教师节快乐」，中部双语短稿。

### 稿4《三分钟英语演讲·我的梦想》封面（舞台蓝）
- **用途**：封面
- **Prompt(EN)**：`A 9-year-old Chinese child with short black hair, brave confident hopeful expression, standing on a school stage holding a microphone, a single bright warm spotlight beam from above, a softly blurred dark auditorium with faint audience silhouettes, inspiring cinematic mood, warm-to-cool stage lighting, children's book illustration style, empty space at the top for a title, no text, no words`
- **Negative**：`text, words, letters, western facial features, extra limbs, deformed hands, adult, blurry, low quality, scary`
- **排版**：顶部「3分钟英语演讲模板·我的梦想」+ 角标「照着填就能上台」。

---

## 二、夏令营截流类（封面为主，正文走免费视频库）

### 第1条《几万块夏令营回来没长进》封面（反转·损失感）
- **Prompt(EN)**：`A flat conceptual illustration split feel: a happy child at a summer camp on one side and the same child back home looking a bit lost on the other, warm muted palette, thoughtful slightly wistful mood, clean modern children's-education illustration style, generous empty space at the top for a title, soft light, no text, no words`
- **Negative**：`text, words, letters, watermark, western features, cluttered, dark, low quality, distorted`
- **排版**：顶部大字「花几万的夏令营·回来英语没长进？」副标「夏令营是加速器·不是发动机」。

### 第2条《选夏令营的坑》封面（自曝内幕）
- **Prompt(EN)**：`A flat illustration of a group of Chinese children sitting together at an overseas summer camp but chatting only among themselves, one child slightly apart, warm daylight, honest and a little ironic mood, modern education illustration style, empty space at the top for a title, no text, no words`
- **Negative**：`text, words, letters, western features only, extra limbs, deformed hands, dark, low quality`
- **排版**：顶部「一群中国娃凑一堆·还是说中文？」副标「选营先看这4件事」。

### 第3条《国内vs海外夏令营》封面（决策对比）
- **Prompt(EN)**：`A clean flat conceptual illustration of a balance scale, an airplane and a globe on one side, a calendar full of daily-practice checkmarks on the other, warm neutral palette, thoughtful decision-making mood, modern education infographic illustration style, empty space at the top for a title, no text, no words`
- **Negative**：`text, words, numbers, letters, watermark, cluttered, dark, low quality, distorted`
- **排版**：顶部「国内几千·海外几万·怎么选？」副标「关键不是出没出国·是逼不逼开口」。

---

## 三、出图执行建议
- **文字卡底图（稿1/3 + 夏令营封面）**：确定性排版为主，AI只出底图 → 走 **ComfyUI 免费**（RealVisXL/flat风格）。
- **叙事插画（稿2 囊萤夜读）**：narrative质量要求高 → **GPT-image 海报级更好（付费）**，或 ComfyUI 兜底。
- **一致性**：四个朗诵封面用统一"儿童绘本+暖光"风格家族，四系列靠主色区分（红金/夜色/暖橙/舞台蓝）。
- **成本**：ComfyUI 全部走本机 ≈¥0；若稿2用 GPT-image，须先报单张预算经Karen同意。
