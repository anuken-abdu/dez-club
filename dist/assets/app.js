(function () {
  "use strict";
  var CITIES = [["almaty", "Алматы", "в Алматы", "/"], ["astana", "Астана", "в Астане", "/goroda/astana/"], ["shymkent", "Шымкент", "в Шымкенте", "/goroda/shymkent/"], ["karaganda", "Караганда", "в Караганде", "/goroda/karaganda/"], ["aktobe", "Актобе", "в Актобе", "/goroda/aktobe/"], ["taraz", "Тараз", "в Таразе", "/goroda/taraz/"], ["pavlodar", "Павлодар", "в Павлодаре", "/goroda/pavlodar/"], ["ust-kamenogorsk", "Усть-Каменогорск", "в Усть-Каменогорске", "/goroda/ust-kamenogorsk/"], ["semey", "Семей", "в Семее", "/goroda/semey/"], ["atyrau", "Атырау", "в Атырау", "/goroda/atyrau/"], ["kostanay", "Костанай", "в Костанае", "/goroda/kostanay/"], ["kyzylorda", "Кызылорда", "в Кызылорде", "/goroda/kyzylorda/"], ["uralsk", "Уральск", "в Уральске", "/goroda/uralsk/"], ["petropavlovsk", "Петропавловск", "в Петропавловске", "/goroda/petropavlovsk/"], ["aktau", "Актау", "в Актау", "/goroda/aktau/"], ["taldykorgan", "Талдыкорган", "в Талдыкоргане", "/goroda/taldykorgan/"], ["turkestan", "Туркестан", "в Туркестане", "/goroda/turkestan/"], ["kokshetau", "Кокшетау", "в Кокшетау", "/goroda/kokshetau/"], ["ekibastuz", "Экибастуз", "в Экибастузе", "/goroda/ekibastuz/"], ["temirtau", "Темиртау", "в Темиртау", "/goroda/temirtau/"], ["zhezkazgan", "Жезказган", "в Жезказгане", "/goroda/zhezkazgan/"], ["konaev", "Конаев", "в Конаеве", "/goroda/konaev/"], ["kaskelen", "Каскелен", "в Каскелене", "/goroda/kaskelen/"], ["talgar", "Талгар", "в Талгаре", "/goroda/talgar/"], ["esik", "Есик", "в Есике", "/goroda/esik/"], ["balkhash", "Балхаш", "в Балхаше", "/goroda/balkhash/"], ["zhanaozen", "Жанаозен", "в Жанаозене", "/goroda/zhanaozen/"], ["rudny", "Рудный", "в Рудном", "/goroda/rudny/"], ["satpaev", "Сатпаев", "в Сатпаеве", "/goroda/satpaev/"], ["ridder", "Риддер", "в Риддере", "/goroda/ridder/"], ["stepnogorsk", "Степногорск", "в Степногорске", "/goroda/stepnogorsk/"]];
  var SEARCH = [["Дезинфекция, дезинсекция, дератизация в Алматы — СЭС служба DezClub", "/", "главная сэс санэпидемстанция"], ["Дезинсекция в Алматы — заказать, цены по запросу", "/uslugi/dezinsekciya/", "уничтожение насекомых"], ["Дезинфекция в Алматы — заказать, цены по запросу", "/uslugi/dezinfekciya/", "уничтожение вирусов и бактерий"], ["Дератизация в Алматы — заказать, цены по запросу", "/uslugi/deratizaciya/", "уничтожение грызунов"], ["Фумигация в Алматы — заказать, цены по запросу", "/uslugi/fumigaciya/", "обработка газом"], ["Дезодорация в Алматы — заказать, цены по запросу", "/uslugi/dezodoraciya/", "уничтожение запахов"], ["Озонирование помещений в Алматы — заказать, цены по запросу", "/uslugi/ozonirovanie/", "уничтожение запахов, бактерий, вирусов, грибков"], ["Акарицидная обработка в Алматы — заказать, цены по запросу", "/uslugi/akaricidnaya-obrabotka/", "обработка территории от клещей"], ["Гербицидная обработка в Алматы — заказать, цены по запросу", "/uslugi/gerbicidnaya-obrabotka/", "уничтожение сорняков"], ["Санитарная обработка для юридических лиц в Алматы — заказать, цены по запросу", "/uslugi/yuridicheskim-licam/", "договор, акты, журналы для СЭС"], ["Pest Control — пест-контроль в Алматы — заказать, цены по запросу", "/uslugi/pest-control/", "системная защита объекта"], ["Услуги дезинфекции, дезинсекции и дератизации в Алматы", "/uslugi/", "услуги"], ["Уничтожение тараканов в Алматы — обработка с гарантией по договору", "/vrediteli/tarakany/", "тараканов"], ["Уничтожение клопов в Алматы — обработка с гарантией по договору", "/vrediteli/klopy/", "клопов"], ["Уничтожение пылевых клещей в Алматы — обработка с гарантией по договору", "/vrediteli/pylevye-kleshchi/", "пылевых клещей"], ["Уничтожение ос и осиных гнёзд в Алматы — обработка с гарантией по договору", "/vrediteli/osy/", "ос и осиных гнёзд"], ["Уничтожение мокриц в Алматы — обработка с гарантией по договору", "/vrediteli/mokricy/", "мокриц"], ["Уничтожение короедов в Алматы — обработка с гарантией по договору", "/vrediteli/koroedy/", "короедов"], ["Уничтожение блох в Алматы — обработка с гарантией по договору", "/vrediteli/blohi/", "блох"], ["Уничтожение мух в Алматы — обработка с гарантией по договору", "/vrediteli/muhi/", "мух"], ["Уничтожение муравьёв в Алматы — обработка с гарантией по договору", "/vrediteli/muravi/", "муравьёв"], ["Уничтожение моли в Алматы — обработка с гарантией по договору", "/vrediteli/mol/", "моли"], ["Уничтожение крыс в Алматы — обработка с гарантией по договору", "/vrediteli/krysy/", "крыс"], ["Уничтожение мышей в Алматы — обработка с гарантией по договору", "/vrediteli/myshi/", "мышей"], ["Уничтожение насекомых и грызунов в Алматы", "/vrediteli/", "вредители насекомые"], ["Обработка квартиры от тараканов, клопов, грызунов в Алматы", "/obekty/kvartiry/", "квартиры"], ["Обработка общежития от тараканов, клопов, грызунов в Алматы", "/obekty/obshchezhitiya/", "общежития"], ["Обработка кафе и ресторана от тараканов, клопов, грызунов в Алматы", "/obekty/kafe/", "кафе и ресторана"], ["Обработка склада от тараканов, клопов, грызунов в Алматы", "/obekty/sklady/", "склада"], ["Обработка гостиницы от тараканов, клопов, грызунов в Алматы", "/obekty/gostinicy/", "гостиницы"], ["Обработка офиса от тараканов, клопов, грызунов в Алматы", "/obekty/ofisy/", "офиса"], ["Обработка магазина от тараканов, клопов, грызунов в Алматы", "/obekty/magaziny/", "магазина"], ["Обработка бытовки от тараканов, клопов, грызунов в Алматы", "/obekty/bytovki/", "бытовки"], ["Обработка подвала от тараканов, клопов, грызунов в Алматы", "/obekty/podvaly/", "подвала"], ["Обработка частного дома от тараканов, клопов, грызунов в Алматы", "/obekty/doma/", "частного дома"], ["Обработка предприятия от тараканов, клопов, грызунов в Алматы", "/obekty/predpriyatiya/", "предприятия"], ["Обработка участка от тараканов, клопов, грызунов в Алматы", "/obekty/uchastki/", "участка"], ["Обработка квартир, кафе, складов, офисов в Алматы", "/obekty/", "объекты помещения"], ["Дезинфекция, дезинсекция, дератизация в Астане — СЭС служба", "/goroda/astana/", "Астана в Астане"], ["Дезинфекция, дезинсекция, дератизация в Шымкенте — СЭС служба", "/goroda/shymkent/", "Шымкент в Шымкенте"], ["Дезинфекция, дезинсекция, дератизация в Караганде — СЭС служба", "/goroda/karaganda/", "Караганда в Караганде"], ["Дезинфекция, дезинсекция, дератизация в Актобе — СЭС служба", "/goroda/aktobe/", "Актобе в Актобе"], ["Дезинфекция, дезинсекция, дератизация в Таразе — СЭС служба", "/goroda/taraz/", "Тараз в Таразе"], ["Дезинфекция, дезинсекция, дератизация в Павлодаре — СЭС служба", "/goroda/pavlodar/", "Павлодар в Павлодаре"], ["Дезинфекция, дезинсекция, дератизация в Усть-Каменогорске — СЭС служба", "/goroda/ust-kamenogorsk/", "Усть-Каменогорск в Усть-Каменогорске"], ["Дезинфекция, дезинсекция, дератизация в Семее — СЭС служба", "/goroda/semey/", "Семей в Семее"], ["Дезинфекция, дезинсекция, дератизация в Атырау — СЭС служба", "/goroda/atyrau/", "Атырау в Атырау"], ["Дезинфекция, дезинсекция, дератизация в Костанае — СЭС служба", "/goroda/kostanay/", "Костанай в Костанае"], ["Дезинфекция, дезинсекция, дератизация в Кызылорде — СЭС служба", "/goroda/kyzylorda/", "Кызылорда в Кызылорде"], ["Дезинфекция, дезинсекция, дератизация в Уральске — СЭС служба", "/goroda/uralsk/", "Уральск в Уральске"], ["Дезинфекция, дезинсекция, дератизация в Петропавловске — СЭС служба", "/goroda/petropavlovsk/", "Петропавловск в Петропавловске"], ["Дезинфекция, дезинсекция, дератизация в Актау — СЭС служба", "/goroda/aktau/", "Актау в Актау"], ["Дезинфекция, дезинсекция, дератизация в Талдыкоргане — СЭС служба", "/goroda/taldykorgan/", "Талдыкорган в Талдыкоргане"], ["Дезинфекция, дезинсекция, дератизация в Туркестане — СЭС служба", "/goroda/turkestan/", "Туркестан в Туркестане"], ["Дезинфекция, дезинсекция, дератизация в Кокшетау — СЭС служба", "/goroda/kokshetau/", "Кокшетау в Кокшетау"], ["Дезинфекция, дезинсекция, дератизация в Экибастузе — СЭС служба", "/goroda/ekibastuz/", "Экибастуз в Экибастузе"], ["Дезинфекция, дезинсекция, дератизация в Темиртау — СЭС служба", "/goroda/temirtau/", "Темиртау в Темиртау"], ["Дезинфекция, дезинсекция, дератизация в Жезказгане — СЭС служба", "/goroda/zhezkazgan/", "Жезказган в Жезказгане"], ["Дезинфекция, дезинсекция, дератизация в Конаеве — СЭС служба", "/goroda/konaev/", "Конаев в Конаеве"], ["Дезинфекция, дезинсекция, дератизация в Каскелене — СЭС служба", "/goroda/kaskelen/", "Каскелен в Каскелене"], ["Дезинфекция, дезинсекция, дератизация в Талгаре — СЭС служба", "/goroda/talgar/", "Талгар в Талгаре"], ["Дезинфекция, дезинсекция, дератизация в Есике — СЭС служба", "/goroda/esik/", "Есик в Есике"], ["Дезинфекция, дезинсекция, дератизация в Балхаше — СЭС служба", "/goroda/balkhash/", "Балхаш в Балхаше"], ["Дезинфекция, дезинсекция, дератизация в Жанаозене — СЭС служба", "/goroda/zhanaozen/", "Жанаозен в Жанаозене"], ["Дезинфекция, дезинсекция, дератизация в Рудном — СЭС служба", "/goroda/rudny/", "Рудный в Рудном"], ["Дезинфекция, дезинсекция, дератизация в Сатпаеве — СЭС служба", "/goroda/satpaev/", "Сатпаев в Сатпаеве"], ["Дезинфекция, дезинсекция, дератизация в Риддере — СЭС служба", "/goroda/ridder/", "Риддер в Риддере"], ["Дезинфекция, дезинсекция, дератизация в Степногорске — СЭС служба", "/goroda/stepnogorsk/", "Степногорск в Степногорске"], ["Дезинфекция и дератизация по всему Казахстану — города", "/goroda/", "города казахстан"], ["Как подготовить квартиру к обработке от насекомых", "/stati/kak-podgotovit-kvartiru-k-obrabotke/", "статья"], ["Что делать после обработки: проветривание, уборка и сроки", "/stati/chto-delat-posle-obrabotki/", "статья"], ["Какие документы по дезинфекции нужны бизнесу", "/stati/dokumenty-po-dezinfekcii-dlya-biznesa/", "статья"], ["Как понять, что в доме клопы: признаки и что делать", "/stati/kak-ponyat-chto-v-dome-klopy/", "статья"], ["Статьи о дезинсекции и дезинфекции", "/stati/", "статьи памятки"], ["Портфолио — видео наших работ", "/portfolio/", "портфолио видео работы"], ["Отзывы клиентов", "/otzyvy/", "отзывы"], ["Оплата и реквизиты ТОО DezClub", "/oplata/", "реквизиты оплата бин иик счет"], ["Контакты санитарной службы DezClub в Алматы", "/kontakty/", "контакты телефон адрес"], ["О компании ТОО DezClub — санитарная служба", "/o-kompanii/", "о компании"]];
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

  /* ================= ИИ-чат ================= */
  var chat = $("#chat"), chB = $("#chatB"), chQ = $("#chatQ"), chF = $("#chatF"), chI = $("#chatI"), chWa = $("#chatWa");
  var hist = [];
  try { hist = JSON.parse(store.sget("dz_chat") || "[]"); } catch (e) { hist = []; }
  var ctx = { pest: null, obj: null, askedContact: false };
  var busy = false;

  var KB = [
    { k: ["таракан", "прусак"], pest: "тараканы", a: "Тараканов уничтожаем препаратами длительного действия и гелевыми приманками: обрабатываем кухню, санузел, щели плинтусов, места у труб и за техникой. Препарат продолжает работать и после обработки, поэтому погибают и молодые особи из яиц.", u: "/vrediteli/tarakany/" },
    { k: ["клоп"], pest: "клопы", a: "От клопов обрабатываем спальные места, диваны, плинтусы, розетки и все щели рядом с кроватью — препаратами, которые действуют на взрослых и личинок. При сильном заражении назначаем контрольный осмотр. Мебель обычно выбрасывать не нужно.", u: "/vrediteli/klopy/" },
    { k: ["крыс", "мыш", "грызун"], pest: "грызуны", a: "Для крыс и мышей ставим закрытые приманочные станции, недоступные детям и животным, и ловушки, находим и подсказываем, какие ходы закрыть. Для бизнеса ведём схему точек и журнал.", u: "/uslugi/deratizaciya/" },
    { k: ["блох"], pest: "блохи", a: "Блох уничтожаем на полу, плинтусах, коврах, мягкой мебели и в местах отдыха животных — препарат действует и на личинок. Питомца нужно обработать у ветеринара в тот же период. Если блохи из подвала, лучше обработать и подвал.", u: "/vrediteli/blohi/" },
    { k: ["муравь", "муравей"], pest: "муравьи", a: "Муравьёв выводим приманками, которые они уносят в гнездо, — так погибает вся колония с маткой. Обрабатываем места выхода, щели и периметр дома, на участке — муравейники.", u: "/vrediteli/muravi/" },
    { k: ["клещ"], pest: "клещи", a: "Если речь об участке — проводим акарицидную обработку травы и кустарников, перед этим траву лучше скосить. Если о пылевых клещах в квартире — обрабатываем текстиль и мягкую мебель, можно дополнить озонированием.", u: "/uslugi/akaricidnaya-obrabotka/" },
    { k: [" ос ", " осы", " осин", " осам", "шершн", "осиное", "осиные"], pest: "осы", a: "Осиные гнёзда уничтожает специалист в защитной экипировке: обрабатывает гнездо, затем снимает и утилизирует его. Лучше всего вечером или рано утром.", u: "/vrediteli/osy/" },
    { k: ["моль", "моли"], pest: "моль", a: "Обрабатываем шкафы, гардеробные, ковры и кухонные шкафы. Подскажем, какие продукты выбросить и что постирать. Вещи выбрасывать не нужно.", u: "/vrediteli/mol/" },
    { k: ["мух", "комар", "мошк"], pest: "мухи", a: "Обрабатываем места выплода и посадки мух и комаров: подвалы, мусорные площадки, подсобные помещения, территорию. Для кафе и производств предлагаем обработку по графику.", u: "/vrediteli/muhi/" },
    { k: ["мокриц"], pest: "мокрицы", a: "Мокрицы приходят на сырость — обрабатываем ванную, трубы, подвал и периметр дома и подсказываем, что сделать с влажностью, чтобы они не вернулись.", u: "/vrediteli/mokricy/" },
    { k: ["короед", "древоточ", "жук"], pest: "короеды", a: "Деревянные конструкции обрабатываем препаратами глубокого проникновения, при сильном заражении — фумигацией. Деревья на участке обрабатываем отдельно.", u: "/vrediteli/koroedy/" },
    { k: ["вирус", "бактер", "дезинфекц", "ковид", "covid", "болел", "инфекц"], a: "Проводим дезинфекцию поверхностей и воздуха методом холодного тумана и влажной обработки — после болезни, перед открытием объекта или планово. Выдаём акт выполненных работ.", u: "/uslugi/dezinfekciya/" },
    { k: ["плесен", "грибок", "сырост", "затоп"], a: "При плесени и после затопления проводим дезинфекцию стен, углов, санузлов и подвалов, при необходимости — дезодорацию. Подскажем, как снизить влажность, чтобы грибок не вернулся.", u: "/uslugi/dezinfekciya/" },
    { k: ["запах", "вонь", "воня", "гарь", "пожар", "дезодор"], a: "Стойкие запахи (гарь, сырость, животные, табак) убираем дезодорацией — нейтрализаторами в виде тумана, которые расщепляют молекулы запаха, — и при необходимости озонированием.", u: "/uslugi/dezodoraciya/" },
    { k: ["озон"], a: "Озонирование уничтожает запахи, бактерии, вирусы, грибок и пылевых клещей без химических остатков. На время работы генератора в помещении не должно быть людей, животных и растений.", u: "/uslugi/ozonirovanie/" },
    { k: ["фумигац", "зерно", "контейнер", "поддон"], a: "Фумигацию газом проводим для складов, зерна, продукции, древесины и поддонов — она уничтожает насекомых на всех стадиях, включая яйца внутри продукции.", u: "/uslugi/fumigaciya/" },
    { k: ["сорняк", "гербицид", "трава"], a: "Гербицидную обработку проводим на участках и промышленных территориях — сплошную или избирательную, чтобы не повредить газон и культурные растения.", u: "/uslugi/gerbicidnaya-obrabotka/" },
    { k: ["сэс", "договор", "юрлиц", "юр лиц", "тоо", " ип ", "кафе", "ресторан", "магазин", "склад", "офис", "предприят", "проверк", "журнал", " акт", "акты", "бизнес", "pest", "пест"], a: "Для организаций работаем по договору: акты выполненных работ, журналы учёта, схема точек контроля, безналичный расчёт. Обработки проводим в нерабочее время. Можем заключить годовой договор с плановыми выездами.", u: "/uslugi/yuridicheskim-licam/" },
    { k: ["безнал", " счет", "счет на", "выставить", "реквизит", "оплат", " бин", "каспи", "kaspi", "наличн", "перевод"], a: "Оплата наличными, переводом или по безналичному расчёту на счёт ТОО «DezClub». Все реквизиты есть на странице «Оплата». Для счёта пришлите реквизиты вашей организации в WhatsApp.", u: "/oplata/" },
    { k: ["безопас", " дет", "малыш", "ребен", "ребён", "беремен", "кошк", "собак", "животн", "аллерг", "вредно", "опасно"], a: "Подбираем препараты, разрешённые в Казахстане, с учётом того, кто живёт в помещении. На время обработки людям и животным нужно уйти. Когда можно вернуться, специалист скажет в зависимости от препарата; после — проветривание и влажная уборка контактных поверхностей. Если в доме беременные, маленькие дети или аллергики, обязательно скажите об этом заранее.", u: "/stati/chto-delat-posle-obrabotki/" },
    { k: ["подготов", "что убрать", "перед обработ"], a: "Перед обработкой: уберите продукты и посуду в закрытые шкафы или холодильник, освободите доступ к плинтусам и местам за мебелью, при обработке от клопов снимите постельное бельё. Людям и животным нужно уйти на время работы.", u: "/stati/kak-podgotovit-kvartiru-k-obrabotke/" },
    { k: ["после обработ", "вернуть", "когда можно", "проветр", "мыть", "уборк"], a: "После возвращения проветрите помещение и протрите поверхности, которых касаются руки и продукты. Плинтусы, щели и места за мебелью не мойте в течение срока, который назовёт специалист, — там препарат продолжает работать.", u: "/stati/chto-delat-posle-obrabotki/" },
    { k: ["гарант"], a: "Гарантия и контрольный осмотр прописываются в договоре — условия зависят от вида обработки и объекта. Если вредители вернутся в гарантийный срок, приезжаем повторно по условиям договора.", u: null },
    { k: ["сколько длит", "долго", "сколько времени", "по времени"], a: "Обработка квартиры обычно занимает от часа до нескольких часов — зависит от площади и метода. Точное время скажем при расчёте.", u: null },
    { k: ["город", "астан", "шымкент", "караганд", "актоб", "атырау", "актау", "павлодар", "семей", "костанай", "тараз", "уральск", "кызылорд", "область", "выезж", "казахстан"], a: "Основная база — в Алматы, работаем по всему Казахстану. Напишите ваш город и адрес — согласуем выезд и стоимость.", u: "/goroda/" },
    { k: ["график", "выходн", "ночь", "ночью", "вечер", "суббот", "воскрес", "часы работ", "время работ"], a: "Время выезда согласуем при заявке; для бизнеса работаем вечером, ночью и в выходные, чтобы не останавливать работу.", u: null },
    { k: ["адрес", "где наход", "офис ваш", "приехать к вам"], a: "Мы находимся в Алматы: Турксибский район, ул. Бекмаханова, 96. Специалист сам приезжает к вам на объект.", u: "/kontakty/" }
  ];
  var PRICE = ["цен", "стоим", "сколько стоит", "почем", "почём", "прайс", "тенге", "₸", "дорого", "сколько будет"];
  var HELLO = ["здравств", "привет", "добрый", "салем", "сәлем", "салам", "hello", "hi"];
  var THANKS = ["спасибо", "рахмет", "благодар"];

  function has(t, arr) { for (var i = 0; i < arr.length; i++) if (t.indexOf(arr[i]) > -1) return true; return false; }
  var PHONE_RE = /(\+?7|8)[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}/;

  function local(text) {
    var t = " " + norm(text) + " ";
    var ph = text.match(PHONE_RE);
    if (ph) {
      return { a: "Спасибо! Чтобы заявка точно дошла до специалиста, нажмите кнопку ниже — откроется WhatsApp с вашим вопросом и номером. Если удобнее, позвоните: +7 700 525 01 08.", wa: true };
    }
    var hits = KB.filter(function (it) { return has(t, it.k); });
    var price = has(t, PRICE);
    if (hits.length) {
      var h = hits[0];
      if (h.pest) ctx.pest = h.pest;
      var a = h.a;
      if (price) a += "\n\nСтоимость зависит от площади и степени заражения — назовём её до выезда. Подскажите, какая площадь помещения и это квартира, дом или объект бизнеса?";
      else if (!ctx.askedContact) { a += "\n\nЧтобы рассчитать стоимость, напишите площадь и тип помещения, а также ваш номер — специалист свяжется с вами."; ctx.askedContact = true; }
      return { a: a, u: h.u };
    }
    if (price) return { a: "Стоимость зависит от вредителя, площади, типа объекта и степени заражения" + (ctx.pest ? " (" + ctx.pest + ")" : "") + ". Напишите эти данные и ваш номер — назовём точную цену до выезда. Быстрее всего — в WhatsApp.", wa: true };
    if (/\d+\s*(м2|м²|кв|квадрат|метр)/.test(t) || /(комнат|однушк|двушк|трешк|трёшк)/.test(t)) return { a: "Понял, спасибо. Оставьте номер телефона или нажмите кнопку WhatsApp — специалист рассчитает стоимость и согласует время выезда.", wa: true };
    if (has(t, HELLO) && t.length < 30) return { a: "Здравствуйте! Расскажите, что случилось: какие вредители или какая задача, и какой у вас объект — квартира, дом или бизнес?" };
    if (has(t, THANKS)) return { a: "Пожалуйста! Если появятся вопросы — пишите. Для заявки можно нажать «Продолжить в WhatsApp» внизу чата." };
    if (has(t, ["оператор", "человек", "менеджер", "специалист", "позвон", "перезвон", "живой"])) return { a: "Конечно. Оставьте номер телефона здесь или нажмите кнопку — откроется WhatsApp, и специалист ответит лично. Телефон: +7 700 525 01 08.", wa: true };
    return { a: "Хороший вопрос — точно ответит специалист. Опишите ситуацию подробнее или оставьте номер, а быстрее всего — напишите нам в WhatsApp.", wa: true };
  }

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function transcript() {
    var u = hist.filter(function (m) { return m.r === "u"; }).map(function (m) { return m.t; }).slice(-4);
    return "Здравствуйте! Пишу из онлайн-чата на сайте." + (u.length ? "\nМой вопрос: " + u.join(" / ") : "") + "\nГород: " + city[1] + ".";
  }
  function addMsg(r, t, extra, save) {
    var d = document.createElement("div");
    d.className = "msg " + (r === "u" ? "u" : r === "t" ? "t" : "b");
    d.innerHTML = esc(t);
    if (extra && extra.u && location.pathname !== extra.u) {
      d.innerHTML += '\n<a href="' + extra.u + '">Подробнее на сайте →</a>';
    }
    if (extra && extra.wa) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn btn-wa"; b.textContent = "Отправить заявку в WhatsApp";
      b.addEventListener("click", function () { openWa(transcript()); });
      d.appendChild(document.createElement("br")); d.appendChild(b);
    }
    chB.appendChild(d); chB.scrollTop = chB.scrollHeight;
    if (save !== false && r !== "t") { hist.push({ r: r, t: t, x: extra || null }); store.sset("dz_chat", JSON.stringify(hist.slice(-40))); }
    return d;
  }
  var QUICK = ["Тараканы", "Клопы", "Крысы и мыши", "Дезинфекция", "Для бизнеса и СЭС", "Сколько стоит?"];
  function quick(show) {
    chQ.innerHTML = "";
    if (!show) return;
    QUICK.forEach(function (q) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = q;
      b.addEventListener("click", function () { send(q); });
      chQ.appendChild(b);
    });
  }
  function greet() {
    addMsg("b", "Здравствуйте! Я онлайн-консультант DezClub. Подскажу по обработке от насекомых и грызунов, дезинфекции и документам для бизнеса. Что у вас случилось?");
  }
  function openChat() {
    closeDrw(); closeMega(); hideTip();
    chat.classList.add("on"); document.body.classList.add("chat-open");
    if (window.matchMedia("(max-width:1023px)").matches) lock(true);
    if (!chB.children.length) {
      if (hist.length) hist.forEach(function (m) { addMsg(m.r, m.t, m.x, false); }); else greet();
      quick(hist.filter(function (m) { return m.r === "u"; }).length === 0);
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
  function ai(text) {
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
    busy = true; quick(false);
    addMsg("u", text);
    var typing = addMsg("t", "Консультант печатает…", null, false);
    var fallback = local(text);
    ai(text).then(function (j) {
      typing.remove();
      addMsg("b", j.reply, { wa: !!j.wa || PHONE_RE.test(text) });
    }).catch(function () {
      setTimeout(function () { typing.remove(); addMsg("b", fallback.a, { u: fallback.u, wa: fallback.wa }); }, 500);
    }).then(function () { busy = false; chWa.href = waUrl(transcript()); });
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
    setTimeout(function () { if (!chat.classList.contains("on") && !document.querySelector(".mdl.on,.drw.on")) tip.classList.add("on"); }, 15000);
    $("[data-tip-x]", tip).addEventListener("click", function () { hideTip(); store.sset("dz_tip", "1"); });
  }

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
