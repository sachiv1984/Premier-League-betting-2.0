import json
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def get_fixtures_data():
    """Scrape fixtures from OneFootball"""
    try:
        link = "https://onefootball.com/en/competition/premier-league-9/fixtures"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        source = requests.get(link, headers=headers).text
        page = BeautifulSoup(source, "lxml")
        fix = page.find_all("a", class_="MatchCard_matchCard__iOv4G")
        
        fixtures = []
        for i in range(len(fix)):
            fixture_text = fix[i].get_text(separator=" ")
            fixtures.append(fixture_text.strip())
        
        return fixtures
    except Exception as e:
        print(f"Error scraping fixtures: {e}")
        return []

def save_fixtures_json(fixtures):
    """Save fixtures to JSON file"""
    data = {
        "last_updated": datetime.now().isoformat(),
        "fixtures": fixtures,
        "total_count": len(fixtures)
    }
    
    # Save to docs directory for GitHub Pages
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    json_path = os.path.join(docs_dir, 'fixtures.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(fixtures)} fixtures to {json_path}")

def main():
    print("Starting fixtures scraper...")
    fixtures = get_fixtures_data()
    
    if fixtures:
        save_fixtures_json(fixtures)
        print("Fixtures updated successfully!")
    else:
        print("No fixtures found or error occurred")

if __name__ == "__main__":
    main()
