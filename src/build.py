# -*- coding: utf-8 -*-
"""Генератор статического сайта DezClub → ../dist"""
import json, os, shutil, html, datetime, re
from pathlib import Path
from urllib.parse import quote

from data import *
from icons import icon, ui

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
TODAY = datetime.date.today().isoformat()
YEAR = datetime.date.today().year
E = html.escape

SVC = {s["slug"]: s for s in SERVICES}
PEST = {p["slug"]: p for p in PESTS}
OBJ = {o[0]: o for o in OBJECTS}
CITY = {c[0]: c for c in CITIES}

def city_url(slug):
    return "/" if slug == "almaty" else f"/goroda/{slug}/"

def wa(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"

def wa_attr(text):
    """ссылка в WhatsApp: href для Алматы, JS подставит выбранный город"""
    return f'href="{wa(text + " Город: Алматы.")}" data-wa="{E(text)}" target="_blank" rel="noopener"'

PAGES = []          # для sitemap и поиска
SEARCH = []

# ------------------------------------------------------------------ части
LOGO_IMG = '<img class="logo-em" src="/assets/logo-mark.png" alt="" width="88" height="72">'

def logo(tag="a"):
    return f'''<a class="logo" href="/" aria-label="{BRAND} — на главную">{LOGO_IMG}<span class="logo-t"><span class="logo-n">DezClub</span><span class="logo-tag">{BRAND_TAG}</span></span></a>'''

def mega_groups(s):
    slug = s["slug"]
    objs_all = [(o[1], f"/obekty/{o[0]}/") for o in OBJECTS]
    def objs(*keys): return [(OBJ[k][1], f"/obekty/{k}/") for k in keys]
    def pests(*keys): return [(PEST[k]["name"], f"/vrediteli/{k}/") for k in keys]
    def svcs(*keys): return [(SVC[k]["name"], f"/uslugi/{k}/") for k in keys]
    v = f"/uslugi/{slug}/#vidy"
    G = {
        "dezinsekciya": [[("Уничтожение насекомых", pests(*[p["slug"] for p in PESTS if p["svc"] == "dezinsekciya"])),
                          ("По видам", [(k[0], v) for k in s["kinds"]])],
                         [("По помещениям", objs_all)]],
        "dezinfekciya": [[("Виды дезинфекции", [(k[0], v) for k in s["kinds"]]),
                          ("Вместе с дезинфекцией", svcs("ozonirovanie", "dezodoraciya"))],
                         [("По помещениям", objs_all)]],
        "deratizaciya": [[("Грызуны", pests("krysy", "myshi")), ("По видам", [(k[0], v) for k in s["kinds"]])],
                         [("По помещениям", objs("kvartiry", "doma", "podvaly", "sklady", "kafe", "magaziny", "predpriyatiya"))]],
        "fumigaciya": [[("Что обрабатываем", [(k[0], v) for k in s["kinds"]] + objs("sklady", "predpriyatiya")),
                        ("Вредители", pests("koroedy", "mol"))], []],
        "dezodoraciya": [[("Какие запахи", [(k[0], v) for k in s["kinds"]])],
                         [("Вместе с дезодорацией", svcs("ozonirovanie", "dezinfekciya"))]],
        "ozonirovanie": [[("Где применяем", [(k[0], v) for k in s["kinds"]] + objs("kvartiry", "ofisy", "gostinicy"))],
                         [("Против чего", pests("pylevye-kleshchi") + svcs("dezodoraciya", "dezinfekciya"))]],
        "akaricidnaya-obrabotka": [[("Территории", objs("uchastki", "doma")), ("По видам", [(k[0], v) for k in s["kinds"]])],
                                   [("Вместе с обработкой участка", svcs("gerbicidnaya-obrabotka") + pests("muravi", "osy"))]],
        "gerbicidnaya-obrabotka": [[("Территории", objs("uchastki", "doma", "predpriyatiya")), ("По видам", [(k[0], v) for k in s["kinds"]])],
                                   [("Вместе с гербицидной", svcs("akaricidnaya-obrabotka"))]],
        "yuridicheskim-licam": [[("Объекты", objs("kafe", "magaziny", "sklady", "ofisy", "gostinicy", "obshchezhitiya", "predpriyatiya"))],
                                [("Формат работы", [(k[0], v) for k in s["kinds"]] + [("Реквизиты и оплата", "/oplata/")])]],
        "pest-control": [[("Для кого", objs("predpriyatiya", "sklady", "kafe", "gostinicy", "magaziny"))],
                         [("Входит в систему", svcs("dezinsekciya", "deratizaciya", "dezinfekciya"))]],
    }
    return G[slug]

def mega():
    left, panels = [], []
    for i, s in enumerate(SERVICES):
        on = " on" if i == 0 else ""
        left.append(f'<li class="{on.strip()}" data-i="{i}"><a href="/uslugi/{s["slug"]}/">{icon(s["icon"])}<span class="t"><b>{s["name"]}</b><small>{s["sub"]}</small></span>{ui("right")}</a></li>')
        cols = []
        for col in mega_groups(s):
            gs = "".join(f'<div class="mega-g"><h4>{E(h)}</h4><ul>' + "".join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in items) + "</ul></div>" for h, items in col)
            cols.append(f"<div>{gs}</div>")
        desc = "" if s["slug"] == "dezinsekciya" else f'<p class="mega-desc">{E(s["lead"])}</p>'
        panels.append(f'<div class="mega-p{on}" data-p="{i}">{desc}<div class="mega-cols">{"".join(cols)}</div><a class="mega-more" href="/uslugi/{s["slug"]}/">Подробнее об услуге «{s["name"]}» {ui("arrow")}</a></div>')
    return f'''<div class="mega" id="mega"><div class="wrap"><div class="mega-in">
<ul class="mega-l">{"".join(left)}</ul>
<div class="mega-m">{"".join(panels)}</div>
<div class="mega-r">
  <div class="srch"><label class="sr" for="q1">Поиск по сайту</label><input id="q1" type="search" placeholder="Поиск по сайту" autocomplete="off" data-search>{ui("search")}<ul class="srch-r"></ul></div>
  <div class="promo"><div class="promo-v">{icon("s_pest")}<strong>{PROMO_BIG} на обработку</strong></div>
  <div class="promo-b"><h4>Опыт работы {EXPERIENCE}</h4><p>Менеджер {MANAGER[1]} подскажет, какая обработка нужна, и посчитает стоимость с учётом скидки.</p><button class="btn btn-o" type="button" data-chat>Спросить {MANAGER[1]}а</button></div></div>
</div></div></div></div>'''

def header():
    nav_company = [("О компании", "/o-kompanii/"), ("Лицензия и документы", "/dokumenty/"), ("Оплата и реквизиты", "/oplata/"), ("Портфолио", "/portfolio/"), ("Отзывы", "/otzyvy/"), ("Города", "/goroda/")]
    nav_pests = [(p["name"], f"/vrediteli/{p['slug']}/") for p in PESTS]
    nav_obj = [(o[1], f"/obekty/{o[0]}/") for o in OBJECTS]
    dd = lambda items: '<ul class="dd">' + "".join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in items) + "</ul>"
    return f'''<a class="skip" href="#main">К содержимому</a>
<header class="hdr">
 <div class="wrap hdr-top">
  {logo()}
  <div class="hdr-c">
   <button class="city-btn" type="button" data-city-open>{ui("pin")}<span data-c>Алматы</span></button>
   <a class="hdr-ph" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
   <span class="hdr-note">Звонки и WhatsApp</span>
  </div>
  <div class="hdr-geo"><span>Опыт работы {EXPERIENCE}</span><strong>{PROMO_BIG}</strong><span>По всему Казахстану</span></div>
  <div class="hdr-act">
   <a class="btn btn-wa" {wa_attr("Здравствуйте! Нужна консультация по обработке.")}>{ui("wa")}WhatsApp</a>
   <button class="btn btn-y" type="button" data-open="callback">Заказать звонок</button>
  </div>
  <div class="hdr-mob">
   <a class="m-ph" href="tel:{PHONE_TEL}" aria-label="Позвонить">{ui("phone")}</a>
   <button class="m-menu" type="button" data-drw aria-label="Меню">{ui("menu")}</button>
  </div>
 </div>
 <div class="hdr-city"><div class="wrap"><button class="city-btn" type="button" data-city-open>{ui("pin")}<span data-c>Алматы</span></button><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div></div>
 <nav class="nav" aria-label="Основное меню"><div class="wrap nav-in">
  <button class="nav-all" type="button" aria-expanded="false" aria-controls="mega" data-mega>Все услуги {ui("chev")}</button>
  <ul class="nav-l">
   <li><button type="button">О компании {ui("chev")}</button>{dd(nav_company)}</li>
   <li><button type="button">Вредители {ui("chev")}</button>{dd(nav_pests)}</li>
   <li><button type="button">Объекты {ui("chev")}</button>{dd(nav_obj)}</li>
   <li><a href="/portfolio/">Портфолио</a></li>
   <li><a href="/otzyvy/">Отзывы</a></li>
   <li><a href="/ceny/">Цены</a></li>
   <li><a href="/stati/">Статьи</a></li>
   <li><a href="/kontakty/">Контакты</a></li>
  </ul>
 </div>{mega()}</nav>
</header>'''

def drawer():
    svc = "".join(f'<li><a href="/uslugi/{s["slug"]}/">{icon(s["icon"])}{s["name"]}</a></li>' for s in SERVICES)
    pst = "".join(f'<li><a href="/vrediteli/{p["slug"]}/">{icon(p["icon"])}{p["name"]}</a></li>' for p in PESTS)
    obj = "".join(f'<li><a href="/obekty/{o[0]}/">{o[1]}</a></li>' for o in OBJECTS)
    sub = lambda t, items: f'<li><details><summary>{t} {ui("chev")}</summary><ul class="drw-sub">{items}</ul></details></li>'
    return f'''<div class="drw" id="drw" aria-hidden="true"><div class="drw-bg" data-drw-x></div>
<div class="drw-p" role="dialog" aria-modal="true" aria-label="Меню">
 <div class="drw-top">{logo()}<button class="mdl-x" type="button" data-drw-x aria-label="Закрыть">{ui("close")}</button></div>
 <button class="city-btn" type="button" data-city-open>{ui("pin")}Ваш город: <span data-c>Алматы</span></button>
 <div class="srch"><label class="sr" for="q2">Поиск по сайту</label><input id="q2" type="search" placeholder="Поиск по сайту" autocomplete="off" data-search>{ui("search")}<ul class="srch-r"></ul></div>
 <ul class="drw-l">
  {sub("Все услуги", svc)}{sub("Вредители", pst)}{sub("Объекты", obj)}
  <li><a href="/portfolio/">Портфолио</a></li><li><a href="/otzyvy/">Отзывы</a></li><li><a href="/o-kompanii/">О компании</a></li>
  <li><a href="/ceny/">Цены и скидки</a></li><li><a href="/dokumenty/">Лицензия и документы</a></li><li><a href="/oplata/">Оплата и реквизиты</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/goroda/">Города</a></li><li><a href="/kontakty/">Контакты</a></li>
 </ul>
 <div class="drw-ct"><a class="btn btn-c" href="tel:{PHONE_TEL}">{ui("phone")}{PHONE_DISPLAY}</a><button class="btn btn-o" type="button" data-chat>Онлайн-консультант</button></div>
</div></div>'''

