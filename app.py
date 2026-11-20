from fastapi import FastAPI, Request
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


FERROALLOYS = [
("ferromolybdenum-60","Ферромолибден 60","https://alapmet.com/wp-content/uploads/2023/06/ferromolybdenum.jpg"),
("ferromolybdenum-50","Ферромолибден 50","https://www.cnxhyalloy.com/uploads/2021/08/ferromolybdenum.jpg"),
("ferromanganese-fmn78","Ферромарганец ФМн78","https://upload.wikimedia.org/wikipedia/commons/1/1d/Ferromangan%C3%A8se_m%C3%A9tal.jpg"),
("ferromanganese-fmn95","Ферромарганец ФМн95","https://upload.wikimedia.org/wikipedia/commons/8/8a/Ferromangan%C3%A8se_carbur%C3%A9.jpg"),
("ferrosilicon-fs75","Ферросилиций ФС75","https://www.za-refractories.com/uploads/2021/06/ferro-silicon-75.jpg"),
("ferrosilicomanganese-mns17","Ферросиликомарганец МнС17","https://www.brndistic.com/wp-content/uploads/2020/12/ferro-silico-manganese.jpg"),
]

PAGES = {
"/": ("Главная", """<section class="hero"><div class="eyebrow">Промышленность · Металлургия · Закупки</div><h1>Воскресенский Литейный Завод</h1><p>Закупка лома цветных и редких металлов, ферросплавов и металлосодержащего сырья. Принимаем предложения от поставщиков и предприятий.</p><div class="actions"><a class="btn" href="/procurement">Предложить металл</a><a class="btn secondary" href="/quotes">Смотреть котировки</a></div></section><section class="grid"><a class="tile" href="/metals"><b>Каталог металлов</b><span>Основные цветные, драгоценные и редкие металлы</span></a><a class="tile" href="/quotes"><b>Биржевые ориентиры</b><span>Справочные цены и даты обновления из Croncopia</span></a><a class="tile" href="/procurement"><b>Закупки ВЛЗ</b><span>Условия и отправка предложения на закупку</span></a></section><section class="panel"><h2>ВЛЗ — работа с металлами</h2><p>На тестовом сайте собраны основные направления закупки, каталог сырья и справочные котировки из единого источника.</p><div class="stats"><div><strong>23</strong><small>серии источника</small></div><div><strong>1</strong><small>источник котировок</small></div><div><strong>USD</strong><small>валюта исходных данных</small></div></div></section>"""),
"/about": ("О заводе", """<section class="pagehead"><div class="eyebrow">О предприятии</div><h1>Воскресенский Литейный Завод</h1><p>Информация о предприятии и направлениях деятельности.</p></section><section class="panel"><h2>Профиль деятельности</h2><p>Закупка лома цветных и редких металлов, ферросплавов и металлосодержащего сырья. Работа с промышленными предприятиями, переработчиками и поставщиками.</p><p class="muted">Исторические сведения, производственные мощности, сертификаты и фотографии производства будут добавлены после согласования материалов завода.</p></section>"""),
"/metals": ("Ферросплавы", """<section class="pagehead"><div class="eyebrow">Каталог ВЛЗ · Раздел 1</div><h1>Ферросплавы</h1><p>Выберите позицию, чтобы открыть отдельную страницу с информацией о продукте.</p></section><section class="productgrid">"""+ "".join(f'<a class="productcard" href="/metals/{slug}"><img src="{photo}" alt="{name}" loading="lazy"><div class="productbody"><span class="productnum">{i:02d}</span><h2>{name}</h2><span class="productmore">Подробнее →</span></div></a>' for i,(slug,name,photo) in enumerate(FERROALLOYS,1)) + """</section>"""),
"/quotes": ("Биржевые котировки", """<section class="pagehead"><div class="eyebrow">Рыночная информация</div><h1>Котировки металлов</h1><p>Справочные агрегированные цены из единого источника Croncopia. Значения не являются офертой или гарантированной ценой сделки.</p></section><section class="panel"><div class="tablewrap"><table><thead><tr><th>Металл</th><th>Цена</th><th>Единица</th><th>Метка источника</th><th>Статус</th></tr></thead><tbody id="rows"><tr><td colspan="5">Загрузка котировок…</td></tr></tbody></table></div><p class="muted" id="source">Источник: Croncopia.</p><button class="btn" onclick="loadQuotes()">Обновить таблицу</button></section><script>async function loadQuotes(){const b=document.getElementById('rows');b.innerHTML='<tr><td colspan="5">Загрузка…</td></tr>';try{const r=await fetch('/api/quotes');const j=await r.json();b.innerHTML=j.quotes.map(q=>'<tr><td>'+q.metal+'</td><td class="price">'+(q.price==null?'Нет данных':Number(q.price).toLocaleString('ru-RU',{maximumFractionDigits:2})+' '+q.currency)+'</td><td>'+q.unit+'</td><td>'+(q.timestamp?new Date(q.timestamp).toLocaleString('ru-RU'):'—')+'</td><td>'+(q.status==='available'?'Доступна':'Нет данных')+'</td></tr>').join('');document.getElementById('source').textContent='Источник: Croncopia. Данные запрашиваются при открытии страницы; цены справочные.'}catch(e){b.innerHTML='<tr><td colspan="5">Не удалось получить данные. Повторите позже.</td></tr>'}}loadQuotes();setInterval(loadQuotes,300000);</script>"""),
"/procurement": ("Закупки", """<section class="pagehead"><div class="eyebrow">Поставщикам</div><h1>Закупка металлов и сырья</h1><p>ВЛЗ рассматривает предложения по лому цветных и редких металлов, ферросплавам и металлосодержащему сырью.</p></section><section class="panel"><h2>Что указать в предложении</h2><ul><li>Наименование металла и форма материала</li><li>Объём партии и местонахождение</li><li>Содержание основного элемента и примеси</li><li>Ориентировочная цена</li><li>Фотографии, паспорт качества или анализ</li></ul><p class="muted">Контактная форма и передача заявок будут подключены после согласования адреса электронной почты и правил обработки данных.</p><a class="btn" href="/contacts">Связаться с ВЛЗ</a></section>"""),
"/news": ("Новости", """<section class="pagehead"><div class="eyebrow">Новости</div><h1>Новости ВЛЗ</h1><p>Новости предприятия и отраслевые публикации.</p></section><section class="panel"><p>Раздел подготовлен. Публикации будут добавляться через административную панель после подключения управления контентом.</p></section>"""),
"/contacts": ("Контакты", """<section class="pagehead"><div class="eyebrow">Связаться с нами</div><h1>Контакты ВЛЗ</h1><p>По вопросам поставок металлолома, ферросплавов и сотрудничества.</p></section><section class="panel"><h2>Отдел закупок</h2><p>Телефон и электронная почта будут размещены после подтверждения актуальных контактных данных предприятия.</p><p class="muted">Пока это тестовая версия сайта. Не отправляйте через неё конфиденциальные документы.</p></section>""")
}
STYLE = """<style>.productgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.productcard{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:transform .18s,box-shadow .18s}.productcard:hover{transform:translateY(-3px);box-shadow:0 8px 24px #302c2618}.productcard img{display:block;width:100%;height:190px;object-fit:cover;background:#e6e0d7}.productbody{padding:16px 18px}.productnum{color:var(--copper);font-size:12px;font-weight:700}.productbody h2{font-size:18px;margin:8px 0 14px}.productmore{color:var(--copper);font-size:14px;font-weight:700}.detailgrid{display:grid;grid-template-columns:1.1fr 1fr;gap:20px;align-items:start}.detailphoto{background:white;border:1px solid var(--line);border-radius:16px;padding:14px}.detailphoto img{width:100%;height:360px;object-fit:contain;background:#f5f2ed}.detailphoto small{display:block;color:var(--muted);margin:10px 4px 2px}@media(max-width:700px){.productgrid{grid-template-columns:repeat(2,1fr);gap:12px}.productcard img{height:140px}.productbody{padding:12px}.productbody h2{font-size:16px}.detailgrid{grid-template-columns:1fr}.detailphoto img{height:260px}}
:root{--ink:#29251f;--muted:#77716a;--copper:#a96338;--cream:#f4f1eb;--line:#e5ded4}*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:16px Arial,sans-serif}header{background:#25231f;color:white;padding:18px max(22px,calc((100% - 1120px)/2));display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}.brand{font-weight:800;letter-spacing:.04em}.brand span{color:#d89a6c}nav{display:flex;gap:18px;flex-wrap:wrap}nav a{font-size:14px;color:#eee}a{color:inherit;text-decoration:none}main{max-width:1120px;margin:auto;padding:34px 22px}.hero,.pagehead{background:linear-gradient(120deg,#302c26,#62503e);color:white;border-radius:18px;padding:48px 38px;margin-bottom:24px}.eyebrow{color:#e2b18b;text-transform:uppercase;letter-spacing:.14em;font-size:12px}.hero h1,.pagehead h1{font-size:clamp(30px,5vw,52px);max-width:780px;line-height:1.08;margin:14px 0}.hero p,.pagehead p{color:#e8ded4;max-width:700px;line-height:1.6}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.btn{display:inline-block;background:var(--copper);color:white;padding:13px 18px;border:0;border-radius:8px;font-weight:700;cursor:pointer}.btn.secondary{background:transparent;border:1px solid #cbb29d}.panel,.tile{background:white;border:1px solid var(--line);border-radius:16px;padding:24px;margin:20px 0}.panel h2{margin-top:0}.panel p,.panel li{line-height:1.65}.muted,.tile span{color:var(--muted);line-height:1.5}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.tile{display:block;margin:0}.tile b,.tile span{display:block}.tile span{margin-top:8px;font-size:14px}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}.stats div{background:#faf8f5;border:1px solid var(--line);padding:18px;border-radius:12px}.stats strong{display:block;color:var(--copper);font-size:24px}.stats small{color:var(--muted)}.metalgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metal{padding:15px;background:#faf8f5;border:1px solid var(--line);border-radius:10px}.tablewrap{overflow:auto}table{border-collapse:collapse;width:100%;min-width:680px}th,td{text-align:left;padding:13px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:12px;text-transform:uppercase}td.price{font-weight:700;font-variant-numeric:tabular-nums}footer{background:#25231f;color:#ddd;padding:28px;text-align:center;font-size:13px}@media(max-width:700px){header{padding:16px 18px}nav{gap:12px}.hero,.pagehead{padding:32px 22px}.panel{padding:18px}.grid{grid-template-columns:1fr}.stats{grid-template-columns:1fr}.metalgrid{grid-template-columns:repeat(2,1fr)}}
</style>"""
def render_page_with_body(title: str, body: str):
    links=[("/", "Главная"),("/about","О заводе"),("/metals","Каталог металлов"),("/quotes","Котировки"),("/procurement","Закупки"),("/news","Новости"),("/contacts","Контакты")]
    nav="".join(f'<a href="{u}">{label}</a>' for u,label in links)
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — ВЛЗ</title>{STYLE}</head><body><header><a class="brand" href="/">ВЛЗ <span>●</span> ВОСКРЕСЕНСКИЙ ЛИТЕЙНЫЙ ЗАВОД</a><nav>{nav}</nav></header><main>{body}</main><footer>© Воскресенский Литейный Завод · Тестовая версия сайта</footer></body></html>"""

def render_page(path: str):
    title, body = PAGES.get(path, PAGES["/"])
    links=[("/", "Главная"),("/about","О заводе"),("/metals","Каталог металлов"),("/quotes","Котировки"),("/procurement","Закупки"),("/news","Новости"),("/contacts","Контакты")]
    nav="".join(f'<a href="{u}"'+(' aria-current="page"' if u==path else '')+f'>{label}</a>' for u,label in links)
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Воскресенский Литейный Завод</title>{STYLE}</head><body><header><a class="brand" href="/">ВЛЗ <span>●</span> ВОСКРЕСЕНСКИЙ ЛИТЕЙНЫЙ ЗАВОД</a><nav>{nav}</nav></header><main>{body}</main><footer>© Воскресенский Литейный Завод · Тестовая версия сайта</footer></body></html>"""
@app.get("/",response_class=HTMLResponse)
@app.get("/about",response_class=HTMLResponse)
@app.get("/metals",response_class=HTMLResponse)
@app.get("/quotes",response_class=HTMLResponse)
@app.get("/procurement",response_class=HTMLResponse)
@app.get("/news",response_class=HTMLResponse)
@app.get("/contacts",response_class=HTMLResponse)
def pages(request: Request):
    return HTMLResponse(render_page(request.url.path))
@app.get("/admin.html",response_class=HTMLResponse)
def admin():
    return HTMLResponse("""<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>ВЛЗ — администрирование</title><style>body{font:16px Arial;background:#f4f1eb;padding:24px;color:#24211d}main{max-width:680px;margin:auto;background:white;padding:24px;border-radius:16px}a{color:#98552f}</style><main><h1>ВЛЗ — тестовая панель</h1><p>Тестовый стенд. Управление закупочными ценами, заявками и новостями будет подключено отдельным этапом.</p><p><a href='/'>Вернуться на сайт</a></p><p><a href='/api/health'>Проверить сервер</a></p></main>""")
