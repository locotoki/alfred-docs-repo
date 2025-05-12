# Testing Standards

**Last Updated:** 2025-05-14  
**Owner:** Documentation Team  
**Status:** Active

## Overview

This document establishes the testing standards for the Alfred Agent Platform v2. It provides comprehensive guidelines for all types of testing, from unit tests to end-to-end testing, including best practices, tools, and code examples. These standards ensure consistency, quality, and reliability across all components of the platform.

## Testing Requirements

### Coverage Targets

- **Minimum Code Coverage**: 80% across all components
- **Critical Path Coverage**: 95% for core functionality and critical paths
- **Agent Coverage**: 85% for agent implementations
- **API Coverage**: 90% for all public APIs

### Required Test Types

| Test Type | Requirement | Purpose | Tools |
|-----------|-------------|---------|-------|
| Unit Tests | Required for all components | Test individual functions and classes in isolation | pytest, unittest |
| Integration Tests | Required for all services | Test component interactions and workflows | pytest, requests, mock |
| End-to-End Tests | Required for critical workflows | Test complete user journeys | pytest, Selenium, Cypress |
| Load Tests | Required for API endpoints | Verify performance under load | Locust, Apache JMeter |
| Security Tests | Required for authentication flows | Verify security measures | OWASP ZAP, Burp Suite |

### Test Organization

- Tests must mirror the application structure
- Group tests by module/component
- Use descriptive test names that explain what is being tested
- Use fixtures for test setup

```
/tests
├── unit/
│   ├── agents/
│   │   ├── test_social_intelligence.py
│   │   └── test_financial_tax.py
│   └── core/
│       ├── test_a2a_protocol.py
│       └── test_pubsub.py
├── integration/
│   ├── test_agent_pubsub.py
│   └── test_supabase_storage.py
└── e2e/
    ├── test_workflows.py
    └── test_api_endpoints.py
```

## Unit Testing

### Principles

1. **Isolation**: Test functions and classes in isolation
2. **Independence**: Tests should not depend on other tests
3. **Speed**: Unit tests should execute quickly (milliseconds)
4. **Mocking**: External dependencies should be mocked
5. **Coverage**: Focus on business logic, edge cases, and error handling

### Unit Test Structure

Follow the Arrange-Act-Assert (AAA) pattern:

```python
def test_process_user_data_updates_preferences():
    # Arrange
    profile = UserProfile(
        user_id="user123",
        name="Test User",
        email="test@example.com",
        preferences={"notify": "true"},
        roles=["user"]
    )
    
    # Act
    result = process_user_data(profile, update_preferences=True)
    
    # Assert
    assert result.preferences["theme"] == "dark"
    assert result.preferences["notify"] == "true"
```

### Using Fixtures

Use fixtures for reusable test setup:

```python
@pytest.fixture
def mock_pubsub():
    return MagicMock()

@pytest.fixture
def mock_supabase():
    return MagicMock()

@pytest.fixture
def agent(mock_pubsub, mock_supabase, mock_policy):
    return YourAgentName(
        pubsub_transport=mock_pubsub,
        supabase_transport=mock_supabase,
        policy_middleware=mock_policy
    )
```

### Mocking External Services

Mock external dependencies to isolate unit tests:

```python
@pytest.mark.asyncio
async def test_process_task(agent):
    # Create test envelope
    envelope = A2AEnvelope(
        intent="YOUR_INTENT_1",
        content={
            "field1": "test value",
            "field2": 42,
            "option": "option_a"
        }
    )
    
    # Mock chain response
    with patch.object(agent.custom_chain_1, 'process') as mock_process:
        mock_process.return_value = YourResponseModel1(
            result_field1="result",
            result_field2=3.14,
            status="success",
            details=[{"key": "value"}],
            timestamp="2025-05-01T12:00:00Z"
        )
        
        # Process task
        result = await agent.process_task(envelope)
        
        # Assert result
        assert result["status"] == "success"
        assert result["intent"] == "YOUR_INTENT_1"
        assert "result" in result
```

## Integration Testing

### Principles

1. **Component Interactions**: Test how components work together
2. **Real Dependencies**: Use real dependencies when practical
3. **Test Environment**: Use test databases and emulators
4. **Tagging**: Tag integration tests appropriately (`@pytest.mark.integration`)

### Integration Test Structure

```python
@pytest.mark.integration
async def test_task_creation_persists_to_database():
    # Arrange
    task_service = TaskService(db_connection)
    task_data = {"title": "Test Task", "priority": 1}
    
    # Act
    created_task = await task_service.create_task(task_data)
    retrieved_task = await task_service.get_task(created_task.id)
    
    # Assert
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.id == created_task.id
```

### Testing Agent Communication

Test agent interactions through the Pub/Sub system:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_workflow():
    # Initialize real transports (using emulators)
    pubsub = PubSubTransport(project_id="test-project")
    supabase = SupabaseTransport(database_url="postgresql://user:pass@localhost:5432/postgres")
    policy = PolicyMiddleware()
    
    # Create agent
    agent = YourAgentName(
        pubsub_transport=pubsub,
        supabase_transport=supabase,
        policy_middleware=policy
    )
    
    # Start agent
    await agent.start()
    
    # Create test envelope
    envelope = A2AEnvelope(
        intent="YOUR_INTENT_1",
        content={
            "field1": "test value",
            "field2": 42,
            "option": "option_a"
        }
    )
    
    # Publish task
    await pubsub.publish_task(envelope)
    
    # Wait for processing and verify results
    await asyncio.sleep(2)
    task_result = await supabase.get_task_result(envelope.task_id)
    assert task_result["status"] == "completed"
