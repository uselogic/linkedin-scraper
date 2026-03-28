# LinkedIn Post Scraper

A Flask web application that scrapes LinkedIn posts using Playwright.

## Features

- Scrapes LinkedIn posts to extract text, images, and videos
- Web UI for easy interaction
- REST API endpoint for programmatic access
- Files saved organized by type

## Tech Stack

- **Backend**: Flask (Python)
- **Scraping**: Playwright (headless Chromium)
- **Frontend**: HTML, CSS (glassmorphism design)

## Project Structure

```
├── app.py                    # Flask application
├── linkedin_scraper.py       # LinkedIn scraping logic
├── scraper.py                # General story scraper (IndianSexStories)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── .gitignore
├── templates/
│   ├── index.html           # Main story scraper UI
│   └── linkedin.html        # LinkedIn scraper UI
├── static/
│   └── style.css            # Shared styles
├── linkedin text/           # Created at runtime - scraped text
├── linkedin image/          # Created at runtime - downloaded images
├── linkedin video/          # Created at runtime - downloaded videos
└── texts/                   # Created at runtime - story text files
```

## Deployment Options

### Option 1: Railway (Recommended)

1. Push this code to a GitHub repository
2. Go to [railway.app](https://railway.app) and sign up
3. Create new project → Deploy from GitHub
4. Select your repository
5. Set build command:
   ```
   pip install -r requirements.txt && playwright install --with-deps chromium
   ```
6. Set start command:
   ```
   python app.py
   ```
7. Deploy

### Option 2: Docker (Any Provider)

```bash
# Build image
docker build -t linkedin-scraper .

# Run container
docker run -p 5000:5000 linkedin-scraper
```

Deploy the image to:
- Railway
- Render
- Fly.io
- DigitalOcean App Platform
- Any container hosting service

## Environment Variables

- `PORT`: Port to run the Flask app (default: 5000)

## Usage

1. Open `http://localhost:5000/linkedin`
2. Enter a LinkedIn post URL
3. Click "Scrape Post"
4. View downloaded files in respective directories

## API Endpoints

- `GET /` - Main story scraper UI
- `GET /linkedin` - LinkedIn scraper UI
- `POST /api/scrape_linkedin` - Scrape LinkedIn post
- `GET /api/tags` - Get available tags (story scraper)
- `POST /api/headlines` - Get headlines for tag
- `POST /api/scrape` - Scrape story

## Notes

- First deploy may take longer (~5-10 min) to download Chromium
- Free tier services may sleep after inactivity
- Files are stored ephemerally; consider cloud storage for persistence
- Be mindful of LinkedIn's Terms of Service
