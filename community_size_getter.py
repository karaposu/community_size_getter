import os
from urllib.parse import urlparse
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class CommunitySizeGetter:
    def __init__(
        self,
        subreddit_name,
        twitter_handle,
        discord_invite_link,
        telegram_channel_name,
        use_proxy=True,
        use_ssl=False,
        cert_path=None
    ):
        """
        :param subreddit_name: Name of the subreddit
        :param twitter_handle: (not used in this example, but available)
        :param discord_invite_link: Discord invite URL
        :param telegram_channel_name: (not used in this example, but available)
        :param use_proxy: Boolean indicating whether to route traffic through the proxy
        :param use_ssl: Whether to connect to Bright Data's proxy via HTTPS or HTTP
        :param cert_path: Path to Bright Data's CA cert (if you want to trust a self-signed cert).
                          Only relevant if use_ssl=True.
        """
        self.subreddit_name = subreddit_name
        self.twitter_handle = twitter_handle
        self.discord_invite_link = discord_invite_link
        self.telegram_channel_name = telegram_channel_name

        # Store this for reference
        self.use_proxy = use_proxy

        if self.use_proxy:
            # Read proxy credentials from environment variables
            proxy_username = os.getenv("PROXY_USERNAME")
            proxy_password = os.getenv("PROXY_PASSWORD")
            proxy_host = os.getenv("PROXY_HOST")
            proxy_port = os.getenv("PROXY_PORT")
            
            # Decide whether to use "http" or "https" for the proxy
            protocol = "https" if use_ssl else "http"

            # Build the proxies dict
            self.proxies = {
                "http":  f"{protocol}://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
                "https": f"{protocol}://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
            }

            # Decide how to handle SSL verification
            if use_ssl:
                # If using an HTTPS proxy, pass in the custom CA cert path or True to use system certs
                self.verify = cert_path if cert_path else True
            else:
                # Common approach: connect to the proxy over HTTP, often skipping SSL verification
                self.verify = False
        else:
            # If not using a proxy at all, set proxies to None and do normal SSL verification
            self.proxies = None
            self.verify = True
    
    def get_subreddit_size(self):
        
        import praw
        import os
        from dotenv import load_dotenv
        load_dotenv()

        REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
        REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
        user_agent="YourBot/0.1"

        reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=user_agent)

        # Initialize PRAW
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=user_agent
        )

        try:
            subreddit = reddit.subreddit( self.subreddit_name)
            return subreddit.subscribers
        except Exception as e:
            print(f"An error occurred while fetching subscriber count for { self.subreddit_name}: {e}")
            return None

            

    def get_subreddit_size_by_request(self):
        """
        Fetch the subscriber count from the specified subreddit.
        """
        # url = f"https://www.reddit.com/r/{self.subreddit_name}/about.json"
        url = f"https://old.reddit.com/r/{self.subreddit_name}/about.json"
        headers = {"User-Agent": "PepeSubredditSizeCollector/1.0"}
        
        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=self.proxies,
                verify=self.verify
            )
            response.raise_for_status()
            data = response.json()
            return data["data"]["subscribers"]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Reddit: {e}")
            return None

    def fetch_discord_server_size(self):
        """
        Fetch the member count of a Discord server via an invite link.
        """
        parsed_url = urlparse(self.discord_invite_link)
        path_parts = parsed_url.path.rstrip("/").split("/")
        invite_code = path_parts[-1] if path_parts else ""

        if not invite_code:
            print("Failed to extract invite code from the invite link.")
            return None

        url = f"https://discord.com/api/v10/invites/{invite_code}?with_counts=true"
        headers = {"User-Agent": "DiscordServerSizeFetcher/1.0"}
        
        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=self.proxies,
                verify=self.verify
            )
            response.raise_for_status()
            data = response.json()
            return data.get("approximate_member_count")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Discord server size: {e}")
            return None

    def get_all(self):
        """Get subreddit subscriber count and Discord server size in one call."""
        subreddit_size = self.get_subreddit_size()
        discord_size = self.fetch_discord_server_size()
        todays_date = datetime.now().strftime("%Y-%m-%d")

        return {
            "subreddit_size": subreddit_size,
            "discord_size": discord_size,
            "date": todays_date
        }

def main():
    # Example usage:
    subreddit = "pepecoin"
    twitter = ""
    discord_invite_link = "https://discord.com/invite/6NXJt25q2J"
    telegram = ""
    
    cert_path= "/Users/ns/Desktop/projects/community_size_getter/brightdata_ssl_port_33335.crt"
    
    csg = CommunitySizeGetter(
        subreddit_name=subreddit,
        twitter_handle=twitter,
        discord_invite_link=discord_invite_link,
        telegram_channel_name=telegram,
        use_proxy=False,     # Toggle this to False to skip the proxy
        use_ssl=False,      # Toggle this to True to use an HTTPS proxy
        cert_path=cert_path
    )

    result = csg.get_all()
    print(result)

if __name__ == "__main__":
    main()
