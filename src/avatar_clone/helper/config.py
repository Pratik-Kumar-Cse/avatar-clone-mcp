import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Access environment variables and store them in variables
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 5004))
WEBHOOK_ENDPOINT = os.getenv("WEBHOOK_ENDPOINT")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

# Add more variables as needed
# EXAMPLE_VAR = os.getenv('EXAMPLE_VAR')

# You can now use these variables throughout your project
