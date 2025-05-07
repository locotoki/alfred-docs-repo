# YouTube Workflow Documentation

This directory contains comprehensive documentation and tools for implementing and maintaining the YouTube workflows in the Alfred Agent Platform v2.

## Contents

1. [Quick Start Guide](./quick-start-guide.md) - A concise overview of the project structure and implementation status
2. [Implementation Plan](./implementation-plan.md) - Detailed step-by-step guide for completing the implementation
3. [Troubleshooting Guide](./troubleshooting-guide.md) - Solutions for common issues and diagnostic procedures
4. [Environment Check Script](./environment-check-script.sh) - Bash script to automatically check for and fix common issues

## Usage

### Getting Started

If you're new to the YouTube workflow implementation, start with the Quick Start Guide to understand the project structure and current status.

### For New Sessions

Run the environment check script at the beginning of each development session:

```bash
cd /home/locotoki/projects/alfred-agent-platform-v2/docs/phase6-mission-control/youtube-workflows
chmod +x environment-check-script.sh
./environment-check-script.sh
```

This will verify your environment configuration and alert you to any issues.

### Implementing Features

Follow the Implementation Plan for a detailed guide on completing the YouTube workflow integration, including specific code changes and testing procedures.

### Troubleshooting

If you encounter issues during implementation or testing, refer to the Troubleshooting Guide for solutions to common problems.

## Document Maintenance

These documents should be treated as living documents and updated as the implementation progresses. After making significant changes to the codebase, please update the relevant documentation to reflect the current status.

## Core Workflows

1. **Niche-Scout** - Identifies trending YouTube niches based on metrics and trends
2. **Seed-to-Blueprint** - Generates YouTube channel strategies from seed videos or niches

## Key Files

- `/services/mission-control/src/services/youtube-workflows.ts` - Core service for YouTube API integration
- `/services/mission-control/src/pages/api/social-intel/niche-scout.ts` - Niche Scout API proxy
- `/services/mission-control/src/pages/api/social-intel/seed-to-blueprint.ts` - Blueprint API proxy
- `/services/mission-control/src/pages/workflows/niche-scout/index.tsx` - Niche Scout form
- `/services/mission-control/src/pages/workflows/seed-to-blueprint/index.tsx` - Blueprint form