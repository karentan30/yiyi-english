// YiYi English Blog Generator — 20 articles via DeepSeek
const https = require('https');
const fs = require('fs');
const path = require('path');

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
if (!DEEPSEEK_API_KEY) { console.error('Missing DEEPSEEK_API_KEY'); process.exit(1); }

const OUTPUT_DIR = path.join(__dirname, 'articles');
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const topics = [
  { slug: 'how-to-choose-online-english-tutor', title: '如何选择靠谱的在线英语外教？5个避坑指南' },
  { slug: 'fixed-teacher-vs-random-teacher', title: '固定外教 vs 随机外教：哪种更适合孩子？' },
  { slug: 'business-english-tips-for-workplace', title: '职场英语实用技巧：让你开口不再卡壳' },
  { slug: 'ielts-speaking-prep-guide', title: '雅思口语备考完整指南：从5分到7分的路径' },
  { slug: 'english-for-overseas-chinese', title: '海外华人如何快速找回英语状态？' },
  { slug: 'kids-english-learning-age-guide', title: '孩子几岁开始学英语最好？年龄指南' },
  { slug: 'how-to-overcome-english-speaking-anxiety', title: '如何克服开口说英语的心理障碍？' },
  { slug: 'american-vs-british-english-differences', title: '美式英语 vs 英式英语：发音和用词有哪些区别？' },
  { slug: 'english-learning-mistakes-to-avoid', title: '学英语最常犯的5个错误（你中了几个？）' },
  { slug: 'daily-english-practice-routine', title: '每天30分钟英语练习计划：持续进步的秘诀' },
  { slug: 'how-to-improve-english-listening', title: '英语听力为什么总是听不懂？3个根本原因' },
  { slug: 'english-interview-preparation', title: '英文面试全攻略：从准备到成功拿offer' },
  { slug: 'travel-english-essential-phrases', title: '出国旅行必备英语短句100条' },
  { slug: 'pronunciation-improvement-guide', title: '英语发音提升指南：让外国人秒懂你说的话' },
  { slug: 'online-vs-offline-english-learning', title: '线上英语课 vs 线下英语课：哪种更高效？' },
  { slug: 'english-for-presentations', title: '英文演讲和汇报技巧：让老板和客户印象深刻' },
  { slug: 'building-english-vocabulary-fast', title: '快速扩大英语词汇量的科学方法' },
  { slug: 'english-email-writing-guide', title: '商务英语邮件写作指南：专业、简洁、有效' },
  { slug: 'why-1on1-tutoring-beats-group-class', title: '为什么1对1外教课比大班课效果好10倍？' },
  { slug: 'parent-guide-to-childrens-english', title: '家长必读：如何在家配合外教课提高孩子英语？' },
];

