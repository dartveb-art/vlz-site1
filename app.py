from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import urllib.request, json
app=FastAPI(title="Воскресенский Литейный Завод")

METALS=[
("gold","Золото","troy_ounce","USD/тр. унц."),
("silver","Серебро","troy_ounce","USD/тр. унц."),
("platinum","Платина","troy_ounce","USD/тр. унц."),
("palladium","Палладий","troy_ounce","USD/тр. унц."),
("copper","Медь","metric_ton","USD/т"),
("aluminum","Алюминий","metric_ton","USD/т"),
("cobalt","Кобальт","metric_ton","USD/т"),
("gallium","Галлий","kilogram","USD/кг"),
("indium","Индий","kilogram","USD/кг"),
("iridium","Иридий","troy_ounce","USD/тр. унц."),
("iron_ore","Железная руда","metric_ton","USD/т"),
("lead","Свинец","metric_ton","USD/т"),
("lithium_carbonate","Карбонат лития","metric_ton","USD/т"),
("molybdenum","Молибден","kilogram","USD/кг"),
("neodymium","Неодим","kilogram","USD/кг"),
("nickel","Никель","metric_ton","USD/т"),
("rhodium","Родий","troy_ounce","USD/тр. унц."),
("ruthenium","Рутений","troy_ounce","USD/тр. унц."),
("tellurium","Теллур","kilogram","USD/кг"),
("tin","Олово","metric_ton","USD/т"),
("uranium","Уран (U3O8)","pound","USD/фунт"),
("zinc","Цинк","metric_ton","USD/т"),
("steel","Сталь (HRC)","metric_ton","USD/т"),
]
@app.get("/api/health")
def health(): return {"status":"ok","service":"VLZ preview"}
@app.get("/api/quotes")
def quotes():
    out=[]
    for slug,title,unit,unit_label in METALS:
        url=f"https://croncopia.com/api/metals/{slug}.json"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"VLZ-preview/1.0"})
            with urllib.request.urlopen(req,timeout=8) as r: data=json.loads(r.read().decode())
            price=data.get("price")
            if isinstance(price,dict): price=price.get(unit)
            out.append({"metal":title,"slug":slug,"price":price,"currency":data.get("base","USD"),"unit":unit_label,"timestamp":data.get("timestamp"),"sources":data.get("sources"),"status":"available" if price is not None else "missing"})
        except Exception as e:
            out.append({"metal":title,"slug":slug,"price":None,"currency":"USD","unit":unit_label,"timestamp":None,"sources":0,"status":"unavailable"})
    return {"provider":"Croncopia","updated":"live request","quotes":out}
@app.get("/",response_class=HTMLResponse)
def home():
 return HTML
@app.get("/admin.html",response_class=HTMLResponse)
def admin():
 return """<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>ВЛЗ — администрирование</title><style>body{font:16px Arial;background:#f4f1eb;padding:24px;color:#24211d}main{max-width:680px;margin:auto;background:white;padding:24px;border-radius:16px}a{color:#98552f}</style><main><h1>ВЛЗ — тестовая панель</h1><p>Публичный тестовый стенд. В этой облегчённой сборке редактирование закупочных цен и управление заявками ещё не подключены.</p><p><a href='/'>Вернуться на сайт</a></p><p>Статус API: <a href='/api/health'>проверить</a></p></main>"""