def footer():
    svc = "".join(f'<li><a href="/uslugi/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    pst = "".join(f'<li><a href="/vrediteli/{p["slug"]}/">{p["name"]}</a></li>' for p in PESTS)
    obj = "".join(f'<li><a href="/obekty/{o[0]}/">{o[1]}</a></li>' for o in OBJECTS)
    return f'''<footer class="ftr"><div class="wrap">
 <div class="ftr-g">
  <div>{logo()}<p class="ftr-req">{BRAND_SUB.capitalize()}.<br>{E(COMPANY["legal"])}, БИН {COMPANY["bin"]}<br><a href="/dokumenty/">Лицензия № {LICENSE_NO} от {LICENSE_DATE}</a><br>{E(COMPANY["address"])}</p></div>
  <div class="f-col"><h4>Услуги {ui("chev")}</h4><ul>{svc}</ul></div>
  <div class="f-pst f-col"><h4>Вредители {ui("chev")}</h4><ul>{pst}</ul></div>
  <div class="f-obj f-col"><h4>Объекты {ui("chev")}</h4><ul>{obj}</ul></div>
  <div class="f-col f-ct"><h4>Контакты {ui("chev")}</h4>
   <a class="ftr-ph" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
   <ul><li><a {wa_attr("Здравствуйте! Нужна консультация.")}>Написать в WhatsApp</a></li>
   <li><a href="/kontakty/">Адрес и карта</a></li><li><a href="/ceny/">Цены и скидки</a></li><li><a href="/oplata/">Оплата и реквизиты</a></li><li><a href="/dokumenty/">Лицензия и документы</a></li><li><a href="/o-kompanii/">О компании</a></li><li><a href="/portfolio/">Портфолио</a></li><li><a href="/otzyvy/">Отзывы</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/goroda/">Города Казахстана</a></li></ul>
  </div>
 </div>
 <div class="ftr-soc">{social_html()}</div>
 <div class="ftr-b"><span>© {YEAR} {E(COMPANY["legal"])}. Дезинфекция, дезинсекция и дератизация по всему Казахстану.</span><a href="/privacy-policy/">Политика конфиденциальности</a></div>
</div></footer>'''

def svc_options():
    return "".join(f"<option>{s['name']}</option>" for s in SERVICES) + "<option>Другое</option>"

def city_options():
    return "".join(f'<option value="{c[0]}">{c[1]}</option>' for c in CITIES)

def overlays():
    cities = "".join(f'<li><button type="button" data-city-set="{c[0]}">{c[1]}</button></li>' for c in CITIES)
    return f'''
<div class="fnav"><button class="fnav-b" type="button" data-back aria-label="Назад">{ui("left")}</button><button class="fnav-b" type="button" data-top aria-label="Наверх">{ui("up")}</button></div>
<button class="fab" type="button" data-chat aria-label="Чат с менеджером"><span class="fab-i fab-av" style="background-image:url({MANAGER[2]}?v={MV})"><i class="on-dot"></i></span><span class="t"><b>{MANAGER[1]}, менеджер</b><small>Отвечу на вопросы сразу</small></span></button>
<div class="fab-tip" id="fabTip"><button type="button" aria-label="Скрыть" data-tip-x>{ui("close")}</button><span class="ft-av" style="background-image:url({MANAGER[2]}?v={MV})"></span><span><b>{MANAGER[1]}</b>Здравствуйте! Подскажу цену за минуту. Сейчас действуют скидки до 30%.</span></div>
<div class="mbar"><a class="btn btn-c" href="tel:{PHONE_TEL}">{ui("phone")}Позвонить</a><a class="btn btn-wa" {wa_attr("Здравствуйте! Нужна консультация по обработке.")}>{ui("wa")}WhatsApp</a></div>

<section class="chat" id="chat" aria-label="Онлайн-консультант" role="dialog">
 <div class="chat-h"><span class="fab-i fab-av" style="background-image:url({MANAGER[2]}?v={MV})"><i class="on-dot"></i></span><div><b>{MANAGER[1]} Ериков</b><small>менеджер {BRAND} · <span id="chatSt">онлайн</span></small></div><button class="chat-x" type="button" data-chat-x aria-label="Закрыть чат">{ui("close")}</button></div>
 <div class="chat-b" id="chatB" aria-live="polite"></div>
 <div class="qr" id="chatQ"></div>
 <form class="chat-f" id="chatF" autocomplete="off"><label class="sr" for="chatI">Сообщение</label><input id="chatI" maxlength="600" placeholder="Напишите вопрос…"><button type="submit" aria-label="Отправить">{ui("send")}</button></form>
 <a class="chat-wa" id="chatWa" href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener">{ui("wa")}Продолжить в WhatsApp</a>
</section>

<div class="mdl" id="callback" role="dialog" aria-modal="true" aria-labelledby="cbT"><div class="mdl-c">
 <button class="mdl-x" type="button" data-x aria-label="Закрыть">{ui("close")}</button>
 <h3 id="cbT">Заказать звонок</h3><p>Оставьте имя и номер — откроется WhatsApp с готовой заявкой, специалист перезвонит.</p>
 <form class="frm" data-wa-form="Здравствуйте! Прошу перезвонить."><div class="fld"><label for="cbN">Имя</label><input id="cbN" name="name" autocomplete="name" required></div>
 <div class="fld"><label for="cbP">Телефон</label><input id="cbP" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required data-mask></div>
 <button class="btn btn-y" type="submit">Отправить заявку</button><p class="frm-note">Нажимая кнопку, вы соглашаетесь с <a href="/privacy-policy/">политикой конфиденциальности</a>. Или позвоните: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p></form>
</div></div>

<div class="mdl mdl-city" id="cityM" role="dialog" aria-modal="true" aria-labelledby="ctT"><div class="mdl-c">
 <button class="mdl-x" type="button" data-x aria-label="Закрыть">{ui("close")}</button>
 <h3 id="ctT">Выберите ваш город</h3><p>Работаем по всему Казахстану. Основная база — в Алматы.</p>
 <div class="srch"><label class="sr" for="ctQ">Найти город</label><input id="ctQ" type="search" placeholder="Найти город" autocomplete="off">{ui("search")}</div>
 <ul class="city-g">{cities}</ul>
</div></div>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Просмотр"><button class="x" type="button" aria-label="Закрыть">{ui("close")}</button><button class="p" type="button" aria-label="Назад">{ui("left")}</button><div class="lb-m"></div><button class="n" type="button" aria-label="Вперёд">{ui("right")}</button></div>
{drawer()}'''

# ------------------------------------------------------------------ schema
def org_schema():
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE_URL + "/#org",
        "name": BRAND, "legalName": COMPANY["legal"].replace('"', ""), "taxID": COMPANY["bin"],
        "description": f"Санитарная служба: дезинфекция, дезинсекция, дератизация, фумигация, озонирование и pest control в Алматы и по всему Казахстану. Опыт работы {EXPERIENCE}, {PROMO_TXT}.",
        "currenciesAccepted": "KZT", "paymentAccepted": "Наличные, перевод, безналичный расчёт",
        "sameAs": [r[4] for r in RATINGS] + list(GIS_CITY.values()) + [v["url"] for v in VIDEOS],
        "url": SITE_URL + "/", "logo": SITE_URL + "/assets/logo.png", "image": SITE_URL + "/assets/og.png",
        "telephone": PHONE_TEL,
        "address": {"@type": "PostalAddress", "streetAddress": COMPANY["street"], "addressLocality": "Алматы",
                    "addressRegion": "Алматы", "addressCountry": "KZ"},
        "geo": {"@type": "GeoCoordinates", "latitude": COMPANY["lat"], "longitude": COMPANY["lng"]},
        "areaServed": [{"@type": "Country", "name": "Казахстан"}] + [{"@type": "City", "name": c[1]} for c in CITIES],
        "founder": {"@type": "Person", "name": COMPANY["director"], "jobTitle": "Генеральный директор"},
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                          "name": f"Лицензия на оказание услуг по дезинфекции, дезинсекции, дератизации № {LICENSE_NO} от {LICENSE_DATE}",
                          "url": SITE_URL + "/dokumenty/",
                          "recognizedBy": {"@type": "GovernmentOrganization", "name": LICENSE_BY}},
        "employee": [{"@type": "Person", "name": n, "jobTitle": r} for n, r in TEAM],
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "contactType": "customer service",
                         "availableLanguage": ["ru", "kk"], "areaServed": "KZ"},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{SITE_URL}/uslugi/{s['slug']}/"}} for s in SERVICES],
    }

def crumbs_schema(cr):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(cr)]}

def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def service_schema(name, url, desc, city="Казахстан"):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
            "description": desc, "url": SITE_URL + url, "provider": {"@id": SITE_URL + "/#org"},
            "areaServed": [{"@type": "City", "name": c[1]} for c in CITIES] if city == "Казахстан" else {"@type": "City", "name": city}}

# ------------------------------------------------------------------ страница
def page(path, title, desc, body, schemas=(), crumbs=None, city_fixed=None, kw="", prio="0.7"):
    url = path
    full = SITE_URL + url
    og_img = og_for(url, title)
    crumbs_html = ""
    sch = [org_schema()] + list(schemas)
    if crumbs:
        cr = [("Главная", "/")] + crumbs
        sch.append(crumbs_schema(cr))
        crumbs_html = '<nav aria-label="Навигация"><ol class="crumbs">' + "".join(
            (f'<li><a href="{u}">{E(n)}</a></li>' if i < len(cr) - 1 else f'<li aria-current="page">{E(n)}</li>') for i, (n, u) in enumerate(cr)) + "</ol></nav>"
        body = body.replace("<!--CRUMBS-->", crumbs_html)
    gtag = ""
    if GADS_ID:
        gtag = f'<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id={GADS_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GADS_ID}");gtag("config","{GA4_ID}");</script>'
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>' for s in sch)
    data_city = f' data-city="{city_fixed}" data-fixed="1"' if city_fixed else ""
    doc = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{full}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#4f9f2a">
