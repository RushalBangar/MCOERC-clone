#!/usr/bin/env python3
"""
apply_theme.py  –  MCOERC Premium Theme Propagator
Applies the Slate-Navy & Metallic Gold design system to all HTML pages.
Run from: d:\Projects\MCOERC\MCOERC-clone\
"""

import os
import re
from pathlib import Path

# ── Root directory of the website ──
ROOT = Path(__file__).parent

# ── Files / directories to skip ──
SKIP_FILES = {'index.html', 'home.html', 'apply_theme.py', 'apply_seo.py'}
SKIP_DIRS  = {'.git', 'assets', 'node_modules'}

# ── Collect all HTML files ──
def get_html_files():
    files = []
    for path in ROOT.rglob('*.html'):
        if path.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files

# ── Determine the relative path prefix back to root ──
def get_prefix(file_path: Path) -> str:
    depth = len(file_path.relative_to(ROOT).parts) - 1
    return '../' * depth  # '' for root, '../' for one level deep, etc.

# ── Premium <head> block ──
PREMIUM_HEAD_TEMPLATE = """\
<head>
  <!-- Standard SEO Metadata -->
  {title_tag}
  {meta_desc}
  <meta name="keywords" content="Matoshri College of Engineering, MCOERC, Nashik, Engineering College Nashik, Autonomous Institute SPPU, Matoshri Education Society, Best Engineering College Maharashtra, B.Tech, M.Tech, MCA">
  <meta name="author" content="Matoshri College of Engineering &amp; Research Centre">
  <meta name="robots" content="index, follow">

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="shortcut icon" type="image/x-icon" href="{pfx}assets/images/favicon.png">

  <!-- Premium Design System -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="{pfx}assets/css/style.css">
  <link rel="stylesheet" id="layoutstyle" href="{pfx}assets/color/theme.css">
</head>"""

# ── Premium header (root-relative paths replaced by caller) ──
PREMIUM_HEADER_TEMPLATE = """\
<!-- ── HEADER / NAVIGATION ── -->
<header class="premium-header">
  <div class="top-bar">
    <div class="premium-container" style="display: flex; justify-content: space-between;">
      <div style="display:flex; align-items:center;">
        <a href="{pfx}library.html"><i class="fa fa-book"></i> Library</a>
        <a href="{pfx}feedback.html"><i class="fa fa-comment"></i> Feedback</a>
        <a href="https://learning.matoshri.edu.in/" target="_blank"><i class="fa fa-graduation-cap"></i> Knowledge Base</a>
      </div>
      <div style="display:flex; align-items:center;">
        <a href="{pfx}contact.html"><i class="fa fa-phone"></i> +91 253 230 2000</a>
        <a href="mailto:info@mcoerc.ac.in"><i class="fa fa-envelope"></i> info@mcoerc.ac.in</a>
      </div>
    </div>
  </div>
  <div class="premium-container">
    <nav class="navbar-main">
      <a href="{pfx}index.html" class="brand-wrapper">
        <img src="{pfx}assets/images/logo/mcoerc.png" alt="MCOERC">
        <div class="brand-text">
          <span class="brand-title">Matoshri College of Engineering</span>
          <p>An Autonomous Institute · Nashik</p>
        </div>
      </a>
      <button class="mobile-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">
        <i class="fa fa-bars"></i>
      </button>
      <ul class="nav-links">
        <li><a href="{pfx}index.html">Home</a></li>
        <li>
          <a href="{pfx}about.html">About <i class="fa fa-chevron-down" style="font-size:0.65em; margin-left:4px;"></i></a>
          <div class="dropdown-menu">
            <a href="{pfx}about.html">About Institute</a>
            <a href="{pfx}vision.html">Vision &amp; Mission</a>
            <a href="{pfx}secretary.html">Secretary's Desk</a>
            <a href="{pfx}principal.html">Director's Desk</a>
            <a href="{pfx}gb.html">Governing Body</a>
            <a href="{pfx}council.html">Academic Council</a>
            <a href="{pfx}governance.html">Governance</a>
          </div>
        </li>
        <li>
          <a href="{pfx}academics/computer.html">Academics <i class="fa fa-chevron-down" style="font-size:0.65em; margin-left:4px;"></i></a>
          <div class="dropdown-menu">
            <a href="{pfx}academics/computer.html">Computer Engineering</a>
            <a href="{pfx}academics/it.html">Information Technology</a>
            <a href="{pfx}academics/electronics.html">Electronics &amp; TC Engg.</a>
            <a href="{pfx}academics/mechanical.html">Mechanical Engineering</a>
            <a href="{pfx}academics/civil.html">Civil Engineering</a>
            <a href="{pfx}academics/electrical.html">Electrical Engineering</a>
            <a href="{pfx}academics/aids.html">AI &amp; Data Science</a>
            <a href="{pfx}academics/mca.html">MCA</a>
          </div>
        </li>
        <li>
          <a href="{pfx}admissions/fe.html">Admissions <i class="fa fa-chevron-down" style="font-size:0.65em; margin-left:4px;"></i></a>
          <div class="dropdown-menu">
            <a href="{pfx}admissions/fe.html">First Year UG (B.Tech)</a>
            <a href="{pfx}admissions/dsy.html">Direct Second Year</a>
            <a href="{pfx}admissions/me.html">M.Tech / MCA PG</a>
            <a href="{pfx}admissions/phd.html">Ph.D</a>
          </div>
        </li>
        <li><a href="{pfx}admin.html">Administration</a></li>
        <li><a href="{pfx}tpo.html">Placements</a></li>
      </ul>
      <a href="{pfx}admissions/fe.html" class="btn-premium btn-accent">Apply Now <i class="fa fa-arrow-right"></i></a>
    </nav>
  </div>
</header>"""

