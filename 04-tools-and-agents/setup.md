# Setup Guide for Example 4: Tools and Agents

## Prerequisites

1. **Complete Example 3**: Make sure you've successfully run the memory chains example
2. **Python 3.8 or higher** installed on your system
3. **OpenAI API key** (same as previous examples)
4. **Understanding of memory and chains** from Example 3

## Step-by-Step Setup

### 1. Navigate to the Example Directory
```bash
cd 04-tools-and-agents
```

### 2. Set Up Virtual Environment (if not already done)
```bash
# Create virtual environment (if you haven't already)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key
```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file and add your OpenAI API key
# Replace 'your_openai_api_key_here' with your actual API key
```

### 5. Test the Setup
```bash
python tools_and_agents.py
```

## Expected Output

If everything is set up correctly, you should see output like:

```
🔧 Tool Usage Demo
========================================

🔧 Testing weather tool:
Input: New York
Output: Weather in New York: 22°C, Sunny, Humidity: 65%, Wind: 10 km/h

🔧 Testing calculator tool:
Input: 150 * 1.085
Output: Result: 150 * 1.085 = 162.75

🔧 Testing search tool:
Input: return policy
Output: Search results for 'return policy':
Information about return policy - This is a simulated search result.
More details about return policy - Another simulated result.

🤖 Tools and Agents Example: Customer Service Agent
============================================================

📋 Scenario 1: A customer is asking about delivery delays due to weather in New York. Can you check the weather?
--------------------------------------------------
🤖 Agent Response: Let me check the current weather in New York for you.
[Agent uses weather tool]
Weather in New York: 22°C, Sunny, Humidity: 65%, Wind: 10 km/h

Based on the current weather conditions, there shouldn't be any delivery delays due to weather in New York today.
```

## What's New in This Example

### 1. Custom Tools
- **WeatherTool**: Simulates weather API calls
- **CalculatorTool**: Performs mathematical calculations
- **SearchTool**: Simulates web search functionality
- **CustomerDatabaseTool**: Simulates customer database lookups

### 2. Agent Configuration
- **Agent Types**: CONVERSATIONAL_REACT_DESCRIPTION for chat-based interactions
- **Tool Integration**: Agents automatically choose which tools to use
- **Memory Integration**: Conversation history is maintained
- **Verbose Mode**: Shows agent reasoning process

### 3. Agent Reasoning
- **Tool Selection**: Agents decide which tools are needed
- **Multi-tool Usage**: Complex requests use multiple tools
- **Result Synthesis**: Combines tool results into coherent responses

## Key Differences from Example 3

| Feature | Example 3 | Example 4 |
|---------|-----------|-----------|
| Tools | No external tools | Custom tools for specific tasks |
| Reasoning | Basic chain execution | Autonomous tool selection |
| Capabilities | Limited to LLM knowledge | Access to external data and APIs |
| Complexity | Sequential chains | Agent-based decision making |
| Autonomy | Manual chain selection | Automatic tool selection |

## Interactive Features

The example includes:
- **Tool Usage Demo**: Shows individual tool functionality
- **Agent Examples**: Pre-built scenarios demonstrating agent reasoning
- **Interactive Mode**: Real-time conversation with the agent
- **Specialized Agents**: Different agents for different use cases

## Agent Types Explained

### CONVERSATIONAL_REACT_DESCRIPTION
- Best for chat-based interactions
- Maintains conversation context
- Good for customer service scenarios

### ZERO_SHOT_REACT_DESCRIPTION
- For single-turn tasks
- No conversation memory
- Good for one-off requests

### STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
- For structured conversations
- Maintains conversation structure
- Good for guided interactions

## Tool Categories

### Information Tools
- **Weather**: Get current weather conditions
- **Search**: Find information on the web
- **Database**: Look up customer information

### Computation Tools
- **Calculator**: Perform mathematical calculations
- **Currency Converter**: Convert between currencies
- **Unit Converter**: Convert between units

### Action Tools
- **Email Sender**: Send emails
- **File Operations**: Read/write files
- **API Calls**: Make external API requests

## Agent Reasoning Process

### 1. Input Analysis
Agent analyzes the user's request to understand what's needed.

### 2. Tool Selection
Agent decides which tools are appropriate for the request.

### 3. Tool Execution
Agent calls the selected tools with appropriate parameters.

### 4. Result Synthesis
Agent combines tool results into a coherent response.

## Troubleshooting

### Common Issues:

1. **"Tool not found"**
   - Check tool names and descriptions
   - Ensure tools are properly registered with the agent
   - Verify tool imports are correct

2. **"Agent confusion"**
   - Improve tool descriptions to be more specific
   - Add more examples to tool descriptions
   - Use verbose mode to see agent reasoning

3. **"Memory issues"**
   - Check memory configuration
   - Ensure memory is properly attached to agent
   - Verify memory key matches prompt variables

4. **"Performance issues"**
   - Monitor tool execution times
   - Consider caching frequently used results
   - Optimize tool implementations

### Performance Tips:

1. **Tool Caching**: Cache frequently used tool results
2. **Parallel Execution**: Run independent tools simultaneously
3. **Tool Optimization**: Optimize tool implementations
4. **Agent Tuning**: Adjust agent parameters for your use case

## Real-World Integration

### Weather API Integration
```python
# Replace simulated weather with real API
import requests

def get_real_weather(location):
    api_key = "your_weather_api_key"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.json()
```

### Database Integration
```python
# Replace simulated database with real database
import sqlite3

def get_customer_info(customer_id):
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    return cursor.fetchone()
```

## Next Steps

Once you've successfully run this example, you're ready for:
- **Example 5**: LangGraph basics for workflow orchestration
- **Example 6**: Advanced LangGraph for complex workflows
- **Example 7**: Real-world application with full integration

Each example builds upon the previous ones, so make sure you understand the tools and agents concepts before proceeding! 