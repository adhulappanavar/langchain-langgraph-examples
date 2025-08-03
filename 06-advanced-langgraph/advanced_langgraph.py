"""
Example 6: Advanced LangGraph

This example demonstrates advanced LangGraph concepts including:
- Parallel execution of multiple nodes
- Advanced state management and conditional logic
- Error handling and recovery mechanisms
- Multi-agent coordination
- Dynamic routing based on runtime conditions
"""

import os
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, TypedDict, Annotated, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolExecutor
from langchain.tools import BaseTool

# Load environment variables
load_dotenv()

# Define the advanced state structure
class AdvancedWorkflowState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]
    customer_id: str
    request_type: str
    priority: str
    complexity: str
    parallel_results: Dict[str, Any]
    error_log: List[str]
    retry_count: int
    workflow_status: str
    agent_coordination: Dict[str, Any]
    dynamic_routing: Dict[str, Any]

# Advanced tools for parallel execution
class WeatherTool(BaseTool):
    name: str = "weather"
    description: str = "Get current weather information for a specific location"
    
    def _run(self, location: str) -> str:
        try:
            # Simulate API call with potential delay
            time.sleep(0.5)
            weather_data = {
                "location": location,
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%",
                "wind": "10 km/h"
            }
            return json.dumps(weather_data)
        except Exception as e:
            return f"Error getting weather for {location}: {str(e)}"
    
    def _arun(self, location: str):
        raise NotImplementedError("Async not implemented")

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Perform mathematical calculations"
    
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
    name: str = "customer_database"
    description: str = "Look up customer information and order history"
    
    def _run(self, customer_id: str) -> str:
        try:
            # Simulate database lookup with potential delay
            time.sleep(0.3)
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
            return json.dumps(customer_data)
        except Exception as e:
            return f"Error looking up customer {customer_id}: {str(e)}"
    
    def _arun(self, customer_id: str):
        raise NotImplementedError("Async not implemented")

class ShippingCalculatorTool(BaseTool):
    name: str = "shipping_calculator"
    description: str = "Calculate shipping costs and delivery times"
    
    def _run(self, location: str, weight: str) -> str:
        try:
            # Simulate shipping calculation
            time.sleep(0.4)
            shipping_data = {
                "location": location,
                "weight": weight,
                "standard_shipping": "$15.00",
                "express_shipping": "$25.00",
                "delivery_time_standard": "3-5 business days",
                "delivery_time_express": "1-2 business days"
            }
            return json.dumps(shipping_data)
        except Exception as e:
            return f"Error calculating shipping for {location}: {str(e)}"
    
    def _arun(self, location: str, weight: str):
        raise NotImplementedError("Async not implemented")

