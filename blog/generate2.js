// YiYi English Blog Generator — 80 more articles via DeepSeek
const https = require('https');
const fs = require('fs');
const path = require('path');

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
if (!DEEPSEEK_API_KEY) { console.error('Missing DEEPSEEK_API_KEY'); process.exit(1); }

const OUTPUT_DIR = path.join(__dirname, 'articles');
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const topics = [
  { slug: 'yiyi-article-021', title: '孩子英语口语差的5个根本原因' },
  { slug: 'yiyi-article-022', title: '外教1对1 vs 大班课，哪个适合你的孩子' },
  { slug: 'yiyi-article-023', title: '3-6岁英语启蒙，家长最常踩的坑' },
  { slug: 'yiyi-article-024', title: '雅思口语7分备考计划（完整版）' },
  { slug: 'yiyi-article-025', title: '海外华人孩子双语教育全攻略' },
  { slug: 'yiyi-article-026', title: '孩子学了5年英语还是"哑巴英语"怎么办' },
  { slug: 'yiyi-article-027', title: '职场人如何在3个月内突破英语表达瓶颈' },
  { slug: 'yiyi-article-028', title: '欧美外教和菲律宾外教的真实区别' },
  { slug: 'yiyi-article-029', title: '线上英语课怎么选？10个关键指标' },
  { slug: 'yiyi-article-030', title: '让孩子爱上说英语的6个家庭游戏' },
  { slug: 'yiyi-article-031', title: '雅思托福口语考场真实题型解析' },
  { slug: 'yiyi-article-032', title: '成人英语学习：为什么你的方法错了' },
  { slug: 'yiyi-article-033', title: '孩子英语发音不准怎么纠正' },
  { slug: 'yiyi-article-034', title: '如何评估一个英语老师是否真的好' },
  { slug: 'yiyi-article-035', title: '移民前英语准备：你需要的不只是词汇量' },
  { slug: 'yiyi-article-036', title: '英语学习焦虑症：如何克服开口恐惧' },
  { slug: 'yiyi-article-037', title: '商务英语：外企人必会的50个表达' },
  { slug: 'yiyi-article-038', title: '孩子不愿意说英语？心理根源和解法' },
  { slug: 'yiyi-article-039', title: '海外华人二代中文英文双语平衡策略' },
  { slug: 'yiyi-article-040', title: '英语学习效率低？可能是方法问题' },
  { slug: 'yiyi-article-041', title: '小学英语和中学英语的衔接怎么做' },
  { slug: 'yiyi-article-042', title: '留学申请面试英语准备全指南' },
  { slug: 'yiyi-article-043', title: '固定外教一对一的优势到底在哪里' },
  { slug: 'yiyi-article-044', title: '英语听力差的核心原因和训练方法' },
  { slug: 'yiyi-article-045', title: '如何给孩子创造英语环境（家里没外教也能做到）' },
  { slug: 'yiyi-article-046', title: '职场英语：如何在会议中用英语发言不尴尬' },
  { slug: 'yiyi-article-047', title: '孩子英语作文写作提升全攻略' },
  { slug: 'yiyi-article-048', title: '英语音标学习：大人也能学好的方法' },
  { slug: 'yiyi-article-049', title: '语言学习黄金期：为什么3-12岁特别重要' },
  { slug: 'yiyi-article-050', title: '海外华人孩子拒绝说中文怎么办' },
  { slug: 'yiyi-article-051', title: '英语阅读理解从60分到90分的方法' },
  { slug: 'yiyi-article-052', title: '孩子学英语注意力不集中怎么办' },
  { slug: 'yiyi-article-053', title: '美式英语 vs 英式英语：有什么实际区别' },
  { slug: 'yiyi-article-054', title: '英语学习App推荐：哪些真的有用' },
  { slug: 'yiyi-article-055', title: '孩子英语词汇量怎么高效扩充' },
  { slug: 'yiyi-article-056', title: '考研英语和日常英语：学习策略有什么不同' },
  { slug: 'yiyi-article-057', title: '外教课前怎么预习效果翻倍' },
  { slug: 'yiyi-article-058', title: '英语学习坚持不下去？这5个方法帮你保持动力' },
  { slug: 'yiyi-article-059', title: '给孩子选英语课：家长问得最多的10个问题' },
  { slug: 'yiyi-article-060', title: '英语写作常见错误：中国学生最容易犯的' },
  { slug: 'yiyi-article-061', title: '从零开始学英语：成人自学路线图' },
  { slug: 'yiyi-article-062', title: '孩子英语考试成绩好但不会说话的原因' },
  { slug: 'yiyi-article-063', title: '英语学习中的"高原期"：如何突破平台' },
  { slug: 'yiyi-article-064', title: '孩子英语课堂上不开口怎么办' },
  { slug: 'yiyi-article-065', title: '海外华人职场英语：如何和本地同事高效沟通' },
  { slug: 'yiyi-article-066', title: '托福口语从20分到27分的备考策略' },
  { slug: 'yiyi-article-067', title: '孩子学英语的正确打开方式：分龄指南' },
  { slug: 'yiyi-article-068', title: '英语口语中的"填充词"：如何减少eh、um、like' },
  { slug: 'yiyi-article-069', title: '如何帮孩子建立英语自信心' },
  { slug: 'yiyi-article-070', title: '成人英语口语7天快速入门计划' },
  { slug: 'yiyi-article-071', title: '英语学习误区：背单词到底有没有用' },
  { slug: 'yiyi-article-072', title: '国际学校英语和普通学校英语的差距怎么弥合' },
  { slug: 'yiyi-article-073', title: '孩子英语课回来不复习怎么办' },
  { slug: 'yiyi-article-074', title: '海外华人：英语生活化的100个实用技巧' },
  { slug: 'yiyi-article-075', title: '英语演讲技巧：公开场合说英语不紧张' },
  { slug: 'yiyi-article-076', title: '孩子英语敏感期：如何把握最佳学习窗口' },
  { slug: 'yiyi-article-077', title: '留学后英语还是很差怎么回事' },
  { slug: 'yiyi-article-078', title: '英语学习中的石化效应怎么破' },
  { slug: 'yiyi-article-079', title: '给老人学英语的最简单方法' },
  { slug: 'yiyi-article-080', title: '英语学习投资回报率：怎么选性价比最高的方式' },
  { slug: 'yiyi-article-081', title: '孩子学英语：如何与外教建立良好关系' },
  { slug: 'yiyi-article-082', title: '英语自我介绍：从30秒到3分钟的模版' },
  { slug: 'yiyi-article-083', title: '职场英语邮件写作：让老外秒回的技巧' },
  { slug: 'yiyi-article-084', title: '孩子英语课外阅读推荐书单（分年龄）' },
  { slug: 'yiyi-article-085', title: '英语发音美化：减少中国口音的6个方法' },
  { slug: 'yiyi-article-086', title: '英语学习时间管理：每天只有30分钟怎么学' },
  { slug: 'yiyi-article-087', title: '孩子双语思维怎么培养' },
  { slug: 'yiyi-article-088', title: '雅思写作Task 2高分结构模板' },
  { slug: 'yiyi-article-089', title: '海外工作英语生存手册：第一个月怎么过' },
  { slug: 'yiyi-article-090', title: '英语学习的神经科学：大脑是怎么习得语言的' },
  { slug: 'yiyi-article-091', title: '孩子学英语：家长最应该做和最不应该做的事' },
  { slug: 'yiyi-article-092', title: '商务英语谈判技巧：如何用英语赢得客户' },
  { slug: 'yiyi-article-093', title: '英语口音问题：发音不标准影响多大' },
  { slug: 'yiyi-article-094', title: '孩子的英语课程进度慢怎么加速' },
  { slug: 'yiyi-article-095', title: '海外华人：如何用英语融入当地社区' },
  { slug: 'yiyi-article-096', title: '英语学习书单：成人提升的10本必读' },
  { slug: 'yiyi-article-097', title: '孩子英语学习目标设定：家长怎么正确引导' },
  { slug: 'yiyi-article-098', title: '职场英语：电话视频会议英语全攻略' },
  { slug: 'yiyi-article-099', title: '孩子学英语要不要参加比赛' },
  { slug: 'yiyi-article-100', title: '英语学习是一辈子的事：如何持续进步' },
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
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;color:#1e2d40;background:#f0f8ff;line-height:1.8}
.header{background:#fff;border-bottom:1px solid #dce8f5;padding:14px 20px}
.brand{font-size:20px;font-weight:700;color:#1a56db;text-decoration:none}
.container{max-width:800px;margin:0 auto;padding:40px 20px}
h1{font-size:26px;font-weight:700;line-height:1.4;margin-bottom:20px;color:#1e2d40}
h2{font-size:20px;font-weight:700;margin:36px 0 14px;color:#1e2d40;border-left:4px solid #1a56db;padding-left:12px}
h3{font-size:17px;font-weight:700;margin:22px 0 10px;color:#1a56db}
p{margin-bottom:14px;font-size:15px;color:#3a4a5c}
.faq-section{background:#e8f0fe;border-radius:16px;padding:24px;margin:36px 0}
.faq-item{margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid #c5d8f5}
.faq-item:last-child{border:none;margin:0;padding:0}
.faq-q{display:block;font-size:15px;font-weight:800;color:#1e2d40;margin-bottom:8px}
.faq-a{font-size:14px;color:#3a4a5c}
.cta-box{background:linear-gradient(135deg,#1a56db,#0e3fa8);border-radius:16px;padding:28px;text-align:center;margin:40px 0;color:#fff}
.cta-box h3{color:#fff;font-size:20px;margin-bottom:10px}
.cta-box p{color:rgba(255,255,255,0.85);margin-bottom:20px}
.cta-btn{display:inline-block;background:#fff;color:#1a56db;font-weight:800;font-size:16px;padding:14px 32px;border-radius:12px;text-decoration:none}
footer{background:#0d1e35;color:rgba(255,255,255,0.5);text-align:center;padding:24px;font-size:12px}
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
  <h3>准备好突破英语了吗？</h3>
  <p>YiYi English固定欧美外教1对1，第1节课完全免费，专属教学规划+管家全程伴读。</p>
  <a href="https://yiyienglish.com/#contact" class="cta-btn">预约免费试听课 →</a>
</div>
</div>
<footer>© 2026 YiYi English · yiyienglish.com · 实际效果因学员情况而异</footer>
</body>
</html>`;
}

async function main() {
  console.log(`Generating ${topics.length} YiYi English blog articles (batch 2)...`);
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
  console.log('Done! All 80 articles generated.');
}

main();
