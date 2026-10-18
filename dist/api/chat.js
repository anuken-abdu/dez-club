// Vercel Serverless Function: ИИ-консультант DezClub.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и сайт автоматически переключается на встроенный автоответчик.

const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";
const PHONE = "+7 700 525 01 08";

const SYSTEM = `Ты — онлайн-консультант санитарной службы DezClub (ТОО "DezClub", БИН 260340008945) на сайте.
Компания: дезинсекция (тараканы, клопы, блохи, муравьи, моль, осы, мокрицы, короеды, мухи, пылевые клещи), дезинфекция (вирусы, бактерии, плесень, после болезни и затопления), дератизация (крысы, мыши), фумигация (склады, зерно, древесина), дезодорация, озонирование, акарицидная обработка участков от клещей, гербицидная обработка, санитарная обработка для юрлиц, pest control для предприятий.
Основная база — Алматы, Турксибский район, ул. Бекмаханова, 96. Работаем по всему Казахстану.
Для бизнеса: договор, акты выполненных работ, журналы учёта, схема точек контроля, безналичный расчёт, работа в нерабочее время.
Оплата: наличные, перевод, безнал по счёту. Телефон и WhatsApp: ${PHONE}.

Правила ответа:
- Отвечай на языке клиента (русский или казахский), коротко: 2–4 предложения, без markdown, списков и эмодзи.
- Никогда не называй цены, сроки выезда, часы работы, сроки гарантии и названия препаратов — их нет в твоих данных. Про цену говори, что она зависит от площади, типа объекта и степени заражения и называется до выезда.
- Не придумывай факты, которых нет выше. Не давай медицинских рекомендаций; при укусах с сильной реакцией советуй обратиться к врачу.
- Про безопасность: на время обработки людям и животным нужно уйти, время возвращения называет специалист, после — проветривание и влажная уборка контактных поверхностей.
- Цель — помочь и получить заявку: уточни вредителя или задачу, тип объекта, площадь и город, затем попроси номер телефона или предложи нажать кнопку WhatsApp под чатом.
- Если вопрос не по теме компании, вежливо верни разговор к услугам.`;

const hits = new Map();
function limited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 25;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > max;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const raw = Array.isArray(body && body.messages) ? body.messages : [];
  const messages = raw.slice(-12)
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1000) }));
  // API требует чередование ролей и первый ход пользователя
  const clean = [];
  for (const m of messages) {
    if (!clean.length && m.role !== "user") continue;
    if (clean.length && clean[clean.length - 1].role === m.role) clean[clean.length - 1].content += "\n" + m.content;
    else clean.push(m);
  }
  if (!clean.length || clean[clean.length - 1].role !== "user") { res.status(400).json({ error: "bad_request" }); return; }

  const city = typeof body.city === "string" ? body.city.slice(0, 40) : "Алматы";
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: MODEL, max_tokens: 400, system: SYSTEM + `\nГород, выбранный посетителем на сайте: ${city}.`, messages: clean }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    const j = await r.json();
    const reply = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim();
    if (!reply) { res.status(502).json({ error: "empty" }); return; }
    const last = clean[clean.length - 1].content;
    res.status(200).json({ reply, wa: /(\+?7|8)[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}/.test(last) || /whatsapp|ватсап|номер/i.test(reply) });
  } catch (e) {
    res.status(502).json({ error: "fail" });
  }
};
