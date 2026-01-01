"""
Doctor Search & Booking API Routes
Endpoints for finding doctors and booking appointments
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.DoctorInfoAgent import DoctorInfoAgent

# Initialize router
router = APIRouter()

# Initialize Doctor Agent (singleton)
doctor_agent = None
try:
    doctor_agent = DoctorInfoAgent()
    print("Doctor Agent initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Doctor Agent: {e}")
    doctor_agent = None


# Request/Response Models
class AppointmentRequest(BaseModel):
    doctor_id: Optional[int] = None
    doctor_name: str
    date: str
    time: str
    patient_name: str
    patient_email: str
    patient_phone: str
    reason: Optional[str] = None


class AppointmentResponse(BaseModel):
    success: bool
    confirmation_id: Optional[str] = None
    message: str
    error: Optional[str] = None


class DoctorResponse(BaseModel):
    success: bool
    doctors: list = []
    message: Optional[str] = None
    error: Optional[str] = None


@router.get("/doctors", response_model=DoctorResponse)
async def get_doctors(
    search: Optional[str] = Query(None, description="Search term for doctor name"),
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    location: Optional[str] = Query(None, description="Filter by location"),
    available: Optional[bool] = Query(None, description="Filter by availability")
):
    """
    Search for doctors

    Args:
        search: Search term for doctor name
        specialty: Medical specialty filter
        location: Location filter
        available: Only show doctors with available slots

    Returns:
        DoctorResponse with list of doctors
    """
    try:
        if not doctor_agent:
            raise HTTPException(
                status_code=503,
                detail="Doctor service is currently unavailable"
            )

        # Build query based on filters
        if specialty:
            result = doctor_agent.get_available_doctors(specialty)
        else:
            result = doctor_agent.get_available_doctors()

        if not result.get("success"):
            return DoctorResponse(
                success=False,
                doctors=[],
                error=result.get("error", "Failed to fetch doctors")
            )

        # Return the agent output
        return DoctorResponse(
            success=True,
            doctors=[],
            message=result.get("output", "No doctors found")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/doctors/{doctor_id}/slots")
async def get_doctor_slots(
    doctor_id: int,
    date: Optional[str] = Query(None, description="Date to check (YYYY-MM-DD)")
):
    """
    Get available appointment slots for a specific doctor

    Args:
        doctor_id: Doctor's ID
        date: Optional date filter

    Returns:
        Available appointment slots
    """
    try:
        if not doctor_agent:
            raise HTTPException(
                status_code=503,
                detail="Doctor service is currently unavailable"
            )

        # Query for available slots
        result = doctor_agent.get_available_slots()

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Failed to fetch slots")
            }

        return {
            "success": True,
            "slots": result.get("output", "No slots available")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/appointments", response_model=AppointmentResponse)
async def book_appointment(appointment: AppointmentRequest):
    """
    Book doctor appointment

    Args:
        appointment: Appointment details

    Returns:
        AppointmentResponse with confirmation
    """
    try:
        if not doctor_agent:
            raise HTTPException(
                status_code=503,
                detail="Doctor service is currently unavailable"
            )

        # Validate required fields
        if not appointment.doctor_name:
            raise HTTPException(
                status_code=400,
                detail="Doctor name is required"
            )

        if not appointment.date or not appointment.time:
            raise HTTPException(
                status_code=400,
                detail="Date and time are required"
            )

        if not appointment.patient_name or not appointment.patient_email:
            raise HTTPException(
                status_code=400,
                detail="Patient name and email are required"
            )

        # Book appointment using agent
        result = doctor_agent.book_appointment(
            appointment.doctor_name,
            appointment.time
        )

        if not result.get("success"):
            return AppointmentResponse(
                success=False,
                message="Failed to book appointment",
                error=result.get("error", "Unknown error occurred")
            )

        # Generate confirmation ID
        confirmation_id = f"APT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return AppointmentResponse(
            success=True,
            confirmation_id=confirmation_id,
            message=f"Appointment booked successfully with {appointment.doctor_name}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/doctors/specialties")
async def get_specialties():
    """
    Get list of available medical specialties

    Returns:
        List of specialties
    """
    try:
        # This could be dynamic from database in production
        specialties = [
            "Cardiology",
            "Neurology",
            "Orthopedics",
            "Pediatrics",
            "Dermatology",
            "Psychiatry",
            "Internal Medicine",
            "General Surgery",
            "Oncology",
            "Radiology"
        ]

        return {
            "success": True,
            "specialties": specialties
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
