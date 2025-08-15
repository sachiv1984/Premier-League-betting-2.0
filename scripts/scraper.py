import json
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

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
        
        for i in range(len(fix)):
            fixture_text = fix[i].get_text(separator=" ")
            
            # Debug: Print the raw fixture text
            print(f"Raw fixture text: {fixture_text}")
            
            # Replace "Today" and "Tomorrow" with actual dates
            if "Today" in fixture_text:
                fixture_text = fixture_text.replace("Today", today.strftime("%d/%m/%Y"))
            if "Tomorrow" in fixture_text:
                fixture_text = fixture_text.replace("Tomorrow", tomorrow.strftime("%d/%m/%Y"))
            
            # Debug: Print the processed fixture text
            print(f"Processed fixture text: {fixture_text}")
            
            fixtures.append(fixture_text.strip())
        
        return fixtures
    except Exception as e:
        print(f"Error scraping fixtures: {e}")
        return []
