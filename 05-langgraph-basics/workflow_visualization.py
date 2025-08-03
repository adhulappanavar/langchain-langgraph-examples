"""
LangGraph Workflow Flow Visualization

This example visually demonstrates how data flows through a LangGraph workflow,
showing the state changes at each step and how decisions are made.
"""

import time
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

def visualize_workflow_flow():
    """Visualize the complete workflow flow with state changes"""
    print("🔄 LangGraph Workflow Flow Visualization")
    print("=" * 60)
    
    print("\n📋 Customer Service Workflow Overview")
    print("-" * 40)
    print("Input: Customer message")
    print("Output: Comprehensive response with relevant information")
    print("Flow: 5 main nodes with conditional routing")
    
    print("\n🏗️  Workflow Structure")
    print("-" * 40)
    print("┌─────────────────┐")
    print("│  analyze_request│ ← Entry Point")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│  check_weather  │")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│perform_calculat.│")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│ lookup_customer │")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│generate_response│")
    print("└─────────┬───────┘")
    print("          │")
    print("          ▼")
    print("┌─────────────────┐")
    print("│ should_continue │ ← Decision Point")
    print("└─────────┬───────┘")
    print("          │")
    print("    ┌─────┴─────┐")
    print("    ▼           ▼")
    print("┌─────────┐ ┌─────┐")
    print("│continue │ │ END │")
    print("└─────────┘ └─────┘")

