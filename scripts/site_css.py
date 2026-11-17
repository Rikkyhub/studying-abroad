"""サイト共通のデザイン（色・文字・余白・部品）。すべての生成ページが同じ値を使う。

ライト／ダークの色は、ここの TOKENS_* だけに書く。地図などの専用CSSは var(--xxx) で参照する。
"""

# 色。ダークは同じ名前で値だけ変える（ここ以外に :root の色を書かない）
_LIGHT = (
    "--ink:#1b2430;--muted:#566170;--link:#0b5cad;--bg:#fbfaf7;--line:#dcd8cf;--th:#efece5;--code:#efece6;--hl:#fff5d6;"
    "--page:#f3f1ec;--card:#ffffff;--card-line:rgba(20,30,40,.07);"
    "--shadow:0 10px 30px rgba(0,0,0,.05);--shadow-up:0 20px 40px rgba(0,0,0,.10);"
    "--accent:#0b6e6e;--accent-ink:#ffffff;--accent-soft:#e1f1ef;--warn:#8a4b00;--warn-soft:#fdeccf;--bad:#b3261e;"
    "--r-baguio:#c2410c;--r-may:#0b6e6e;--r-aug:#7c3aed;--r-cape:#1d4ed8;--r-common:#4b5563;"
    "--r-baguio-s:#fdebdd;--r-may-s:#dff1ef;--r-aug-s:#ece4fd;--r-cape-s:#dde8fd;--r-common-s:#e8eaed;"
    "--hero:#12343b;--hero-ink:#f4f7f7;--hero-mut:#c3d6d6"
)
_DARK = (
    "--ink:#e6e9ec;--muted:#a6b0ba;--link:#82b8ee;--bg:#14171a;--line:#363c42;--th:#20262b;--code:#21272c;--hl:#2d2813;"
    "--page:#0f1214;--card:#1b1f23;--card-line:rgba(255,255,255,.07);"
    "--shadow:0 10px 30px rgba(0,0,0,.35);--shadow-up:0 20px 40px rgba(0,0,0,.5);"
    "--accent:#5cc2bf;--accent-ink:#06201f;--accent-soft:#13302f;--warn:#f0b561;--warn-soft:#33270f;--bad:#f3857d;"
    "--r-baguio:#fb923c;--r-may:#5cc2bf;--r-aug:#b79cf7;--r-cape:#7ea6f4;--r-common:#a9b2bd;"
    "--r-baguio-s:#3a2214;--r-may-s:#12302e;--r-aug-s:#2a2142;--r-cape-s:#1a2745;--r-common-s:#262b31;"
    "--hero:#0c2a30;--hero-ink:#f0f5f5;--hero-mut:#a9c3c3"
)
_FONTS = (
    '--sans:system-ui,-apple-system,"Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Meiryo",sans-serif;'
    '--mono:ui-monospace,SFMono-Regular,Consolas,monospace;--bar:52px;--rad:12px;--rad-s:8px'
)

TOKENS = (
    ":root{color-scheme:light;" + _LIGHT + ";" + _FONTS + "}\n"
    "@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){color-scheme:dark;" + _DARK + "}}\n"
    ":root[data-theme=\"dark\"]{color-scheme:dark;" + _DARK + "}\n"
)