<meta name="geo.region" content="KZ-75"><meta name="geo.placename" content="Алматы"><meta name="geo.position" content="{COMPANY["lat"]};{COMPANY["lng"]}"><meta name="ICBM" content="{COMPANY["lat"]}, {COMPANY["lng"]}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{full}"><meta property="og:image" content="{SITE_URL}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE_URL}{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/icon-192.png" sizes="192x192" type="image/png"><link rel="icon" href="/favicon.png" sizes="96x96" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"{BRAND}","alternateName":"ТОО DezClub","url":"{SITE_URL}/"}}</script>
<link rel="preload" href="/assets/fonts/montserrat-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/montserrat-cyrillic-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
{ld}{gtag}
</head>
<body{data_city}>
{header()}
<main id="main">
{body}
</main>
{footer()}
{overlays()}
<script>window.DZ={json.dumps({"wa": WA_NUMBER, "ads": GADS_ID, "adsLabel": GADS_CALL_LABEL, "adsLabelWa": GADS_WA_LABEL, "ga": GA4_ID, "price": "", "promo": PROMO_TXT, "exp": EXPERIENCE, "manager": MANAGER[1], "avatar": MANAGER[2] + "?v=" + MV}, ensure_ascii=False)};</script>
<script src="/assets/app.js?v={VER}" defer></script>
</body>
</html>'''
    out = DIST / url.strip("/") / "index.html" if url != "/404.html" else DIST / "404.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    if url != "/404.html":
        PAGES.append((url, prio))
        SEARCH.append([re.sub(r"\s*\|.*$", "", title), url, kw])

# ------------------------------------------------------------------ блоки
def btns_main(text="Здравствуйте! Хочу рассчитать стоимость обработки."):
    text = text.rstrip() + " Хочу узнать про скидку."
    return f'''<div class="btns"><a class="btn btn-y" {wa_attr(text)}>Рассчитать стоимость</a><button class="btn btn-o" type="button" data-chat>Задать вопрос онлайн</button></div>'''

def svc_grid(exclude=None, compact=False, limit=None):
    items = [s for s in SERVICES if s["slug"] != exclude]
    if limit: items = items[:limit]
    if compact:
        return '<div class="oth-g">' + "".join(f'<a class="oth" href="/uslugi/{s["slug"]}/">{icon(s["icon"])}<span>{s["name"]}</span></a>' for s in items) + "</div>"
    return '<div class="svc-g">' + "".join(f'<a class="svc" href="/uslugi/{s["slug"]}/">{icon(s["icon"])}<b>{s["name"]}</b><span>{s["sub"].capitalize()}</span></a>' for s in items) + "</div>"

def pest_grid(exclude=None, only=None):
    items = [p for p in PESTS if p["slug"] != exclude and (not only or p["slug"] in only)]
    return '<div class="pest-g">' + "".join(f'<a class="pest" href="/vrediteli/{p["slug"]}/">{icon(p["icon"])}<span>{p["name"]}</span></a>' for p in items) + "</div>"

def obj_grid(exclude=None):
    return '<div class="obj-g">' + "".join(f'<a class="obj" href="/obekty/{o[0]}/">{o[1]}{ui("right")}</a>' for o in OBJECTS if o[0] != exclude) + "</div>"

def sec(title, inner, sub="", link=None, alt=False, sid=""):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ui("arrow")}</a>' if link else ""
    sp = f"<p>{sub}</p>" if sub else ""
    i = f' id="{sid}"' if sid else ""
    return f'<section class="sec{" sec-alt" if alt else ""}"{i}><div class="wrap"><div class="sec-h"><div><h2>{title}</h2>{sp}</div>{lk}</div>{inner}</div></section>'

def steps_html():
    return '<ol class="steps">' + "".join(f"<li><b>{t}</b><p>{d}</p></li>" for t, d in STEPS) + "</ol>"

def adv_html():
    return '<div class="adv-g">' + "".join(f'<div class="adv">{icon(i)}<div><b>{t}</b><p>{d}</p></div></div>' for i, t, d in ADVANTAGES) + "</div>"

def biz_html():
    docs = ["Договор на дезинфекционные услуги", "Акт выполненных работ", "Журналы учёта обработок", "Схема точек контроля",
            "Безналичный расчёт по счёту", "Работа в нерабочее время"]
    li = "".join(f"<li>{ui('check')}{d}</li>" for d in docs)
    return f'''<section class="sec"><div class="wrap"><div class="biz">
<div><h2>Для бизнеса: всё для санитарной проверки</h2><p>Кафе, магазины, склады, гостиницы, офисы и производства обслуживаем по договору. Документы готовим сами, обработку проводим так, чтобы не останавливать работу.</p>
<div class="btns"><a class="btn btn-y" {wa_attr("Здравствуйте! Нужен договор на обработку для организации.")}>Запросить договор</a><a class="btn btn-o" href="/uslugi/yuridicheskim-licam/" style="background:transparent;color:#fff;border-color:#fff">Подробнее</a></div></div>
<ul>{li}</ul></div></div></section>'''

def poster(v):
    return v["cover"] or f"https://i.ytimg.com/vi/{yt_id(v['url'])}/hqdefault.jpg"

def video_cards(n=None):
    out = []
    for v in (VIDEOS[:n] if n else VIDEOS):
        t, vid = v["title"], yt_id(v["url"])
        out.append(f'<button class="vid" type="button" data-lb="v" data-type="yt" data-src="{vid}" data-url="https://www.youtube.com/shorts/{vid}" title="{E(t)}" aria-label="Смотреть видео: {E(t)}"><img src="{poster(v)}" alt="{E(t)}" loading="lazy" width="480" height="360"><span class="pl">{ui("play")}</span><span class="cap">{E(t)}</span></button>')
    return out

def review_cards():
    return [f'<button class="rev" type="button" data-lb="r" data-type="img" data-src="/images/reviews/review-{i}.webp?v={MV}" aria-label="Открыть отзыв {i}"><img src="/images/reviews/review-{i}.webp?v={MV}" alt="Отзыв клиента {BRAND} №{i}" loading="lazy" width="510" height="800"></button>' for i in range(1, REVIEWS_COUNT + 1)]

def scroller(cards, sid):
    return f'<div class="scr"><div class="scr-t" id="{sid}">{"".join(cards)}</div></div>'

def scr_nav(sid):
    return f'<div class="scr-nav"><button type="button" data-scr="{sid}" data-d="-1" aria-label="Назад">{ui("left")}</button><button type="button" data-scr="{sid}" data-d="1" aria-label="Вперёд">{ui("right")}</button></div>'

def sec_scroll(title, cards, sid, link, sub="", alt=False):
    return f'<section class="sec{" sec-alt" if alt else ""}"><div class="wrap"><div class="sec-h"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div><div style="display:flex;gap:18px;align-items:center">{scr_nav(sid)}<a class="lnk" href="{link[1]}">{link[0]} {ui("arrow")}</a></div></div>{scroller(cards, sid)}</div></section>'

def portfolio_sec(alt=False):
    return sec_scroll("Наши работы", video_cards(), "scrV", ("Всё портфолио", "/portfolio/"), "Короткие видео с реальных объектов: как проходит обработка.", alt)

def reviews_sec(alt=False):
    return sec_scroll("Отзывы клиентов", review_cards(), "scrR", ("Все отзывы", "/otzyvy/"), "Скриншоты сообщений от клиентов — без редактирования.", alt)

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}</summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in faq) + "</div>"

def lead_form(title="Рассчитаем стоимость обработки", text="Оставьте заявку — откроется WhatsApp с вашими данными. Уточним детали и назовём цену до выезда.", svc=None, city="almaty"):
    opts = svc_options()
    if svc:
        opts = opts.replace(f"<option>{svc}</option>", f"<option selected>{svc}</option>")
    copts = city_options().replace(f'value="{city}"', f'value="{city}" selected')
    return f'''<section class="sec"><div class="wrap"><div class="lead">
<div><h2>{title}</h2><p>{text}</p><p>Телефон: <a href="tel:{PHONE_TEL}"><b>{PHONE_DISPLAY}</b></a></p></div>
<form class="frm" data-wa-form="Здравствуйте! Заявка с сайта.">
 <div class="fld"><label for="lfN">Имя</label><input id="lfN" name="name" autocomplete="name" required></div>
 <div class="fld"><label for="lfP">Телефон</label><input id="lfP" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required data-mask></div>
 <div class="fld"><label for="lfS">Услуга</label><select id="lfS" name="service">{opts}</select></div>
 <div class="fld"><label for="lfC">Город</label><select id="lfC" name="city" data-city-sel>{copts}</select></div>
 <div class="fld full"><label for="lfM">Что случилось (необязательно)</label><textarea id="lfM" name="msg" rows="3" placeholder="Например: тараканы на кухне, квартира 60 м²"></textarea></div>
 <div class="full"><button class="btn btn-y" type="submit">Получить расчёт в WhatsApp</button></div>
 <p class="frm-note full">Нажимая кнопку, вы соглашаетесь с <a href="/privacy-policy/">политикой конфиденциальности</a>.</p>
</form></div></div></section>'''

def geo_sec(cur="almaty"):
    distr = "".join(f'<li class="ch">{d} район</li>' for d in ALMATY_DISTRICTS)
    cities = "".join(f'<li><a href="{city_url(c[0])}"{" class=cur" if c[0]==cur else ""}>{c[1]}</a></li>' for c in CITIES)
    return sec("География работы", f'''<div class="geo">
<div><h3>Районы Алматы</h3><p>Выезжаем во все районы города, в пригороды и посёлки Алматинской области.</p><ul class="chips m-clip" id="geoD">{distr}</ul><button class="m-more" type="button" data-more="geoD">Показать все районы {ui("chev")}</button></div>
<div><h3>Города Казахстана</h3><p>Работаем по всему Казахстану. Выберите город, чтобы узнать условия выезда.</p><ul class="chips m-clip" id="geoC">{cities}</ul><button class="m-more" type="button" data-more="geoC">Показать все города {ui("chev")}</button></div></div>''', alt=True)

def hero_art():
    return f'''<div class="hero-art"><img class="hero-ph" src="/images/hero.png?v={MV}" alt="{BRAND} — санитарная служба" width="914" height="1000" fetchpriority="high">
<div class="art-card art-k3">{icon("doc", eager=True)}<span>Договор и акт выполненных работ<small>для квартир, домов и бизнеса</small></span></div></div>'''

FACTS = [f"Опыт работы — {EXPERIENCE}",
         f"Государственная лицензия № {LICENSE_NO} от {LICENSE_DATE}",
         f"{PROMO_BIG.capitalize()} — размер зависит от объёма работ и объекта",
         "Оборудование: генератор горячего тумана IGEBA TF-W 60, генератор холодного тумана SM B100, опрыскиватели STIHL SR 420 и SG 51, живоловки для грызунов",
         "Рейтинг 5.0 на OLX и 5.0 в 2ГИС",
         f"Менеджер — {MANAGER[0]}",
         "Основная база в Алматы, выезд по всему Казахстану",
         "Договор, акт выполненных работ, документы для СЭС"]

def stars():
    return '<span class="stars" aria-hidden="true">★★★★★</span>'

def rate_html(city=None):
    out = []
    for slug, name, val, label, url in RATINGS:
        if slug == "2gis" and city and city != "almaty":
            url = GIS_CITY.get(city)
        ic = f'/assets/ic/{slug}.' + ("svg" if slug == "instagram" else "png")
        mid = f'<b class="rt-v">{E(val)}</b>{stars()}' if val[0].isdigit() else f'<b class="rt-v rt-h">{E(val)}</b>'
        inner = f'<img src="{ic}" alt="{name}" width="56" height="56" loading="lazy"><span class="rt-t"><span class="rt-m">{mid}</span><small>{E(label)}</small></span>{ui("arrow")}'
        out.append(f'<a class="rt" href="{url}" target="_blank" rel="noopener">{inner}</a>' if url else f'<div class="rt rt-off">{inner}</div>')
    return '<div class="rt-g">' + "".join(out) + "</div>"

def rate_sec(alt=False, city=None):
    return f'<section class="sec sec-rt{" sec-alt" if alt else ""}"><div class="wrap">{rate_html(city)}</div></section>'

def social_html():
    return "".join(f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}"><img src="/assets/ic/{slug}.{"svg" if slug == "instagram" else "png"}" alt="{name}" width="40" height="40" loading="lazy"></a>' for slug, name, val, label, url in RATINGS)

def price_of(slug):
    return MAIN_PRICES.get(slug) if SHOW_PRICES else None

def promo_sec():
    return f'''<section class="sec sec-promo"><div class="wrap"><div class="promo-bn">
