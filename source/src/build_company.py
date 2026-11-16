#!/usr/bin/env python3
"""Generates company-site/dist (LoveStrong). Run: python3 src/build_company.py"""
import os, shutil, time, json, re, html as _html
from datetime import date
VER = str(int(time.time()))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.environ.get("OUT_DIR") or os.path.join(ROOT, "company-site", "dist")
PREFIX = os.environ.get("PATH_PREFIX", "")  # 例: /lovestrong（GitHub Pagesのプロジェクトサイト用）
SRC_ASSETS = os.path.join(ROOT, "psyqyo-site", "dist", "assets")
MAIL = "info@example.com"  # TODO: 本当のメールアドレスに直す

BASE = os.environ.get("BASE_URL") or "https://example.com"  # TODO: 公開URLに直す
OG_IMG = BASE + "/assets/og-image.jpg"
ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": "LoveStrong", "url": BASE + "/",
       "description": "ホームページとLPの制作チーム。愛媛大学のサークルのメンバーが元になって活動しています。", "logo": BASE + "/assets/favicon.svg"}

def plain(t):
    return _html.unescape(re.sub(r"<[^>]+>", "", t))

NAV = [("/services/", "制作内容"), ("/works/", "制作実績"), ("/flow/", "ご依頼の流れ"), ("/company/", "チーム概要")]

def header(active, photo):
    items = "".join(f'<a{" class=\"active\"" if h == active else ""} href="{h}">{t}</a>' for h, t in NAV)
    cls = "site-header on-photo" if photo else "site-header solid"
    return f'''<header class="{cls}"><div class="shell header-inner">
<a class="wordmark" href="/"><span class="company-logo">LoveStrong</span></a>
<button class="menu-button" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="メニュー"><span class="bars" aria-hidden="true"></span></button>
<nav class="main-nav" id="main-nav" aria-label="メインナビゲーション">{items}<a class="nav-trial" href="/contact/">お問い合わせ</a></nav>
</div></header>'''

FOOTER = f'''<footer class="site-footer"><div class="shell">
<div class="footer-top"><div class="footer-brand"><span class="company-logo">LoveStrong</span><p>ホームページ・LP制作チーム</p></div>
<div class="footer-cols">
<a href="/services/">制作内容</a><a href="/works/">制作実績</a><a href="/flow/">ご依頼の流れ</a><a href="/company/">チーム概要</a><a href="/contact/">お問い合わせ</a><a href="/privacy/">個人情報の取り扱い</a><a href="mailto:{MAIL}">{MAIL}</a>
</div></div>
<div class="footer-bottom">© <span class="current-year">2026</span> LoveStrong</div>
</div></footer>'''

def cta(title="まずは、ご相談ください。", text="ホームページやLPのこと、どんなことでもご連絡ください。"):
    return f'<section class="cta"><div class="shell cta-inner"><div><h2>{title}</h2><p>{text}</p></div><a class="button button-paper" href="/contact/">お問い合わせ</a></div></section>'

def page(path, title, desc, body, active="", photo=False, faq=None, crumb=None, extra=None, noindex=False):
    url = BASE + path
    ld = []
    if path == "/":
        ld.append({"@context": "https://schema.org", **ORG, "sameAs": []})
        ld[0].pop("sameAs")
        ld.append({"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "LoveStrong", "inLanguage": "ja", "publisher": {"@id": BASE + "/#org"}})
    if extra:
        ld.append(extra)
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": plain(b)}} for a, b in faq]})
    if crumb:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u2} for i, (n, u2) in enumerate([("LoveStrong", BASE + "/")] + crumb)]})
    ld_html = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>\n" for x in ld)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">'
    html = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#8f1a20">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LoveStrong">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMG}">
