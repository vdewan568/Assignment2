"""Generates the five static HTML pages so header/footer stay identical.
Run:  python3 build_pages.py   (output: index.html, lawyer.html, expertise.html, articles.html, contact.html)
The generated files are plain HTML: you can edit them directly afterwards."""

import json, pathlib

OUT = pathlib.Path(__file__).parent

NAV = [
    ("index.html", "Home", "home"),
    ("lawyer.html", "Meet the lawyer", "lawyer"),
    ("expertise.html", "Expertise", "expertise"),
    ("articles.html", "Articles", "articles"),
    ("contact.html", "Contact us", "contact"),
]

MAP_URL = ("https://www.openstreetmap.org/export/embed.html?bbox=57.4793%2C-20.2507%2C57.4993%2C-20.2367"
           "&layer=mapnik&marker=-20.2437%2C57.4893")
MAP_LINK = "https://www.openstreetmap.org/?mlat=-20.2437&mlon=57.4893#map=15/-20.2437/57.4893"

AREAS = [
    ("family", "Family Law", "Divorce, custody, maintenance and family disputes handled with care.",
     "Family disputes are personal and often urgent. Abdallah explains your options plainly, protects your position and aims for outcomes that last, through negotiation where possible and in court where necessary.",
     ["Divorce and separation", "Child custody and access", "Maintenance and support", "Property and family settlements"]),
    ("criminal", "Criminal Law", "Representation from the first police interview through trial and appeal.",
     "Early advice can shape the whole case. Abdallah acts for individuals facing criminal allegations, from the first police interview through to trial and appeal.",
     ["Police interviews and bail", "Defence at trial", "Appeals", "Advice on charges and procedure"]),
    ("labour", "Labour and Employment Law", "Dismissal, contracts, redundancy and workplace disputes.",
     "Work is central to your income and your wellbeing. Abdallah advises employees and employers on rights, obligations and the fairest way to resolve a dispute.",
     ["Unfair or unlawful dismissal", "Employment contracts and terms", "Redundancy and severance", "Workplace disputes and procedures"]),
    ("tenancy", "Tenancy and Rental Law", "Lease disputes, evictions, deposits and rent arrears.",
     "Whether you rent a home or let a property, clear rights and a clear lease prevent most problems. When a dispute does arise, Abdallah acts quickly and practically.",
     ["Lease review and advice", "Eviction and notices", "Deposits and arrears", "Repairs and property condition"]),
    ("commercial", "Commercial Law", "Practical legal support for businesses, from set-up to trade disputes.",
     "Businesses need advice that is quick, commercial and easy to act on. Abdallah supports owners and managers on the legal side of running and growing a company.",
     ["Business set-up advice", "Supplier and customer agreements", "Partnership and shareholder disputes", "Debt recovery"]),
    ("contracts", "Contractual Disputes", "Breach of contract, non-payment and disagreements over what was agreed.",
     "When an agreement is not honoured, the right first step matters. Abdallah reviews the contract, explains your position and pursues the remedy that makes sense.",
     ["Breach and non-performance", "Payment disputes", "Termination of contracts", "Damages and remedies"]),
    ("litigation", "Litigation and Arbitration", "Advocacy before all levels of court and in international arbitration.",
     "Abdallah has appeared before all levels of court and has handled more than 100 international arbitrations. Cases are prepared thoroughly and argued with clarity.",
     ["Civil litigation", "Appeals", "International arbitration", "Enforcement of judgments and awards"]),
    ("mediation", "Mediation", "A faster, lower-cost route to settle disputes without a trial.",
     "Many disputes are best settled early. Mediation is private, quicker and often far less costly than a trial, and it keeps control of the outcome in your hands.",
     ["Family mediation", "Commercial mediation", "Settlement agreements", "Preparing for mediation"]),
    ("drafting", "Contract Drafting", "Clear, enforceable agreements that prevent disputes before they start.",
     "A well-drafted contract is the cheapest legal protection there is. Abdallah drafts and reviews agreements so that each party knows exactly what is promised.",
     ["Employment and service agreements", "Commercial and supply contracts", "Lease agreements", "Review and negotiation of terms"]),
]

# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------
THEME_SCRIPT = ("<script>try{var t=localStorage.getItem('theme');"
                "if(!t&&window.matchMedia('(prefers-color-scheme: dark)').matches){t='dark'}"
                "if(t){document.documentElement.setAttribute('data-theme',t)}}catch(e){}"
                "document.documentElement.classList.add('js');</script>")

BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2.6" '
              'stroke-linecap="round" aria-hidden="true"><path d="M7 35V19a13 13 0 0 1 26 0v16"/>'
              '<path d="M14 35V20a6 6 0 0 1 12 0v15"/></svg>')


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#F6F8F7">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="css/style.css">
  {THEME_SCRIPT}
</head>"""


def header(page):
    items = ""
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == page else ""
        items += f'          <li><a href="{href}"{cur}>{label}</a></li>\n'
    return f"""<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap bar">
      <a class="brand" href="index.html" aria-label="abdallah consultancy firm, home">
        {BRAND_MARK}
        <span class="brand-name">abdallah<small>consultancy firm</small></span>
      </a>

      <nav class="nav" id="nav" aria-label="Main">
        <ul>
{items}          <li class="nav-cta"><a class="btn" href="contact.html#form">Schedule a legal consultation</a></li>
        </ul>
      </nav>

      <div class="bar-actions">
        <button class="icon-btn theme-toggle" type="button" aria-pressed="false" aria-label="Switch to dark mode">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </button>
        <a class="btn btn-sm bar-cta" href="contact.html#form">Book a consultation</a>
        <button class="icon-btn nav-toggle" type="button" aria-expanded="false" aria-controls="nav">
          <span class="visually-hidden">Open menu</span><span></span><span></span><span></span>
        </button>
      </div>
    </div>
    <div class="progress" aria-hidden="true"></div>
  </header>
"""


def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l, _ in NAV)
    return f"""
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="brand" href="index.html" aria-label="abdallah consultancy firm, home">
            {BRAND_MARK}
            <span class="brand-name">abdallah<small>consultancy firm</small></span>
          </a>
          <p class="footer-about">Legal services with high professionalism and outstanding results.</p>
        </div>
        <div>
          <h2>Explore</h2>
          <ul>{links}</ul>
        </div>
        <div>
          <h2>Get in touch</h2>
          <ul>
            <li><a href="tel:+23057995620">+230 57995620</a></li>
            <li><a href="mailto:abdallah@gmail.com">abdallah@gmail.com</a></li>
            <li>1 Example Street, Port Louis</li>
          </ul>
        </div>
      </div>
      <p class="disclaimer">Information on this website is general in nature and does not constitute legal advice.</p>
      <p class="copyright">&copy; 2026 abdallah consultancy firm. Member of the International Bar Society and the National Bar Council.</p>
    </div>
  </footer>

  <button class="to-top" type="button" aria-label="Back to top">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
  </button>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
"""


def cta_band(title="Need advice on a legal matter?", text="Tell us what is happening and we will explain your options."):
    return f"""
    <section class="block block--deep" aria-labelledby="cta-title">
      <div class="wrap cta">
        <div>
          <h2 id="cta-title">{title}</h2>
          <p>{text}</p>
        </div>
        <a class="btn btn-gold" href="contact.html#form">Schedule a legal consultation</a>
      </div>
    </section>