<div class="pb-l"><span class="pb-k">Акция</span><h2>{PROMO_BIG} на обработку</h2><p>{PROMO_HOW} Точную стоимость называем до выезда — без доплат на месте.</p></div>
<div class="pb-r"><div class="pb-price"><small>Скидки</small><b>до 30%</b></div>
<a class="btn btn-y" {wa_attr("Здравствуйте! Хочу узнать стоимость и скидку на обработку.")}>Узнать свою скидку</a><a class="pb-lnk" href="/ceny/">Цены {ui("arrow")}</a></div>
</div></div></section>'''

def offer_box(what, slug=None):
    pr = price_of(slug) if slug else None
    left = f'<div class="of-p"><small>Стоимость</small><b>{pr}</b></div>' if pr else '<div class="of-p"><small>Скидки</small><b>до 30%</b></div>'
    return f'''<div class="offer">{left}
<ul class="of-l"><li>{ui("check")}<span><b>Скидки до 30%</b> — назовём при расчёте</span></li><li>{ui("check")}<span>Цена известна до выезда, без доплат на месте</span></li><li>{ui("check")}<span>Договор и акт выполненных работ</span></li></ul>
<a class="btn btn-y btn-sm" {wa_attr("Здравствуйте! Интересует " + what + ". Подскажите стоимость и скидку.")}>Узнать цену со скидкой</a></div>'''

def equip_sec(alt=False):
    cards = "".join(f'<div class="eq"><div class="eq-im"><img src="/images/equip/{k}.webp?v={MV}" alt="{E(t)}" loading="lazy"></div><b>{E(t)}</b><p>{E(d)}</p></div>' for k, t, d in EQUIPMENT)
    photo = f'<div class="eq eq-ph"><img src="/images/equip/worker.webp?v={MV}" alt="Специалист {BRAND} за работой" loading="lazy"></div>'
    return f'''<section class="sec{" sec-alt" if alt else ""}" id="equip"><div class="wrap"><div class="sec-h"><div><h2>Оборудование</h2><p>Профессиональная техника для квартир, бизнеса и территорий. Опыт работы — {EXPERIENCE}.</p></div></div>
<div class="eq-g m-scroll">{cards}{photo}</div></div></section>'''

def ru_count(n):
    w = "вид" if n % 10 == 1 and n % 100 != 11 else "вида" if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else "видов"
    return f"{n} {w} услуг"

def main_svc_html():
    out = []
    for slug, text, pts in MAIN_SERVICES:
        sv = SVC[slug]; pr = price_of(slug); n = len(CATALOG[slug][2])
        prh = f'<span class="ms-pr">{pr}</span>' if pr else '<span class="ms-pr ms-pr-s">Скидки до 30%</span>'
        out.append(f'''<a class="ms ms-k" href="/uslugi/{slug}/"><span class="ms-im"><img class="ms-ic" src="/assets/ic/{sv["icon"]}.svg" alt="" width="96" height="96" loading="lazy"><img class="ms-ph" src="/images/kategorii/{slug}.jpg?v={MV}" alt="{E(sv["name"])}" loading="lazy" onerror="this.remove()"></span>
<span class="ms-h"><span><b>{sv["name"]}</b><small>{ru_count(n)}</small></span></span>
<p>{E(text)}</p><span class="ms-f">{prh}<span class="ms-go">Подробнее {ui("arrow")}</span></span></a>''')
    return '<div class="ms-g">' + "".join(out) + "</div>"

def kat_card(slug, name, ic, link, price, btn="Заказать"):
    title = f'<a href="{link}">{E(name)}</a>' if link else E(name)
    return f'''<article class="kc"><div class="kc-im"><img class="kc-ic" src="/assets/ic/{ic}.svg" alt="" width="88" height="88" loading="lazy"><img class="kc-ph" src="/images/katalog/{slug}.jpg?v={MV}" alt="{E(name)}" loading="lazy" onerror="this.remove()"></div>
<div class="kc-b"><h3>{title}</h3><span class="kc-pr">{price}</span><a class="btn btn-y kc-btn" {wa_attr("Здравствуйте! Хочу заказать: " + name + ".")}>{btn}</a></div></article>'''
def svc_list_sec(alt=False):
    """Список всех услуг с кнопками «Заказать услугу» — карточки каталога, сгруппированные по категориям."""
    out = ""
    for cat, (name, price, items) in CATALOG.items():
        cards = "".join(kat_card(s, n, ic, ln, price, "Заказать услугу") for s, n, ic, ln in items)
        out += f'<h3 class="sl-t"><a href="/uslugi/{cat}/">{name}</a><small>{ru_count(len(items))}</small></h3><div class="kc-g sl-g">{cards}</div>'
    return sec("Список услуг", out, "Нажмите «Заказать услугу» — откроется WhatsApp с названием услуги. Стоимость с учётом площади и скидки назовём до выезда.", alt=alt)

def catalog_sec(cat, alt=False):
    name, price, items = CATALOG[cat]
    cards = "".join(kat_card(s, n, ic, ln, price) for s, n, ic, ln in items)
    return f'''<section class="sec{" sec-alt" if alt else ""}" id="katalog"><div class="wrap"><div class="sec-h"><div><h2>{name}: {ru_count(len(items))}</h2><p>Нажмите «Заказать» — откроется WhatsApp с названием услуги. Точную стоимость с учётом площади и скидки назовём до выезда.</p></div></div>
<div class="kc-g">{cards}</div></div></section>'''

def price_list_sec(alt=False):
    det = ""
    for cat, (name, price, items) in CATALOG.items():
        rows = "".join(f'<li><span>{E(n)}</span><b>{price}</b></li>' for _, n, _, _ in items)
        det += f'''<details class="pl"><summary><span class="pl-t">{name}</span><span class="pl-n">{ru_count(len(items))} · {price}</span>{ui("chev")}</summary><ul>{rows}</ul>
<div class="pl-f"><a class="lnk" href="/uslugi/{cat}/#katalog">Каталог с фото {ui("arrow")}</a></div></details>'''
    return sec("Стоимость услуг", f'<div class="pl-g">{det}</div><p class="pl-note">Указана начальная стоимость. Итог зависит от площади, степени заражения и объекта — называем его до выезда, без доплат на месте. {PROMO_BIG.capitalize()}.</p>', "", alt=alt)

def partners_sec(alt=False):
    logos = "".join(f'<li class="pt"><img src="/images/partners/{s}.webp?v={MV}" alt="{E(n)} — логотип организации" loading="lazy"></li>' for s, n in PARTNERS)
    join = f'''<li><a class="pt pt-join" {wa_attr(PARTNER_WA)}><svg class="pt-hs" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l8-8 9 3 5-3 6 1 12 8"/><path d="M4 20l7 9 3-1 4 4 3-1 4 4 4-1 3 2 4-4 6-6"/><path d="M21 15l-6 7c-1 2 1 4 3 3l6-5 5 4"/><path d="M24 4v4M15 6l2 3M33 6l-2 3"/></g></svg>
<span><b>Стать нашим партнёром</b><small>Обсудим обслуживание вашего объекта</small></span>{ui("arrow")}</a></li>'''
    adv = [("shield", "Договорное обслуживание", "Понятные условия и системная работа"),
           ("s_biz", "Разные отрасли", "Медицина, торговля, производство и HoReCa"),
           ("check", "Ответственный подход", "Контроль качества и соблюдение согласованных процедур")]
    advh = "".join(f'<li>{icon(i, 44)}<span><b>{t}</b><small>{d}</small></span></li>' for i, t, d in adv)
    return f'''<section class="sec sec-pt{" sec-alt" if alt else ""}" id="partnery"><div class="wrap">
<div class="pt-h"><h2>Нам доверяют</h2><p>Сотрудничаем с организациями на договорной основе, обеспечивая профессиональное санитарное обслуживание и системный контроль качества.</p></div>
<ul class="pt-g">{logos}{join}</ul><ul class="pt-a">{advh}</ul></div></section>'''

def svc_group_sec():
    main = {m[0] for m in MAIN_SERVICES}
    other = [s for s in SERVICES if s["slug"] not in main]
    oth = '<div class="oth-g m-scroll">' + "".join(f'<a class="oth" href="/uslugi/{s["slug"]}/">{icon(s["icon"])}<span>{s["name"]}</span></a>' for s in other) + "</div>"
    return f'''<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>Основные услуги</h2><p>Нажмите на услугу, чтобы узнать подробности, виды обработки и как подготовиться.</p></div><a class="lnk" href="/uslugi/">Все услуги {ui("arrow")}</a></div>
{main_svc_html()}<h3 class="oth-t">Другие услуги</h3>{oth}</div></section>'''

def trust_html():
    lic = f'<li><a href="/dokumenty/"><img src="/assets/ic/b-lic.svg" alt="" width="64" height="64"><span>Лицензия № {LICENSE_NO}</span></a></li>'
    return '<ul class="trust">' + lic + "".join(f'<li><img src="/assets/ic/{b}.svg" alt="" width="64" height="64"><span>{t}</span></li>' for b, t in TRUST) + "</ul>"

def doc_card(slug, title, sub):
    return (f'<button class="doc" type="button" data-lb="d" data-type="img" data-src="/images/docs/{slug}.webp?v={MV}" aria-label="Открыть: {E(title)}">'
            f'<span class="doc-im"><img src="/images/docs/{slug}-s.webp?v={MV}" alt="{E(title)}" loading="lazy" width="560" height="560"></span>'
            f'<b>{E(title)}</b><small>{E(sub)}</small></button>')

def docs_sec(alt=False):
    cards = [doc_card(*d) for _, items in DOCS for d in items]
    return sec_scroll("Лицензия и документы", cards, "scrD", ("Все документы", "/dokumenty/"),
                      f"Государственная лицензия № {LICENSE_NO} от {LICENSE_DATE}, документы специалистов и свидетельства на препараты.", alt)

def initials(n):
    p = n.split()
    return (p[1][0] + p[0][0]) if len(p) > 1 else p[0][0]

def team_html():
    cards = "".join(f'''<li class="tm"><div class="tm-ph"><span>{initials(n)}</span><img src="/images/team/team-{i}.webp?v={MV}" alt="{E(n)} — {E(r)}" width="914" height="1000" loading="lazy" style="object-position:50% 20%" onerror="this.remove()"></div><b>{E(n)}</b><small>{E(r)}</small></li>''' for i, (n, r) in enumerate(TEAM, 1))
    return f'<ul class="team">{cards}</ul>'

def team_sec(alt=False):
    return sec("Наша команда", team_html(), "Специалисты, которые отвечают за качество каждой обработки.", alt=alt, sid="team")

def hero_city(h1, lead, ic, btn_text, city=None):
    """Первый экран городской страницы: тот же блок, что на главной (фото руководителя и карточка «Договор и акт»), с городским заголовком."""
    return f'''<section class="hero hero-c"><div class="wrap"><!--CRUMBS--></div><div class="wrap hero-in"><div>
