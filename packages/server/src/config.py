# @author: adibarra (Alec Ibarra)
# @description: Configuration file for the server.

import os
import sys

from dotenv import load_dotenv

# check if running in production mode
IS_PRODUCTION: bool = bool(set(["--prod", "--production"]) & set(sys.argv))

# load environment variables
if IS_PRODUCTION:
    if not load_dotenv(dotenv_path=os.path.join("..", "..", ".env.production")):
        print(
            "Failed to load environment vars... Does '.env.production' exist?",
            flush=True,
        )
        sys.exit(1)
else:
    if not load_dotenv(dotenv_path=os.path.join("..", "..", ".env.development")):
        print(
            "Failed to load environment vars... Does '.env.development' exist?",
            flush=True,
        )
        sys.exit(1)


# server configuration
API_HOST: str = os.environ.get("API_HOST")
API_PORT: int = int(os.environ.get("API_PORT"))
API_CORS_ORIGINS_REGEX: str = os.environ.get("API_CORS_ORIGINS_REGEX")
SERVICE_POSTGRES_URI: str = os.environ.get("SERVICE_POSTGRES_URI")
