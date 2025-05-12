# Integration Points

*Last Updated: 2025-05-14*  
*Owner: Architecture Team*  
*Status: Active*

## Overview

This document provides a comprehensive overview of the integration points in the Alfred Agent Platform v2. Integration points are the defined interfaces and protocols through which different components of the platform communicate with each other and with external systems. They are critical to the platform's modular architecture, enabling flexibility, extensibility, and interoperability.

The Alfred Agent Platform v2 employs a robust integration architecture that spans from low-level transport mechanisms to high-level application interfaces. This document details each integration point, its purpose, technical specifications, and provides implementation examples to guide developers integrating with the platform.

## Key Integration Categories

The platform's integration points are organized into four main categories:

| Category | Description | Primary Technology | Examples |
|----------|-------------|-------------------|----------|
| **Inter-Agent Communication** | Communication between agents within the platform | A2A Protocol, Pub/Sub | Task delegation, collaborative workflows |
| **External System Integration** | Interfaces for external systems to interact with the platform | REST APIs, Webhooks | WhatsApp integration, Slack bot |
| **Storage Integration** | Interfaces for data persistence and retrieval | Supabase, Qdrant | State management, vector search |
| **Tool Integration** | Integration with specialized AI tools and frameworks | LangChain, CrewAI, n8n | Workflow automation, agent orchestration |

## Inter-Agent Communication

### A2A Protocol

The Agent-to-Agent (A2A) Protocol is the primary mechanism for communication between agents within the platform. It provides a standardized envelope structure for all agent messages.

#### Technical Specifications

- **Transport Layer**: Google Cloud Pub/Sub (primary), Supabase Realtime (secondary)
- **Message Format**: JSON
- **Protocol Version**: 2.1.0
- **Schema Validation**: Required via JSON Schema

#### Integration Example

```python
from libs.a2a_adapter import A2AEnvelope, PubSubTransport

# Create transport
transport = PubSubTransport(project_id="alfred-platform")

# Create message envelope
envelope = A2AEnvelope(
    intent="TREND_ANALYSIS",
    content={
        "url": "https://example.com/article",
        "depth": "standard"
    },
    source_agent_id="social-intelligence-agent",
    destination_agent_id="content-factory-agent"
)

# Send message
await transport.publish_task(envelope)
```

### Agent Pub/Sub Topics

All agents subscribe to specific Pub/Sub topics based on their responsibilities and capabilities. The topic naming follows a standardized pattern:

- `a2a.tasks.create`: For new task creation
- `a2a.tasks.update`: For task status updates
- `a2a.tasks.complete`: For task completion notifications
- `a2a.agent.[agent-id]`: Agent-specific topics

#### Topic Schema

```
a2a.[message-type].[operation].[tenant-id]?
```

## External System Integration

### REST API Gateway

The distributed API Gateway architecture provides a unified entry point for external systems to interact with the platform's capabilities.

#### Technical Specifications

- **Protocol**: HTTPS
- **Authentication**: JWT, API Key
- **Content Type**: application/json
- **Rate Limiting**: Tiered based on client ID
- **Documentation**: OpenAPI 3.0 Specification

#### Key Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/v2/tasks` | POST | Create a new task | JWT |
| `/api/v2/tasks/{task_id}` | GET | Retrieve task status | JWT |
| `/api/v2/tasks/{task_id}/results` | GET | Retrieve task results | JWT |
| `/api/v2/webhooks` | POST | Register webhook | API Key |

#### Integration Example

```python
import requests

# Create a new task
response = requests.post(
    "https://api.alfred-platform.example/api/v2/tasks",
    headers={
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    },
    json={
        "intent": "MARKET_ANALYSIS",
        "content": {
            "topic": "AI assistants",
            "depth": "comprehensive"
        }
    }
)

task_id = response.json()["task_id"]
```

### Webhook Integration

Webhooks enable external systems to receive notifications about events in the platform, such as task completion or status updates.

#### Technical Specifications

- **Delivery Method**: HTTPS POST
- **Payload Format**: JSON
- **Signature Verification**: HMAC-SHA256
- **Retry Policy**: Exponential backoff with 5 retries