<h1>{h1}</h1><p class="hero-lead">{lead}</p>{btns_main(btn_text)}{trust_html()}</div>{hero_art()}</div></section>{rate_sec(city=city)}'''

def ph(h1, lead, ic, btn_text):
    return f'''<section class="ph"><div class="wrap"><!--CRUMBS--></div><div class="wrap ph-in"><div><h1>{h1}</h1><p class="lead-t">{lead}</p>{btns_main(btn_text)}{trust_html()}</div><div class="ph-ic">{icon(ic)}</div></div></section>{rate_sec()}'''

def side_box(svc_name, cur_url=None, list_items=None, list_title="Все услуги"):
    if list_items is None:
        list_items = [(s["name"], f"/uslugi/{s['slug']}/", s["icon"]) for s in SERVICES]
    li = "".join(f'<li><a href="{u}"{" class=cur" if u==cur_url else ""}>{icon(i) if i else ""}{n}</a></li>' for n, u, i in list_items)
    return f'''<aside class="side">
<div class="box"><h3>Узнать стоимость</h3><p>Назовём цену до выезда — нужна площадь, тип объекта и вредитель.</p>
<a class="box-ph" href="tel:{PHONE_TEL}">{ui("phone")}{PHONE_DISPLAY}</a>
<a class="btn btn-wa" {wa_attr(f"Здравствуйте! Интересует: {svc_name}.")}>{ui("wa")}Написать в WhatsApp</a>
<button class="btn btn-o" type="button" data-chat>Спросить онлайн</button></div>
<div class="box"><h3>{list_title}</h3><ul class="side-l">{li}</ul></div></aside>'''

def ck(items):
    return '<ul class="ck">' + "".join(f"<li>{ui('check')}<span>{x}</span></li>" for x in items) + "</ul>"

PREP = ["Уберите продукты, посуду и корм для животных в закрытые шкафы или холодильник",
        "Освободите доступ к плинтусам и местам за мебелью",
        "На время обработки людям и животным нужно покинуть помещение",
        "После возвращения проветрите помещение и протрите контактные поверхности"]

# ------------------------------------------------------------------ страницы
def build_home():
    body = f'''<section class="hero"><div class="wrap hero-in"><div>
<h1>Санитарная служба дезинсекции, дезинфекции, дератизации и пест‑контроля <span data-cin>в Алматы</span></h1>
<p class="hero-lead">Избавляем дома, бизнес и производства от насекомых, грызунов, бактерий и запахов. <b>Подбираем метод под объект</b> — квартиру с детьми, кафе, склад или участок, — работаем <b>по договору</b> и выдаём акт выполненных работ.</p>
{btns_main()}
{trust_html()}
</div>{hero_art()}</div></section>
{rate_sec()}
{svc_group_sec()}
{price_list_sec(alt=True)}
{promo_sec()}
{sec("От кого избавляем", pest_grid(), "Определяем вид вредителя и подбираем средство, которое действует именно на него.", ("Все вредители", "/vrediteli/"), alt=True)}
{sec("Как мы работаем", steps_html())}
{equip_sec(alt=True)}
{portfolio_sec()}
{sec("Почему выбирают " + BRAND, adv_html(), alt=True)}
{team_sec()}
{docs_sec(alt=True)}
{biz_html()}
{partners_sec()}
{sec("Обрабатываем любые объекты", obj_grid(), "", ("Все объекты", "/obekty/"), alt=True)}
{reviews_sec()}
{sec("Частые вопросы", faq_html(FAQ_HOME), alt=True)}
{geo_sec()}
{lead_form()}'''
    page("/", f"Дезинфекция, дезинсекция, дератизация в Алматы — СЭС служба {BRAND}",
         "Санитарная служба DezClub в Алматы и по всему Казахстану: уничтожение тараканов, клопов, грызунов, дезинфекция, озонирование, pest control. Договор и акт для СЭС.",
         body, [faq_schema(FAQ_HOME)], kw="главная сэс санэпидемстанция", prio="1.0")


def build_services():
    for s in SERVICES:
        url = f"/uslugi/{s['slug']}/"
        rel_pests = [p["slug"] for p in PESTS if p["svc"] == s["slug"]]
        kinds = '<div class="kinds">' + "".join(f'<div class="kind"><b>{k}</b><p>{d}</p></div>' for k, d in s["kinds"]) + "</div>"
        pest_block = f'<h2>От каких вредителей</h2>{pest_grid(only=rel_pests)}' if rel_pests else ""
        faq = [(f"Сколько стоит {s['name'].lower()}?", "Стоимость зависит от площади, типа объекта и задачи. Опишите ситуацию в WhatsApp или онлайн-консультанту — назовём цену до выезда."),
               ("Сколько длится обработка?", "Обычно от часа до нескольких часов в зависимости от площади и метода. Точное время скажем при расчёте."),
               ("Вы выдаёте документы?", "Да. После обработки выдаём акт выполненных работ, для организаций — договор, журналы и схемы точек контроля."),
               ("Вы работаете в других городах?", "Да, основная база в Алматы, выезжаем по всему Казахстану. Выберите город в шапке сайта.")]
        body = f'''{ph(f'{s["title"]} <span data-cin>в Алматы</span>', s["lead"], s["icon"], f"Здравствуйте! Интересует {s['name'].lower()}.")}
{catalog_sec(s["slug"]) if s["slug"] in CATALOG else ""}
<section class="sec"><div class="wrap cnt"><article class="prose">
<h2>Как проходит {s["name"].lower()}</h2>{offer_box(s["name"].lower(), s["slug"])}{"".join(f"<p>{p}</p>" for p in s["body"])}
<h2 id="vidy">Виды обработки</h2>{kinds}
{pest_block}
<h2>Этапы работы</h2>{ck([f"<b>{t}.</b> {d}" for t, d in STEPS])}
<h2>Как подготовиться</h2>{ck(PREP)}
<p>Подробнее — в статье <a href="/stati/kak-podgotovit-kvartiru-k-obrabotke/">как подготовить квартиру к обработке</a>.</p>
</article>{side_box(s["name"], url)}</div></section>
{price_list_sec(alt=True)}
{partners_sec()}
{portfolio_sec(alt=True)}
{sec("Частые вопросы", faq_html(faq))}
{sec("Другие услуги", svc_grid(exclude=s["slug"], compact=True, limit=8), alt=True)}
{lead_form(svc=s["name"])}'''
        page(url, SVC_TITLE[s["slug"]] + f" | {BRAND}",
             f"{s['title']} в Алматы и по Казахстану от {BRAND}: {s['sub']}. {s['lead'][:90].rstrip(' ,.')}… Договор и акт.",
             body, [service_schema(s["title"], url, s["lead"]), faq_schema(faq)],
             crumbs=[("Услуги", "/uslugi/"), (s["name"], url)], kw=s["sub"], prio="0.9")
    body = f'''{ph("Услуги санитарной службы", "Дезинсекция, дезинфекция, дератизация, фумигация, озонирование и комплексный pest control для квартир, домов, бизнеса и территорий.", "s_pest", "Здравствуйте! Подскажите, какая обработка мне нужна.")}
{svc_group_sec()}{price_list_sec(alt=True)}{biz_html()}{partners_sec()}{lead_form()}'''
    page("/uslugi/", f"Услуги дезинфекции, дезинсекции и дератизации в Алматы | {BRAND}",
         "Все услуги DezClub: дезинсекция, дезинфекция, дератизация, фумигация, дезодорация, озонирование, акарицидная и гербицидная обработка, pest control.",
         body, crumbs=[("Услуги", "/uslugi/")], kw="услуги", prio="0.8")

SVC_TITLE = {
    "dezinsekciya": "Дезинсекция в Алматы — обработка от насекомых",
    "dezinfekciya": "Дезинфекция в Алматы — от вирусов, бактерий и плесени",
    "deratizaciya": "Дератизация в Алматы — уничтожение крыс и мышей",
    "fumigaciya": "Фумигация в Алматы — обработка складов и продукции",
    "dezodoraciya": "Дезодорация в Алматы — удаление запахов",
    "ozonirovanie": "Озонирование помещений в Алматы — запахи и бактерии",
    "akaricidnaya-obrabotka": "Акарицидная обработка в Алматы — участки от клещей",
    "gerbicidnaya-obrabotka": "Гербицидная обработка в Алматы — уничтожение сорняков",
    "yuridicheskim-licam": "Санобработка для юрлиц в Алматы — документы для СЭС",
    "pest-control": "Пест-контроль (pest control) в Алматы для предприятий",
}
GEN_PL = {"тараканы": "тараканов", "клопы": "клопов", "муравьи": "муравьёв", "моль": "моли", "блохи": "блох", "мухи": "мух",
          "грызуны": "грызунов", "крысы": "крыс", "мыши": "мышей", "жуки": "жуков", "вирусы и бактерии": "вирусов",
          "осы": "ос", "клещи": "клещей", "комары": "комаров", "мокрицы": "мокриц", "насекомые": "насекомых", "птицы": "птиц", "сорняки": "сорняков"}

def build_pests():
    for p in PESTS:
        url = f"/vrediteli/{p['slug']}/"
        s = SVC[p["svc"]]
        faq = p["faq"] + [(f"Сколько стоит уничтожение {p['gen']}?", "Цена зависит от площади, типа объекта и степени заражения. Напишите в WhatsApp — назовём стоимость до выезда."),
                          ("Нужно ли уходить из дома?", "Да, на время обработки людям и животным нужно покинуть помещение. Когда можно вернуться, специалист скажет в зависимости от препарата.")]
        rel_obj = [o for o in OBJECTS if p["name"].lower().split()[0][:5] in " ".join(o[4])]
        if not rel_obj: rel_obj = OBJECTS[:6]
        objl = '<div class="obj-g" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr))">' + "".join(f'<a class="obj" href="/obekty/{o[0]}/">{o[1]}{ui("right")}</a>' for o in rel_obj) + "</div>"
        side_items = [(x["name"], f"/vrediteli/{x['slug']}/", x["icon"]) for x in PESTS]
        body = f'''{ph(f'Уничтожение {p["gen"]} <span data-cin>в Алматы</span>', p["intro"], p["icon"], f"Здравствуйте! Нужна обработка от: {p['name'].lower()}.")}
