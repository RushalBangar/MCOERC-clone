import os
import re
from datetime import datetime

# Root workspace directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# File exclusion lists or special handling if needed
EXCLUDE_DIRS = {".git", "assets"}

def clean_title(title_text):
    # Remove common suffixes to isolate the raw page subject
    suffixes = [
        "- Matoshri College of Engineering (MCOERC)",
        "| MCOERC",
        "— Matoshri College of Engineering & Research Centre",
        "Matoshri College of Engineering & Research Centre",
        "MCOERC —",
        "MCOERC -",
        "MCOERC"
    ]
    cleaned = title_text
    for suffix in suffixes:
        cleaned = re.sub(re.escape(suffix), "", cleaned, flags=re.IGNORECASE)
    
    cleaned = cleaned.strip(" -|—\t\n\r")
    if not cleaned or cleaned.lower() == "mcoerc":
        return "Matoshri College of Engineering & Research Centre"
    
    if cleaned.isupper() and len(cleaned) > 4:
        cleaned = cleaned.title()
        
    return cleaned

def get_custom_alt(src_val, page_name):
    src_lower = src_val.lower()
    if "logo" in src_lower:
        return "Matoshri College of Engineering & Research Centre (MCOERC) Logo"
    if "secretory" in src_lower or "secretary" in src_lower:
        return "Er. Kunal N. Darade - Secretary, Matoshri Education Society"
    if "principal" in src_lower or "director" in src_lower:
        return "Dr. G. K. Kharate - Principal / Director, MCOERC Nashik"
    if "slider" in src_lower or "banner" in src_lower or "campus" in src_lower:
        return f"Matoshri College of Engineering & Research Centre (MCOERC) Campus - {page_name}"
    
    src_basename = os.path.basename(src_val).split('.')[0] if src_val else "image"
    cleaned_name = src_basename.replace('-', ' ').replace('_', ' ').title()
    return f"MCOERC {page_name} - {cleaned_name}"

def enrich_images(content, page_name):
    def img_replacer(match):
        img_tag = match.group(0)
        # Parse alt and src
        alt_match = re.search(r'\balt=["\'](.*?)["\']', img_tag, re.IGNORECASE)
        src_match = re.search(r'\bsrc=["\'](.*?)["\']', img_tag, re.IGNORECASE)
        
        src_val = src_match.group(1) if src_match else ""
        alt_text = get_custom_alt(src_val, page_name)
        
        if not alt_match or not alt_match.group(1).strip():
            if alt_match:
                # Replace empty alt="" with enriched alt text
                img_tag = re.sub(r'\balt=["\'](.*?)["\']', f'alt="{alt_text}"', img_tag, count=1, flags=re.IGNORECASE)
            else:
                # Insert alt text right after '<img'
                img_tag = re.sub(r'<img', f'<img alt="{alt_text}"', img_tag, count=1, flags=re.IGNORECASE)
        return img_tag

    return re.sub(r'<img\b[^>]*>', img_replacer, content, flags=re.IGNORECASE)

