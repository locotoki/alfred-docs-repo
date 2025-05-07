# AI Agent Platform v2 - Technical Architecture Document

## 1. Architecture Snapshot (v2 fusion)

```
┌────────────────────────────────────────────────────────────────┐
│                    Mission-Control UI (Next.js)               │
│        ⬑ Supabase Realtime websockets for live status         │
└────────────────────────────────────────────────────────────────┘
                ▲                             |
                | HTTP (agent card, health)   | WebSocket
┌───────────────┴───────────────┐   ┌────────┴────────┐
│  Specialist Agents (Docker)   │   │ Entry Agent     │
│  • SocialIntel (LangGraph)    │   │  Alfred Slack   │
│  • LegalCompliance (LangGraph)│   │  Bot            │
│  • …                          │   └─────────────────┘
│        |        ▲                         ▲
│        | gRPC   | LangGraph calls         │
└────────┼────────┘                         │
         │                                  │
         ▼                                  │
   ┌────────────┐  Pub/Sub  ┌────────────┐  │
   │ a2a.tasks  │◄──────────┤ a2a.tasks  │◄─┘
   │   .create  │           │ .completed │   Exactly-once
   └────────────┘           └────────────┘   Guarantees
         ▲                                  
         │
┌────────┴─────────┐
│  Supabase DB     │           ┌───────────┐
│  (Postgres +     │           │  Qdrant   │
│   pgvector)      │           │  Vector   │
└──────────────────┘           └───────────┘
```

*Key architecture features*

- **Event-driven architecture** using Google Cloud Pub/Sub
- **Supabase PostgreSQL** with pgvector for state storage and vector embeddings
- **A2A adapter library** for message envelope handling 
- **LangSmith traces** exported to Cloud Trace for unified observability
- **Exactly-once processing** guarantees for message handling

---

## 2. System Components

### 2.1 Entry Agent (Alfred Slack Bot)

- **Function**: The entry point for users, typically through **Slack** commands or direct messages
- **Technology**: Built with **Slack Bolt SDK**
- **Responsibilities**:
  - Receive user input (e.g., slash commands to start new tasks)
  - Publish tasks to the **Pub/Sub** broker
  - Provide task status updates through **Slack**
  - Port: **8011**

### 2.2 Specialist Agents

#### SocialIntelligenceAgent (LangChain)
- **Function**: Process data related to trend analysis, social monitoring, and sentiment analysis
- **Technology**: Uses **LangChain** for orchestration with **LangGraph** for complex workflows
- **Intents**: TREND_ANALYSIS, SOCIAL_MONITOR, SENTIMENT_ANALYSIS
- **YouTube Workflows**: 
  - *Niche-Scout* – identify trending niches
  - *Seed-to-Blueprint* – generate channel strategy & roadmap
- **Storage**: Vector storage with Qdrant + pgvector
- **Port**: **9000**

#### LegalComplianceAgent (LangGraph)
- **Function**: Handles compliance updates and regulatory analysis
- **Technology**: Uses **LangGraph** for reasoning and **LangChain** for summarization
- **Intents**: COMPLIANCE_CHECK, REGULATION_SCAN, POLICY_UPDATE_CHECK, LEGAL_RISK_ASSESSMENT
- **Multi-jurisdiction support**: US, EU, UK, CA, AU, SG, JP, IN
- **Port**: **9002**

#### FinancialTaxAgent
- **Function**: Provides tax estimates and financial analysis
- **Technology**: Uses **LangChain** for orchestrating data processing steps
- **Status**: Under development
- **Port**: **9003** (planned)

### 2.3 Pub/Sub Layer (Event Spine)

- **Function**: Messaging backbone for agent communication
- **Technology**: **Google Cloud Pub/Sub** (emulator for local development)
- **Topics**:
  - `a2a.tasks.create`: For task creation and distribution
  - `a2a.tasks.completed`: For task completion notifications
- **Dead-Letter Queue (DLQ)**: For failed task handling
- **Exactly-once processing**: Prevents duplicate task execution

### 2.4 State & Task Storage (Supabase)

- **Function**: Store agent state and task-related data
- **Technology**: **Supabase PostgreSQL** with **pgvector**
- **Components**:
  - PostgreSQL v15.1.0.117
  - Supabase Auth v2.132.3 (JWT authentication)
  - Supabase REST API v11.2.0 
  - Supabase Realtime v2.25.35 (WebSocket connections)
  - Supabase Storage v0.43.11 (File management)
- **Responsibilities**:
  - Task state management
  - Vector embeddings (pgvector)
  - Authentication
  - Real-time status updates

### 2.5 Vector Search (Qdrant)

- **Function**: Fast vector-based search for embeddings
- **Technology**: **Qdrant v1.7.4**
- **Responsibilities**:
  - Store embeddings from AI model outputs
  - Perform similarity searches
  - Support clustering and relationship analysis

### 2.6 Observability & Monitoring

- **Technology Stack**:
  - **Prometheus v2.48.1**: Metrics collection
  - **Grafana v10.2.3**: Dashboard visualization
  - **LangSmith**: Debugging and performance monitoring
  - **Node Exporter v1.7.0**: System metrics
  - **Postgres Exporter v0.15.0**: Database metrics
- **Dashboards**:
  - Alfred Platform Overview
  - Financial-Tax Agent Dashboard
  - Alfred Platform Service Health
  - Alfred Agent Comparison Dashboard