<section class="sec"><div class="wrap cnt"><article class="prose">
<h2>Признаки, что пора вызывать специалиста</h2>{ck(p["signs"])}
<h2>Как проходит обработка от {p["gen"]}</h2>{offer_box("обработка от " + p["gen"])}<p>{p["how"]}</p>
<p>Обработка входит в услугу <a href="/uslugi/{s["slug"]}/">{s["name"].lower()}</a>. После работы выдаём акт и рекомендации, при необходимости назначаем контрольный осмотр.</p>
<h2>Как подготовиться</h2>{ck(PREP)}
<h2>Где обрабатываем</h2>{objl}
</article>{side_box(p["name"], url, side_items, "Вредители")}</div></section>
{portfolio_sec(alt=True)}
{sec("Частые вопросы", faq_html(faq))}
{sec("Другие вредители", pest_grid(exclude=p["slug"]), alt=True)}
{lead_form(svc=s["name"])}'''
        t = f"Обработка от {p['gen']} в Алматы — уничтожение {p['gen']}"
        if len(t) > 62: t = f"Обработка и уничтожение {p['gen']} в Алматы"
        page(url, f"{t} | {BRAND}",
             f"Обработка, уничтожение и дезинфекция от {p['gen']} в Алматы и по всему Казахстану. {p['intro'][:90].rstrip(' ,.')}… Договор, акт, расчёт в WhatsApp.",
             body, [service_schema(f"Уничтожение {p['gen']}", url, p["intro"]), faq_schema(faq)],
             crumbs=[("Вредители", "/vrediteli/"), (p["name"], url)], kw=p["gen"], prio="0.8")
    body = f'''{ph("Вредители, от которых избавляем", "Насекомые и грызуны в квартирах, домах, на складах и производствах. Выберите вредителя, чтобы узнать, как проходит обработка.", "s_insect", "Здравствуйте! Помогите определить вредителя.")}
{sec("Насекомые и грызуны", pest_grid())}{lead_form()}'''
    page("/vrediteli/", f"Уничтожение насекомых и грызунов в Алматы | {BRAND}",
         "Уничтожение тараканов, клопов, блох, муравьёв, моли, ос, мокриц, короедов, крыс и мышей в Алматы и по всему Казахстану.",
         body, crumbs=[("Вредители", "/vrediteli/")], kw="вредители насекомые", prio="0.8")

def build_objects():
    for slug, name, gen, text, pests in OBJECTS:
        url = f"/obekty/{slug}/"
        faq = [(f"Сколько стоит обработка {gen}?", "Стоимость зависит от площади, вредителя и вида обработки. Назовём точную цену до выезда."),
               ("Когда вы можете приехать?", "Время выезда согласуем при заявке; для бизнеса работаем в нерабочее время и в выходные."),
               ("Выдаёте ли вы документы?", "Да, акт выполненных работ, для организаций — договор и журналы.")]
        side_items = [(o[1], f"/obekty/{o[0]}/", None) for o in OBJECTS]
        body = f'''{ph(f'Обработка {gen} от насекомых и грызунов <span data-cin>в Алматы</span>', text, "s_biz" if slug not in ("kvartiry","doma","uchastki") else ("s_weed" if slug=="uchastki" else "s_insect"), f"Здравствуйте! Нужна обработка: {name.lower()}.")}
<section class="sec"><div class="wrap cnt"><article class="prose">
<h2>С чем чаще всего обращаются</h2>{ck([x.capitalize() for x in pests])}
<h2>Какие обработки проводим</h2>{offer_box("обработка " + gen)}<p>Для объекта подбираем одну или несколько услуг. Нужное сочетание определяет специалист после осмотра или по описанию ситуации.</p>
{svc_grid(compact=True, limit=6)}
<h2>Как проходит работа</h2>{ck([f"<b>{t}.</b> {d}" for t, d in STEPS])}
</article>{side_box(name, url, side_items, "Объекты")}</div></section>
{sec("Частые вопросы", faq_html(faq), alt=True)}
{reviews_sec()}
{lead_form()}'''
        pl = [GEN_PL.get(x, x) for x in pests[:3]]
        plt = (", ".join(pl[:-1]) + " и " + pl[-1]) if len(pl) > 1 else pl[0]
        page(url, f"Обработка {gen} от {plt} в Алматы | {BRAND}",
             f"Дезинсекция, дезинфекция и дератизация {gen} в Алматы и по Казахстану. {text[:100].rstrip(' ,.')}…",
             body, [service_schema(f"Обработка {gen}", url, text), faq_schema(faq)],
             crumbs=[("Объекты", "/obekty/"), (name, url)], kw=gen, prio="0.7")
    body = f'''{ph("Объекты, которые мы обрабатываем", "От квартиры до производства: подбираем обработку под тип помещения, режим работы и требования санитарных правил.", "s_biz", "Здравствуйте! Нужна обработка объекта.")}
{sec("Типы объектов", obj_grid())}{biz_html()}{lead_form()}'''
    page("/obekty/", f"Обработка квартир, кафе, складов, офисов в Алматы | {BRAND}",
         "Дезинфекция, дезинсекция и дератизация квартир, частных домов, кафе, магазинов, складов, офисов, гостиниц, общежитий и предприятий.",
         body, crumbs=[("Объекты", "/obekty/")], kw="объекты помещения", prio="0.7")

def build_cities():
    for slug, name, cin, region, cl in CITIES:
        if slug == "almaty": continue
        url = f"/goroda/{slug}/"
        ctext, cpests = CLIMATE[cl]
        faq = [(f"Вы работаете {cin}?", f"Да. Проводим дезинфекцию, дезинсекцию и дератизацию {cin}, выезжаем также по региону: {region}."),
               ("Как узнать стоимость?", "Напишите в WhatsApp или онлайн-консультанту: вредитель, тип объекта и площадь. Назовём цену до выезда."),
               (f"Работаете ли с организациями {cin}?", "Да, заключаем договор, работаем по безналичному расчёту и выдаём документы для проверки."),
               ("Как быстро приедет специалист?", "Время выезда согласуем при заявке, учитывая адрес и объём работ.")]
        body = f'''{hero_city(f"Дезинфекция, дезинсекция и дератизация {cin}", f"Санитарная служба {BRAND} {cin}: уничтожаем насекомых и грызунов, проводим дезинфекцию, озонирование и обработку территорий для жилья и бизнеса. Регион выезда — {region}.", "map", f"Здравствуйте! Нужна обработка, город {name}.", city=slug)}
{svc_group_sec()}
{svc_list_sec(alt=True)}
{price_list_sec()}
<section class="sec"><div class="wrap cnt"><article class="prose">
<h2>Вредители, с которыми чаще обращаются {cin}</h2><p>{ctext}</p>{ck(cpests)}
<h2>Услуги {cin}</h2>{svc_grid(compact=True)}
<h2>Для организаций {cin}</h2><p>Обслуживаем кафе, магазины, склады, гостиницы, офисы и производства по договору: акты, журналы, схема точек контроля, безналичный расчёт. Плановые обработки проводим в нерабочее время.</p>
<h2>Как заказать</h2>{ck([f"<b>{t}.</b> {d}" for t, d in STEPS])}
</article>{side_box(f"обработка, {name}", None)}</div></section>
{partners_sec(alt=True)}
{portfolio_sec()}
{sec(f"Частые вопросы — {name}", faq_html(faq), alt=True)}
{reviews_sec()}
{geo_sec(slug)}
{lead_form(f"Рассчитаем стоимость обработки {cin}", city=slug)}'''
        page(url, f"Дезинфекция, дезинсекция, дератизация {cin} — СЭС служба | {BRAND}",
             f"Уничтожение тараканов, клопов, крыс и мышей, дезинфекция и озонирование {cin}. {region}. Договор и акт для СЭС. Работаем по всему Казахстану.",
             body, [service_schema(f"Дезинфекция, дезинсекция и дератизация {cin}", url, ctext, city=name), faq_schema(faq)],
             crumbs=[("Города", "/goroda/"), (name, url)], city_fixed=slug, kw=f"{name} {cin}", prio="0.7")
    cl = "".join(f'<li><a href="{city_url(c[0])}">{c[1]}</a></li>' for c in CITIES)
    body = f'''{ph("Работаем по всему Казахстану", "Основная база — в Алматы. Выезжаем в областные центры, города и районы республики. Выберите свой город.", "map", "Здравствуйте! В каком городе вы работаете?")}
{sec("Города", f'<ul class="chips">{cl}</ul>')}{lead_form()}'''
    page("/goroda/", f"Дезинфекция и дератизация по всему Казахстану — города | {BRAND}",
         "Санитарная служба DezClub работает по всему Казахстану: Алматы, Астана, Шымкент, Караганда, Актобе, Атырау и другие города.",
         body, crumbs=[("Города", "/goroda/")], kw="города казахстан", prio="0.6")

def build_articles():
    for a in ARTICLES:
        url = f"/stati/{a['slug']}/"
        content = "".join(f"<{t}>{x}</{t}>" for t, x in a["body"])
        others = [x for x in ARTICLES if x["slug"] != a["slug"]]
        side_items = [(x["title"], f"/stati/{x['slug']}/", None) for x in ARTICLES]
        body = f'''<section class="ph"><div class="wrap"><!--CRUMBS--></div><div class="wrap ph-in"><div><h1>{a["title"]}</h1><p class="lead-t">{a["desc"]}</p></div><div class="ph-ic">{icon("doc")}</div></div></section>
<section class="sec"><div class="wrap cnt"><article class="prose">{content}<div class="btns" style="margin-top:28px"><a class="btn btn-y" {wa_attr("Здравствуйте! Прочитал статью на сайте, есть вопрос.")}>Задать вопрос в WhatsApp</a><button class="btn btn-o" type="button" data-chat>Спросить онлайн</button></div></article>
{side_box("консультация", url, side_items, "Статьи")}</div></section>
{sec("Услуги", svc_grid(compact=True, limit=8), alt=True)}'''
        art = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
               "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": BRAND},
               "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": SITE_URL + url, "inLanguage": "ru"}
        page(url, f"{a['title']} | {BRAND}", a["desc"], body, [art],
             crumbs=[("Статьи", "/stati/"), (a["title"], url)], kw="статья", prio="0.6")
    items = "".join(f'<a class="art-it" href="/stati/{a["slug"]}/"><h3>{a["title"]}</h3><p>{a["desc"]}</p></a>' for a in ARTICLES)
    body = f'''{ph("Статьи и памятки", "Как подготовиться к обработке, что делать после неё и какие документы нужны бизнесу.", "doc", "Здравствуйте! Есть вопрос по обработке.")}
{sec("Полезное", f'<div class="art-list">{items}</div>')}'''
    page("/stati/", f"Статьи о дезинсекции и дезинфекции | {BRAND}", "Памятки и статьи DezClub: подготовка к обработке, поведение после дезинсекции, документы для СЭС, признаки клопов.",
         body, crumbs=[("Статьи", "/stati/")], kw="статьи памятки", prio="0.5")

def build_misc():
    # цены
    factors = ["Вид вредителя или задача: насекомые, грызуны, дезинфекция, запахи",
               "Площадь и тип объекта: квартира, частный дом, кафе, склад, производство",
               "Степень заражения и нужен ли второй этап обработки",
               "Количество обработок и выбранные препараты"]
    pfaq = [("От чего зависит цена?", "От площади, вида вредителя, степени заражения, типа объекта и количества обработок. Точную стоимость называем до выезда — без доплат на месте."),
            ("Какие есть скидки?", "Скидки до 30%. " + PROMO_HOW),
            ("Можно ли оплатить по безналу?", "Да, для организаций выставляем счёт на ТОО «DezClub» и заключаем договор.")]
    prices_note = ""
    body = f'''{ph("Цены на дезинфекцию, дезинсекцию и дератизацию", f"Дезинсекция — от 8 000 ₸, дератизация — от 7 000 ₸, дезинфекция — от 6 000 ₸. Итоговую стоимость называем до выезда. {PROMO_BIG}.", "card", "Здравствуйте! Хочу узнать стоимость обработки.")}
{price_list_sec()}
{promo_sec()}
<section class="sec"><div class="wrap cnt"><article class="prose">{prices_note}
<h2>Из чего складывается стоимость</h2>{ck(factors)}
<p>Напишите в WhatsApp или онлайн-консультанту, что и где нужно обработать, — назовём точную цену с учётом скидки. Для бизнеса возможен годовой договор с плановыми выездами.</p>
</article>{side_box("расчёт стоимости")}</div></section>
{sec("Частые вопросы о ценах", faq_html(pfaq), alt=True)}{lead_form()}'''
    page("/ceny/", f"Цены на дезинфекцию, дезинсекцию и дератизацию в Алматы — скидки до 30% | {BRAND}",
         "Стоимость дезинсекции, дератизации, дезинфекции и pest control в DezClub: от чего зависит цена, скидки до 30%. Точная стоимость — до выезда, без доплат на месте.",
         body, [faq_schema(pfaq)], crumbs=[("Цены", "/ceny/")], kw="цены прайс стоимость скидка акция", prio="0.8")
    # портфолио
    body = f'''{ph("Портфолио: наши работы", "Видео с реальных объектов — квартиры, дома, кафе, склады и территории.", "s_pest", "Здравствуйте! Посмотрел ваши работы, хочу рассчитать стоимость.")}
