# API Standards

**Last Updated:** 2025-05-12  
**Owner:** API Team  
**Status:** Active

## Overview

The Alfred Agent Platform v2 API Standards document defines the guidelines, conventions, and best practices for designing, implementing, and maintaining APIs across the platform. These standards ensure consistency, interoperability, security, and maintainability of all APIs, creating a unified developer experience while enabling seamless integration between components.

These standards cover RESTful API design, Agent-to-Agent (A2A) communication protocol, error handling, security measures, documentation requirements, and versioning strategies. They serve as the authoritative source for API development across the platform, ensuring all agents and services communicate effectively and maintain a high quality of service.

## Project Metadata

| Attribute | Value |
|-----------|-------|
| Status | Active |
| Start Date | 2025-05-01 |
| Target Completion | 2025-07-18 |
| Current Phase | Documentation Standardization |
| Repository | https://github.com/org/alfred-agent-platform-v2 |

## Key Components

### REST API Standards

Defines the conventions for RESTful API design, including resource naming, HTTP methods usage, request/response formats, status codes, filtering, pagination, and sorting strategies.

### Agent-to-Agent Protocol

Specifies the standardized envelope-based messaging format that enables agent-to-agent communication, including message structure, transport mechanisms, reliability guarantees, and security measures.

### Documentation Standards

Outlines the requirements for API documentation, including OpenAPI specifications, reference documentation, usage examples, and changelog maintenance.

### Versioning Strategy

Defines the approach to API versioning, compatibility requirements, and deprecation policies to ensure smooth transitions between API versions.

### Security Requirements

Specifies the security measures required for all platform APIs, including authentication, authorization, encryption, and data protection practices.

## Agent Integration

This project defines standards for all agents within the platform:

| Agent | Role in Project | Integration Point |
|-------|----------------|-------------------|
| Social Intelligence Agent | Consumer/Producer | Follows A2A protocol standards for message exchange |
| Financial-Tax Agent | Consumer/Producer | Exposes REST API following platform standards |
| Legal Compliance Agent | Consumer/Producer | Provides APIs adhering to platform documentation standards |

## Workflows

This project includes the following workflows:

| Workflow | Purpose | Documentation |
|----------|---------|---------------|
| API Design Review | Validate new API designs against standards | [API Design Review Process](../../workflows/api-design-review-workflow.md) |
| API Documentation Generation | Generate API documentation from code | [Documentation Generation Workflow](../../workflows/api-docs-generation-workflow.md) |

## Technical Stack

### Core Technologies

- **OpenAPI 3.0**: Standard specification for RESTful API documentation
- **JSON Schema**: For validating API request/response payloads
- **JWT (JSON Web Tokens)**: For API authentication and authorization
- **Google Cloud Pub/Sub**: Primary transport mechanism for A2A communication
- **Supabase Realtime**: Secondary transport mechanism for A2A communication

### External Dependencies

- **Swagger UI**: For interactive API documentation presentation
- **Postman**: For API testing and collection sharing
- **GitHub Actions**: For automated API linting and documentation generation

## REST API Design Standards

### Resource Naming Conventions

Resources should use noun-based naming with consistent pluralization:

- Use plural nouns for collection resources: `/tasks`, `/agents`, `/workflows`
- Use specific identifiers for single resources: `/tasks/{task_id}`, `/agents/{agent_id}`
- Use hierarchical relationships for nested resources: `/agents/{agent_id}/tasks`
- Use kebab-case for multi-word resource names: `/tax-calculations`, `/workflow-templates`

### HTTP Methods

Use HTTP methods according to their standardized semantics:

| Method | Usage | Safe | Idempotent | Examples |
|--------|-------|------|------------|----------|
| GET | Resource retrieval | Yes | Yes | `GET /agents`, `GET /tasks/{id}` |
| POST | Resource creation | No | No | `POST /tasks`, `POST /analyses` |
| PUT | Full resource update | No | Yes | `PUT /agents/{id}`, `PUT /workflows/{id}` |
| PATCH | Partial resource update | No | No | `PATCH /tasks/{id}`, `PATCH /agents/{id}` |
| DELETE | Resource deletion | No | Yes | `DELETE /tasks/{id}` |

### URL Structure

URLs should follow a consistent structure:

```
https://api.alfred-platform.com/v{major-version}/{resource}/{resource-id}/{sub-resource}
```

Examples:
- `https://api.alfred-platform.com/v1/agents/social-intelligence`
- `https://api.alfred-platform.com/v1/tasks/f47ac10b-58cc/results`

### Request Parameters

- **Path Parameters**: Used for identifying specific resources
  ```
  /tasks/{task_id}
  ```

- **Query Parameters**: Used for filtering, pagination, sorting
  ```
  /tasks?status=completed&created_after=2025-01-01&sort=created_at:desc
  ```

