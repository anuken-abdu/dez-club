# -*- coding: utf-8 -*-
"""SVG-иконки в стиле «циановый duotone». Цвет берётся из currentColor."""

S = 'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" fill="none"'
L = 'fill="currentColor" fill-opacity=".45"'   # светлый тон
W = 'fill="#fff"'

def _svg(body, vb="0 0 48 48", cls="ic"):
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" focusable="false">{body}</svg>'

ICONS = {}

# --- услуги -------------------------------------------------------------
ICONS["s_insect"] = _svg(f'''
<path {S} stroke-width="2.4" d="M18 20 9 15M17 27H7M18 34l-8 6M30 20l9-5M31 27h10M30 34l8 6M21 9l-4-5M27 9l4-5"/>
<ellipse cx="24" cy="28" rx="9.5" ry="13" fill="currentColor"/>
<circle cx="24" cy="12.5" r="4.6" fill="currentColor"/>
<path stroke="#fff" stroke-width="1.8" stroke-linecap="round" d="M24 17v24M18 25h4M26 25h4M17.5 31h4.5M26 31h4.5"/>''')

ICONS["s_virus"] = _svg(f'''
<g {S} stroke-width="2.6"><path d="M24 4v6M24 38v6M4 24h6M38 24h6M9.9 9.9l4.2 4.2M33.9 33.9l4.2 4.2M38.1 9.9l-4.2 4.2M14.1 33.9l-4.2 4.2"/></g>
<g fill="currentColor"><circle cx="24" cy="4" r="2.6"/><circle cx="24" cy="44" r="2.6"/><circle cx="4" cy="24" r="2.6"/><circle cx="44" cy="24" r="2.6"/><circle cx="9.9" cy="9.9" r="2.6"/><circle cx="38.1" cy="38.1" r="2.6"/><circle cx="38.1" cy="9.9" r="2.6"/><circle cx="9.9" cy="38.1" r="2.6"/></g>
<circle cx="24" cy="24" r="13" fill="currentColor"/>
<circle cx="19.5" cy="20" r="3.4" {W}/><circle cx="28.5" cy="27.5" r="2.6" {W}/><circle cx="27" cy="18" r="1.6" {W}/><circle cx="19" cy="29" r="1.7" {W}/>''')

ICONS["s_rat"] = _svg(f'''
<path {S} stroke-width="2.6" d="M11 31c-6 2-8 7-4 10s11 1 14-1"/>
<path fill="currentColor" d="M10 29c0-6 6-11 15-11 5 0 8 1 10 3l9 6c1 1 1 2-1 3l-6 2c-2 3-6 5-12 5H16c-4 0-6-3-6-8z"/>
<circle cx="31" cy="18" r="4.5" {L}/>
<circle cx="37" cy="25" r="1.6" {W}/>
<path {S} stroke-width="2.4" d="M18 36v4M28 36v4"/>''')

ICONS["s_fumig"] = _svg(f'''
<path {S} stroke-width="2.4" d="M16 16h-5v26M11 42h-1"/>
<rect x="21" y="6" width="9" height="5" rx="1" fill="currentColor"/>
<rect x="16" y="11" width="21" height="31" rx="3.5" fill="currentColor"/>
<rect x="19" y="19" width="15" height="15" rx="2" {W}/>
<circle cx="26.5" cy="26.5" r="5" fill="none" stroke="currentColor" stroke-width="2"/>
<path stroke="currentColor" stroke-width="2" d="M23 23l7 7"/>
<rect x="8" y="12" width="4" height="8" rx="1" {L}/>''')

ICONS["s_odor"] = _svg(f'''
<g {S} stroke-width="2.8">
<path d="M5 17h22a5 5 0 1 0-5-5"/>
<path d="M5 25h31a5.5 5.5 0 1 1-5.5 5.5"/>
<path d="M5 33h12a4 4 0 1 1-4 4"/>
</g>
<path {S} stroke-width="2.8" stroke-opacity=".5" d="M31 17h6M41 25h2"/>''')

ICONS["s_ozone"] = _svg(f'''
<circle cx="13" cy="9" r="3" {L}/><circle cx="21" cy="5.5" r="2.2" {L}/><circle cx="30" cy="7.5" r="2.6" {L}/><circle cx="37" cy="12" r="1.8" {L}/>
<path fill="currentColor" d="M13 42a8.5 8.5 0 0 1-1.6-16.8A11 11 0 0 1 32.4 20a9 9 0 0 1 9.1 9.6A6.5 6.5 0 0 1 38 42z"/>
<text x="25" y="37" fill="#fff" font-family="Montserrat,Arial,sans-serif" font-weight="800" font-size="12" text-anchor="middle">O<tspan font-size="7" dy="3">3</tspan></text>''')