<section class="sec"><div class="wrap"><div class="grid-v">{"".join(video_cards())}</div></div></section>
{reviews_sec(alt=True)}{lead_form()}'''
    vids = [{"@context": "https://schema.org", "@type": "VideoObject", "name": v["title"], "description": f"{v['title']} — {BRAND}",
             "thumbnailUrl": poster(v), "contentUrl": v["url"], "embedUrl": f"https://www.youtube.com/embed/{yt_id(v['url'])}", "uploadDate": TODAY} for v in VIDEOS]
    page("/portfolio/", f"Портфолио — видео наших работ | {BRAND}", "Видео реальных обработок DezClub: дезинсекция квартир, дератизация складов, дезинфекция офисов и кафе.",
         body, vids, crumbs=[("Портфолио", "/portfolio/")], kw="портфолио видео работы", prio="0.6")
    # отзывы
    body = f'''{ph("Отзывы клиентов", "Скриншоты сообщений, которые нам присылают клиенты после обработки.", "check", "Здравствуйте! Хочу заказать обработку.")}
{rate_sec()}<section class="sec"><div class="wrap"><div class="grid-v">{"".join(review_cards())}</div></div></section>
{portfolio_sec(alt=True)}{lead_form()}'''
    page("/otzyvy/", f"Отзывы клиентов | {BRAND}", "Отзывы клиентов DezClub об обработке квартир, домов и объектов бизнеса.",
         body, crumbs=[("Отзывы", "/otzyvy/")], kw="отзывы", prio="0.6")
    # оплата
    rows = [("Получатель", COMPANY["legal"]), ("БИН", COMPANY["bin"]), ("ИИК (номер счёта)", COMPANY["iik"]),
            ("БИК банка", COMPANY["bik"]), ("КБе", COMPANY["kbe"]), ("Юридический адрес", "Казахстан, Алматинская обл., г. Алматы, мкр Турксибский, ул. Бекмаханова, дом 96"),
            ("Генеральный директор", COMPANY["director"]), ("Лицензия", f"№ {LICENSE_NO} от {LICENSE_DATE}")]
    tbl = '<table class="req">' + "".join(f'<tr><th>{k}</th><td><span>{E(v)}</span>{"<button class=cp type=button data-copy=\"" + E(v) + "\">копировать</button>" if k in ("БИН","ИИК (номер счёта)","БИК банка") else ""}</td></tr>' for k, v in rows) + "</table>"
    pays = ["Безналичный расчёт по счёту для ТОО и ИП", "Оплата по договору с актом выполненных работ", "Для частных клиентов — наличными или переводом, способ согласуем при заявке"]
    body = f'''{ph("Оплата и реквизиты", "Работаем официально как ТОО. Для организаций выставляем счёт, заключаем договор и передаём закрывающие документы.", "card", "Здравствуйте! Нужен счёт на оплату.")}
<section class="sec"><div class="wrap cnt"><article class="prose">
<h2>Способы оплаты</h2>{ck(pays)}
<h2>Реквизиты</h2>{tbl}
<p style="margin-top:20px">Для выставления счёта пришлите реквизиты вашей организации в WhatsApp.</p>
</article>{side_box("счёт на оплату")}</div></section>{biz_html()}'''
    page("/oplata/", f"Оплата и реквизиты ТОО DezClub | {BRAND}", "Реквизиты ТОО DezClub (БИН 260340008945) и способы оплаты: наличные, перевод, безналичный расчёт для юридических лиц.",
         body, crumbs=[("Оплата", "/oplata/")], kw="реквизиты оплата бин иик счет", prio="0.5")
    # контакты
    q = quote("Алматы, улица Бекмаханова, 96")
    body = f'''{ph("Контакты", f"Звоните или пишите в WhatsApp — ответим, рассчитаем стоимость и согласуем время выезда.", "map", "Здравствуйте! Нужна консультация.")}
<section class="sec"><div class="wrap cnt"><div class="prose">
<h2>Связаться с нами</h2>
<p><b>Телефон и WhatsApp:</b> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
<p><b>Адрес:</b> {E(COMPANY["address"])}</p>
<p><b>Организация:</b> {E(COMPANY["legal"])}, БИН {COMPANY["bin"]}</p>
<p><b>География:</b> Алматы и Алматинская область, выезд по всему Казахстану.</p>
<p><b>Менеджер:</b> {MANAGER[0]}</p>
<h2>Мы в сервисах</h2>{rate_html()}
<iframe class="map" title="DezClub на карте" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={q}&z=15&output=embed"></iframe>
<p style="margin-top:14px"><a href="https://2gis.kz/almaty/search/{q}" target="_blank" rel="noopener">Открыть в 2ГИС</a> · <a href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">Открыть в Google Картах</a></p>
</div>{side_box("консультация")}</div></section>{geo_sec()}'''
    page("/kontakty/", f"Контакты санитарной службы {BRAND} в Алматы", f"Телефон {PHONE_DISPLAY}, WhatsApp, адрес: Алматы, ул. Бекмаханова, 96. Работаем по всему Казахстану.",
         body, crumbs=[("Контакты", "/kontakty/")], kw="контакты телефон адрес", prio="0.6")
    # о компании
    body = f'''{ph(f"О компании {BRAND}", f"{E(COMPANY['legal'])} — санитарная служба дезинфекции, дезинсекции и дератизации. Основная база в Алматы, работаем по всему Казахстану.", "shield", "Здравствуйте! Хочу узнать подробнее о ваших услугах.")}
<section class="sec"><div class="wrap cnt"><article class="prose">
<h2>Коротко о {BRAND}</h2>{ck(FACTS)}
<h2>Чем мы занимаемся</h2><p>Мы уничтожаем насекомых и грызунов, проводим дезинфекцию, дезодорацию и озонирование помещений, обрабатываем территории от клещей и сорняков, а для предприятий выстраиваем систему pest control. Работаем с квартирами, частными домами, кафе, магазинами, складами, гостиницами, офисами и производствами.</p>
<h2>Как мы работаем</h2><p>Каждую обработку начинаем с выяснения ситуации: какой вредитель, какой объект, кто в нём живёт или работает. От этого зависит выбор препарата, метод и время возвращения в помещение. После работы выдаём акт и рекомендации, для бизнеса — полный пакет документов.</p>
<h2>Наши принципы</h2>{adv_html()}
<h2>Документы и стандарты</h2>{trust_html()}
<p>Лицензия, документы специалистов и свидетельства на препараты — на странице <a href="/dokumenty/">«Лицензия и документы»</a>.</p>
<h2>Реквизиты</h2><p>{E(COMPANY["legal"])}, БИН {COMPANY["bin"]}. Генеральный директор — {E(COMPANY["director"])}. Адрес: {E(COMPANY["address"])}. <a href="/oplata/">Все реквизиты</a>.</p>
</article>{side_box("консультация")}</div></section>{equip_sec(alt=True)}{team_sec()}{rate_sec(alt=True)}{portfolio_sec()}{reviews_sec(alt=True)}'''
    page("/o-kompanii/", f"О компании DezClub — опыт работы {EXPERIENCE} | {BRAND}", f"DezClub — санитарная служба дезинфекции, дезинсекции и дератизации: опыт работы {EXPERIENCE}, лицензия № {LICENSE_NO}, скидки до 30%. Алматы и весь Казахстан.",
         body, crumbs=[("О компании", "/o-kompanii/")], kw="о компании", prio="0.5")
    # лицензия и документы
    groups = "".join(f'<h2 class="doc-h">{E(h)}</h2><div class="doc-g">' + "".join(doc_card(*d) for d in items) + "</div>" for h, items in DOCS)
    body = f'''{ph("Лицензия и документы", f"{E(COMPANY['legal'])} работает по государственной лицензии № {LICENSE_NO} от {LICENSE_DATE} на оказание услуг по дезинфекции, дезинсекции и дератизации. Ниже — лицензия, документы о квалификации специалистов и свидетельства о регистрации препаратов, которые мы применяем.", "doc", "Здравствуйте! Нужны копии документов для договора.")}