- **Request Body**: Used for creating or updating resources (JSON format)

### Response Format

All API responses must follow this consistent JSON structure:

```json
{
  "data": {
    // Main response data (object or array)
  },
  "meta": {
    "pagination": {
      "current_page": 1,
      "total_pages": 10,
      "total_items": 100,
      "items_per_page": 10
    },
    "processing_time": "120ms"
  },
  "links": {
    "self": "https://api.alfred-platform.com/v1/tasks?page=1",
    "next": "https://api.alfred-platform.com/v1/tasks?page=2",
    "prev": null
  }
}
```

### HTTP Status Codes

APIs must use appropriate HTTP status codes to indicate request results:

| Status Code | Description | Usage |
|-------------|-------------|-------|
| 200 OK | Request succeeded | Successful GET, PUT, PATCH, DELETE |
| 201 Created | Resource created | Successful POST that creates a resource |
| 204 No Content | Success with no response body | Successful DELETE or PUT with no response |
| 400 Bad Request | Invalid request | Request validation failed |
| 401 Unauthorized | Missing authentication | Authentication required but missing |
| 403 Forbidden | Authentication succeeded but insufficient permissions | Authenticated user lacks permission |
| 404 Not Found | Resource not found | Resource with specified ID doesn't exist |
| 409 Conflict | Request conflicts with current state | Resource already exists or version conflict |
| 422 Unprocessable Entity | Validation failed | Request format correct but content invalid |
| 429 Too Many Requests | Rate limit exceeded | Client has sent too many requests |
| 500 Internal Server Error | Server error | Unexpected server-side error |
| 503 Service Unavailable | Service temporarily unavailable | Service overloaded or down for maintenance |

### Error Handling