# ── Premium breadcrumb ──
BREADCRUMB_TEMPLATE = """\
<!-- ── BREADCRUMB ── -->
<section class="breadcrumb_section">
  <div class="premium-container">
    <div class="page-title">
      <h1>{page_title}</h1>
    </div>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="{pfx}index.html">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page">{page_title}</li>
      </ol>
    </nav>
  </div>
</section>"""

# ── Premium footer ──
PREMIUM_FOOTER_TEMPLATE = """\
<!-- ── FOOTER ── -->
<footer class="premium-footer">
  <div class="premium-container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div style="display:flex; align-items:center; gap:12px;">
          <img src="{pfx}assets/images/logo/mcoerc.png" width="60" style="border-radius:12px;" alt="MCOERC">
          <h2 style="color:#fff; margin:0; font-size:1.8rem;">MCOERC</h2>
        </div>
        <p>Matoshri College of Engineering &amp; Research Centre, Nashik — An Autonomous Institute committed to technical excellence and moral values since 2008.</p>
        <div class="social-links">
          <a href="#"><i class="fab fa-facebook-f"></i></a>
          <a href="#"><i class="fab fa-twitter"></i></a>
          <a href="#"><i class="fab fa-linkedin-in"></i></a>
          <a href="#"><i class="fab fa-youtube"></i></a>
          <a href="#"><i class="fab fa-instagram"></i></a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Quick Links</h4>
        <ul class="footer-links">
          <li><a href="{pfx}about.html">About Institute</a></li>
          <li><a href="{pfx}vision.html">Vision &amp; Mission</a></li>
          <li><a href="{pfx}admin.html">Administration</a></li>
          <li><a href="{pfx}tpo.html">Training &amp; Placement</a></li>
          <li><a href="{pfx}alumni.html">Alumni Network</a></li>
          <li><a href="{pfx}disclosure.html">Mandatory Disclosure</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Academics</h4>
        <ul class="footer-links">
          <li><a href="{pfx}academics/computer.html">Computer Science</a></li>
          <li><a href="{pfx}academics/it.html">Information Tech</a></li>
          <li><a href="{pfx}academics/aids.html">AI &amp; Data Science</a></li>
          <li><a href="{pfx}academics/mechanical.html">Mechanical Engg</a></li>
          <li><a href="{pfx}academics/civil.html">Civil Engineering</a></li>
          <li><a href="{pfx}academics/mca.html">MCA Programme</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact Us</h4>
        <div class="contact-list">
          <div style="display:flex; gap:10px;">
            <i class="fa fa-map-marker-alt" style="margin-top:5px; color:var(--clr-accent);"></i>
            <span>Eklahare, Near Odhagaon, Nashik – 422 003, Maharashtra</span>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <i class="fa fa-phone" style="color:var(--clr-accent);"></i>
            <span>+91 253 230 2000</span>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <i class="fa fa-envelope" style="color:var(--clr-accent);"></i>
            <span>info@mcoerc.ac.in</span>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <i class="fa fa-globe" style="color:var(--clr-accent);"></i>
            <a href="https://www.mcoerc.ac.in" style="color:var(--clr-accent);">www.mcoerc.ac.in</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="premium-container">
      &copy; 2026 Matoshri College of Engineering &amp; Research Centre. All rights reserved.
    </div>
  </div>
</footer>"""

