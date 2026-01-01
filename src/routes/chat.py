"""
AI Chat API Routes
Endpoints for conversational AI assistant
Orchestrates multiple agents based on user query
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.EmergencyServicesAgent import EmergencyServicesAgent
from src.HospitalComparisonAgent import HospitalComparisonAgent
from src.DoctorInfoAgent import DoctorInfoAgent
from src.DiagnosticInfoAgent import DiagnosticInfoAgent

# Initialize router
router = APIRouter()

# Initialize all agents (singleton)
emergency_agent = None
hospital_agent = None
doctor_agent = None
diagnostic_agent = None

try:
    emergency_agent = EmergencyServicesAgent()
    print("Emergency Agent initialized for chat")
except Exception as e:
    print(f"Warning: Could not initialize Emergency Agent: {e}")
    emergency_agent = None

try:
    hospital_agent = HospitalComparisonAgent()
    print("Hospital Agent initialized for chat")
except Exception as e:
    print(f"Warning: Could not initialize Hospital Agent: {e}")
    hospital_agent = None

try:
    doctor_agent = DoctorInfoAgent()
    print("Doctor Agent initialized for chat")
except Exception as e:
    print(f"Warning: Could not initialize Doctor Agent: {e}")
    doctor_agent = None

try:
    diagnostic_agent = DiagnosticInfoAgent()
    print("Diagnostic Agent initialized for chat")
except Exception as e:
    print(f"Warning: Could not initialize Diagnostic Agent: {e}")
    diagnostic_agent = None


# Request/Response Models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []


class ChatResponse(BaseModel):
    response: str
    timestamp: str
    agent_used: Optional[str] = None


class AgentOrchestrator:
    """
    Orchestrates multiple agents based on user query
    Routes queries to the appropriate specialized agent
    """

    def __init__(self):
        self.emergency_agent = emergency_agent
        self.hospital_agent = hospital_agent
        self.doctor_agent = doctor_agent
        self.diagnostic_agent = diagnostic_agent

    def classify_query(self, message: str) -> str:
        """
        Classify user query to determine which agent to use

        Args:
            message: User's message

        Returns:
            Agent type: 'emergency', 'hospital', 'doctor', 'diagnostic', or 'general'
        """
        message_lower = message.lower()

        # Emergency keywords
        emergency_keywords = [
            "emergency", "urgent", "911", "ambulance", "critical",
            "heart attack", "stroke", "accident", "trauma"
        ]
        if any(keyword in message_lower for keyword in emergency_keywords):
            return "emergency"

        # Doctor/appointment keywords
        doctor_keywords = [
            "doctor", "appointment", "book", "schedule", "available slot",
            "consultation", "visit", "check-up", "specialist"
        ]
        if any(keyword in message_lower for keyword in doctor_keywords):
            return "doctor"

        # Lab test/diagnostic keywords
        test_keywords = [
            "test", "lab", "blood", "screening", "diagnostic", "package",
            "checkup", "examination", "scan", "x-ray", "mri", "ct"
        ]
        if any(keyword in message_lower for keyword in test_keywords):
            return "diagnostic"

        # Hospital keywords
        hospital_keywords = [
            "hospital", "compare", "facility", "medical center",
            "healthcare", "clinic"
        ]
        if any(keyword in message_lower for keyword in hospital_keywords):
            return "hospital"

        # Default to general
        return "general"

    def process_query(self, message: str, history: List[Message]) -> Dict:
        """
        Process user query and route to appropriate agent

        Args:
            message: User's message
            history: Conversation history

        Returns:
            Dict with response and metadata
        """
        try:
            # Classify the query
            agent_type = self.classify_query(message)

            # Route to appropriate agent
            if agent_type == "emergency" and self.emergency_agent:
                result = self.emergency_agent.query(message)
                agent_used = "Emergency Services Agent"

            elif agent_type == "doctor" and self.doctor_agent:
                result = self.doctor_agent.query(message)
                agent_used = "Doctor Information Agent"

            elif agent_type == "diagnostic" and self.diagnostic_agent:
                result = self.diagnostic_agent.query(message)
                agent_used = "Diagnostic Information Agent"

            elif agent_type == "hospital" and self.hospital_agent:
                result = self.hospital_agent.compare_hospitals(message)
                agent_used = "Hospital Comparison Agent"
                # Hospital agent returns string directly, not dict
                result = {"success": True, "output": result}

            else:
                # General response when no agent matches
                result = {
                    "success": True,
                    "output": self._generate_general_response(message)
                }
                agent_used = "General Assistant"

            # Extract response
            if result.get("success"):
                response_text = result.get("output", "I'm sorry, I couldn't generate a proper response.")
            else:
                response_text = f"I encountered an error: {result.get('error', 'Unknown error')}"

            return {
                "response": response_text,
                "agent_used": agent_used,
                "success": True
            }

        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error processing your request: {str(e)}",
                "agent_used": "Error Handler",
                "success": False
            }

    def _generate_general_response(self, message: str) -> str:
        """
        Generate a general response for non-specific queries

        Args:
            message: User's message

        Returns:
            General response string
        """
        return (
            "I'm your AI health assistant. I can help you with:\n\n"
            "🏥 Finding and comparing hospitals\n"
            "👨‍⚕️ Searching for doctors and booking appointments\n"
            "🔬 Browsing lab tests and health screening packages\n"
            "🚨 Locating emergency services\n"
            "💊 Answering general health-related questions\n\n"
            "What would you like to know more about?"
        )


# Initialize orchestrator
orchestrator = AgentOrchestrator()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    AI Chat endpoint - connects to multi-agent system

    Request format:
    {
        "message": "User's question",
        "history": [
            {"role": "user", "content": "Previous message"},
            {"role": "assistant", "content": "Previous response"}
        ]
    }

    Returns:
        ChatResponse with AI-generated response
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        # Process query through orchestrator
        result = orchestrator.process_query(
            message=request.message,
            history=request.history
        )

        if not result.get("success"):
            # Still return a response even if there was an error
            return ChatResponse(
                response=result.get("response", "I apologize for the inconvenience."),
                timestamp=datetime.now().isoformat(),
                agent_used=result.get("agent_used", "Error Handler")
            )

        return ChatResponse(
            response=result.get("response", "No response generated"),
            timestamp=datetime.now().isoformat(),
            agent_used=result.get("agent_used", "Unknown")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/chat/history")
async def get_chat_history(
    session_id: Optional[str] = None
):
    """
    Get chat history for a session

    Args:
        session_id: Optional session ID

    Returns:
        Chat history
    """
    try:
        # In production, you would fetch from database
        # For now, return empty history
        return {
            "success": True,
            "history": [],
            "message": "Chat history feature coming soon"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.delete("/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    """
    Clear chat history for a session

    Args:
        session_id: Session ID to clear

    Returns:
        Success confirmation
    """
    try:
        # In production, you would delete from database
        return {
            "success": True,
            "message": f"Chat history cleared for session {session_id}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