All error responses must follow this consistent format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid parameters",
    "details": [
      {
        "field": "income",
        "message": "Income must be a positive number"
      }
    ],
    "request_id": "req_123456",
    "documentation_url": "https://docs.alfred-platform.com/errors/VALIDATION_ERROR"
  }
}
```

### Filtering, Pagination, and Sorting

- **Filtering**: Use query parameters with field names
  ```
  /tasks?status=completed&priority=high
  ```

- **Pagination**: Use `page` and `per_page` parameters
  ```
  /tasks?page=2&per_page=25
  ```

- **Sorting**: Use `sort` parameter with field:direction format
  ```
  /tasks?sort=created_at:desc,priority:asc
  ```

## Agent-to-Agent (A2A) Communication Protocol Standards

The A2A Protocol is a standardized messaging format for agent communication, following these key standards:

### Envelope Structure

All A2A messages must use this envelope structure:

```json
{
  "envelope": {
    "metadata": {
      "id": "uuid",
      "version": "semantic-version",
      "timestamp": "ISO8601-datetime",
      "correlation_id": "uuid",
      "trace_id": "uuid"
    },
    "routing": {
      "source": {
        "agent_id": "string",
        "service_id": "string"
      },
      "destination": {
        "agent_id": "string",
        "service_id": "string"
      },
      "reply_to": "topic-name"
    },
    "security": {
      "auth_token": "jwt",
      "signature": "hmac-sha256",
      "tenant_id": "string"
    }
  },
  "message": {
    "type": "message-type",
    "intent": "operation-intent",
    "payload": {}
  }
}
```

### Message Types

The following message types are standardized:

| Type | Description | Transport Topic |
|------|-------------|----------------|
| TASK_REQUEST | Request for an agent to perform a task | a2a.tasks.create |
| TASK_RESPONSE | Response with task results | a2a.tasks.completed |
| EVENT | Notification of an occurrence | a2a.events |
| HEARTBEAT | Agent availability signal | a2a.heartbeats |
| DISCOVERY | Service discovery message | a2a.discovery |
| CONTROL | System control message | a2a.control |

### Transport Mechanisms

- **Primary**: Google Cloud Pub/Sub
  - Topic naming convention: `a2a.[message_type].[optional_subtype]`
  - Examples: `a2a.tasks.create`, `a2a.events.system`

- **Secondary**: Supabase Realtime
  - Channel naming convention: `a2a:[message_type]:[optional_subtype]`
  - Examples: `a2a:tasks:create`, `a2a:events:system`

### Error Handling

A2A error responses use standardized format and error codes:

```json
{
  "envelope": { /* standard envelope */ },
  "message": {
    "type": "TASK_RESPONSE",
    "intent": "[original intent]",
    "payload": {
      "status": "ERROR",
      "error": {
        "code": "error-code",
        "message": "error description",
        "details": {}
      },
      "original_request": {}
    }
  }
}
```

| Error Code | Description | HTTP Equivalent |
|------------|-------------|----------------|
| INVALID_REQUEST | Malformed request | 400 |
| UNAUTHORIZED | Authentication failed | 401 |
| FORBIDDEN | Authorization failed | 403 |
| NOT_FOUND | Requested resource not found | 404 |
| INTENT_NOT_SUPPORTED | Agent doesn't support intent | 405 |
| TIMEOUT | Processing timed out | 408 |
| INTERNAL_ERROR | Agent internal error | 500 |
| SERVICE_UNAVAILABLE | Agent service unavailable | 503 |

## API Documentation Standards

### OpenAPI Specification

All REST APIs must be documented using OpenAPI 3.0 specification:

- Each API must have a YAML or JSON OpenAPI 3.0 document
- The specification must be kept in sync with the actual implementation
- The specification must include all endpoints, parameters, request bodies, and responses
- The specification should include examples for all operations

### Required Documentation Sections

API documentation must include:

1. **Overview**: Brief description and purpose of the API
2. **Authentication**: Authentication methods and requirements
3. **Endpoints**: All available endpoints with parameters and responses
4. **Error Codes**: All possible error codes with descriptions
5. **Examples**: Request and response examples for each endpoint
6. **Rate Limits**: Any applicable rate limits or quotas
7. **Changelog**: Documentation version history

### Code Examples

Documentation must include code examples in at least two languages:

1. Python (using requests library)
2. JavaScript (using fetch API or axios)

### Versioning and Changelog

All API documentation must maintain a changelog that includes:

- Version number
- Release date
- Changes (added, modified, deprecated, removed)
- Migration guide for breaking changes

## API Versioning Strategy

### Version Scheme

APIs follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible changes that require client updates
- **MINOR**: Backward-compatible new features
- **PATCH**: Backward-compatible bug fixes

### Version Communication

REST APIs communicate version in the URL path:
```
https://api.alfred-platform.com/v1/tasks
```

A2A protocol includes version in the envelope metadata:
```json
"metadata": {
  "version": "2.1.0"
}
```

### Compatibility Requirements

- Minor and patch versions must maintain backward compatibility
- Breaking changes require a new major version
- APIs must support at least one previous major version for 6 months

### Deprecation Policy

- Deprecated features must be marked in documentation
- Deprecation notices must be included in API responses
- Deprecated features must be supported for at least 6 months
- Sunset dates must be communicated at least 3 months in advance

## Security Requirements

### Authentication

All APIs must implement one of these authentication methods:

1. **JWT-based Bearer Token**: Required for all REST APIs
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

2. **API Keys**: For simple internal services
   ```
   X-API-Key: api_key_xyz123
   ```

3. **OAuth 2.0**: For third-party integration

### Authorization

- All APIs must implement role-based access control (RBAC)
- Multi-tenant isolation must be enforced at the API level
- Authorization checks must be performed for every request

### Transport Security

- All API communications must use TLS 1.2+
- HTTP Strict Transport Security (HSTS) must be enabled
- Certificate pinning should be implemented for mobile clients

### Data Protection

- Sensitive data must be encrypted in transit and at rest
- PII must be handled according to platform data protection policies
- Rate limiting must be implemented to prevent abuse

## Implementation Examples

### REST API Controller Example (Python - FastAPI)

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

router = APIRouter(prefix="/tasks", tags=["Tasks"])

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    priority: str = Field(..., regex="^(low|medium|high)$")
    due_date: Optional[str] = Field(None, regex="^\\d{4}-\\d{2}-\\d{2}$")

class Task(BaseModel):
    id: UUID
    title: str
    description: str
    priority: str
    status: str
    created_at: str
    updated_at: str
    due_date: Optional[str] = None

class TaskList(BaseModel):
    data: List[Task]
    meta: dict
    links: dict

@router.get("/", response_model=TaskList)
async def list_tasks(
    status: Optional[str] = Query(None, regex="^(pending|in_progress|completed)$"),
    priority: Optional[str] = Query(None, regex="^(low|medium|high)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at:desc")
):
    """
    List tasks with optional filtering, pagination, and sorting.
    """
    # Implementation omitted
    return {
        "data": [
            # Task objects
        ],
        "meta": {
            "pagination": {
                "current_page": page,
                "total_pages": 5,
                "total_items": 100,
                "items_per_page": per_page
            }
        },
        "links": {
            "self": f"/tasks?page={page}&per_page={per_page}",
            "next": f"/tasks?page={page+1}&per_page={per_page}" if page < 5 else None,
            "prev": f"/tasks?page={page-1}&per_page={per_page}" if page > 1 else None
        }
    }

@router.post("/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """
    Create a new task.
    """
    # Implementation omitted
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": "pending",
        "created_at": "2025-05-12T10:30:00Z",
        "updated_at": "2025-05-12T10:30:00Z",
        "due_date": task.due_date
    }

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: UUID):
    """
    Get a specific task by ID.
    """
    # Implementation omitted
    return {
        "id": task_id,
        "title": "Example Task",
        "description": "This is an example task",
        "priority": "high",
        "status": "pending",
        "created_at": "2025-05-12T10:30:00Z",
        "updated_at": "2025-05-12T10:30:00Z",
        "due_date": "2025-06-01"
    }
```

