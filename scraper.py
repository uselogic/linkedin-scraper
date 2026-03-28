import os
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "desktop": True}
)

BASE_URL = "https://www.indiansexstories3.com/"


def get_valid_filename(s):
    import re

    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def get_tags():
    tags_url = "https://www.indiansexstories3.com/tags/"
    response = scraper.get(tags_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    tags = []

    for a in soup.find_all("a"):
        href = a.get("href")
        if href and ("/tag/" in href or "/tags/" in href):
            name = a.get_text(strip=True)
            if name and len(name) > 1:
                tags.append(
                    {
                        "name": name,
                        "url": href
                        if href.startswith("http")
                        else urljoin(BASE_URL, href),
                    }
                )

    unique_tags = []
    seen = set()
    for t in tags:
        if t["url"] not in seen:
            seen.add(t["url"])
            unique_tags.append(t)

    return unique_tags


def get_headlines_from_tag(tag_url):
    response = scraper.get(tag_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = []

    for h in soup.find_all(["h2", "h3"]):
        a = h.find("a")
        if a and a.get("href"):
            title = a.get_text(strip=True)
            if title:
                headlines.append(
                    {
                        "title": title,
                        "url": a.get("href")
                        if a.get("href").startswith("http")
                        else urljoin(BASE_URL, a.get("href")),
                    }
                )

    if not headlines:
        for a in soup.find_all("a", rel=["bookmark"]):
            title = a.get_text(strip=True)
            if title:
                headlines.append(
                    {
                        "title": title,
                        "url": a.get("href")
                        if a.get("href").startswith("http")
                        else urljoin(BASE_URL, a.get("href")),
                    }
                )

    unique_headlines = []
    seen = set()
    for h in headlines:
        if h["url"] not in seen:
            seen.add(h["url"])
            unique_headlines.append(h)

    return unique_headlines


def scrape_story(story_url, headline):
    response = scraper.get(story_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    content_div = soup.find("div", class_="entry-content")
    if content_div:
        paragraphs = content_div.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    text_content = [
        p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    texts_dir = os.path.join(base_dir, "texts")
    os.makedirs(texts_dir, exist_ok=True)

    filename = f"{get_valid_filename(headline)}.txt"
    file_path = os.path.join(texts_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"--- {headline} ---\n")
        f.write(f"URL: {story_url}\n\n")
        f.write("\n\n".join(text_content))

    return file_path