<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
{ld_html}</head>
<body>
{header(active, photo)}
<main>
{body}
</main>
{FOOTER}
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
'''
    out = os.path.join(DIST, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)

FAQ_TOP = [
("LoveStrongは、どんなチームですか？","ホームページとLP（ランディングページ）をつくるチームです。愛媛大学のサークルのメンバーが元になって活動しています。"),
("どんなものをつくってもらえますか？","会社やお店のホームページ、サービス紹介のページ、LPなどです。まだ形が決まっていない段階でも、ご相談ください。"),
("費用はいくらですか？","ホームページの制作は無料です。公開したあとの保守（運用・修正のサポート）を、月5,000円でお受けしています。くわしくは、メールでご相談ください。"),
("問い合わせ先を教えてください。",f'メールでご連絡ください。宛先は <a class="text-link" href="mailto:{MAIL}">{MAIL}</a> です。'),
]

# ------------------------------------------------------------ top
top = f'''
<section class="hero"><div class="shell hero-inner">
<h1>無料でホームページを<br>作成します！！</h1>
<p class="hero-lead">ホームページ・LP制作チーム　LoveStrong</p>
<div class="hero-actions"><a class="button button-orange" href="/services/">制作内容を見る</a><a class="button button-line" href="/contact/">お問い合わせ</a></div>
</div></section>

<section class="section"><div class="shell prose">
<h2>LoveStrongとは</h2>
<p>LoveStrongは、ホームページとLPをつくるチームです。愛媛大学のサークルのメンバーが元になって活動しています。</p>
<p>会社やお店、サービスの魅力が、見る人にきちんと伝わるページを、一緒に考えながらつくります。</p>
</div></section>

<section class="section section-white"><div class="shell prose">
<h2>大事にしていること</h2>
<p>ページは、つくって終わりではありません。見てもらって、問い合わせにつながってはじめて役に立ちます。</p>
<p>だから、見た目だけでなく、何を伝えたいか、誰に見てほしいかを、最初にしっかり伺います。</p>
</div></section>

<section class="section section-white" id="business"><div class="shell">
<h2>制作内容</h2>
<p class="lead">ホームページとLPを中心に、Webページの制作を行っています。</p>
<dl class="profile">
<div><dt>ホームページ</dt><dd>会社、お店、サークルや団体のホームページ。</dd></div>
<div><dt>LP</dt><dd>商品やサービス、イベントを紹介する、1ページ完結のページ。</dd></div>
<div><dt>料金</dt><dd>制作は無料です。公開後の保守は、月5,000円です。</dd></div>
</dl>
<p style="margin-top:40px"><a class="button button-orange" href="/services/">くわしく見る</a></p>
</div></section>

<section class="section"><div class="shell">
<h2>制作実績</h2>
<p class="lead">いま載せているのは、このサイトです。これから、手がけたものを追加していきます。</p>
<p style="margin-top:24px"><a class="button button-orange" href="/works/">制作実績を見る</a></p>
</div></section>

<section class="section section-white"><div class="shell prose">
<h2>よくある質問</h2>
{"".join(f"<details><summary>{a}</summary><p>{b}</p></details>" for a, b in FAQ_TOP)}
</div></section>