"""


def map_block(caption="Ebene, Mauritius"):
    # Marker is placed in Ebene. Adjust the lat/lon in the URL to the confirmed office location.
    return f"""<figure class="map">
            <iframe title="Map showing the office location in Ebene, Mauritius" src="{MAP_URL}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </figure>
          <p class="map-caption">{caption}. <a href="{MAP_LINK}" target="_blank" rel="noopener">Open a larger map<span class="visually-hidden"> (opens in a new tab)</span></a></p>"""


def faq(items):
    out = '<div class="faq">\n'
    for i, (q, a) in enumerate(items, 1):
        out += f"""        <div class="faq-item">
          <h3><button class="faq-q" type="button" id="faq-q{i}" aria-expanded="false" aria-controls="faq-a{i}">{q}</button></h3>
          <div class="faq-a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}"><div><p>{a}</p></div></div>
        </div>
"""
    return out + "      </div>"


def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name)


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------
def home():
    area_links = "".join(
        f'<a class="area-link" href="expertise.html#{i}"><h3>{n}</h3><p>{s}</p></a>\n          ' for i, n, s, _, _ in AREAS)
    return head("abdallah consultancy firm | Barrister in Port Louis, Mauritius",
                "Legal services with high professionalism and outstanding results. Barrister Abdallah acts in court, arbitration and mediation.") + header("home") + f"""
  <main id="main" tabindex="-1">

    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <h1 id="hero-title">Legal services with high professionalism and outstanding results.</h1>
          <p class="lead">Abdallah is a barrister with a domestic and international practice who has appeared before all levels of court.</p>
          <div class="hero-actions">
            <a class="btn" href="contact.html#form">Schedule a legal consultation</a>
            <a class="btn btn-ghost" href="expertise.html">See areas of expertise</a>
          </div>
        </div>
        <figure class="hero-media">
          <!-- Replace with a royalty-free portrait (Unsplash / Pexels), saved as WebP -->
          <div class="arch"><img src="assets/portrait-placeholder.svg" width="520" height="650" alt="Placeholder portrait of Abdallah, barrister"></div>
          <figcaption class="hero-badge"><strong>National Bar Council</strong>and International Bar Society member</figcaption>
        </figure>
      </div>
    </section>

    <div class="wrap">
      <div class="stats">
        <div class="stat"><span class="stat-num" data-count="200" data-suffix="+">200+</span><span class="stat-label">clients acted for</span></div>
        <div class="stat"><span class="stat-num" data-count="200" data-suffix="+">200+</span><span class="stat-label">litigation cases handled</span></div>
        <div class="stat"><span class="stat-num" data-count="100" data-suffix="+">100+</span><span class="stat-label">international arbitrations</span></div>
      </div>
    </div>

    <section class="block" aria-labelledby="services-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="services-title">Nine areas of practice, one point of contact</h2>
          <p>Choose an area to see the kinds of matters Abdallah handles.</p>
        </div>
        <div class="area-list reveal">
          {area_links}</div>
      </div>
    </section>

    <section class="block block--tint" aria-labelledby="reviews-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="reviews-title">What clients say</h2>
        </div>
        <div class="slider" data-slider role="group" aria-roledescription="carousel" aria-label="Client reviews">
          <div class="viewport">
            <div class="slides">
              <div class="slide"><figure class="quote">
                <blockquote><p>Clear advice at every step. I always knew what was happening with my case and what came next.</p></blockquote>
                <figcaption><strong>Client name</strong><span class="tag">Placeholder review</span></figcaption>
              </figure></div>
              <div class="slide"><figure class="quote">
                <blockquote><p>Calm, prepared and direct. The hearing went exactly as we had discussed beforehand.</p></blockquote>
                <figcaption><strong>Client name</strong><span class="tag">Placeholder review</span></figcaption>
              </figure></div>
              <div class="slide"><figure class="quote">
                <blockquote><p>A difficult dispute settled quickly, and without the stress I expected.</p></blockquote>
                <figcaption><strong>Client name</strong><span class="tag">Placeholder review</span></figcaption>
              </figure></div>
            </div>
          </div>
          <div class="slider-controls">
            <button class="icon-btn slider-prev" type="button" aria-label="Previous review"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>
            <div class="dots"></div>
            <button class="icon-btn slider-next" type="button" aria-label="Next review"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
            <button class="btn btn-ghost btn-sm slider-pause" type="button" aria-pressed="false">Pause</button>
          </div>
        </div>
      </div>
    </section>
{cta_band()}
    <section class="block" aria-labelledby="visit-title">
      <div class="wrap split">
        <div>
          <h2 id="visit-title">Visit us in Ebene</h2>
          <p class="lead">Meet in person or arrange a call. Send your details and we will confirm a time.</p>
          <dl class="details">
            <div><dt>Phone</dt><dd><a href="tel:+23057995620">+230 57995620</a></dd></div>
            <div><dt>Email</dt><dd><a href="mailto:abdallah@gmail.com">abdallah@gmail.com</a></dd></div>
            <div><dt>Address</dt><dd>1 Example Street, Port Louis</dd></div>
          </dl>
        </div>
        <div>
          {map_block()}
        </div>
      </div>
    </section>

  </main>
