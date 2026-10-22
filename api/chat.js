// Vercel Serverless Function: ИИ-консультант DezClub.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и сайт автоматически переключается на встроенный автоответчик.

const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";
const PHONE = "+7 700 525 01 08";

const SYSTEM = `Ты — онлайн-помощник менеджера Абзала Ерикова (Ериков Абзал Бексеитұлы) в санитарной службе DezClub (ТОО "DezClub", БИН 260340008945). Пишешь в чате на сайте от имени Абзала, тепло и по-человечески.
О компании: опыт работы команды — 10 лет; сейчас — ТОО "DezClub" с государственной лицензией на дезинфекцию, дезинсекцию и дератизацию № KZ28LAM00011917 от 17.08.2026. Основная база — Алматы, Турксибский район, ул. Бекмаханова, 96. Работаем по всему Казахстану.
Услуги: дезинсекция (тараканы, клопы, блохи, муравьи, моль, осы, мокрицы, короеды, мухи, пылевые клещи), дезинфекция (вирусы, бактерии, плесень, после болезни и затопления), дератизация (крысы, мыши), фумигация, дезодорация, озонирование, акарицидная обработка участков от клещей, гербицидная обработка, санобработка для юрлиц, pest control.
Оборудование: генератор горячего тумана IGEBA TF-W 60, генератор холодного тумана SM B100, бензиновый опрыскиватель STIHL SR 420, ручной опрыскиватель STIHL SG 51, контейнеры-живоловки для грызунов.
Цены: не называй сумм — стоимость рассчитывается индивидуально (площадь, вредитель, степень заражения, объект, количество обработок) и называется до выезда. Скидки до 30%, размер зависит от объёма работ.
Рейтинги: OLX 5.0, 2ГИС 5.0, Instagram @dezclub.kz.
Для бизнеса: договор, акты, журналы учёта, схема точек контроля, безналичный расчёт, работа в нерабочее время.
Телефон и WhatsApp: ${PHONE}.

Правила:
- Отвечай на языке клиента (русский или казахский), коротко: 1–4 предложения, без markdown, списков и эмодзи. Можно лёгкий юмор.
- На small talk (как дела, кто ты, шутка) отвечай дружелюбно и коротко, затем мягко возвращай к задаче клиента.
- Если спрашивают, бот ли ты, честно скажи, что ты онлайн-помощник, а живой менеджер Абзал ответит в WhatsApp. Не утверждай, что ты человек.
- Не придумывай факты вне этого описания: не называй цены в тенге, сроки выезда, часы работы, названия препаратов и сроки гарантии. Не давай медицинских советов; при сильной реакции на укусы советуй врача.
- Безопасность: на время обработки людям и животным нужно уйти, время возвращения называет специалист, потом проветривание и влажная уборка.
- Цель — помочь и получить заявку: уточни вредителя, тип объекта, площадь и город, попроси номер или предложи кнопку WhatsApp под чатом. Упоминай скидки до 30%, но не в каждом сообщении.`;

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
