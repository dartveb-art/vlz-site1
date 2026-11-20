from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import urllib.request, json
app=FastAPI(title="Воскресенский Литейный Завод")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
("ferromolybdenum-60","Ферромолибден 60","https://raw.githubusercontent.com/dartveb-art/vlz-site1/main/static/images/ferromolybdenum-60.jpg"),
("ferromolybdenum-50","Ферромолибден 50","https://raw.githubusercontent.com/dartveb-art/vlz-site1/main/static/images/ferromolybdenum-50.jpg"),
("ferromanganese-fmn78","Ферромарганец ФМн78","https://upload.wikimedia.org/wikipedia/commons/1/1d/Ferromangan%C3%A8se_m%C3%A9tal.jpg"),
("ferromanganese-fmn95","Ферромарганец ФМн95","https://upload.wikimedia.org/wikipedia/commons/8/8a/Ferromangan%C3%A8se_carbur%C3%A9.jpg"),
("ferrosilicon-fs75","Ферросилиций ФС75","https://www.za-refractories.com/uploads/2021/06/ferro-silicon-75.jpg"),
("ferrosilicomanganese-mns17","Ферросиликомарганец МнС17","https://www.brndistic.com/wp-content/uploads/2020/12/ferro-silico-manganese.jpg"),
]

HIGH_ALLOYS = [
("ei868","ЭИ868 (ХН60ВТ)",""),
("ei435","ЭИ435 (ХН78Т)",""),
("ei437","ЭИ437 (ХН77ТЮР)",""),
]

STAINLESS_ALLOYS = [
("nickel-n1-n3","Никель Н-1, Н-3",""),
("nichrome-x20n80","Нихром Х20Н80",""),
("nichrome-x15n60","Нихром Х15Н60",""),
]

OTHER_METALS = [
("molybdenum-piece","Молибден, кусок",""),
("molybdenum-wire","Молибден, проволока",""),
("molybdenum-turnings","Молибден, стружка",""),
]

def catalog_cards(items):
    return "".join(f'<a class="productcard" href="/metals/{slug}">'+(f'<img src="{photo}" alt="{name}" loading="lazy">' if photo else '<div class="photo-pending">Фото будет добавлено</div>')+f'<div class="productbody"><span class="productnum">{i:02d}</span><h2>{name}</h2><span class="productmore">Подробнее →</span></div></a>' for i,(slug,name,photo) in enumerate(items,1))