""" + footer()


# --------------------------------------------------------------------------
# Meet the lawyer
# --------------------------------------------------------------------------
def lawyer():
    return head("Meet the lawyer | abdallah consultancy firm",
                "Abdallah is an experienced barrister with domestic and international practice, 200+ clients and 100+ international arbitrations.") + header("lawyer") + f"""
  <main id="main" tabindex="-1">

    <section class="page-head">
      <div class="wrap">
        <h1>Meet the lawyer</h1>
        <p class="lead">An experienced barrister with domestic and international practice.</p>
      </div>
    </section>

    <section class="block" aria-labelledby="bio-title" style="padding-top:1rem">
      <div class="wrap split split--top">
        <figure class="hero-media" style="margin:0">
          <!-- Replace with a royalty-free portrait (Unsplash / Pexels), saved as WebP -->
          <div class="arch"><img src="assets/portrait-placeholder.svg" width="520" height="650" alt="Placeholder portrait of Abdallah, barrister" loading="lazy"></div>
        </figure>
        <div>
          <h2 id="bio-title">Biography</h2>
          <p>Abdallah is an experienced barrister with a domestic and international practice who has appeared before all levels of court.</p>
          <p>Abdallah has acted for more than 200 clients, handled more than 200 litigation cases and conducted more than 100 international arbitrations. Abdallah is also a regular legal commentator in the media.</p>
          <p>Clients choose Abdallah for professionalism, preparation and results. Every matter starts with a clear explanation of your options, and ends with a result you can rely on.</p>
          <a class="btn" href="contact.html#form">Schedule a legal consultation</a>
        </div>
      </div>
    </section>

    <section class="block block--tint" aria-labelledby="hl-title">
      <div class="wrap">
        <div class="section-head"><h2 id="hl-title">Highlights</h2></div>
        <div class="highlights reveal">
          <div class="hl"><strong data-count="200" data-suffix="+">200+</strong><span>clients acted for</span></div>
          <div class="hl"><strong data-count="200" data-suffix="+">200+</strong><span>litigation cases handled</span></div>
          <div class="hl"><strong data-count="100" data-suffix="+">100+</strong><span>international arbitrations</span></div>
          <div class="hl"><strong>All levels of court</strong><span>appearances in domestic and international matters</span></div>
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="mem-title">
      <div class="wrap">
        <div class="section-head"><h2 id="mem-title">Memberships</h2></div>
        <div class="member-list">
          <div class="member"><h3>International Bar Society</h3><p>Member</p></div>
          <div class="member"><h3>National Bar Council</h3><p>Member</p></div>
        </div>
      </div>
    </section>

    <section class="block block--tint" aria-labelledby="media-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="media-title">Media appearances</h2>
          <p>Abdallah is a regular legal commentator. The entries below are placeholders until real appearances are added.</p>
        </div>
        <ul class="media-list">
          <li><span>Television interview on a current legal topic</span><span class="tag">Placeholder</span></li>
          <li><span>Radio commentary on a recent court ruling</span><span class="tag">Placeholder</span></li>
          <li><span>Newspaper legal column</span><span class="tag">Placeholder</span></li>
        </ul>
      </div>
    </section>
{cta_band()}
  </main>
