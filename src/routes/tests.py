"""
Lab Tests API Routes
Endpoints for browsing and booking lab tests
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.DiagnosticInfoAgent import DiagnosticInfoAgent

# Initialize router
router = APIRouter()

# Initialize Diagnostic Agent (singleton)
diagnostic_agent = None
try:
    diagnostic_agent = DiagnosticInfoAgent()
    print("Diagnostic Agent initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Diagnostic Agent: {e}")
    diagnostic_agent = None


# Request/Response Models
class TestBookingRequest(BaseModel):
    test_id: Optional[int] = None
    test_name: str
    patient_name: str
    patient_email: str
    patient_phone: str
    preferred_date: str
    preferred_time: Optional[str] = None
    location: Optional[str] = None


class TestBookingResponse(BaseModel):
    success: bool
    booking_id: Optional[str] = None
    message: str
    error: Optional[str] = None


class TestResponse(BaseModel):
    success: bool
    tests: list = []
    message: Optional[str] = None
    error: Optional[str] = None


@router.get("/tests", response_model=TestResponse)
async def get_lab_tests(
    category: Optional[str] = Query(None, description="Filter by category (blood, imaging, etc.)"),
    search: Optional[str] = Query(None, description="Search term"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    fasting: Optional[str] = Query(None, description="Fasting requirement (yes/no)")
):
    """
    Get lab tests with filters

    Args:
        category: Test category filter
        search: Search term for test name
        max_price: Maximum price filter
        fasting: Fasting requirement filter

    Returns:
        TestResponse with list of tests
    """
    try:
        if not diagnostic_agent:
            raise HTTPException(
                status_code=503,
                detail="Diagnostic service is currently unavailable"
            )

        # Build query based on filters
        query_parts = []

        if category:
            query_parts.append(f"{category} tests")

        if search:
            query_parts.append(f"related to {search}")

        if max_price:
            query_parts.append(f"under ${max_price}")

        if fasting == "yes":
            query_parts.append("requiring fasting")
        elif fasting == "no":
            query_parts.append("not requiring fasting")

        # Construct natural language query
        if query_parts:
            query = "Show me " + " ".join(query_parts)
        else:
            query = "Show me all available lab tests"

        # Query diagnostic agent
        result = diagnostic_agent.query(query)

        if not result.get("success"):
            return TestResponse(
                success=False,
                tests=[],
                error=result.get("error", "Failed to fetch lab tests")
            )

        # Return the agent output
        return TestResponse(
            success=True,
            tests=[],
            message=result.get("output", "No tests found")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/tests/{test_name}")
async def get_test_details(test_name: str):
    """
    Get detailed information about a specific test

    Args:
        test_name: Name of the test

    Returns:
        Detailed test information
    """
    try:
        if not diagnostic_agent:
            raise HTTPException(
                status_code=503,
                detail="Diagnostic service is currently unavailable"
            )

        # Query diagnostic agent
        result = diagnostic_agent.get_lab_test_info(test_name)

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Failed to fetch test details")
            }

        return {
            "success": True,
            "test_details": result.get("output", "No details found")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/tests/condition/{condition}")
async def get_tests_for_condition(condition: str):
    """
    Get recommended tests for a specific health condition

    Args:
        condition: Health condition (e.g., "diabetes", "heart disease")

    Returns:
        Recommended tests for the condition
    """
    try:
        if not diagnostic_agent:
            raise HTTPException(
                status_code=503,
                detail="Diagnostic service is currently unavailable"
            )

        if not condition or not condition.strip():
            raise HTTPException(
                status_code=400,
                detail="Condition is required"
            )

        # Query diagnostic agent
        result = diagnostic_agent.find_tests_by_condition(condition)

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Failed to fetch recommended tests")
            }

        return {
            "success": True,
            "condition": condition,
            "recommended_tests": result.get("output", "No recommendations found")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/tests/packages")
async def get_health_packages():
    """
    Get available health screening packages

    Returns:
        List of health screening packages
    """
    try:
        if not diagnostic_agent:
            raise HTTPException(
                status_code=503,
                detail="Diagnostic service is currently unavailable"
            )

        # Query diagnostic agent
        result = diagnostic_agent.get_health_screening_packages()

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Failed to fetch packages")
            }

        return {
            "success": True,
            "packages": result.get("output", "No packages found")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/book-test", response_model=TestBookingResponse)
async def book_test(booking: TestBookingRequest):
    """
    Book a lab test

    Args:
        booking: Test booking details

    Returns:
        TestBookingResponse with confirmation
    """
    try:
        if not diagnostic_agent:
            raise HTTPException(
                status_code=503,
                detail="Diagnostic service is currently unavailable"
            )

        # Validate required fields
        if not booking.test_name:
            raise HTTPException(
                status_code=400,
                detail="Test name is required"
            )

        if not booking.patient_name or not booking.patient_email:
            raise HTTPException(
                status_code=400,
                detail="Patient name and email are required"
            )

        if not booking.preferred_date:
            raise HTTPException(
                status_code=400,
                detail="Preferred date is required"
            )

        # Generate booking ID
        booking_id = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # In production, you would:
        # 1. Save booking to database
        # 2. Send confirmation email
        # 3. Update test availability

        return TestBookingResponse(
            success=True,
            booking_id=booking_id,
            message=f"Test '{booking.test_name}' booked successfully for {booking.preferred_date}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/tests/categories")
async def get_test_categories():
    """
    Get list of available test categories

    Returns:
        List of test categories
    """
    try:
        categories = [
            {"id": "blood", "name": "Blood Tests", "icon": "🩸"},
            {"id": "imaging", "name": "Imaging", "icon": "📷"},
            {"id": "cardiac", "name": "Cardiac", "icon": "💓"},
            {"id": "diabetes", "name": "Diabetes", "icon": "🍬"},
            {"id": "thyroid", "name": "Thyroid", "icon": "🦋"},
            {"id": "liver", "name": "Liver Function", "icon": "🫀"},
            {"id": "kidney", "name": "Kidney Function", "icon": "🫘"},
            {"id": "vitamin", "name": "Vitamin & Nutrition", "icon": "💊"}
        ]

        return {
            "success": True,
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