## 3. Core Libraries

### 3.1 A2A Adapter Library

The A2A (Agent-to-Agent) adapter library handles message envelope creation, validation, and processing:

```python
# libs/pubsub_adapter/envelope.py
from pydantic import BaseModel, Field

class Artifact(BaseModel):
    key: str
    uri: str

class A2AEnvelope(BaseModel):
    intent: str
    role: str
    artifacts: list[Artifact] = Field(default_factory=list)
    trace_id: str
    correlation_id: str | None = None
```

### 3.2 Exactly-Once Handler

Ensures messages are processed exactly once through Supabase database table:

```sql
-- Supabase migration file
create table processed_msgs (
  message_id  text primary key,
  processed_at timestamp default now()
);
create index on processed_msgs (processed_at);
```

```python
async def already_seen(conn, message_id: str) -> bool:
    try:
        await conn.execute(
            "insert into processed_msgs(message_id) values($1) on conflict do nothing",
            message_id,
        )
        return False
    except asyncpg.UniqueViolationError:
        return True
```

A daily Supabase `cron` job deletes rows older than 48 hours to keep the table slim.

### 3.3 Policy Middleware

Middleware applied before LangChain chain execution:

- PII scrubbing (regex patterns)
- Rate limiting per `slack_user_id` via Redis counters
- Content moderation (profanity filter)

### 3.4 Tracing & Evaluation

OpenTelemetry integration with LangSmith:

```python
import opentelemetry.trace as ot

tracer = ot.get_tracer("alfred")
with tracer.start_as_current_span("pubsub_handler", attributes={"trace_id": trace_id}):
    # Processing logic here
```

## 4. System Data Flow

### 4.1 Task Creation and Execution Flow

1. **User Input (Slack)**:
   - User sends a command to Alfred Slack Bot
2. **Task Published to Pub/Sub**:
   - Alfred publishes a message to `a2a.tasks.create` with A2A envelope
3. **Specialist Agent Subscription**:
   - Relevant agent subscribes and processes based on intent
4. **Processing & Storage**:
   - Agent processes task and stores results in Supabase and Qdrant
5. **Task Completion**:
   - Agent publishes to `a2a.tasks.completed` with results
6. **State & Real-Time Updates**:
   - Updates pushed to Mission Control UI via Supabase Realtime
7. **Task Completion Notification**:
   - User notified via Slack or Mission Control UI

### 4.2 Error Handling & Retry Logic

- Tasks that fail are retried with exponential backoff
- Tasks that fail repeatedly are sent to Dead-Letter Queue (DLQ)
- Monitoring alerts trigger on queue backlogs

### 4.3 Agent Card Generation

```python
def generate_agent_card(agent_class):
    return {
        "schema_version": "0.4",
        "name": agent_class.__name__,
        "intents": agent_class.supported_intents,
        "role": agent_class.role,
        "endpoints": {
            "health": f"http://{agent_class.host}:{agent_class.port}/health"
        }
    }
```

## 5. System Design Considerations

### 5.1 Scalability

- **Horizontal Scaling**: Each agent scales independently
- **Pub/Sub**: Cloud-managed message broker with auto-scaling
- **Containerization**: Docker-based deployment for consistent scaling
- **Autoscale Guard**: Cloud Run with `maxInstances=20`, `minInstances=0`

### 5.2 Fault Tolerance

- **Retries & DLQ**: Automatic retries before Dead-Letter Queue
- **Idempotency**: Unique `task_id` ensures exactly-once processing
- **State Management**: Persistent state in Supabase

### 5.3 Security

- **Authorization**: JWT-based authentication
- **Encryption**: Data encrypted at rest (Supabase/Qdrant) and in transit (TLS)
- **PII Handling**: Automatic scrubbing via Policy Middleware
- **Rate Limiting**: Prevents abuse by limiting requests per user

## 6. CI/CD and Development

### 6.1 CI/CD Pipelines

- **Unit tests** (`pytest -m fast`) run on every PR
- **Smoke test** GitHub Actions job:
  1. `docker compose up -d supabase pubsub-emulator agents`
  2. Publish sample `a2a.tasks.create`
  3. Assert a `tasks.completed` arrives within 20 seconds

### 6.2 Monitoring and Alerts

- PromQL alert: `pubsub.subscription.num_undelivered_messages > 1_000 for 5m`
- Health checks on all agent endpoints
- Grafana dashboards for real-time monitoring

## 7. Future Extensions

### 7.1 Vertex AI Engine Integration

A `make spike-vertex` target that:
- Builds an agent image with minimal shim (`gunicorn main:app`)
- Deploys to Vertex AI Agent Builder for cost-vs-latency metrics
- Publishes result to BigQuery for side-by-side comparison

### 7.2 Modular Agent Framework

- New agents can be added by implementing the A2A envelope schema
- Pub/Sub topics can be extended for new message types
- Architecture supports plug-and-play integration of new capabilities

---

## Conclusion

This Technical Architecture Document outlines the Alfred Agent Platform v2, designed with modularity, scalability, and fault tolerance as core principles. The event-driven architecture with Pub/Sub, combined with state management in Supabase and vector search in Qdrant, creates a robust foundation for AI agent interactions.

The platform supports real-time monitoring, end-to-end tracing, and a plug-and-play agent framework that allows easy extension with new capabilities while maintaining system integrity.