""" + footer()


# --------------------------------------------------------------------------
# Expertise
# --------------------------------------------------------------------------
def expertise():
    nav = "".join(f'<li><a href="#{i}">{n}</a></li>' for i, n, *_ in AREAS)
    sections = ""
    for i, n, _s, long, matters in AREAS:
        lis = "".join(f"<li>{m}</li>" for m in matters)
        sections += f"""
          <section class="area reveal" id="{i}" aria-labelledby="{i}-h">
            <h2 id="{i}-h">{n}</h2>
            <p>{long}</p>
            <ul class="matters">{lis}</ul>
            <a class="btn btn-ghost" href="contact.html?area={i}#form">Ask about {n.lower()}</a>
          </section>
"""
    return head("Expertise | abdallah consultancy firm",
                "Family, criminal, labour, tenancy, commercial, contractual, litigation, arbitration, mediation and contract drafting.") + header("expertise") + f"""
  <main id="main" tabindex="-1">

    <section class="page-head">
      <div class="wrap">
        <h1>Areas of expertise</h1>
        <p class="lead">Nine practice areas covering disputes, advice and documents for individuals and businesses.</p>
      </div>
    </section>

    <div class="wrap areas-layout" style="padding-bottom:4rem">
      <nav class="area-nav" aria-label="Practice areas"><ul>{nav}</ul></nav>
      <div>{sections}      </div>
    </div>
{cta_band()}
  </main>
""" + footer()


# --------------------------------------------------------------------------
# Articles
# --------------------------------------------------------------------------
def articles():
    fallback = (OUT / "data" / "articles.json").read_text(encoding="utf-8").replace("</", "<\\/")
    return head("Articles | abdallah consultancy firm",
                "General legal information on family, tenancy, mediation and more, written in plain language.") + header("articles") + f"""
  <main id="main" tabindex="-1">

    <section class="page-head">
      <div class="wrap">
        <h1>Articles</h1>
        <p class="lead">General legal information in plain language. Articles load from <code>data/articles.json</code>, so adding one is a single entry.</p>
      </div>
    </section>

    <section class="block" style="padding-top:1rem" aria-label="Article list">
      <div class="wrap">
        <div class="toolbar">
          <div class="chips" id="article-chips" role="group" aria-label="Filter by topic"></div>
          <div class="field search">
            <label class="visually-hidden" for="article-search">Search articles</label>
            <input type="text" id="article-search" placeholder="Search articles" autocomplete="off">
          </div>
        </div>
        <p class="count" id="article-count" role="status" aria-live="polite">Loading articles…</p>
        <div class="cards" id="article-cards"></div>
      </div>
    </section>

    <dialog id="article-dialog" aria-labelledby="dlg-title">
      <button class="icon-btn dlg-close" type="button" aria-label="Close article">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
      <div class="dlg-body" id="dlg-content"></div>
    </dialog>

    <script type="application/json" id="articles-fallback">{fallback}</script>
{cta_band("Have a question about your own situation?", "General articles cannot replace advice on your case. Tell us what is happening.")}
  </main>
