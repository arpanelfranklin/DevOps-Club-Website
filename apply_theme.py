#!/usr/bin/env python3
"""DevOps Club: logo placement + purple/blue re-theme.
Usage:  python3 apply_theme.py [index.html]
Makes index.html.bak first. Prints anything it could not find."""
import re, sys, shutil

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(path, encoding='utf-8').read()
if 'DEVOPS THEME' in s:
    sys.exit('Already patched.')
shutil.copy(path, path + '.bak')
miss = []

def R(old, new, rx=False, glob=False):
    global s
    n = len(re.findall(old, s)) if rx else s.count(old)
    if n == 0 or (n > 1 and not glob):
        miss.append(old[:70]); return
    s = re.sub(old, lambda m: new, s) if rx else s.replace(old, new)

# ── 1. Colours: seed palette -> logo palette ─────────────────────
R('#ef493c', 'var(--accent)', glob=True)
R('#241a12', '#0b0a14', glob=True)
R('#e7e2d8', '#ecebf3', glob=True)
R('#fffdf8', '#fbfaff', glob=True)
R('rgba(255,253,248,', 'rgba(251,250,255,', glob=True)
R("ctx.strokeStyle = `rgba(239,73,60,${s.alpha})`;",
  "ctx.strokeStyle = `rgba(${s.phase > Math.PI ? '91,155,213' : '169,123,255'},${s.alpha})`;")
R("'rgba(239,73,60,.18)'", "'rgba(109,47,201,.2)'")
R("'rgba(23,23,23,.08)'", "'rgba(91,155,213,.18)'")

# ── 2. Head: title, favicon, link preview ────────────────────────
R(r'<title>.*?</title>', '''<title>DevOps Club — Bennett University</title>
<meta name="description" content="DevOps Club of Bennett University: workshops, hackathons and a student community for cloud, CI/CD and GitOps." />
<meta name="theme-color" content="#0b0a14" />
<link rel="icon" type="image/png" href="img/favicon.png" />
<meta property="og:title" content="DevOps Club — Bennett University" />
<meta property="og:description" content="Learn, build, automate and scale. Open to all students." />
<meta property="og:image" content="https://YOUR-DOMAIN/img/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />''', rx=True)

# ── 3. Nav ───────────────────────────────────────────────────────
R('<a href="#" class="nav-mark" data-rev style="--d:0ms">Fallow <span>Row</span></a>',
  '<a href="#" class="nav-mark" data-rev style="--d:0ms"><img src="img/devops-logo.png" alt="" class="nav-logo">DevOps <span>Club</span></a>')
R('>Varieties</a>', '>Positions</a>')
R('>Packets</a>', '>About</a>')
R('>Seasons</a>', '>Journey</a>')
R('>Pricing</a>', '>Events</a>')
R('aria-label="Varieties"', 'aria-label="Positions"')

# ── 4. Hero ──────────────────────────────────────────────────────
R(r'aria-label="Fallow Row[^"]*"', 'aria-label="DevOps Club of Bennett University"', rx=True)
R('<div class="hero-eyebrow t-display" id="hero-eyebrow">',
  '<img src="img/devops-logo.png" alt="DevOps Club logo" class="hero-logo">\n      <div class="hero-eyebrow t-display" id="hero-eyebrow">')
R('Est. 2016 · Noida', 'Bennett University · Greater Noida')
R('Open-Pollinated · Untreated', 'Open to All · Free Workshops')

# ── 5. About packet: logo badge + real copy (replaces seed data) ─
R('<canvas class="packet-plate" id="packet-plate" aria-hidden="true"></canvas>',
  '<img class="packet-plate" src="img/devops-logo.png" alt="DevOps Club logo">')
R(r"lot:\s+'[^']*'", "lot:  'ACTIVE'", rx=True)
R(r"germ:\s+'[^']*'", "germ: 'Cloud & DevOps'", rx=True)
R(r"sow:\s+'[^']*'", "sow:  'Open To All'", rx=True)
R(r"date:\s+'[^']*'", "date: 'Deploy Success'", rx=True)
R('Variety confirmed: Mortgage Lifter', 'Learn & Build: workshops from zero')
R('Germination result: 94% viable', 'Automate & Scale: CI/CD and IaC')
R('Lot assigned: FRW-2601', 'Open source culture: ship in public')
R('Packet sealed. Ready to ship.', 'Peer collaboration: learn together')

# ── 6. Footer ────────────────────────────────────────────────────
R('<div class="footer-brand-name">DevOps <span>Club</span></div>',
  '<div class="footer-brand-name"><img src="img/devops-logo.png" alt="" class="footer-logo">DevOps <span>Club</span></div>')
R('Bennet University', 'Bennett University')

# ── 7. CSS ───────────────────────────────────────────────────────
CSS = r'''
/* ═══ DEVOPS THEME — logo palette ═══ */
:root { --accent:#6d2fc9; --blue:#5b9bd5; }
#stage-hero, #stage-artifact, footer, nav { --accent:#a97bff; }
.packet { --accent:#6d2fc9; }

nav {
  background: rgba(11,10,20,.72);
  -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(251,250,255,.08);
  padding-block: 12px;
}
.nav-mark { display:flex; align-items:center; gap:10px; }
.nav-logo { height:34px; width:auto; display:block; }

.hero-logo { display:block; width:clamp(84px,11vw,132px); height:auto; margin:0 auto 22px; }
.hero-brand {
  background: linear-gradient(90deg, var(--blue), var(--accent));
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
}

.rail-meter-fill, .artifact-meter-fill {
  background: linear-gradient(90deg, var(--blue), var(--accent));
}

.packet-plate { flex:1 1 0; min-height:0; width:100%; object-fit:contain; background:#000; padding:14px; }

.footer-brand-name { display:flex; align-items:center; gap:12px; }
.footer-logo { height:44px; width:auto; display:block; }
'''
R('</style>', CSS + '</style>')

open(path, 'w', encoding='utf-8').write(s)
print('Patched', path, '(backup:', path + '.bak)')
if miss:
    print('\nNot found (already changed or different text):')
    for m in miss: print('  -', m)
