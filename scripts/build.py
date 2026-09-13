#!/usr/bin/env python3
"""Build fluentin.app: index (en), zh/ (zh-Hant), privacy/, terms/, support/.
Layout mirrors lossic.app / rocketbucket.app: sticky nav, centred hero with icon + serif h1 +
badge + phone shot, feature grid, numbered steps, privacy card, FAQ, bottom CTA, footer.

    python3 scripts/build.py
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_REPO = ROOT.parent / "fluentin"
LAST_UPDATED = "September 12, 2026"

CSS = """
:root{--teal:#24666A;--teal-deep:#1B4F52;--teal-tint:#DFEEEE;--ink:#23302F;--muted:#66716F;--bg:#FFF8EE;--card:#FFFFFF;--border:rgba(36,102,106,.16);--shadow:0 24px 80px rgba(35,48,47,.18)}
@media(prefers-color-scheme:dark){:root{--teal:#5FB0B4;--teal-deep:#8FD0D3;--teal-tint:#1E3335;--ink:#EEF2F1;--muted:#A3B0AE;--bg:#151D1D;--card:#1C2626;--border:rgba(95,176,180,.22);--shadow:0 24px 80px rgba(0,0,0,.55)}}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg);line-height:1.65;-webkit-font-smoothing:antialiased}
nav{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;max-width:1080px;margin:0 auto;padding:.9rem 1.5rem;backdrop-filter:saturate(180%) blur(16px)}
nav .brand{display:flex;align-items:center;gap:.55rem;font-weight:700;font-size:1.05rem;text-decoration:none;color:var(--ink)}
nav .brand img{width:28px;height:28px;border-radius:7px}
nav .links{display:flex;align-items:center;flex-wrap:wrap}
nav .links a{color:var(--muted);text-decoration:none;margin-left:1.4rem;font-size:.92rem}nav .links a:hover{color:var(--teal)}
nav .lang{margin-left:1.4rem;font-size:.9rem;color:var(--muted)}nav .lang a{margin:0 .15rem;text-decoration:none;color:var(--muted)}nav .lang a.active{color:var(--ink);font-weight:700}
@media(max-width:720px){nav{flex-direction:column;gap:.45rem;padding:.7rem 1rem .65rem}nav .links{justify-content:center;gap:.2rem 1rem}nav .links a{margin-left:0;font-size:.86rem}nav .lang{margin-left:0}.hero{padding-top:2.6rem}}
.hero{max-width:1080px;margin:0 auto;padding:4.2rem 1.5rem 0;text-align:center}
.hero .app-icon{width:108px;height:108px;border-radius:24px;box-shadow:0 12px 36px rgba(35,48,47,.22);margin-bottom:1.6rem}
.hero h1{font-family:"New York",Georgia,"Times New Roman",serif;font-size:clamp(2.2rem,6vw,3.4rem);line-height:1.18;letter-spacing:-.02em;font-weight:700;max-width:820px;margin:0 auto}
.hero h1 em{font-style:normal;background:linear-gradient(transparent 58%,rgba(36,102,106,.28) 58%,rgba(36,102,106,.28) 94%,transparent 94%);padding:0 .06em}
.hero p.sub{color:var(--muted);font-size:1.16rem;max-width:700px;margin:1.2rem auto 0}
.badge{display:inline-flex;align-items:center;gap:.45rem;margin-top:1.8rem;font-size:.88rem;font-weight:600;color:var(--teal-deep);background:var(--teal-tint);border:1px solid var(--border);padding:.45rem 1rem;border-radius:999px}
.badge::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--teal);animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
.hero .phones{display:flex;justify-content:center;gap:1.4rem;margin:3.2rem auto 0;flex-wrap:wrap}
.hero .phones img{width:min(280px,64vw);height:auto;border-radius:34px;filter:drop-shadow(0 28px 56px rgba(35,48,47,.28))}
section.features{max-width:1080px;margin:0 auto;padding:4.6rem 1.5rem 1rem}
h2.section-title{font-family:"New York",Georgia,"Times New Roman",serif;font-size:1.9rem;letter-spacing:-.02em;margin-bottom:1.6rem;text-align:center}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.1rem}
.feature{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1.6rem}
.feature .icon{width:42px;height:42px;border-radius:11px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;margin-bottom:.9rem;color:var(--teal-deep);font-weight:800;font-family:Georgia,serif}
.feature h3{font-size:1.04rem;margin-bottom:.35rem}.feature p{font-size:.94rem;color:var(--muted)}
section.how{max-width:880px;margin:0 auto;padding:4.2rem 1.5rem 1rem;text-align:center}
p.section-sub{color:var(--muted);max-width:560px;margin:-.8rem auto 2.4rem}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.6rem;text-align:left}
.step .num{font-size:.8rem;font-weight:700;color:var(--teal-deep);background:var(--teal-tint);border-radius:999px;width:26px;height:26px;display:flex;align-items:center;justify-content:center;margin-bottom:.7rem}
.step h3{font-size:1rem;margin-bottom:.3rem}.step p{font-size:.92rem;color:var(--muted)}
.verdicts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;max-width:880px;margin:0 auto;padding:1rem 1.5rem 0}
.verdict{border-radius:14px;padding:1.1rem 1.2rem;border:1px solid var(--border);background:var(--card)}
.verdict b{display:block;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.3rem}
.verdict.ok b{color:#2E7D32}.verdict.close b{color:#C77700}.verdict.no b{color:#B3261E}
section.privacy{max-width:780px;margin:4.2rem auto 0;padding:0 1.5rem}
.privacy-card{background:var(--teal-tint);border:1px solid var(--border);border-radius:20px;padding:2.2rem;text-align:center}
.privacy-card h2{font-family:"New York",Georgia,serif;font-size:1.5rem;letter-spacing:-.02em;margin-bottom:.7rem}
.privacy-card p{color:var(--muted);font-size:.98rem;max-width:620px;margin:0 auto}.privacy-card a{color:var(--teal-deep)}
section.faq{max-width:720px;margin:0 auto;padding:4.2rem 1.5rem 2rem}
.faq details{border-bottom:1px solid var(--border);padding:1rem .2rem}
.faq summary{cursor:pointer;font-weight:600;font-size:1rem;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}
.faq summary::-webkit-details-marker{display:none}.faq summary::after{content:"+";color:var(--teal);font-size:1.3rem;font-weight:400;flex-shrink:0}.faq details[open] summary::after{content:"–"}
.faq details p{color:var(--muted);font-size:.95rem;padding-top:.6rem}
.bottom-cta{text-align:center;padding:4.5rem 1.5rem;background:linear-gradient(180deg,transparent,var(--teal-tint))}
.bottom-cta h2{font-family:"New York",Georgia,serif;font-size:1.8rem;letter-spacing:-.02em;margin-bottom:1.4rem}
.cta.pending{display:inline-flex;align-items:center;gap:.5rem;background:transparent;color:var(--muted);border:1.5px dashed var(--border);border-radius:12px;padding:.85rem 1.5rem;font-weight:600;font-size:.98rem;cursor:default;text-decoration:none}
footer{border-top:1px solid var(--border);padding:2.2rem 1.5rem;text-align:center;color:var(--muted);font-size:.88rem}footer a{color:var(--teal-deep);text-decoration:none;margin:0 .2rem}
/* CJK typography (rocketbucket.app pattern): system CJK sans, looser leading, sans headings
   with positive tracking; a serif Latin face would fall back to Songti and look mixed. */
html[lang="zh-Hant"] body{font-family:"PingFang TC","SF Pro TC",-apple-system,BlinkMacSystemFont,"Heiti TC","Microsoft JhengHei","Noto Sans TC",sans-serif;line-height:1.75}
html[lang="zh-Hant"] .hero h1,html[lang="zh-Hant"] h2.section-title,html[lang="zh-Hant"] .bottom-cta h2,html[lang="zh-Hant"] .privacy-card h2{font-family:inherit;font-weight:800;letter-spacing:.01em}
html[lang="zh-Hant"] .hero h1{line-height:1.25;font-size:clamp(2rem,5.4vw,3rem)}
html[lang="zh-Hant"] .hero h1 em{font-style:normal}
html[lang="zh-Hant"] .hero p.sub{font-size:1.1rem;line-height:1.8}
html[lang="zh-Hant"] .feature h3,html[lang="zh-Hant"] .step h3,html[lang="zh-Hant"] .faq summary{letter-spacing:.01em}
html[lang="zh-Hant"] .verdict b{letter-spacing:.06em}
/* legal pages */
main.legal{max-width:720px;margin:0 auto;padding:3rem 1.4rem 4rem}main.legal a{color:var(--teal-deep)}
main.legal h1{font-family:"New York",Georgia,serif;font-size:2rem;letter-spacing:-.02em;margin-bottom:.4rem}
main.legal .updated{color:var(--muted);font-size:.9rem;margin-bottom:2.2rem}main.legal h2{font-size:1.25rem;margin:2rem 0 .6rem}
main.legal p,main.legal li{font-size:.98rem;margin-bottom:.7rem}main.legal ul{padding-left:1.3rem;margin-bottom:.7rem}
main.legal .home{display:inline-block;margin-bottom:2rem;font-size:.92rem;text-decoration:none}
main.legal .card{border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.3rem;margin:1.2rem 0;background:var(--card)}
"""

# ------------------------------------------------------------------ copy
T = {
 "en": dict(
  lang="en", path="/", title="FluentIn — Speak like a local, anywhere",
  desc="FluentIn teaches how people actually talk in a city or an industry: read the situation, say it out loud, get judged like a local would judge you.",
  nav=["Features", "How it works", "FAQ"], nav_ids=["features", "how", "faq"],
  h1='School taught you standard English.<br>FluentIn teaches you how <em>that street</em> actually talks.',
  sub="Regional slang and industry jargon, drilled by speaking. You read the situation in your language, hold the button, say it in English — and find out whether a local would have said it that way.",
  badge="iPhone · in App Store review", shots=("en-02-prompt.png", "en-03-reveal.png"),
  features_title="What makes it different",
  features=[("Say it, don't type it", "Hold the button and speak. The recogniser is biased toward each phrase so it hears the slang instead of “correcting” it."),
            ("Three verdicts, not two", "Local — that's how they say it. Close — right meaning, wrong wording. Not it. The middle one is the feedback textbooks can't give."),
            ("A social card for every phrase", "Who says it, where it lands, where it doesn't, and where it came from. Slang without the room it belongs in is a trap."),
            ("Real people, not voice actors", "Hear the phrase in the wild through YouTube — a New Yorker saying it in context, not a studio read."),
            ("Hints you control", "Nothing, the word count, first letters, or the whole sentence with one key word blanked out. You decide how hard."),
            ("Your language, your key", "Prompts in English or 繁體中文. Optional AI judge for grey-zone answers with your own Gemini key — no FluentIn servers.")],
  how_title="How a card works", how_sub="One phrase at a time, thirty seconds each.",
  steps=[("Read the situation", "“You're at the bodega counter and want the breakfast sandwich…” — in your language, never a translation to memorise."),
         ("Hold and say it", "Speak the English a local would use. Release when you're done."),
         ("Get the verdict", "Local, Close, or Not it — with the reason when you turn on the AI judge."),
         ("See the whole card", "The phrase, who says it, where it's safe, and a clip of someone saying it for real.")],
  verdicts=[("ok", "Local", "That's how they say it."), ("close", "Close", "Meaning's right — but that's not how locals say it."), ("no", "Not it", "Different meaning, or nothing heard.")],
  privacy_h="No servers. No accounts. Nothing sold.",
  privacy_p='Speech is recognised on your device with Apple\'s speech framework. The only network calls are the ones you opt into: an AI judge with your own API key, and YouTube\'s embedded player. <a href="/privacy/">Privacy policy</a> · <a href="/terms/">Terms</a>',
  faq_title="Questions",
  faq=[("Which packs exist?", "Fluent in New York — 50 phrases: on line, bodega, chopped cheese, the super, walk-up, stabilized, OMNY, deadass, brick… London, Silicon Valley, Wall Street and Singapore are being written."),
       ("Do I need to speak?", "No. Tap the blanked word and type the missing letters instead. The judge is the same."),
       ("What's the AI judge?", "When the on-device matcher can't decide, your transcribed answer and the exercise's phrase list go to Gemini with the API key you paste in Settings, and you get a verdict plus a one-line reason. Without a key the app is fully usable; undecided answers count as wrong."),
       ("Is the slang safe to use?", "Each card says where it lands and where it doesn't. Some cards are marked recognition-first: understand them, don't lead with them."),
       ("Who writes the cards?", "We draft them, and people who live there review them before a pack ships. Corrections: hello@fluentin.app.")],
  cta_h="Fluent in New York is the first pack.", cta="Coming to the App Store",
  footer_privacy="Privacy", footer_terms="Terms", footer_support="Support",
 ),
 "zh": dict(
  lang="zh-Hant", path="/zh/", title="FluentIn — 講得像當地人，去哪都行",
  desc="FluentIn 教你一個城市、一個行業裡的人真正怎麼講：看情境、開口說、讓當地人的標準來判你。",
  nav=["特色", "怎麼玩", "常見問題"], nav_ids=["features", "how", "faq"],
  h1='學校教你標準英語。<br>我們教你<em>那條街上的人</em>真正怎麼講。',
  sub="地域俚語與行業行話，用「說」來練。用你的語言看情境、按住按鈕、用英文說出來——然後知道當地人會不會這樣講。",
  badge="iPhone · App Store 審核中", shots=("zh-Hant-02-prompt.png", "zh-Hant-03-reveal.png"),
  features_title="跟別的英語 app 差在哪",
  features=[("開口說，不是打字", "按住按鈕講話。辨識器會朝每張卡的說法偏置，聽得到俚語，而不是把它「糾正」成標準英文。"),
            ("三種結果，不是兩種", "地道——當地人就是這樣講。接近——意思對、說法不對。不是這個。中間那個是教科書給不了的回饋。"),
            ("每句都有社交說明卡", "誰會這樣說、什麼場合能講、什麼場合別講、從哪來的。不知道場合的俚語是陷阱。"),
            ("真人，不是配音員", "透過 YouTube 聽這句話在真實世界怎麼出現——紐約人在情境裡講出來，不是錄音室。"),
            ("提示你自己決定", "完全不提示、幾個字、每個字的第一個字母，或整句只遮一個關鍵字。難度你選。"),
            ("你的語言、你的金鑰", "題目可用繁體中文或 English。灰色地帶的答案可選用你自己的 Gemini 金鑰交給 AI 判——沒有 FluentIn 伺服器。")],
  how_title="一張卡怎麼玩", how_sub="一次一句，三十秒。",
  steps=[("看情境", "「你在 bodega 櫃台想點早餐三明治……」——用你的語言描述當下，不是給你一句翻譯背。"),
         ("按住、說出來", "用當地人會用的英文說。說完放開。"),
         ("拿到判定", "地道、接近、或不是這個——開了 AI 判題還會附一句理由。"),
         ("看完整張卡", "完整寫法、誰會這樣說、什麼場合安全，以及一段真人講這句話的影片。")],
  verdicts=[("ok", "地道", "當地人就是這樣講。"), ("close", "接近", "意思對，但當地人不會這樣說。"), ("no", "不是這個", "意思不同，或沒聽到。")],
  privacy_h="沒有伺服器。沒有帳號。不賣資料。",
  privacy_p='語音在你的裝置上用 Apple 的語音框架辨識。唯二的網路連線都是你自己選擇開啟的：用你自己 API 金鑰的 AI 判題，以及 YouTube 的嵌入播放器。<a href="/privacy/">隱私政策</a> · <a href="/terms/">使用條款</a>',
  faq_title="常見問題",
  faq=[("有哪些語言包？", "Fluent in 紐約——50 句：on line、bodega、chopped cheese、the super、walk-up、stabilized、OMNY、deadass、brick……倫敦、矽谷、華爾街、新加坡正在寫。"),
       ("一定要開口嗎？", "不用。點題目裡被遮住的字，直接打剩下的字母。判題是同一套。"),
       ("AI 判題是什麼？", "裝置上比對不出來時，你的答案文字和這題的說法清單會用你在設定裡貼的金鑰送給 Gemini，回一個判定加一句理由。沒有金鑰 app 一樣能用，判不出來的答案算錯。"),
       ("這些俚語用了安全嗎？", "每張卡都寫了什麼場合能講、什麼場合別講。有些卡標為「先聽懂」：理解它，但不要主動用。"),
       ("卡片是誰寫的？", "我們起草，住在當地的人審過才上架。指正請寄 hello@fluentin.app。")],
  cta_h="Fluent in 紐約是第一個包。", cta="即將上架 App Store",
  footer_privacy="隱私政策", footer_terms="使用條款", footer_support="支援",
 ),
}

LANG_SWITCH = [("en", "/", "EN"), ("zh", "/zh/", "繁中")]


def head(t, url, extra_meta=""):
    alts = "".join(f'<link rel="alternate" hreflang="{T[k]["lang"]}" href="https://fluentin.app{T[k]["path"]}">' for k in T)
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['title'])}</title>
<meta name="description" content="{html.escape(t['desc'])}">
<meta property="og:title" content="FluentIn"><meta property="og:description" content="{html.escape(t['desc'])}">
<meta property="og:image" content="https://fluentin.app/og.png"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{alts}<link rel="alternate" hreflang="x-default" href="https://fluentin.app/">
<link rel="icon" type="image/png" href="/icon.png">
{extra_meta}<style>{CSS}</style>
</head>"""


def nav(t, key):
    links = "".join(f'<a href="#{i}">{html.escape(n)}</a>' for n, i in zip(t["nav"], t["nav_ids"]))
    lang = " · ".join(f'<a href="{p}" class="{"active" if k == key else ""}">{lbl}</a>' for k, p, lbl in LANG_SWITCH)
    return f"""<nav><a class="brand" href="{t['path']}"><img src="/icon.png" alt="">FluentIn</a>
<div class="links">{links}<span class="lang">{lang}</span></div></nav>"""


def landing(key):
    t = T[key]
    icons = ["🎤", "3", "☺", "▶", "_", "⌨"]
    feats = "".join(f'<div class="feature"><div class="icon">{icons[i]}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for i, (h, p) in enumerate(t["features"]))
    steps = "".join(f'<div class="step"><div class="num">{i+1}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for i, (h, p) in enumerate(t["steps"]))
    verdicts = "".join(f'<div class="verdict {c}"><b>{html.escape(l)}</b>{html.escape(p)}</div>' for c, l, p in t["verdicts"])
    faq = "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in t["faq"])
    shots = "".join(f'<img src="/shots/{s}" alt="FluentIn screenshot" width="1290" height="2796" loading="lazy">' for s in t["shots"])
    redirect = ""
    if key == "en":
        redirect = """<script>(function(){var p=new URLSearchParams(location.search);if(p.get("lang")==="en")return;var s=null;try{s=localStorage.getItem("fluentin-lang")}catch(e){}if(s){if(s!=="/")location.replace(s);return}var L=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||""];for(var i=0;i<L.length;i++){var l=L[i].toLowerCase();if(/^zh/.test(l)){location.replace("/zh/");return}if(/^en/.test(l))return}})();</script>"""
    remember = """<script>document.addEventListener("click",function(e){var a=e.target.closest(".lang a");if(!a)return;try{localStorage.setItem("fluentin-lang",a.getAttribute("href"))}catch(e){}});</script>"""
    return f"""{head(t, "https://fluentin.app" + t['path'], redirect + remember)}
<body>
{nav(t, key)}
<header class="hero">
  <img class="app-icon" src="/icon.png" alt="FluentIn icon">
  <h1>{t['h1']}</h1>
  <p class="sub">{html.escape(t['sub'])}</p>
  <div class="badge">{html.escape(t['badge'])}</div>
  <div class="phones">{shots}</div>
</header>
<section class="features" id="features">
  <h2 class="section-title">{html.escape(t['features_title'])}</h2>
  <div class="features-grid">{feats}</div>
</section>
<section class="how" id="how">
  <h2 class="section-title">{html.escape(t['how_title'])}</h2>
  <p class="section-sub">{html.escape(t['how_sub'])}</p>
  <div class="steps">{steps}</div>
</section>
<div class="verdicts">{verdicts}</div>
<section class="privacy"><div class="privacy-card"><h2>{html.escape(t['privacy_h'])}</h2><p>{t['privacy_p']}</p></div></section>
<section class="faq" id="faq"><h2 class="section-title">{html.escape(t['faq_title'])}</h2><div class="faq">{faq}</div></section>
<div class="bottom-cta"><h2>{html.escape(t['cta_h'])}</h2><span class="cta pending">{html.escape(t['cta'])}</span></div>
<footer>© 2026 FluentIn · <a href="/privacy/">{t['footer_privacy']}</a> · <a href="/terms/">{t['footer_terms']}</a> · <a href="/support/">{t['footer_support']}</a> · <a href="mailto:hello@fluentin.app">hello@fluentin.app</a></footer>
</body></html>
"""


def legal(title, desc, updated, body_html):
    t = dict(T["en"], title=f"{title} — FluentIn", desc=desc)
    return f"""{head(t, "https://fluentin.app/" + title.lower().split()[0] + "/")}
<body>
<main class="legal">
  <a class="home" href="/">← FluentIn</a>
  <h1>{title}</h1>
  <div class="updated">Last updated: {updated} · Applies to FluentIn for iOS</div>
{body_html}
  <footer style="margin-top:3rem">© 2026 FluentIn · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/support/">Support</a></footer>
</main>
</body></html>
"""


PRIVACY = """
  <div class="card"><p><strong>The short version:</strong> FluentIn has no servers and no accounts. Speech is recognised on your device. The only network calls are the ones you opt into — an AI judge with your own API key, and YouTube's embedded player — and both go straight from your phone to that provider.</p></div>

  <h2>What we collect</h2>
  <p>Nothing that identifies you. FluentIn has no accounts, no analytics SDKs, no advertising, and no third-party trackers. We operate no server that your device talks to.</p>

  <h2>Microphone and speech recognition</h2>
  <p>When you hold the talk button, your speech is transcribed with Apple's Speech framework. Depending on your device and iOS settings, Apple may process speech on its servers under <a href="https://www.apple.com/legal/privacy/">Apple's privacy policy</a>. FluentIn does not record or store audio, and the transcript exists only for the current exercise.</p>

  <h2>Optional AI judge (your own API key)</h2>
  <p>In Settings you may paste your own API key for an AI provider (Gemini in the global edition; DeepSeek in the China edition). If you do, then only when the on-device matcher cannot decide, FluentIn sends the transcribed text of your answer and the exercise's phrase list directly from your device to that provider, under the provider's own privacy policy (<a href="https://policies.google.com/privacy">Google</a>, <a href="https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html">DeepSeek</a>). FluentIn never receives your key or your answers. The key is stored in your device's Keychain and is removed when you clear the field or delete the app.</p>

  <h2>YouTube clips</h2>
  <p>Some answers include a short clip played through YouTube's official embedded player. When a clip plays, YouTube (Google) receives the request under <a href="https://policies.google.com/privacy">its privacy policy</a>, exactly as if you opened the video in a browser. FluentIn does not download or store any media.</p>

  <h2>Data stored on your device</h2>
  <p>Your language and hint preferences are stored locally in the app's preferences; your API key, if any, in the Keychain. Deleting the app deletes them. Nothing is synced to a FluentIn account because there is none.</p>

  <h2>Children</h2>
  <p>FluentIn is intended for learners aged 13 and up and does not knowingly collect data from children. It collects no personal data from anyone.</p>

  <h2>Changes</h2>
  <p>If this policy changes, the new version is published at this address with a new date, and material changes are noted in the app's release notes.</p>

  <h2>Contact</h2>
  <p><a href="mailto:privacy@fluentin.app">privacy@fluentin.app</a></p>
"""

TERMS = """
  <h2>What FluentIn is</h2>
  <p>FluentIn is language-learning software: a speaking drill for regional slang and industry jargon in English. We provide the software and the drill content. We do not provide language instruction as a service, and no results are guaranteed.</p>

  <h2>Content</h2>
  <ul>
    <li>Phrases, situations and social cards are editorial content written and reviewed by us and by people who live in the region described. They describe how some people speak in some places at some times. Register, safety and currency notes are our best judgement, not guarantees; using a phrase is your call and your responsibility.</li>
    <li>Video clips are served by YouTube's embedded player from public YouTube videos under <a href="https://www.youtube.com/t/terms">YouTube's Terms of Service</a>. We do not host, download, alter or claim rights to them. If you own a video and want it removed from a card, write to us and we will.</li>
    <li>The FluentIn name, icon and drill content are ours. You may not copy the content into another product.</li>
  </ul>

  <h2>Your own API key</h2>
  <p>If you enable the AI judge you use your own account with a third-party provider (Google Gemini, or DeepSeek in the China edition). Their terms, pricing and availability apply; any charges they bill are yours. FluentIn is not a party to that relationship and cannot see or recover your key.</p>

  <h2>Acceptable use</h2>
  <p>Do not use FluentIn to harass or demean people, or to extract its content for redistribution. Do not attempt to circumvent the App Store's purchase or distribution rules.</p>

  <h2>Purchases</h2>
  <p>FluentIn is currently free. If paid features are introduced, they will be sold through the App Store under Apple's terms; pricing, billing, renewal and refunds are handled by Apple.</p>

  <h2>Warranty disclaimer</h2>
  <p>FluentIn is provided "as is", without warranty of any kind. Speech recognition, the on-device matcher and any AI judge make mistakes; a verdict is a learning aid, not an authority. We do not warrant that third-party services (Apple speech, YouTube, AI providers) remain available or accurate.</p>

  <h2>Limitation of liability</h2>
  <p>To the maximum extent permitted by law, we are not liable for indirect, incidental or consequential damages arising from use of FluentIn, including social outcomes of using a phrase. Our total liability for any claim is limited to the amount you paid for FluentIn in the twelve months preceding the claim.</p>

  <h2>Changes and termination</h2>
  <p>We may update these terms; the current version always lives at this address, and material changes will be noted in the app's release notes. You can stop using FluentIn at any time by deleting it, which removes all local data.</p>

  <h2>Contact</h2>
  <p><a href="mailto:hello@fluentin.app">hello@fluentin.app</a></p>
"""

SUPPORT = """
  <h2>Contact</h2>
  <p>Email <a href="mailto:support@fluentin.app">support@fluentin.app</a>. Include your iOS version and, if it concerns a specific phrase, the card shown on the answer screen.</p>

  <h2>Common questions</h2>
  <p><strong>The app didn't hear me.</strong> Hold the button for the whole phrase and release when you are done. Check Settings → Privacy &amp; Security → Microphone and Speech Recognition are on for FluentIn. In loud places, tap the blanked word and type instead.</p>
  <p><strong>It transcribed a standard word instead of the slang.</strong> Speech recognisers are trained on standard English. FluentIn biases them toward each card's phrase, but some words (yerrr, ock) still get "corrected". Try again, or type it.</p>
  <p><strong>What does the AI judge do?</strong> When the on-device check can't decide, your transcribed answer and the exercise's phrase list are sent to Gemini with the API key you pasted in Settings, and you get a verdict plus a one-line reason. Without a key, undecided answers count as wrong.</p>
  <p><strong>Testing my key says "Key rejected".</strong> Keys from <a href="https://aistudio.google.com/apikey">Google AI Studio</a> start with "AIza". Make sure the Generative Language API is enabled on that key and it has no application restrictions.</p>
  <p><strong>A clip is wrong or offensive.</strong> Clips are YouTube moments where a local says the phrase; some are machine-found and marked "unverified". Tell us the card and we will remove or replace it.</p>
  <p><strong>Something on a card is inaccurate.</strong> Every pack is reviewed by people who live there, and we still get things wrong. Corrections welcome at the address above.</p>
"""


def main():
    (ROOT / "shots").mkdir(exist_ok=True)
    for key in T:
        out = ROOT / T[key]["path"].strip("/") / "index.html" if key != "en" else ROOT / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(landing(key), encoding="utf-8")
    (ROOT / "privacy").mkdir(exist_ok=True); (ROOT / "terms").mkdir(exist_ok=True); (ROOT / "support").mkdir(exist_ok=True)
    (ROOT / "privacy/index.html").write_text(legal("Privacy Policy", "FluentIn privacy policy: no servers, no accounts, on-device speech; optional AI judge with your own API key.", LAST_UPDATED, PRIVACY), encoding="utf-8")
    (ROOT / "terms/index.html").write_text(legal("Terms of Service", "FluentIn terms of service.", LAST_UPDATED, TERMS), encoding="utf-8")
    (ROOT / "support/index.html").write_text(legal("Support", "FluentIn support: contact and common questions.", LAST_UPDATED, SUPPORT), encoding="utf-8")
    print("built: index, zh, privacy, terms, support")


if __name__ == "__main__":
    main()
