# Customer Service Workflow: Understand → Classify → Route → Respond

## 🎯 Overview

This example demonstrates a real-world customer service automation workflow using sequential chains. Each step processes the customer inquiry and passes structured information to the next step.

## 📊 Customer Service Workflow Diagram

```
Customer Message: "I can't reset my password and I'm frustrated!"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOMER SERVICE WORKFLOW                   │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   STEP 1:       │    │   STEP 2:       │    │   STEP 3:       │    │   STEP 4:       │
│  Understanding  │───▶│ Classification  │───▶│    Routing      │───▶│   Response      │
│                 │    │                 │    │                 │    │                 │
│ Input: message  │    │ Input: understanding│ Input: understanding│ Input: all previous
│ Output: structured│  │ Output: category │ Output: department │ Output: response
│ Temp: 0.2       │    │ Temp: 0.3       │ Temp: 0.2       │ Temp: 0.7       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
    ↓                       ↓                       ↓                       ↓
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              CUSTOMER SERVICE RESULT                                  │
│  {                                                                                    │
│    "understanding": {main_issue: "password reset", emotion: "frustrated", ...},      │
│    "classification": {category: "technical", complexity: "simple", ...},              │
│    "routing": {department: "technical", priority: "high", ...},                       │
│    "response": "I understand your frustration with the password reset..."              │
│  }                                                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Detailed Step-by-Step Flow

### Step 1: Understanding Chain
```
Input: "I can't reset my password and I'm frustrated!"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    UNDERSTANDING CHAIN                         │
├─────────────────────────────────────────────────────────────────┤
│ LLM: GPT-3.5-turbo (temperature=0.2, max_tokens=200)         │
│                                                                 │
│ Pydantic Parser: CustomerInquiry                              │
│ - main_issue: str                                             │
│ - customer_emotion: str                                       │
│ - urgency_level: UrgencyLevel                                 │
│ - context: List[str]                                          │
│                                                                 │
│ Prompt: "Analyze the following customer inquiry..."            │
│                                                                 │
│ Output Key: "understanding"                                   │
└─────────────────────────────────────────────────────────────────┘
    ↓
Output: {
  "main_issue": "password reset failure",
  "customer_emotion": "frustrated",
  "urgency_level": "high",
  "context": ["been trying for 2 hours", "nothing works"]
}
```

### Step 2: Classification Chain
```
Input: understanding = {main_issue: "password reset failure", ...}
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CLASSIFICATION CHAIN                        │
├─────────────────────────────────────────────────────────────────┤
│ LLM: GPT-3.5-turbo (temperature=0.3, max_tokens=150)         │
│                                                                 │
│ Pydantic Parser: Classification                               │
│ - category: str                                               │
│ - subcategory: str                                            │
│ - complexity: str                                             │
│ - estimated_resolution_time: str                              │
│ - requires_escalation: bool                                   │
│                                                                 │
│ Prompt: "Based on the customer inquiry analysis..."            │
│                                                                 │
│ Output Key: "classification"                                  │
└─────────────────────────────────────────────────────────────────┘
    ↓
Output: {
  "category": "technical",
  "subcategory": "authentication",
  "complexity": "simple",
  "estimated_resolution_time": "5-10 minutes",
  "requires_escalation": false
}
```

### Step 3: Routing Chain
```
Input: understanding = {...}
Input: classification = {category: "technical", ...}
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                      ROUTING CHAIN                             │
├─────────────────────────────────────────────────────────────────┤
│ LLM: GPT-3.5-turbo (temperature=0.2, max_tokens=150)         │
│                                                                 │
│ Pydantic Parser: RoutingDecision                              │
│ - department: Department                                       │
│ - priority: str                                               │
│ - agent_requirements: List[str]                               │
│ - sla_target: str                                             │
│                                                                 │
│ Prompt: "Based on the understanding and classification..."     │
│                                                                 │
│ Output Key: "routing"                                         │
└─────────────────────────────────────────────────────────────────┘
    ↓
Output: {
  "department": "technical",
  "priority": "high",
  "agent_requirements": ["password reset expertise", "customer service skills"],
  "sla_target": "30 minutes"
}
```

### Step 4: Response Chain
```
Input: customer_message = "I can't reset my password..."
Input: understanding = {...}
Input: classification = {...}
Input: routing = {...}
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE CHAIN                              │
├─────────────────────────────────────────────────────────────────┤
│ LLM: GPT-3.5-turbo (temperature=0.7, max_tokens=300)         │
│                                                                 │
│ Prompt: "Generate an appropriate customer service response..." │
│                                                                 │
│ Output Key: "response"                                        │
└─────────────────────────────────────────────────────────────────┘
    ↓
