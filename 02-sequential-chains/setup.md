# Setup Guide for Example 2: Sequential Chains

## Prerequisites

1. **Complete Example 1**: Make sure you've successfully run the first example
2. **Python 3.8 or higher** installed on your system
3. **OpenAI API key** (same as Example 1)
4. **Understanding of basic LangChain concepts** from Example 1

## Step-by-Step Setup

### 1. Navigate to the Example Directory
```bash
cd 02-sequential-chains
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
python sequential_chains.py
```

## Expected Output

If everything is set up correctly, you should see output like:

```
🤖 LangChain Example 2: Sequential Chains
============================================================

📚 Story 1: a robot discovering emotions
==================================================

📖 STORY:
In a gleaming laboratory filled with whirring machines and blinking lights...

🔍 ANALYSIS:
{
  "themes": ["self-discovery", "emotions", "humanity"],
  "tone": "contemplative and hopeful",
  "complexity": "moderate",
  "target_audience": "young adults and adults"
}

📝 SUMMARY:
A robot named Nova begins to experience emotions for the first time...

🏷️  TITLE:
"The Awakening of Nova: A Robot's Journey to Feel"

🔧 Chain Composition Demo
========================================
🎯 Topic: a wise old tree that can talk
...
```

## What's New in This Example

### 1. SequentialChain
- Combines multiple chains in sequence
- Automatically passes outputs between chains
- Shows intermediate steps with `verbose=True`

### 2. Output Parsing
- Uses Pydantic models for structured output
- Ensures consistent data format
- Makes outputs available to subsequent chains

### 3. Chain Composition
- Each chain has a specific purpose
- Different temperature settings for different tasks
- Modular and reusable components

## Key Differences from Example 1

| Feature | Example 1 | Example 2 |
|---------|-----------|-----------|
| Chains | Single LLMChain | Multiple chains in sequence |
| Output | Simple text | Structured data with parsing |
| Complexity | Basic | Intermediate |
| Reusability | Limited | High (modular chains) |
| Debugging | Basic | Verbose mode with intermediate steps |

## Interactive Features

The example includes:
- **Interactive Mode**: Enter your own topics
- **Chain Composition Demo**: Shows manual chain composition
- **Verbose Output**: See each step of the process

## Troubleshooting

### Common Issues:

1. **"Pydantic validation error"**
   - The LLM output doesn't match the expected format
   - Try adjusting the temperature or prompt for more consistent output
   - Check the parser format instructions

2. **"Output key not found"**
   - Make sure each chain has a unique `output_key`
   - Verify the chain order in the SequentialChain

3. **"Variable not found"**
   - Check that all required variables are available
   - Ensure chains are in the correct order

4. **"Import error for Pydantic"**
   - Make sure you installed all requirements: `pip install -r requirements.txt`
   - Pydantic should be included with LangChain

### Performance Tips:

1. **Temperature Settings**: Use lower temperatures for analysis (0.3) and higher for creativity (0.8)
2. **Token Limits**: Set appropriate `max_tokens` for each chain
3. **Model Selection**: Use appropriate models for each task
4. **Error Handling**: Add try-catch blocks for robust execution

## Next Steps

Once you've successfully run this example, you're ready for:
- **Example 3**: Memory chains for conversation context
- **Example 4**: Tools and agents for external integrations
- **Example 5**: LangGraph basics for workflow orchestration

Each example builds upon the previous ones, so make sure you understand the sequential chain concepts before proceeding! 