ICONS["s_tick"] = _svg(f'''
<g {S} stroke-width="2.4"><path d="M15 22l-7-5-2-5M14 28H6l-3 3M16 33l-6 5v5M33 22l7-5 2-5M34 28h8l3 3M32 33l6 5v5"/><path d="M20 8l-2-4M28 8l2-4"/></g>
<circle cx="24" cy="11" r="4.5" fill="currentColor"/>
<ellipse cx="24" cy="28" rx="11" ry="12.5" fill="currentColor"/>
<path {L} d="M24 17c5 0 8 3 8 7 0 3-3 6-8 6s-8-3-8-6c0-4 3-7 8-7z"/>
<path stroke="#fff" stroke-width="1.8" stroke-linecap="round" d="M24 31v7"/>''')

ICONS["s_weed"] = _svg(f'''
<g {S} stroke-width="2.6">
<path d="M24 44c0-10-2-16-8-22"/><path d="M24 44c0-12 3-20 9-26"/><path d="M24 44c-1-7-5-11-12-13"/><path d="M24 44c2-8 7-12 14-12"/><path d="M24 44V26"/>
</g>
<g {L}><circle cx="16" cy="12" r="2.4"/><circle cx="33" cy="9" r="3"/><circle cx="9" cy="22" r="2"/><circle cx="40" cy="20" r="2.2"/><circle cx="24" cy="16" r="2.6"/></g>
<path {S} stroke-width="1.6" d="M33 9v9M16 12v8"/>''')

ICONS["s_biz"] = _svg(f'''
<rect x="7" y="8" width="20" height="34" rx="2" fill="currentColor"/>
<rect x="29" y="20" width="13" height="22" rx="2" {L}/>
<g {W}><rect x="11" y="13" width="4" height="4" rx=".6"/><rect x="19" y="13" width="4" height="4" rx=".6"/><rect x="11" y="21" width="4" height="4" rx=".6"/><rect x="19" y="21" width="4" height="4" rx=".6"/><rect x="11" y="29" width="4" height="4" rx=".6"/><rect x="19" y="29" width="4" height="4" rx=".6"/><rect x="14" y="36" width="6" height="6"/></g>
<g fill="currentColor"><rect x="32" y="25" width="7" height="2.4" rx="1"/><rect x="32" y="30" width="7" height="2.4" rx="1"/><rect x="32" y="35" width="7" height="2.4" rx="1"/></g>''')

ICONS["s_pest"] = _svg(f'''
<circle cx="20" cy="20" r="14" {L}/>
<circle cx="20" cy="20" r="14" {S} stroke-width="3.2"/>
<path {S} stroke-width="5.5" d="M31 31l11 11"/>
<path {S} stroke-width="3.2" d="M13.5 20.5l4.5 4.5 8.5-9"/>''')

# --- вредители ----------------------------------------------------------
ICONS["cockroach"] = _svg(f'''
<path {S} stroke-width="2.2" d="M21 10C17 5 12 3 6 4M27 10c4-5 9-7 15-6M17 22l-9-3-3-5M16 29l-10 2-2 5M18 36l-6 6M31 22l9-3 3-5M32 29l10 2 2 5M30 36l6 6"/>
<path fill="currentColor" d="M24 15c7 0 9 7 9 15s-4 14-9 14-9-6-9-14 2-15 9-15z"/>
<path fill="currentColor" d="M19 15a5 4 0 0 1 10 0z"/>
<path stroke="#fff" stroke-width="1.6" d="M24 17v26"/>
<path {L} d="M17 19c3-2 11-2 14 0-2 2-12 2-14 0z"/>''')

ICONS["bedbug"] = _svg(f'''
<path {S} stroke-width="2.2" d="M14 22l-8-3M13 29H5M15 36l-6 4M34 22l8-3M35 29h8M33 36l6 4M21 9l-3-5M27 9l3-5"/>
<circle cx="24" cy="11" r="3.8" fill="currentColor"/>
<path fill="currentColor" d="M24 15c10 0 13 7 13 14s-5 15-13 15-13-8-13-15 3-14 13-14z"/>
<g stroke="#fff" stroke-width="1.5" fill="none"><path d="M14 24c6 2 14 2 20 0M12.5 30c7 2 16 2 23 0M14 36c6 2 14 2 20 0"/></g>''')

ICONS["mite"] = _svg(f'''
<g {S} stroke-width="2.2"><path d="M16 20 9 14M15 26H6M16 32l-7 5M32 20l7-6M33 26h9M32 32l7 5"/></g>
<circle cx="24" cy="12" r="4" fill="currentColor"/>
<circle cx="24" cy="27" r="11" fill="currentColor"/>
<circle cx="20" cy="24" r="2.2" {W} fill-opacity=".8"/><circle cx="27" cy="29" r="1.8" {W} fill-opacity=".8"/>''')

