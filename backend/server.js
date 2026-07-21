// Node 18+ has fetch built-in; no import needed
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Allow requests from GitHub Pages and localhost during dev
app.use(cors({
  origin: [
    'https://karentan30.github.io',
    'https://www.yiyienglish.com',
    'http://localhost:3000',
    'http://127.0.0.1:5500',
    'null' // local file:// opens
  ]
}));
app.use(express.json());

// Health check
app.get('/health', (req, res) => res.json({ ok: true }));

// Lead capture — sends email via Resend
app.post('/api/lead', async (req, res) => {
  const { name, phone, age } = req.body || {};

  if (!name || !phone) {
    return res.status(400).json({ error: '姓名和手机号不能为空' });
  }

  const RESEND_API_KEY = process.env.RESEND_API_KEY || 're_88naYiM1_5pWkuaRCD3FBJXuJPGoZu99n';
  const TO_EMAIL = process.env.NOTIFY_EMAIL || 'tan42204@gmail.com';

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'YiYi英语 <onboarding@resend.dev>',
        to: [TO_EMAIL],
        subject: `新询盘：${name} ${phone}`,
        html: `
          <h2>YiYi英语 新预约试听</h2>
          <table style="border-collapse:collapse;width:100%;max-width:480px">
            <tr><td style="padding:8px 12px;background:#f5f1ff;font-weight:bold">家长称呼</td><td style="padding:8px 12px">${name}</td></tr>
            <tr><td style="padding:8px 12px;background:#f5f1ff;font-weight:bold">手机号</td><td style="padding:8px 12px">${phone}</td></tr>
            <tr><td style="padding:8px 12px;background:#f5f1ff;font-weight:bold">孩子年龄段</td><td style="padding:8px 12px">${age || '未填写'}</td></tr>
          </table>
          <p style="margin-top:16px;color:#666">请在24小时内联系该家长安排试听。</p>
        `
      })
    });

    if (!response.ok) {
      const err = await response.json();
      console.error('Resend error:', err);
      return res.status(502).json({ error: '邮件发送失败，请稍后重试' });
    }

    console.log(`[LEAD] ${new Date().toISOString()} | ${name} | ${phone} | ${age}`);
    return res.json({ success: true });

  } catch (e) {
    console.error('Lead API error:', e);
    return res.status(500).json({ error: '服务器错误，请稍后重试' });
  }
});

app.listen(PORT, () => {
  console.log(`YiYi English backend running on port ${PORT}`);
});
