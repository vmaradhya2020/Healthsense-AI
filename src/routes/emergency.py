"""
Emergency Services API Routes
Endpoints for finding emergency facilities and ambulance services
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import sys
import os
import sqlite3

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
class HospitalInfo(BaseModel):
    name: str
    address: str = "Address not available"
    phone: str = "Phone not available"
    distance: str = "Distance not available"
    driveTime: str = "N/A"
    ambulanceAvailable: bool
    emergencyServices: str = "Emergency Services Available"

class EmergencyResponse(BaseModel):
    success: bool
    hospitals: List[HospitalInfo] = []
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
        if not zipcode or not zipcode.strip():
            raise HTTPException(
                status_code=400,
                detail="ZIP code is required"
            )

        # Query database directly for structured data
        db_path = "src/emergency.db"

        if not os.path.exists(db_path):
            # Fallback to agent if database doesn't exist
            if not emergency_agent:
                raise HTTPException(
                    status_code=503,
                    detail="Emergency service is currently unavailable"
                )
            result = emergency_agent.find_emergency_services(zipcode)
            return EmergencyResponse(
                success=result.get("success", False),
                hospitals=[],
                message=result.get("output", "No emergency services found"),
                error=result.get("error")
            )

        # Connect to database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query emergency directory (column names have spaces and capital letters)
        cursor.execute(
            'SELECT * FROM emergency_directory WHERE "Zip Code" = ?',
            (int(zipcode),)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return EmergencyResponse(
                success=True,
                hospitals=[],
                message=f"No emergency hospitals found in ZIP code {zipcode}. Please call 911 for immediate assistance."
            )

        # Convert database rows to hospital objects
        hospitals = []
        for row in rows:
            # Parse ambulance availability
            ambulance_text = row['Ambulance Available'].lower()
            ambulance_available = 'yes' in ambulance_text

            hospital = HospitalInfo(
                name=row['Hospital Name'],
                address=f"ZIP Code: {row['Zip Code']}",
                phone="Call 911 for Emergency",
                distance="N/A",
                driveTime="N/A",
                ambulanceAvailable=ambulance_available,
                emergencyServices="24/7 Emergency Services"
            )
            hospitals.append(hospital)

        return EmergencyResponse(
            success=True,
            hospitals=hospitals,
            message=f"Found {len(hospitals)} emergency hospital(s) in ZIP code {zipcode}"
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