{cta()}
'''
page("/", "LoveStrong｜ホームページ・LP制作チーム", "LoveStrongは、ホームページとLPをつくるチームです。愛媛大学のサークルのメンバーが元になって活動しています。", top, "", photo=True, faq=FAQ_TOP)

# ------------------------------------------------------------ company
company = f'''
<section class="page-hero"><div class="shell"><h1>チーム概要</h1><p>LoveStrongについて。</p></div></section>
<section class="section"><div class="shell">
<h2>大事にしていること</h2>
<p class="lead">伝えたいことが、見る人にきちんと届くページをつくる。</p>
<dl class="profile">
<div><dt>聞く</dt><dd>何を伝えたいか、誰に見てほしいかを、最初にしっかり伺う。</dd></div>
<div><dt>わかりやすさ</dt><dd>見た目だけでなく、読みやすさと使いやすさを大事にする。</dd></div>
<div><dt>誠実</dt><dd>できることと、できないことを、正直にお伝えする。</dd></div>
<div><dt>改善</dt><dd>公開したあとも、使われ方を見ながら直していく。</dd></div>
</dl>
</div></section>
<section class="section section-white"><div class="shell">
<h2>チーム情報</h2>
<dl class="profile" style="margin-top:0">
<div><dt>チーム名</dt><dd>LoveStrong</dd></div>
<div><dt>成り立ち</dt><dd>愛媛大学のサークルのメンバーが元になって活動しています。</dd></div>
<div><dt>事業内容</dt><dd>ホームページ・LPの制作、公開後の保守</dd></div>
<div><dt>お問い合わせ</dt><dd><a class="text-link" href="mailto:{MAIL}">{MAIL}</a></dd></div>
</dl>
</div></section>
{cta()}
'''
page("/company/", "チーム概要｜LoveStrong", "ホームページ・LP制作チーム LoveStrong のチーム概要。", company, "/company/", crumb=[("チーム概要", BASE + "/company/")])

# ------------------------------------------------------------ contact
contact = f'''
<div class="shell trial-wrap">
<h1>お問い合わせ</h1>
<p class="lead">ホームページやLPの制作のご相談など、お気軽にご連絡ください。</p>
<dl class="profile" style="margin-top:40px">
<div><dt>メール</dt><dd><a class="text-link" href="mailto:{MAIL}">{MAIL}</a></dd></div>
<div><dt>チーム名</dt><dd>LoveStrong</dd></div>
</dl>
<p class="form-note" style="margin-top:24px">内容を確認のうえ、順次ご返信いたします。</p>
</div>
'''
page("/contact/", "お問い合わせ｜LoveStrong", "LoveStrongへのお問い合わせ。", contact, "", crumb=[("お問い合わせ", BASE + "/contact/")])

# ------------------------------------------------------------ services
services = f'''
<section class="page-hero"><div class="shell"><h1>制作内容</h1><p>ホームページとLPを中心に、Webページをつくります。</p></div></section>
<section class="section"><div class="shell">
<dl class="profile" style="margin-top:0">
<div><dt>ホームページ</dt><dd>会社、お店、サークルや団体のホームページ。複数ページの構成にも対応します。</dd></div>
<div><dt>LP</dt><dd>商品やサービス、イベントを紹介する、1ページ完結のページ。問い合わせや申し込みにつなげる作りにします。</dd></div>
<div><dt>スマホ対応</dt><dd>パソコンでもスマートフォンでも見やすい形にします。</dd></div>
<div><dt>制作費</dt><dd>無料です。</dd></div>
<div><dt>保守</dt><dd>公開後の運用と修正のサポートです。月5,000円です。</dd></div>
<div><dt>ご相談</dt><dd>何をつくればいいか決まっていない段階でも、内容の整理から一緒に行います。</dd></div>
</dl>
<p style="margin-top:40px"><a class="button button-orange" href="/contact/">制作のご相談</a></p>
</div></section>
{cta("まずは、ご相談ください。", "ホームページやLPのこと、どんなことでもご連絡ください。")}
'''
page("/services/", "制作内容｜LoveStrong", "LoveStrongの制作内容。ホームページとLPの制作。", services, "/services/", crumb=[("制作内容", BASE + "/services/")])

# ------------------------------------------------------------ works
works = f'''
<section class="page-hero"><div class="shell"><h1>制作実績</h1><p>手がけたものを、ここに載せていきます。</p></div></section>
<section class="section"><div class="shell">
<dl class="profile" style="margin-top:0">
<div><dt>このサイト</dt><dd>LoveStrongのホームページです。スマホでもパソコンでも見やすい形にしています。</dd></div>
</dl>
<p style="margin-top:40px">制作実績は、これから追加していきます。</p>
</div></section>
{cta()}
'''
page("/works/", "制作実績｜LoveStrong", "LoveStrongの制作実績。", works, "/works/", crumb=[("制作実績", BASE + "/works/")])

# ------------------------------------------------------------ flow
flow = f'''
<section class="page-hero"><div class="shell"><h1>ご依頼の流れ</h1><p>ご相談から公開までの進め方です。</p></div></section>
<section class="section"><div class="shell">
<dl class="profile" style="margin-top:0">
<div><dt>1. ご相談</dt><dd>メールでご連絡ください。</dd></div>
<div><dt>2. ヒアリング</dt><dd>伝えたいこと、見てほしい人、ご希望を伺います。</dd></div>
<div><dt>3. ご提案</dt><dd>つくる内容と進め方をご提案します。制作は無料です。保守は月5,000円です。ご納得いただいてから進めます。</dd></div>
<div><dt>4. 制作・確認</dt><dd>実際の画面を見ていただきながら、直していきます。</dd></div>
<div><dt>5. 公開・保守</dt><dd>公開したあとは、保守（月5,000円）で、運用と修正をサポートします。</dd></div>
</dl>
<p style="margin-top:40px"><a class="button button-orange" href="/contact/">お問い合わせ</a></p>
</div></section>
{cta()}
'''
page("/flow/", "ご依頼の流れ｜LoveStrong", "LoveStrongへのご依頼の流れ。", flow, "/flow/", crumb=[("ご依頼の流れ", BASE + "/flow/")])

# ------------------------------------------------------------ privacy
privacy = f'''
<section class="page-hero"><div class="shell"><h1>個人情報の取り扱い</h1><p>お問い合わせでお預かりする情報について。</p></div></section>
<section class="section"><div class="shell prose">
<h2>お問い合わせ</h2>
<p>お問い合わせでお送りいただいたお名前、メールアドレス、お問い合わせ内容は、ご返信と、お問い合わせへの対応のために使います。</p>
<h2 style="margin-top:56px">窓口</h2>
<p>LoveStrong　<a class="text-link" href="mailto:{MAIL}">{MAIL}</a></p>
</div></section>
'''
page("/privacy/", "個人情報の取り扱い｜LoveStrong", "LoveStrongの個人情報の取り扱い。", privacy, "", crumb=[("個人情報の取り扱い", BASE + "/privacy/")])

# ------------------------------------------------------------ assets
os.makedirs(os.path.join(DIST, "assets"), exist_ok=True)
shutil.copy(os.path.join(ROOT, "src", "company.css"), os.path.join(DIST, "assets", "site.css"))
for f in ("og-image.jpg",):
    shutil.copy(os.path.join(SRC_ASSETS, f), os.path.join(DIST, "assets", f))

# ------------------------------------------------------------ seo files
open(os.path.join(DIST, "assets", "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#8f1a20"/><text x="32" y="46" font-size="40" font-family="sans-serif" font-weight="700" text-anchor="middle" fill="#fff">L</text></svg>')
today = date.today().isoformat()
urls = [("/", "1.0"), ("/services/", "0.9"), ("/works/", "0.8"), ("/flow/", "0.8"), ("/company/", "0.7"), ("/contact/", "0.6"), ("/privacy/", "0.3")]
open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n")
open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8").write(f"""User-agent: *
Allow: /

# AI検索・AIアシスタントのクローラーも歓迎します
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {BASE}/sitemap.xml
""")
faq_txt = "\n".join(f"### {a}\n{plain(b)}\n" for a, b in FAQ_TOP)
open(os.path.join(DIST, "llms.txt"), "w", encoding="utf-8").write(f"""# LoveStrong

> LoveStrongは、ホームページとLPをつくるチームです。愛媛大学のサークルのメンバーが元になって活動しています。

## 要点
- 事業：ホームページ・LPの制作、公開後の保守
- 料金：制作は無料、保守は月5,000円
- 問い合わせ：{MAIL}

## ページ
- [トップ]({BASE}/)
- [制作内容]({BASE}/services/)
- [制作実績]({BASE}/works/)
- [ご依頼の流れ]({BASE}/flow/)
- [チーム概要]({BASE}/company/)
- [お問い合わせ]({BASE}/contact/)

## よくある質問
{faq_txt}""")
open(os.path.join(DIST, "_headers"), "w", encoding="utf-8").write("""/llms.txt
  Content-Type: text/plain; charset=utf-8
/robots.txt
  Content-Type: text/plain; charset=utf-8
/sitemap.xml
  Content-Type: application/xml; charset=utf-8
/assets/*
  Cache-Control: public, max-age=86400
/assets/site.css
  Cache-Control: public, max-age=3600
/assets/site.js
  Cache-Control: public, max-age=3600
""")
open(os.path.join(DIST, "404.html"), "w", encoding="utf-8").write("""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>ページが見つかりません｜LoveStrong</title><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><style>body{font-family:"Noto Sans JP",sans-serif;background:#ffffff;color:#26221e;margin:0;padding:96px 24px;text-align:center}a{color:#8f1a20}</style></head><body><h1>ページが見つかりません</h1><p>お探しのページは移動したか、なくなった可能性があります。</p><p><a href="/">トップへ</a>　<a href="/contact/">お問い合わせ</a></p></body></html>""")

js = '''for (const year of document.querySelectorAll(".current-year")) {
  year.textContent = String(new Date().getFullYear());
}