Output: "I understand your frustration with the password reset issue. I can see you've been trying for 2 hours, and that's definitely not the experience we want for our customers. Let me help you get this resolved quickly. I'm routing this to our technical team who specializes in authentication issues. They should be able to help you within 30 minutes. In the meantime, here are a few things you can try..."
```

## 🎯 Real-World Customer Service Examples

### Example 1: Technical Issue (High Urgency)
```
Input: "I've been trying to reset my password for 2 hours and nothing works! This is ridiculous!"

Understanding:
- Main Issue: Password reset failure
- Emotion: Frustrated
- Urgency: High
- Context: 2 hours of trying, nothing works

Classification:
- Category: Technical
- Subcategory: Authentication
- Complexity: Simple
- Resolution Time: 5-10 minutes
- Escalation: No

Routing:
- Department: Technical
- Priority: High
- Agent Requirements: Password reset expertise
- SLA: 30 minutes

Response: "I understand your frustration with the password reset issue..."
```

### Example 2: Billing Inquiry (Medium Urgency)
```
Input: "My bill this month is $200 more than usual. I don't understand why it's so high."

Understanding:
- Main Issue: Unexpected bill increase
- Emotion: Confused
- Urgency: Medium
- Context: $200 increase, unusual amount

Classification:
- Category: Billing
- Subcategory: Bill inquiry
- Complexity: Moderate
- Resolution Time: 15-30 minutes
- Escalation: No

Routing:
- Department: Billing
- Priority: Medium
- Agent Requirements: Billing expertise, customer service skills
- SLA: 2 hours

Response: "I can see you're concerned about the unexpected increase in your bill..."
```

### Example 3: Sales Inquiry (Low Urgency)
```
Input: "Hi, I'm interested in upgrading my plan. Can you tell me about the premium features?"

Understanding:
- Main Issue: Plan upgrade inquiry
- Emotion: Interested
- Urgency: Low
- Context: Premium features interest

Classification:
- Category: Sales
- Subcategory: Plan upgrade
- Complexity: Simple
- Resolution Time: 10-15 minutes
- Escalation: No

Routing:
- Department: Sales
- Priority: Low
- Agent Requirements: Sales expertise, product knowledge
- SLA: 4 hours

Response: "Great to hear you're interested in upgrading your plan! I'd be happy to walk you through our premium features..."
```

## 🔧 Technical Implementation

### Customer Service Chain Configuration
```python
customer_service_chain = SequentialChain(
    chains=[understanding_chain, classification_chain, routing_chain, response_chain],
    input_variables=["customer_message"],
    output_variables=["understanding", "classification", "routing", "response"],
    verbose=True
)
```

### Data Flow in Practice
```python
# 1. Customer sends message
customer_message = "I can't reset my password and I'm frustrated!"

# 2. SequentialChain automatically:
#    - Runs understanding_chain with customer_message
#    - Passes understanding output to classification_chain
#    - Passes understanding + classification to routing_chain
#    - Passes all previous outputs to response_chain

# 3. Returns comprehensive result
result = chain.run(customer_message=customer_message)
# result = {
#     "understanding": {...},
#     "classification": {...},
#     "routing": {...},
#     "response": "..."
# }
```

## 🎯 Benefits of This Approach

### 1. **Consistent Understanding**
- Structured analysis of customer intent
- Consistent emotion and urgency detection
- Standardized context extraction

### 2. **Intelligent Classification**
- Automatic categorization of issues
- Complexity assessment
- Escalation decision making

### 3. **Optimal Routing**
- Department assignment based on analysis
- Priority level determination
- Agent skill matching

### 4. **Personalized Responses**
- Context-aware responses
- Emotion-appropriate tone
- Clear next steps and expectations

## 🚀 Real-World Applications

### Customer Service Automation
- **Chatbots**: Automated first-line support
- **Ticket Routing**: Intelligent ticket assignment
- **Response Generation**: Consistent, professional responses
- **Escalation Management**: Automatic escalation decisions

### Quality Assurance
- **Response Quality**: Consistent response standards
- **Routing Accuracy**: Proper department assignment
- **SLA Compliance**: Automatic SLA target setting
- **Customer Satisfaction**: Emotion-aware responses

### Analytics and Insights
- **Issue Trends**: Categorization for trend analysis
- **Response Times**: SLA tracking and optimization
- **Customer Emotions**: Sentiment analysis for improvement
- **Agent Performance**: Skill-based routing optimization

This customer service workflow demonstrates how sequential chains can create sophisticated, real-world applications that improve customer experience while maintaining consistency and efficiency! 