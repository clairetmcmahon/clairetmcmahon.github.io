#!/usr/bin/env python3
"""Build the public site with Python's standard library; no paid services needed."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'website/content.json').read_text())
ORIGIN = DATA['origin'].rstrip('/')
def e(value):
    return html.escape(str(value), quote=True)

def link(url, label, cls=''):
    return f'<a href="{e(url)}"' + (f' class="{cls}"' if cls else '') + f'>{e(label)}</a>'

def page(title, path, body, description, active=''):
    nav = ''.join(f'<a href="{url}"' + (' aria-current="page"' if active == name else '') + f'>{name}</a>' for name, url in [('About', '/'), ('Research', '/research/'), ('Blog', '/blog/'), ('Tools', '/tools/'), ('CV', '/cv/')])
    full_title = f'{title} | Claire McMahon' if title != 'Claire McMahon' else 'Claire McMahon | Economics · Harvard University'
    person = {'@context': 'https://schema.org', '@type': 'Person', 'name': DATA['name'], 'url': ORIGIN, 'jobTitle': 'Economics PhD student', 'affiliation': {'@type': 'CollegeOrUniversity', 'name': 'Harvard University'}}
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full_title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#f8f7f3">
<link rel="canonical" href="{ORIGIN}{path}"><link rel="icon" href="/assets/site/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{ORIGIN}{path}"><meta property="og:image" content="{ORIGIN}/images/headshot.png">
<link rel="stylesheet" href="/assets/site/style.css"><script type="application/ld+json">{json.dumps(person)}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="wordmark" href="/">Claire McMahon<span class="brand-dot" aria-hidden="true">.</span></a><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main">{body}</main>
<footer class="site-footer"><div><a class="footer-name" href="/">Claire McMahon</a><span>Economics · Harvard University</span></div><a href="mailto:{DATA['email']}">Get in touch <span aria-hidden="true">↗</span></a></footer></body></html>'''

def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')

def paper(p, compact=False):
    co = f'<p class="coauthors">With {e(p["coauthors"])}</p>' if p['coauthors'] else ''
    controls = '<div class="paper-links">' + ''.join(link(u, t) for t, u in p['links']) + '</div>'
    abstract = f'<details><summary>Abstract</summary><p>{e(p["abstract"])}</p></details>'
    return f'<article class="paper" id="{p["id"]}"><p class="eyebrow">{e(p["venue"])}</p><h3>{link(p["url"], p["title"])}</h3>{co}<p class="paper-summary">{e(p["summary"])}</p>' + ('' if compact else abstract) + controls + '</article>'

def intro(kicker, title, subtitle):
    return f'<div class="page-intro"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{subtitle}</p></div>'

atlas_art = '<svg viewBox="0 0 320 150" fill="none" aria-hidden="true"><g stroke="currentColor" stroke-width="1"><circle cx="160" cy="75" r="58"/><circle cx="160" cy="75" r="39"/><path d="M160 7v136M92 75h136M119 34l82 82M119 116l82-82" opacity=".35"/><path d="m180 37-11 47-29 29 11-47z" fill="currentColor" fill-opacity=".12"/><path d="m160 75 20-38-11 47z" fill="currentColor"/></g><circle cx="160" cy="75" r="3" fill="currentColor"/></svg>'
sizing_art = '<svg viewBox="0 0 320 150" fill="none" aria-hidden="true"><g stroke="currentColor" stroke-width="1"><path d="M68 24v100h186"/><path d="M70 121c20-2 43-8 63-28s39-48 61-58 42-12 58-13" stroke-width="2"/><path d="M158 124V70h95" stroke-dasharray="4 5" opacity=".5"/><circle cx="158" cy="70" r="5" fill="currentColor"/></g></svg>'

def tool_cards():
    return f'''<div class="tools-grid"><article class="tool-card"><div class="tool-art">{atlas_art}</div><div class="tool-copy"><p class="eyebrow">Innovation funding</p><h2><a href="https://atlasofinnovation.org/">The Atlas of Innovation <span aria-hidden="true">↗</span></a></h2><p>Explore funding mechanisms for frontier R&amp;D. A toolkit to help policymakers and philanthropists match the way they fund innovation to the problem they want to solve.</p><a class="text-link" href="https://atlasofinnovation.org/">Explore the Atlas <span aria-hidden="true">↗</span></a></div></article>
<article class="tool-card"><div class="tool-art sizing">{sizing_art}</div><div class="tool-copy"><p class="eyebrow">Market shaping</p><h2><a href="https://www.marketshapingaccelerator.org/pull-incentive-sizing-tool/">Pull Incentive Sizing Tool <span aria-hidden="true">↗</span></a></h2><p>A practical guide and interactive calculator for estimating the incentives needed to accelerate innovation, accounting for development costs, risk, and time.</p><a class="text-link" href="https://www.marketshapingaccelerator.org/pull-incentive-sizing-tool/">Explore the tool <span aria-hidden="true">↗</span></a></div></article></div>'''

home = f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">Economics · Harvard University</p><h1>Claire McMahon</h1><p class="hero-lede">I study incentives for innovation<br class="desktop-break"> and global health.</p><div class="bio"><p>I am a PhD student in economics at Harvard University. My research explores how market shaping can encourage innovation for global health and pandemic preparedness.</p><p>Previously, I was a research professional at the <a href="https://www.marketshapingaccelerator.org/">Market Shaping Accelerator</a> at the University of Chicago. I graduated from Dartmouth College with a BA in Mathematics and Economics.</p></div><div class="hero-links"><a href="mailto:{DATA['email']}">Email <span aria-hidden="true">↗</span></a><a href="/files/McMahon_CV.pdf">Curriculum vitae <span class="file-label">PDF</span></a><a href="https://scholar.google.com/citations?user=wQ_D6bgAAAAJ&amp;hl=en">Google Scholar <span aria-hidden="true">↗</span></a></div></div><figure class="portrait"><img src="/images/headshot.png" alt="Claire McMahon" width="1700" height="1945" fetchpriority="high"><figcaption>Cambridge, Massachusetts</figcaption></figure></section>
<section class="home-section"><div class="section-heading"><h2>Recent research</h2><a class="text-link" href="/research/">All research <span aria-hidden="true">→</span></a></div>{paper(DATA['papers'][0], True)}</section>
<section class="home-section"><div class="section-heading"><h2>Research into practice</h2><a class="text-link" href="/tools/">Tools <span aria-hidden="true">→</span></a></div><p class="section-note">Resources for designing and funding innovation.</p>{tool_cards()}</section>'''
write('index.html', page('Claire McMahon', '/', home, 'Claire McMahon is a Harvard economics PhD student studying incentives for innovation, global health, and pandemic preparedness.', 'About'))

research = intro('Research', 'Papers &amp; publications', 'Innovation, global health, and the design of incentives.')
for category in ['Working papers', 'Publications']:
    research += f'<section class="research-section"><h2 class="section-label">{category}</h2><div>' + ''.join(paper(p) for p in DATA['papers'] if p['category'] == category) + '</div></section>'
write('research/index.html', page('Research', '/research/', research, 'Research and working papers by Claire McMahon on innovation, global health, and economic opportunity.', 'Research'))

blog = intro('Blog', 'Ideas in practice', 'Writing on innovation, market shaping, and global health.')
for year in ['2025', '2024']:
    blog += f'<section class="research-section blog-section"><h2 class="section-label">{year}</h2><div>'
    for p in DATA['posts']:
        if p['year'] != year:
            continue
        byline = f'<p class="coauthors">With {e(p["coauthors"])}</p>' if p['coauthors'] else ''
        blog += f'<article class="post"><p class="eyebrow">{e(p["publisher"])} · {e(p["date"])}</p><h2>{link(p["url"], p["title"])}</h2>{byline}<a class="text-link" href="{e(p["url"])}">Read post <span aria-hidden="true">↗</span></a></article>'
    blog += '</div></section>'
write('blog/index.html', page('Blog', '/blog/', blog, 'Blog posts by Claire McMahon on pandemic preparedness, vaccines, and neonatal sepsis diagnostics.', 'Blog'))

tools = intro('Tools', 'Research into practice', 'Practical resources for policymakers, philanthropists, and innovation funders.') + tool_cards() + '<p class="tools-footnote">Developed with collaborators at the Market Shaping Accelerator and partner organizations. Full contributor details are available on each project’s website.</p>'
write('tools/index.html', page('Tools', '/tools/', tools, 'Explore the Atlas of Innovation and Pull Incentive Sizing Tool.', 'Tools'))

cv = intro('Curriculum vitae', 'CV', 'Education, research, and professional experience.') + '<div class="cv-actions"><a class="button" href="/files/McMahon_CV.pdf">Open CV <span aria-hidden="true">↗</span></a><a class="text-link" href="/files/McMahon_CV.pdf" download="Claire-McMahon-CV.pdf">Download PDF <span aria-hidden="true">↓</span></a></div><object class="cv-viewer" data="/files/McMahon_CV.pdf" type="application/pdf" aria-label="Claire McMahon’s curriculum vitae"><p><a href="/files/McMahon_CV.pdf">Open the CV as a PDF.</a></p></object>'
write('cv/index.html', page('CV', '/cv/', cv, 'Curriculum vitae of Claire McMahon, Economics PhD student at Harvard University.', 'CV'))
write('404.html', page('Page not found', '/404.html', intro('404', 'A different direction.', 'This page may have moved. You can find my work in the links below.') + '<div class="recovery-links"><a class="button" href="/">Back to home</a><a class="text-link" href="/research/">Browse research →</a></div>', 'Find research, writing, and tools by Claire McMahon.'))

def redirect(path, destination):
    write(path, f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page moved | Claire McMahon</title><link rel="canonical" href="{e(destination)}"><meta http-equiv="refresh" content="0;url={e(destination)}"></head><body><p>This page has moved. <a href="{e(destination)}">Continue to the page</a>.</p></body></html>')
for alias, destination in [('about/index.html', '/'), ('about.html', '/'), ('research.html', '/research/'), ('blog-posts/index.html', '/blog/'), ('cv.html', '/cv/')]:
    redirect(alias, destination)
for p in DATA['papers']:
    redirect(f'publications/{p["id"]}/index.html', p['url'])
for p in DATA['posts']:
    redirect(f'posts/{p["year"]}/{p["id"]}/index.html', p['url'])
paths = ['/', '/research/', '/blog/', '/tools/', '/cv/']
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{ORIGIN}{p}</loc></url>' for p in paths) + '</urlset>\n')
write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
write('.nojekyll', '')
print('Built 5 main pages, 404, legacy redirects, sitemap, and robots.txt.')
