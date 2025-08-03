"""
Example 5: LangGraph Basics - Core Concepts

This example explains the core concepts of LangGraph:
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

def demonstrate_langgraph_concepts():
    """Demonstrate the core concepts of LangGraph"""
    print("🔄 LangGraph Basics: Core Concepts")
    print("=" * 60)
    
    print("\n📋 1. StateGraph - The Foundation")
    print("-" * 40)
    print("StateGraph is the main container for workflows in LangGraph.")
    print("It manages the flow of data and execution between nodes.")
    print("Example: workflow = StateGraph(WorkflowState)")
    
    print("\n📋 2. State Management")
    print("-" * 40)
    print("State flows through the entire workflow, carrying information between nodes.")
    print("Each node can read from and update the state.")
    print("Example state structure:")
    print("  - messages: Conversation history")
    print("  - customer_id: Current customer")
    print("  - issue_type: Type of inquiry")
    print("  - workflow_status: Current step")
    
    print("\n📋 3. Nodes - Processing Functions")
    print("-" * 40)
    print("Nodes are individual functions that process the state.")
    print("Each node receives state as input and returns updated state.")
    print("Example nodes:")
    print("  - analyze_customer_request: Determines issue type")
    print("  - check_weather_if_needed: Gets weather information")
    print("  - perform_calculations_if_needed: Does math")
    print("  - lookup_customer_info_if_needed: Gets customer data")
    print("  - generate_final_response: Creates final response")
    
    print("\n📋 4. Edges - Connections Between Nodes")
    print("-" * 40)
    print("Edges define the flow between nodes.")
    print("They can be simple (linear) or conditional (dynamic).")
    print("Example edges:")
    print("  - analyze_request → check_weather")
    print("  - check_weather → perform_calculations")
    print("  - perform_calculations → lookup_customer")
    print("  - lookup_customer → generate_response")
    
    print("\n📋 5. Conditional Edges - Dynamic Routing")
    print("-" * 40)
    print("Conditional edges allow different paths based on state.")
    print("A routing function decides which path to take.")
    print("Example:")
    print("  - If workflow_status == 'completed' → END")
    print("  - Else → continue to next node")
    
    print("\n📋 6. Workflow Structure")
    print("-" * 40)
    print("Our customer service workflow:")
    print("┌─────────────────┐")
    print("│  analyze_request│")
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
    print("│ should_continue │")
    print("└─────────┬───────┘")
    print("          │")
    print("    ┌─────┴─────┐")
    print("    ▼           ▼")
    print("┌─────────┐ ┌─────┐")
    print("│continue │ │ END │")
    print("└─────────┘ └─────┘")

def demonstrate_node_functions():
    """Show examples of node functions"""
    print("\n🔧 Node Function Examples")
    print("=" * 40)
    
    print("\n📝 Example 1: Analyze Customer Request")
    print("-" * 30)
    print("def analyze_customer_request(state: WorkflowState) -> WorkflowState:")
    print("    # Get the latest message")
    print("    latest_message = state['messages'][-1].content")
    print("    ")
    print("    # Determine issue type")
    print("    if 'weather' in latest_message.lower():")
    print("        state['issue_type'] = 'weather_inquiry'")
    print("    elif 'calculate' in latest_message.lower():")
    print("        state['issue_type'] = 'calculation_request'")
    print("    ")
    print("    return state")
    
    print("\n📝 Example 2: Check Weather If Needed")
    print("-" * 30)
    print("def check_weather_if_needed(state: WorkflowState) -> WorkflowState:")
    print("    if state['issue_type'] == 'weather_inquiry':")
    print("        # Get weather information")
    print("        weather_info = get_weather_data()")
    print("        state['weather_info'] = weather_info")
    print("        state['messages'].append(AIMessage(content=weather_info))")
    print("    else:")
    print("        state['weather_info'] = 'Not needed'")
    print("    ")
    print("    return state")

def demonstrate_workflow_creation():
    """Show how to create a workflow"""
    print("\n🏗️  Workflow Creation Example")
    print("=" * 40)
    
    print("\n📝 Step 1: Create StateGraph")
    print("-" * 30)
    print("workflow = StateGraph(WorkflowState)")
    
    print("\n📝 Step 2: Add Nodes")
    print("-" * 30)
    print("workflow.add_node('analyze_request', analyze_customer_request)")
    print("workflow.add_node('check_weather', check_weather_if_needed)")
    print("workflow.add_node('perform_calculations', perform_calculations_if_needed)")
    print("workflow.add_node('lookup_customer', lookup_customer_info_if_needed)")
    print("workflow.add_node('generate_response', generate_final_response)")
    
    print("\n📝 Step 3: Add Edges")
    print("-" * 30)
    print("workflow.add_edge('analyze_request', 'check_weather')")
    print("workflow.add_edge('check_weather', 'perform_calculations')")
    print("workflow.add_edge('perform_calculations', 'lookup_customer')")
    print("workflow.add_edge('lookup_customer', 'generate_response')")
    
    print("\n📝 Step 4: Add Conditional Edges")
    print("-" * 30)
    print("workflow.add_conditional_edges('generate_response', should_continue, {")
    print("    'continue': 'analyze_request',")
    print("    'end': END")
    print("})")
    
    print("\n📝 Step 5: Set Entry Point and Compile")
    print("-" * 30)
    print("workflow.set_entry_point('analyze_request')")
    print("app = workflow.compile(checkpointer=MemorySaver())")

def demonstrate_benefits():
    """Show the benefits of using LangGraph"""
    print("\n🎯 Benefits of LangGraph")
    print("=" * 40)
    
    print("\n✅ 1. Structured Workflows")
    print("   - Clear step-by-step processes")
    print("   - Easy to understand and maintain")
    print("   - Modular design with reusable components")
    
    print("\n✅ 2. State Management")
    print("   - Information persists across nodes")
    print("   - No need to pass data manually")
    print("   - Automatic state updates")
    
    print("\n✅ 3. Conditional Logic")
    print("   - Dynamic routing based on conditions")
    print("   - Different paths for different scenarios")
    print("   - Flexible workflow execution")
    
    print("\n✅ 4. Debugging and Monitoring")
    print("   - Easy to track workflow execution")
    print("   - Clear visibility into each step")
    print("   - State inspection at any point")
    
    print("\n✅ 5. Scalability")
    print("   - Easy to add new nodes")
    print("   - Simple to modify workflow logic")
    print("   - Reusable components across workflows")

def demonstrate_comparison():
    """Compare LangGraph with other approaches"""
    print("\n🔄 Comparison: LangGraph vs Other Approaches")
    print("=" * 50)
    
    print("\n📊 Sequential Chains (Example 2)")
    print("-" * 30)
    print("✅ Simple linear execution")
    print("❌ No conditional logic")
    print("❌ Limited state management")
    print("❌ Hard to debug complex flows")
    
    print("\n📊 Agents with Tools (Example 4)")
    print("-" * 30)
    print("✅ Autonomous decision making")
    print("✅ Tool integration")
    print("❌ Less structured workflow")
    print("❌ Harder to predict execution path")
    
    print("\n📊 LangGraph (Example 5)")
    print("-" * 30)
    print("✅ Structured workflows")
    print("✅ Conditional logic")
    print("✅ State management")
    print("✅ Easy debugging")
    print("✅ Predictable execution")
    print("✅ Modular design")

if __name__ == "__main__":
    # Demonstrate core concepts
    demonstrate_langgraph_concepts()
    
    # Show node function examples
    demonstrate_node_functions()
    
    # Show workflow creation
    demonstrate_workflow_creation()
    
    # Show benefits
    demonstrate_benefits()
    
    # Show comparison
    demonstrate_comparison()
    
    print("\n🎉 LangGraph Basics Concepts Explained!")
    print("\nNext Steps:")
    print("📚 Learn more about LangGraph: https://langchain-ai.github.io/langgraph/")
    print("🔧 Try building your own workflows")
    print("🚀 Explore advanced features like parallel execution")
    print("💡 Consider real-world applications") 