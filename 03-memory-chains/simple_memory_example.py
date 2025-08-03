"""
Simple Memory Example: Demonstrating Memory with Customer Service

This example shows how to properly use memory components with LangChain chains.
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.schema import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

def create_memory_aware_customer_service():
    """Create a customer service chain with memory"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=300
    )
    
    # Create memory component
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="customer_message"
    )
    
    prompt = PromptTemplate(
        input_variables=["customer_message", "chat_history"],
        template="""You are a helpful customer service representative. Use the conversation history to provide contextual responses.

Previous Conversation:
{chat_history}

Current Customer Message: {customer_message}

Provide a helpful, empathetic response that:
1. Acknowledges the customer's issue
2. References previous context when relevant
3. Provides clear next steps
4. Maintains a professional, helpful tone

Response:"""
    )
    
    return LLMChain(llm=llm, prompt=prompt, memory=memory)

def run_memory_conversation():
    """Run a conversation with memory"""
    print("🎯 Simple Memory Example: Customer Service with Memory")
    print("=" * 60)
    
    # Create the chain with memory
    chain = create_memory_aware_customer_service()
    
    # Conversation scenarios
    conversations = [
        # Scenario 1: Technical issue with follow-ups
        [
            "I can't log into my account. The password reset isn't working.",
            "I tried that already. It's been 2 hours and nothing works!",
            "Can you just reset it for me? I have an important meeting in 30 minutes.",
            "Thanks! That worked. You're the best!"
        ],
        # Scenario 2: Billing issue with clarification
        [
            "My bill is much higher than usual this month.",
            "It's $200 more than last month. I don't understand why.",
            "Can you explain what the extra charges are for?",
            "That makes sense now. Thanks for clarifying."
        ]
    ]
    
    for scenario_num, messages in enumerate(conversations, 1):
        print(f"\n🔄 Conversation Scenario {scenario_num}")
        print("=" * 50)
        
        # Reset memory for each scenario
        chain = create_memory_aware_customer_service()
        
        for turn_num, message in enumerate(messages, 1):
            print(f"\n📧 Turn {turn_num}: '{message}'")
            print("-" * 40)
            
            try:
                # Run the chain
                response = chain.invoke({"customer_message": message})
                
                print(f"🤖 Assistant: {response['text']}")
                
                # Show memory state
                print(f"\n🧠 Memory State:")
                if chain.memory.chat_memory.messages:
                    print("Previous messages:")
                    for i, msg in enumerate(chain.memory.chat_memory.messages[-4:], 1):
                        role = "👤 Customer" if isinstance(msg, HumanMessage) else "🤖 Assistant"
                        print(f"  {i}. {role}: {msg.content[:100]}...")
                else:
                    print("  No previous messages")
                
            except Exception as e:
                print(f"❌ Error: {e}")

def demonstrate_memory_types():
    """Demonstrate different types of memory components"""
    print("\n🧠 Memory Types Demo")
    print("=" * 40)
    
    # 1. ConversationBufferMemory
    print("\n1️⃣ ConversationBufferMemory (Full History)")
    buffer_memory = ConversationBufferMemory(return_messages=True)
    
    # Add some messages
    buffer_memory.chat_memory.add_user_message("I can't log in")
    buffer_memory.chat_memory.add_ai_message("I understand you're having login issues. Let me help you.")
    buffer_memory.chat_memory.add_user_message("I tried resetting my password")
    buffer_memory.chat_memory.add_ai_message("I see you've already tried password reset. Let me escalate this.")
    
    print("Full conversation history:")
    for message in buffer_memory.chat_memory.messages:
        role = "👤 User" if isinstance(message, HumanMessage) else "🤖 Assistant"
        print(f"  {role}: {message.content}")
    
    # 2. ConversationSummaryMemory
    print("\n2️⃣ ConversationSummaryMemory (Summarized)")
    summary_memory = ConversationSummaryMemory(llm=ChatOpenAI(temperature=0))
    
    # Add the same messages
    summary_memory.chat_memory.add_user_message("I can't log in")
    summary_memory.chat_memory.add_ai_message("I understand you're having login issues. Let me help you.")
    summary_memory.chat_memory.add_user_message("I tried resetting my password")
    summary_memory.chat_memory.add_ai_message("I see you've already tried password reset. Let me escalate this.")
    
    print("Conversation summary:")
    print(f"  {summary_memory.buffer}")

def interactive_memory_conversation():
    """Run an interactive conversation with memory"""
    print("\n🎮 Interactive Memory Conversation")
    print("=" * 50)
    print("Start a conversation with the customer service bot.")
    print("The bot will remember your previous messages and maintain context.")
    print("Type 'quit' to end the conversation.")
    print("-" * 50)
    
    # Create the chain
    chain = create_memory_aware_customer_service()
    
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
            response = chain.invoke({"customer_message": message})
            
            print(f"\n🤖 Assistant: {response['text']}")
            
            # Show memory info
            memory_count = len(chain.memory.chat_memory.messages)
            print(f"📝 Memory: {memory_count} messages stored")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_conversation_chain():
    """Demonstrate the built-in ConversationChain"""
    print("\n💬 ConversationChain Demo")
    print("=" * 40)
    
    # Create a conversation chain with memory
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory()
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    # Test conversation
    messages = [
        "Hi, I'm having trouble with my account.",
        "I can't log in, it says my password is wrong.",
        "I tried resetting it but the email never came.",
        "Thanks for your help!"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📧 Turn {i}: '{message}'")
        print("-" * 30)
        
        try:
            response = conversation.predict(input=message)
            print(f"🤖 Assistant: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("💡 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    # Demonstrate memory types
    demonstrate_memory_types()
    
    # Demonstrate conversation chain
    demonstrate_conversation_chain()
    
    # Run memory conversation examples
    run_memory_conversation()
    
    # Ask if user wants to try interactive mode
    try:
        choice = input("\n🎮 Would you like to try interactive memory conversation? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_memory_conversation()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 