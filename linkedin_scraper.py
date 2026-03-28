import os
from datetime import datetime
import requests
from playwright.sync_api import sync_playwright


def get_timestamp():
    """Return the current date and time in the specified format."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def download_file(url, folder, prefix, ext, serial):
    """Downloads a file and saves it using the naming convention."""
    try:
        if url.startswith("data:"):
            return None

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        filename = f"{prefix}_{serial}.{ext}"
        filepath = os.path.join(folder, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {filename}")
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def api_scrape_linkedin_post(url):
    """Scrapes a LinkedIn post using Playwright and returns the saved paths."""
    print(f"Starting API Playwright to scrape: {url}")

    # 1. Setup Directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    text_dir = os.path.join(base_dir, "linkedin text")
    img_dir = os.path.join(base_dir, "linkedin image")
    vid_dir = os.path.join(base_dir, "linkedin video")

    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(vid_dir, exist_ok=True)

    timestamp = get_timestamp()

    saved_files = {"text": [], "images": [], "videos": []}
    text_content = ""

    # 2. Launch Browser Session
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        try:
            # Navigate to the LinkedIn URL
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)

            # --- A. Extract Text Component ---
            print("Extracting text...")
            texts = []
            main_content = page.query_selector(
                "article, .core-section-container__content, .feed-shared-update-v2"
            )
            if main_content:
                text_val = main_content.inner_text().strip()
                if text_val:
                    texts.append(text_val)
            else:
                og_desc = page.query_selector('meta[property="og:description"]')
                if og_desc:
                    texts.append(og_desc.get_attribute("content"))

                paragraphs = page.query_selector_all("p")
                for para in paragraphs:
                    text_val = para.inner_text().strip()
                    if text_val and len(text_val) > 10:
                        texts.append(text_val)

            if texts:
                seen = set()
                unique_texts = []
                for t in texts:
                    if t not in seen:
                        seen.add(t)
                        unique_texts.append(t)

                text_filename = f"{timestamp}_1.txt"
                text_filepath = os.path.join(text_dir, text_filename)
                full_text = "\n\n---\n\n".join(unique_texts)
                with open(text_filepath, "w", encoding="utf-8") as f:
                    f.write(full_text)
                saved_files["text"].append(text_filename)
                text_content = full_text
                print(f"Saved Text: {text_filename}")

            # --- B. Extract Image Component ---
            print("Extracting images...")
            images = page.query_selector_all("img")
            img_urls = set()
            for img in images:
                src = img.get_attribute("src")
                if src and src.startswith("http"):
                    img_urls.add(src)

            img_serial = 1
            for src in img_urls:
                path = download_file(src, img_dir, timestamp, "jpg", img_serial)
                if path:
                    filename = os.path.basename(path)
                    saved_files["images"].append(f"/download/linkedin image/{filename}")
                img_serial += 1

            # --- C. Extract Video Component ---
            print("Extracting videos...")
            video_urls = set()
            videos = page.query_selector_all("video, source")
            for vid in videos:
                src = vid.get_attribute("src")
                if src and src.startswith("http"):
                    video_urls.add(src)

            vid_serial = 1
            for src in video_urls:
                path = download_file(src, vid_dir, timestamp, "mp4", vid_serial)
                if path:
                    filename = os.path.basename(path)
                    saved_files["videos"].append(f"/download/linkedin video/{filename}")
                vid_serial += 1

        except Exception as e:
            print(f"An error occurred during Playwright scraping: {e}")
            raise e
        finally:
            print("Closing browser...")
            browser.close()

    # Return both file URLs for download and the actual text content
    return {
        "text": text_content,
        "text_files": saved_files["text"],
        "images": saved_files["images"],
        "videos": saved_files["videos"],
    }


def scrape_linkedin_post(url):
    api_scrape_linkedin_post(url)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("Enter LinkedIn Post URL: ")

    if target_url:
        scrape_linkedin_post(target_url)
    else:
        print("No URL provided. Exiting.")
