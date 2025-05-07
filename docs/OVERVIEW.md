# Alfred Agent Platform Documentation Overview

This page serves as a comprehensive overview and index for all Alfred Agent Platform documentation.

## Platform Architecture

The Alfred Agent Platform is built on a modern, event-driven architecture that enables scalable agent-to-agent communication.

### Core Components

1. **Agent System**
   - [Agent Core Integration Plan](/docs/agent-core/integration-plan.md) - Integration of LangChain, LangGraph, and LangSmith
   - [LangChain vs Vertex AI Tradeoffs](/docs/agent-core/langchain-vs-vertex-ai.md) - Analysis of platform choices
   - [Financial Tax Agent](/docs/agents/financial-tax-agent.md) - Specialized agent for financial calculations
   - [Agent Development Guide](/docs/development/agent-development.md) - How to create new agents

2. **Architecture**
   - [System Design](/docs/architecture/system-design.md) - High-level architecture overview
   - [Technical Architecture](/docs/architecture/technical-architecture.md) - Detailed architecture documentation
   - [Re-architecture Plan](/docs/architecture/re-architecture-plan.md) - Plan for updating the platform with Supabase and Pub/Sub

3. **APIs & Protocols**
   - [API Documentation](/docs/api/api-documentation.md) - Complete API specifications
   - [A2A Protocol](/docs/api/a2a-protocol.md) - Agent-to-Agent communication protocol

4. **Mission Control & UI**
   - [Implementation Plan](/docs/phase6-mission-control/implementation-plan.md) - Plans for the central UI
   - [Requirements](/docs/phase6-mission-control/requirements.md) - Mission Control requirements
   - [YouTube Workflows Guide](/docs/phase6-mission-control/youtube-workflows/README.md) - Guide for YouTube content workflows

5. **Agent Orchestrator**
   - [Architecture](/agent-orchestrator/ARCHITECTURE.md) - Orchestrator architecture
   - [Features](/agent-orchestrator/FEATURES.md) - Available features
   - [Niche Idea Generator](/docs/agent-orchestrator/niche_Idea_generator/README.md) - YouTube content research tool

## Development & Operations

1. **Project Planning**
   - [Master Project Plan (Latest)](/docs/development/AI%20Agent%20Platform%20v2%20-%20Master%20Project%20Plan%20v1.1.md) - Current project roadmap
   - [Technical Design Guide](/docs/development/AI%20Agent%20Platform%20v2–%20Technical%20Design%20Guide.md) - Design principles and patterns

2. **Development Processes**
   - [CI/CD Pipeline](/docs/development/ci-cd-pipeline.md) - Automated build and deployment
   - [Test Plan & Test Cases](/docs/development/test-plan.md) - Testing strategy

3. **Operations**
   - [Deployment Guide](/docs/operations/deployment.md) - Deployment procedures
   - [Maintenance Guide](/docs/operations/maintenance-guide.md) - Ongoing maintenance tasks
   - [Security Plan](/docs/operations/security-plan.md) - Security controls and practices
   - [WSL Backups](/docs/operations/wsl-backups.md) - WSL backup procedures
   - [Monitoring Dashboards](/docs/monitoring/dashboards.md) - Platform monitoring

4. **Status & Issues**
   - [Current Gaps and Issues](/docs/CURRENT_GAPS_AND_ISSUES.md) - Known issues
   - [Implementation Status](/docs/IMPLEMENTATION_STATUS.md) - Current implementation status
   - [Infrastructure Status](/docs/INFRASTRUCTURE_STATUS.md) - Infrastructure status
   - [Service Containerization](/docs/SERVICE_CONTAINERIZATION.md) - Container status
   - [Shared Libraries](/docs/SHARED_LIBRARIES.md) - Common code libraries
   - [Troubleshooting](/docs/TROUBLESHOOTING.md) - Common issues and solutions

## Feature Areas

### YouTube Content Creation Workflow

The platform includes specialized workflows for YouTube content creation:

1. **Niche Idea Generator**
   - [Architecture](/docs/agent-orchestrator/niche_Idea_generator/architecture.md)
   - [UI Lanes](/docs/agent-orchestrator/niche_Idea_generator/ui-lanes.md)
   - [Taxonomy Rules](/docs/agent-orchestrator/niche_Idea_generator/taxonomy-rules.md)
   - [Wizard Specs](/docs/agent-orchestrator/niche_Idea_generator/wizard-specs.md)

2. **YouTube Workflows**
   - [Quick Start Guide](/docs/phase6-mission-control/youtube-workflows/quick-start-guide.md)
   - [Troubleshooting Guide](/docs/phase6-mission-control/youtube-workflows/troubleshooting-guide.md)

### Financial Services

The platform provides financial services through specialized agents:

1. **Financial Tax Agent**
   - [Documentation](/docs/agents/financial-tax-agent.md)
   - [Deployment Checklist](/docs/agents/financial-tax-deployment-checklist.md)

## Getting Started

For new developers or users, we recommend starting with these key documents:

1. [System Design](/docs/architecture/system-design.md) - Overview of the platform
2. [Technical Architecture](/docs/architecture/technical-architecture.md) - Detailed architecture
3. [Master Project Plan](/docs/development/AI%20Agent%20Platform%20v2%20-%20Master%20Project%20Plan%20v1.1.md) - Current roadmap
4. [Agent Development Guide](/docs/development/agent-development.md) - Creating new agents

For operations staff:

1. [Deployment Guide](/docs/operations/deployment.md) - How to deploy
2. [Maintenance Guide](/docs/operations/maintenance-guide.md) - Ongoing maintenance
3. [Security Plan](/docs/operations/security-plan.md) - Security measures

## Document Conventions

Documentation in this repository follows these conventions:

1. Markdown format for all documents
2. Relative links for cross-references
3. Diagrams in text format (ASCII) or SVG
4. Code examples as syntax-highlighted blocks