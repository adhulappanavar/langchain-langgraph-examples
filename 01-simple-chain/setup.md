# Setup Guide for Example 1

## Prerequisites

1. **Python 3.8 or higher** installed on your system
2. **OpenAI API key** - Get one from [OpenAI's website](https://platform.openai.com/api-keys)

## Step-by-Step Setup

### 1. Navigate to the Example Directory
```bash
cd 01-simple-chain
```

### 2. Create a Virtual Environment (Recommended)
```bash
# Create virtual environment
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
python simple_chain.py
```

## Expected Output

If everything is set up correctly, you should see output like:

```
🤖 LangChain Example 1: Simple Chain
==================================================

📝 Story 1: a magical cat that can fly
------------------------------
Once upon a time, there was a fluffy orange cat named Whiskers who discovered...

📝 Story 2: a robot learning to cook
------------------------------
In a gleaming stainless steel kitchen, ChefBot-3000 stood before a cutting board...

📝 Story 3: a time-traveling backpack
------------------------------
Emma's ordinary school backpack had always been her trusted companion...
```

## Troubleshooting

### Common Issues:

1. **"OPENAI_API_KEY not found"**
   - Make sure you created the `.env` file
   - Verify your API key is correctly entered
   - Check that the file is in the same directory as `simple_chain.py`

2. **"ModuleNotFoundError"**
   - Make sure you installed the requirements: `pip install -r requirements.txt`
   - Verify you're in the correct virtual environment

3. **"Authentication error"**
   - Check that your OpenAI API key is valid
   - Ensure you have sufficient credits in your OpenAI account

4. **"Rate limit exceeded"**
   - Wait a moment and try again
   - Consider upgrading your OpenAI plan if this happens frequently

## Next Steps

Once you've successfully run this example, you're ready to move on to more complex examples that will introduce:

- Sequential chains
- Memory components
- Tools and agents
- LangGraph workflows

Each example builds upon the previous ones, so make sure you understand this basic example before proceeding! 