def demonstrate_flow_with_example():
    """Demonstrate the flow with a specific example"""
    print("\n🎯 Example: Weather + Calculation Request")
    print("-" * 40)
    print("Customer Message: 'I need weather info and want to calculate shipping costs'")
    print("Customer ID: CUST456")
    
    print("\n📊 Step-by-Step Flow Visualization")
    print("=" * 50)
    
    # Step 1: Initial State
    print("\n🔵 STEP 1: Initial State")
    print("-" * 30)
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
    print("📋 State:")
    for key, value in initial_state.items():
        if key == "messages":
            print(f"  {key}: [HumanMessage: '{value[0].content}']")
        else:
            print(f"  {key}: '{value}'")
    
    # Step 2: Analyze Request
    print("\n🔵 STEP 2: analyze_request Node")
    print("-" * 30)
    print("🔍 Processing: Analyzing customer request...")
    
    # Simulate analysis
    latest_message = initial_state["messages"][-1].content
    if "weather" in latest_message.lower() and "calculate" in latest_message.lower():
        issue_type = "complex_inquiry"
        priority = "high"
    elif "weather" in latest_message.lower():
        issue_type = "weather_inquiry"
        priority = "medium"
    elif "calculate" in latest_message.lower():
        issue_type = "calculation_request"
        priority = "high"
    else:
        issue_type = "general_inquiry"
        priority = "low"
    
    state_after_analysis = {
        "messages": initial_state["messages"],
        "customer_id": "CUST456",
        "issue_type": issue_type,
        "priority": priority,
        "weather_info": "",
        "calculation_result": "",
        "customer_info": "",
        "workflow_status": "analyzed"
    }
    
    print("📊 Analysis Result:")
    print(f"  Issue Type: {issue_type}")
    print(f"  Priority: {priority}")
    print("📋 Updated State:")
    for key, value in state_after_analysis.items():
        if key == "messages":
            print(f"  {key}: [HumanMessage: '{value[0].content}']")
        else:
            print(f"  {key}: '{value}'")
    
    # Step 3: Check Weather
    print("\n🔵 STEP 3: check_weather Node")
    print("-" * 30)
    print("🌤️  Processing: Checking weather if needed...")
    
    if state_after_analysis["issue_type"] in ["weather_inquiry", "complex_inquiry"]:
        weather_info = "Weather in New York: 22°C, Sunny, Humidity: 65%, Wind: 10 km/h"
        state_after_analysis["weather_info"] = weather_info
        state_after_analysis["messages"].append(AIMessage(content=f"Weather information: {weather_info}"))
        print(f"🌤️  Weather checked: {weather_info}")
    else:
        state_after_analysis["weather_info"] = "Not needed"
        print("🌤️  Weather check skipped")
    
    state_after_analysis["workflow_status"] = "weather_checked"
    
    print("📋 Updated State:")
    for key, value in state_after_analysis.items():
        if key == "messages":
            print(f"  {key}: [{len(value)} messages]")
            for i, msg in enumerate(value):
                print(f"    {i+1}. {type(msg).__name__}: '{msg.content}'")
        else:
            print(f"  {key}: '{value}'")
    
    # Step 4: Perform Calculations
    print("\n🔵 STEP 4: perform_calculations Node")
    print("-" * 30)
    print("🧮 Processing: Performing calculations if needed...")
    
    if state_after_analysis["issue_type"] in ["calculation_request", "complex_inquiry"]:
        calculation_result = "Result: 25 * 1.09 = 27.25 (shipping with tax)"
        state_after_analysis["calculation_result"] = calculation_result
        state_after_analysis["messages"].append(AIMessage(content=f"Calculation result: {calculation_result}"))
        print(f"🧮 Calculation performed: {calculation_result}")
    else:
        state_after_analysis["calculation_result"] = "Not needed"
        print("🧮 Calculation skipped")
    
    state_after_analysis["workflow_status"] = "calculations_done"
    
    print("📋 Updated State:")
    for key, value in state_after_analysis.items():
        if key == "messages":
            print(f"  {key}: [{len(value)} messages]")
            for i, msg in enumerate(value):
                print(f"    {i+1}. {type(msg).__name__}: '{msg.content}'")
        else:
            print(f"  {key}: '{value}'")
    
    # Step 5: Lookup Customer
    print("\n🔵 STEP 5: lookup_customer Node")
    print("-" * 30)
    print("👤 Processing: Looking up customer info if needed...")
    
    if state_after_analysis["issue_type"] == "customer_inquiry":
        customer_info = f"Customer CUST456: John Doe, john.doe@example.com, Orders: 2"
        state_after_analysis["customer_info"] = customer_info
        state_after_analysis["messages"].append(AIMessage(content=f"Customer information: {customer_info}"))
        print(f"👤 Customer info looked up: {customer_info}")
    else:
        state_after_analysis["customer_info"] = "Not needed"
        print("👤 Customer lookup skipped")
    
    state_after_analysis["workflow_status"] = "customer_lookup_done"
    
    print("📋 Updated State:")
    for key, value in state_after_analysis.items():
        if key == "messages":
            print(f"  {key}: [{len(value)} messages]")
            for i, msg in enumerate(value):
                print(f"    {i+1}. {type(msg).__name__}: '{msg.content}'")
        else:
            print(f"  {key}: '{value}'")
    
    # Step 6: Generate Final Response
    print("\n🔵 STEP 6: generate_response Node")
    print("-" * 30)
    print("📝 Processing: Generating final response...")
    
    response_parts = []
    if state_after_analysis["weather_info"] != "Not needed":
        response_parts.append(f"Weather: {state_after_analysis['weather_info']}")
    
    if state_after_analysis["calculation_result"] != "Not needed":
        response_parts.append(f"Calculation: {state_after_analysis['calculation_result']}")
    
    if state_after_analysis["customer_info"] != "Not needed":
        response_parts.append(f"Customer: {state_after_analysis['customer_info']}")
    
    final_response = " | ".join(response_parts)
    state_after_analysis["messages"].append(AIMessage(content=final_response))
    state_after_analysis["workflow_status"] = "completed"
    
    print(f"📝 Final response: {final_response}")
    
    print("📋 Final State:")
    for key, value in state_after_analysis.items():
        if key == "messages":
            print(f"  {key}: [{len(value)} messages]")
            for i, msg in enumerate(value):
                print(f"    {i+1}. {type(msg).__name__}: '{msg.content}'")
        else:
            print(f"  {key}: '{value}'")
    
    # Step 7: Decision Point
    print("\n🔵 STEP 7: should_continue Decision Point")
    print("-" * 30)
    print("🤔 Processing: Should workflow continue or end?")
    
    if state_after_analysis["workflow_status"] == "completed":
        decision = "end"
        print("✅ Decision: END - Workflow completed successfully")
    else:
        decision = "continue"
        print("🔄 Decision: CONTINUE - More processing needed")
    
    print(f"🎯 Routing to: {decision.upper()}")

