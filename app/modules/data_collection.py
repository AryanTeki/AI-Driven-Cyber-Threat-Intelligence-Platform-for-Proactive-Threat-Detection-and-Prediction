from typing import Dict, List
import requests
try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False
try:
    import praw
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False
from bs4 import BeautifulSoup
from datetime import datetime

class DataCollector:
    def __init__(self, config: Dict):
        self.config = config
        self._init_apis()
    
    def _init_apis(self):
        # Initialize API clients
        self.otx_client = OTXClient(self.config['otx_api_key'])
        self.vt_client = VirusTotalClient(self.config['vt_api_key'])
        
        # Initialize optional clients
        self.twitter_client = None
        self.reddit_client = None
        
        if TWITTER_AVAILABLE:
            try:
                self.twitter_client = self._init_twitter()
            except Exception as e:
                print(f"Failed to initialize Twitter client: {e}")
        
        if REDDIT_AVAILABLE:
            try:
                self.reddit_client = self._init_reddit()
            except Exception as e:
                print(f"Failed to initialize Reddit client: {e}")
    
    def _init_twitter(self):
        if not TWITTER_AVAILABLE:
            return None
        auth = tweepy.OAuthHandler(
            self.config['twitter_api_key'],
            self.config['twitter_api_secret']
        )
        return tweepy.API(auth)
    
    def _init_reddit(self):
        if not REDDIT_AVAILABLE:
            return None
        return praw.Reddit(
            client_id=self.config['reddit_client_id'],
            client_secret=self.config['reddit_client_secret'],
            user_agent=self.config['reddit_user_agent']
        )
    
    def collect_threat_feeds(self) -> List[Dict]:
        """Collect data from threat intelligence feeds"""
        threats = []
        try:
            threats.extend(self.otx_client.get_pulses())
        except Exception as e:
            print(f"Error collecting OTX feeds: {e}")
        
        try:
            threats.extend(self.vt_client.get_reports())
        except Exception as e:
            print(f"Error collecting VirusTotal reports: {e}")
        
        return threats
    
    def monitor_social_media(self) -> List[Dict]:
        """Monitor social media for cyber threat indicators"""
        indicators = []
        
        # Twitter monitoring
        if self.twitter_client:
            try:
                indicators.extend(self._monitor_twitter())
            except Exception as e:
                print(f"Error monitoring Twitter: {e}")
        
        # Reddit monitoring
        if self.reddit_client:
            try:
                indicators.extend(self._monitor_reddit())
            except Exception as e:
                print(f"Error monitoring Reddit: {e}")
        
        return indicators
    
    def _monitor_twitter(self) -> List[Dict]:
        """Monitor Twitter for threat indicators"""
        if not self.twitter_client:
            return []
        # Implementation would go here
        return []
    
    def _monitor_reddit(self) -> List[Dict]:
        """Monitor Reddit for threat indicators"""
        if not self.reddit_client:
            return []
        # Implementation would go here
        return []
    
    def scrape_dark_web(self) -> List[Dict]:
        """Scrape dark web sources for threat intelligence"""
        # Implementation would require proper dark web access setup
        return []
    
    def collect_internal_logs(self) -> List[Dict]:
        """Collect and parse internal network logs"""
        # Implementation depends on internal logging setup
        return []

class OTXClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://otx.alienvault.com/api/v1"
    
    def get_pulses(self) -> List[Dict]:
        headers = {"X-OTX-API-KEY": self.api_key}
        response = requests.get(f"{self.base_url}/pulses/subscribed", headers=headers)
        return response.json().get("results", [])

class VirusTotalClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/vtapi/v2"
    
    def get_reports(self) -> List[Dict]:
        params = {"apikey": self.api_key}
        response = requests.get(f"{self.base_url}/file/reports", params=params)
        return response.json() 