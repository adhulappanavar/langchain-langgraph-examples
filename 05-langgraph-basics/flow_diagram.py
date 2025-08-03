"""
LangGraph Workflow Flow Diagram

This creates a visual representation of how data flows through a LangGraph workflow,
showing state changes and decision points.
"""

def print_flow_diagram():
    """Print a visual flow diagram of the LangGraph workflow"""
    print("🔄 LangGraph Workflow Flow Diagram")
    print("=" * 60)
    
    print("\n📊 Data Flow Visualization")
    print("=" * 40)
    
    print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CUSTOMER SERVICE WORKFLOW                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUT STATE                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ messages: [HumanMessage: "I need weather and calculate shipping"] │   │
│  │ customer_id: "CUST456"                                            │   │
│  │ issue_type: ""                                                    │   │
│  │ priority: ""                                                      │   │
│  │ weather_info: ""                                                  │   │
│  │ calculation_result: ""                                            │   │
│  │ customer_info: ""                                                 │   │
│  │ workflow_status: ""                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           analyze_request NODE                             │
│  🔍 Processing: Analyzing customer request...                            │
│  📊 Result: issue_type="complex_inquiry", priority="high"               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ messages: [HumanMessage: "I need weather and calculate shipping"] │   │
│  │ customer_id: "CUST456"                                            │   │
│  │ issue_type: "complex_inquiry"                                     │   │
│  │ priority: "high"                                                  │   │
│  │ weather_info: ""                                                  │   │
│  │ calculation_result: ""                                            │   │
│  │ customer_info: ""                                                 │   │
│  │ workflow_status: "analyzed"                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           check_weather NODE                              │
│  🌤️  Processing: Checking weather if needed...                          │
│  📊 Result: weather_info="Weather in NY: 22°C, Sunny..."               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ messages: [2 messages]                                            │   │
│  │   - HumanMessage: "I need weather and calculate shipping"         │   │
│  │   - AIMessage: "Weather information: Weather in NY: 22°C..."      │   │
│  │ customer_id: "CUST456"                                            │   │
│  │ issue_type: "complex_inquiry"                                     │   │
│  │ priority: "high"                                                  │   │
│  │ weather_info: "Weather in NY: 22°C, Sunny, Humidity: 65%..."     │   │
│  │ calculation_result: ""                                            │   │
│  │ customer_info: ""                                                 │   │
│  │ workflow_status: "weather_checked"                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       perform_calculations NODE                           │
│  🧮 Processing: Performing calculations if needed...                     │
│  📊 Result: calculation_result="Result: 25 * 1.09 = 27.25"             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ messages: [3 messages]                                            │   │
│  │   - HumanMessage: "I need weather and calculate shipping"         │   │
│  │   - AIMessage: "Weather information: Weather in NY: 22°C..."      │   │
│  │   - AIMessage: "Calculation result: Result: 25 * 1.09 = 27.25"   │   │
│  │ customer_id: "CUST456"                                            │   │
│  │ issue_type: "complex_inquiry"                                     │   │
│  │ priority: "high"                                                  │   │
│  │ weather_info: "Weather in NY: 22°C, Sunny, Humidity: 65%..."     │   │
│  │ calculation_result: "Result: 25 * 1.09 = 27.25"                   │   │
│  │ customer_info: ""                                                 │   │
│  │ workflow_status: "calculations_done"                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         lookup_customer NODE                              │
│  👤 Processing: Looking up customer info if needed...                   │
│  📊 Result: customer_info="Not needed" (skipped)                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ messages: [3 messages]                                            │   │
│  │   - HumanMessage: "I need weather and calculate shipping"         │   │
│  │   - AIMessage: "Weather information: Weather in NY: 22°C..."      │   │
│  │   - AIMessage: "Calculation result: Result: 25 * 1.09 = 27.25"   │   │
│  │ customer_id: "CUST456"                                            │   │
│  │ issue_type: "complex_inquiry"                                     │   │
│  │ priority: "high"                                                  │   │
│  │ weather_info: "Weather in NY: 22°C, Sunny, Humidity: 65%..."     │   │
│  │ calculation_result: "Result: 25 * 1.09 = 27.25"                   │   │
│  │ customer_info: "Not needed"                                       │   │
│  │ workflow_status: "customer_lookup_done"                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        generate_response NODE                             │
│  📝 Processing: Generating final response...                             │
│  📊 Result: Final comprehensive response                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ messages: [4 messages]                                            │   │
│  │   - HumanMessage: "I need weather and calculate shipping"         │   │
│  │   - AIMessage: "Weather information: Weather in NY: 22°C..."      │   │
│  │   - AIMessage: "Calculation result: Result: 25 * 1.09 = 27.25"   │   │
│  │   - AIMessage: "Weather: Weather in NY: 22°C... | Calculation..." │   │
│  │ customer_id: "CUST456"                                            │   │
│  │ issue_type: "complex_inquiry"                                     │   │
│  │ priority: "high"                                                  │   │
│  │ weather_info: "Weather in NY: 22°C, Sunny, Humidity: 65%..."     │   │
│  │ calculation_result: "Result: 25 * 1.09 = 27.25"                   │   │
│  │ customer_info: "Not needed"                                       │   │
│  │ workflow_status: "completed"                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        should_continue DECISION                           │
│  🤔 Processing: Should workflow continue or end?                        │
│  📊 Decision: END (workflow_status == "completed")                     │
│  🎯 Routing: END                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT STATE                                 │
│  ✅ Workflow completed successfully!                                     │
│  📋 Final Response: "Weather: Weather in NY: 22°C... | Calculation..."  │
└─────────────────────────────────────────────────────────────────────────────┘
""")

def print_conditional_flow_examples():
    """Show examples of different conditional flows"""
    print("\n🔄 Conditional Flow Examples")
    print("=" * 40)
    
    print("\n📋 Example 1: Weather Only Request")
    print("-" * 30)
    print("Input: 'What's the weather like in Chicago?'")
    print("Flow: analyze → weather → calc(skip) → customer(skip) → response → end")
    print("State Evolution:")
    print("  Initial: issue_type=''")
    print("  analyze: issue_type='weather_inquiry'")
    print("  weather: weather_info='Weather in Chicago: 18°C, Cloudy...'")
    print("  calc: calculation_result='Not needed' (skipped)")
    print("  customer: customer_info='Not needed' (skipped)")
    print("  response: Final response with weather only")
    
    print("\n📋 Example 2: Calculation Only Request")
    print("-" * 30)
    print("Input: 'Calculate shipping costs of $25 with 9% tax'")
    print("Flow: analyze → weather(skip) → calc → customer(skip) → response → end")
    print("State Evolution:")
    print("  Initial: issue_type=''")
    print("  analyze: issue_type='calculation_request'")
    print("  weather: weather_info='Not needed' (skipped)")
    print("  calc: calculation_result='Result: 25 * 1.09 = 27.25'")
    print("  customer: customer_info='Not needed' (skipped)")
    print("  response: Final response with calculation only")
    
    print("\n📋 Example 3: Complex Request")
    print("-" * 30)
    print("Input: 'I need weather info and want to calculate shipping costs'")
    print("Flow: analyze → weather → calc → customer(skip) → response → end")
    print("State Evolution:")
    print("  Initial: issue_type=''")
    print("  analyze: issue_type='complex_inquiry'")
    print("  weather: weather_info='Weather in NY: 22°C, Sunny...'")
    print("  calc: calculation_result='Result: 25 * 1.09 = 27.25'")
    print("  customer: customer_info='Not needed' (skipped)")
    print("  response: Final response with weather + calculation")

def print_key_insights():
    """Print key insights about the flow"""
    print("\n🎯 Key Insights About LangGraph Flow")
    print("=" * 50)
    
    print("\n✅ 1. State Persistence")
    print("   - State flows through all nodes")
    print("   - Each node can read and update state")
    print("   - Information accumulates across nodes")
    
    print("\n✅ 2. Conditional Execution")
    print("   - Nodes can skip execution based on state")
    print("   - Different paths for different scenarios")
    print("   - Dynamic workflow routing")
    
    print("\n✅ 3. Message Accumulation")
    print("   - Messages grow as workflow progresses")
    print("   - Each node can add new messages")
    print("   - Final response combines all information")
    
    print("\n✅ 4. Decision Points")
    print("   - Conditional edges enable dynamic routing")
    print("   - Workflow can loop or end based on state")
    print("   - Complex logic in simple routing functions")
    
    print("\n✅ 5. Modular Design")
    print("   - Each node has a single responsibility")
    print("   - Easy to add/remove/modify nodes")
    print("   - Reusable components across workflows")

if __name__ == "__main__":
    # Print the main flow diagram
    print_flow_diagram()
    
    # Show conditional flow examples
    print_conditional_flow_examples()
    
    # Show key insights
    print_key_insights()
    
    print("\n🎉 Flow Diagram Complete!")
    print("\nThis visualization shows how:")
    print("📊 State evolves through each node")
    print("🔄 Information accumulates across steps")
    print("🎯 Decisions are made based on state")
    print("📝 Messages grow with each interaction")
    print("✅ Final output combines all collected data") 