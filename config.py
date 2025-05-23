import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
PATHS = {
    'synology': os.getenv('SYNOLOGY_PATH'),
    'nas': os.getenv('NAS_PATH'),
    'stock': os.getenv('STOCK_PATH'),
    'inv-cotizar': os.getenv('INVCOTIZAR_PATH')
}

# Destination paths
DESTINATIONS = {
    'synology': os.getenv('SYNOLOGY_DEST'),
    'nas': os.getenv('NAS_DEST')
}

# Update times
UPDATE_TIMES = {
    'stock': "06:00",
    'synology': "06:03",
    'nas': "06:05",
    'inv-cotizar': "06:08"
}

# Retry settings
RETRY_SETTINGS = {
    'max_retries': 3,
    'retry_delay': 60,  # seconds
    'check_interval': 5  # seconds
}

# Logging settings
LOG_SETTINGS = {
    'log_file': "procesos.log",
    'log_level': "INFO",
    'log_format': "%(asctime)s - %(levelname)s - %(message)s",
    'date_format': "%Y-%m-%d %H:%M:%S"
} 