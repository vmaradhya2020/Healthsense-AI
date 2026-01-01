"""
API Routes Package
Contains all API endpoints for HealthSense AI
"""

from . import emergency
from . import hospitals
from . import doctors
from . import tests
from . import chat

__all__ = ["emergency", "hospitals", "doctors", "tests", "chat"]