HTML="""<!doctype html><html lang=ru><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Воскресенский Литейный Завод — ВЛЗ</title><style>
:root{--ink:#28251f;--muted:#77716a;--copper:#a96338;--cream:#f4f1eb;--line:#e5ded4}*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:16px Arial,sans-serif}header{background:#25231f;color:white;padding:18px max(22px,calc((100% - 1120px)/2));display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}.brand{font-weight:800;letter-spacing:.04em}.brand span{color:#d89a6c}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:inherit;text-decoration:none}nav a{font-size:14px;color:#eee}main{max-width:1120px;margin:auto;padding:34px 22px}.hero{background:linear-gradient(120deg,#302c26,#62503e);color:white;border-radius:18px;padding:48px 38px;margin-bottom:26px}.eyebrow{color:#e2b18b;text-transform:uppercase;letter-spacing:.14em;font-size:12px}.hero h1{font-size:clamp(30px,5vw,52px);max-width:780px;line-height:1.08;margin:14px 0}.hero p{color:#e8ded4;max-width:650px;line-height:1.6}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.btn{background:var(--copper);color:white;padding:13px 18px;border-radius:8px;font-weight:700}.btn.secondary{background:transparent;border:1px solid #cbb29d}.section{background:white;border:1px solid var(--line);border-radius:16px;padding:24px;margin:22px 0}.section h2{margin:0 0 8px}.muted{color:var(--muted);line-height:1.5}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.stat{background:#faf8f5;border:1px solid var(--line);padding:18px;border-radius:12px}.stat b{display:block;color:var(--copper);font-size:23px;margin-bottom:5px}.tablewrap{overflow:auto}table{border-collapse:collapse;width:100%;min-width:620px}th,td{text-align:left;padding:13px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:12px;text-transform:uppercase}td.price{font-weight:700;font-variant-numeric:tabular-nums}.status{font-size:12px;color:#4b7753}.foot{color:var(--muted);font-size:12px;line-height:1.5}footer{background:#25231f;color:#ddd;padding:28px;text-align:center;font-size:13px}@media(max-width:600px){header{padding:16px 18px}.hero{padding:32px 22px}.section{padding:18px}.stats{grid-template-columns:1fr}}
</style></head><body><header><div class=brand>ВЛЗ <span>●</span> ВОСКРЕСЕНСКИЙ ЛИТЕЙНЫЙ ЗАВОД</div><nav><a href='#about'>О заводе</a><a href='#metals'>Металлы</a><a href='#quotes'>Котировки</a><a href='#contact'>Контакты</a></nav></header><main><section class=hero><div class=eyebrow>Промышленность · Металлургия · Закупки</div><h1>Воскресенский Литейный Завод</h1><p>Закупка лома цветных и редких металлов, ферросплавов и металлосодержащего сырья. Работаем с предложениями поставщиков.</p><div class=actions><a class=btn href='#contact'>Предложить металл</a><a class='btn secondary' href='#quotes'>Биржевые ориентиры</a></div></section><section id=about class=section><h2>ВЛЗ — работа с металлами</h2><p class=muted>Тестовая версия сайта завода. Здесь собраны основные направления закупки и справочные котировки металлов из единого открытого источника.</p><div class=stats><div class=stat><b>23</b>серии котировок</div><div class=stat><b>1</b>источник данных</div><div class=stat><b>USD</b>валюта источника</div></div></section><section id=metals class=section><h2>Каталог металлов</h2><p class=muted>Цветные, драгоценные, редкие металлы и сырьевые позиции.</p><p>Медь · Алюминий · Никель · Цинк · Свинец · Олово · Кобальт · Молибден · Вольфрам · Золото · Серебро · Платина · Палладий · Редкие металлы</p></section><section id=quotes class=section><h2>Котировки металлов</h2><p class=muted>Данные Croncopia. Справочные агрегированные цены, не гарантированная цена сделки и не оферта.</p><div class=tablewrap><table><thead><tr><th>Металл</th><th>Цена</th><th>Единица</th><th>Обновление источника</th></tr></thead><tbody id=rows><tr><td colspan=4>Загружаем данные…</td></tr></tbody></table></div><p class=foot id=source>Источник: Croncopia · обновление по метке времени источника.</p></section><section id=contact class=section><h2>Предложить металл к закупке</h2><p class=muted>Тестовая форма обратной связи. Временная версия не отправляет заявки на почту и не сохраняет персональные данные.</p><p>Для коммерческого предложения подготовьте: наименование металла, форму материала, объём, содержание основного элемента и фотографии/паспорт качества.</p></section></main><footer>© Воскресенский Литейный Завод · Тестовая версия сайта</footer><script>
async function load(){const body=document.getElementById('rows');try{const r=await fetch('/api/quotes');const j=await r.json();body.innerHTML=j.quotes.map(q=>'<tr><td>'+q.metal+'</td><td class=price>'+(q.price==null?'Нет данных':Number(q.price).toLocaleString('ru-RU',{maximumFractionDigits:2}))+' '+q.currency+'</td><td>'+q.unit+'</td><td>'+ (q.timestamp?new Date(q.timestamp).toLocaleString('ru-RU'):'—')+'</td></tr>').join('');document.getElementById('source').textContent='Источник: Croncopia · число поставщиков в агрегате указано в API · цены справочные.'}catch(e){body.innerHTML='<tr><td colspan=4>Не удалось получить котировки. Повторите позже.</td></tr>'}}load();setInterval(load,300000);
</script></body></html>"""
