"""
Hospital Comparison API Routes
Endpoints for searching and comparing hospitals
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.HospitalComparisonAgent import HospitalComparisonAgent

# Initialize router
router = APIRouter()

# Initialize Hospital Agent (singleton)
hospital_agent = None
try:
    hospital_agent = HospitalComparisonAgent()
    print("Hospital Agent initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Hospital Agent: {e}")
    hospital_agent = None


# Response Models
class HospitalResponse(BaseModel):
    success: bool
    hospitals: list = []
    message: Optional[str] = None
    error: Optional[str] = None


@router.get("/hospitals", response_model=HospitalResponse)
async def get_hospitals(
    search: Optional[str] = Query(None, description="Search term for hospital name"),
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    rating: Optional[float] = Query(None, description="Minimum rating (0-5)"),
    beds: Optional[str] = Query(None, description="Filter by bed count"),
    location: Optional[str] = Query(None, description="Filter by location")
):
    """
    Get and filter hospitals

    Args:
        search: Search term for hospital name
        specialty: Filter by medical specialty
        rating: Minimum rating filter
        beds: Bed count filter
        location: Location filter

    Returns:
        HospitalResponse with list of hospitals
    """
    try:
        if not hospital_agent:
            raise HTTPException(
                status_code=503,
                detail="Hospital service is currently unavailable"
            )

        # Build query based on filters
        query_parts = []

        if search:
            query_parts.append(f"hospitals named '{search}'")

        if specialty:
            query_parts.append(f"specialized in {specialty}")

        if location:
            query_parts.append(f"located in {location}")

        if rating:
            query_parts.append(f"with rating above {rating}")

        if beds:
            query_parts.append(f"with {beds} beds")

        # Construct natural language query
        if query_parts:
            query = "Find " + " ".join(query_parts)
        else:
            query = "Show me all hospitals"

        # Query hospital agent
        result = hospital_agent.compare_hospitals(query)

        # For now, return the raw output
        # In production, you would parse this into structured data
        return HospitalResponse(
            success=True,
            hospitals=[],
            message=result
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/hospitals/compare")
async def compare_hospitals(
    hospital_ids: str = Query(..., description="Comma-separated hospital IDs or names to compare")
):
    """
    Compare specific hospitals

    Args:
        hospital_ids: Comma-separated list of hospital IDs or names

    Returns:
        Comparison results for specified hospitals
    """
    try:
        if not hospital_agent:
            raise HTTPException(
                status_code=503,
                detail="Hospital service is currently unavailable"
            )

        hospitals_list = [h.strip() for h in hospital_ids.split(",")]

        if len(hospitals_list) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 hospitals required for comparison"
            )

        query = f"Compare these hospitals: {', '.join(hospitals_list)}"

        # Query hospital agent
        result = hospital_agent.compare_hospitals(query)

        return {
            "success": True,
            "comparison": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/hospitals/specialties")
async def get_hospitals_by_specialty(
    specialty: str = Query(..., description="Medical specialty to search for")
):
    """
    Find hospitals by medical specialty

    Args:
        specialty: Medical specialty (e.g., "cardiology", "neurology")

    Returns:
        List of hospitals offering the specialty
    """
    try:
        if not hospital_agent:
            raise HTTPException(
                status_code=503,
                detail="Hospital service is currently unavailable"
            )

        if not specialty or not specialty.strip():
            raise HTTPException(
                status_code=400,
                detail="Specialty is required"
            )

        query = f"Find hospitals with {specialty} specialty"

        # Query hospital agent
        result = hospital_agent.compare_hospitals(query)

        return {
            "success": True,
            "specialty": specialty,
            "hospitals": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