#### Integration Example

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook/alfred', methods=['POST'])
def alfred_webhook():
    # Verify signature
    signature = request.headers.get('X-Alfred-Signature')
    payload = request.get_data()
    expected_signature = hmac.new(
        webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        return jsonify({"error": "Invalid signature"}), 401
    
    # Process webhook payload
    data = request.json
    task_id = data["task_id"]
    status = data["status"]
    
    # Handle event based on type
    if data["event_type"] == "task.completed":
        # Process completed task
        results = data["results"]
        # ...
    
    return jsonify({"status": "success"}), 200
```

## Storage Integration

### Supabase Integration

Supabase serves as the primary state storage and authentication provider for the platform.

#### Technical Specifications

- **Connection**: PostgreSQL client libraries
- **Authentication**: JWT, Role-based RLS
- **Real-time Capabilities**: Subscriptions for state changes
- **Schemas**: Strictly defined for each agent type

#### Integration Example

```python
from supabase import create_client

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key)

# Store task state
task_data = {
    "task_id": "task-123",
    "status": "processing",
    "created_at": "2025-05-14T10:30:00Z",
    "agent_id": "social-intelligence-agent",
    "content": {
        "url": "https://example.com/article",
        "depth": "standard"
    }
}

supabase.table("tasks").insert(task_data).execute()

# Query task state
task = supabase.table("tasks").select("*").eq("task_id", "task-123").execute()
```

### Qdrant Vector Store

Qdrant provides vector search capabilities for semantic search and retrieval of embeddings.

#### Technical Specifications

- **Connection**: HTTP or gRPC
- **Authentication**: API Key
- **Vector Dimensions**: Configurable per collection
- **Distance Metrics**: Cosine, Euclidean, Dot Product

#### Integration Example

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Initialize client
client = QdrantClient(url="https://qdrant.alfred-platform.example", api_key="...")

# Create or update a point
client.upsert(
    collection_name="articles",
    points=[
        models.PointStruct(
            id="article-123",
            vector=[0.1, 0.2, 0.3, ...],  # 1536-dimensional vector
            payload={
                "url": "https://example.com/article",
                "title": "AI Advances in 2025",
                "summary": "Recent developments in AI technology..."
            }
        )
    ]
)

# Search for similar content
search_result = client.search(
    collection_name="articles",
    query_vector=[0.15, 0.22, 0.31, ...],
    limit=5
)
```

## Tool Integration

### LangChain Integration

LangChain is the primary framework for building agent workflows and integrating language models.

#### Technical Specifications

- **Version Compatibility**: LangChain 0.1.5+
- **Integration Points**: Custom chains, tools, and agents
- **State Management**: LangChain state persistence via Supabase
- **Tracing**: LangSmith integration for debugging

#### Integration Example

```python
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI

# Create an agent with tools
llm = ChatOpenAI(model="gpt-4-turbo")
tools = [
    AlfredAnalysisTool(),  # Custom tool that calls platform APIs
    AlfredResearchTool(),
    AlfredPublishTool()
]

agent = create_structured_chat_agent(llm, tools, system_message)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Execute agent
result = agent_executor.invoke({"input": "Analyze recent AI trends"})
```

### CrewAI Integration

CrewAI provides team-based agent orchestration for complex workflows.

#### Technical Specifications

- **Version Compatibility**: CrewAI 0.21.0+
- **Integration Pattern**: Adapter for Alfred agents
- **State Persistence**: Task states stored in Supabase
- **Execution Models**: Sequential, hierarchical, consensus

#### Integration Example

```python
from crewai import Agent, Task, Crew, Process
from alfredplatform.crewai_adapter import AlfredAgentAdapter

# Create Alfred-adapted agents
social_intel_agent = AlfredAgentAdapter(
    agent_id="social-intelligence-agent",
    role="Researcher",
    goal="Discover trending topics in the target niche",
    backstory="Expert at social media trend analysis"
)

content_creation_agent = AlfredAgentAdapter(
    agent_id="content-factory-agent",
    role="Content Creator",
    goal="Create engaging content based on research",
    backstory="Skilled content creator with SEO expertise"
)

# Define tasks
research_task = Task(
    description="Research trending topics in AI assistants",
    agent=social_intel_agent
)

content_task = Task(
    description="Create a blog post outline based on the research",
    agent=content_creation_agent,
    context=[research_task]
)

# Create crew
crew = Crew(
    agents=[social_intel_agent, content_creation_agent],
    tasks=[research_task, content_task],
    process=Process.sequential
)

# Execute workflow
result = crew.kickoff()
```

### n8n Integration

n8n provides no-code/low-code workflow automation for the platform.

#### Technical Specifications