```

## End-to-End Testing

### Principles

1. **Complete Workflows**: Test entire user journeys
2. **Real Services**: Use actual service interactions
3. **User Perspective**: Test from the user's point of view
4. **Tagging**: Tag E2E tests appropriately (`@pytest.mark.e2e`)

### E2E Test Example

```python
@pytest.mark.e2e
async def test_content_analysis_workflow():
    # Arrange
    client = TestClient(app)
    input_data = {"url": "https://example.com/article"}
    
    # Act
    response = client.post("/api/analyze", json=input_data)
    result_id = response.json()["result_id"]
    
    # Poll for completion
    status = "processing"
    for _ in range(10):
        status_response = client.get(f"/api/results/{result_id}")
        status = status_response.json()["status"]
        if status == "completed":
            break
        time.sleep(1)
    
    # Get final result
    result_response = client.get(f"/api/results/{result_id}")
    
    # Assert
    assert status == "completed"
    assert result_response.status_code == 200
    assert "sentiment" in result_response.json()
    assert "keywords" in result_response.json()
```

### E2E Test Cases

Key workflows that must have E2E test coverage:

1. **Task Lifecycle**: Complete task creation, processing, and result retrieval
2. **Agent Collaboration**: Multiple agents working together on a complex task
3. **Critical User Journeys**: Full user workflows from UI interaction to result display

## Load Testing

### Principles

1. **Performance Benchmarks**: Establish clear performance targets
2. **Realistic Scenarios**: Simulate real-world usage patterns
3. **Scaling Verification**: Test system behavior under increasing load

### Load Test Example

```python
from locust import HttpUser, task, between

class PlatformLoadTest(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def analyze_content(self):
        self.client.post("/api/analyze", json={
            "url": "https://example.com/article",
            "depth": "standard"
        })
    
    @task(3)
    def get_results(self):
        self.client.get("/api/results/latest")
```

## Security Testing

### Security Test Focus Areas

- **Authentication**: Test authentication mechanisms for all endpoints
- **Authorization**: Verify proper access controls
- **Data Protection**: Ensure sensitive data is protected
- **Input Validation**: Test for injection vulnerabilities

### Security Test Example

```python
def test_api_requires_authentication():
    # Arrange
    client = TestClient(app)
    
    # Act
    response = client.get("/api/tasks")
    
    # Assert
    assert response.status_code == 401
    
    # Act with authentication
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Assert
    assert response.status_code == 200
```

## Test Data Management

### Test Data Principles

1. **Isolation**: Test data should not affect production environments
2. **Reproducibility**: Tests should produce the same results when run multiple times
3. **Cleanup**: Tests should clean up any data they create

### Test Database Setup

```python
@pytest.fixture(scope="session")
def test_db():
    # Set up test database
    engine = create_engine("postgresql://test:test@localhost:5432/test_db")
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Cleanup
    session.close()
    Base.metadata.drop_all(engine)
```

## Continuous Integration

### CI Pipeline Requirements

1. **Automation**: All tests should run automatically on each pull request
2. **Fast Feedback**: Unit tests should run first, followed by integration and E2E tests
3. **Report Generation**: Test results should be clearly reported
4. **Coverage Reports**: Code coverage should be tracked over time

### CI Configuration Example

```yaml
name: Test Suite

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run unit tests
        run: pytest tests/unit
      - name: Run integration tests
        run: pytest tests/integration
      - name: Generate coverage report
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage report
        uses: codecov/codecov-action@v2
```

## Testing Best Practices

1. **Test Independence**: Each test should run independently of others
2. **Clear Intent**: Tests should clearly communicate what they're testing
3. **Fast Execution**: Tests should execute quickly to provide rapid feedback
4. **Deterministic Results**: Tests should produce the same results each time they're run
5. **Focus on Behavior**: Test behavior, not implementation details
6. **Realistic Data**: Use realistic test data that simulates actual usage
7. **Error Scenarios**: Test both happy path and error scenarios
8. **Readability**: Write tests that are easy to understand and maintain
9. **DRY Principles**: Use fixtures and helpers to avoid repetition
10. **Continuous Refinement**: Regularly review and improve tests

## Testing Tools and Frameworks

| Category | Tools |
|----------|-------|
| Test Framework | pytest, unittest |
| Code Coverage | pytest-cov, coverage.py |
| Mocking | unittest.mock, pytest-mock |
| API Testing | requests, httpx, pytest-httpx |
| UI Testing | Selenium, Cypress, Playwright |
| Load Testing | Locust, JMeter |
| Security Testing | OWASP ZAP, Burp Suite |
| Test Runners | tox, nox |
| CI Integration | GitHub Actions, Jenkins, CircleCI |

## Related Documentation

- [Development Guidelines](/project/development-guidelines-migrated.md)
- [Project Integration Guide](/project/project-integration-guide-migrated.md)
- [API Standards](/project/api-standards-migrated.md)
- [Agent Implementation Guide](/agents/guides/agent-implementation-guide-migrated.md)
- [Test Plan & Test Cases](/tools/outputs/test-case-inventory.md)