const menuButton = document.querySelector(".menu-button");
const mainNav = document.querySelector("#main-nav");
const setMenu = (open) => {
  if (open) {
    const hd = document.querySelector(".site-header");
    const hit = document.elementsFromPoint(window.innerWidth / 2, 36).find((e) => !hd.contains(e));
    let el = hit ? (hit.closest("section, footer") || hit) : document.body;
    let rgb = [246, 243, 239];
    while (el) { const m = getComputedStyle(el).backgroundColor.match(/rgba?\\(([^)]+)\\)/); if (m) { const v = m[1].split(",").map(parseFloat); if (v.length < 4 || v[3] > 0.5) { rgb = v.slice(0, 3); break; } } el = el.parentElement; }
    const light = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255 > 0.6;
    const fg = light ? "29, 24, 20" : "255, 255, 255";
    hd.style.setProperty("--menu-bg", "rgba(" + rgb.join(",") + ", .95)");
    hd.style.setProperty("--menu-fg", "rgb(" + fg + ")");
    hd.style.setProperty("--menu-line", "rgba(" + fg + ", .3)");
    const r = menuButton.getBoundingClientRect();
    mainNav.style.setProperty("--mx", Math.round(r.left + r.width / 2) + "px");
    mainNav.style.setProperty("--my", Math.round(r.top + r.height / 2) + "px");
  }
  mainNav.classList.toggle("open", open);
  document.body.classList.toggle("menu-open", open);
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "閉じる" : "メニュー");
  window.dispatchEvent(new Event("resize"));
};
if (menuButton && mainNav) {
  menuButton.addEventListener("click", () => setMenu(!mainNav.classList.contains("open")));
  mainNav.addEventListener("click", (event) => { if (event.target.closest("a")) setMenu(false); });
  window.addEventListener("keydown", (event) => { if (event.key === "Escape") setMenu(false); });
}

