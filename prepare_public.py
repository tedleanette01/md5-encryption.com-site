from pathlib import Path
import json
import shutil
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
BASE = "https://md5-encryption.com"

STATIC_PUBLIC = [
    "index.html",
    "about.html",
    "tools.html",
    "md5-generator.html",
    "md5-checksum.html",
    "file-md5-checker.html",
    "legal-notice.html",
    "404.html",
    "robots.txt",
]

INDEXABLE_STATIC = [
    "/",
    "/about.html",
    "/tools.html",
    "/md5-generator.html",
    "/md5-checksum.html",
    "/file-md5-checker.html",
]

def copy_required(src: Path, dst: Path):
    if not src.is_file():
        raise FileNotFoundError(f"Required public file is missing: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def main():
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    posts = json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))

    for name in STATIC_PUBLIC:
        copy_required(ROOT / name, PUBLIC / name)

    blog_urls = []
    for post in posts:
        slug = post["slug"]
        image = post["image"]
        copy_required(ROOT / "blogs" / f"{slug}.html", PUBLIC / "blogs" / f"{slug}.html")
        copy_required(ROOT / "images" / image, PUBLIC / "images" / image)
        blog_urls.append(f"/blogs/{slug}.html")

    urls = INDEXABLE_STATIC + blog_urls
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in urls:
        loc = BASE + ("/" if path == "/" else path)
        sitemap.append(f"  <url><loc>{escape(loc)}</loc></url>")
    sitemap.append('</urlset>')
    (PUBLIC / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (PUBLIC / ".nojekyll").write_text("", encoding="utf-8")

    print(f"public/ prepared: {len(STATIC_PUBLIC)} static files, {len(posts)} live blogs, {len(posts)} live blog images")
    print(f"sitemap.xml: {len(urls)} indexable URLs")

if __name__ == "__main__":
    main()
