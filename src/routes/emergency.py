"""
Emergency Services API Routes
Endpoints for finding emergency facilities and ambulance services
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.EmergencyServicesAgent import EmergencyServicesAgent

# Initialize router
router = APIRouter()

# Initialize Emergency Agent (singleton)
emergency_agent = None
try:
    emergency_agent = EmergencyServicesAgent()
    print("Emergency Agent initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Emergency Agent: {e}")
    emergency_agent = None


# Response Models
class EmergencyResponse(BaseModel):
    success: bool
    hospitals: list = []
    message: Optional[str] = None
    error: Optional[str] = None


@router.get("/emergency", response_model=EmergencyResponse)
async def get_emergency_services(
    zipcode: str = Query(..., description="ZIP code to search for emergency services")
):
    """
    Find nearest emergency hospitals by ZIP code

    Args:
        zipcode: ZIP code to search (e.g., "10001")

    Returns:
        EmergencyResponse with list of emergency facilities
    """
    try:
        if not emergency_agent:
            raise HTTPException(
                status_code=503,
                detail="Emergency service is currently unavailable"
            )

        if not zipcode or not zipcode.strip():
            raise HTTPException(
                status_code=400,
                detail="ZIP code is required"
            )

        # Query emergency agent
        result = emergency_agent.find_emergency_services(zipcode)

        if not result.get("success"):
            return EmergencyResponse(
                success=False,
                hospitals=[],
                error=result.get("error", "Failed to fetch emergency services")
            )

        # Parse the output from agent
        output = result.get("output", "")

        # For now, return the raw output
        # In production, you would parse this into structured data
        return EmergencyResponse(
            success=True,
            hospitals=[],
            message=output
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/emergency/ambulance")
async def get_ambulance_services(
    zipcode: Optional[str] = Query(None, description="Optional ZIP code filter")
):
    """
    Find hospitals with ambulance services

    Args:
        zipcode: Optional ZIP code to filter results

    Returns:
        List of hospitals with ambulance availability
    """
    try:
        if not emergency_agent:
            raise HTTPException(
                status_code=503,
                detail="Emergency service is currently unavailable"
            )

        # Query emergency agent
        result = emergency_agent.find_ambulance_services(zipcode)

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Failed to fetch ambulance services")
            }

        return {
            "success": True,
            "message": result.get("output", "No ambulance services found")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/emergency/nearest")
async def get_nearest_emergency(
    zipcode: str = Query(..., description="Your current ZIP code")
):
    """
    Get nearest emergency facility to your location

    Args:
        zipcode: Your current ZIP code

    Returns:
        Nearest emergency facility information
    """
    try:
        if not emergency_agent:
            raise HTTPException(
                status_code=503,
                detail="Emergency service is currently unavailable"
            )

        if not zipcode or not zipcode.strip():
            raise HTTPException(
                status_code=400,
                detail="ZIP code is required"
            )

        # Query emergency agent
        result = emergency_agent.get_nearest_emergency(zipcode)

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Failed to find nearest emergency facility")
            }

        return {
            "success": True,
            "facility": result.get("output", "No emergency facility found")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