def demonstrate_different_scenarios():
    """Show how different inputs create different flows"""
    print("\n🔄 Different Scenario Flows")
    print("=" * 40)
    
    scenarios = [
        {
            "name": "Weather Only",
            "message": "What's the weather like in Chicago?",
            "expected_flow": "analyze → weather → calc(skip) → customer(skip) → response → end"
        },
        {
            "name": "Calculation Only",
            "message": "Calculate shipping costs of $25 with 9% tax",
            "expected_flow": "analyze → weather(skip) → calc → customer(skip) → response → end"
        },
        {
            "name": "Customer Only",
            "message": "Look up my customer information",
            "expected_flow": "analyze → weather(skip) → calc(skip) → customer → response → end"
        },
        {
            "name": "Complex Request",
            "message": "I need weather info and want to calculate shipping costs",
            "expected_flow": "analyze → weather → calc → customer(skip) → response → end"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"Message: '{scenario['message']}'")
        print(f"Expected Flow: {scenario['expected_flow']}")
        print("-" * 40)

def demonstrate_state_evolution():
    """Show how state evolves through the workflow"""
    print("\n📊 State Evolution Through Workflow")
    print("=" * 50)
    
    print("\n🔄 State Changes at Each Node:")
    print("-" * 30)
    
    states = [
        {
            "node": "Initial",
            "issue_type": "",
            "weather_info": "",
            "calculation_result": "",
            "customer_info": "",
            "workflow_status": ""
        },
        {
            "node": "analyze_request",
            "issue_type": "complex_inquiry",
            "weather_info": "",
            "calculation_result": "",
            "customer_info": "",
            "workflow_status": "analyzed"
        },
        {
            "node": "check_weather",
            "issue_type": "complex_inquiry",
            "weather_info": "Weather in New York: 22°C, Sunny...",
            "calculation_result": "",
            "customer_info": "",
            "workflow_status": "weather_checked"
        },
        {
            "node": "perform_calculations",
            "issue_type": "complex_inquiry",
            "weather_info": "Weather in New York: 22°C, Sunny...",
            "calculation_result": "Result: 25 * 1.09 = 27.25",
            "customer_info": "",
            "workflow_status": "calculations_done"
        },
        {
            "node": "lookup_customer",
            "issue_type": "complex_inquiry",
            "weather_info": "Weather in New York: 22°C, Sunny...",
            "calculation_result": "Result: 25 * 1.09 = 27.25",
            "customer_info": "Not needed",
            "workflow_status": "customer_lookup_done"
        },
        {
            "node": "generate_response",
            "issue_type": "complex_inquiry",
            "weather_info": "Weather in New York: 22°C, Sunny...",
            "calculation_result": "Result: 25 * 1.09 = 27.25",
            "customer_info": "Not needed",
            "workflow_status": "completed"
        }
    ]
    
    for state in states:
        print(f"\n🔵 {state['node']}:")
        print(f"  issue_type: '{state['issue_type']}'")
        print(f"  weather_info: '{state['weather_info'][:30]}{'...' if len(state['weather_info']) > 30 else ''}'")
        print(f"  calculation_result: '{state['calculation_result'][:30]}{'...' if len(state['calculation_result']) > 30 else ''}'")
        print(f"  customer_info: '{state['customer_info']}'")
        print(f"  workflow_status: '{state['workflow_status']}'")

if __name__ == "__main__":
    # Show workflow structure
    visualize_workflow_flow()
    
    # Demonstrate flow with example
    demonstrate_flow_with_example()
    
    # Show different scenarios
    demonstrate_different_scenarios()
    
    # Show state evolution
    demonstrate_state_evolution()
    
    print("\n🎉 Workflow Flow Visualization Complete!")
    print("\nKey Insights:")
    print("✅ State flows through each node, accumulating information")
    print("✅ Each node can read from and update the state")
    print("✅ Conditional logic determines which nodes execute")
    print("✅ The final state contains all collected information")
    print("✅ Decision points route to different paths based on state") 