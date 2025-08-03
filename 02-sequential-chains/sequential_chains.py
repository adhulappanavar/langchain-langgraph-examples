"""
Example 2: Sequential Chains

This example demonstrates how to create chains that perform multiple operations in sequence.
We'll take a story generation chain and add analysis, summarization, and title generation steps.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# Load environment variables
load_dotenv()

class StoryAnalysis(BaseModel):
    """Structure for story analysis output"""
    themes: List[str] = Field(description="Main themes in the story")
    tone: str = Field(description="Overall tone of the story")
    complexity: str = Field(description="Complexity level (simple, moderate, complex)")
    target_audience: str = Field(description="Target audience for the story")

def create_story_generation_chain():
    """Create the initial story generation chain"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=200
    )
    
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a creative, engaging story about {topic}. Make it 3-4 paragraphs long with a clear beginning, middle, and end."
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="story")

def create_story_analysis_chain():
    """Create a chain to analyze the generated story"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=150
    )
    
    parser = PydanticOutputParser(pydantic_object=StoryAnalysis)
    
    prompt = PromptTemplate(
        input_variables=["story"],
        template="Analyze the following story and provide insights about its themes, tone, complexity, and target audience:\n\n{story}\n\n{format_instructions}",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="analysis")

def create_summary_chain():
    """Create a chain to summarize the story"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.4,
        max_tokens=100
    )
    
    prompt = PromptTemplate(
        input_variables=["story"],
        template="Create a concise, 2-3 sentence summary of the following story:\n\n{story}"
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="summary")

def create_title_chain():
    """Create a chain to generate a title for the story"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.6,
        max_tokens=50
    )
    
    prompt = PromptTemplate(
        input_variables=["story", "themes"],
        template="Based on this story and its themes ({themes}), generate a catchy, creative title:\n\n{story}"
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="title")

def create_sequential_chain():
    """Create a sequential chain that combines all the individual chains"""
    
    # Create individual chains
    story_chain = create_story_generation_chain()
    analysis_chain = create_story_analysis_chain()
    summary_chain = create_summary_chain()
    title_chain = create_title_chain()
    
    # Create the sequential chain
    sequential_chain = SequentialChain(
        chains=[story_chain, analysis_chain, summary_chain, title_chain],
        input_variables=["topic"],
        output_variables=["story", "analysis", "summary", "title"],
        verbose=True  # This will show the intermediate steps
    )
    
    return sequential_chain

def run_example():
    """Run the sequential chain example"""
    print("🤖 LangChain Example 2: Sequential Chains")
    print("=" * 60)
    
    # Create the sequential chain
    chain = create_sequential_chain()
    
    # Test topics
    topics = [
        "a robot discovering emotions",
        "a magical library that changes stories",
        "a time-traveling chef"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n📚 Story {i}: {topic}")
        print("=" * 50)
        
        try:
            # Run the sequential chain
            result = chain.invoke({"topic": topic})
            
            # Display results in a structured way
            print(f"\n📖 STORY:")
            print(result["story"])
            
            print(f"\n🔍 ANALYSIS:")
            print(result["analysis"])
            
            print(f"\n📝 SUMMARY:")
            print(result["summary"])
            
            print(f"\n🏷️  TITLE:")
            print(result["title"])
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Make sure you have set up your OpenAI API key in the .env file")

def interactive_mode():
    """Run the chain in interactive mode"""
    print("\n🎮 Interactive Mode")
    print("Enter topics for story generation (type 'quit' to exit)")
    print("-" * 50)
    
    chain = create_sequential_chain()
    
    while True:
        topic = input("\n🎯 Enter a topic: ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not topic:
            print("⚠️  Please enter a topic!")
            continue
        
        try:
            print("🤔 Generating story and analysis...")
            result = chain.invoke({"topic": topic})
            
            print(f"\n📖 STORY:")
            print(result["story"])
            
            print(f"\n🔍 ANALYSIS:")
            print(result["analysis"])
            
            print(f"\n📝 SUMMARY:")
            print(result["summary"])
            
            print(f"\n🏷️  TITLE:")
            print(result["title"])
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_chain_composition():
    """Demonstrate how to compose chains manually"""
    print("\n🔧 Chain Composition Demo")
    print("=" * 40)
    
    # Create individual chains
    story_chain = create_story_generation_chain()
    summary_chain = create_summary_chain()
    
    topic = "a wise old tree that can talk"
    
    print(f"🎯 Topic: {topic}")
    print("\n📖 Step 1: Generate story...")
    story_result = story_chain.invoke({"topic": topic})
    print(story_result)
    
    print("\n📝 Step 2: Generate summary...")
    summary_result = summary_chain.invoke({"story": story_result})
    print(summary_result)
    
    print("\n✨ This demonstrates manual chain composition!")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Run the main example
    run_example()
    
    # Demonstrate chain composition
    demonstrate_chain_composition()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 