# ── Premium scripts (back-to-top, header shrink, scroll progress) ──
PREMIUM_SCRIPTS = """\
<!-- ── BACK TO TOP ── -->
<button id="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" style="
  position:fixed; bottom:2rem; right:2rem; z-index:9000;
  width:48px; height:48px; border-radius:50%;
  background:linear-gradient(135deg, var(--clr-accent), #ca8a04);
  border:none; cursor:pointer; color:var(--clr-primary);
  box-shadow: 0 8px 24px rgba(234,179,8,0.4);
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem; opacity:0; transform:translateY(10px);
  transition: opacity 0.4s ease, transform 0.4s ease;
  pointer-events:none;
"><i class="fa fa-arrow-up"></i></button>

<!-- ── PREMIUM UX SCRIPTS ── -->
<script>
  // Header Shrink on Scroll
  const _hdr = document.querySelector('.premium-header');
  if (_hdr) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 80) {
        _hdr.style.background = 'rgba(255,255,255,0.97)';
        _hdr.style.boxShadow = '0 4px 30px rgba(0,0,0,0.12)';
        const nm = _hdr.querySelector('.navbar-main');
        if (nm) nm.style.padding = '0.45rem 0';
      } else {
        _hdr.style.background = 'rgba(255,255,255,0.85)';
        _hdr.style.boxShadow = '';
        const nm = _hdr.querySelector('.navbar-main');
        if (nm) nm.style.padding = '0.8rem 0';
      }
    });
  }

  // Back-to-Top Button
  const _btt = document.getElementById('back-to-top');
  if (_btt) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 350) {
        _btt.style.opacity = '1';
        _btt.style.transform = 'translateY(0)';
        _btt.style.pointerEvents = 'auto';
      } else {
        _btt.style.opacity = '0';
        _btt.style.transform = 'translateY(10px)';
        _btt.style.pointerEvents = 'none';
      }
    });
  }

  // Glowing Gold Scroll Progress Bar
  document.addEventListener('DOMContentLoaded', () => {
    const pc = document.createElement('div');
    pc.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:4px;z-index:9999;pointer-events:none;';
    const pb = document.createElement('div');
    pb.style.cssText = 'width:0%;height:100%;background:linear-gradient(to right,#eab308,#fde047);box-shadow:0 0 8px rgba(234,179,8,0.6);transition:width 0.1s ease-out;';
    pc.appendChild(pb); document.body.appendChild(pc);
    window.addEventListener('scroll', () => {
      pb.style.width = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight) * 100) + '%';
    });

    // IntersectionObserver Reveal
    const els = document.querySelectorAll('.section-header, .premium-card, .glass-card, .notice-wrapper, .stat-card');
    els.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(28px)';
      el.style.transition = `opacity 0.6s cubic-bezier(0.16,1,0.3,1) ${(i%5)*70}ms, transform 0.6s cubic-bezier(0.16,1,0.3,1) ${(i%5)*70}ms`;
    });
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
    els.forEach(el => obs.observe(el));
  });
</script>"""