# 部品の見た目。JS が参照するクラス名・data-label は変えない
COMPONENTS = r"""
*{box-sizing:border-box}
html{scroll-padding-top:calc(var(--bar) + 14px)}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.8 var(--sans)}
a{color:var(--link);text-underline-offset:3px} a:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible,button:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
h1{font-size:2rem;line-height:1.35;margin:10px 0 10px;font-weight:800;letter-spacing:.01em}
h2{font-size:1.4rem;line-height:1.45;margin:52px 0 12px;padding-top:0;font-weight:800}
h3{font-size:1.12rem;line-height:1.55;margin:30px 0 8px;font-weight:700} h4{font-size:1rem;margin:22px 0 4px}
p{margin:10px 0} p,li{max-width:72ch} .lead{color:var(--ink);margin:0 0 6px;font-size:1.05rem} .muted{color:var(--muted);font-size:.93rem}
.note{background:var(--warn-soft);color:var(--ink);padding:12px 16px;margin:18px 0;max-width:none;border-radius:var(--rad-s)}
ol.todo{margin:8px 0;padding-left:1.6em} ol.todo li{margin:6px 0} ul.facts{margin:8px 0;padding-left:1.4em;color:var(--muted)}
.scroll{margin:14px 0 24px;border:1px solid var(--line);border-radius:var(--rad);background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:.94rem;line-height:1.65}
th,td{padding:10px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);overflow-wrap:anywhere;word-break:normal;line-break:strict}
td{min-width:4.4em} tbody tr:last-child td{border-bottom:0}
thead th:first-child{border-top-left-radius:calc(var(--rad) - 1px)} thead th:last-child{border-top-right-radius:calc(var(--rad) - 1px)}
tbody tr:last-child td:first-child{border-bottom-left-radius:calc(var(--rad) - 1px)} tbody tr:last-child td:last-child{border-bottom-right-radius:calc(var(--rad) - 1px)} tbody tr:nth-child(even) td{background:color-mix(in srgb,var(--th) 42%,transparent)}
th{position:sticky;top:var(--bar);z-index:2;background:var(--th);font-weight:700;border-bottom:1px solid var(--line)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.c,th.c{text-align:center}
td strong{font-weight:700}
code{font-family:var(--mono);font-size:.9em;background:var(--code);padding:1px 5px;border-radius:4px}
pre{background:var(--code);padding:12px 14px;overflow-x:auto;border-radius:var(--rad-s)} pre code{padding:0;background:none}
blockquote{margin:16px 0;background:var(--accent-soft);padding:6px 16px;border-radius:var(--rad-s)}
ul,ol{padding-left:1.5em} li{margin:4px 0}
.check{display:inline-block;width:.9em;height:.9em;border:1.5px solid var(--muted);margin-right:6px;vertical-align:-1px;border-radius:3px}
.check.done{background:var(--link);border-color:var(--link)}
form.calc{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px 20px;margin:10px 0 14px}
form.calc label{display:grid;gap:4px;font-size:.93rem;color:var(--muted)}
form.calc input,form.calc select{font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--line);padding:8px 10px;min-width:0;width:100%;border-radius:var(--rad-s)}
form.calc output{font-size:1.1rem;font-variant-numeric:tabular-nums;color:var(--ink);min-height:1.8em}
article,h1,p,li{overflow-wrap:anywhere}
main.page{padding-bottom:24px}

/* ---- 上部ナビ（全ページ共通）：ブランド＋横並び＋「ほか」 ---- */
header.bar{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line)}
header.bar .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:2px 18px;min-height:var(--bar)}
header.bar .brand{font-weight:900;font-size:1.02rem;color:var(--ink);text-decoration:none;white-space:nowrap;padding:10px 0;margin-right:auto}
header.bar nav.menu{display:flex;align-items:center;gap:2px 4px;font-size:.92rem}
header.bar nav.menu>a,header.bar nav.menu>details>summary{padding:7px 12px;border-radius:999px;text-decoration:none;color:var(--ink);white-space:nowrap;cursor:pointer;list-style:none;font-weight:500;min-height:36px;display:inline-flex;align-items:center}
header.bar nav.menu>details>summary::-webkit-details-marker{display:none}
header.bar nav.menu>details>summary::after{content:"\25BE";margin-left:4px;color:var(--muted);font-size:.8em}
header.bar nav.menu>a:hover,header.bar nav.menu>details>summary:hover{background:var(--th)}
header.bar nav.menu [aria-current]{background:var(--ink);color:var(--bg);font-weight:700}
header.bar nav.menu>details.on>summary{background:var(--ink);color:var(--bg);font-weight:700}
header.bar nav.menu>details.on>summary::after{color:var(--bg)}
header.bar nav.menu>details{position:relative}
header.bar .drop{position:absolute;right:0;top:calc(100% + 6px);min-width:250px;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);box-shadow:var(--shadow-up);padding:8px;display:grid;gap:2px;z-index:30}
header.bar .drop a{display:block;padding:7px 12px;border-radius:var(--rad-s);text-decoration:none;color:var(--ink);font-size:.92rem;white-space:normal}
header.bar .drop a:hover{background:var(--th)}
header.bar .drop a[aria-current]{background:var(--ink);color:var(--bg);font-weight:700}
header.bar .drop .dl{font-size:.74rem;font-weight:700;color:var(--muted);padding:8px 12px 2px;margin:0;letter-spacing:.06em;max-width:none}
@media(max-width:860px){
header.bar .wrap{flex-wrap:nowrap;overflow-x:auto;gap:6px;scrollbar-width:thin}
header.bar .brand{margin-right:8px;padding:10px 0}
header.bar nav.menu{flex:none}
header.bar nav.menu>details{position:static}
header.bar .drop{position:fixed;left:12px;right:12px;top:calc(var(--bar) + 4px);min-width:0;max-height:calc(100vh - var(--bar) - 20px);overflow:auto}
}

/* ---- ページの見出し帯・パンくず・目次 ---- */
.crumb{margin:20px 0 0;color:var(--muted);font-size:.9rem}
.crumb a{color:var(--muted)}
.page-head{margin:6px 0 4px}
.page-head .tag{display:inline-block;font-size:.8rem;font-weight:700;padding:2px 10px;border-radius:999px;background:var(--r-common-s);color:var(--r-common);margin-bottom:4px}
.page-head .tag.r-baguio{background:var(--r-baguio-s);color:var(--r-baguio)}
.page-head .tag.r-may{background:var(--r-may-s);color:var(--r-may)}
.page-head .tag.r-aug{background:var(--r-aug-s);color:var(--r-aug)}
.page-head .tag.r-cape{background:var(--r-cape-s);color:var(--r-cape)}
nav.toc{display:flex;flex-wrap:wrap;gap:6px 8px;margin:16px 0 8px;padding:12px 14px;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);font-size:.92rem}
nav.toc .label{font-weight:700;color:var(--muted);align-self:center;margin-right:4px}
nav.toc a{padding:3px 12px;border-radius:999px;background:var(--th);color:var(--ink);text-decoration:none}
nav.toc a:hover{background:var(--accent-soft);color:var(--accent)}

/* ---- フッター ---- */
footer{color:var(--muted);font-size:.9rem;margin-top:56px;padding:18px 0 44px;border-top:1px solid var(--line)}
footer p{max-width:none}
nav.all{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:6px 28px;margin:14px 0;font-size:.94rem}
nav.all .g{font-weight:700;color:var(--muted);margin-top:8px} nav.all a{display:block;padding:1px 0}
nav.all details.g-fold{align-self:start} nav.all details.g-fold>summary{cursor:pointer;font-weight:700;color:var(--muted);padding:2px 0}
nav.all details.g-fold[open]>summary{margin-bottom:2px}
nav.all a[aria-current]{font-weight:700;color:var(--ink)}
details.more.notes{margin:4px 0 8px}

/* ---- トップ ---- */
body.home{background:var(--page)}
.top{max-width:1120px;overflow:visible}
.top h2{margin:60px 0 6px;font-size:1.45rem}
.sec-lead{color:var(--muted);font-size:.95rem;margin:6px 0 0;max-width:72ch}
.hero{background:var(--hero);color:var(--hero-ink);border-radius:20px;padding:44px 36px 36px;margin:22px 0 8px}
.hero h1{color:var(--hero-ink);font-size:2.2rem;margin:0 0 10px}
.hero .lead{color:var(--hero-ink);max-width:60ch}
.hero .hero-note{margin:16px 0 0;font-size:.92rem;color:var(--hero-mut);max-width:70ch}
.hero .cta{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0}
.hero .cta a{display:inline-block;padding:11px 20px;border-radius:999px;font-weight:700;text-decoration:none;background:var(--hero-ink);color:var(--hero)}
.hero .cta a.alt{background:transparent;color:var(--hero-ink);box-shadow:inset 0 0 0 1.5px var(--hero-mut)}
.stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:18px 0}
.stat-row .stat{background:var(--card);border:1px solid var(--card-line);border-radius:var(--rad);padding:16px 18px;box-shadow:var(--shadow)}
.stat .k{font-size:.82rem;color:var(--muted);margin:0}
.stat .v{font-size:1.6rem;font-weight:800;font-variant-numeric:tabular-nums;margin:2px 0 0;line-height:1.35}
.stat .s{font-size:.82rem;color:var(--muted);margin:2px 0 0}

/* ---- カード ---- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:24px;padding:20px 0 28px;overflow:visible;align-items:stretch}
.card{display:block;position:relative;background:var(--card);border:1px solid var(--card-line);border-radius:var(--rad);padding:22px 22px 20px;color:var(--ink);text-decoration:none;box-shadow:var(--shadow);transition:transform .25s ease,box-shadow .25s ease}
.card.wide{grid-column:1/-1;margin:20px 0 28px}
.card h3{font-size:1.1rem;margin:2px 0 6px;line-height:1.5}
.card p{margin:6px 0;max-width:none}
.card .eyebrow{font-size:.85rem;color:var(--muted);margin:0 0 2px}
.card .val{font-size:1.75rem;line-height:1.3;font-weight:700;font-variant-numeric:tabular-nums;margin:4px 0 8px}
.card .sub{font-size:.9rem;color:var(--muted);line-height:1.7}
.card .status{font-size:.88rem;font-weight:700;margin:2px 0 6px}
.card .go{display:block;margin-top:12px;font-size:.9rem;font-weight:700;color:var(--link)}
.card .go::after{content:" \2192"}
a.card:focus-visible{outline:2px solid var(--link);outline-offset:4px}
.card .n,dl.kv dd{font-variant-numeric:tabular-nums}
dl.kv{margin:8px 0}
dl.kv div{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:6px 0;border-bottom:1px solid var(--line)}
dl.kv div:last-child{border-bottom:0}
dl.kv dt{color:var(--muted);font-size:.9rem} dl.kv dd{margin:0;font-weight:700}
.card .scroll{margin:0;border:0;border-radius:0}
.card ol.todo{margin:8px 0 8px} .card ul.facts{margin:8px 0 0}
.card.reg{border-top:4px solid var(--c,var(--r-common))}
.card.reg .eyebrow{color:var(--c,var(--muted));font-weight:700}
.card.reg-baguio{--c:var(--r-baguio)} .card.reg-may{--c:var(--r-may)} .card.reg-aug{--c:var(--r-aug)} .card.reg-cape{--c:var(--r-cape)} .card.reg-common{--c:var(--r-common)}

.card.doc{padding:18px 20px}
.card.doc h3{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin:0 0 6px}
.card.doc .cnt{font-size:.8rem;font-weight:700;color:var(--muted)}
.card.doc ul{margin:4px 0 0;padding-left:1.1em} .card.doc li{margin:4px 0;font-size:.92rem}
.docs-grid{grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}

/* ---- 開閉（長いページ） ---- */
details.more{margin:0} details.more>summary{cursor:pointer;list-style:none;color:var(--ink)}
details.more>summary::-webkit-details-marker{display:none}
details.more .hint{color:var(--link);font-size:.82rem;margin-left:4px;white-space:nowrap}
details.more[open]>summary{font-weight:700;margin-bottom:4px} details.more[open]>summary .hint{display:none}
details.more>.full{padding:6px 0 4px 12px;box-shadow:inset 2px 0 0 var(--line)}
details.sec{margin:12px 0;border:1px solid var(--line);border-radius:var(--rad);background:var(--card)}
details.sec>summary{cursor:pointer;padding:12px 16px;list-style:none}
details.sec>summary::-webkit-details-marker{display:none}
details.sec>summary::before{content:"\25B8";float:left;margin:3px 10px 0 0;color:var(--accent);transition:transform .2s}
details.sec[open]>summary::before{transform:rotate(90deg)}
details.sec>summary h2{display:inline;margin:0;padding:0;border:0;font-size:1.18rem}
details.sec>:not(summary){margin-left:16px;margin-right:16px} details.sec>.scroll{margin-left:16px;margin-right:16px}
details.sec[open]>summary{border-bottom:1px solid var(--line);margin-bottom:12px}
details.sec>:last-child{margin-bottom:16px}
.sec-tools{margin:10px 0} .sec-tools button{font:inherit;font-size:.88rem;padding:5px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);cursor:pointer;margin-right:6px}
details.fold{margin:12px 0 28px} details.fold>summary{cursor:pointer;font-weight:700;padding:12px 16px;border:1px solid var(--line);border-radius:var(--rad);background:var(--card);list-style:none}
details.fold>summary::-webkit-details-marker{display:none} details.fold>summary::before{content:"\25B8";display:inline-block;margin-right:8px;color:var(--accent);transition:transform .2s}
details.fold[open]>summary::before{transform:rotate(90deg)}

/* ---- ルート作成・コスト表・日程プランナー（JS が使うクラス） ---- */
.route-pre{margin:8px 0 2px}.route-pre .lbl{font-weight:700;margin-right:6px}
.route-pre .pre-btn{font:inherit;font-size:.88rem;padding:5px 15px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);cursor:pointer;margin:2px 4px 2px 0}
.route-pre .pre-btn.on{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.route-desc{color:var(--muted);font-size:.88rem;margin:2px 0 8px}
.route-t td.chk{text-align:center}.route-t td.chk input{width:auto;min-width:0;transform:scale(1.25)}
.route-ask{display:block;margin:12px 0 4px;font-weight:700;font-size:.9rem}
.route-ask textarea{display:block;width:100%;margin-top:4px;font:inherit;font-size:.92rem;padding:8px 10px;border:1px solid var(--line);border-radius:var(--rad-s);background:var(--bg);color:var(--ink)}
.route-cost{font-size:.92rem;margin:2px 0 8px;font-weight:700}.route-cost.dim{color:var(--muted);font-weight:400}.route-cost.over{color:var(--bad)}
.route-t td.sub{font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.route-days{font-size:.92rem;margin:2px 0 8px}.route-days.dim{color:var(--muted)}.route-days.over{color:var(--bad);font-weight:700}
.route-t td select{width:100%;min-width:5.5em;font:inherit;font-size:.9rem;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}
.route-bar button:disabled{opacity:.45;cursor:default}
.route-t td input{width:100%;min-width:6em;font:inherit;font-size:.9rem;padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}
.route-t tr.fix td{background:color-mix(in srgb,var(--accent) 10%,transparent);text-align:center}
.route-t td.ops{white-space:nowrap}.route-t td.ops button{font:inherit;font-size:.8rem;padding:2px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink);cursor:pointer;margin-right:3px}
.route-bar button{font:inherit;font-size:.9rem;padding:6px 16px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);cursor:pointer;margin:6px 6px 0 0}
.route-sum{font-weight:700;margin:10px 0}
.triage{margin:12px 0 4px;padding:14px 16px;border:1px solid var(--line);border-radius:var(--rad);background:var(--card);font-size:.92rem}
.triage .big{font-size:1.4rem;font-weight:800;font-variant-numeric:tabular-nums}
.triage .muted,.triage .tri-note{color:var(--muted);font-size:.85rem}
.triage button{font:inherit;font-size:.88rem;padding:5px 12px;border:1px solid var(--line);border-radius:999px;background:var(--bg);color:var(--ink);cursor:pointer;margin:6px 6px 0 0}
.triage .tri-hide{display:inline-block;margin:6px 12px 0 0}
.triage .tri-filter{margin:8px 0 4px}
.triage .tri-filter button[aria-pressed=true]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
th.tri,td.tri{min-width:7em;white-space:nowrap}
td.tri select,td.tri input[type=text]{font:inherit;font-size:.88rem;max-width:11em;padding:3px 6px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}
td.tri input[type=text]{width:11em}
tr.skip td:not(.tri){text-decoration:line-through;opacity:.5}
tr.hold td:not(.tri){opacity:.75}
tr[hidden]{display:none}

/* ---- カルーセル ---- */
.carousel{position:relative}
.car-track{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;padding:20px 4px 32px;-webkit-overflow-scrolling:touch}
.car-track>.card{flex:0 0 min(300px,80%);scroll-snap-align:start}
.car-btn{position:absolute;top:50%;transform:translateY(-60%);z-index:2;width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:1.4rem;line-height:1;cursor:pointer;box-shadow:var(--shadow)}
.car-btn.prev{left:-12px} .car-btn.next{right:-12px} .car-btn:focus-visible{outline:2px solid var(--link);outline-offset:2px}
.car-btn[disabled]{opacity:.35;cursor:default}

@media (prefers-reduced-motion:reduce){.car-track{scroll-behavior:auto}}
@media (hover:hover){.card:hover{transform:translateY(-6px);box-shadow:var(--shadow-up)}}
@media (prefers-reduced-motion:reduce){.card{transition:none}.card:hover{transform:none}}

/* ---- 携帯 ---- */
@media(max-width:760px){.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch} table:not(.cal):not(.pl){min-width:560px} th{position:static}}
@media(max-width:640px){
.hero{padding:30px 20px 26px;border-radius:16px} .hero h1{font-size:1.7rem}
.scroll{overflow-x:visible;border:0;background:none;border-radius:0}
.scroll table:not(:has(td[data-label])){min-width:0;table-layout:auto}
.scroll table:not(:has(td[data-label])) th,.scroll table:not(:has(td[data-label])) td{padding:7px 6px;overflow-wrap:anywhere}
.scroll table:has(td[data-label]){min-width:0;display:block}
.scroll table:has(td[data-label]) thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.scroll table:has(td[data-label]) tbody,.scroll table:has(td[data-label]) tr{display:block}
.scroll table:has(td[data-label]) tr{margin:0 0 12px;border:1px solid var(--line);border-radius:var(--rad);background:var(--card);overflow:hidden}
.scroll table:has(td[data-label]) td{display:block;padding:8px 12px;border-bottom:1px solid var(--line);background:none!important;min-width:0;text-align:left}
.scroll table:has(td[data-label]) td:last-child{border-bottom:0}
.scroll table:has(td[data-label]) td::before{content:attr(data-label);display:block;font-weight:700;color:var(--muted);font-size:.8rem;margin-bottom:2px}
.scroll table:has(td[data-label]) td.n,.scroll table:has(td[data-label]) td.c{text-align:left;white-space:normal}
}
@media(max-width:480px){body{font-size:15.5px} th,td{padding:7px 9px} h1{font-size:1.5rem}}
"""

BASE_CSS = TOKENS + COMPONENTS