const header = document.querySelector(".site-header");
const cta = document.querySelector(".mobile-cta");
const hero = document.querySelector(".hero");
const markScrolled = () => {
  if (header) header.classList.toggle("scrolled", window.scrollY > 24);
  if (cta) cta.classList.toggle("show", window.scrollY > (hero ? hero.offsetHeight - 200 : 200));
};
window.addEventListener("scroll", markScrolled, { passive: true });
markScrolled();


// ヘッダーを、その下にある背景色に合わせて変える
if (header) {
  const parse = (c) => { const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const v = m[1].split(",").map((x) => parseFloat(x)); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
  const bgAt = (el) => { while (el) { const c = parse(getComputedStyle(el).backgroundColor); if (c && c.a > 0.5) return c; el = el.parentElement; } return { r: 246, g: 243, b: 239, a: 1 }; };
  const colorAt = (y) => {
    const hit = document.elementsFromPoint(window.innerWidth / 2, y).find((e) => !header.contains(e));
    const base = hit ? (hit.closest("section, footer") || hit) : document.body;
    const c = bgAt(base);
    return `rgb(${c.r}, ${c.g}, ${c.b})`;
  };
  const lumOf = (css) => { const c = parse(css); return (0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b) / 255; };
  const inkOf = (css) => (lumOf(css) > 0.6 ? "#1d1814" : "#ffffff");
  const invOf = (ink) => (ink === "#ffffff" ? "#1d1814" : "#ffffff");
  const layerA = header.querySelector(".header-inner");
  const layerB = layerA.cloneNode(true);
  layerB.removeAttribute("id");
  layerB.querySelectorAll("[id]").forEach((e) => e.removeAttribute("id"));
  layerB.querySelectorAll("a, button").forEach((e) => e.setAttribute("tabindex", "-1"));
  layerB.setAttribute("aria-hidden", "true");
  layerB.classList.add("header-clone");
  layerB.style.display = "none";
  layerA.after(layerB);
  const paint = (el, ink) => { el.style.color = ink; el.style.setProperty("--hfg", ink); el.style.setProperty("--hinv", invOf(ink)); };
  let ticking = false;
  const run = () => {
    ticking = false;
    const h = Math.round(header.getBoundingClientRect().height);
    const top = colorAt(1);
    const bottom = colorAt(h - 1);
    const menuOpen = document.body.classList.contains("menu-open");
    if (top === bottom || menuOpen) {
      header.style.setProperty("--hbg", top);
      layerA.style.clipPath = "";
      layerB.style.display = "none";
      paint(layerA, inkOf(top));
      return;
    }
    let lo = 1, hi = h - 1;
    while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (colorAt(mid) === top) lo = mid; else hi = mid; }
    header.style.setProperty("--hbg", `linear-gradient(to bottom, ${top} ${hi}px, ${bottom} ${hi}px)`);
    layerA.style.clipPath = `inset(0 0 ${h - hi}px 0)`;
    layerB.style.clipPath = `inset(${hi}px 0 0 0)`;
    layerB.style.display = "";
    paint(layerA, inkOf(top));
    paint(layerB, inkOf(bottom));
  };
  const syncHeader = () => { if (!ticking) { ticking = true; requestAnimationFrame(run); } };
  window.addEventListener("scroll", syncHeader, { passive: true });
  window.addEventListener("resize", syncHeader);
  window.addEventListener("load", syncHeader);
  run();
}

