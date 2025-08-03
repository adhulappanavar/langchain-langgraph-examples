"""
Customer Service Example: Understand → Classify → Route → Respond

This example demonstrates how sequential chains can be used for customer service automation.
We'll process customer inquiries through a 4-step workflow.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
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
    customer_emotion: str = Field(description="Customer's emotional state (frustrated, happy, confused, etc.)")
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
    """Create a chain to understand the customer inquiry"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,  # Low temperature for consistent understanding
        max_tokens=200
    )
    
    parser = PydanticOutputParser(pydantic_object=CustomerInquiry)
    
    prompt = PromptTemplate(
        input_variables=["customer_message"],
        template="""Analyze the following customer inquiry and extract key information:

Customer Message: {customer_message}

Please understand:
- What is the main issue or question?
- What is the customer's emotional state?
- How urgent is this issue?
- What additional context is provided?

{format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="understanding")

def create_classification_chain():
    """Create a chain to classify the inquiry"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=150
    )
    
    parser = PydanticOutputParser(pydantic_object=Classification)
    
    prompt = PromptTemplate(
        input_variables=["understanding"],
        template="""Based on the customer inquiry analysis, classify the issue:

{understanding}

Please classify:
- Main category and subcategory
- Complexity level
- Estimated resolution time
- Whether escalation is needed

{format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="classification")

def create_routing_chain():
    """Create a chain to determine routing"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=150
    )
    
    parser = PydanticOutputParser(pydantic_object=RoutingDecision)
    
    prompt = PromptTemplate(
        input_variables=["understanding", "classification"],
        template="""Based on the understanding and classification, determine the best routing:

Understanding: {understanding}
Classification: {classification}

Please determine:
- Which department should handle this
- Priority level
- Required agent skills
- SLA target time

{format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
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
        template="""Generate an appropriate customer service response based on the analysis:

Original Message: {customer_message}
Understanding: {understanding}
Classification: {classification}
Routing: {routing}

Create a professional, empathetic response that:
1. Acknowledges the customer's issue
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

def run_customer_service_example():
    """Run the customer service example"""
    print("🎯 Customer Service Example: Understand → Classify → Route → Respond")
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
            
            # Display results in a structured way
            print(f"\n🔍 UNDERSTANDING:")
            print(f"Main Issue: {result['understanding']}")
            
            print(f"\n🏷️  CLASSIFICATION:")
            print(f"Category: {result['classification']}")
            
            print(f"\n🔄 ROUTING:")
            print(f"Department: {result['routing']}")
            
            print(f"\n💬 RESPONSE:")
            print(result['response'])
            
        except Exception as e:
            print(f"❌ Error: {e}")

def interactive_customer_service():
    """Run the customer service chain in interactive mode"""
    print("\n🎮 Interactive Customer Service Mode")
    print("Enter customer messages to process (type 'quit' to exit)")
    print("-" * 60)
    
    chain = create_customer_service_chain()
    
    while True:
        message = input("\n📧 Enter customer message: ").strip()
        
        if message.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not message:
            print("⚠️  Please enter a message!")
            continue
        
        try:
            print("🤔 Processing customer inquiry...")
            result = chain.invoke({"customer_message": message})
            
            print(f"\n🔍 UNDERSTANDING:")
            print(f"Main Issue: {result['understanding']}")
            
            print(f"\n🏷️  CLASSIFICATION:")
            print(f"Category: {result['classification']}")
            
            print(f"\n🔄 ROUTING:")
            print(f"Department: {result['routing']}")
            
            print(f"\n💬 RESPONSE:")
            print(result['response'])
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_manual_workflow():
    """Demonstrate manual chain composition for customer service"""
    print("\n🔧 Manual Customer Service Workflow Demo")
    print("=" * 50)
    
    # Create individual chains
    understanding_chain = create_understanding_chain()
    classification_chain = create_classification_chain()
    routing_chain = create_routing_chain()
    response_chain = create_response_chain()
    
    message = "I can't access my account and I have an important meeting in 30 minutes!"
    
    print(f"📧 Customer Message: '{message}'")
    
    print("\n🔍 Step 1: Understanding...")
    understanding_result = understanding_chain.invoke({"customer_message": message})
    print(f"Understanding: {understanding_result}")
    
    print("\n🏷️  Step 2: Classification...")
    classification_result = classification_chain.invoke({"understanding": understanding_result})
    print(f"Classification: {classification_result}")
    
    print("\n🔄 Step 3: Routing...")
    routing_result = routing_chain.invoke({"understanding": understanding_result, "classification": classification_result})
    print(f"Routing: {routing_result}")
    
    print("\n💬 Step 4: Response Generation...")
    response_result = response_chain.invoke({
        "customer_message": message,
        "understanding": understanding_result,
        "classification": classification_result,
        "routing": routing_result
    })
    print(f"Response: {response_result}")
    
    print("\n✨ This demonstrates manual workflow composition!")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Run the main example
    run_customer_service_example()
    
    # Demonstrate manual workflow
    demonstrate_manual_workflow()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive customer service mode? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_customer_service()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 