""" + footer()


# --------------------------------------------------------------------------
# Contact
# --------------------------------------------------------------------------
def contact():
    opts = "".join(f'<option value="{i}">{n}</option>' for i, n, *_ in AREAS)
    check = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M8 12.5l3 3 5-6"/></svg>'
    faqs = faq([
        ("How do I schedule a consultation?", "Complete the form on this page or call +230 57995620. Say which practice area your matter falls under and we will suggest a time."),
        ("What should I include in my message?", "Describe what happened, who is involved and any deadlines or court dates. Please do not send original documents or sensitive personal data through this form."),
        ("Does sending a message create a lawyer-client relationship?", "No. A lawyer-client relationship begins only when an engagement has been agreed. Information on this website is general in nature and does not constitute legal advice."),
        ("What if my matter is urgent?", "Call +230 57995620 and mention any court dates or deadlines in your message."),
    ])
    return head("Contact us | abdallah consultancy firm",
                "Schedule a legal consultation with Abdallah, barrister. Phone +230 57995620, email abdallah@gmail.com.") + header("contact") + f"""
  <main id="main" tabindex="-1">

    <section class="page-head">
      <div class="wrap">
        <h1>Contact us</h1>
        <p class="lead">Tell us about your matter and we will reply with the next step.</p>
      </div>
    </section>

    <section class="block" style="padding-top:1rem" aria-label="Contact form and details">
      <div class="wrap split split--top">
        <div id="form" style="scroll-margin-top:6rem">
          <form id="contact-form" novalidate>
            <div class="form-grid">
              <div class="field">
                <label for="name">Full name</label>
                <input type="text" id="name" name="name" autocomplete="name" required aria-describedby="name-error">
                <p class="error" id="name-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" autocomplete="email" required aria-describedby="email-error">
                <p class="error" id="email-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="phone">Phone</label>
                <input type="tel" id="phone" name="phone" autocomplete="tel" placeholder="+230 5xxx xxxx" required aria-describedby="phone-error">
                <p class="error" id="phone-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="area">Practice area</label>
                <select id="area" name="area" required aria-describedby="area-error">
                  <option value="">Select an area</option>
                  {opts}
                  <option value="other">Other or not sure</option>
                </select>
                <p class="error" id="area-error" aria-live="polite"></p>
              </div>
              <div class="field field-full">
                <label for="message">Message</label>
                <textarea id="message" name="message" maxlength="1000" required aria-describedby="message-error message-count"></textarea>
                <p class="hint"><span class="error" id="message-error" aria-live="polite"></span><span id="message-count">0 / 1000</span></p>
              </div>
              <div class="field field-full">
                <div class="check">
                  <input type="checkbox" id="consent" name="consent" required aria-describedby="consent-error">
                  <label for="consent">I agree that my details may be used to reply to this enquiry, and I understand that sending this form does not create a lawyer-client relationship.</label>
                </div>
                <p class="error" id="consent-error" aria-live="polite"></p>
              </div>
              <div class="field-full"><button class="btn" type="submit">Send message</button></div>
            </div>
          </form>

          <div class="success" id="form-success" role="status" tabindex="-1" hidden>
            {check}
            <h2>Message received</h2>
            <p>Thank you, <span id="success-name"></span>. Abdallah's office will reply to <strong id="success-email"></strong> as soon as possible.</p>
            <button class="btn btn-ghost" type="button" id="send-another">Send another message</button>
          </div>
        </div>

        <div>
          <h2>Office details</h2>
          <dl class="details">
            <div><dt>Phone</dt><dd><a href="tel:+23057995620">+230 57995620</a></dd></div>
            <div><dt>Email</dt><dd><a href="mailto:abdallah@gmail.com">abdallah@gmail.com</a></dd></div>
            <div><dt>Address</dt><dd>1 Example Street, Port Louis</dd></div>
          </dl>
          <div style="margin-top:2rem">
            {map_block()}
          </div>
        </div>
      </div>
    </section>

    <section class="block block--tint" aria-labelledby="faq-title">
      <div class="wrap">
        <div class="section-head"><h2 id="faq-title">Before you get in touch</h2></div>
        {faqs}
      </div>
    </section>

  </main>
""" + footer()


if __name__ == "__main__":
    write("index.html", home())
    write("lawyer.html", lawyer())
    write("expertise.html", expertise())
    write("articles.html", articles())
    write("contact.html", contact())
