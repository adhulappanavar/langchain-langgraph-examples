"""
Fixed Customer Service Example: Understand → Classify → Route → Respond

This version fixes the Pydantic parsing issues and improves emotion detection.
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Load environment variables
load_dotenv()

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Department(str, Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    SALES = "sales"
    GENERAL = "general"
    ESCALATION = "escalation"

class CustomerInquiry(BaseModel):
    """Structure for understanding customer inquiry"""
    main_issue: str = Field(description="The primary issue or question")
    customer_emotion: str = Field(description="Customer's emotional state (frustrated, happy, confused, angry, stressed)")
    urgency_level: UrgencyLevel = Field(description="How urgent this issue is")
    context: List[str] = Field(description="Additional context or details mentioned")

class Classification(BaseModel):
    """Structure for classifying the inquiry"""
    category: str = Field(description="Main category of the inquiry")
    subcategory: str = Field(description="Specific subcategory")
    complexity: str = Field(description="Complexity level (simple, moderate, complex)")
    estimated_resolution_time: str = Field(description="Estimated time to resolve")
    requires_escalation: bool = Field(description="Whether this needs escalation")

class RoutingDecision(BaseModel):
    """Structure for routing decision"""
    department: Department = Field(description="Which department should handle this")
    priority: str = Field(description="Priority level (low, medium, high, urgent)")
    agent_requirements: List[str] = Field(description="Required agent skills or expertise")
    sla_target: str = Field(description="Service level agreement target time")

def create_understanding_chain():
    """Create a chain to understand the customer inquiry with improved parsing"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,  # Slightly higher for better parsing
        max_tokens=200
    )
    
    prompt = PromptTemplate(
        input_variables=["customer_message"],
        template="""Analyze the following customer inquiry and extract key information.

Customer Message: {customer_message}

Emotion Detection Guidelines:
- Frustrated: "nothing works", "ridiculous", "trying for hours", multiple exclamations
- Happy: "thanks", "appreciate", "great service", positive feedback
- Confused: "I don't understand", "why is this", questioning language
- Angry: "this is ridiculous", "useless", strong negative language
- Stressed: "deadline", "urgent", "meeting soon", time pressure

Urgency Indicators:
- Low: general inquiries, no time pressure
- Medium: some concern, seeking information
- High: immediate need, significant problem
- Critical: deadline, urgent meeting, system down

Return a JSON object with this exact format:
{{
  "main_issue": "brief description of the main problem",
  "customer_emotion": "frustrated/happy/confused/angry/stressed",
  "urgency_level": "low/medium/high/critical",
  "context": ["key detail 1", "key detail 2"]
}}

JSON Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="understanding")

def create_classification_chain():
    """Create a chain to classify the inquiry"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=150
    )
    
    prompt = PromptTemplate(
        input_variables=["understanding"],
        template="""Based on the customer inquiry analysis, classify the issue.

Analysis: {understanding}

Categories:
- Technical: password, login, app crashes, system issues
- Billing: charges, payments, invoices, pricing
- Sales: upgrades, features, plans, pricing
- General: general questions, feedback, complaints

Return a JSON object with this exact format:
{{
  "category": "technical/billing/sales/general",
  "subcategory": "specific subcategory",
  "complexity": "simple/moderate/complex",
  "estimated_resolution_time": "time estimate",
  "requires_escalation": true/false
}}

JSON Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="classification")

def create_routing_chain():
    """Create a chain to determine routing"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=150
    )
    
    prompt = PromptTemplate(
        input_variables=["understanding", "classification"],
        template="""Based on the understanding and classification, determine the best routing.

Understanding: {understanding}
Classification: {classification}

Departments:
- technical: system issues, login problems, app crashes
- billing: payment issues, charges, invoices
- sales: upgrades, features, plans
- general: general inquiries, feedback
- escalation: urgent issues, complex problems

Return a JSON object with this exact format:
{{
  "department": "technical/billing/sales/general/escalation",
  "priority": "low/medium/high/urgent",
  "agent_requirements": ["skill1", "skill2"],
  "sla_target": "time target"
}}

JSON Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="routing")

def create_response_chain():
    """Create a chain to generate appropriate response"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,  # Higher temperature for more natural responses
        max_tokens=300
    )
    
    prompt = PromptTemplate(
        input_variables=["customer_message", "understanding", "classification", "routing"],
        template="""Generate an appropriate customer service response based on the analysis.

Original Message: {customer_message}
Understanding: {understanding}
Classification: {classification}
Routing: {routing}

Create a professional, empathetic response that:
1. Acknowledges the customer's issue and emotion
2. Shows understanding of their situation
3. Provides clear next steps
4. Sets appropriate expectations
5. Maintains a helpful, professional tone

Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="response")

def create_customer_service_chain():
    """Create the complete customer service workflow"""
    
    # Create individual chains
    understanding_chain = create_understanding_chain()
    classification_chain = create_classification_chain()
    routing_chain = create_routing_chain()
    response_chain = create_response_chain()
    
    # Create the sequential chain
    customer_service_chain = SequentialChain(
        chains=[understanding_chain, classification_chain, routing_chain, response_chain],
        input_variables=["customer_message"],
        output_variables=["understanding", "classification", "routing", "response"],
        verbose=True
    )
    
    return customer_service_chain

def parse_json_output(output_str):
    """Parse JSON output from LLM"""
    try:
        # Try to extract JSON from the output
        if isinstance(output_str, str):
            # Find JSON-like content
            start = output_str.find('{')
            end = output_str.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = output_str[start:end]
                return json.loads(json_str)
        return output_str
    except:
        return output_str

def run_customer_service_example():
    """Run the customer service example with improved parsing"""
    print("🎯 Fixed Customer Service Example: Understand → Classify → Route → Respond")
    print("=" * 70)
    
    # Create the chain
    chain = create_customer_service_chain()
    
    # Test customer messages
    customer_messages = [
        "I've been trying to reset my password for 2 hours and nothing works! This is ridiculous!",
        "Hi, I'm interested in upgrading my plan. Can you tell me about the premium features?",
        "My bill this month is $200 more than usual. I don't understand why it's so high.",
        "The app keeps crashing every time I try to upload a file. I have a deadline tomorrow!",
        "Thanks for the great service! I wanted to let you know how much I appreciate your help."
    ]
    
    for i, message in enumerate(customer_messages, 1):
        print(f"\n📧 Customer Message {i}:")
        print(f"'{message}'")
        print("=" * 60)
        
        try:
            # Run the chain
            result = chain.invoke({"customer_message": message})
            
            # Parse JSON outputs
            understanding = parse_json_output(result["understanding"])
            classification = parse_json_output(result["classification"])
            routing = parse_json_output(result["routing"])
            
            # Display results in a structured way
            print(f"\n🔍 UNDERSTANDING:")
            print(f"Main Issue: {understanding.get('main_issue', 'N/A')}")
            print(f"Emotion: {understanding.get('customer_emotion', 'N/A')}")
            print(f"Urgency: {understanding.get('urgency_level', 'N/A')}")
            print(f"Context: {understanding.get('context', [])}")
            
            print(f"\n🏷️  CLASSIFICATION:")
            print(f"Category: {classification.get('category', 'N/A')}")
            print(f"Subcategory: {classification.get('subcategory', 'N/A')}")
            print(f"Complexity: {classification.get('complexity', 'N/A')}")
            print(f"Resolution Time: {classification.get('estimated_resolution_time', 'N/A')}")
            print(f"Escalation: {classification.get('requires_escalation', 'N/A')}")
            
            print(f"\n🔄 ROUTING:")
            print(f"Department: {routing.get('department', 'N/A')}")
            print(f"Priority: {routing.get('priority', 'N/A')}")
            print(f"Agent Requirements: {routing.get('agent_requirements', [])}")
            print(f"SLA Target: {routing.get('sla_target', 'N/A')}")
            
            print(f"\n💬 RESPONSE:")
            print(result["response"])
            
        except Exception as e:
            print(f"❌ Error: {e}")

def emotion_analysis_demo():
    """Demonstrate emotion detection with examples"""
    print("\n🎭 Emotion Detection Demo")
    print("=" * 40)
    
    examples = [
        ("I'm so frustrated with this service!", "Expected: frustrated (high intensity)"),
        ("Thanks for your help!", "Expected: happy (positive feedback)"),
        ("I don't understand why this happened", "Expected: confused (seeking explanation)"),
        ("This is absolutely ridiculous!", "Expected: angry (strong negative language)"),
        ("I have a deadline in 30 minutes!", "Expected: stressed (time pressure)")
    ]
    
    for message, expected in examples:
        print(f"\n📝 Message: '{message}'")
        print(f"🎯 {expected}")
        
        # Simple emotion detection
        emotion_indicators = {
            "frustrated": ["frustrated", "nothing works", "trying for"],
            "happy": ["thanks", "appreciate", "great", "love"],
            "confused": ["don't understand", "why", "confused"],
            "angry": ["ridiculous", "useless", "terrible"],
            "stressed": ["deadline", "urgent", "meeting", "soon"]
        }
        
        detected_emotion = "neutral"
        for emotion, indicators in emotion_indicators.items():
            if any(indicator in message.lower() for indicator in indicators):
                detected_emotion = emotion
                break
        
        print(f"🔍 Detected: {detected_emotion}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Run emotion analysis demo
    emotion_analysis_demo()
    
    # Run the main example
    run_customer_service_example() 