### A2A Protocol Implementation Example (JavaScript)

```javascript
const { PubSub } = require('@google-cloud/pubsub');
const { v4: uuidv4 } = require('uuid');

class A2AProtocol {
  constructor(agentId, serviceId, authToken) {
    this.agentId = agentId;
    this.serviceId = serviceId;
    this.authToken = authToken;
    this.pubsub = new PubSub();
  }
  
  createEnvelope(destinationAgent, destinationService = null) {
    return {
      metadata: {
        id: uuidv4(),
        version: '2.1.0',
        timestamp: new Date().toISOString(),
        correlation_id: uuidv4(),
        trace_id: uuidv4()
      },
      routing: {
        source: {
          agent_id: this.agentId,
          service_id: this.serviceId
        },
        destination: {
          agent_id: destinationAgent,
          service_id: destinationService
        },
        reply_to: `a2a.tasks.completed.${this.agentId}`
      },
      security: {
        auth_token: this.authToken,
        signature: null,
        tenant_id: 'default'
      }
    };
  }
  
  createTaskRequest(destinationAgent, intent, payload, destinationService = null) {
    const envelope = this.createEnvelope(destinationAgent, destinationService);
    const message = {
      type: 'TASK_REQUEST',
      intent: intent,
      payload: payload
    };
    return { envelope, message };
  }
  
  async sendMessage(message, topic) {
    const messageJson = JSON.stringify(message);
    const messageBuffer = Buffer.from(messageJson);
    const messageId = await this.pubsub.topic(topic).publish(messageBuffer);
    return messageId;
  }
}

module.exports = A2AProtocol;
```

## Testing and Validation

### API Testing Requirements

APIs must include these test types:

1. **Unit Tests**: For individual endpoint logic
2. **Integration Tests**: For API interactions with other components
3. **Contract Tests**: Verifying API adheres to specification
4. **Performance Tests**: Validating response times and throughput
5. **Security Tests**: Checking for vulnerabilities

### Validation Tools

These tools must be used for API validation:

- **JSON Schema**: For validating request/response payloads
- **Spectral**: For linting OpenAPI specifications
- **Postman Collections**: For API testing and documentation

## Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| REST API Standards | Completed | Fully documented and implemented |
| A2A Protocol | Completed | v2.1.0 released and in use |
| Documentation Standards | In Progress | Template implementation ongoing |
| Versioning Strategy | Completed | Implemented across all APIs |
| Security Requirements | Completed | Applied to all existing APIs |

## Operations

### Monitoring Requirements

All APIs must implement these monitoring capabilities:

- Request volume metrics
- Response time metrics (average, p95, p99)
- Error rate metrics (by status code)
- Custom business metrics for key operations

### Rate Limiting

APIs must implement rate limiting based on:

- Per-client limits (requests per minute)
- Burst allowances for occasional spikes
- Tiered limits based on client type

### Scaling Considerations

- APIs should be stateless to enable horizontal scaling
- Resource-intensive operations should be asynchronous
- Cache frequently accessed, rarely changing resources

## Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Response Time (p95) | < 200ms | 180ms |
| Availability | 99.95% | 99.97% |
| Error Rate | < 0.5% | 0.3% |
| Throughput | 1000 req/s | 850 req/s |

## Security and Compliance

### Security Considerations

- All APIs must pass OWASP Top 10 security review
- Authentication tokens must expire after 24 hours
- Sensitive operations must use multi-factor authentication
- APIs must not expose internal implementation details

### Compliance Requirements

- APIs must maintain audit logs for all operations
- PII handling must comply with GDPR and CCPA requirements
- All APIs must pass compliance review before production deployment

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking changes | High | Medium | Strict version compatibility testing |
| API throttling | Medium | High | Implement backoff strategies and rate limit notifications |
| Security vulnerabilities | High | Low | Regular security audits and penetration testing |
| Performance degradation | Medium | Medium | Performance monitoring and autoscaling |

## Future Roadmap

- Implement GraphQL API for complex data queries
- Enhance A2A protocol with bidirectional streaming
- Add comprehensive API analytics dashboard
- Support WebSocket for real-time notifications

## Related Documentation

- [A2A Protocol Guide](../../api/a2a-protocol.md)
- [Project Integration Guide](./project-integration-guide-migrated.md)
- [Development Guidelines](./development-guidelines-migrated.md)
- [Security Implementation Guide](../architecture/security-architecture.md)

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [JSON:API Specification](https://jsonapi.org/)
- [OAuth 2.0 Framework](https://oauth.net/2/)
- [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3)