// Vercel Serverless Function: сохраняет заявку с сайта до открытия WhatsApp и отправляет её в Telegram.
// Переменные окружения (Vercel → Settings → Environment Variables):
//   TELEGRAM_BOT_TOKEN — токен бота от @BotFather
//   TELEGRAM_CHAT_ID   — id чата или группы, куда слать заявки (можно несколько через запятую)
// Без переменных функция отвечает 503, а сайт как обычно открывает WhatsApp — заявка не теряется.

const hits = new Map();
function limited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 8;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > max;
}
const clip = (v, n = 300) => String(v == null ? "" : v).replace(/[\u0000-\u001f]+/g, " ").trim().slice(0, n);
const esc = (s) => s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ ok: false }); return; }
  const token = process.env.TELEGRAM_BOT_TOKEN, chats = (process.env.TELEGRAM_CHAT_ID || "").split(",").map((x) => x.trim()).filter(Boolean);
  if (!token || !chats.length) { res.status(503).json({ ok: false, error: "not configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) { res.status(429).json({ ok: false }); return; }
  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } }
  b = b || {};
  if (b.website) { res.status(200).json({ ok: true }); return; } // honeypot: боты заполняют скрытое поле
  const phone = clip(b.phone, 40);
  if (phone.replace(/\D/g, "").length < 10) { res.status(400).json({ ok: false }); return; }
  const utm = b.utm && typeof b.utm === "object" ? Object.entries(b.utm).map(([k, v]) => `${clip(k, 30)}=${clip(v, 120)}`).join(", ") : "";
  const lines = [
    "<b>Заявка с сайта DezClub</b>",
    `Имя: ${esc(clip(b.name, 80))}`,
    `Телефон: ${esc(phone)}`,
    b.service ? `Услуга: ${esc(clip(b.service, 120))}` : "",
    b.city ? `Город: ${esc(clip(b.city, 60))}` : "",
    b.msg ? `Комментарий: ${esc(clip(b.msg, 600))}` : "",
    `Страница: ${esc(clip(b.page, 200))}`,
    utm ? `UTM: ${esc(utm)}` : "",
    `Время: ${new Date().toLocaleString("ru-RU", { timeZone: "Asia/Almaty" })}`,
    `Браузер: ${esc(clip(req.headers["user-agent"], 160))}`,
  ].filter(Boolean).join("\n");
  try {
    await Promise.all(chats.map((chat_id) => fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id, text: lines, parse_mode: "HTML", disable_web_page_preview: true }),
    })));
    res.status(200).json({ ok: true });
  } catch (e) {
    res.status(502).json({ ok: false });
  }
};