def strip_existing_seo_tags(head_content):
    # Remove existing title
    head_content = re.sub(r'<title>.*?</title>\s*', '', head_content, flags=re.IGNORECASE)
    # Remove existing description
    head_content = re.sub(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'].*?["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    head_content = re.sub(r'<meta[^>]*content=["\'].*?["\'][^>]*name=["\']description["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    # Remove existing keywords
    head_content = re.sub(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\'].*?["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    head_content = re.sub(r'<meta[^>]*content=["\'].*?["\'][^>]*name=["\']keywords["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    # Remove existing author
    head_content = re.sub(r'<meta[^>]*name=["\']author["\'][^>]*content=["\'].*?["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    head_content = re.sub(r'<meta[^>]*content=["\'].*?["\'][^>]*name=["\']author["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    # Remove existing robots
    head_content = re.sub(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'].*?["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    # Remove existing OpenGraph or Twitter Card metadata to prevent duplicates
    head_content = re.sub(r'<meta[^>]*property=["\']og:.*?["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    head_content = re.sub(r'<meta[^>]*name=["\']twitter:.*?["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    # Remove existing canonical links
    head_content = re.sub(r'<link[^>]*rel=["\']canonical["\'][^>]*>\s*', '', head_content, flags=re.IGNORECASE)
    return head_content

def make_seo_block(cleaned_title, desc, relative_path):
    # Formulate standardized URLs (slash separated, even on Windows)
    url_path = relative_path.replace("\\", "/")
    canonical_url = f"https://www.mcoerc.ac.in/{url_path}"
    if url_path in ["index.html", "home.html"]:
        canonical_url = "https://www.mcoerc.ac.in/"
        
    full_title = f"{cleaned_title} | Matoshri College of Engineering & Research Centre (MCOERC) Nashik"
    if cleaned_title == "Matoshri College of Engineering & Research Centre":
        full_title = "MCOERC | Matoshri College of Engineering & Research Centre Nashik (Autonomous)"

    seo_block = f"""
  <!-- Standard SEO Metadata -->
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="Matoshri College of Engineering, MCOERC, Nashik, Engineering College Nashik, Autonomous Institute SPPU, Matoshri Education Society, Kunal Darade, Best Engineering College Maharashtra, Admissions 2025, B.Tech, M.Tech, MCA, Computer Engineering, IT, AI Data Science">
  <meta name="author" content="Matoshri College of Engineering & Research Centre">
  <meta name="robots" content="index, follow">

  <!-- OpenGraph Metadata for Social Media -->
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="https://www.mcoerc.ac.in/assets/images/logo/mcoerc.png">
  <meta property="og:site_name" content="MCOERC Autonomous Nashik">
  <meta property="og:locale" content="en_US">

  <!-- Twitter Card Metadata -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{full_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://www.mcoerc.ac.in/assets/images/logo/mcoerc.png">

  <!-- Canonical Link -->
  <link rel="canonical" href="{canonical_url}">
"""
    return seo_block

def process_html_file(file_path):
    relative_path = os.path.relpath(file_path, ROOT_DIR)
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 1. Title Extraction
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    original_title = title_match.group(1) if title_match else "MCOERC"
    cleaned_title = clean_title(original_title)

    # 2. Description Extraction
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\'][^>]*>', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\'][^>]*>', content, re.IGNORECASE)
    
    if desc_match and desc_match.group(1).strip():
        desc = desc_match.group(1).strip()
    else:
        desc = f"Explore the {cleaned_title} at Matoshri College of Engineering & Research Centre (MCOERC), Nashik. Learn about our autonomous programmes, academic excellence, faculty, and state-of-the-art facilities."

    # 3. Process Header Brand Title (Change h1 to span class="brand-title")
    # This prevents duplicate h1 issues
    content = re.sub(
        r'(<div class="brand-text">\s*)<h1>Matoshri College of Engineering</h1>',
        r'\1<span class="brand-title">Matoshri College of Engineering</span>',
        content,
        flags=re.IGNORECASE
    )

    # 4. Process Head Metadata
    head_match = re.search(r'<head>(.*?)</head>', content, re.IGNORECASE | re.DOTALL)
    if head_match:
        head_content = head_match.group(1)
        cleaned_head_content = strip_existing_seo_tags(head_content)
        seo_block = make_seo_block(cleaned_title, desc, relative_path)
        new_head = f"<head>{seo_block}\n{cleaned_head_content.lstrip()}\n</head>"
        content = content[:head_match.start()] + new_head + content[head_match.end():]

    # 5. Image Alt tag enrichment
    content = enrich_images(content, cleaned_title)

    # Save changes
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Processed: {relative_path} | Title: {cleaned_title}")
    return relative_path, cleaned_title

def main():
    print("Starting SEO Optimization traversal...")
    pages = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Exclude specific directories in place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                rel_path, clean_t = process_html_file(full_path)
                pages.append((rel_path, clean_t))
                
    # 6. Generate sitemap.xml
    generate_sitemap(pages)
    
    # 7. Generate robots.txt
    generate_robots()
    
    print("\nSEO Optimization traversal complete successfully!")

def generate_sitemap(pages):
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Sort pages to keep it organized
    pages.sort(key=lambda x: x[0])
    
    for rel_path, _ in pages:
        url_path = rel_path.replace("\\", "/")
        
        # Determine priority and change frequency
        if url_path in ["index.html", "home.html"]:
            loc = "https://www.mcoerc.ac.in/"
            priority = "1.0"
            freq = "daily"
        else:
            loc = f"https://www.mcoerc.ac.in/{url_path}"
            priority = "0.8" if "/" not in url_path else "0.6"
            freq = "weekly"
            
        xml_content += f"  <url>\n"
        xml_content += f"    <loc>{loc}</loc>\n"
        xml_content += f"    <lastmod>{date_str}</lastmod>\n"
        xml_content += f"    <changefreq>{freq}</changefreq>\n"
        xml_content += f"    <priority>{priority}</priority>\n"
        xml_content += f"  </url>\n"
        
    xml_content += '</urlset>\n'
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print(f"\nGenerated sitemap.xml with {len(pages)} URLs at: {sitemap_path}")

def generate_robots():
    robots_path = os.path.join(ROOT_DIR, "robots.txt")
    robots_content = """# robots.txt for Matoshri College of Engineering & Research Centre (MCOERC)
User-agent: *
Allow: /

# Sitemap Location
Sitemap: https://www.mcoerc.ac.in/sitemap.xml
"""
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
        
    print(f"Generated robots.txt at: {robots_path}")

if __name__ == "__main__":
    main()
