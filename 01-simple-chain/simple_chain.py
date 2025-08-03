"""
Example 1: Simple LangChain Chain

This example demonstrates the most basic usage of LangChain - creating a simple LLM chain
that takes user input and generates a response using OpenAI's language model.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

def create_simple_chain():
    """
    Create a simple LLM chain that generates creative writing based on a topic.
    """
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = very creative)
        max_tokens=150
    )
    
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["topic"],
        template="Write a short, creative story about {topic}. Make it engaging and fun to read."
    )
    
    # Create the chain by combining the LLM and prompt
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    return chain

def run_example():
    """
    Run the simple chain example.
    """
    print("🤖 LangChain Example 1: Simple Chain")
    print("=" * 50)
    
    # Create the chain
    chain = create_simple_chain()
    
    # Test with different topics
    topics = [
        "a magical cat that can fly",
        "a robot learning to cook",
        "a time-traveling backpack"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n📝 Story {i}: {topic}")
        print("-" * 30)
        
        try:
            # Run the chain
            response = chain.invoke({"topic": topic})
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Make sure you have set up your OpenAI API key in the .env file")

def interactive_mode():
    """
    Run the chain in interactive mode where users can input their own topics.
    """
    print("\n🎮 Interactive Mode")
    print("Enter topics for creative stories (type 'quit' to exit)")
    print("-" * 40)
    
    chain = create_simple_chain()
    
    while True:
        topic = input("\n🎯 Enter a topic: ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not topic:
            print("⚠️  Please enter a topic!")
            continue
        
        try:
            print("🤔 Generating story...")
            response = chain.invoke({"topic": topic})
            print(f"📖 {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Run the example
    run_example()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 