def extract_page_title_from_html(html: str, filename: str) -> str:
    """Try to find the page's <h1> or infer from <title> tag."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return title or filename.replace('.html','').replace('-',' ').replace('_',' ').title()
    m2 = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m2:
        t = m2.group(1).split('|')[0].strip()
        return t
    return filename.replace('.html','').replace('-',' ').replace('_',' ').title()


def extract_title_tag(html: str) -> str:
    m = re.search(r'(<title>.*?</title>)', html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else '<title>MCOERC | Matoshri College of Engineering</title>'


def extract_meta_desc(html: str) -> str:
    m = re.search(r'(<meta\s+name=["\']description["\'][^>]*>)', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(r'(<meta\s+[^>]*name=["\']description["\'][^>]*>)', html, re.IGNORECASE)
    return m2.group(1).strip() if m2 else '<meta name="description" content="Matoshri College of Engineering &amp; Research Centre, Nashik – An Autonomous Institute.">'


def extract_body_content(html: str) -> str:
    """Extract everything between the breadcrumb / page-content and the footer."""
    # Try to find content between breadcrumb end and footer start
    content_match = re.search(
        r'(?:<!-- END SECTION BANNER -->|</section>\s*<!-- END SECTION BANNER -->|breadcrumb_section[^>]*>.*?</section>)(.*?)(?=<!-- START FOOTER|<footer\b)',
        html, re.IGNORECASE | re.DOTALL
    )
    if content_match:
        return content_match.group(1).strip()
    
    # Fallback: try page-content div
    pc_match = re.search(r'<div[^>]+class=["\'][^"\']*page-content[^"\']*["\'][^>]*>(.*?)</div>\s*(?=<!-- START FOOTER|<footer\b)', html, re.IGNORECASE | re.DOTALL)
    if pc_match:
        return f'<div class="page-content">\n{pc_match.group(1).strip()}\n</div>'
    
    # Last resort: extract everything between </header> and <footer
    body_match = re.search(r'</header>(.*?)<footer', html, re.IGNORECASE | re.DOTALL)
    if body_match:
        content = body_match.group(1).strip()
        # remove admission enquiry modal, breadcrumb, old scrollup link
        content = re.sub(r'<!-- START SECTION BANNER.*?<!-- END SECTION BANNER -->', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<div[^>]+class=["\'][^"\']*modal[^"\']*["\'][^>]*>.*?</div>\s*</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<!-- Floating Action Button.*?-->', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<div[^>]+class=["\'][^"\']*glass-fab[^"\']*["\'][^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
        return content.strip()
    
    return '<div class="premium-section"><div class="premium-container"><p>Content unavailable – please rebuild this page.</p></div></div>'


def transform_page(file_path: Path):
    pfx = get_prefix(file_path)
    html = file_path.read_text(encoding='utf-8', errors='replace')
    
    # Extract key pieces from original
    title_tag  = extract_title_tag(html)
    meta_desc  = extract_meta_desc(html)
    page_title = extract_page_title_from_html(html, file_path.stem)
    body_content = extract_body_content(html)
    
    # Build the new clean HTML
    head = PREMIUM_HEAD_TEMPLATE.format(pfx=pfx, title_tag=title_tag, meta_desc=meta_desc)
    header = PREMIUM_HEADER_TEMPLATE.format(pfx=pfx)
    breadcrumb = BREADCRUMB_TEMPLATE.format(pfx=pfx, page_title=page_title)
    footer = PREMIUM_FOOTER_TEMPLATE.format(pfx=pfx)
    
    new_html = f"""<!DOCTYPE html>
<html lang="en">
{head}

<body>

{header}

{breadcrumb}

<div class="page-wrapper" style="min-height:60vh; padding: 4rem 0; background: var(--clr-bg);">
{body_content}
</div>

{footer}

{PREMIUM_SCRIPTS}

</body>
</html>
"""
    file_path.write_text(new_html, encoding='utf-8')
    return True


def main():
    files = get_html_files()
    print(f"Found {len(files)} HTML pages to process.\n")
    success, failed = 0, []
    for f in sorted(files):
        try:
            transform_page(f)
            rel = f.relative_to(ROOT)
            print(f"  ✓  {rel}")
            success += 1
        except Exception as e:
            print(f"  ✗  {f.relative_to(ROOT)}  —  {e}")
            failed.append(f)
    
    print(f"\n{'─'*50}")
    print(f"Done! {success} pages updated successfully.")
    if failed:
        print(f"{len(failed)} pages failed:")
        for f in failed:
            print(f"   • {f.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
