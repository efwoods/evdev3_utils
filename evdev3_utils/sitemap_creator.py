import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time


class SitemapGenerator:
    def __init__(self, base_url, max_pages=1000, delay=1.0):
        self.base_url = base_url.rstrip("/")
        self.max_pages = max_pages
        self.delay = delay
        self.visited = set()
        self.to_visit = [self.base_url]

    def is_internal_link(self, url):
        # Check if url is internal to base_url domain
        base_netloc = urlparse(self.base_url).netloc
        url_netloc = urlparse(url).netloc
        return base_netloc == url_netloc or url_netloc == ""

    def normalize_url(self, url):
        # Normalize URLs (remove fragments, query params optional)
        parsed = urlparse(urljoin(self.base_url, url))
        return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")

    def crawl(self):
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue
            print(f"Crawling: {url}")
            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    print(f"Failed to retrieve {url}: Status {response.status_code}")
                    self.visited.add(url)
                    continue
                soup = BeautifulSoup(response.text, "html.parser")
                self.visited.add(url)
                # Find all <a> tags
                for link_tag in soup.find_all("a", href=True):
                    href = link_tag["href"]
                    normalized = self.normalize_url(href)
                    if (
                        self.is_internal_link(normalized)
                        and normalized not in self.visited
                        and normalized not in self.to_visit
                    ):
                        self.to_visit.append(normalized)
                time.sleep(self.delay)  # polite crawl delay
            except Exception as e:
                print(f"Error crawling {url}: {e}")
                self.visited.add(url)

    def generate_sitemap_xml(self):
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in sorted(self.visited):
            sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
        sitemap_xml += "</urlset>"
        return sitemap_xml


if __name__ == "__main__":
    BASE_URL = "https://neuralnexus.site"
    generator = SitemapGenerator(BASE_URL)
    generator.crawl()
    sitemap_content = generator.generate_sitemap_xml()
    with open("sitemap.xml", "w") as f:
        f.write(sitemap_content)
    print("Sitemap generated and saved as sitemap.xml")