ICONS["wasp"] = _svg(f'''
<path {L} d="M22 18C14 6 4 8 5 14s10 7 17 6zM26 18c8-12 18-10 17-4s-10 7-17 6z"/>
<circle cx="24" cy="12" r="4.5" fill="currentColor"/>
<ellipse cx="24" cy="21" rx="4" ry="4" fill="currentColor"/>
<path fill="currentColor" d="M24 25c5 0 7 5 7 9 0 6-4 10-7 11-3-1-7-5-7-11 0-4 2-9 7-9z"/>
<g stroke="#fff" stroke-width="2.2"><path d="M17.5 31h13M18 37h12"/></g>
<path {S} stroke-width="2" d="M21 8l-3-4M27 8l3-4"/>''')

ICONS["woodlouse"] = _svg(f'''
<g {S} stroke-width="2"><path d="M13 16l-6-2M12 22H5M12 28l-7 1M13 34l-6 3M35 16l6-2M36 22h7M36 28l7 1M35 34l6 3M20 7l-4-4M28 7l4-4"/></g>
<path fill="currentColor" d="M24 7c8 0 12 6 12 18 0 11-5 18-12 18s-12-7-12-18C12 13 16 7 24 7z"/>
<g stroke="#fff" stroke-width="1.6" fill="none"><path d="M14 15h20M13 21h22M12.5 27h23M13 33h22M15 39h18"/></g>''')

ICONS["beetle"] = _svg(f'''
<g {S} stroke-width="2.2"><path d="M14 20l-8-4M13 28H5M15 36l-6 5M34 20l8-4M35 28h8M33 36l6 5M20 7l-3-4M28 7l3-4"/></g>
<path fill="currentColor" d="M18 9h12l2 6H16z"/>
<path fill="currentColor" d="M24 15c8 0 12 5 12 14s-5 15-12 15-12-6-12-15 4-14 12-14z"/>
<path stroke="#fff" stroke-width="1.8" d="M24 16v28"/>
<path {L} d="M16 21c2-3 5-4 7-4v10c-3 0-6-2-7-6zM32 21c-2-3-5-4-7-4v10c3 0 6-2 7-6z" fill="#fff" fill-opacity=".35"/>''')

ICONS["flea"] = _svg(f'''
<path fill="currentColor" d="M12 26c0-10 9-16 19-14 7 2 11 8 9 15-2 8-10 11-18 10-6-1-10-5-10-11z"/>
<path fill="currentColor" d="M12 22c-3-2-6-1-7 1 1 3 4 4 7 3z"/>
<g {S} stroke-width="2.4"><path d="M22 36l-4 8M28 36l2 8M34 33l8 6 1 5"/><path d="M5 22 2 19"/></g>
<path stroke="#fff" stroke-width="1.5" fill="none" d="M20 16c2 6 2 14 0 20M27 13c2 7 2 16 0 23M33 15c2 6 2 12 0 18"/>''')

ICONS["fly"] = _svg(f'''
<path {L} d="M21 20C12 10 3 13 5 19s9 7 16 4zM27 20c9-10 18-7 16-1s-9 7-16 4z"/>
<circle cx="24" cy="12" r="5.5" fill="currentColor"/>
<circle cx="20.8" cy="11" r="2.2" {W} fill-opacity=".6"/><circle cx="27.2" cy="11" r="2.2" {W} fill-opacity=".6"/>
<path fill="currentColor" d="M24 17c5 0 6 5 6 11 0 8-3 15-6 15s-6-7-6-15c0-6 1-11 6-11z"/>
<g stroke="#fff" stroke-width="1.6"><path d="M19 27h10M19 33h10"/></g>
<g {S} stroke-width="2"><path d="M18 23l-6 6M30 23l6 6M19 31l-6 8M29 31l6 8"/></g>''')

ICONS["ant"] = _svg(f'''
<g {S} stroke-width="2.2"><path d="M21 22l-9-6-3 2M21 25H9l-3 4M22 28l-7 8v6M27 22l9-6 3 2M27 25h12l3 4M26 28l7 8v6M21 6l-4-3M27 6l4-3"/></g>
<circle cx="24" cy="9.5" r="4.8" fill="currentColor"/>
<ellipse cx="24" cy="22" rx="4" ry="5.5" fill="currentColor"/>
<ellipse cx="24" cy="36" rx="7" ry="9" fill="currentColor"/>
<path {L} fill="#fff" fill-opacity=".35" d="M20 33c1-3 3-4 4-4s3 1 4 4c-1 1-7 1-8 0z"/>''')

