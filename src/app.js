(function () {
  "use strict";
  var CITIES = /*__CITIES__*/[];
  var SEARCH = /*__SEARCH__*/[];
  var CFG = window.DZ || {};
  var WA = CFG.wa;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    sget: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    sset: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };
  function waUrl(text) { return "https://wa.me/" + WA + "?text=" + encodeURIComponent(text); }
  function openWa(text) {
    var u = waUrl(text);
    var w = null;
    try { w = window.open(u, "_blank"); } catch (e) {}
    if (w) { try { w.opener = null; } catch (e) {} } else location.href = u;
    track();
  }
  function track() {
    if (CFG.ads && CFG.adsLabel && typeof window.gtag === "function") {
      window.gtag("event", "conversion", { send_to: CFG.ads + "/" + CFG.adsLabel });
    }
  }
  var lockCount = 0;
  function lock(on) {
    lockCount = Math.max(0, lockCount + (on ? 1 : -1));
    document.documentElement.style.overflow = lockCount ? "hidden" : "";
  }

  /* ---------------- город ---------------- */
  function findCity(slug) { for (var i = 0; i < CITIES.length; i++) if (CITIES[i][0] === slug) return CITIES[i]; return CITIES[0]; }
  var body = document.body;
  var qCity = null;
  try { qCity = new URLSearchParams(location.search).get("city"); } catch (e) {}
  if (qCity && CITIES.some(function (c) { return c[0] === qCity; })) store.set("dz_city", qCity);
  var city = findCity(body.getAttribute("data-fixed") ? body.getAttribute("data-city") : (store.get("dz_city") || "almaty"));
  if (body.getAttribute("data-fixed")) store.set("dz_city", city[0]);

  function applyCity() {
    $$("[data-c]").forEach(function (el) { el.textContent = city[1]; });
    $$("[data-cin]").forEach(function (el) { el.textContent = city[2]; });
    $$("a[data-wa]").forEach(function (a) { a.href = waUrl(a.getAttribute("data-wa") + " Город: " + city[1] + "."); });
    $$("[data-city-sel]").forEach(function (s) { s.value = city[0]; });
    $$("[data-city-set]").forEach(function (b) { b.classList.toggle("cur", b.getAttribute("data-city-set") === city[0]); });
  }
  applyCity();

  /* ---------------- модальные окна ---------------- */
  var lastFocus = null;
  function openM(m) {
    if (!m) return;
    closeMega();
    lastFocus = document.activeElement;
    m.classList.add("on"); lock(true);
    var f = m.querySelector("input,button:not(.mdl-x)"); if (f) setTimeout(function () { f.focus(); }, 30);
  }
  function closeM(m) {
    if (!m || !m.classList.contains("on")) return;
    m.classList.remove("on"); lock(false);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  $$(".mdl").forEach(function (m) {
    m.addEventListener("click", function (e) { if (e.target === m || e.target.closest("[data-x]")) closeM(m); });
  });
  $$("[data-open]").forEach(function (b) { b.addEventListener("click", function () { closeDrw(); openM(document.getElementById(b.getAttribute("data-open"))); }); });

  var cityM = $("#cityM");
  $$("[data-city-open]").forEach(function (b) { b.addEventListener("click", function () { closeDrw(); openM(cityM); }); });
  var ctQ = $("#ctQ");
  if (ctQ) ctQ.addEventListener("input", function () {
    var q = ctQ.value.trim().toLowerCase();
    $$("[data-city-set]").forEach(function (b) { b.parentNode.style.display = !q || b.textContent.toLowerCase().indexOf(q) > -1 ? "" : "none"; });
  });
  $$("[data-city-set]").forEach(function (b) {
    b.addEventListener("click", function () {
      city = findCity(b.getAttribute("data-city-set"));
      store.set("dz_city", city[0]);
      closeM(cityM);
      var p = location.pathname;
      if (p === "/" || /^\/goroda\/[^/]+\/?$/.test(p)) { if (p !== city[3]) { location.href = city[3]; return; } }
      applyCity();
    });
  });
  $$("[data-city-sel]").forEach(function (s) {
    s.addEventListener("change", function () { city = findCity(s.value); store.set("dz_city", city[0]); applyCity(); });
  });

  /* ---------------- мега-меню ---------------- */
  var mega = $("#mega"), megaBtn = $("[data-mega]");
  function closeMega() { if (mega && mega.classList.contains("open")) { mega.classList.remove("open"); megaBtn.setAttribute("aria-expanded", "false"); } }
  if (mega && megaBtn) {
    megaBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var o = !mega.classList.contains("open");
      mega.classList.toggle("open", o); megaBtn.setAttribute("aria-expanded", o ? "true" : "false");
    });
    var lis = $$(".mega-l li", mega), pans = $$(".mega-p", mega);
    function act(i) {
      lis.forEach(function (l, k) { l.classList.toggle("on", k === i); });
      pans.forEach(function (p, k) { p.classList.toggle("on", k === i); });
    }
    lis.forEach(function (l, i) {
      l.addEventListener("mouseenter", function () { act(i); });
      l.querySelector("a").addEventListener("focus", function () { act(i); });
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".mega") && !e.target.closest("[data-mega]")) closeMega(); });
  }

  /* ---------------- поиск ---------------- */
  function norm(s) { return (s || "").toLowerCase().replace(/ё/g, "е"); }
  $$("[data-search]").forEach(function (inp) {
    var box = inp.parentNode.querySelector(".srch-r"), idx = -1;
    function render() {
      var q = norm(inp.value.trim());
      if (q.length < 2) { box.classList.remove("on"); box.innerHTML = ""; return; }
      var words = q.split(/\s+/);
      var res = SEARCH.filter(function (it) {
        var h = norm(it[0] + " " + it[2]);
        return words.every(function (w) { return h.indexOf(w.slice(0, Math.max(3, w.length - 2))) > -1; });
      }).slice(0, 8);
      idx = -1;
      box.innerHTML = res.length ? res.map(function (r) { return '<li><a href="' + r[1] + '">' + r[0].replace(/</g, "&lt;") + "</a></li>"; }).join("")
        : '<li class="no">Ничего не нашли. Спросите онлайн-консультанта.</li>';
      box.classList.add("on");
    }
    inp.addEventListener("input", render);
    inp.addEventListener("keydown", function (e) {
      var links = $$("a", box);
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); if (!links.length) return;
        idx = (idx + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
        links.forEach(function (l, i) { l.classList.toggle("act", i === idx); });
      } else if (e.key === "Enter") {
        e.preventDefault(); var l = links[idx > -1 ? idx : 0]; if (l) location.href = l.href;
      }
    });
    document.addEventListener("click", function (e) { if (!inp.parentNode.contains(e.target)) box.classList.remove("on"); });
  });

  /* ---------------- мобильное меню ---------------- */
  var drw = $("#drw");
  function closeDrw() { if (drw && drw.classList.contains("on")) { drw.classList.remove("on"); drw.setAttribute("aria-hidden", "true"); lock(false); } }
  $$("[data-drw]").forEach(function (b) { b.addEventListener("click", function () { drw.classList.add("on"); drw.setAttribute("aria-hidden", "false"); lock(true); }); });
  $$("[data-drw-x]").forEach(function (b) { b.addEventListener("click", closeDrw); });

  /* ---------------- прокрутка карточек ---------------- */
  $$("[data-scr]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = document.getElementById(b.getAttribute("data-scr")); if (!t) return;
      var c = t.firstElementChild; var w = c ? c.getBoundingClientRect().width + 20 : 300;
      t.scrollBy({ left: w * parseInt(b.getAttribute("data-d"), 10), behavior: "smooth" });
    });
  });

  /* ---------------- лайтбокс ---------------- */
  var lb = $("#lb"), lbM = lb ? $(".lb-m", lb) : null, group = [], gi = 0;
  function lbShow() {
    var it = group[gi]; if (!it) return;
    var src = it.getAttribute("data-src"), t = it.getAttribute("data-type");
    lbM.innerHTML = "";
    var el;
    if (t === "video") {
      el = document.createElement("video");
      el.src = src; el.controls = true; el.autoplay = true; el.playsInline = true; el.setAttribute("playsinline", "");
      var img = it.querySelector("img"); if (img) el.poster = img.currentSrc || img.src;
      el.onerror = function () { lbM.innerHTML = '<p style="color:#fff;text-align:center">Видео скоро появится.</p>'; };
    } else {
      el = document.createElement("img"); el.src = src; el.alt = it.getAttribute("aria-label") || "";
    }
    lbM.appendChild(el);
    var multi = group.length > 1;
    $(".p", lb).style.display = multi ? "" : "none"; $(".n", lb).style.display = multi ? "" : "none";
  }
  function lbOpen(it) {
    var g = it.getAttribute("data-lb");
    group = $$('[data-lb="' + g + '"]').filter(function (x) { return x.offsetParent !== null || x === it; });
    var seen = {}; group = group.filter(function (x) { var s = x.getAttribute("data-src"); if (seen[s]) return false; seen[s] = 1; return true; });
    gi = Math.max(0, group.map(function (x) { return x.getAttribute("data-src"); }).indexOf(it.getAttribute("data-src")));
    lb.classList.add("on"); lock(true); lbShow();
  }
  function lbClose() { if (!lb.classList.contains("on")) return; lb.classList.remove("on"); lbM.innerHTML = ""; lock(false); }
  function lbGo(d) { gi = (gi + d + group.length) % group.length; lbShow(); }
  if (lb) {
    document.addEventListener("click", function (e) { var it = e.target.closest("[data-lb]"); if (it) { e.preventDefault(); lbOpen(it); } });
    $(".x", lb).addEventListener("click", lbClose);
    $(".p", lb).addEventListener("click", function () { lbGo(-1); });
    $(".n", lb).addEventListener("click", function () { lbGo(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target === lbM) lbClose(); });
    var sx = 0;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50 && group.length > 1) lbGo(dx < 0 ? 1 : -1); });
  }

  /* ---------------- формы ---------------- */
  function fmtPhone(v) {
    var d = v.replace(/\D/g, "");
    if (d[0] === "8") d = "7" + d.slice(1);
    if (d && d[0] !== "7") d = "7" + d;
    d = d.slice(0, 11);
    var r = "+7";
    if (d.length > 1) r += " (" + d.slice(1, 4);
    if (d.length >= 4) r += ")";
    if (d.length > 4) r += " " + d.slice(4, 7);
    if (d.length > 7) r += "-" + d.slice(7, 9);
    if (d.length > 9) r += "-" + d.slice(9, 11);
    return r;
  }
  $$("[data-mask]").forEach(function (i) {
    i.addEventListener("focus", function () { if (!i.value) i.value = "+7 ("; });
    i.addEventListener("blur", function () { if (i.value.replace(/\D/g, "").length <= 1) i.value = ""; });
    i.addEventListener("input", function () { i.value = fmtPhone(i.value); });
  });
  $$("[data-wa-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true, parts = [f.getAttribute("data-wa-form")];
      var n = f.elements.name, p = f.elements.phone;
      [n, p].forEach(function (x) { if (x) x.classList.remove("err"); });
      if (n && n.value.trim().length < 2) { n.classList.add("err"); ok = false; }
      if (p && p.value.replace(/\D/g, "").length !== 11) { p.classList.add("err"); ok = false; }
      if (!ok) { (f.querySelector(".err") || {}).focus && f.querySelector(".err").focus(); return; }
      if (n) parts.push("Имя: " + n.value.trim());
      if (p) parts.push("Телефон: " + p.value.trim());
      if (f.elements.service) parts.push("Услуга: " + f.elements.service.value);
      var cs = f.elements.city ? findCity(f.elements.city.value)[1] : city[1];
      parts.push("Город: " + cs);
      if (f.elements.msg && f.elements.msg.value.trim()) parts.push("Комментарий: " + f.elements.msg.value.trim());
      openWa(parts.join("\n"));
      var m = f.closest(".mdl"); if (m) closeM(m);
      f.reset();
    });
  });
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="tel:"], a[href*="wa.me/"]');
    if (a && a.getAttribute("href").indexOf(CFG.wa) > -1) track();
    else if (a && a.getAttribute("href").indexOf("tel:") === 0) track();
  });
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-copy");
      function done() { var t = b.textContent; b.textContent = "скопировано"; setTimeout(function () { b.textContent = t; }, 1500); }
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(v).then(done, fallback); else fallback();
      function fallback() { var ta = document.createElement("textarea"); ta.value = v; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (er) {} ta.remove(); }
    });
  });

  /* ================= ИИ-чат: менеджер Абзал ================= */
  var chat = $("#chat"), chB = $("#chatB"), chQ = $("#chatQ"), chF = $("#chatF"), chI = $("#chatI"), chWa = $("#chatWa");
  var P = CFG.price || "от 4 990 ₸", PROMO = CFG.promo || "скидка 10% при заявке с сайта", MGR = CFG.manager || "Абзал";
  var AV = CFG.avatar || "";
  var hist = [];
  try { hist = JSON.parse(store.sget("dz_chat") || "[]"); } catch (e) { hist = []; }
  var ctx = { pest: null, askedContact: false, lastTopic: null };
  var busy = false;
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  var PRICE_LINE = "Цены " + P + ", точная сумма зависит от площади и степени заражения. Плюс действует " + PROMO + ".";

  var KB = [
    { k: ["таракан", "прусак"], pest: "тараканы", a: "Тараканов уничтожаем препаратами длительного действия и гелевыми приманками: кухня, санузел, щели плинтусов, места у труб и за техникой. Средство продолжает работать после обработки, поэтому погибают и молодые особи из яиц.", u: "/vrediteli/tarakany/", q: ["Сколько стоит?", "Как подготовиться?", "Это безопасно для детей?"] },
    { k: ["клоп"], pest: "клопы", a: "С клопами справимся. Обрабатываем кровати, диваны, плинтусы, розетки и все щели рядом со спальным местом — средствами, которые действуют и на взрослых, и на личинок. Мебель обычно выбрасывать не нужно.", u: "/vrediteli/klopy/", q: ["Сколько стоит?", "Нужно ли уходить из дома?", "Как подготовиться?"] },
    { k: ["крыс", "мыш", "грызун"], pest: "грызуны", a: "Для крыс и мышей ставим закрытые приманочные станции — дети и животные до них не доберутся — и ловушки. Находим, откуда приходят грызуны, и подсказываем, какие ходы закрыть. Для бизнеса ведём схему точек и журнал.", u: "/uslugi/deratizaciya/", q: ["Сколько стоит?", "Это безопасно для кошки?", "Нужен договор для СЭС"] },
    { k: ["блох"], pest: "блохи", a: "Блох уничтожаем на полу, плинтусах, коврах, мягкой мебели и в местах отдыха животных — средство действует и на личинок. Питомца нужно обработать у ветеринара в тот же период. Если блохи идут из подвала, лучше обработать и его.", u: "/vrediteli/blohi/", q: ["Сколько стоит?", "Как подготовиться?"] },
    { k: ["муравь", "муравей"], pest: "муравьи", a: "Муравьёв выводим приманками, которые они уносят в гнездо, — так погибает вся колония вместе с маткой. Обрабатываем места выхода, щели и периметр дома, на участке — муравейники.", u: "/vrediteli/muravi/", q: ["Сколько стоит?"] },
    { k: ["клещ"], pest: "клещи", a: "Если речь об участке — делаем акарицидную обработку травы и кустарников, траву перед этим лучше скосить. Если о пылевых клещах в квартире — обрабатываем текстиль и мягкую мебель, можно дополнить озонированием.", u: "/uslugi/akaricidnaya-obrabotka/", q: ["Сколько стоит?"] },
    { k: [" ос ", " осы", " осин", " осам", "шершн", "осиное", "осиные"], pest: "осы", a: "Осиные гнёзда убирает специалист в защитной экипировке: обрабатывает гнездо, потом снимает и утилизирует его. Лучше всего вечером или рано утром, когда осы внутри.", u: "/vrediteli/osy/", q: ["Сколько стоит?"] },
    { k: ["моль", "моли"], pest: "моль", a: "Обрабатываем шкафы, гардеробные, ковры и кухонные шкафы. Подскажем, какие продукты выбросить и что постирать. Вещи выбрасывать не нужно.", u: "/vrediteli/mol/", q: ["Сколько стоит?"] },
    { k: ["мух", "комар", "мошк"], pest: "мухи", a: "Обрабатываем места выплода и посадки мух и комаров: подвалы, мусорные площадки, подсобки, территорию. Для кафе и производств — обработка по графику.", u: "/vrediteli/muhi/", q: ["Сколько стоит?"] },
    { k: ["мокриц"], pest: "мокрицы", a: "Мокрицы приходят на сырость — обрабатываем ванную, трубы, подвал и периметр дома и подсказываем, что сделать с влажностью, чтобы они не вернулись.", u: "/vrediteli/mokricy/", q: ["Сколько стоит?"] },
    { k: ["короед", "древоточ", "жук"], pest: "короеды", a: "Деревянные конструкции обрабатываем средствами глубокого проникновения, при сильном заражении — фумигацией. Деревья на участке обрабатываем отдельно.", u: "/vrediteli/koroedy/", q: ["Сколько стоит?"] },
    { k: ["вирус", "бактер", "дезинфекц", "ковид", "covid", "болел", "инфекц"], a: "Дезинфекцию делаем холодным туманом и влажной обработкой поверхностей — после болезни, перед открытием объекта или планово. Выдаём акт выполненных работ.", u: "/uslugi/dezinfekciya/", q: ["Сколько стоит?", "Нужен договор для СЭС"] },
    { k: ["плесен", "грибок", "сырост", "затоп"], a: "При плесени и после затопления дезинфицируем стены, углы, санузлы и подвалы, при необходимости убираем запах. Подскажем, как снизить влажность, чтобы грибок не вернулся.", u: "/uslugi/dezinfekciya/", q: ["Сколько стоит?"] },
    { k: ["запах", "вонь", "воня", "гарь", "пожар", "дезодор"], a: "Стойкие запахи — гарь, сырость, животные, табак — убираем дезодорацией: нейтрализатор в виде тумана расщепляет молекулы запаха, а не маскирует его. При необходимости добавляем озонирование.", u: "/uslugi/dezodoraciya/", q: ["Сколько стоит?"] },
    { k: ["озон"], a: "Озонирование уничтожает запахи, бактерии, вирусы, грибок и пылевых клещей без химических остатков. Пока работает генератор, в помещении не должно быть людей, животных и растений.", u: "/uslugi/ozonirovanie/", q: ["Сколько стоит?"] },
    { k: ["фумигац", "зерно", "контейнер", "поддон"], a: "Фумигацию газом проводим для складов, зерна, продукции, древесины и поддонов — она уничтожает насекомых на всех стадиях, включая яйца внутри продукции.", u: "/uslugi/fumigaciya/", q: ["Сколько стоит?"] },
    { k: ["сорняк", "гербицид", "трава"], a: "Гербицидную обработку делаем на участках и промышленных территориях — сплошную или избирательную, чтобы не задеть газон и культурные растения.", u: "/uslugi/gerbicidnaya-obrabotka/", q: ["Сколько стоит?"] },
    { k: ["оборудован", "туман", "генератор", "опрыскив", "чем обрабат", "аппарат"], a: "Работаем профессиональным оборудованием: генератор горячего тумана, оборудование холодного тумана и ранцевый моторный опрыскиватель-воздуходувка для территорий. Туман проникает в щели и труднодоступные места, куда не достать обычным распылителем.", u: "/o-kompanii/#equip", q: ["Сколько стоит?"] },
    { k: ["сэс", "договор", "юрлиц", "юр лиц", "тоо", " ип ", "кафе", "ресторан", "магазин", "склад", "офис", "предприят", "проверк", "журнал", " акт", "акты", "бизнес", "pest", "пест"], a: "Для организаций работаем по договору: акты, журналы учёта, схема точек контроля, безналичный расчёт. Обрабатываем в нерабочее время, можно оформить годовой договор с плановыми выездами.", u: "/uslugi/yuridicheskim-licam/", q: ["Сколько стоит?", "Реквизиты для счёта"] },
    { k: ["безнал", " счет", "счёт", "счет на", "выставить", "реквизит", "оплат", " бин", "каспи", "kaspi", "наличн", "перевод"], a: "Оплата наличными, переводом или по безналичному расчёту на счёт ТОО «DezClub». Реквизиты есть на странице «Оплата», а для счёта пришлите реквизиты вашей организации в WhatsApp.", u: "/oplata/" },
    { k: ["безопас", " дет", "малыш", "ребен", "ребён", "беремен", "кошк", "собак", "животн", "аллерг", "вредно", "опасно"], a: "Используем средства, разрешённые в Казахстане, и подбираем их под тех, кто живёт в помещении. На время обработки людям и животным нужно уйти, когда можно вернуться — скажет специалист. Потом проветривание и влажная уборка контактных поверхностей. Если дома беременные, малыши или аллергики — обязательно предупредите заранее.", u: "/stati/chto-delat-posle-obrabotki/" },
    { k: ["подготов", "что убрать", "перед обработ"], a: "Перед обработкой: уберите продукты и посуду в шкафы или холодильник, освободите доступ к плинтусам и местам за мебелью, при обработке от клопов снимите постельное бельё. Людям и животным на время работы нужно уйти.", u: "/stati/kak-podgotovit-kvartiru-k-obrabotke/" },
    { k: ["после обработ", "вернуть", "когда можно", "проветр", "мыть", "уборк", "уходить из дома", "уходить из квартир"], a: "Да, на время обработки нужно уйти. После возвращения проветрите помещение и протрите поверхности, которых касаются руки и продукты. Плинтусы, щели и места за мебелью не мойте, пока не пройдёт срок, который назовёт специалист, — там средство продолжает работать.", u: "/stati/chto-delat-posle-obrabotki/" },
    { k: ["лиценз", "сертификат", "документы компании", "разрешени", "квалификац"], a: "Работаем официально: у ТОО «DezClub» государственная лицензия на дезинфекцию, дезинсекцию и дератизацию № KZ28LAM00011917 от 17.08.2026. У специалистов есть документы о квалификации, на препараты — свидетельства о регистрации. Всё можно посмотреть на сайте.", u: "/dokumenty/" },
    { k: ["рейтинг", "отзыв", "olx", "олх", "2гис", "2gis", "инстаграм", "instagram", "инста"], a: "Рейтинг 5.0 на OLX и 5.0 в 2ГИС, а фото и видео работ — в нашем Instagram @dezclub.kz. Скриншоты отзывов клиентов есть на сайте.", u: "/otzyvy/" },
    { k: ["с какого года", "сколько лет", "опыт", "давно работа", "давно на рынке", "2017"], a: "Команда DezClub работает с 2017 года. За это время обрабатывали квартиры, частные дома, кафе, склады, гостиницы и производства.", u: "/o-kompanii/" },
    { k: ["гарант"], a: "Гарантия и контрольный осмотр прописываются в договоре — условия зависят от вида обработки и объекта. Если вредители вернутся в гарантийный срок, приедем повторно по условиям договора.", u: null },
    { k: ["скидк", "акци", "промо", "дешевле", "подешевле"], a: "Сейчас действует " + PROMO + ": просто напишите, что нашли нас на сайте. Цены на все услуги " + P + ".", u: "/ceny/", q: ["Рассчитать мою стоимость"] },
    { k: ["сколько длит", "долго", "сколько времени", "по времени"], a: "Обработка квартиры обычно занимает от часа до нескольких часов — зависит от площади и метода. Точное время скажу при расчёте.", u: null },
    { k: ["срочно", "сегодня", "сейчас", "как быстро", "когда приед"], a: "Постараемся приехать как можно быстрее — время согласуем сразу при заявке. Оставьте номер или напишите в WhatsApp, и я сразу передам заявку специалисту.", wa: true },
    { k: ["город", "астан", "шымкент", "караганд", "актоб", "атырау", "актау", "павлодар", "семей", "костанай", "тараз", "уральск", "кызылорд", "область", "выезж", "казахстан"], a: "Основная база — в Алматы, работаем по всему Казахстану. Напишите город и адрес — согласуем выезд и стоимость.", u: "/goroda/" },
    { k: ["график", "выходн", "ночь", "ночью", "вечер", "суббот", "воскрес", "часы работ", "время работ", "во сколько"], a: "Время выезда согласуем при заявке, для бизнеса работаем вечером, ночью и в выходные, чтобы не останавливать работу.", u: null },
    { k: ["адрес", "где наход", "офис ваш", "приехать к вам"], a: "Мы в Алматы: Турксибский район, ул. Бекмаханова, 96. Но обычно ехать никуда не нужно — специалист сам приезжает на объект.", u: "/kontakty/" }
  ];
  var TALK = [
    { k: ["как дела", "как ты", "как жизнь", "как настроение", "как сам", "қалайсыз", "калайсыз", "как поживаешь"], a: ["Всё отлично, спасибо, что спросили! Работы много, тараканам в городе не позавидуешь. А у вас как — чем могу помочь?", "Хорошо, спасибо! День продуктивный. Рассказывайте, что у вас случилось — подскажу.", "Отлично! Только что помог одному клиенту с клопами. Чем помочь вам?"] },
    { k: ["кто ты", "ты кто", "как тебя зовут", "как вас зовут", "твое имя", "твоё имя", "с кем я"], a: ["Я онлайн-помощник менеджера " + MGR + " Ерикова из DezClub. Отвечаю сразу на вопросы по обработке, ценам и документам, а если нужно — подключится сам " + MGR + " в WhatsApp."] },
    { k: ["ты бот", "ты робот", "ты человек", "ты живой", "это бот", "нейросет", "искусственн", " ии ", "chatgpt", "гпт"], a: ["Честно: я онлайн-помощник, отвечаю автоматически, чтобы вам не ждать. Живой менеджер " + MGR + " Ериков ответит в WhatsApp — кнопка внизу чата."] },
    { k: ["спасибо", "рахмет", "благодар", "спс"], a: ["Пожалуйста! Обращайтесь, если что-то ещё понадобится.", "Всегда рад помочь! Если решите заказать — напомните, что вы с сайта, — будет скидка 10%.", "Не за что! Хорошего дня и чтобы никаких тараканов."] },
    { k: ["пока", "до свидания", "до встречи", "всего доброго", "хорошего дня", "сау бол"], a: ["До свидания! Если что — пишите, я на связи.", "Всего доброго! Будем рады помочь."] },
    { k: ["доброе утро"], a: ["Доброе утро! Чем могу помочь?"] },
    { k: ["добрый вечер"], a: ["Добрый вечер! Расскажите, что случилось — подскажу."] },
    { k: ["шутк", "анекдот", "пошути", "рассмеши"], a: ["Таракан приходит домой и говорит жене: «Всё, собирай вещи, к соседям вызвали DezClub». Так что можете спать спокойно :)", "Говорят, тараканы переживут что угодно. Мы просто не встречали тех тараканов, которые пережили бы нашу обработку :)"] },
    { k: ["погод"], a: ["Про погоду не подскажу, а вот про насекомых — сколько угодно :) Кстати, в тёплый сезон активнее муравьи, клещи и осы."] },
    { k: [" ок ", " окей", "понятно", "ясно", "хорошо", " понял", "поняла", "супер", "отлично", "класс"], a: ["Отлично! Если готовы — оставьте номер или нажмите «Продолжить в WhatsApp», и я передам заявку.", "Хорошо! Если появятся вопросы — пишите, я здесь."], wa: true },
    { k: ["дорого", "дороговато", "много денег"], a: ["Понимаю. Цены " + P + ", а ещё действует " + PROMO + ". Напишите площадь и что за вредители — посчитаю честно, без лишних услуг."] }
  ];
  var PRICE = ["цен", "стоим", "сколько стоит", "почем", "почём", "прайс", "тенге", "₸", "сколько будет", "рассчитать"];
  var HELLO = ["здравств", "привет", "добрый день", "салем", "сәлем", "салам", "hello", " hi ", "здраст", "ассалам", "салют"];

  function has(t, arr) { for (var i = 0; i < arr.length; i++) if (t.indexOf(arr[i]) > -1) return true; return false; }
  var PHONE_RE = /(\+?7|8)[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}/;

  function local(text) {
    var t = " " + norm(text).replace(/[!?.,;:()]/g, " ") + " ";
    var hello = has(t, HELLO);
    var pre = hello ? pick(["Здравствуйте! ", "Добрый день! ", "Здравствуйте, рад помочь! "]) : "";
    if (PHONE_RE.test(text)) return { a: "Спасибо, номер записал! Чтобы заявка точно дошла, нажмите кнопку ниже — откроется WhatsApp с вашим вопросом и номером. " + MGR + " свяжется с вами. Можно и позвонить: +7 700 525 01 08.", wa: true };
    var price = has(t, PRICE);
    var hits = KB.filter(function (it) { return has(t, it.k); });
    if (hits.length) {
      var h = hits[0];
      if (h.pest) ctx.pest = h.pest;
      var a = pre + h.a;
      if (price) a += "\n\n" + PRICE_LINE + " Подскажите площадь и тип помещения — квартира, дом или бизнес?";
      else if (!ctx.askedContact && !h.wa) { a += "\n\nЧтобы назвать точную цену, напишите площадь и тип помещения или оставьте номер."; ctx.askedContact = true; }
      return { a: a, u: h.u, q: h.q, wa: h.wa };
    }
    if (price) return { a: pre + PRICE_LINE + (ctx.pest ? " Для обработки (" + ctx.pest + ")" : "") + " Напишите площадь, тип объекта и что за вредители — назову точную цену до выезда.", u: "/ceny/", q: ["Квартира до 50 м²", "Частный дом", "Кафе / бизнес"] };
    if (/\d+\s*(м2|м²|кв|квадрат|метр)/.test(t) || has(t, ["комнат", "однушк", "двушк", "трешк", "трёшк", "квартира до", "частный дом", "бизнес"])) return { a: "Понял, спасибо! Оставьте номер или нажмите кнопку WhatsApp — специалист рассчитает стоимость с учётом скидки и согласует время.", wa: true };
    for (var i = 0; i < TALK.length; i++) if (has(t, TALK[i].k)) return { a: pre + pick(TALK[i].a), wa: TALK[i].wa };
    if (hello) return { a: pick(["Здравствуйте! Меня зовут " + MGR + ", я менеджер DezClub. Что у вас случилось — какие вредители или какая задача?", "Здравствуйте! Рад вас видеть. Расскажите, что беспокоит: насекомые, грызуны, дезинфекция?"]), q: ["Тараканы", "Клопы", "Крысы и мыши", "Сколько стоит?"] };
    if (has(t, ["оператор", "человек", "менеджер", "специалист", "позвон", "перезвон", "живой"])) return { a: "Конечно! Оставьте номер здесь или нажмите кнопку — откроется WhatsApp, и " + MGR + " ответит лично. Телефон: +7 700 525 01 08.", wa: true };
    if (has(t, [" мат ", "дурак", "идиот", "тупой"])) return { a: "Давайте спокойно — я здесь, чтобы помочь. Расскажите, что случилось?" };
    return { a: pick(["Хороший вопрос! Чтобы ответить точно, уточню у специалиста. Опишите ситуацию подробнее или оставьте номер — быстрее всего в WhatsApp.", "Тут лучше подскажет специалист. Напишите детали или нажмите кнопку WhatsApp — " + MGR + " ответит лично."]), wa: true };
  }

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function now() { var d = new Date(); return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2); }
  function transcript() {
    var u = hist.filter(function (m) { return m.r === "u"; }).map(function (m) { return m.t; }).slice(-4);
    return "Здравствуйте! Пишу из онлайн-чата на сайте (скидка с сайта)." + (u.length ? "\nМой вопрос: " + u.join(" / ") : "") + "\nГород: " + city[1] + ".";
  }
  function avatar() { var s = document.createElement("span"); s.className = "m-av"; if (AV) s.style.backgroundImage = "url(" + AV + ")"; return s; }
  function scrollEnd() { chB.scrollTop = chB.scrollHeight; }
  function decorate(bubble, extra) {
    if (extra && extra.u && location.pathname !== extra.u.split("#")[0]) {
      var a = document.createElement("a"); a.href = extra.u; a.className = "m-lnk"; a.textContent = "Подробнее на сайте →";
      bubble.appendChild(document.createElement("br")); bubble.appendChild(a);
    }
    if (extra && extra.wa) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn btn-wa"; b.textContent = "Отправить заявку в WhatsApp";
      b.addEventListener("click", function () { openWa(transcript()); });
      bubble.appendChild(document.createElement("br")); bubble.appendChild(b);
    }
  }
  function row(r, t, time) {
    var w = document.createElement("div"); w.className = "mrow " + r;
    if (r === "b") w.appendChild(avatar());
    var d = document.createElement("div"); d.className = "msg " + r;
    var txt = document.createElement("span"); txt.className = "m-t"; txt.textContent = t || "";
    d.appendChild(txt);
    var tm = document.createElement("small"); tm.className = "m-time"; tm.textContent = time || now();
    d.appendChild(tm);
    w.appendChild(d); chB.appendChild(w); scrollEnd();
    return { w: w, d: d, txt: txt };
  }
  function save(r, t, extra) { hist.push({ r: r, t: t, x: extra || null, tm: now() }); store.sset("dz_chat", JSON.stringify(hist.slice(-40))); }
  function addUser(t) { row("u", t); save("u", t); }
  function addStatic(m) { var o = row(m.r, m.t, m.tm); if (m.r === "b") decorate(o.d, m.x); }
  function typingRow() {
    var w = document.createElement("div"); w.className = "mrow b typing"; w.appendChild(avatar());
    var d = document.createElement("div"); d.className = "msg b"; d.innerHTML = '<span class="dots"><i></i><i></i><i></i></span>';
    w.appendChild(d); chB.appendChild(w); scrollEnd(); return w;
  }
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function botSay(text, extra, done) {
    var st = $("#chatSt"); if (st) st.textContent = "печатает…";
    var tw = typingRow();
    var think = Math.min(2200, 650 + text.length * 9);
    setTimeout(function () {
      tw.remove();
      var o = row("b", "");
      var words = text.split(/(\s+)/), i = 0;
      function step() {
        if (reduce) { o.txt.textContent = text; i = words.length; }
        else { o.txt.textContent += words.slice(i, i + 2).join(""); i += 2; }
        scrollEnd();
        if (i < words.length) setTimeout(step, 28);
        else { decorate(o.d, extra); scrollEnd(); save("b", text, extra); if (st) st.textContent = "онлайн"; done && done(); }
      }
      step();
    }, reduce ? 200 : think);
  }
  var QUICK = ["Тараканы", "Клопы", "Крысы и мыши", "Дезинфекция", "Сколько стоит?", "Есть скидки?"];
  function quick(list) {
    chQ.innerHTML = "";
    (list || []).forEach(function (q) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = q;
      b.addEventListener("click", function () { send(q); });
      chQ.appendChild(b);
    });
  }
  function greet() {
    var h = new Date().getHours();
    var hi = h < 5 ? "Доброй ночи" : h < 12 ? "Доброе утро" : h < 18 ? "Добрый день" : "Добрый вечер";
    botSay(hi + "! Меня зовут " + MGR + ", я менеджер DezClub. Подскажу по обработке от насекомых и грызунов, ценам и документам. Кстати, сейчас действует " + PROMO + ". Что у вас случилось?", null, function () { quick(QUICK); });
  }
  function openChat() {
    closeDrw(); closeMega(); hideTip();
    chat.classList.add("on"); document.body.classList.add("chat-open");
    if (window.matchMedia("(max-width:1023px)").matches) lock(true);
    if (!chB.children.length) {
      if (hist.length) { hist.forEach(addStatic); quick(hist.filter(function (m) { return m.r === "u"; }).length ? [] : QUICK); }
      else greet();
    }
    chWa.href = waUrl(transcript());
    setTimeout(function () { chI.focus(); }, 50);
    store.sset("dz_tip", "1");
  }
  function closeChat() {
    if (!chat.classList.contains("on")) return;
    chat.classList.remove("on"); document.body.classList.remove("chat-open");
    if (window.matchMedia("(max-width:1023px)").matches) lock(false);
  }
  function ai() {
    var msgs = hist.filter(function (m) { return m.r === "u" || m.r === "b"; }).slice(-12).map(function (m) { return { role: m.r === "u" ? "user" : "assistant", content: m.t }; });
    while (msgs.length && msgs[0].role !== "user") msgs.shift();
    var ctrl = window.AbortController ? new AbortController() : null;
    var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 12000);
    return fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: msgs, city: city[1], page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { clearTimeout(to); if (!r.ok) throw new Error("http"); return r.json(); })
      .then(function (j) { if (!j || !j.reply) throw new Error("empty"); return j; });
  }
  function send(text) {
    text = (text || "").trim();
    if (!text || busy) return;
    busy = true; quick([]);
    addUser(text);
    var fb = local(text);
    function finish() { busy = false; chWa.href = waUrl(transcript()); }
    ai().then(function (j) {
      botSay(j.reply, { wa: !!j.wa || PHONE_RE.test(text) }, finish);
    }).catch(function () {
      botSay(fb.a, { u: fb.u, wa: fb.wa }, function () { if (fb.q) quick(fb.q); finish(); });
    });
  }
  if (chat) {
    $$("[data-chat]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); openChat(); }); });
    $$("[data-chat-x]").forEach(function (b) { b.addEventListener("click", closeChat); });
    chF.addEventListener("submit", function (e) { e.preventDefault(); var v = chI.value; chI.value = ""; send(v); });
    chWa.addEventListener("click", function () { chWa.href = waUrl(transcript()); track(); });
  }
  var tip = $("#fabTip");
  function hideTip() { if (tip) tip.classList.remove("on"); }
  if (tip && !store.sget("dz_tip")) {
    setTimeout(function () { if (!chat.classList.contains("on") && !document.querySelector(".mdl.on,.drw.on") && !document.body.classList.contains("at-end")) tip.classList.add("on"); }, 12000);
    $("[data-tip-x]", tip).addEventListener("click", function (e) { e.stopPropagation(); hideTip(); store.sset("dz_tip", "1"); });
    tip.addEventListener("click", function () { openChat(); });
  }

  /* ---------------- наверх / назад / прозрачность у конца ---------------- */
  var bTop = $("[data-top]"), bBack = $("[data-back]");
  var inner = location.pathname !== "/";
  if (bBack) {
    bBack.hidden = !inner;
    bBack.addEventListener("click", function () {
      var ref = document.referrer, same = false;
      try { same = ref && new URL(ref).host === location.host; } catch (e) {}
      if (same && history.length > 1) { history.back(); return; }
      var cr = $$(".crumbs a"); location.href = cr.length ? cr[cr.length - 1].getAttribute("href") : "/";
    });
  }
  if (bTop) bTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  var ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (bTop) bTop.hidden = y < 500;
    var end = y + window.innerHeight >= document.documentElement.scrollHeight - 140;
    document.body.classList.toggle("at-end", end && y > 200);
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------------- тараканы в подвале ---------------- */
  (function () {
    var ftr = $(".ftr"), lay = ftr ? $(".roaches", ftr) : null;
    if (!lay || reduce || !window.requestAnimationFrame) return;
    var alive = [], visible = false, timer = null, kills = 0;
    var SAY = ["Попался!", "Минус один", "DezClub не дремлет", "Ещё один готов", "Чисто!"];
    function spawn() {
      if (!visible || alive.length >= 4 || document.hidden) return;
      var W = ftr.clientWidth, H = ftr.clientHeight;
      var el = document.createElement("div"); el.className = "roach";
      el.innerHTML = '<img src="/assets/ic/cockroach.svg" alt="">';
      lay.appendChild(el);
      var size = el.offsetWidth || 46;
      var dir = Math.random() < .5 ? 1 : -1;
      var r = { el: el, x: dir > 0 ? -size : W + size, y: 40 + Math.random() * Math.max(60, H - 120), vx: dir * (90 + Math.random() * 110), t: Math.random() * 6, amp: 18 + Math.random() * 30, dead: false, pause: 0 };
      el.addEventListener("click", function () { squash(r); });
      alive.push(r);
    }
    function squash(r) {
      if (r.dead) return; r.dead = true; kills++;
      r.el.classList.add("dead");
      var s = document.createElement("div"); s.className = "splat";
      s.textContent = kills > 1 ? pick(SAY) + " (" + kills + ")" : pick(SAY);
      s.style.left = r.x + "px"; s.style.top = (r.y - 26) + "px"; lay.appendChild(s);
      setTimeout(function () { s.remove(); }, 1400);
      setTimeout(function () { r.el.style.transition = "opacity .6s"; r.el.style.opacity = "0"; }, 700);
      setTimeout(function () { r.el.remove(); alive = alive.filter(function (x) { return x !== r; }); }, 1400);
    }
    var last = 0;
    function tick(ts) {
      var dt = last ? Math.min(.05, (ts - last) / 1000) : 0; last = ts;
      var W = ftr.clientWidth;
      alive.forEach(function (r) {
        if (r.dead) return;
        if (r.pause > 0) { r.pause -= dt; r.el.firstChild.style.animationPlayState = "paused"; }
        else {
          r.el.firstChild.style.animationPlayState = "running";
          r.t += dt * 2.2; r.x += r.vx * dt;
          if (Math.random() < .004) r.pause = .3 + Math.random() * .7;
        }
        var y = r.y + Math.sin(r.t) * r.amp, dy = Math.cos(r.t) * r.amp * 2.2;
        var ang = Math.atan2(dy, r.vx) * 180 / Math.PI + 90;
        r.el.style.transform = "translate(" + r.x + "px," + y + "px) rotate(" + ang + "deg)";
        if ((r.vx > 0 && r.x > W + 60) || (r.vx < 0 && r.x < -60)) { r.dead = true; r.el.remove(); }
      });
      alive = alive.filter(function (r) { return !r.dead || r.el.isConnected; });
      if (visible || alive.length) requestAnimationFrame(tick); else last = 0;
    }
    function loop() { spawn(); timer = setTimeout(loop, 1800 + Math.random() * 3200); }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        var v = es[0].isIntersecting;
        if (v && !visible) { visible = true; last = 0; requestAnimationFrame(tick); clearTimeout(timer); setTimeout(spawn, 400); loop(); }
        if (!v) { visible = false; clearTimeout(timer); }
      }, { threshold: .15 }).observe(ftr);
    }
  })();

  /* ---------------- Esc ---------------- */
  document.addEventListener("keydown", function (e) {
    if (lb && lb.classList.contains("on")) {
      if (e.key === "Escape") lbClose(); else if (e.key === "ArrowLeft") lbGo(-1); else if (e.key === "ArrowRight") lbGo(1);
      return;
    }
    if (e.key !== "Escape") return;
    var m = $(".mdl.on"); if (m) { closeM(m); return; }
    if (drw && drw.classList.contains("on")) { closeDrw(); return; }
    if (chat && chat.classList.contains("on")) { closeChat(); return; }
    closeMega();
  });
})();
