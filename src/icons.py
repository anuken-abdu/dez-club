# -*- coding: utf-8 -*-
"""SVG-иконки в стиле «циановый duotone». Цвет берётся из currentColor."""

S = 'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" fill="none"'
L = 'fill="currentColor" fill-opacity=".45"'   # светлый тон
W = 'fill="#fff"'

def _svg(body, vb="0 0 48 48", cls="ic"):
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" focusable="false">{body}</svg>'

ALT = {}

def icon(name, size=48, eager=False):
    """Реалистичная иконка из assets/ic (файл SVG, кэшируется браузером)."""
    lz = "" if eager else ' loading="lazy"'
    return f'<img class="ic" src="/assets/ic/{name}.svg" alt="" width="{size}" height="{size}" decoding="async"{lz}>'

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

