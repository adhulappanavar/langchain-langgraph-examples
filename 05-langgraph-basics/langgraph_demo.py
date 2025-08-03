"""
Example 5: LangGraph Basics Demo

This example demonstrates the core concepts of LangGraph without requiring OpenAI API:
- State management
- Node functions
- Workflow orchestration
- Conditional logic
"""

import os
from typing import Dict, List, Any, TypedDict, Annotated
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Define the state structure
class WorkflowState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]
    customer_id: str
    issue_type: str
    priority: str
    weather_info: str
    calculation_result: str
    customer_info: str
    workflow_status: str

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
        # Simulate weather check
        location = "New York"  # Default location
        weather_info = f"Weather in {location}: 22°C, Sunny, Humidity: 65%, Wind: 10 km/h"
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
        # Simulate calculation
        calculation_result = "Result: 150 * 1.085 = 162.75"
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
        customer_info = f"Customer {customer_id}: John Doe, john.doe@example.com, Orders: 2"
        state["customer_info"] = customer_info
        
        # Add response to messages
        state["messages"].append(AIMessage(content=f"Customer information: {customer_info}"))
        print(f"👤 Customer info looked up: {customer_info}")
    else:
        state["customer_info"] = "Not needed"
        print("👤 Customer lookup skipped")
    
    state["workflow_status"] = "customer_lookup_done"
    return state

def generate_final_response(state: WorkflowState) -> WorkflowState:
    """Generate a final response based on all collected information"""
    print("📝 Generating final response...")
    
    # Create a comprehensive response
    response_parts = []
    
    if state["weather_info"] != "Not needed":
        response_parts.append(f"Weather: {state['weather_info']}")
    
    if state["calculation_result"] != "Not needed":
        response_parts.append(f"Calculation: {state['calculation_result']}")
    
    if state["customer_info"] != "Not needed":
        response_parts.append(f"Customer: {state['customer_info']}")
    
    if not response_parts:
        response_parts.append("Thank you for your inquiry. How can I help you further?")
    
    final_response = " | ".join(response_parts)
    state["messages"].append(AIMessage(content=final_response))
    state["workflow_status"] = "completed"
    
    print(f"📝 Final response: {final_response}")
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
    workflow.add_node("generate_response", generate_final_response)
    
    # Add edges
    workflow.add_edge("analyze_request", "check_weather")
    workflow.add_edge("check_weather", "perform_calculations")
    workflow.add_edge("perform_calculations", "lookup_customer")
    workflow.add_edge("lookup_customer", "generate_response")
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
                "customer_info": "",
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
    """Demonstrate how state is managed throughout the workflow"""
    print("\n📊 State Management Demo")
    print("=" * 40)
    
    # Create the workflow
    app = create_customer_service_workflow()
    
    # Test a complex scenario
    initial_state = {
        "messages": [HumanMessage(content="I need weather info and want to calculate shipping costs")],
        "customer_id": "CUST456",
        "issue_type": "",
        "priority": "",
        "weather_info": "",
        "calculation_result": "",
        "customer_info": "",
        "workflow_status": ""
    }
    
    try:
        result = app.invoke(initial_state)
        
        print("📊 State throughout workflow:")
        print(f"  - Issue Type: {result['issue_type']}")
        print(f"  - Priority: {result['priority']}")
        print(f"  - Weather Info: {result['weather_info']}")
        print(f"  - Calculation Result: {result['calculation_result']}")
        print(f"  - Customer Info: {result['customer_info']}")
        print(f"  - Workflow Status: {result['workflow_status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demonstrate_workflow_structure():
    """Demonstrate the workflow structure and concepts"""
    print("\n🏗️  Workflow Structure Demo")
    print("=" * 40)
    
    print("📋 LangGraph Core Concepts:")
    print("1. StateGraph: The main workflow container")
    print("2. Nodes: Individual processing functions")
    print("3. Edges: Connections between nodes")
    print("4. State: Data that flows through the workflow")
    print("5. Conditional Edges: Dynamic routing based on conditions")
    
    print("\n🔄 Our Workflow Structure:")
    print("analyze_request → check_weather → perform_calculations → lookup_customer → generate_response")
    print("                                                                    ↓")
    print("                                                              should_continue")
    print("                                                                    ↓")
    print("                                                              continue/end")
    
    print("\n📊 State Flow:")
    print("Initial State → Node 1 → Updated State → Node 2 → Updated State → ... → Final State")
    
    print("\n🎯 Key Benefits:")
    print("✅ Structured workflow with clear steps")
    print("✅ State persistence across nodes")
    print("✅ Conditional logic for dynamic routing")
    print("✅ Modular design with reusable nodes")
    print("✅ Easy to debug and maintain")

if __name__ == "__main__":
    # Run workflow examples
    run_workflow_examples()
    
    # Demonstrate state management
    demonstrate_state_management()
    
    # Demonstrate workflow structure
    demonstrate_workflow_structure()
    
    print("\n🎉 LangGraph Basics demonstration completed!")
    print("\nKey Concepts Demonstrated:")
    print("✅ State Management: Information flows through the workflow")
    print("✅ Node Functions: Each step processes the state")
    print("✅ Conditional Logic: Different paths based on conditions")
    print("✅ Workflow Orchestration: Structured multi-step processes")
    print("✅ Graph Structure: Nodes and edges define the workflow") 