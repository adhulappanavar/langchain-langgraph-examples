# Understanding Example 2: Sequential Chains

## What are Sequential Chains?

Sequential chains allow you to combine multiple LangChain operations in a specific order, where the output of one chain becomes the input to the next. This is a powerful way to build complex workflows from simple, reusable components.

## Key Concepts in This Example

### 1. SequentialChain
The `SequentialChain` class combines multiple chains and executes them in order:
```python
sequential_chain = SequentialChain(
    chains=[story_chain, analysis_chain, summary_chain, title_chain],
    input_variables=["topic"],
    output_variables=["story", "analysis", "summary", "title"],
    verbose=True
)
```

**Parameters explained:**
- `chains`: List of chains to execute in order
- `input_variables`: Variables that the first chain needs
- `output_variables`: Variables that will be available in the final result
- `verbose`: Shows intermediate steps during execution

### 2. Output Parsing with Pydantic
We use Pydantic models to structure the output from the analysis chain:
```python
class StoryAnalysis(BaseModel):
    themes: List[str] = Field(description="Main themes in the story")
    tone: str = Field(description="Overall tone of the story")
    complexity: str = Field(description="Complexity level")
    target_audience: str = Field(description="Target audience")
```

This ensures consistent, structured output that can be used by subsequent chains.

### 3. Chain Composition
Each chain has a specific purpose:
- **Story Generation**: Creates the initial content
- **Analysis**: Extracts structured insights
- **Summary**: Creates a concise version
- **Title Generation**: Creates a catchy title

## Code Breakdown

### Creating Individual Chains
Each chain is created with specific parameters:

```python
def create_story_generation_chain():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.8,  # More creative for story generation
        max_tokens=200
    )
    
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a creative, engaging story about {topic}..."
    )
    
    return LLMChain(llm=llm, prompt=prompt, output_key="story")
```

**Key differences from Example 1:**
- `output_key`: Specifies the key for this chain's output
- Different temperatures for different tasks
- Structured prompts for specific purposes

### Using Output Parsers
The analysis chain uses a Pydantic parser for structured output:

```python
parser = PydanticOutputParser(pydantic_object=StoryAnalysis)
prompt = PromptTemplate(
    input_variables=["story"],
    template="Analyze the following story...\n\n{format_instructions}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

This ensures the LLM returns data in the exact format we need.

### Combining Chains
The sequential chain automatically handles the flow of data:

1. **Input**: `topic` → Story Generation Chain
2. **Output**: `story` → Analysis Chain
3. **Output**: `analysis` → Summary Chain
4. **Output**: `summary` → Title Chain
5. **Final Output**: All results combined

## What You've Learned

1. **Chain Composition**: How to combine multiple chains
2. **Output Parsing**: Using Pydantic for structured data
3. **Sequential Execution**: Automatic flow between chains
4. **Intermediate Results**: Accessing outputs from each step
5. **Verbose Mode**: Debugging and understanding the flow

## Advanced Concepts Introduced

### Temperature Control
Different chains use different temperature settings:
- **Story Generation**: `temperature=0.8` (creative)
- **Analysis**: `temperature=0.3` (consistent)
- **Summary**: `temperature=0.4` (balanced)
- **Title**: `temperature=0.6` (creative but controlled)

### Output Keys
Each chain specifies an `output_key` that becomes available to subsequent chains:
- `story` → available to analysis, summary, and title chains
- `analysis` → available to title chain
- `summary` → final output
- `title` → final output

### Manual Chain Composition
The example also shows how to manually compose chains:
```python
story_result = story_chain.run(topic=topic)
summary_result = summary_chain.run(story=story_result)
```

This gives you more control but requires manual management of data flow.

## Benefits of Sequential Chains

1. **Modularity**: Each chain has a single responsibility
2. **Reusability**: Chains can be reused in different combinations
3. **Maintainability**: Easy to modify individual steps
4. **Debugging**: Can test each chain independently
5. **Scalability**: Easy to add new steps to the workflow

## Common Patterns

### Error Handling
Each chain can have its own error handling:
```python
try:
    result = chain.run(topic=topic)
except Exception as e:
    print(f"❌ Error: {e}")
```

### Conditional Execution
You can conditionally execute chains based on results:
```python
if "error" not in story_result:
    analysis_result = analysis_chain.run(story=story_result)
```

### Parallel Execution
For independent operations, you can run chains in parallel (we'll see this in later examples).

## Next Steps

In upcoming examples, you'll learn about:
- **Memory**: Maintaining context across interactions
- **Tools**: Integrating external APIs and functions
- **Agents**: Creating autonomous systems
- **LangGraph**: Building complex workflows with state management

## Troubleshooting

### Common Issues:

1. **Output Key Conflicts**: Make sure each chain has a unique output key
2. **Variable Dependencies**: Ensure all required variables are available
3. **Parser Errors**: Check that Pydantic models match expected output
4. **Chain Order**: Verify chains are in the correct sequence

### Performance Tips:

1. **Batch Processing**: Process multiple inputs together when possible
2. **Caching**: Cache intermediate results for expensive operations
3. **Parallel Execution**: Run independent chains in parallel
4. **Model Selection**: Use appropriate models for each task 