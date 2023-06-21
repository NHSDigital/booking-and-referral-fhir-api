from .environment import ENV


# Api Details
ENVIRONMENT = ENV["environment"]
BASE_URL = f"https://{ENVIRONMENT}.api.service.nhs.uk"
BASE_PATH = ENV["base_path"]
PROXY_NAME = ENV["proxy_name"]
CLIENT_ID = ENV["client_id"]
CLIENT_SECRET = ENV["client_secret"]
REDIRECT_URL = ENV["redirect_url"]
TARGET_ID = ENV["target_id"]
