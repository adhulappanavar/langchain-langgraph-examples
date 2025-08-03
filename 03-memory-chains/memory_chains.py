"""
Example 3: Memory Chains

This example demonstrates how to add conversation memory to the customer service workflow.
We'll build upon the customer service example from Example 2 and add memory components
to maintain context across multiple interactions.
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.schema import HumanMessage, AIMessage
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

def create_memory_aware_understanding_chain():
    """Create a chain to understand customer inquiry with memory context"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=200
    )
    
    prompt = PromptTemplate(
        input_variables=["customer_message"],
        template="""Analyze the following customer inquiry.

Current Message: {customer_message}

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
  "context": ["key detail 1", "key detail 2"],
  "is_followup": true/false,
  "references_previous": "what previous issue this refers to"
}}

JSON Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="understanding")

def create_memory_aware_classification_chain():
    """Create a chain to classify the inquiry with memory context"""
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
  "requires_escalation": true/false,
  "is_new_issue": true/false,
  "related_to_previous": "how this relates to previous issues"
}}

JSON Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="classification")

def create_memory_aware_routing_chain():
    """Create a chain to determine routing with memory context"""
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
  "sla_target": "time target",
  "should_continue_session": true/false,
  "session_notes": "important context for next agent"
}}

JSON Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="routing")

def create_memory_aware_response_chain():
    """Create a chain to generate contextual responses"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=300
    )
    
    prompt = PromptTemplate(
        input_variables=["customer_message", "understanding", "classification", "routing"],
        template="""Generate an appropriate customer service response based on the analysis.

Current Message: {customer_message}
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

def create_memory_aware_customer_service_chain():
    """Create the complete memory-aware customer service workflow"""
    
    # Create individual chains with memory
    understanding_chain = create_memory_aware_understanding_chain()
    classification_chain = create_memory_aware_classification_chain()
    routing_chain = create_memory_aware_routing_chain()
    response_chain = create_memory_aware_response_chain()
    
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
        if isinstance(output_str, str):
            start = output_str.find('{')
            end = output_str.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = output_str[start:end]
                return json.loads(json_str)
        return output_str
    except:
        return output_str

def run_multi_turn_conversation():
    """Run a multi-turn conversation example"""
    print("🎯 Memory Chains Example: Multi-turn Customer Service Conversation")
    print("=" * 70)
    
    # Create the chain
    chain = create_memory_aware_customer_service_chain()
    
    # Multi-turn conversation scenarios
    conversation_scenarios = [
        # Scenario 1: Technical issue with follow-ups
        [
            "I can't log into my account. The password reset isn't working.",
            "I tried that already. It's been 2 hours and nothing works!",
            "Can you just reset it for me? I have an important meeting in 30 minutes.",
            "Thanks! That worked. You're the best!"
        ],
        # Scenario 2: Billing issue with clarification
        [
            "My bill is much higher than usual this month.",
            "It's $200 more than last month. I don't understand why.",
            "Can you explain what the extra charges are for?",
            "That makes sense now. Thanks for clarifying."
        ],
        # Scenario 3: Sales inquiry with follow-up
        [
            "Hi, I'm interested in upgrading my plan.",
            "What are the main differences between basic and premium?",
            "How much more does the premium plan cost?",
            "Perfect! I'd like to upgrade to premium."
        ]
    ]
    
    for scenario_num, messages in enumerate(conversation_scenarios, 1):
        print(f"\n🔄 Conversation Scenario {scenario_num}")
        print("=" * 50)
        
        # Reset memory for each scenario
        chain = create_memory_aware_customer_service_chain()
        
        for turn_num, message in enumerate(messages, 1):
            print(f"\n📧 Turn {turn_num}: '{message}'")
            print("-" * 40)
            
            try:
                # Run the chain
                result = chain.invoke({"customer_message": message})
                
                # Parse JSON outputs
                understanding = parse_json_output(result["understanding"])
                classification = parse_json_output(result["classification"])
                routing = parse_json_output(result["routing"])
                
                # Display results
                print(f"🔍 Understanding:")
                print(f"  Main Issue: {understanding.get('main_issue', 'N/A')}")
                print(f"  Emotion: {understanding.get('customer_emotion', 'N/A')}")
                print(f"  Is Follow-up: {understanding.get('is_followup', 'N/A')}")
                print(f"  References: {understanding.get('references_previous', 'N/A')}")
                
                print(f"\n🏷️  Classification:")
                print(f"  Category: {classification.get('category', 'N/A')}")
                print(f"  Is New Issue: {classification.get('is_new_issue', 'N/A')}")
                print(f"  Related To: {classification.get('related_to_previous', 'N/A')}")
                
                print(f"\n🔄 Routing:")
                print(f"  Department: {routing.get('department', 'N/A')}")
                print(f"  Continue Session: {routing.get('should_continue_session', 'N/A')}")
                print(f"  Session Notes: {routing.get('session_notes', 'N/A')}")
                
                print(f"\n💬 Response:")
                print(result["response"])
                
            except Exception as e:
                print(f"❌ Error: {e}")

def demonstrate_memory_types():
    """Demonstrate different types of memory components"""
    print("\n🧠 Memory Types Demo")
    print("=" * 40)
    
    # 1. ConversationBufferMemory
    print("\n1️⃣ ConversationBufferMemory (Full History)")
    buffer_memory = ConversationBufferMemory(return_messages=True)
    
    # Add some messages
    buffer_memory.chat_memory.add_user_message("I can't log in")
    buffer_memory.chat_memory.add_ai_message("I understand you're having login issues. Let me help you.")
    buffer_memory.chat_memory.add_user_message("I tried resetting my password")
    buffer_memory.chat_memory.add_ai_message("I see you've already tried password reset. Let me escalate this.")
    
    print("Full conversation history:")
    for message in buffer_memory.chat_memory.messages:
        role = "👤 User" if isinstance(message, HumanMessage) else "🤖 Assistant"
        print(f"  {role}: {message.content}")
    
    # 2. ConversationSummaryMemory
    print("\n2️⃣ ConversationSummaryMemory (Summarized)")
    summary_memory = ConversationSummaryMemory(llm=ChatOpenAI(temperature=0))
    
    # Add the same messages
    summary_memory.chat_memory.add_user_message("I can't log in")
    summary_memory.chat_memory.add_ai_message("I understand you're having login issues. Let me help you.")
    summary_memory.chat_memory.add_user_message("I tried resetting my password")
    summary_memory.chat_memory.add_ai_message("I see you've already tried password reset. Let me escalate this.")
    
    print("Conversation summary:")
    print(f"  {summary_memory.buffer}")

def interactive_memory_conversation():
    """Run an interactive conversation with memory"""
    print("\n🎮 Interactive Memory Conversation")
    print("=" * 50)
    print("Start a conversation with the customer service bot.")
    print("The bot will remember your previous messages and maintain context.")
    print("Type 'quit' to end the conversation.")
    print("-" * 50)
    
    # Create the chain
    chain = create_memory_aware_customer_service_chain()
    
    while True:
        message = input("\n👤 You: ").strip()
        
        if message.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye! Thanks for the conversation.")
            break
        
        if not message:
            print("⚠️  Please enter a message!")
            continue
        
        try:
            print("🤔 Processing...")
            result = chain.invoke({"customer_message": message})
            
            # Parse and display understanding
            understanding = parse_json_output(result["understanding"])
            print(f"\n🔍 Understanding: {understanding.get('customer_emotion', 'N/A')} emotion, "
                  f"{understanding.get('urgency_level', 'N/A')} urgency")
            
            if understanding.get('is_followup'):
                print(f"📝 Follow-up detected: {understanding.get('references_previous', 'N/A')}")
            
            print(f"\n🤖 Assistant: {result['response']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Demonstrate memory types
    demonstrate_memory_types()
    
    # Run multi-turn conversation examples
    run_multi_turn_conversation()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive memory conversation? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_memory_conversation()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 