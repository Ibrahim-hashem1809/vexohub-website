from pathlib import Path
import json
from html import escape

root = Path(__file__).resolve().parents[1]
stories = root / "stories"
catalog = json.loads((stories / "stories.json").read_text())
story = catalog[0]
fb = "https://www.facebook.com/profile.php?id=61596727980276"
minutes = max(1, round(sum(len(p.split()) for p in story["paragraphs"]) / 180))

def header(prefix):
    return f"""<a class="skip" href="#main">انتقل إلى المحتوى</a>
<header class="header"><div class="wrap nav">
<a class="brand" href="{prefix}"><img src="{prefix}assets/brand.png" width="53" height="53" alt=""><span><b>حكاية تانية</b><small>روايات وقصص عربية</small></span></a>
<nav aria-label="القائمة الرئيسية"><a href="{prefix}#library">المكتبة</a><a href="{fb}" target="_blank" rel="noopener noreferrer">تابعنا</a></nav>
</div></header>"""

def head(title, description, suffix, prefix):
    return f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#080f1b"><link rel="canonical" href="https://vexohub.app/stories/{suffix}">
<meta property="og:type" content="{'article' if suffix else 'website'}"><meta property="og:locale" content="ar_AR">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="https://vexohub.app/stories/{suffix}">
<meta property="og:image" content="https://vexohub.app/stories/assets/{escape(story["image"], quote=True)}">
<meta property="og:image:alt" content="{escape(story["imageAlt"], quote=True)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}assets/brand.png"><link rel="stylesheet" href="{prefix}assets/style.css">
<script src="{prefix}assets/app.js" defer></script></head><body>"""

def footer():
    return f"""<footer><div class="wrap"><span>حكاية تانية · كل نهاية وراها حكاية تانية</span>
<div class="footer-links"><a href="{fb}" target="_blank" rel="noopener noreferrer">Facebook</a></div></div></footer>"""

def reading_minutes(item):
    return max(1, round(sum(len(p.split()) for p in item["paragraphs"]) / 180))

def story_card(item):
    return f"""<article class="story-card" data-story-card="{escape(item['id'])}" data-category="{escape(item['category'])}" data-search="{escape(item['title']+' '+item['category']+' '+item.get('keywords',''))}">
