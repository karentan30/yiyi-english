#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朗诵演讲类·AI童声朗读demo视频（多主题版）
样式对标 Sunny Words v2 音乐播放器版(Karen认可的爆款格式)：假播放器UI + 双语歌词滚动堆叠
（无真实儿童照片——用主题色背景代替"唱歌小孩"素材图，因本视频是AI合成童声demo，不能暗示真人小孩出镜）
零成本：edge-tts免费童声 + Chrome无头截图 + ffmpeg拼接
每个主题独立配色(TOPICS[key]["bg"]/["cta_bg"])，布局/头像/字幕结构完全复用《我的祖国》定稿版，只换色+文案+POEM
用法：python3 gen_recitation_video.py                 → 生成 NEW_TOPIC_KEYS 里全部新主题（不含我的祖国，它已定稿别再碰）
      python3 gen_recitation_video.py changcheng jiaoshi → 只生成指定主题
"""
import os, subprocess, tempfile, sys, html as _H

HERE = os.path.dirname(os.path.abspath(__file__))
AVATAR_ICON_REL = os.path.join("我的祖国", "assets", "avatar_icon.png")  # 所有主题共用同一张AI插画头像，非真人小孩照片
AVATAR_ICON = os.path.join(HERE, AVATAR_ICON_REL)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = '"PingFang SC","Microsoft YaHei",sans-serif'
W, H = 1080, 1440  # 小红书图文笔记标准尺寸(3:4)，与同系列卡片(gen_recitation_cards.py)保持一致
VOICE = "en-US-AnaNeural"  # edge-tts 免费童声（Cute/Cartoon风格），非真人
GOLD = "#f4c542"  # 全系列统一金色点缀，跟主题背景色形成"深色+金"的国潮既视感，只换底色不换这个锚点色

def e(s): return _H.escape(str(s)) if s is not None else ""

def render(html_body, out, w=W, h=H):
    doc = f"<!doctype html><meta charset=utf-8><style>*{{margin:0;box-sizing:border-box;font-family:{FONT}}}body{{width:{w}px;height:{h}px;overflow:hidden}}</style>{html_body}"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(doc); tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=2", f"--window-size={w},{h}", f"--screenshot={out}", f"file://{tmp}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)

def ffprobe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    return float(out)

def tts_line(text, out_mp3):
    subprocess.run(["edge-tts", "--voice", VOICE, "--text", text, "--write-media", out_mp3],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def to_wav(mp3_in, wav_out):
    subprocess.run(["ffmpeg", "-y", "-i", mp3_in, "-ar", "44100", "-ac", "1", wav_out],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def make_silence(seconds, out_wav):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-t", f"{seconds}", out_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

MARCH_STEPS = [
    (261.63, 329.63, 392.00, 523.25),  # C-E-G-C5（I，主和弦，齐奏更饱满）
    (349.23, 440.00, 523.25),          # F-A-C5（IV）
    (392.00, 493.88, 587.33),          # G-B-D5（V，推向解决）
    (261.63, 329.63, 392.00, 523.25),  # C-E-G-C5（I，落回主调）
]
STEP_DUR = 1.4
STEP_OFFSET = 0.55  # 稳定的进行曲步伐感，比琶音密集紧凑，但每一步仍是衰减音，不会持续嗡鸣

def _make_chord_note(freqs, dur, out_wav):
    """一步"齐奏和弦"：几个音同时响+指数衰减包络，营造进行曲"整齐有力"的气势，而不是持续嗡鸣"""
    parts = [f"(0.5*sin(2*PI*{f}*t)+0.3*sin(2*PI*2*{f}*t)+0.15*sin(2*PI*4*{f}*t)+0.08*sin(2*PI*7*{f}*t))" for f in freqs]
    scale = round(1.3 / len(freqs), 3)
    expr = f"(({'+'.join(parts)})*{scale})*exp(-4.0*t)"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={dur}",
        "-af", "aformat=sample_rates=44100:channel_layouts=mono", out_wav],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def make_bgm(duration, tmpdir, out_wav):
    """零成本自制轻音乐床：明亮进行曲风格——I-IV-V-I和弦齐奏按稳定步伐循环，全系列统一同一种BGM气质(未接到修改要求)
    每一步都是衰减音，绝不留持续发声的层，所以不会嗡鸣"""
    n_steps = int(duration // STEP_OFFSET) + 2
    step_files = []
    for i in range(n_steps):
        freqs = MARCH_STEPS[i % len(MARCH_STEPS)]
        nf = os.path.join(tmpdir, f"bgm_step{i}.wav")
        _make_chord_note(freqs, STEP_DUR, nf)
        step_files.append(nf)

    inputs = []
    for nf in step_files:
        inputs += ["-i", nf]
    delay_parts, mix_labels = [], []
    for j in range(n_steps):
        off_ms = int(j * STEP_OFFSET * 1000)
        delay_parts.append(f"[{j}]adelay={off_ms}|{off_ms}[d{j}]")
        mix_labels.append(f"[d{j}]")
    fc = ";".join(delay_parts) + ";" + "".join(mix_labels) + f"amix=inputs={n_steps}:normalize=0[arp]"
    fc += ";[arp]lowpass=f=3200,volume=1.3[arpo]"
    fade_out_st = max(0.1, duration - 3)
    fc += f";[arpo]volume=0.45,afade=t=in:st=0:d=1.0,afade=t=out:st={fade_out_st}:d=3,aformat=sample_rates=44100:channel_layouts=mono[out]"

    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", fc, "-map", "[out]", "-t", str(duration), out_wav]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

AI_BADGE = "AI示范朗读 · 非真人童声"
INTRO_HOLD = 0.6   # 开头别拖，前几秒容易划走影响完播/转化
OUTRO_HOLD = 1.0
OVERVIEW_HOLD = 2.0
CTA_HOLD = 3.5

def gap_for(line_dur):
    """句间停顿按本句时长动态给，读完到切下一句之间留出跟读窗口（专家评审：0.45s固定间隔孩子来不及跟读）"""
    return round(max(1.0, line_dur * 0.6), 2)

AVATAR_CORNER_W, AVATAR_CORNER_H = 300, 200  # 右上角头像占位尺寸
AVATAR_INSET = 24  # 头像离画布边缘的安全边距，避免贴死画布角
CONTENT_RIGHT = AVATAR_CORNER_W + AVATAR_INSET + 16  # 标题/AI徽章统一让右的宽度，跟头像对齐成"左栏文字+右栏头像"两栏结构

def ai_badge_html():
    """右下角小角标，不占标题区，字号缩小到刚好能看清但不抢视觉焦点"""
    return f'<div style="position:absolute;bottom:20px;right:20px;z-index:9"><span style="display:inline-block;background:rgba(0,0,0,.55);color:#fff;font-size:16px;font-weight:800;padding:6px 14px;border-radius:16px;letter-spacing:.5px;white-space:nowrap">⚠️ {e(AI_BADGE)}</span></div>'

def avatar_badge_html():
    """右上角AI头像（插画风，非真人小孩照片）·跟页面其他卡片同款圆角+描边，融入整体设计"""
    return f'''<div style="position:absolute;top:{AVATAR_INSET}px;right:{AVATAR_INSET}px;width:{AVATAR_CORNER_W}px;height:{AVATAR_CORNER_H}px;overflow:hidden;border-radius:24px 24px 0 60px;border:4px solid {GOLD};box-shadow:0 8px 20px rgba(0,0,0,.3);z-index:8">
<img src="file://{AVATAR_ICON}" style="width:100%;height:100%;object-fit:cover;object-position:top center">
</div>'''

# ======================== 主题配色库（9个新主题+1个已定稿的我的祖国原样保留）========================
# bg/cta_bg 遵循同一套"深色起 → 中间过渡 → 稍亮收"的三段渐变公式(跟我的祖国RED_BG一致的亮度曲线)，
# 保证GOLD(#f4c542)在任何主题上都读得清，只换色相不破坏可读性。
TOPICS = {
    "woguozuguo": {  # 已定稿，保留原样，不在 NEW_TOPIC_KEYS 里，不会被批量重跑
        "folder": "我的祖国",
        "title_en": "My Motherland", "title_cn": "我的祖国",
        "player_title": "跟读 · 我的祖国",
        "bg": "linear-gradient(165deg,#8c1a1a 0%,#a3221f 55%,#c0392b 100%)",
        "cta_bg": "linear-gradient(165deg,#7a1414,#a3221f)",
        "icons": ["🏠", "🇨🇳", "🏛️", "🏯", "🌊", "👧", "🗣️", "🏠", "❤️"],
        "poem": [
            ("I live in China, a country I love.", "我住在中国，我爱这片土地。"),
            ("Our flag is red, with five golden stars.", "我们的国旗是红色的，上面有五颗金星。"),
            ("Beijing is our capital, old and new.", "北京是我们的首都，古老又崭新。"),
            ("The Great Wall winds across the hills.", "长城蜿蜒在群山之上。"),
            ("The Yellow River flows through our land.", "黄河奔流过我们的土地。"),
            ("I have black hair and bright black eyes.", "我有黑色的头发，明亮的黑眼睛。"),
            ("I speak Chinese, and I say it with pride.", "我说中文，我骄傲地说出它。"),
            ("I am Chinese. This is my home.", "我是中国人，这里是我的家。"),
            ("I love you, China.", "我爱你，中国。"),
        ],
    },
    "changcheng": {
        "folder": "长城",
        "title_en": "The Great Wall", "title_cn": "长城",
        "player_title": "跟读 · 长城",
        "bg": "linear-gradient(165deg,#3d2e1f 0%,#5c4530 55%,#7a5c42 100%)",
        "cta_bg": "linear-gradient(165deg,#2e2216,#5c4530)",
        "icons": ["🧱", "⛰️", "🪨", "🏡", "☁️", "🚶", "💪", "🇨🇳", "😊"],
        "poem": [
            ("The Great Wall is old, and the Great Wall is strong.", "长城很古老，长城很坚固。"),
            ("It climbs up mountains, so high and so long.", "它爬上高山，又高又长。"),
            ("Long ago, people built it stone by stone.", "很久以前，人们一块石头一块石头地建造它。"),
            ("It guards our land, it guards our home.", "它守护我们的土地，守护我们的家。"),
            ("From the wall, I see the clouds and the sky.", "站在长城上，我能看见云朵和天空。"),
            ("I walk along it, and I wonder why.", "我沿着它走，心中充满好奇。"),
            ("It took great courage, it took great hands.", "它凝聚了无数的勇气与双手。"),
            ("The Great Wall stands for our motherland.", "长城代表着我们的祖国。"),
            ("I am proud, for the Great Wall is mine.", "我很骄傲，因为长城是属于我的。"),
        ],
    },
    "wuxingqi": {
        "folder": "五星红旗",
        "title_en": "The Five-Star Red Flag", "title_cn": "五星红旗",
        "player_title": "跟读 · 五星红旗",
        "bg": "linear-gradient(165deg,#5c0f0f 0%,#7a1414 55%,#931c1c 100%)",
        "cta_bg": "linear-gradient(165deg,#4a0d0d,#7a1414)",
        "icons": ["⭐", "🚩", "✨", "🌟", "🏫", "🧍", "🫡", "🇨🇳", "❤️"],
        "poem": [
            ("Red is the color, and stars shine bright.", "红色是它的颜色，星星闪闪发光。"),
            ("Our flag flies high, from morning to night.", "我们的国旗高高飘扬，从早到晚。"),
            ("One big star, and four small by its side.", "一颗大星星，旁边四颗小星星。"),
            ("Together they shine, together with pride.", "它们一起闪耀，一起骄傲。"),
            ("It flies at school, it flies in the square.", "它飘扬在学校，飘扬在广场。"),
            ("Every Monday morning, we all stand there.", "每个星期一的早晨，我们都站在那里。"),
            ("We sing our song, we salute with our hand.", "我们唱着国歌，向它敬礼。"),
            ("The flag is a symbol of our motherland.", "国旗是我们祖国的象征。"),
            ("I love this flag, red as my heart.", "我爱这面国旗，红得像我的心。"),
        ],
    },
    "guoqing": {
        "folder": "国庆节",
        "title_en": "National Day", "title_cn": "国庆节",
        "player_title": "跟读 · 国庆节",
        "bg": "linear-gradient(165deg,#8c2a10 0%,#b8431a 55%,#d65e22 100%)",
        "cta_bg": "linear-gradient(165deg,#7a2410,#b8431a)",
        "icons": ["🍂", "🎉", "🏮", "😄", "🚩", "🎆", "🌱", "🎂", "🇨🇳"],
        "poem": [
            ("October comes, and the sky turns clear.", "十月来了，天空变得晴朗。"),
            ("It's National Day, a day we hold dear.", "这是国庆节，我们珍视的一天。"),
            ("Red flags and lanterns fill every street.", "红旗和灯笼挂满每条街道。"),
            ("Smiling faces, everyone we meet.", "每个人脸上都带着笑容。"),
            ("We watch the flag rise, up in the air.", "我们看着国旗冉冉升起。"),
            ("Fireworks bloom, like flowers everywhere.", "烟花绽放，像漫天的花朵。"),
            ("Year by year, our country has grown.", "年复一年，我们的祖国不断成长。"),
            ("Happy birthday, China, the land I call home!", "生日快乐，中国，这是我的家。"),
            ("On this day, I'm proud to say: I'm Chinese!", "在这一天，我骄傲地说：我是中国人！"),
        ],
    },
    "zhongqiu": {
        "folder": "中秋节",
        "title_en": "Mid-Autumn Festival", "title_cn": "中秋节",
        "player_title": "跟读 · 中秋节",
        "bg": "linear-gradient(165deg,#0d1b3e 0%,#16295c 55%,#233b7a 100%)",
        "cta_bg": "linear-gradient(165deg,#0a1530,#16295c)",
        "icons": ["🌕", "🌙", "👨‍👩‍👧", "🥮", "👵", "⭐", "🌝", "💛", "🙏"],
        "poem": [
            ("The moon is round, and shining so bright.", "月亮又圆又亮。"),
            ("Mid-Autumn Festival, my favorite night.", "中秋节，我最喜欢的夜晚。"),
            ("We sit together, my family and me.", "我们一家人坐在一起。"),
            ("Sharing mooncakes, as sweet as can be.", "分享着甜甜的月饼。"),
            ("Grandma tells stories of a lady on the moon.", "奶奶讲着关于月亮上仙女的故事。"),
            ("Under the stars, we sing an old tune.", "在星空下，我们唱着古老的歌谣。"),
            ("Far or near, we look at the same moon above.", "无论多远，我们抬头看的是同一轮月亮。"),
            ("Mid-Autumn Festival is a festival of love.", "中秋节是团圆和爱的节日。"),
            ("I wish my family peace, and joy, and light.", "我祝愿家人平安喜乐，团团圆圆。"),
        ],
    },
    "jiaoshi": {
        "folder": "教师节",
        "title_en": "Teacher's Day", "title_cn": "教师节",
        "player_title": "跟读 · 教师节",
        "bg": "linear-gradient(165deg,#16301f 0%,#234a30 55%,#326043 100%)",
        "cta_bg": "linear-gradient(165deg,#102419,#234a30)",
        "icons": ["👩‍🏫", "🌅", "📖", "⚖️", "💛", "🌱", "📅", "🙏", "🎓"],
        "poem": [
            ("My teacher smiles, and welcomes me in.", "老师微笑着，欢迎我走进教室。"),
            ("Every morning, a new day begins.", "每天早晨，新的一天开始了。"),
            ("She teaches me letters, she teaches me songs.", "她教我认字，教我唱歌。"),
            ("She helps me see what is right, what is wrong.", "她帮我分辨对与错。"),
            ("When I make mistakes, she's patient and kind.", "当我犯错时，她耐心又善良。"),
            ("She waters my dreams, she opens my mind.", "她浇灌我的梦想，开启我的智慧。"),
            ("September comes, it's Teacher's Day today.", "九月到了，今天是教师节。"),
            ('"Thank you, teacher," is what I want to say.', "“谢谢您，老师”，这是我想说的话。"),
            ("I'll work hard and make you proud one day.", "我会努力学习，有一天让您为我骄傲。"),
        ],
    },
    "mengxiang": {
        "folder": "我的梦想",
        "title_en": "My Dream", "title_cn": "我的梦想",
        "player_title": "跟读 · 我的梦想",
        "bg": "linear-gradient(165deg,#201540 0%,#362463 55%,#4d3585 100%)",
        "cta_bg": "linear-gradient(165deg,#180f30,#362463)",
        "icons": ["✈️", "🛠️", "🌍", "🌟", "👩‍⚕️", "🧳", "💭", "💪", "✨"],
        "poem": [
            ("Some day I will fly, up high in the sky.", "有一天我会飞翔，飞向高高的天空。"),
            ("Some day I will build, some day I will try.", "有一天我会去创造，去尝试。"),
            ("I dream of a world that is kind and free.", "我梦想一个善良而自由的世界。"),
            ("I dream of the person that I want to be.", "我梦想成为我想成为的人。"),
            ("Maybe a doctor, maybe a star.", "也许是医生，也许是明星。"),
            ("Maybe I'll travel, near and far.", "也许我会去旅行，走遍天涯海角。"),
            ("Dreams don't come easy, I know that it's true.", "梦想不会轻易实现，我知道这是真的。"),
            ("But I will work hard, in all that I do.", "但我会在每件事上努力。"),
            ("This is my dream, and I will make it come true.", "这是我的梦想，我会让它成真。"),
        ],
    },
    "mama": {
        "folder": "我的妈妈",
        "title_en": "My Mom", "title_cn": "我的妈妈",
        "player_title": "跟读 · 我的妈妈",
        "bg": "linear-gradient(165deg,#7a2f3d 0%,#9c465a 55%,#b8637a 100%)",
        "cta_bg": "linear-gradient(165deg,#672535,#9c465a)",
        "icons": ["🌅", "🍳", "🤝", "🤗", "🛌", "😊", "💼", "🌦️", "❤️"],
        "poem": [
            ("My mom wakes up early, before the sun.", "妈妈总是在太阳升起前就早早醒来。"),
            ("She makes my breakfast, and then we run.", "她给我做早餐，然后我们一起出发。"),
            ("She holds my hand when I cross the street.", "过马路时她牵着我的手。"),
            ("Her hug is warm, her voice is sweet.", "她的拥抱很温暖，她的声音很甜美。"),
            ("When I am sick, she stays by my side.", "我生病时，她一直陪在我身边。"),
            ("When I do well, she's full of pride.", "我表现好时，她满脸骄傲。"),
            ("She works all day, but never complains.", "她辛苦一整天，却从不抱怨。"),
            ("Through sunny days and rainy days.", "无论晴天还是雨天。"),
            ("Mom, I love you, more than words can say.", "妈妈，我爱你，胜过千言万语。"),
        ],
    },
    "jiaxiang": {
        "folder": "我的家乡",
        "title_en": "My Hometown", "title_cn": "我的家乡",
        "player_title": "跟读 · 我的家乡",
        "bg": "linear-gradient(165deg,#123c4a 0%,#1d5c68 55%,#2c7a6f 100%)",
        "cta_bg": "linear-gradient(165deg,#0d2e38,#1d5c68)",
        "icons": ["🏞️", "⛰️", "🛤️", "☀️", "🐦", "💬", "🧭", "🏠", "💚"],
        "poem": [
            ("My hometown sits by a river, calm and wide.", "我的家乡坐落在一条宽阔平静的河边。"),
            ("Green hills and old streets, side by side.", "青山与老街并肩而立。"),
            ("I know every corner, every little lane.", "我熟悉每一个角落，每一条小巷。"),
            ("I've walked them in sunshine, I've walked them in rain.", "我在阳光下走过，也在雨中走过。"),
            ("The smell of the morning, the sound of the birds.", "清晨的气息，鸟儿的歌声。"),
            ("My hometown speaks to me, without any words.", "我的家乡，无需言语，便懂得我心。"),
            ("No matter how far away I may roam.", "无论我走到多远的地方。"),
            ("My heart always circles back to my home.", "我的心总会绕回我的家。"),
            ("This is my hometown, and I love it so.", "这就是我的家乡，我深深地爱着它。"),
        ],
    },
    "pengyou": {
        "folder": "我的好朋友",
        "title_en": "My Best Friend", "title_cn": "我的好朋友",
        "player_title": "跟读 · 我的好朋友",
        "bg": "linear-gradient(165deg,#a35c0a 0%,#c97d18 55%,#e0992a 100%)",
        "cta_bg": "linear-gradient(165deg,#8a4c08,#c97d18)",
        "icons": ["🤗", "😄", "🍪", "🤫", "🤝", "💛", "⏰", "🧡", "🙏"],
        "poem": [
            ("I have a friend, kind and true.", "我有一个善良真诚的朋友。"),
            ("We laugh together, me and you.", "我们一起欢笑，你和我。"),
            ("We share our snacks, we share our toys.", "我们分享零食，分享玩具。"),
            ("We share our secrets, we share our joys.", "我们分享秘密，分享快乐。"),
            ("When I fall down, you help me stand.", "当我摔倒时，你扶我站起来。"),
            ("When you feel sad, I hold your hand.", "当你难过时，我握住你的手。"),
            ("We don't need much, just time to play.", "我们不需要太多，只需要时间一起玩耍。"),
            ("Best friends forever, come what may.", "永远的好朋友，无论发生什么。"),
            ("Thank you, my friend, for being you.", "谢谢你，我的朋友，谢谢你成为你自己。"),
        ],
    },
}
NEW_TOPIC_KEYS = ["changcheng", "wuxingqi", "guoqing", "zhongqiu", "jiaoshi", "mengxiang", "mama", "jiaxiang", "pengyou"]

# ---------- 帧1：全文总览（家长一眼看到整篇中英文，可截屏/利于小红书搜索）----------
def overview_frame(topic, out):
    rows = ""
    for en, cn in topic["poem"]:
        rows += f'''<div style="padding:11px 0">
<div style="font-size:37px;font-weight:800;color:#fff;line-height:1.28">{e(en)}</div>
<div style="font-size:29px;color:{GOLD};font-weight:700;margin-top:3px">{e(cn)}</div>
</div>'''
    body = f'''<div style="position:relative;width:{W}px;height:{H}px;background:{topic["bg"]};overflow:hidden;display:flex;flex-direction:column">
{ai_badge_html()}
{avatar_badge_html()}
<div style="position:absolute;bottom:64px;right:20px;z-index:9"><span style="display:inline-block;background:{GOLD};color:#3a2a10;font-size:16px;font-weight:900;padding:6px 14px;border-radius:16px;white-space:nowrap">免费领 · 中英双语朗诵稿</span></div>
<div style="flex:none;padding:100px {CONTENT_RIGHT}px 12px 56px;text-align:center;color:#fff">
  <div style="font-size:40px;font-weight:900">{e(topic["title_en"])} {e(topic["title_cn"])}</div>
  <div style="font-size:26px;color:rgba(255,255,255,.75);font-weight:700;margin-top:8px">全文预览 · 往下跟着朗读</div>
</div>
<div style="flex:1;padding:4px 60px;overflow:hidden">{rows}</div>
<div style="flex:none;padding-bottom:34px;text-align:center;font-size:21px;color:rgba(255,255,255,.65)">原创双语朗诵稿 · 仅供亲子跟读练习参考</div>
</div>'''
    render(body, out)

# ---------- 帧2：仿音乐播放器 · 全文9句一屏到底（全程都在屏幕上，读到哪句哪句放大高亮，其余变暗但看得清）----------
def fmt_t(sec):
    m = int(sec // 60); s = int(sec % 60)
    return f"{m}:{s:02d}"

def lines_all_html(topic, active_idx):
    """9句话从头到尾都在同一屏上（不分页、不滚走），当前句放大高亮，其余变暗但仍看得清
    每行固定槽位高度，只变字号/透明度不变占位，切句时文字块不会整体跳动"""
    rows = []
    for j, (en, cn) in enumerate(topic["poem"]):
        active = (j == active_idx)
        size_en = 40 if active else 32
        size_zh = 33 if active else 23
        opacity = 1.0 if active else 0.55
        cur = "border-bottom:3px solid #FF8C42;padding-bottom:3px;display:inline-block" if active else ""
        icon = f'<span style="font-size:26px;margin-right:8px;vertical-align:2px">{topic["icons"][j]}</span>' if active else ""
        rows.append(f'''<div style="height:108px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:{opacity}">
<div style="font-size:{size_en}px;font-weight:900;color:#fff;line-height:1.18;text-shadow:0 2px 10px rgba(0,0,0,.5);white-space:nowrap">{icon}{e(en)}</div>
<div style="font-size:{size_zh}px;font-weight:700;color:{GOLD};margin-top:4px;{cur}">{e(cn)}</div>
</div>''')
    return "".join(rows)

def player_frame(topic, active_idx, start, end, total, out):
    progress_pct = min(100, max(0, start / total * 100))
    lyric_html = lines_all_html(topic, active_idx) if active_idx is not None else ""
    body = f'''<div style="position:relative;width:{W}px;height:{H}px;background:{topic["bg"]};overflow:hidden">
{ai_badge_html()}
{avatar_badge_html()}
<div style="position:absolute;top:86px;left:0;right:0;text-align:center;padding:0 {CONTENT_RIGHT}px 0 50px">
  <div style="font-size:50px;font-weight:900;color:#fff">{e(topic["player_title"])}</div>
</div>
<div style="position:absolute;left:0;right:0;top:190px;bottom:236px;padding:0 46px;display:flex;flex-direction:column;justify-content:center">{lyric_html}</div>
<div style="position:absolute;left:0;right:0;bottom:120px;padding:0 40px">
  <div style="text-align:center;font-size:16px;color:rgba(255,255,255,.55);margin-bottom:14px">原创双语朗诵稿 · 仅供跟读参考</div>
  <div style="padding:0 10px">
    <div style="display:flex;justify-content:space-between;font-size:18px;color:rgba(255,255,255,.75);margin-bottom:6px"><span>{fmt_t(start)}</span><span>{fmt_t(total)}</span></div>
    <div style="position:relative;height:5px;border-radius:3px;background:rgba(255,255,255,.28)">
      <div style="position:absolute;left:0;top:0;bottom:0;width:{progress_pct:.1f}%;background:#fff;border-radius:3px"></div>
      <div style="position:absolute;top:50%;left:{progress_pct:.1f}%;transform:translate(-50%,-50%);width:14px;height:14px;border-radius:50%;background:#fff;box-shadow:0 0 10px rgba(255,255,255,.7)"></div>
    </div>
  </div>
  <div style="margin-top:18px;display:flex;align-items:center;justify-content:center">
    <span style="width:56px;height:56px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:24px;color:#a3221f">⏸</span>
  </div>
</div>
</div>'''
    render(body, out)

def cta_frame(topic, out):
    body = f'''<div style="position:relative;width:{W}px;height:{H}px;background:{topic["cta_bg"]};color:#fff;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 70px">
{ai_badge_html()}
{avatar_badge_html()}
<div style="font-size:60px;font-weight:900;line-height:1.35;margin-bottom:46px">想要这份<br><span style="color:{GOLD}">《{e(topic["title_cn"])}》</span>全文？</div>
<div style="background:rgba(255,255,255,.14);border-radius:26px;padding:40px 36px;font-size:38px;font-weight:800;line-height:1.6">评论区扣【朗诵稿】，我发全文</div>
<div style="margin-top:44px;font-size:30px;color:rgba(255,255,255,.9);font-weight:700;line-height:1.6">娃念完想知道发音对不对？进群外教帮你过一遍</div>
<div style="margin-top:30px;font-size:26px;color:{GOLD};font-weight:800">划走可能就找不到啦，先点赞收藏～</div>
<div style="position:absolute;bottom:44px;left:64px;right:64px;font-size:22px;color:rgba(255,255,255,.6)">发音练手/示范/参考 · 不承诺效果 · 全程无微信号，口令仅在群内公开发放</div>
</div>'''
    render(body, out)

def main(topic_key):
    topic = TOPICS[topic_key]
    outdir = os.path.join(HERE, topic["folder"])
    tmpdir = os.path.join(outdir, "_tmp_video")
    os.makedirs(tmpdir, exist_ok=True)
    poem = topic["poem"]

    print(f"[{topic_key}] ① 合成逐句童声音频（edge-tts, 免费）…")
    line_wavs = []
    for i, (en, _) in enumerate(poem):
        mp3 = os.path.join(tmpdir, f"line{i}.mp3")
        wav = os.path.join(tmpdir, f"line{i}.wav")
        tts_line(en, mp3)
        to_wav(mp3, wav)
        line_wavs.append(wav)
    line_durs = [ffprobe_dur(w) for w in line_wavs]
    gaps = [gap_for(d) for d in line_durs]
    print("   逐句时长(s):", [round(d, 2) for d in line_durs])

    timeline = []
    cum = INTRO_HOLD
    timeline.append((0.0, INTRO_HOLD))
    for d, gap in zip(line_durs, gaps):
        timeline.append((cum, cum + d + gap))
        cum += d + gap
    total = cum + OUTRO_HOLD

    print(f"[{topic_key}] ② 生成静音间隔 + 拼接音轨…")
    overview_sil = os.path.join(tmpdir, "overview_sil.wav"); make_silence(OVERVIEW_HOLD, overview_sil)
    intro_sil = os.path.join(tmpdir, "intro_sil.wav"); make_silence(INTRO_HOLD, intro_sil)
    gap_sils = []
    for i, gap in enumerate(gaps):
        p = os.path.join(tmpdir, f"gap_sil{i}.wav"); make_silence(gap, p); gap_sils.append(p)
    outro_sil = os.path.join(tmpdir, "outro_sil.wav"); make_silence(OUTRO_HOLD, outro_sil)
    cta_sil = os.path.join(tmpdir, "cta_sil.wav"); make_silence(CTA_HOLD, cta_sil)

    audio_list = os.path.join(tmpdir, "audio_concat.txt")
    with open(audio_list, "w", encoding="utf-8") as f:
        f.write(f"file '{overview_sil}'\n")
        f.write(f"file '{intro_sil}'\n")
        for w, gsil in zip(line_wavs, gap_sils):
            f.write(f"file '{w}'\n")
            f.write(f"file '{gsil}'\n")
        f.write(f"file '{outro_sil}'\n")
        f.write(f"file '{cta_sil}'\n")
    final_audio = os.path.join(tmpdir, "final_audio.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audio_list, "-c", "copy", final_audio],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[{topic_key}] ②b 配一条轻音乐床（自制正弦和弦，零成本无版权问题）…")
    voice_dur = ffprobe_dur(final_audio)
    bgm_wav = os.path.join(tmpdir, "bgm.wav")
    make_bgm(voice_dur, tmpdir, bgm_wav)
    mixed_audio = os.path.join(tmpdir, "mixed_audio.wav")
    subprocess.run(["ffmpeg", "-y", "-i", final_audio, "-i", bgm_wav,
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]",
        "-map", "[aout]", mixed_audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    final_audio = mixed_audio

    print(f"[{topic_key}] ③ 渲染视频帧（Chrome无头截图）…")
    frames = []
    ov_png = os.path.join(tmpdir, "f_overview.png"); overview_frame(topic, ov_png)
    frames.append((ov_png, OVERVIEW_HOLD))

    intro_png = os.path.join(tmpdir, "f_intro.png"); player_frame(topic, None, 0.0, INTRO_HOLD, total, intro_png)
    frames.append((intro_png, INTRO_HOLD))

    for i in range(len(poem)):
        start, end = timeline[i + 1]
        p = os.path.join(tmpdir, f"f_line{i}.png")
        player_frame(topic, i, start, end, total, p)
        frames.append((p, end - start))

    last = len(poem) - 1
    outro_png = os.path.join(tmpdir, "f_outro.png")
    player_frame(topic, last, cum, total, total, outro_png)
    frames.append((outro_png, OUTRO_HOLD))

    cta_png = os.path.join(tmpdir, "f_cta.png"); cta_frame(topic, cta_png)
    frames.append((cta_png, CTA_HOLD))

    print(f"[{topic_key}] ④ ffmpeg 拼接图片序列 + 音轨…")
    concat_path = os.path.join(tmpdir, "concat_video.txt")
    with open(concat_path, "w", encoding="utf-8") as f:
        for path, dur in frames:
            f.write(f"file '{path}'\n")
            f.write(f"duration {dur}\n")
        f.write(f"file '{frames[-1][0]}'\n")

    OUT = os.path.join(outdir, f"{topic['folder']}-AI童声朗读demo.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_path,
        "-i", final_audio,
        "-map", "0:v", "-map", "1:a",
        "-vf", f"scale={W}:{H},format=yuv420p",
        "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUT,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ [{topic_key}] 输出 → {OUT}")
    return OUT

if __name__ == "__main__":
    keys = sys.argv[1:] or NEW_TOPIC_KEYS
    for k in keys:
        main(k)
