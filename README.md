# Alfred Documentation Repository

This repository contains documentation for the Alfred Agent Platform and its components.

**[📑 View the Complete Documentation Overview](/docs/OVERVIEW.md)**

## Contents

### Platform Documentation

- [Current Gaps and Issues](/docs/CURRENT_GAPS_AND_ISSUES.md)
- [Implementation Status](/docs/IMPLEMENTATION_STATUS.md)
- [Infrastructure Status](/docs/INFRASTRUCTURE_STATUS.md)
- [Service Containerization](/docs/SERVICE_CONTAINERIZATION.md)
- [Shared Libraries](/docs/SHARED_LIBRARIES.md)
- [Troubleshooting](/docs/TROUBLESHOOTING.md)

### Architecture & Design

- [System Design](/docs/architecture/system-design.md)
- [Technical Architecture](/docs/architecture/technical-architecture.md)
- [Re-architecture Plan](/docs/architecture/re-architecture-plan.md)
- [A2A Protocol](/docs/api/a2a-protocol.md)

### API Documentation

- [A2A Protocol](/docs/api/a2a-protocol.md)
- [API Documentation](/docs/api/api-documentation.md)

### Development

- [Master Project Plan (v1.0)](/docs/development/AI%20Agent%20Platform%20v2%20-%20Master%20Project%20Plan.md)
- [Master Project Plan (v1.1 - Latest)](/docs/development/AI%20Agent%20Platform%20v2%20-%20Master%20Project%20Plan%20v1.1.md)
- [Technical Design Guide](/docs/development/AI%20Agent%20Platform%20v2–%20Technical%20Design%20Guide.md)
- [CI/CD Pipeline](/docs/development/ci-cd-pipeline.md)
- [Test Plan & Test Cases](/docs/development/test-plan.md)
- [Agent Development](/docs/development/agent-development.md)

### Agent Orchestrator

The Agent Orchestrator is a UI service for managing agent workflows:

- [Architecture](/agent-orchestrator/ARCHITECTURE.md)
- [Features](/agent-orchestrator/FEATURES.md)
- [Theming](/agent-orchestrator/THEMING.md)
- [Update Guide](/agent-orchestrator/UPDATE-GUIDE.md)

#### Niche Idea Generator

A feature for YouTube content research:

- [Architecture](/docs/agent-orchestrator/niche_Idea_generator/architecture.md)
- [UI Lanes](/docs/agent-orchestrator/niche_Idea_generator/ui-lanes.md)
- [Taxonomy Rules](/docs/agent-orchestrator/niche_Idea_generator/taxonomy-rules.md)
- [Wizard Specs](/docs/agent-orchestrator/niche_Idea_generator/wizard-specs.md)

### Agent Core

- [Integration Plan](/docs/agent-core/integration-plan.md)
- [LangChain vs Vertex AI Tradeoffs](/docs/agent-core/langchain-vs-vertex-ai.md)

### Agents

- [Financial Tax Agent](/docs/agents/financial-tax-agent.md)
- [Deployment Checklist](/docs/agents/financial-tax-deployment-checklist.md)

### Mission Control & YouTube Workflows

- [Implementation Plan](/docs/phase6-mission-control/implementation-plan.md)
- [Requirements](/docs/phase6-mission-control/requirements.md)
- [YouTube Workflows Guide](/docs/phase6-mission-control/youtube-workflows/README.md)
- [Quick Start Guide](/docs/phase6-mission-control/youtube-workflows/quick-start-guide.md)
- [Troubleshooting Guide](/docs/phase6-mission-control/youtube-workflows/troubleshooting-guide.md)

### Operations

- [Deployment](/docs/operations/deployment.md)
- [Security Plan](/docs/operations/security-plan.md)
- [Maintenance Guide](/docs/operations/maintenance-guide.md)
- [WSL Backups](/docs/operations/wsl-backups.md)
- [Monitoring Dashboards](/docs/monitoring/dashboards.md)

## Key Documentation

The following documents serve as the single source of truth for understanding the Alfred Agent Platform:

1. **[Master Project Plan (Latest)](/docs/development/AI%20Agent%20Platform%20v2%20-%20Master%20Project%20Plan%20v1.1.md)** - Comprehensive project roadmap with completed phases, current work, and upcoming tasks
2. **[Technical Architecture](/docs/architecture/technical-architecture.md)** - Detailed architecture documentation with component descriptions and data flows
3. **[System Design](/docs/architecture/system-design.md)** - High-level architecture overview
4. **[API Documentation](/docs/api/api-documentation.md)** - Complete API specifications for platform integration
5. **[A2A Protocol](/docs/api/a2a-protocol.md)** - Details of the Agent-to-Agent communication protocol
6. **[CI/CD Pipeline](/docs/development/ci-cd-pipeline.md)** - Automated build, test, and deployment process
7. **[Test Plan & Test Cases](/docs/development/test-plan.md)** - Testing strategy and specific test cases
8. **[Infrastructure Status](/docs/INFRASTRUCTURE_STATUS.md)** - Current state of infrastructure and services
9. **[Maintenance Guide](/docs/operations/maintenance-guide.md)** - Operations procedures, troubleshooting, and maintenance tasks
10. **[Security Plan](/docs/operations/security-plan.md)** - Security controls and practices
11. **[Mission Control Implementation Plan](/docs/phase6-mission-control/implementation-plan.md)** - Plans for the central management UI
12. **[Re-architecture Plan](/docs/architecture/re-architecture-plan.md)** - Plan for updating the platform architecture using Supabase and Pub/Sub
13. **[Agent Core Integration Plan](/docs/agent-core/integration-plan.md)** - Plan for integrating LangChain, LangGraph, and LangSmith 
14. **[LangChain vs Vertex AI Tradeoffs](/docs/agent-core/langchain-vs-vertex-ai.md)** - Comparison of LangChain and Vertex AI Agent Builder

## How to Use This Repository

This documentation repository is designed to be a central reference for all Alfred platform components.
Each component has its own directory with relevant documentation files.

## Contributing

To add or update documentation:

1. Clone this repository
2. Create or update documentation files
3. Submit a pull request

Please maintain the existing directory structure and follow markdown best practices.