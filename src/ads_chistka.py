# -*- coding: utf-8 -*-
"""DezClub: чистка мусорного трафика (по поисковым запросам из отчёта).
1-dobavit-minus-slova.xlsx — новые минус-слова в существующий список «DezClub минус-слова» (он уже привязан ко всем кампаниям).
2-udalit-shirokie-klyuchi.xlsx — удаление фразовых «сэс / санэпидемстанция / санобработка + город» (точные остаются).
Загрузка: Инструменты → Массовые действия → Загрузки."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ads_goroda as A
from data import CITIES

OUT = Path(__file__).resolve().parent.parent / "google-ads" / "chistka"
NEW = [
    # чужие ниши из отчёта и похожие
    "массаж", "боди", "спа", "сауна", "салон", "риэлтор", "риелтор", "агентство недвижимости", "недвижимость", "аренда", "посуточно", "сдам", "сниму",
    "асхана", "кафе на", "банкетный зал", "домофон", "видеонаблюдение", "сантехник", "электрик", "такси", "грузоперевозки", "эвакуатор", "автосервис",
    "шиномонтаж", "химчистка", "прачечная", "парикмахерская", "стоматология", "клиника", "аптека", "ветеринар", "ветклиника", "зоомагазин",
    # названия других компаний и порталов из отчёта
    "санэко", "батыс дез", "аяхан", "камкорлык", "qosimsha", "косымша", "2гис", "2gis", "olx", "kaspi",
    # государственная СЭС и справки
    "санэпидемстанция адрес", "сэс адрес", "сэс телефон", "сэс официальный", "сэс график", "сэс режим работы", "госсанэпиднадзор", "санэпиднадзор",
    "справку", "заключение сэс", "санитарно эпидемиологическое заключение", "проверка сэс",
]
NEW = [n for n in dict.fromkeys(NEW) if n not in A.NEG_PHRASE]
RISKY = ["сэс", "санэпидемстанция", "санобработка"]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*"): f.unlink()
    # минус-слова не должны резать наши ключи
    allkw = []
    for slug, nom, cin, region, _ in CITIES:
        kw, kin, alts, p2 = A.city_forms(slug, nom, cin)
        for g in A.G:
            for b in g[2]:
                allkw += [f"{b} {kw}"] + [f"{b} {a}" for a in alts]
            allkw += g[3]
    bad = [(n, k) for n in NEW for k in allkw if f" {n} " in f" {k} "]
    if bad: print("конфликт:", bad[:10]); raise SystemExit(1)
    neg = [{"Action": "Add", "Negative keyword list name": A.NEG_LIST, "Negative keyword": n, "Keyword or list": "Keyword", "Match type": "Phrase Match"} for n in NEW]
    A.xlsx(OUT / "1-dobavit-minus-slova.xlsx", ["Action", "Negative keyword list name", "Negative keyword", "Keyword or list", "Match type"], neg)
    rem = []
    for slug, nom, cin, region, _ in CITIES:
        C = "DezClub Астана" if slug == "astana" else A.camp(nom)
        kw, kin, alts, p2 = A.city_forms(slug, nom, cin)
        for b in RISKY:
            for form in [f"{b} {kw}"] + [f"{b} {a}" for a in alts]:
                rem.append({"Action": "Remove", "Campaign": C, "Ad group": "Дезинфекция и СЭС", "Keyword": f'"{form}"'})
    A.xlsx(OUT / "2-udalit-shirokie-klyuchi.xlsx", ["Action", "Campaign", "Ad group", "Keyword"], rem)
    print("минус-слов", len(neg), "удалить ключей", len(rem))

if __name__ == "__main__":
    main()
