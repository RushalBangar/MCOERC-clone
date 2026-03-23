import os
import re

TARGET_DIR = r"d:\Projects\MCOERC\matoshri_clone"

css_files_to_remove = [
    "glassmorphism.css",
    "premium-design-system.css",
    "page-template.css",
    "theme-elements.css",
    "yit-featurebox.css",
    "yit-elements.css",
    "blog.css"
]

js_files_to_remove = [
    "premium-ui.js",
    "premium-core.js",
    "gsap.min.js",
    "ScrollTrigger.min.js",
    "countUp.umd.js"
]

# Classes to remove from body tags in HTML
classes_to_remove = ["premium-theme"]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Remove CSS linked tags
    for css in css_files_to_remove:
        # Match <link ... href="...css_file..." ... >
        pattern = re.compile(r'<link[^>]*href="[^"]*?' + re.escape(css) + r'"[^>]*>\s*', re.IGNORECASE)
        content = pattern.sub('', content)

    # 2. Remove JS script tags
    for js in js_files_to_remove:
        # Match <script ... src="...js_file..." ... ></script>
        pattern = re.compile(r'<script[^>]*src="[^"]*?' + re.escape(js) + r'"[^>]*>\s*</script>\s*', re.IGNORECASE)
        content = pattern.sub('', content)

    # 3. Remove 'premium-theme' class from <body>
    content = re.sub(r'(<body[^>]*\sclass=[\'"][^\'"]*?)(\s*premium-theme\s*)([^\'"]*[\'"])', r'\1 \3', content)
    # clean up empty class attributes
    content = re.sub(r'\sclass=[\'"]\s*[\'"]', '', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

for root, _, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))

print("Cleanup completed.")