PAGES = {
"/": ("Главная", """<section class="hero"><div class="eyebrow">Промышленность · Металлургия · Закупки</div><h1>Воскресенский Литейный Завод</h1><p>Закупка лома цветных и редких металлов, ферросплавов и металлосодержащего сырья. Принимаем предложения от поставщиков и предприятий.</p><div class="actions"><a class="btn" href="/procurement">Предложить металл</a><a class="btn secondary" href="/quotes">Смотреть котировки</a></div></section><section class="grid"><a class="tile" href="/metals"><b>Каталог металлов</b><span>Основные цветные, драгоценные и редкие металлы</span></a><a class="tile" href="/quotes"><b>Биржевые ориентиры</b><span>Справочные цены и даты обновления из Croncopia</span></a><a class="tile" href="/procurement"><b>Закупки ВЛЗ</b><span>Условия и отправка предложения на закупку</span></a></section><section class="panel"><h2>ВЛЗ — работа с металлами</h2><p>На тестовом сайте собраны основные направления закупки, каталог сырья и справочные котировки из единого источника.</p><div class="stats"><div><strong>23</strong><small>серии источника</small></div><div><strong>1</strong><small>источник котировок</small></div><div><strong>USD</strong><small>валюта исходных данных</small></div></div></section>"""),
"/about": ("О заводе", """<section class="pagehead"><div class="eyebrow">О предприятии</div><h1>Воскресенский Литейный Завод</h1><p>Информация о предприятии и направлениях деятельности.</p></section><section class="panel"><h2>Профиль деятельности</h2><p>Закупка лома цветных и редких металлов, ферросплавов и металлосодержащего сырья. Работа с промышленными предприятиями, переработчиками и поставщиками.</p><p class="muted">Исторические сведения, производственные мощности, сертификаты и фотографии производства будут добавлены после согласования материалов завода.</p></section>"""),
"/metals": ("Каталог металлов", """<section class="pagehead"><div class="eyebrow">Каталог ВЛЗ</div><h1>Каталог металлов</h1><p>Выберите позицию, чтобы открыть отдельную страницу.</p></section><section id="ferroalloys"><h2>1. Ферросплавы</h2><div class="productgrid">"""+catalog_cards(FERROALLOYS)+"""</div></section><section id="high-alloys"><h2>2. Высочка</h2><div class="productgrid">"""+catalog_cards(HIGH_ALLOYS)+"""</div></section><section id="stainless"><h2>3. Нержавейка</h2><div class="productgrid">"""+catalog_cards(STAINLESS_ALLOYS)+"""</div></section><section id="other"><h2>4. Прочее</h2><div class="productgrid">"""+catalog_cards(OTHER_METALS)+"""</div></section>"""),
"/quotes": ("Биржевые котировки", """<section class="pagehead"><div class="eyebrow">Рыночная информация</div><h1>Котировки металлов</h1><p>Справочные агрегированные цены из единого источника Croncopia. Значения не являются офертой или гарантированной ценой сделки.</p></section><section class="panel"><div class="tablewrap"><table><thead><tr><th>Металл</th><th>Цена</th><th>Единица</th><th>Метка источника</th><th>Статус</th></tr></thead><tbody id="rows"><tr><td colspan="5">Загрузка котировок…</td></tr></tbody></table></div><p class="muted" id="source">Источник: Croncopia.</p><button class="btn" onclick="loadQuotes()">Обновить таблицу</button></section><script>async function loadQuotes(){const b=document.getElementById('rows');b.innerHTML='<tr><td colspan="5">Загрузка…</td></tr>';try{const r=await fetch('/api/quotes');const j=await r.json();b.innerHTML=j.quotes.map(q=>'<tr><td>'+q.metal+'</td><td class="price">'+(q.price==null?'Нет данных':Number(q.price).toLocaleString('ru-RU',{maximumFractionDigits:2})+' '+q.currency)+'</td><td>'+q.unit+'</td><td>'+(q.timestamp?new Date(q.timestamp).toLocaleString('ru-RU'):'—')+'</td><td>'+(q.status==='available'?'Доступна':'Нет данных')+'</td></tr>').join('');document.getElementById('source').textContent='Источник: Croncopia. Данные запрашиваются при открытии страницы; цены справочные.'}catch(e){b.innerHTML='<tr><td colspan="5">Не удалось получить данные. Повторите позже.</td></tr>'}}loadQuotes();setInterval(loadQuotes,300000);</script>"""),
"/procurement": ("Закупки", """<section class="pagehead"><div class="eyebrow">Поставщикам</div><h1>Закупка металлов и сырья</h1><p>ВЛЗ рассматривает предложения по лому цветных и редких металлов, ферросплавам и металлосодержащему сырью.</p></section><section class="panel"><h2>Что указать в предложении</h2><ul><li>Наименование металла и форма материала</li><li>Объём партии и местонахождение</li><li>Содержание основного элемента и примеси</li><li>Ориентировочная цена</li><li>Фотографии, паспорт качества или анализ</li></ul><p class="muted">Контактная форма и передача заявок будут подключены после согласования адреса электронной почты и правил обработки данных.</p><a class="btn" href="/contacts">Связаться с ВЛЗ</a></section>"""),
"/news": ("Новости", """<section class="pagehead"><div class="eyebrow">Новости</div><h1>Новости ВЛЗ</h1><p>Новости предприятия и отраслевые публикации.</p></section><section class="panel"><p>Раздел подготовлен. Публикации будут добавляться через административную панель после подключения управления контентом.</p></section>"""),
"/contacts": ("Контакты", """<section class="pagehead"><div class="eyebrow">Связаться с нами</div><h1>Контакты ВЛЗ</h1><p>По вопросам поставок металлолома, ферросплавов и сотрудничества.</p></section><section class="panel"><h2>Отдел закупок</h2><p>Телефон и электронная почта будут размещены после подтверждения актуальных контактных данных предприятия.</p><p class="muted">Пока это тестовая версия сайта. Не отправляйте через неё конфиденциальные документы.</p></section>""")
}
STYLE = """<style>
:root{--ink:#22272a;--muted:#6e777a;--line:#e4e7e6;--paper:#f5f6f4;--white:#fff;--copper:#b87349;--copper-dark:#8e5234;--deep:#20282b;--shadow:0 18px 48px rgba(24,32,34,.09)}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
a{color:inherit;text-decoration:none}
header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.96);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:16px max(22px,calc((100% - 1180px)/2));display:flex;align-items:center;justify-content:space-between;gap:24px;box-shadow:0 4px 18px rgba(20,30,32,.035)}
.brand{font-weight:850;letter-spacing:.045em;font-size:14px;line-height:1.25;white-space:nowrap}.brand span{color:var(--copper);font-size:17px;margin:0 5px}
nav{display:flex;gap:clamp(10px,1.7vw,23px);flex-wrap:wrap;align-items:center}nav a{font-size:12px;color:#4d5659;font-weight:750;letter-spacing:.035em;transition:color .2s}nav a:hover,nav a[aria-current=page]{color:var(--copper-dark)}
main{max-width:1180px;margin:auto;padding:34px 22px 70px}
.hero,.pagehead{position:relative;overflow:hidden;background:linear-gradient(118deg,#202a2d 0%,#303c3e 60%,#4a4037 100%);color:white;border-radius:5px;padding:clamp(34px,6vw,72px);margin:0 0 26px;box-shadow:var(--shadow)}
.hero:after,.pagehead:after{content:"";position:absolute;width:470px;height:470px;right:-130px;top:-220px;border:1px solid rgba(221,185,150,.22);border-radius:50%;box-shadow:0 0 0 52px rgba(221,185,150,.045),0 0 0 105px rgba(221,185,150,.035),0 0 0 158px rgba(221,185,150,.025);pointer-events:none}
.eyebrow{position:relative;z-index:1;color:#dfb18c;text-transform:uppercase;letter-spacing:.17em;font-size:11px;font-weight:800}
.hero h1,.pagehead h1{position:relative;z-index:1;font-size:clamp(34px,5.5vw,64px);max-width:800px;line-height:1.04;letter-spacing:-.045em;margin:17px 0 18px;font-weight:780}
.hero p,.pagehead p{position:relative;z-index:1;color:#d9e0de;max-width:720px;line-height:1.75;font-size:clamp(15px,1.6vw,18px)}
.actions{position:relative;z-index:1;display:flex;gap:12px;flex-wrap:wrap;margin-top:27px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;background:linear-gradient(135deg,var(--copper),var(--copper-dark));color:white;padding:13px 20px;border:1px solid transparent;border-radius:3px;font-size:13px;font-weight:800;letter-spacing:.02em;cursor:pointer;transition:transform .2s,box-shadow .2s}.btn:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(184,115,73,.25)}.btn.secondary{background:transparent;border-color:rgba(255,255,255,.45);color:#fff}
.panel,.tile{background:var(--white);border:1px solid var(--line);border-radius:5px;padding:clamp(20px,3vw,30px);margin:20px 0;box-shadow:0 8px 28px rgba(30,40,40,.035)}.panel h2{margin:0 0 14px;font-size:clamp(22px,3vw,30px);letter-spacing:-.025em}.panel p,.panel li{line-height:1.75;color:#505a5d}.muted,.tile span{color:var(--muted);line-height:1.65}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.tile{display:block;margin:0;position:relative;transition:transform .2s,border-color .2s}.tile:hover{transform:translateY(-3px);border-color:#c99a78}.tile b,.tile span{display:block}.tile b{font-size:18px}.tile span{margin-top:8px;font-size:13px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}.stats div{background:#f8f7f4;border:1px solid var(--line);padding:18px;border-radius:4px}.stats strong{display:block;color:var(--copper-dark);font-size:25px;line-height:1.2}.stats small{color:var(--muted);font-size:12px}
.metalgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metal{padding:15px;background:#faf9f6;border:1px solid var(--line);border-radius:4px}
.tablewrap{overflow:auto;border:1px solid var(--line);border-radius:4px}table{border-collapse:collapse;width:100%;min-width:680px;background:#fff}th,td{text-align:left;padding:14px 16px;border-bottom:1px solid var(--line)}th{background:#f5f3ef;color:#6e777a;font-size:11px;text-transform:uppercase;letter-spacing:.08em}td{font-size:14px}td.price{font-weight:800;font-variant-numeric:tabular-nums;color:var(--copper-dark)}
.photo-pending{display:grid;place-items:center;height:205px;background:linear-gradient(135deg,#ecebe7,#d9d8d2);color:#77716a;font-size:13px;text-align:center;letter-spacing:.04em}.detailphoto .photo-pending{height:330px}
#high-alloys,#stainless,#other{margin-top:44px}
.productgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.productcard{display:block;min-width:0;background:#fff;border:1px solid var(--line);border-radius:5px;overflow:hidden;transition:transform .22s,box-shadow .22s,border-color .22s}.productcard:hover{transform:translateY(-4px);box-shadow:var(--shadow);border-color:#c99a78}
.productcard img{display:block;width:100%;height:205px;object-fit:cover;background:#e8e5df;transition:transform .4s}.productcard:hover img{transform:scale(1.025)}
.productbody{position:relative;padding:17px 19px 19px}.productnum{display:inline-block;color:var(--copper-dark);font-size:11px;font-weight:850;letter-spacing:.1em}.productbody h2{font-size:18px;line-height:1.3;margin:7px 0 15px;letter-spacing:-.02em}.productmore{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--line);padding-top:12px;color:var(--copper-dark);font-size:12px;font-weight:800}
.detailgrid{display:grid;grid-template-columns:1.08fr 1fr;gap:22px;align-items:start}.detailphoto{background:white;border:1px solid var(--line);border-radius:5px;padding:14px;box-shadow:0 8px 28px rgba(30,40,40,.04)}.detailphoto img{display:block;width:100%;height:370px;object-fit:contain;background:#f7f6f3}.detailphoto small{display:block;color:var(--muted);margin:10px 4px 2px;font-size:12px}.detailgrid .panel{margin:0}
footer{background:#20282b;color:#d6ddda;padding:27px 22px;text-align:center;font-size:12px;letter-spacing:.025em}
@media(max-width:900px){header{align-items:flex-start;flex-direction:column;gap:12px}nav{gap:14px}.productgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.grid{grid-template-columns:1fr 1fr}}
@media(max-width:700px){html{scroll-padding-top:130px}header{padding:13px 18px}.brand{white-space:normal;font-size:12px}nav{width:100%;gap:8px 15px}nav a{font-size:11px}main{padding:20px 14px 48px}.hero,.pagehead{padding:34px 23px;border-radius:4px}.hero h1,.pagehead h1{font-size:clamp(32px,9vw,46px)}.hero:after,.pagehead:after{right:-300px}.panel{padding:18px}.grid{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}.metalgrid{grid-template-columns:repeat(2,1fr)}.productgrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.productcard img{height:145px}.productbody{padding:12px}.productbody h2{font-size:15px}.productmore{font-size:11px}.photo-pending{height:145px;font-size:11px}.detailgrid{grid-template-columns:1fr;gap:14px}.detailphoto img{height:260px}.detailphoto .photo-pending{height:240px}th,td{padding:11px 12px}}
@media(max-width:380px){.productgrid{grid-template-columns:1fr}.productcard img{height:190px}.stats{grid-template-columns:1fr}}
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
@app.get("/metals/{slug}",response_class=HTMLResponse)
def ferro_detail(slug: str):
    item=next((x for x in FERROALLOYS + HIGH_ALLOYS + STAINLESS_ALLOYS + OTHER_METALS if x[0]==slug),None)
    if not item:
        return HTMLResponse(render_page("/metals"),status_code=404)
    _,name,photo=item
    category="Высочка" if item in HIGH_ALLOYS else ("Нержавейка" if item in STAINLESS_ALLOYS else ("Прочее" if item in OTHER_METALS else "Ферросплавы"))
    photo_html=f'<img src="{photo}" alt="{name}"><small>Фактический вид партии может отличаться.</small>' if photo else '<div class="photo-pending">Фото будет добавлено</div>'
    body=f"""<section class="pagehead"><div class="eyebrow"><a href="/metals">Каталог / {category}</a></div><h1>{name}</h1><p>Карточка товарной позиции Воскресенского Литейного Завода.</p></section><section class="detailgrid"><div class="detailphoto">{photo_html}</div><div class="panel"><h2>{name}</h2><p>Позиция каталога ВЛЗ. Раздел «{category}».</p><p class="muted">Точная химическая спецификация, фракция, наличие и условия поставки уточняются по документам конкретной партии.</p><a class="btn" href="/procurement">Запросить условия поставки</a><p><a href="/metals">← Вернуться в каталог</a></p></div></section>"""
    return HTMLResponse(render_page_with_body(name,body))

@app.get("/admin.html",response_class=HTMLResponse)
def admin():
    return HTMLResponse("""<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>ВЛЗ — администрирование</title><style>body{font:16px Arial;background:#f4f1eb;padding:24px;color:#24211d}main{max-width:680px;margin:auto;background:white;padding:24px;border-radius:16px}a{color:#98552f}</style><main><h1>ВЛЗ — тестовая панель</h1><p>Тестовый стенд. Управление закупочными ценами, заявками и новостями будет подключено отдельным этапом.</p><p><a href='/'>Вернуться на сайт</a></p><p><a href='/api/health'>Проверить сервер</a></p></main>""")
