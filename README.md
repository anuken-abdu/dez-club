# DezClub — сайт санитарной службы

Готовый сайт лежит в `dist/` — его и выкладываем на хостинг.

## Структура
- `src/data.py` — весь текст: услуги, вредители, объекты, города, статьи, реквизиты, подписи к видео, домен, телефон, ID Google Ads.
- `src/build.py` — сборка сайта: `python3 src/build.py` → `dist/`.
- `src/app.js` — меню, выбор города, поиск, чат-автоответчик, формы, просмотр видео и отзывов.
- `assets/styles.css`, `assets/fonts/` — стили и шрифт Montserrat (локально, без CDN).
- `api/chat.js` — серверная функция ИИ-консультанта для Vercel.
- `images/`, `videos/` — медиа. Фото и видео загружать в корневые `images/` и `videos/`: Vercel при каждом деплое сам копирует их в `dist/`. Имена файлов — в `images/README.txt`.

## Перед запуском
1. Домен: в `src/data.py` поменять `SITE_URL` (сейчас `https://dezclub.kz`), пересобрать.
2. Видео и отзывы: положить 9 видео в `videos/work-1.mp4…work-9.mp4`, обложки в `images/portfolio/`, 7 скриншотов в `images/reviews/`, поправить подписи `VIDEOS` в `src/data.py`, пересобрать.

## Деплой на Vercel
Выложить папку `dist/` как проект (Framework: Other, без сборки). Статика и функция `/api/chat` подхватятся автоматически.

## ИИ-чат
- Без ключа чат работает как автоответчик по встроенной базе ответов и передаёт заявку в WhatsApp.
- Чтобы включить ответы ИИ: Vercel → Settings → Environment Variables → `ANTHROPIC_API_KEY` = ключ из console.anthropic.com, затем Redeploy. Модель можно сменить переменной `ANTHROPIC_MODEL`. Если ИИ недоступен, сайт сам переключается на автоответчик.

## Google Ads
В `src/data.py` заполнить `GADS_ID` (AW-…) и `GADS_CALL_LABEL` — клики по телефону и WhatsApp будут отправляться как конверсии.

## SEO/GEO
sitemap.xml, robots.txt, llms.txt, JSON-LD (LocalBusiness, Service, FAQPage, BreadcrumbList, Article, VideoObject), канонические ссылки, Open Graph, 30 городских страниц. После запуска добавить сайт в Google Search Console и отправить sitemap.