ICONS["moth"] = _svg(f'''
<path fill="currentColor" d="M22 18 6 8c-4 0-4 10 0 16l16 2z"/>
<path fill="currentColor" d="M26 18 42 8c4 0 4 10 0 16l-16 2z"/>
<path {L} d="M22 27 9 30c-3 4 1 11 6 9l7-7zM26 27l13 3c3 4-1 11-6 9l-7-7z"/>
<rect x="21.5" y="13" width="5" height="26" rx="2.5" fill="currentColor"/>
<path {S} stroke-width="2" d="M22 13c-2-4-5-7-9-8M26 13c2-4 5-7 9-8"/>
<g {W} fill-opacity=".6"><circle cx="13" cy="16" r="2"/><circle cx="35" cy="16" r="2"/></g>''')

ICONS["rat"] = ICONS["s_rat"]
ICONS["mouse"] = _svg(f'''
<path {S} stroke-width="2.4" d="M10 33c-6 0-8 4-6 7"/>
<path fill="currentColor" d="M9 31c0-7 6-12 14-12 6 0 10 3 13 6l7 5c1 1 0 2-1 2l-5 1c-3 3-7 5-12 5H14c-3 0-5-3-5-7z"/>
<circle cx="29" cy="17" r="6" {L}/>
<circle cx="29" cy="17" r="3" fill="currentColor"/>
<circle cx="37" cy="27" r="1.5" {W}/>
<path {S} stroke-width="2.2" d="M17 38v3M27 38v3"/>''')

# --- преимущества (линейные) -------------------------------------------
def _line(d, extra=""):
    return _svg(f'<g {S} stroke-width="2.4">{d}</g>{extra}', cls="ic ic-line")

ICONS["doc"] = _line('<path d="M12 5h17l9 9v29H12z"/><path d="M29 5v9h9M18 22h14M18 29h14M18 36h8"/>')
ICONS["shield"] = _line('<path d="M24 4 8 10v12c0 11 7 18 16 22 9-4 16-11 16-22V10z"/><path d="m17 24 5 5 10-11"/>')
ICONS["time"] = _line('<circle cx="24" cy="25" r="17"/><path d="M24 15v10l7 5M19 4h10"/>')
ICONS["check"] = _line('<rect x="7" y="7" width="34" height="34" rx="8"/><path d="m15 24 6 6 12-13"/>')
ICONS["card"] = _line('<rect x="5" y="11" width="38" height="26" rx="4"/><path d="M5 19h38M11 30h8"/>')
ICONS["map"] = _line('<path d="M24 43s-13-12-13-23a13 13 0 0 1 26 0c0 11-13 23-13 23z"/><circle cx="24" cy="20" r="5"/>')

# --- интерфейс -----------------------------------------------------------
def ui(name):
    d = UI[name]
    return f'<svg class="ui ui-{name}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{d}</svg>'

US = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
UI = {
    "pin": f'<path {US} d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle {US} cx="12" cy="9.5" r="2.5"/>',
    "phone": f'<path {US} d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": f'<rect {US} x="3" y="5" width="18" height="14" rx="2"/><path {US} d="m3 7 9 6 9-6"/>',
    "chev": f'<path {US} d="m6 9 6 6 6-6"/>',
    "right": f'<path {US} d="m9 6 6 6-6 6"/>',
    "left": f'<path {US} d="m15 6-6 6 6 6"/>',
    "arrow": f'<path {US} d="M7 17 17 7M8 7h9v9"/>',
    "search": f'<circle {US} cx="11" cy="11" r="7"/><path {US} d="m20 20-4-4"/>',
    "close": f'<path {US} d="M6 6l12 12M18 6 6 18"/>',
    "menu": f'<path {US} d="M4 7h16M4 12h16M4 17h16"/>',
    "play": '<path fill="currentColor" d="M8 5.5v13a1 1 0 0 0 1.5.9l10.4-6.5a1 1 0 0 0 0-1.8L9.5 4.6A1 1 0 0 0 8 5.5z"/>',
    "send": f'<path {US} d="M21 3 10 14M21 3l-7 18-4-7-7-4z"/>',
    "chat": f'<path {US} d="M4 5h16v11H9l-5 4z"/><path {US} d="M8 10h8M8 13h5"/>',
    "check": f'<path {US} d="m5 12 5 5 9-10"/>',
    "clock": f'<circle {US} cx="12" cy="12" r="9"/><path {US} d="M12 7v5l3 2"/>',
    "wa": '<path fill="currentColor" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.05 21.8h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88zm8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.41z"/>',
}

def icon(name):
    return ICONS[name]
