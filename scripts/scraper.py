import json
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import re  # Import regular expressions for date pattern matching

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
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        # Regular expression to match dates in the format DD/MM/YYYY
        date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
        
        for i in range(len(fix)):
            fixture_text = fix[i].get_text(separator=" ")
            
            # Debug: Print the raw fixture text
            print(f"Raw fixture text: {fixture_text}")
            
            # Check if "Tomorrow" is present and replace it with the correct date
            if "Tomorrow" in fixture_text:
                print(f"'Tomorrow' found in fixture: {fixture_text}")
                fixture_text = fixture_text.replace("Tomorrow", tomorrow.strftime("%d/%m/%Y"))
            
            # Check if the fixture text already contains a date
            if not date_pattern.search(fixture_text):  # No date format present
                print(f"No date found in fixture: {fixture_text}. Assuming 'Today'.")
                # Append today's date before the time
                parts = fixture_text.rsplit(" ", 1)  # Split into main text and time
                fixture_text = f"{parts[0]} {today.strftime('%d/%m/%Y')} {parts[1]}"
            
            # Debug: Print the processed fixture text
            print(f"Processed fixture text: {fixture_text}")
            
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