- **Version Compatibility**: n8n 1.5.0+
- **Integration Pattern**: Custom nodes for Alfred platform
- **Authentication**: JWT for API access
- **Webhook Support**: Bidirectional with platform

#### Integration Example

```json
{
  "nodes": [
    {
      "name": "Alfred Platform",
      "type": "n8n-nodes-alfred.alfredPlatform",
      "position": [100, 300],
      "parameters": {
        "operation": "createTask",
        "authentication": "jwtAuth",
        "intent": "MARKET_ANALYSIS",
        "content": {
          "topic": "="{{$json.topic}}",
          "depth": "comprehensive"
        },
        "waitForCompletion": true
      }
    },
    {
      "name": "Process Results",
      "type": "Function",
      "position": [400, 300],
      "parameters": {
        "functionCode": "return { processed: $input.all()[0].json.results.map(r => r.title) };"
      }
    }
  ],
  "connections": {
    "Alfred Platform": {
      "main": [
        [
          {
            "node": "Process Results",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Authentication and Security

All integration points implement consistent authentication and security mechanisms:

### Authentication Methods

| Method | Use Case | Implementation |
|--------|----------|----------------|
| **JWT** | Service-to-service, API calls | JSON Web Tokens signed with RS256 |
| **API Keys** | External system integration | UUID v4 with role-specific permissions |
| **RLS** | Database access control | Row-level security policies in Supabase |
| **HMAC Signatures** | Webhook verification | SHA-256 signatures of payloads |

### Security Controls

1. **Transport Security**: All communications use TLS 1.3+
2. **Rate Limiting**: Tiered rate limits based on client identity
3. **Input Validation**: Schema validation for all incoming data
4. **Audit Logging**: All API calls and agent activities are logged

## Integration Patterns

The following integration patterns should be used when interacting with the platform:

### 1. Asynchronous Processing Pattern

For long-running tasks, use the asynchronous processing pattern:

```
1. Client submits task → API Gateway
2. API Gateway returns task_id immediately
3. Client polls /tasks/{task_id} for status
4. When complete, client retrieves results from /tasks/{task_id}/results
```

### 2. Webhook Notification Pattern

For event-driven architectures, use the webhook notification pattern:

```
1. Client registers webhook URL at /api/v2/webhooks
2. Client submits task → API Gateway
3. When task state changes, platform sends webhook notification
4. Client processes webhook payload
```

### 3. Message-Based Integration Pattern

For platform extensions, use the message-based integration pattern:

```
1. Extension subscribes to relevant Pub/Sub topics
2. Extension processes incoming messages
3. Extension publishes response messages
4. Platform routes messages to appropriate components
```

## Versioning and Backward Compatibility

Integration points follow these versioning principles:

1. **Semantic Versioning**: All APIs follow semantic versioning (MAJOR.MINOR.PATCH)
2. **Backward Compatibility**: Minor and patch versions maintain backward compatibility
3. **Deprecation Policy**: Major version changes are announced 3 months in advance
4. **Multiple Version Support**: Major versions are supported for 12 months after deprecation

## Error Handling

All integration points implement consistent error handling:

1. **HTTP Status Codes**: RESTful APIs use standard HTTP status codes
2. **Error Payloads**: Structured error responses with code, message, and details
3. **Validation Errors**: Field-level validation errors with specifics
4. **Idempotency Keys**: Support for idempotent operations to prevent duplicates

## Testing and Verification

### Integration Test Resources

The platform provides the following resources for integration testing:

1. **Sandbox Environment**: https://sandbox.alfred-platform.example
2. **Mock Servers**: OpenAPI-generated mock servers for API testing
3. **Test Fixtures**: Sample payloads for all integration points
4. **Integration Test Suite**: Automated tests for validating integrations

### Environment-Specific Configurations

| Environment | Base URL | Purpose |
|-------------|----------|---------|
| Sandbox | https://sandbox.alfred-platform.example | Development and testing |
| Staging | https://staging.alfred-platform.example | Pre-production validation |
| Production | https://api.alfred-platform.example | Production use |

## Related Documentation

- [System Architecture](/architecture/system-architecture.md)
- [Agent Core Framework](/architecture/agent-core.md)
- [A2A Protocol](/api/a2a-protocol.md)
- [API Gateway](/api/api-gateway.md)
- [CrewAI Integration Guide](/project/crewai-integration-guide.md)
- [N8N Integration Guide](/project/n8n-integration-guide.md)