<a href="{escape(item['id'])}/"><img class="story-image" src="assets/{escape(item['image'])}" alt="{escape(item['imageAlt'])}" width="1536" height="1024" loading="lazy"></a>
<div class="card-body"><div class="meta"><span class="tag">{escape(item['category'])}</span><span>{reading_minutes(item)} دقائق قراءة</span><span>قصة قصيرة</span></div>
<h3><a href="{escape(item['id'])}/">{escape(item['title'])}</a></h3><p>{escape(item['description'])}</p>
<div class="card-bottom"><a class="button primary" href="{escape(item['id'])}/">اقرأ القصة</a><button class="quiet" type="button" data-save="{escape(item['id'])}" aria-pressed="false">احفظ لوقت لاحق</button></div></div></article>"""

cards_html = "".join(story_card(item) for item in catalog)
category_options = "".join(f'<option value="{escape(category, quote=True)}">{escape(category)}</option>' for category in dict.fromkeys(item["category"] for item in catalog))

description = escape(story["description"])
index = head("حكاية تانية | روايات وقصص عربية", "قصص عربية مكتملة من الرومانسية والتشويق والرعب. اكتشف حكايتك القادمة واحفظها لوقت لاحق.", "", "./") + header("./")
index += f"""
<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div><p class="eyebrow">حكايات قصيرة. أثر يبقى طويلًا.</p>
<h1>أغلق ضجيج العالم.<br><em>وافتح حكاية.</em></h1>
<p class="lead">ثمّة عوالم لا تحتاج إلى سفر… فقط إلى صفحة أولى. اكتشف قصصًا عربية من الحب والتشويق والغموض، ودع النهاية تفاجئك.</p>
<div class="actions"><a class="button primary" href="{story['id']}/">ابدأ القراءة</a><a class="button" href="#library">تصفّح المكتبة</a></div>
<p class="notice">كل نهاية وراها حكاية تانية.</p></div>
<a class="hero-art" href="{story['id']}/" aria-label="اقرأ قصة {escape(story['title'])}">
<img src="assets/{story['image']}" width="1536" height="1024" alt="{escape(story['imageAlt'])}" fetchpriority="high">
<div class="art-note"><strong>{escape(story['title'])}</strong><span>{escape(story['category'])} · {minutes} دقائق</span></div></a>
</div></section>
<section class="library" id="library"><div class="wrap">
<div class="section-heading"><div><p class="eyebrow">على رفّ الحكايات</p><h2>اختر حكايتك القادمة</h2></div><p data-count aria-live="polite">{len(catalog)} قصص للقراءة</p></div>
<div class="filters" role="search" aria-label="البحث في القصص">
<div class="search"><label class="sr-only" for="search">ابحث عن قصة</label><input id="search" data-search type="search" placeholder="ابحث عن عنوان أو حكاية…" autocomplete="off"></div>
<label class="sr-only" for="category">تصنيف القصة</label><select id="category" data-category><option value="">كل التصنيفات</option>{category_options}</select>
<button class="button" type="button" data-saved-filter aria-pressed="false">المحفوظات</button></div>
<div class="cards"><div class="story-list">
{cards_html}
<p class="empty" data-empty hidden></p>
<p class="live" data-status role="status"></p>
</div><aside class="editor-note"><span class="ornament" aria-hidden="true">“</span><p class="eyebrow">حكايات تستحق وقتك</p><h3>حبّ يعبر المحن،<br>وغموض ينتظر قارئه.</h3>
<p>اختر القصة التي تناسب مزاجك. تابع الصفحة لتعرف موعد وصول حكايات جديدة إلى المكتبة.</p>
<a class="button" href="{fb}" target="_blank" rel="noopener noreferrer">تابع حكاية تانية</a>
<p>المحفوظات تُحفظ على متصفحك، دون الحاجة إلى إنشاء حساب.</p></aside></div>
</div></section></main>""" + footer() + "</body></html>"
(stories / "index.html").write_text(index)

for story in catalog:
    minutes = reading_minutes(story)
    parts = []
    for paragraph in story["paragraphs"]:
        if paragraph == "***":
            parts.append("<hr>")
        else:
            cls = ' class="dialogue"' if paragraph.startswith("—") else ""
            parts.append(f"<p{cls}>{escape(paragraph)}</p>")
    reader = head(story["title"] + " | حكاية تانية", story["description"], story["id"] + "/", "../").replace("<body>", '<body class="light" data-reader>') + header("../")
    reader += f"""
    <main id="main"><section class="wrap reader-head">
    <a class="back" href="../#library">العودة إلى مكتبة الحكايات</a>
    <h1>{escape(story['title'])}</h1><div class="meta"><span class="tag">{escape(story['category'])}</span><span>{minutes} دقائق قراءة</span><span>قصة قصيرة</span></div>
    <p class="notice">{'تحتوي هذه القصة على مشاهد رعب وجريمة.' if story['category'] == 'رعب' else 'قصة رومانسية مكتملة تتضمن مواقف تشويق واعتداء.'}</p>
    <img class="reader-cover" src="../assets/{story['image']}" width="1536" height="1024" alt="{escape(story['imageAlt'])}">
    </section>
    <div class="toolbar"><div class="wrap tools" role="group" aria-label="أدوات القراءة">
    <div class="tool-group"><button class="quiet" type="button" data-size="-1" aria-label="تصغير الخط">خط أصغر</button><button class="quiet" type="button" data-size="1" aria-label="تكبير الخط">خط أكبر</button><button class="quiet" type="button" data-theme aria-label="تفعيل الخلفية الليلية">الخلفية: نهارية ☀</button></div>
    <div class="tool-group"><button class="quiet" type="button" data-save="{story['id']}" aria-pressed="false">احفظ لوقت لاحق</button><button class="quiet" type="button" data-share>شارك القصة</button></div>
    </div><div class="progress" role="progressbar" aria-label="تقدّم قراءة القصة" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span data-progress></span></div></div>
    <article class="wrap story-text" data-article aria-label="نص قصة {escape(story['title'])}">{"".join(parts)}</article>
    <div class="wrap ending"><p class="eyebrow">تمّت الحكاية</p><h2>ما زال على الرفّ مكان لحكاية أخرى.</h2>
    <p>لو عجبتك القصة، تابع صفحة «حكاية تانية» ليصلك كل جديد… فهناك دائمًا حكاية أخرى تنتظرك. 📖</p>
    <div class="actions" style="justify-content:center"><a class="button primary" href="{fb}" target="_blank" rel="noopener noreferrer">تابع الصفحة</a><a class="button" href="../#library">العودة للمكتبة</a></div><p class="live" data-status role="status"></p></div></main>""" + footer() + "</body></html>"
    (stories / story["id"]).mkdir(exist_ok=True)
    (stories / story["id"] / "index.html").write_text(reader)
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += '  <url><loc>https://vexohub.app/stories/</loc><priority>1.0</priority></url>\n'
for item in catalog:
    sitemap += f'  <url><loc>https://vexohub.app/stories/{escape(item["id"])}/</loc><priority>0.8</priority></url>\n'
(stories / "sitemap.xml").write_text(sitemap + '</urlset>\n')
