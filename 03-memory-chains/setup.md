# Setup Guide for Example 3: Memory Chains

## Prerequisites

1. **Complete Example 2**: Make sure you've successfully run the customer service example
2. **Python 3.8 or higher** installed on your system
3. **OpenAI API key** (same as previous examples)
4. **Understanding of sequential chains** from Example 2

## Step-by-Step Setup

### 1. Navigate to the Example Directory
```bash
cd 03-memory-chains
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
python memory_chains.py
```

## Expected Output

If everything is set up correctly, you should see output like:

```
🧠 Memory Types Demo
========================================

1️⃣ ConversationBufferMemory (Full History)
Full conversation history:
  👤 User: I can't log in
  🤖 Assistant: I understand you're having login issues. Let me help you.
  👤 User: I tried resetting my password
  🤖 Assistant: I see you've already tried password reset. Let me escalate this.

2️⃣ ConversationSummaryMemory (Summarized)
Conversation summary:
  The user is having login issues and has already tried password reset...

🎯 Memory Chains Example: Multi-turn Customer Service Conversation
======================================================================

🔄 Conversation Scenario 1
==================================================

📧 Turn 1: 'I can't log into my account. The password reset isn't working.'
----------------------------------------
🔍 Understanding:
  Main Issue: login failure
  Emotion: frustrated
  Is Follow-up: false
  References: N/A

🏷️  Classification:
  Category: technical
  Is New Issue: true
  Related To: N/A

🔄 Routing:
  Department: technical
  Continue Session: true
  Session Notes: Customer having login issues

💬 Response:
I understand you're having trouble logging into your account...
```

## What's New in This Example

### 1. Memory Components
- **ConversationBufferMemory**: Stores full conversation history
- **ConversationSummaryMemory**: Stores summarized conversation history
- **Memory Integration**: Chains now have access to conversation context

### 2. Enhanced Analysis
- **Follow-up Detection**: Identifies when customers are continuing previous issues
- **Context Awareness**: Responses consider conversation history
- **Session Management**: Maintains context across multiple interactions

### 3. Multi-turn Conversations
- **Scenario Testing**: Pre-built conversation scenarios
- **Interactive Mode**: Real-time conversation with memory
- **Context Preservation**: Information persists across turns

## Key Differences from Example 2

| Feature | Example 2 | Example 3 |
|---------|-----------|-----------|
| Memory | No memory | Full conversation memory |
| Context | Single message | Multi-turn context |
| Follow-ups | Not handled | Automatically detected |
| Session | Stateless | Stateful with context |
| UX | Basic | Enhanced with continuity |

## Interactive Features

The example includes:
- **Memory Types Demo**: Shows different memory components
- **Multi-turn Scenarios**: Pre-built conversation examples
- **Interactive Mode**: Real-time conversation with memory
- **Context Display**: Shows how memory affects analysis

## Memory Concepts Explained

### ConversationBufferMemory
- Stores every message in the conversation
- Provides full context for analysis
- Best for short to medium conversations

### ConversationSummaryMemory
- Summarizes conversation history
- Reduces token usage for long conversations
- Maintains key context without full history

### Memory Integration
- Chains automatically access conversation history
- Prompts include previous context
- Responses consider full conversation

## Troubleshooting

### Common Issues:

1. **"Memory not working"**
   - Check that memory is properly attached to chains
   - Verify memory_key matches prompt variables
   - Ensure memory is shared across relevant chains

2. **"Token limit exceeded"**
   - Use ConversationSummaryMemory for long conversations
   - Implement memory size limits
   - Clear memory when starting new sessions

3. **"Context not preserved"**
   - Check memory integration in chain creation
   - Verify memory is being passed correctly
   - Ensure memory is not being reset unexpectedly

4. **"Follow-up detection not working"**
   - Check that conversation history is being included in prompts
   - Verify JSON parsing is working correctly
   - Ensure memory is being maintained across turns

### Performance Tips:

1. **Memory Type Selection**: Choose appropriate memory type for your use case
2. **Token Management**: Monitor token usage with memory components
3. **Memory Cleanup**: Clear memory when starting new sessions
4. **Memory Persistence**: Save important context for later use

## Next Steps

Once you've successfully run this example, you're ready for:
- **Example 4**: Tools and agents for external integrations
- **Example 5**: LangGraph basics for workflow orchestration
- **Example 6**: Advanced LangGraph for complex workflows

Each example builds upon the previous ones, so make sure you understand the memory chain concepts before proceeding! 