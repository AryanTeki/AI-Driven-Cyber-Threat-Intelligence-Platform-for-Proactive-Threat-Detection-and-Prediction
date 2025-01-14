from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Optional imports with better error handling
REDDIT_AVAILABLE = False

try:
    import praw
    REDDIT_AVAILABLE = True
    logger.info("Reddit integration available")
except ImportError as e:
    logger.warning(f"Reddit integration not available: {e}")

class TwitterAPIv2Client:
    """Simple Twitter API v2 client"""
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.twitter.com/2"
        self.bearer_token = None
    
    def _get_bearer_token(self) -> str:
        """Get bearer token for API authentication"""
        if self.bearer_token:
            return self.bearer_token
        
        auth_url = "https://api.twitter.com/oauth2/token"
        auth = (self.api_key, self.api_secret)
        data = {'grant_type': 'client_credentials'}
        
        try:
            response = requests.post(auth_url, auth=auth, data=data)
            response.raise_for_status()
            self.bearer_token = response.json()['access_token']
            return self.bearer_token
        except Exception as e:
            logger.error(f"Error getting Twitter bearer token: {e}")
            return None
    
    def search_tweets(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search tweets using Twitter API v2"""
        if not self._get_bearer_token():
            return []
        
        search_url = f"{self.base_url}/tweets/search/recent"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {
            'query': query,
            'max_results': max_results,
            'tweet.fields': 'created_at,text'
        }
        
        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []

class DataCollector:
    def __init__(self, config: Dict):
        self.config = config
        self._init_apis()
    
    def _init_apis(self):
        # Initialize API clients with error handling
        self.otx_client = None
        self.vt_client = None
        self.twitter_client = None
        self.reddit_client = None
        
        try:
            if self.config.get('otx_api_key'):
                self.otx_client = OTXClient(self.config['otx_api_key'])
                logger.info("OTX client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OTX client: {e}")
        
        try:
            if self.config.get('vt_api_key'):
                self.vt_client = VirusTotalClient(self.config['vt_api_key'])
                logger.info("VirusTotal client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize VirusTotal client: {e}")
        
        # Initialize Twitter client
        try:
            if all(self.config.get(k) for k in ['twitter_api_key', 'twitter_api_secret']):
                self.twitter_client = TwitterAPIv2Client(
                    self.config['twitter_api_key'],
                    self.config['twitter_api_secret']
                )
                logger.info("Twitter client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
        
        # Initialize Reddit client
        if REDDIT_AVAILABLE:
            try:
                if all(self.config.get(k) for k in ['reddit_client_id', 'reddit_client_secret']):
                    self.reddit_client = self._init_reddit()
                    logger.info("Reddit client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Reddit client: {e}")
    
    def _init_reddit(self):
        """Initialize Reddit client with error handling"""
        if not REDDIT_AVAILABLE:
            return None
        
        try:
            reddit = praw.Reddit(
                client_id=self.config['reddit_client_id'],
                client_secret=self.config['reddit_client_secret'],
                user_agent=self.config['reddit_user_agent']
            )
            # Test the connection
            reddit.user.me()
            return reddit
        except Exception as e:
            logger.error(f"Reddit authentication failed: {e}")
            return None
    
    def collect_threat_feeds(self) -> List[Dict]:
        """Collect data from threat intelligence feeds with error handling"""
        threats = []
        
        # Collect from OTX
        if self.otx_client:
            try:
                otx_threats = self.otx_client.get_pulses()
                threats.extend(otx_threats)
                logger.info(f"Collected {len(otx_threats)} threats from OTX")
            except Exception as e:
                logger.error(f"Error collecting OTX feeds: {e}")
        
        # Collect from VirusTotal
        if self.vt_client:
            try:
                vt_threats = self.vt_client.get_reports()
                threats.extend(vt_threats)
                logger.info(f"Collected {len(vt_threats)} threats from VirusTotal")
            except Exception as e:
                logger.error(f"Error collecting VirusTotal reports: {e}")
        
        return threats
    
    def monitor_social_media(self) -> List[Dict]:
        """Monitor social media for cyber threat indicators with error handling"""
        indicators = []
        
        # Twitter monitoring
        if self.twitter_client:
            try:
                twitter_indicators = self._monitor_twitter()
                indicators.extend(twitter_indicators)
                logger.info(f"Collected {len(twitter_indicators)} indicators from Twitter")
            except Exception as e:
                logger.error(f"Error monitoring Twitter: {e}")
        
        # Reddit monitoring
        if self.reddit_client:
            try:
                reddit_indicators = self._monitor_reddit()
                indicators.extend(reddit_indicators)
                logger.info(f"Collected {len(reddit_indicators)} indicators from Reddit")
            except Exception as e:
                logger.error(f"Error monitoring Reddit: {e}")
        
        return indicators
    
    def _monitor_twitter(self) -> List[Dict]:
        """Monitor Twitter for threat indicators with error handling"""
        if not self.twitter_client:
            return []
        
        try:
            # Search for cybersecurity-related tweets
            keywords = ["cybersecurity", "malware", "ransomware", "data breach"]
            tweets = []
            
            for keyword in keywords:
                try:
                    search_results = self.twitter_client.search_tweets(keyword)
                    tweets.extend([
                        {
                            'source': 'twitter',
                            'text': tweet['text'],
                            'timestamp': tweet['created_at'],
                            'keyword': keyword
                        }
                        for tweet in search_results
                    ])
                except Exception as e:
                    logger.error(f"Error searching Twitter for keyword '{keyword}': {e}")
            
            return tweets
        except Exception as e:
            logger.error(f"Error in Twitter monitoring: {e}")
            return []
    
    def _monitor_reddit(self) -> List[Dict]:
        """Monitor Reddit for threat indicators with error handling"""
        if not self.reddit_client:
            return []
        
        try:
            # Monitor relevant subreddits
            subreddits = ["cybersecurity", "netsec", "malware"]
            posts = []
            
            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit_client.subreddit(subreddit_name)
                    new_posts = subreddit.new(limit=100)
                    
                    posts.extend([
                        {
                            'source': 'reddit',
                            'title': post.title,
                            'text': post.selftext,
                            'timestamp': datetime.fromtimestamp(post.created_utc),
                            'subreddit': subreddit_name
                        }
                        for post in new_posts
                    ])
                except Exception as e:
                    logger.error(f"Error monitoring subreddit '{subreddit_name}': {e}")
            
            return posts
        except Exception as e:
            logger.error(f"Error in Reddit monitoring: {e}")
            return []
    
    def scrape_dark_web(self) -> List[Dict]:
        """Scrape dark web sources for threat intelligence"""
        logger.warning("Dark web scraping not implemented")
        return []
    
    def collect_internal_logs(self) -> List[Dict]:
        """Collect and parse internal network logs"""
        logger.warning("Internal log collection not implemented")
        return []

class OTXClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://otx.alienvault.com/api/v1"
    
    def get_pulses(self) -> List[Dict]:
        """Get threat pulses from OTX with error handling"""
        headers = {"X-OTX-API-KEY": self.api_key}
        try:
            response = requests.get(
                f"{self.base_url}/pulses/subscribed",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.Timeout:
            logger.error("OTX request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching OTX pulses: {e}")
            return []
        except ValueError as e:
            logger.error(f"Error parsing OTX response: {e}")
            return []

class VirusTotalClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/vtapi/v2"
    
    def get_reports(self) -> List[Dict]:
        """Get threat reports from VirusTotal with error handling"""
        params = {"apikey": self.api_key}
        try:
            response = requests.get(
                f"{self.base_url}/file/reports",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result if isinstance(result, list) else [result]
        except requests.exceptions.Timeout:
            logger.error("VirusTotal request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching VirusTotal reports: {e}")
            return []
        except ValueError as e:
            logger.error(f"Error parsing VirusTotal response: {e}")
            return []