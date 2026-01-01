"""
Constants and Configuration for HealthSense AI
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# API Keys - ALWAYS load from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Validate API key is set
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found! Please set it in .env file or environment variable."
    )

# File Paths
DIAGNOSTIC_INFO_FILE_PATH = "data/Hospital_Information_with_Lab_Tests.csv"
HOSPITAL_INFO_FILE_PATH = "data/Hospital_General_Information.csv"
EMERGENCY_DATA_PATH = "data/hospitals_emergency_data.csv"

# Database Paths
APPOINTMENTS_DB_PATH = "src/appointments.db"
EMERGENCY_DB_PATH = "src/emergency.db"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 7860
