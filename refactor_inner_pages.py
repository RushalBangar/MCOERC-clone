import os
import re

TARGET_DIR = r"d:\Projects\MCOERC\matoshri_clone"

def get_depth(filepath, base_dir):
    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    return depth

def adjust_paths(content, depth):
    if depth == 0:
        return content
    # Replace href="..., src="..., etc. starting with "assets/" or "xyz.html" to "../" * depth
    prefix = '../' * depth
    # Adjust assets
    content = re.sub(r'(href|src)="assets/', rf'\1="{prefix}assets/', content)
    # Adjust root html links: href="about.html", "index.html", etc.
    content = re.sub(r'href="(?!http|mailto|#|\.\.)([a-zA-Z0-9_-]+\.html)', rf'href="{prefix}\1"', content)
    # Adjust subdirectory html links (e.g. href="academics/computer.html")
    content = re.sub(r'href="(academics/|admissions/|facilities/)(.*?\.html)', rf'href="{prefix}\1\2"', content)
    return content

def main():
    # 1. Read the new header and footer from index.html
    index_path = os.path.join(TARGET_DIR, "index.html")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()

    # Extract header: from <!-- ── HEADER / NAVIGATION ── --> to </header>
    header_match = re.search(r'<!-- ── HEADER / NAVIGATION ── -->(.*?)</header>', index_html, re.DOTALL)
    if not header_match:
        print("Could not find header in index.html")
        return
    new_header_base = f"<!-- START HEADER -->\n{header_match.group(1).strip()}\n</header>\n<!-- END HEADER -->"

    # Extract footer: from <!-- ── FOOTER ── --> to </footer>
    footer_match = re.search(r'<!-- ── FOOTER ── -->(.*?)</footer>', index_html, re.DOTALL)
    if not footer_match:
        print("Could not find footer in index.html")
        return
    new_footer_base = f"<!-- START FOOTER SECTION -->\n{footer_match.group(1).strip()}\n</footer>\n<!-- END FOOTER SECTION -->"

    # 2. Iterate through all other HTML files and replace
    count = 0
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                depth = get_depth(filepath, TARGET_DIR)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original = content
                
                # Adjust paths for header and footer BEFORE injecting
                adjusted_header = adjust_paths(new_header_base, depth)
                adjusted_footer = adjust_paths(new_footer_base, depth)
                
                # Replace Header
                content = re.sub(
                    r'<!-- START HEADER -->.*?<!-- END HEADER -->',
                    adjusted_header,
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )
                
                # Replace Footer
                content = re.sub(
                    r'<!-- START FOOTER SECTION -->.*?<!-- END FOOTER SECTION -->',
                    adjusted_footer,
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
    
    print(f"Refactored header/footer in {count} HTML files.")
    
    # 3. Append legacy aliases to style.css
    legacy_css = """

/* ── LEGACY ALIASES FOR INNER PAGES ── */
.padding_four_tb, .page-content { padding: 4rem 0; background: var(--clr-bg); }
.heading_s3 h3, .heading_s3 h4 { font-family: var(--font-heading); color: var(--clr-primary); font-size: 2rem; margin-bottom: 1.5rem; }
.text-black { color: var(--clr-text) !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.85rem; }
.bg-dark { background-color: var(--clr-primary) !important; }
.bg-white { background-color: #ffffff !important; }
.box_shadow4 { box-shadow: var(--shadow-md) !important; border: 1px solid var(--clr-border); border-radius: var(--radius-md); }
.table { width: 100%; margin-bottom: 2rem; border-collapse: collapse; }
.table th, .table td { padding: 1rem; text-align: left; border-bottom: 1px solid var(--clr-border); }
.table th { background: var(--clr-bg-alt); font-weight: 600; font-family: var(--font-heading); color: var(--clr-primary); }
.breadcrumb_section { background: linear-gradient(135deg, var(--clr-primary) 0%, var(--clr-primary-light) 100%); padding: 6rem 0 4rem; color: #fff; text-align: center; }
.page-title h1 { color: #fff; font-size: 2.8rem; margin: 0; }
.breadcrumb { list-style: none; display: flex; justify-content: center; gap: 0.5rem; padding: 0; margin-top: 1rem; }
.breadcrumb-item a { color: var(--clr-accent); text-decoration: none; }
.breadcrumb-item.active { color: #cbd5e1; }
.breadcrumb-item + .breadcrumb-item::before { content: "›"; color: rgba(255,255,255,0.5); padding-right: 0.5rem; }
.animation { animation: heroFadeUp 0.8s ease forwards; }
.text-justify { text-align: justify; margin-bottom: 1.25rem; font-size: 1.05rem; }
.radius_none { border-radius: 0 !important; }
"""
    style_path = os.path.join(TARGET_DIR, "assets", "css", "style.css")
    with open(style_path, 'a', encoding='utf-8') as f:
        f.write(legacy_css)
    print("Appended legacy aliases to style.css")

if __name__ == "__main__":
    main()
