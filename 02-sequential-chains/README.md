# Example 2: Sequential Chains

## What you'll learn:
- Creating chains that perform multiple operations in sequence
- Using output from one chain as input to another
- Understanding the power of chaining operations
- Building more complex workflows with LangChain

## Concepts covered:
- **SequentialChain**: Combining multiple chains in sequence
- **Output Parsing**: Extracting structured data from LLM responses
- **Chain Composition**: Building complex workflows from simple components
- **Intermediate Results**: Using outputs from previous steps

## Prerequisites:
- Complete Example 1: Simple Chain
- Understanding of basic LangChain concepts
- OpenAI API key (same as Example 1)

## Building on Example 1:
This example takes the simple story generation from Example 1 and adds:
1. **Analysis Step**: Analyze the generated story
2. **Summary Step**: Create a concise summary
3. **Title Generation**: Generate an appropriate title
4. **Sequential Execution**: Run all steps in order

## Next examples will introduce:
- Memory to maintain context across interactions
- Tools for external API integration
- Agents for autonomous decision-making
- LangGraph for complex workflow orchestration 