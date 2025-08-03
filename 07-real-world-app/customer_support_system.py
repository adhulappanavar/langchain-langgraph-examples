"""
Example 7: Real-world Customer Support Application

This example demonstrates a complete, production-ready customer support system
that integrates all LangChain and LangGraph concepts into a realistic agentic flow.
"""

import os
import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, TypedDict, Annotated, Optional
from enum import Enum
from dataclasses import dataclass
from dotenv import load_dotenv

# LangChain and LangGraph imports
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enums for better type safety
class IntentType(Enum):
    ORDER_INQUIRY = "order_inquiry"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING_ISSUE = "billing_issue"
    SHIPPING_TRACKING = "shipping_tracking"
    PRODUCT_INFORMATION = "product_information"
    COMPLAINT = "complaint"
    GENERAL_INQUIRY = "general_inquiry"

class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class AgentType(Enum):
    INTENT_CLASSIFIER = "intent_classifier"
    ORDER_AGENT = "order_agent"
    TECHNICAL_AGENT = "technical_agent"
    BILLING_AGENT = "billing_agent"
    SHIPPING_AGENT = "shipping_agent"
    ESCALATION_AGENT = "escalation_agent"

# Data classes for structured data
@dataclass
class CustomerInfo:
    customer_id: str
    name: str
    email: str
    phone: Optional[str] = None
    loyalty_tier: str = "standard"
    total_orders: int = 0
    total_spent: float = 0.0

@dataclass
class OrderInfo:
    order_id: str
    customer_id: str
    status: str
    items: List[Dict]
    total_amount: float
    shipping_address: str
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[str] = None

# Define the comprehensive state structure
class CustomerSupportState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]
    customer_info: Optional[CustomerInfo]
    intent_type: Optional[IntentType]
    priority_level: Optional[PriorityLevel]
    current_agent: Optional[AgentType]
    conversation_id: str
    session_start_time: datetime
    workflow_status: str
    agent_results: Dict[str, Any]
    escalation_reason: Optional[str]
    follow_up_required: bool
    sentiment_score: float
    response_time_ms: int
    error_log: List[str]
    performance_metrics: Dict[str, Any] 