<section class="sec"><div class="wrap">{groups}
<p class="doc-note">Подлинность лицензии можно проверить на портале <a href="https://elicense.kz" target="_blank" rel="noopener">elicense.kz</a> по номеру {LICENSE_NO}. Копии документов для договора и проверок отправим по запросу в WhatsApp.</p></div></section>
{team_sec(alt=True)}{biz_html()}'''
    lic_sch = {"@context": "https://schema.org", "@type": "WebPage", "name": "Лицензия и документы", "url": SITE_URL + "/dokumenty/",
               "about": {"@id": SITE_URL + "/#org"}}
    page("/dokumenty/", f"Лицензия на дезинфекцию № {LICENSE_NO} и документы | {BRAND}",
         f"Государственная лицензия ТОО «DezClub» на дезинфекцию, дезинсекцию и дератизацию № {LICENSE_NO} от {LICENSE_DATE}, документы специалистов и свидетельства на препараты.",
         body, [lic_sch], crumbs=[("Лицензия и документы", "/dokumenty/")], kw="лицензия документы сертификаты свидетельства", prio="0.6")
    # политика конфиденциальности
    P = [
     ("1. Общие положения", [f"Настоящая политика определяет порядок обработки и защиты персональных данных пользователей сайта {SITE_URL.replace('https://','')} (далее — Сайт). Оператор персональных данных — {COMPANY['legal']}, БИН {COMPANY['bin']}, адрес: {COMPANY['address']} (далее — Оператор).",
       "Обработка персональных данных осуществляется в соответствии с Законом Республики Казахстан «О персональных данных и их защите». Используя Сайт и отправляя заявку, пользователь подтверждает согласие с настоящей политикой."]),
     ("2. Какие данные мы обрабатываем", ["Данные, которые пользователь указывает сам: имя, номер телефона, город, описание задачи и сообщения, отправленные через онлайн-консультант, форму заявки или WhatsApp.",
       "Данные, которые собираются автоматически: технические сведения о посещении (тип устройства и браузера, страницы, время визита), файлы cookie и сведения из локального хранилища браузера (выбранный город, история чата в текущем сеансе)."]),
     ("3. Цели обработки", ["Ответ на обращения и консультация по услугам; расчёт стоимости и согласование выезда специалиста; заключение и исполнение договора, подготовка актов и иных документов; улучшение работы Сайта и оценка эффективности рекламы. Рекламные рассылки направляются только с отдельного согласия пользователя."]),
     ("4. Передача третьим лицам", ["Данные передаются только сотрудникам Оператора, выполняющим обработку на объекте, и только для оказания услуги. Оператор не продаёт и не передаёт персональные данные третьим лицам в рекламных целях без согласия пользователя.",
       "Для работы Сайта используются сторонние сервисы: мессенджер WhatsApp (при переходе в чат), сервисы веб-аналитики и рекламы Google, карты Google, а также сервис обработки сообщений онлайн-консультанта. Эти сервисы обрабатывают данные по собственным правилам. Данные также могут быть предоставлены государственным органам в случаях, предусмотренных законодательством Республики Казахстан."]),
     ("5. Хранение и защита", ["Оператор принимает организационные и технические меры для защиты данных от неправомерного доступа, изменения, раскрытия и уничтожения: ограничение доступа, защита учётных записей, использование защищённого соединения (HTTPS).",
       "Персональные данные хранятся не дольше, чем этого требуют цели обработки или законодательство, после чего удаляются или обезличиваются."]),
     ("6. Права пользователя", ["Пользователь вправе получить сведения о своих персональных данных, потребовать их уточнения, блокирования или удаления, отозвать согласие на обработку, а также обратиться в уполномоченный орган по защите персональных данных. Для этого достаточно связаться с Оператором по контактам, указанным ниже."]),
     ("7. Файлы cookie", ["Cookie и локальное хранилище браузера используются для удобства работы Сайта (запоминание города, работа чата) и для аналитики. Пользователь может ограничить или удалить cookie в настройках браузера; при этом часть функций Сайта может работать некорректно."]),
     ("8. Контакты", [f"По вопросам обработки персональных данных: телефон и WhatsApp {PHONE_DISPLAY}, адрес: {COMPANY['address']}."]),
     ("9. Изменение политики", ["Оператор вправе вносить изменения в настоящую политику. Актуальная редакция всегда размещена на этой странице и вступает в силу с момента публикации."]),
    ]
    content = "".join(f"<h2>{h}</h2>" + "".join(f"<p>{E(x)}</p>" for x in ps) for h, ps in P)
    body = f'''<section class="ph"><div class="wrap"><!--CRUMBS--></div><div class="wrap ph-in"><div><h1>Политика конфиденциальности</h1><p class="lead-t">Как {E(COMPANY["legal"])} обрабатывает и защищает персональные данные пользователей сайта. Редакция от 18.10.2026.</p></div><div class="ph-ic">{icon("shield")}</div></div></section>
<section class="sec"><div class="wrap"><article class="prose">{content}</article></div></section>'''
    page("/privacy-policy/", f"Политика конфиденциальности | {BRAND}", f"Политика обработки персональных данных {COMPANY['legal']}: какие данные собираются на сайте, цели, передача, хранение и права пользователей.",
         body, crumbs=[("Политика конфиденциальности", "/privacy-policy/")], kw="политика конфиденциальности персональные данные", prio="0.2")
    # 404
    body = f'''<section class="ph"><div class="wrap ph-in" style="padding-top:60px"><div><h1>Страница не найдена</h1><p class="lead-t">Возможно, она была перемещена. Перейдите на главную или выберите услугу.</p><div class="btns"><a class="btn btn-y" href="/">На главную</a><a class="btn btn-o" href="/uslugi/">Все услуги</a></div></div><div class="ph-ic">{icon("s_pest")}</div></div></section>{sec("Услуги", svc_grid(compact=True, limit=8))}'''
    page("/404.html", f"Страница не найдена | {BRAND}", "Страница не найдена.", body)

# ------------------------------------------------------------------ сервисные файлы
OG_JOBS = {}
def og_for(url, title):
    import hashlib
    slug = "home" if url == "/" else url.strip("/").replace("/", "-").replace(".html", "")
    big = re.sub(r"\s*\|.*$", "", title)
    big = big.split(" — ")[0].strip()
    if url == "/": big = "Дезинфекция, дезинсекция и дератизация"
    h = hashlib.md5(("2" + big).encode()).hexdigest()[:8]
    OG_JOBS[slug] = big
    return f"/images/og/{slug}.jpg?v={h}"

def build_og():
    import json as _j, hashlib
    from playwright.sync_api import sync_playwright
    out = ROOT / "images" / "og"; out.mkdir(parents=True, exist_ok=True)
    man_p = out / "manifest.json"
    man = _j.loads(man_p.read_text()) if man_p.exists() else {}
    import base64
    def b64(p): return base64.b64encode(p.read_bytes()).decode()
    F = ROOT / "assets" / "fonts"
    css = "".join(f"@font-face{{font-family:M;font-weight:{w};src:url(data:font/woff2;base64,{b64(F / f'montserrat-{sub}-{w}-normal.woff2')}) format('woff2')}}" for w in (600, 800) for sub in ("cyrillic", "latin"))
    logo = "data:image/png;base64," + b64(ROOT / "assets" / "logo-mark.png")
    OGV = "2"
    todo = {k: v for k, v in OG_JOBS.items() if man.get(k) != OGV + v or not (out / f"{k}.jpg").exists()}
    if todo:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
            for k, big in todo.items():
                fs = 80 if len(big) < 30 else 66 if len(big) < 48 else 56
                html_ = f'''<html><head><style>{css}
body{{margin:0;width:1200px;height:630px;overflow:hidden;font-family:M,Arial,sans-serif}}
.b{{width:1200px;height:630px;box-sizing:border-box;background:radial-gradient(circle at 50% 0%,#ffffff 0,#eef6e7 55%,#dcedcf 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 70px;border-bottom:18px solid #3d8520}}
.lg{{display:flex;align-items:center;gap:16px;margin-bottom:24px}} .lg img{{height:84px}} .lg b{{font-family:Georgia,serif;font-size:50px;color:#3d8520}}
h1{{font-size:{fs}px;line-height:1.1;font-weight:800;color:#1f2420;margin:0 0 22px;max-width:1060px}}
.pr{{font-size:36px;font-weight:600;color:#2f6e17;margin-bottom:26px}}
.ph{{font-size:62px;font-weight:800;color:#fff;background:#3d8520;border-radius:22px;padding:8px 36px}}
</style></head><body><div class="b"><div class="lg"><img src="{logo}"><b>DezClub</b></div><h1>{html.escape(big)}</h1><div class="pr">Скидки до 30% · опыт работы {EXPERIENCE}</div><div class="ph">{PHONE_DISPLAY}</div></div></body></html>'''
                pg.set_content(html_); pg.wait_for_timeout(120)
                pg.screenshot(path=str(out / f"{k}.jpg"), type="jpeg", quality=84)
                man[k] = OGV + big
            b.close()
        man_p.write_text(_j.dumps(man, ensure_ascii=False, indent=0))
    print("og:", len(OG_JOBS), "rendered:", len(todo))

def build_meta():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, p in PAGES:
        sm.append(f"<url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "YandexBot", "Bingbot"]
    rb = "".join(f"User-agent: {x}\nAllow: /\n\n" for x in bots)
    (DIST / "robots.txt").write_text(f"{rb}User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    llms = [f"# {BRAND} — санитарная служба (Казахстан)", "",
            f"> {COMPANY['legal']} (БИН {COMPANY['bin']}) — дезинфекция, дезинсекция, дератизация, фумигация, дезодорация, озонирование, акарицидная и гербицидная обработка, pest control. Основная база — Алматы ({COMPANY['street']}), работа по всему Казахстану.", "",
            f"- Телефон и WhatsApp: {PHONE_DISPLAY}", f"- Сайт: {SITE_URL}/", "- Клиенты: квартиры, частные дома, кафе, магазины, склады, гостиницы, офисы, общежития, предприятия, участки",
            "- Документы: договор, акт выполненных работ, журналы учёта, схема точек контроля; безналичный расчёт для юрлиц",
            f"- Государственная лицензия на дезинфекцию, дезинсекцию, дератизацию № {LICENSE_NO} от {LICENSE_DATE} ({LICENSE_BY}): {SITE_URL}/dokumenty/", "",
            "## Ключевые факты"] + [f"- {x}" for x in FACTS] + [
            f"- Генеральный директор: {COMPANY['director']}",
            "- Команда: " + "; ".join(f"{n} — {r}" for n, r in TEAM),
            "- Рейтинги и профили: " + "; ".join(f"{name} {val} ({url})" for _, name, val, _, url in RATINGS),
            "", "## Цены и скидки"] + [f"- {v[0]} — {v[1]}: " + "; ".join(n for _, n, _, _ in v[2]) for v in CATALOG.values()] + ["- Итоговая стоимость зависит от площади, вредителя, степени заражения и объекта, называется до выезда.",
            f"- Скидки: {PROMO_TXT}. {PROMO_HOW}", f"- Подробнее: {SITE_URL}/ceny/",
            "", "## Оборудование"] + [f"- {t}: {d}" for _, t, d in EQUIPMENT] + [
            "", "## Частые вопросы"] + [f"- {q} — {a}" for q, a in FAQ_HOME] + ["",
            "## Услуги"] + [f"- [{s['title']}]({SITE_URL}/uslugi/{s['slug']}/): {s['sub']}" for s in SERVICES] + \
           ["", "## Вредители"] + [f"- [Уничтожение {p['gen']}]({SITE_URL}/vrediteli/{p['slug']}/)" for p in PESTS] + \
           ["", "## Города"] + [f"- [{c[1]}]({SITE_URL}{city_url(c[0])})" for c in CITIES] + \
           ["", "## Статьи"] + [f"- [{a['title']}]({SITE_URL}/stati/{a['slug']}/)" for a in ARTICLES] + \
           ["", "## Контакты", f"- [Контакты]({SITE_URL}/kontakty/)", f"- [Реквизиты]({SITE_URL}/oplata/)"]
    (DIST / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (DIST / "vercel.json").write_text(json.dumps({
        "trailingSlash": True,
        "headers": [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
                    {"source": "/(images|videos)/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000"}]}],
    }, indent=2), encoding="utf-8")

def build_assets():
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    js = (ROOT / "src" / "app.js").read_text(encoding="utf-8")
    cities = [[c[0], c[1], c[2], city_url(c[0])] for c in CITIES]
    js = js.replace("/*__CITIES__*/[]", json.dumps(cities, ensure_ascii=False)).replace("/*__SEARCH__*/[]", json.dumps(SEARCH, ensure_ascii=False))
    (DIST / "assets" / "app.js").write_text(js, encoding="utf-8")
    for d in ("images", "videos"):
        if (ROOT / d).exists():
            shutil.copytree(ROOT / d, DIST / d, dirs_exist_ok=True)
    for f in ("favicon.png", "favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        if (ROOT / "assets" / f).exists():
            shutil.copy(ROOT / "assets" / f, DIST / f)
    (DIST / "site.webmanifest").write_text(json.dumps({"name": "DezClub — санитарная служба", "short_name": BRAND, "start_url": "/", "display": "browser", "background_color": "#ffffff", "theme_color": "#4f9f2a", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")

VER = "2610251800"
MV = VER

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_home(); build_services(); build_pests(); build_objects(); build_cities(); build_articles(); build_misc()
    build_og(); build_assets(); build_meta()
    print("pages:", len(PAGES))