# Advanced node functions with error handling
def analyze_complex_request(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Analyze the request and determine complexity and routing"""
    print("🔍 Analyzing complex request...")
    
    try:
        messages = state["messages"]
        if not messages:
            state["error_log"].append("No messages found in state")
            return state
        
        latest_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        
        # Advanced analysis logic
        if "weather" in latest_message.lower() and "calculate" in latest_message.lower():
            state["request_type"] = "complex_multi_service"
            state["priority"] = "high"
            state["complexity"] = "high"
        elif "weather" in latest_message.lower():
            state["request_type"] = "weather_inquiry"
            state["priority"] = "medium"
            state["complexity"] = "low"
        elif "calculate" in latest_message.lower() or "shipping" in latest_message.lower():
            state["request_type"] = "calculation_request"
            state["priority"] = "high"
            state["complexity"] = "medium"
        elif "customer" in latest_message.lower():
            state["request_type"] = "customer_inquiry"
            state["priority"] = "high"
            state["complexity"] = "low"
        else:
            state["request_type"] = "general_inquiry"
            state["priority"] = "low"
            state["complexity"] = "low"
        
        state["workflow_status"] = "analyzed"
        state["parallel_results"] = {}
        state["error_log"] = []
        state["retry_count"] = 0
        state["agent_coordination"] = {}
        state["dynamic_routing"] = {}
        
        print(f"📊 Analysis: Type={state['request_type']}, Priority={state['priority']}, Complexity={state['complexity']}")
        
    except Exception as e:
        state["error_log"].append(f"Error in analysis: {str(e)}")
        print(f"❌ Analysis error: {e}")
    
    return state

def execute_parallel_tasks(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Execute multiple tasks in parallel based on request type"""
    print("⚡ Executing parallel tasks...")
    
    try:
        request_type = state.get("request_type", "")
        parallel_results = {}
        
        # Determine which tasks to run in parallel
        tasks_to_run = []
        
        if "weather" in request_type or "complex" in request_type:
            tasks_to_run.append(("weather", "New York"))
        
        if "calculate" in request_type or "complex" in request_type:
            tasks_to_run.append(("calculator", "150 * 1.085"))
        
        if "customer" in request_type:
            tasks_to_run.append(("customer_database", "CUST123"))
        
        if "shipping" in request_type or "complex" in request_type:
            tasks_to_run.append(("shipping_calculator", "New York, 5kg"))
        
        # Execute tasks in parallel (simulated)
        for task_name, task_input in tasks_to_run:
            try:
                if task_name == "weather":
                    tool = WeatherTool()
                    result = tool._run(task_input)
                elif task_name == "calculator":
                    tool = CalculatorTool()
                    result = tool._run(task_input)
                elif task_name == "customer_database":
                    tool = CustomerDatabaseTool()
                    result = tool._run(task_input)
                elif task_name == "shipping_calculator":
                    tool = ShippingCalculatorTool()
                    result = tool._run(task_input)
                else:
                    result = f"Unknown task: {task_name}"
                
                parallel_results[task_name] = result
                print(f"✅ {task_name}: {result[:50]}...")
                
            except Exception as e:
                error_msg = f"Error in {task_name}: {str(e)}"
                parallel_results[task_name] = error_msg
                state["error_log"].append(error_msg)
                print(f"❌ {error_msg}")
        
        state["parallel_results"] = parallel_results
        state["workflow_status"] = "parallel_completed"
        
    except Exception as e:
        state["error_log"].append(f"Error in parallel execution: {str(e)}")
        print(f"❌ Parallel execution error: {e}")
    
    return state

def coordinate_agents(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Coordinate multiple agents based on parallel results"""
    print("🤝 Coordinating agents...")
    
    try:
        parallel_results = state.get("parallel_results", {})
        coordination_data = {}
        
        # Analyze results and coordinate agents
        if "weather" in parallel_results:
            weather_data = parallel_results["weather"]
            if "Error" not in weather_data:
                coordination_data["weather_agent"] = {
                    "status": "success",
                    "data": weather_data,
                    "recommendations": ["Weather conditions are favorable for delivery"]
                }
            else:
                coordination_data["weather_agent"] = {
                    "status": "error",
                    "error": weather_data
                }
        
        if "calculator" in parallel_results:
            calc_data = parallel_results["calculator"]
            if "Error" not in calc_data:
                coordination_data["calculation_agent"] = {
                    "status": "success",
                    "data": calc_data,
                    "recommendations": ["Cost calculation completed successfully"]
                }
            else:
                coordination_data["calculation_agent"] = {
                    "status": "error",
                    "error": calc_data
                }
        
        if "customer_database" in parallel_results:
            customer_data = parallel_results["customer_database"]
            if "Error" not in customer_data:
                coordination_data["customer_agent"] = {
                    "status": "success",
                    "data": customer_data,
                    "recommendations": ["Customer information retrieved"]
                }
            else:
                coordination_data["customer_agent"] = {
                    "status": "error",
                    "error": customer_data
                }
        
        if "shipping_calculator" in parallel_results:
            shipping_data = parallel_results["shipping_calculator"]
            if "Error" not in shipping_data:
                coordination_data["shipping_agent"] = {
                    "status": "success",
                    "data": shipping_data,
                    "recommendations": ["Shipping options calculated"]
                }
            else:
                coordination_data["shipping_agent"] = {
                    "status": "error",
                    "error": shipping_data
                }
        
        state["agent_coordination"] = coordination_data
        state["workflow_status"] = "agents_coordinated"
        
        print(f"🤝 Coordinated {len(coordination_data)} agents")
        
    except Exception as e:
        state["error_log"].append(f"Error in agent coordination: {str(e)}")
        print(f"❌ Agent coordination error: {e}")
    
    return state

def determine_dynamic_routing(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Determine routing based on current state and results"""
    print("🎯 Determining dynamic routing...")
    
    try:
        coordination_data = state.get("agent_coordination", {})
        error_log = state.get("error_log", [])
        routing_decision = {}
        
        # Analyze coordination results and determine next steps
        successful_agents = [name for name, data in coordination_data.items() if data.get("status") == "success"]
        failed_agents = [name for name, data in coordination_data.items() if data.get("status") == "error"]
        
        if len(failed_agents) > 0:
            routing_decision["action"] = "retry_failed_agents"
            routing_decision["failed_agents"] = failed_agents
            routing_decision["retry_count"] = state.get("retry_count", 0) + 1
        elif len(successful_agents) > 0:
            routing_decision["action"] = "generate_comprehensive_response"
            routing_decision["successful_agents"] = successful_agents
        else:
            routing_decision["action"] = "fallback_response"
            routing_decision["reason"] = "No agents succeeded"
        
        # Add routing logic based on request type
        request_type = state.get("request_type", "")
        if "complex" in request_type:
            routing_decision["complexity"] = "high"
            routing_decision["requires_specialized_response"] = True
        else:
            routing_decision["complexity"] = "low"
            routing_decision["requires_specialized_response"] = False
        
        state["dynamic_routing"] = routing_decision
        state["workflow_status"] = "routing_determined"
        
        print(f"🎯 Routing decision: {routing_decision['action']}")
        
    except Exception as e:
        state["error_log"].append(f"Error in dynamic routing: {str(e)}")
        print(f"❌ Dynamic routing error: {e}")
    
    return state

def handle_retry_failed_agents(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Retry failed agents with exponential backoff"""
    print("🔄 Retrying failed agents...")
    
    try:
        routing_data = state.get("dynamic_routing", {})
        failed_agents = routing_data.get("failed_agents", [])
        retry_count = routing_data.get("retry_count", 1)
        
        if retry_count > 3:
            state["error_log"].append("Maximum retry attempts exceeded")
            state["workflow_status"] = "max_retries_exceeded"
            return state
        
        # Simulate retry with exponential backoff
        backoff_time = 2 ** retry_count
        print(f"⏳ Waiting {backoff_time} seconds before retry...")
        time.sleep(min(backoff_time, 5))  # Cap at 5 seconds
        
        # Retry failed agents
        for agent_name in failed_agents:
            try:
                if agent_name == "weather_agent":
                    tool = WeatherTool()
                    result = tool._run("New York")
                elif agent_name == "calculation_agent":
                    tool = CalculatorTool()
                    result = tool._run("150 * 1.085")
                elif agent_name == "customer_agent":
                    tool = CustomerDatabaseTool()
                    result = tool._run("CUST123")
                elif agent_name == "shipping_agent":
                    tool = ShippingCalculatorTool()
                    result = tool._run("New York, 5kg")
                
                # Update coordination data
                coordination_data = state.get("agent_coordination", {})
                if agent_name in coordination_data:
                    coordination_data[agent_name] = {
                        "status": "success",
                        "data": result,
                        "retry_count": retry_count
                    }
                
                print(f"✅ Retry successful for {agent_name}")
                
            except Exception as e:
                error_msg = f"Retry failed for {agent_name}: {str(e)}"
                state["error_log"].append(error_msg)
                print(f"❌ {error_msg}")
        
        state["retry_count"] = retry_count
        state["workflow_status"] = "retry_completed"
        
    except Exception as e:
        state["error_log"].append(f"Error in retry handling: {str(e)}")
        print(f"❌ Retry handling error: {e}")
    
    return state

def generate_comprehensive_response(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Generate a comprehensive response based on all agent results"""
    print("📝 Generating comprehensive response...")
    
    try:
        coordination_data = state.get("agent_coordination", {})
        routing_data = state.get("dynamic_routing", {})
        
        response_parts = []
        
        # Build response from successful agents
        for agent_name, agent_data in coordination_data.items():
            if agent_data.get("status") == "success":
                if agent_name == "weather_agent":
                    weather_info = agent_data.get("data", "")
                    response_parts.append(f"Weather Information: {weather_info}")
                elif agent_name == "calculation_agent":
                    calc_info = agent_data.get("data", "")
                    response_parts.append(f"Calculation Results: {calc_info}")
                elif agent_name == "customer_agent":
                    customer_info = agent_data.get("data", "")
                    response_parts.append(f"Customer Information: {customer_info}")
                elif agent_name == "shipping_agent":
                    shipping_info = agent_data.get("data", "")
                    response_parts.append(f"Shipping Options: {shipping_info}")
        
        # Add recommendations
        recommendations = []
        for agent_data in coordination_data.values():
            if agent_data.get("status") == "success":
                agent_recs = agent_data.get("recommendations", [])
                recommendations.extend(agent_recs)
        
        if recommendations:
            response_parts.append(f"Recommendations: {'; '.join(recommendations)}")
        
        # Add error information if any
        error_log = state.get("error_log", [])
        if error_log:
            response_parts.append(f"Note: Some services encountered issues: {'; '.join(error_log[:3])}")
        
        final_response = " | ".join(response_parts)
        state["messages"].append(AIMessage(content=final_response))
        state["workflow_status"] = "completed"
        
        print(f"📝 Generated comprehensive response with {len(response_parts)} sections")
        
    except Exception as e:
        state["error_log"].append(f"Error in response generation: {str(e)}")
        print(f"❌ Response generation error: {e}")
    
    return state

def generate_fallback_response(state: AdvancedWorkflowState) -> AdvancedWorkflowState:
    """Generate a fallback response when all agents fail"""
    print("🛡️ Generating fallback response...")
    
    try:
        error_log = state.get("error_log", [])
        request_type = state.get("request_type", "general_inquiry")
        
        fallback_response = f"I apologize, but I'm currently unable to process your {request_type} request. "
        fallback_response += "Please try again later or contact our support team for assistance. "
        
        if error_log:
            fallback_response += f"Technical details: {'; '.join(error_log[:2])}"
        
        state["messages"].append(AIMessage(content=fallback_response))
        state["workflow_status"] = "completed_with_fallback"
        
        print("🛡️ Generated fallback response")
        
    except Exception as e:
        state["error_log"].append(f"Error in fallback response: {str(e)}")
        print(f"❌ Fallback response error: {e}")
    
    return state

def should_continue(state: AdvancedWorkflowState) -> str:
    """Determine if the workflow should continue or end"""
    workflow_status = state.get("workflow_status", "")
    
    if workflow_status == "completed":
        return "end"
    elif workflow_status == "completed_with_fallback":
        return "end"
    elif workflow_status == "max_retries_exceeded":
        return "fallback"
    elif workflow_status == "retry_completed":
        return "coordinate"
    elif workflow_status == "routing_determined":
        routing_data = state.get("dynamic_routing", {})
        action = routing_data.get("action", "")
        
        if action == "retry_failed_agents":
            return "retry"
        elif action == "generate_comprehensive_response":
            return "comprehensive"
        elif action == "fallback_response":
            return "fallback"
        else:
            return "end"
    else:
        return "continue"

def create_advanced_workflow():
    """Create the advanced workflow with parallel execution and error handling"""
    
    # Create the state graph
    workflow = StateGraph(AdvancedWorkflowState)
    
    # Add nodes
    workflow.add_node("analyze_request", analyze_complex_request)
    workflow.add_node("parallel_execution", execute_parallel_tasks)
    workflow.add_node("coordinate_agents", coordinate_agents)
    workflow.add_node("determine_routing", determine_dynamic_routing)
    workflow.add_node("retry_failed", handle_retry_failed_agents)
    workflow.add_node("comprehensive_response", generate_comprehensive_response)
    workflow.add_node("fallback_response", generate_fallback_response)
    
    # Add edges
    workflow.add_edge("analyze_request", "parallel_execution")
    workflow.add_edge("parallel_execution", "coordinate_agents")
    workflow.add_edge("coordinate_agents", "determine_routing")
    
    # Add conditional edges for dynamic routing
    workflow.add_conditional_edges("determine_routing", should_continue, {
        "retry": "retry_failed",
        "comprehensive": "comprehensive_response",
        "fallback": "fallback_response",
        "coordinate": "coordinate_agents",
        "end": END
    })
    
    workflow.add_conditional_edges("retry_failed", should_continue, {
        "coordinate": "coordinate_agents",
        "fallback": "fallback_response",
        "end": END
    })
    
    workflow.add_conditional_edges("comprehensive_response", should_continue, {
        "end": END
    })
    
    workflow.add_conditional_edges("fallback_response", should_continue, {
        "end": END
    })
    
    # Set entry point
    workflow.set_entry_point("analyze_request")
    
    # Compile the workflow
    app = workflow.compile(checkpointer=MemorySaver())
    
    return app

def run_advanced_workflow_examples():
    """Run examples of the advanced workflow"""
    print("🚀 Advanced LangGraph: Complex Workflow with Parallel Execution")
    print("=" * 70)
    
    # Create the workflow
    app = create_advanced_workflow()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Complex Multi-Service Request",
            "message": "I need weather information for New York, calculate shipping costs for a 5kg package, and look up my customer information. Also calculate the total cost with tax.",
            "customer_id": "CUST456"
        },
        {
            "name": "Weather + Calculation Request",
            "message": "What's the weather like in Chicago and can you calculate shipping costs for a 3kg package?",
            "customer_id": "CUST789"
        },
        {
            "name": "Customer Information Request",
            "message": "Can you look up my customer information and order history?",
            "customer_id": "CUST123"
        },
        {
            "name": "Simple Weather Request",
            "message": "What's the weather like in Miami?",
            "customer_id": "CUST001"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"Message: {scenario['message']}")
        print("-" * 60)
        
        try:
            # Initialize state
            initial_state = {
                "messages": [HumanMessage(content=scenario['message'])],
                "customer_id": scenario['customer_id'],
                "request_type": "",
                "priority": "",
                "complexity": "",
                "parallel_results": {},
                "error_log": [],
                "retry_count": 0,
                "workflow_status": "",
                "agent_coordination": {},
                "dynamic_routing": {}
            }
            
            # Run the workflow
            result = app.invoke(initial_state)
            
            print(f"\n✅ Workflow completed!")
            print(f"Final Status: {result['workflow_status']}")
            print(f"Agents Coordinated: {len(result['agent_coordination'])}")
            print(f"Errors: {len(result['error_log'])}")
            print(f"Final Response: {result['messages'][-1].content[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_parallel_execution():
    """Demonstrate parallel execution capabilities"""
    print("\n⚡ Parallel Execution Demo")
    print("=" * 40)
    
    print("🔄 Parallel execution allows multiple tasks to run simultaneously:")
    print("  - Weather API calls")
    print("  - Database lookups")
    print("  - Calculation operations")
    print("  - Shipping calculations")
    
    print("\n📊 Benefits:")
    print("  ✅ Faster execution time")
    print("  ✅ Better resource utilization")
    print("  ✅ Improved user experience")
    print("  ✅ Scalable architecture")

def demonstrate_error_handling():
    """Demonstrate error handling and recovery"""
    print("\n🛡️ Error Handling Demo")
    print("=" * 40)
    
    print("🔄 Error handling mechanisms:")
    print("  - Automatic retry with exponential backoff")
    print("  - Graceful degradation")
    print("  - Fallback responses")
    print("  - Error logging and monitoring")
    
    print("\n📊 Recovery strategies:")
    print("  ✅ Retry failed operations")
    print("  ✅ Provide partial results")
    print("  ✅ Generate fallback responses")
    print("  ✅ Log errors for debugging")

def demonstrate_agent_coordination():
    """Demonstrate multi-agent coordination"""
    print("\n🤝 Agent Coordination Demo")
    print("=" * 40)
    
    print("🔄 Multi-agent coordination:")
    print("  - Weather Agent: Provides weather information")
    print("  - Calculation Agent: Performs mathematical operations")
    print("  - Customer Agent: Retrieves customer data")
    print("  - Shipping Agent: Calculates shipping options")
    
    print("\n📊 Coordination benefits:")
    print("  ✅ Specialized agents for specific tasks")
    print("  ✅ Parallel processing capabilities")
    print("  ✅ Better error isolation")
    print("  ✅ Scalable architecture")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Run advanced workflow examples
    run_advanced_workflow_examples()
    
    # Demonstrate advanced features
    demonstrate_parallel_execution()
    demonstrate_error_handling()
    demonstrate_agent_coordination()
    
    print("\n🎉 Advanced LangGraph demonstration completed!")
    print("\nKey Advanced Features Demonstrated:")
    print("✅ Parallel Execution: Multiple tasks running simultaneously")
    print("✅ Error Handling: Robust retry and recovery mechanisms")
    print("✅ Agent Coordination: Multiple specialized agents working together")
    print("✅ Dynamic Routing: Runtime path determination based on state")
    print("✅ Advanced State Management: Complex state tracking and persistence") 