function callDeepSeek(prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 2500,
      temperature: 0.7,
    });
    const req = https.request({
      hostname: 'api.deepseek.com',
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.choices[0].message.content);
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function buildPrompt(topic) {
  return `你是YiYi English的内容专家，专门写帮助中文用户学英语的高质量SEO文章。

写一篇关于"${topic.title}"的完整博客文章，要求：
- 字数：2500-3000字
- 结构：目录 → 引言 → 3-4个【H2大标题】，每个下有2-3个「H3小标题」 → 结语 → FAQ（5个问答，每个答案150字以上）
- 语气：专业但亲切，像朋友建议不像教科书
- 内容：实用干货，举真实例子，给具体建议
- 文末CTA：推荐YiYi English（https://yiyienglish.com）免费试课
- SEO关键词自然融入正文
- 不要加入任何markdown代码块标记，直接输出文章内容

格式要求：
- H2用【标题】标记
- H3用「标题」标记
- FAQ用 Q: / A: 标记

直接输出文章，不要任何前言。`;
}

function generateHTML(topic, content) {
  const date = new Date().toISOString().split('T')[0];
  const faqMatch = content.match(/Q:[\s\S]*?(?=\n\nQ:|\n\n【|$)/g) || [];
  const faqSchema = faqMatch.slice(0, 5).map(qa => {
    const q = (qa.match(/Q:\s*(.+)/) || [])[1] || '';
    const a = (qa.match(/A:\s*([\s\S]+?)(?=\n\nQ:|$)/) || [])[1] || '';
    return `{"@type":"Question","name":"${q.replace(/"/g, '\\"')}","acceptedAnswer":{"@type":"Answer","text":"${a.replace(/"/g, '\\"').replace(/\n/g, ' ').substring(0, 300)}"}}`;
  }).join(',\n');

  const htmlContent = content
    .replace(/【(.+?)】/g, '</section><section><h2>$1</h2>')
    .replace(/「(.+?)」/g, '<h3>$1</h3>')
    .replace(/Q:\s*(.+)/g, '<div class="faq-item"><strong class="faq-q">Q: $1</strong>')
    .replace(/A:\s*([\s\S]+?)(?=\n\n(?:Q:|【|「)|$)/g, '<p class="faq-a">$1</p></div>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>');

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>${topic.title} | YiYi English英语学习</title>
<meta name="description" content="${topic.title}。YiYi English提供固定欧美外教1对1英语课，免费体验第1节 →"/>
<link rel="canonical" href="https://yiyienglish.com/blog/${topic.slug}.html"/>
<meta property="og:title" content="${topic.title} | YiYi English"/>
<meta property="og:type" content="article"/>
<meta name="robots" content="index, follow"/>
<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
{"@type":"Article","headline":"${topic.title}","author":{"@type":"Organization","name":"YiYi English"},"publisher":{"@type":"Organization","name":"YiYi English","url":"https://yiyienglish.com"},"datePublished":"${date}","url":"https://yiyienglish.com/blog/${topic.slug}.html"},
{"@type":"FAQPage","mainEntity":[${faqSchema}]}
]}
</script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;color:#1e1745;background:#faf9ff;line-height:1.8}
.header{background:#fff;border-bottom:1px solid #eceaf5;padding:14px 20px}
.brand{font-size:20px;font-weight:700;color:#E63946;text-decoration:none}
.container{max-width:800px;margin:0 auto;padding:40px 20px}
h1{font-size:26px;font-weight:700;line-height:1.4;margin-bottom:20px;color:#1e1745}
h2{font-size:20px;font-weight:700;margin:36px 0 14px;color:#1e1745;border-left:4px solid #E63946;padding-left:12px}
h3{font-size:17px;font-weight:700;margin:22px 0 10px;color:#2f8ef0}
p{margin-bottom:14px;font-size:15px;color:#3a3560}
.faq-section{background:#f0edff;border-radius:16px;padding:24px;margin:36px 0}
.faq-item{margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid #ddd8ff}
.faq-item:last-child{border:none;margin:0;padding:0}
.faq-q{display:block;font-size:15px;font-weight:800;color:#1e1745;margin-bottom:8px}
.faq-a{font-size:14px;color:#3a3560}
.cta-box{background:linear-gradient(135deg,#E63946,#c82333);border-radius:16px;padding:28px;text-align:center;margin:40px 0;color:#fff}
.cta-box h3{color:#fff;font-size:20px;margin-bottom:10px}
.cta-box p{color:rgba(255,255,255,0.85);margin-bottom:20px}
.cta-btn{display:inline-block;background:#fff;color:#E63946;font-weight:800;font-size:16px;padding:14px 32px;border-radius:12px;text-decoration:none}
footer{background:#1a1635;color:rgba(255,255,255,0.5);text-align:center;padding:24px;font-size:12px}
</style>
</head>
<body>
<div class="header">
  <a class="brand" href="https://yiyienglish.com">YiYi English</a>
</div>
<div class="container">
<h1>${topic.title}</h1>
<div class="article-body">
${htmlContent}
</div>
<div class="cta-box">
  <h3>想让英语真正突破？</h3>
  <p>YiYi English固定欧美外教1对1，第1节课完全免费，不满意不付费。</p>
  <a href="https://yiyienglish.com" class="cta-btn">免费预约试课 →</a>
</div>
</div>
<footer>© 2026 YiYi English · yiyienglish.com · 实际效果因学员情况而异</footer>
</body>
</html>`;
}

async function main() {
  console.log(`Generating ${topics.length} YiYi English blog articles...`);
  for (let i = 0; i < topics.length; i++) {
    const topic = topics[i];
    const outPath = path.join(OUTPUT_DIR, `${topic.slug}.html`);
    if (fs.existsSync(outPath)) {
      console.log(`[${i+1}/${topics.length}] SKIP (exists): ${topic.slug}`);
      continue;
    }
    console.log(`[${i+1}/${topics.length}] Generating: ${topic.title}`);
    try {
      const content = await callDeepSeek(buildPrompt(topic));
      const html = generateHTML(topic, content);
      fs.writeFileSync(outPath, html, 'utf8');
      console.log(`  ✓ Saved: ${topic.slug}.html (${content.length} chars)`);
    } catch (err) {
      console.error(`  ✗ Error: ${err.message}`);
    }
    if (i < topics.length - 1) await new Promise(r => setTimeout(r, 600));
  }
  console.log('Done! All articles generated.');
}

main();