const contactForm = document.querySelector("#contact-form");
if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(contactForm);
    const lines = [
      `お名前：${formData.get("name")}`,
      `メールアドレス：${formData.get("email")}`,
      "",
      "お問い合わせ内容：",
      formData.get("message"),
    ];
    const subject = encodeURIComponent("お問い合わせ");
    const body = encodeURIComponent(lines.join("\\n"));
    window.location.href = `mailto:''' + MAIL + '''?subject=${subject}&body=${body}`;
  });
}
'''
open(os.path.join(DIST, "assets", "site.js"), "w", encoding="utf-8").write(js)
open(os.path.join(ROOT, "company-site", "wrangler.jsonc"), "w").write('''{
  "name": "lovestrong-site",
  "compatibility_date": "2026-10-22",
  "assets": { "directory": "dist" }
}
''')
if PREFIX:
    for dp, _, fs in os.walk(DIST):
        for fn in fs:
            if fn.endswith((".html", ".css", ".js")):
                fp = os.path.join(dp, fn)
                t = open(fp, encoding="utf-8").read()
                t = re.sub(r'((?:href|src)=")/(?!/)', lambda m: m.group(1) + PREFIX + "/", t)
                t = t.replace('url("/assets', 'url("' + PREFIX + '/assets').replace("'/assets", "'" + PREFIX + "/assets")
                open(fp, "w", encoding="utf-8").write(t)
print("built company")
