"""
Example 4: Tools and Agents

This example demonstrates how to create agents that can use external tools and APIs.
We'll build upon the customer service example and add tools for weather, calculations,
and web search, creating an autonomous system that can make decisions about which tools to use.
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from typing import Optional, Type
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Custom tool for weather information
class WeatherTool(BaseTool):
    name: str = "weather"
    description: str = "Get current weather information for a specific location"
    
    def _run(self, location: str) -> str:
        """Get weather information for a location"""
        try:
            # Simulate weather API call (in real implementation, you'd use a real weather API)
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

# Custom tool for calculations
class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Perform mathematical calculations"
    
    def _run(self, expression: str) -> str:
        """Evaluate a mathematical expression"""
        try:
            # Simple calculator (in production, use a safer evaluation method)
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression)
            return f"Result: {expression} = {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
    
    def _arun(self, expression: str):
        raise NotImplementedError("Async not implemented")

# Custom tool for web search
class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search for information on the web"
    
    def _run(self, query: str) -> str:
        """Search for information"""
        try:
            # Simulate web search (in real implementation, you'd use a search API)
            search_results = {
                "query": query,
                "results": [
                    f"Information about {query} - This is a simulated search result.",
                    f"More details about {query} - Another simulated result.",
                    f"Latest news about {query} - Simulated news result."
                ]
            }
            return f"Search results for '{query}':\n" + "\n".join(search_results["results"])
        except Exception as e:
            return f"Error searching for {query}: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("Async not implemented")

# Custom tool for customer service database lookup
class CustomerDatabaseTool(BaseTool):
    name: str = "customer_database"
    description: str = "Look up customer information and order history"
    
    def _run(self, customer_id: str) -> str:
        """Look up customer information"""
        try:
            # Simulate customer database (in real implementation, you'd connect to a real database)
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

def create_customer_service_agent():
    """Create a customer service agent with tools"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # Create memory for conversation history
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create tools
    tools = [
        WeatherTool(),
        CalculatorTool(),
        SearchTool(),
        CustomerDatabaseTool()
    ]
    
    # Create the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent

def run_agent_examples():
    """Run examples of the agent using different tools"""
    print("🤖 Tools and Agents Example: Customer Service Agent")
    print("=" * 60)
    
    # Create the agent
    agent = create_customer_service_agent()
    
    # Test scenarios
    scenarios = [
        # Weather-related customer inquiry
        "A customer is asking about delivery delays due to weather in New York. Can you check the weather?",
        
        # Calculation request
        "A customer wants to know the total cost including tax for an order of $150.00 with 8.5% tax rate. Can you calculate this?",
        
        # Search for information
        "A customer is asking about our return policy. Can you search for information about our return policy?",
        
        # Customer database lookup
        "A customer with ID CUST123 is calling about their recent order. Can you look up their information?",
        
        # Complex scenario combining multiple tools
        "A customer in Los Angeles is asking about delivery times and wants to know the weather there. They also want to calculate shipping costs of $25 plus 9% tax."
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario}")
        print("-" * 50)
        
        try:
            # Run the agent
            response = agent.invoke({"input": scenario})
            print(f"🤖 Agent Response: {response['output']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_tool_usage():
    """Demonstrate individual tool usage"""
    print("\n🔧 Tool Usage Demo")
    print("=" * 40)
    
    # Test individual tools
    tools = {
        "weather": WeatherTool(),
        "calculator": CalculatorTool(),
        "search": SearchTool(),
        "customer_database": CustomerDatabaseTool()
    }
    
    test_cases = [
        ("weather", "New York"),
        ("calculator", "150 * 1.085"),
        ("search", "return policy"),
        ("customer_database", "CUST123")
    ]
    
    for tool_name, input_data in test_cases:
        print(f"\n🔧 Testing {tool_name} tool:")
        print(f"Input: {input_data}")
        
        try:
            result = tools[tool_name]._run(input_data)
            print(f"Output: {result}")
        except Exception as e:
            print(f"Error: {e}")

def interactive_agent_conversation():
    """Run an interactive conversation with the agent"""
    print("\n🎮 Interactive Agent Conversation")
    print("=" * 50)
    print("Start a conversation with the customer service agent.")
    print("The agent can use tools to help answer your questions.")
    print("Available tools: weather, calculator, search, customer_database")
    print("Type 'quit' to end the conversation.")
    print("-" * 50)
    
    # Create the agent
    agent = create_customer_service_agent()
    
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
            response = agent.invoke({"input": message})
            print(f"\n🤖 Agent: {response['output']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_agent_reasoning():
    """Demonstrate how agents reason about tool selection"""
    print("\n🧠 Agent Reasoning Demo")
    print("=" * 40)
    
    # Create the agent
    agent = create_customer_service_agent()
    
    # Complex scenarios that require multiple tools
    complex_scenarios = [
        "A customer in Chicago wants to know if their delivery will be delayed due to weather, and they want to calculate the total cost of their $200 order with 7% tax.",
        
        "A customer is asking about our shipping policy and wants to know the weather in Seattle. They also need to calculate shipping costs of $15 plus 8.25% tax.",
        
        "A customer with ID CUST456 is calling about their order. They want to know the weather in their area (Miami) and need help calculating a refund amount of $75 minus 10% restocking fee."
    ]
    
    for i, scenario in enumerate(complex_scenarios, 1):
        print(f"\n🧠 Complex Scenario {i}:")
        print(f"Input: {scenario}")
        print("-" * 40)
        
        try:
            response = agent.invoke({"input": scenario})
            print(f"🤖 Agent Response: {response['output']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def create_specialized_agent(agent_type: str):
    """Create specialized agents for different use cases"""
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    if agent_type == "sales":
        # Sales agent with pricing and product tools
        tools = [
            CalculatorTool(),
            SearchTool(),
            Tool(
                name="product_catalog",
                func=lambda x: f"Product information: {x} - Price: $99.99, In stock: Yes",
                description="Look up product information and pricing"
            )
        ]
    elif agent_type == "support":
        # Support agent with technical tools
        tools = [
            SearchTool(),
            CustomerDatabaseTool(),
            Tool(
                name="system_status",
                func=lambda x: f"System status for {x}: All systems operational",
                description="Check system status and technical issues"
            )
        ]
    else:
        # General customer service agent
        tools = [WeatherTool(), CalculatorTool(), SearchTool(), CustomerDatabaseTool()]
    
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

def demonstrate_specialized_agents():
    """Demonstrate different types of specialized agents"""
    print("\n🎯 Specialized Agents Demo")
    print("=" * 40)
    
    agent_types = {
        "sales": "Sales Agent - Focuses on products and pricing",
        "support": "Support Agent - Focuses on technical issues",
        "general": "General Agent - Handles all types of inquiries"
    }
    
    test_questions = {
        "sales": "What's the price of our premium product and can you calculate the total with tax?",
        "support": "A customer is having technical issues. Can you check system status?",
        "general": "What's the weather like in Boston and can you calculate shipping costs?"
    }
    
    for agent_type, description in agent_types.items():
        print(f"\n🎯 {description}")
        print("-" * 30)
        
        agent = create_specialized_agent(agent_type)
        question = test_questions[agent_type]
        
        print(f"Question: {question}")
        
        try:
            response = agent.invoke({"input": question})
            print(f"Response: {response['output']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Demonstrate individual tools
    demonstrate_tool_usage()
    
    # Run agent examples
    run_agent_examples()
    
    # Demonstrate agent reasoning
    demonstrate_agent_reasoning()
    
    # Demonstrate specialized agents
    demonstrate_specialized_agents()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive agent conversation? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_agent_conversation()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 