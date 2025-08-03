"""
Example 5: LangGraph Basics

This example demonstrates how to create complex workflows using LangGraph.
We'll build upon the tools and agents from Example 4 and add workflow orchestration,
state management, and conditional logic.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, TypedDict, Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Define the state structure
class WorkflowState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]
    customer_id: str
    issue_type: str
    priority: str
    weather_info: str
    calculation_result: str
    search_results: str
    customer_info: str
    next_step: str
    workflow_status: str

# Custom tools (simplified versions from Example 4)
class WeatherTool(BaseTool):
    name = "weather"
    description = "Get current weather information for a specific location"
    
    def _run(self, location: str) -> str:
        try:
            weather_data = {
                "location": location,
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%",
                "wind": "10 km/h"
            }
            return f"Weather in {location}: {weather_data['temperature']}, {weather_data['condition']}, Humidity: {weather_data['humidity']}, Wind: {weather_data['wind']}"
        except Exception as e:
            return f"Error getting weather for {location}: {str(e)}"
    
    def _arun(self, location: str):
        raise NotImplementedError("Async not implemented")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Perform mathematical calculations"
    
    def _run(self, expression: str) -> str:
        try:
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression)
            return f"Result: {expression} = {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
    
    def _arun(self, expression: str):
        raise NotImplementedError("Async not implemented")

class CustomerDatabaseTool(BaseTool):
    name = "customer_database"
    description = "Look up customer information and order history"
    
    def _run(self, customer_id: str) -> str:
        try:
            customer_data = {
                "customer_id": customer_id,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "orders": [
                    {"order_id": "ORD001", "date": "2024-01-15", "total": "$150.00"},
                    {"order_id": "ORD002", "date": "2024-02-20", "total": "$75.50"}
                ],
                "status": "active"
            }
            return f"Customer {customer_id}: {customer_data['name']}, {customer_data['email']}, Orders: {len(customer_data['orders'])}"
        except Exception as e:
            return f"Error looking up customer {customer_id}: {str(e)}"
    
    def _arun(self, customer_id: str):
        raise NotImplementedError("Async not implemented")

# Node functions for the workflow
def analyze_customer_request(state: WorkflowState) -> WorkflowState:
    """Analyze the customer request and determine the issue type and priority"""
    print("🔍 Analyzing customer request...")
    
    # Get the latest message
    messages = state["messages"]
    if not messages:
        return state
    
    latest_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
    
    # Simple analysis logic
    if "weather" in latest_message.lower():
        state["issue_type"] = "weather_inquiry"
        state["priority"] = "medium"
    elif "calculate" in latest_message.lower() or "cost" in latest_message.lower():
        state["issue_type"] = "calculation_request"
        state["priority"] = "high"
    elif "customer" in latest_message.lower() or "order" in latest_message.lower():
        state["issue_type"] = "customer_inquiry"
        state["priority"] = "high"
    else:
        state["issue_type"] = "general_inquiry"
        state["priority"] = "low"
    
    state["workflow_status"] = "analyzed"
    print(f"📊 Issue Type: {state['issue_type']}, Priority: {state['priority']}")
    
    return state

def check_weather_if_needed(state: WorkflowState) -> WorkflowState:
    """Check weather if the request is weather-related"""
    print("🌤️  Checking weather if needed...")
    
    if state["issue_type"] == "weather_inquiry":
        # Extract location from message (simplified)
        messages = state["messages"]
        latest_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        
        # Simple location extraction
        location = "New York"  # Default location
        if "chicago" in latest_message.lower():
            location = "Chicago"
        elif "miami" in latest_message.lower():
            location = "Miami"
        elif "los angeles" in latest_message.lower():
            location = "Los Angeles"
        
        weather_tool = WeatherTool()
        weather_info = weather_tool._run(location)
        state["weather_info"] = weather_info
        
        # Add response to messages
        state["messages"].append(AIMessage(content=f"Weather information: {weather_info}"))
        print(f"🌤️  Weather checked: {weather_info}")
    else:
        state["weather_info"] = "Not needed"
        print("🌤️  Weather check skipped")
    
    state["workflow_status"] = "weather_checked"
    return state

def perform_calculations_if_needed(state: WorkflowState) -> WorkflowState:
    """Perform calculations if the request involves calculations"""
    print("🧮 Performing calculations if needed...")
    
    if state["issue_type"] == "calculation_request":
        messages = state["messages"]
        latest_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        
        # Simple calculation extraction
        calculation = "150 * 1.085"  # Default calculation
        if "tax" in latest_message.lower():
            calculation = "150 * 1.085"  # 8.5% tax
        elif "shipping" in latest_message.lower():
            calculation = "25 * 1.09"  # 9% tax on shipping
        
        calculator_tool = CalculatorTool()
        calculation_result = calculator_tool._run(calculation)
        state["calculation_result"] = calculation_result
        
        # Add response to messages
        state["messages"].append(AIMessage(content=f"Calculation result: {calculation_result}"))
        print(f"🧮 Calculation performed: {calculation_result}")
    else:
        state["calculation_result"] = "Not needed"
        print("🧮 Calculation skipped")
    
    state["workflow_status"] = "calculations_done"
    return state

def lookup_customer_info_if_needed(state: WorkflowState) -> WorkflowState:
    """Look up customer information if needed"""
    print("👤 Looking up customer info if needed...")
    
    if state["issue_type"] == "customer_inquiry":
        customer_id = state.get("customer_id", "CUST123")
        
        customer_tool = CustomerDatabaseTool()
        customer_info = customer_tool._run(customer_id)
        state["customer_info"] = customer_info
        
        # Add response to messages
        state["messages"].append(AIMessage(content=f"Customer information: {customer_info}"))
        print(f"👤 Customer info retrieved: {customer_info}")
    else:
        state["customer_info"] = "Not needed"
        print("👤 Customer lookup skipped")
    
    state["workflow_status"] = "customer_info_retrieved"
    return state

def determine_next_step(state: WorkflowState) -> WorkflowState:
    """Determine the next step based on the current state"""
    print("🎯 Determining next step...")
    
    issue_type = state["issue_type"]
    priority = state["priority"]
    
    if priority == "high":
        if issue_type == "calculation_request":
            state["next_step"] = "provide_calculation_response"
        elif issue_type == "customer_inquiry":
            state["next_step"] = "provide_customer_response"
        else:
            state["next_step"] = "escalate_to_human"
    elif priority == "medium":
        if issue_type == "weather_inquiry":
            state["next_step"] = "provide_weather_response"
        else:
            state["next_step"] = "provide_general_response"
    else:
        state["next_step"] = "provide_general_response"
    
    state["workflow_status"] = "next_step_determined"
    print(f"🎯 Next step: {state['next_step']}")
    
    return state

def generate_final_response(state: WorkflowState) -> WorkflowState:
    """Generate the final response based on all collected information"""
    print("💬 Generating final response...")
    
    response_parts = []
    
    # Add weather information if available
    if state.get("weather_info") and state["weather_info"] != "Not needed":
        response_parts.append(f"Weather: {state['weather_info']}")
    
    # Add calculation result if available
    if state.get("calculation_result") and state["calculation_result"] != "Not needed":
        response_parts.append(f"Calculation: {state['calculation_result']}")
    
    # Add customer information if available
    if state.get("customer_info") and state["customer_info"] != "Not needed":
        response_parts.append(f"Customer: {state['customer_info']}")
    
    # Generate appropriate response based on next step
    next_step = state["next_step"]
    
    if next_step == "provide_calculation_response":
        response = f"Here's your calculation: {state.get('calculation_result', 'Calculation completed')}"
    elif next_step == "provide_customer_response":
        response = f"Here's your customer information: {state.get('customer_info', 'Customer info retrieved')}"
    elif next_step == "provide_weather_response":
        response = f"Here's the weather information: {state.get('weather_info', 'Weather checked')}"
    elif next_step == "escalate_to_human":
        response = "This is a high-priority issue. I'm escalating this to a human agent who will contact you shortly."
    else:
        response = "I've processed your request. " + " ".join(response_parts) if response_parts else "Thank you for your inquiry."
    
    # Add final response to messages
    state["messages"].append(AIMessage(content=response))
    state["workflow_status"] = "completed"
    
    print(f"💬 Final response: {response}")
    return state

def should_continue(state: WorkflowState) -> str:
    """Determine if the workflow should continue or end"""
    if state["workflow_status"] == "completed":
        return "end"
    else:
        return "continue"

def create_customer_service_workflow():
    """Create the customer service workflow using LangGraph"""
    
    # Create the state graph
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("analyze_request", analyze_customer_request)
    workflow.add_node("check_weather", check_weather_if_needed)
    workflow.add_node("perform_calculations", perform_calculations_if_needed)
    workflow.add_node("lookup_customer", lookup_customer_info_if_needed)
    workflow.add_node("determine_next", determine_next_step)
    workflow.add_node("generate_response", generate_final_response)
    
    # Add edges
    workflow.add_edge("analyze_request", "check_weather")
    workflow.add_edge("check_weather", "perform_calculations")
    workflow.add_edge("perform_calculations", "lookup_customer")
    workflow.add_edge("lookup_customer", "determine_next")
    workflow.add_edge("determine_next", "generate_response")
    workflow.add_conditional_edges("generate_response", should_continue, {
        "continue": "analyze_request",
        "end": END
    })
    
    # Set entry point
    workflow.set_entry_point("analyze_request")
    
    # Compile the workflow
    app = workflow.compile(checkpointer=MemorySaver())
    
    return app

def run_workflow_examples():
    """Run examples of the customer service workflow"""
    print("🔄 LangGraph Basics: Customer Service Workflow")
    print("=" * 60)
    
    # Create the workflow
    app = create_customer_service_workflow()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Weather Inquiry",
            "message": "What's the weather like in Chicago? I'm concerned about delivery delays.",
            "customer_id": "CUST001"
        },
        {
            "name": "Calculation Request",
            "message": "I need to calculate the total cost for my order of $150 with 8.5% tax.",
            "customer_id": "CUST002"
        },
        {
            "name": "Customer Inquiry",
            "message": "Can you look up my customer information? My ID is CUST123.",
            "customer_id": "CUST123"
        },
        {
            "name": "Complex Request",
            "message": "I'm in Miami and need to know the weather, plus calculate shipping costs of $25 with 9% tax.",
            "customer_id": "CUST003"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"Message: {scenario['message']}")
        print("-" * 50)
        
        try:
            # Initialize state
            initial_state = {
                "messages": [HumanMessage(content=scenario['message'])],
                "customer_id": scenario['customer_id'],
                "issue_type": "",
                "priority": "",
                "weather_info": "",
                "calculation_result": "",
                "search_results": "",
                "customer_info": "",
                "next_step": "",
                "workflow_status": ""
            }
            
            # Run the workflow
            result = app.invoke(initial_state)
            
            print(f"\n✅ Workflow completed!")
            print(f"Final Status: {result['workflow_status']}")
            print(f"Final Response: {result['messages'][-1].content}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_state_management():
    """Demonstrate state management in the workflow"""
    print("\n📊 State Management Demo")
    print("=" * 40)
    
    app = create_customer_service_workflow()
    
    # Test with a simple scenario
    initial_state = {
        "messages": [HumanMessage(content="What's the weather in New York?")],
        "customer_id": "CUST001",
        "issue_type": "",
        "priority": "",
        "weather_info": "",
        "calculation_result": "",
        "search_results": "",
        "customer_info": "",
        "next_step": "",
        "workflow_status": ""
    }
    
    print("🔄 Running workflow with state tracking...")
    
    try:
        result = app.invoke(initial_state)
        
        print("\n📊 Final State:")
        for key, value in result.items():
            if key != "messages":
                print(f"  {key}: {value}")
        
        print(f"\n💬 Messages:")
        for i, message in enumerate(result["messages"]):
            role = "👤 User" if isinstance(message, HumanMessage) else "🤖 Assistant"
            print(f"  {i+1}. {role}: {message.content}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def interactive_workflow():
    """Run an interactive workflow session"""
    print("\n🎮 Interactive Workflow Session")
    print("=" * 50)
    print("Start a conversation with the customer service workflow.")
    print("The workflow will process your request through multiple steps.")
    print("Type 'quit' to end the session.")
    print("-" * 50)
    
    app = create_customer_service_workflow()
    
    while True:
        message = input("\n👤 You: ").strip()
        
        if message.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye! Thanks for the conversation.")
            break
        
        if not message:
            print("⚠️  Please enter a message!")
            continue
        
        try:
            print("🔄 Processing through workflow...")
            
            initial_state = {
                "messages": [HumanMessage(content=message)],
                "customer_id": "CUST001",
                "issue_type": "",
                "priority": "",
                "weather_info": "",
                "calculation_result": "",
                "search_results": "",
                "customer_info": "",
                "next_step": "",
                "workflow_status": ""
            }
            
            result = app.invoke(initial_state)
            
            print(f"\n🤖 Assistant: {result['messages'][-1].content}")
            print(f"📊 Workflow Status: {result['workflow_status']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_workflow_visualization():
    """Demonstrate the workflow structure"""
    print("\n🔄 Workflow Structure Visualization")
    print("=" * 50)
    
    print("""
    Customer Service Workflow:
    
    ┌─────────────────┐
    │  analyze_request │ ← Entry Point
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │  check_weather   │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │perform_calculations│
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │ lookup_customer  │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │ determine_next   │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │generate_response │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │  should_continue │ ← Conditional Edge
    └─────────┬───────┘
              │
        ┌─────┴─────┐
        ▼           ▼
    ┌─────────┐ ┌─────────┐
    │  END    │ │continue │
    └─────────┘ └─────────┘
    """)

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Demonstrate workflow visualization
    demonstrate_workflow_visualization()
    
    # Demonstrate state management
    demonstrate_state_management()
    
    # Run workflow examples
    run_workflow_examples()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive workflow? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_workflow()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 