# Directory Structure Analysis

This document analyzes the directory structure of the source documentation folder to help plan the migration process.

## Top-Level Directory Structure

The source documentation folder has the following top-level directories:

- `/agent-orchestrator` - Documentation related to the agent orchestration system
- `/agents` - Documentation for individual agents
- `/alfred_assistant_implementation` - Documentation for Alfred assistant implementation
- `/api` - API documentation
- `/architecture` - Architecture documentation
- `/archive` - Archived documentation
- `/assets` - Documentation assets (images, diagrams, etc.)
- `/atlas` - Atlas system documentation
- `/development` - Development guidelines and documents
- `/examples` - Example documentation
- `/family-user-management` - User management documentation
- `/governance` - Governance documentation
- `/infrastructure-crew` - Infrastructure crew documentation
- `/integrations` - Integration documentation
- `/interfaces` - Interface documentation
- `/llm` - LLM-related documentation
- `/monitoring` - Monitoring documentation
- `/operations` - Operations documentation
- `/phase2` - Phase 2 documentation
- `/phase6-mission-control` - Phase 6 mission control documentation
- `/project` - Project documentation
- `/projects` - Project-specific documentation
- `/schemas` - Schema documentation
- `/services` - Service documentation
- `/staging-area` - Staging area for documentation
- `/templates` - Documentation templates
- `/tools` - Documentation tools
- `/workflows` - Workflow documentation

## Document Count by Directory

| Directory | Document Count |
|-----------|---------------|
| agent-orchestrator | 12 |
| agents | 14 |
| alfred_assistant_implementation | 4 |
| api | 1 |
| architecture | 4 |
| atlas | 7 |
| development | 3 |
| examples | 3 |
| family-user-management | 5 |
| governance | 9 |
| infrastructure-crew | 11 |
| integrations | 1 |
| interfaces | 1 |
| llm | 3 |
| monitoring | 1 |
| operations | 3 |
| phase6-mission-control | 8 |
| project | 8 |
| root | 33 |
| services | 4 |
| staging-area | 136 |
| templates | 4 |
| tools | 44 |
| workflows | 12 |

Total documents: 331

## Document Count by Phase

| Phase | Description | Document Count |
|-------|-------------|---------------|
| Phase 2 | Core Documentation Migration | 15 (completed) |
| Phase 3 | Agent Documentation | 30 |
| Phase 4 | Workflow & API Documentation | 15 |
| Phase 5 | Service & Operations Documentation | 22 |
| Phase 6 | Verification & Gap Filling | 216 |
| Phase 7 | Final Review & Launch | 33 |

## Categorization for Migration

Based on this structure, we can categorize the documentation into the following categories for migration planning:

### Phase 2 (Core Documentation Migration) - 100% Complete

- Core Architecture Documentation
- API Documentation
- Project Documentation
- High-Priority Workflow Documentation

### Phase 3 (Agent Documentation) - Scheduled for 2025-06-12 to 2025-06-19

Priority directories:
- `/agents/**`
- `/agent-orchestrator/**`
- `/alfred_assistant_implementation/**`

### Phase 4 (Workflow & API Documentation) - Scheduled for 2025-06-20 to 2025-06-27

Priority directories:
- `/workflows/**`
- `/api/**` (remaining)
- `/integrations/**`
- `/interfaces/**`

### Phase 5 (Service & Operations Documentation) - Scheduled for 2025-06-30 to 2025-07-04

Priority directories:
- `/services/**`
- `/operations/**`
- `/monitoring/**`
- `/infrastructure-crew/**`
- `/llm/**`

### Phase 6 (Verification & Gap Filling) - Scheduled for 2025-07-07 to 2025-07-11

Focus areas:
- `/staging-area/**` - Review and process remaining documents (136 files)
- `/tools/**` - Documentation tools and outputs (44 files)
- `/architecture/**`, `/project/**`, `/development/**` - Remaining core documentation
- `/governance/**`, `/examples/**`, `/templates/**` - Supporting documentation
- Any remaining documents from other directories

### Phase 7 (Final Review & Launch) - Scheduled for 2025-07-14 to 2025-07-18

- Root directory files (33 files)
- Final verification
- Cross-reference checking
- Documentation system launch

## Detailed Inventory

For each phase, we have created a detailed inventory of files to be migrated, including:
- Source path
- Target path
- Migration status
- Processing type (migrate/consolidate/archive)
- Assigned to
- Deadline

These detailed inventories are stored in `/home/locotoki/alfred-docs-repo/inventory/phases/` for tracking purposes:

- [Phase 3 Inventory](/inventory/phases/phase3_inventory.md) - Agent Documentation (30 files)
- [Phase 4 Inventory](/inventory/phases/phase4_inventory.md) - Workflow & API Documentation (15 files)
- [Phase 5 Inventory](/inventory/phases/phase5_inventory.md) - Service & Operations Documentation (22 files)
- [Phase 6 Inventory](/inventory/phases/phase6_inventory.md) - Verification & Gap Filling (216 files)
- [Phase 7 Inventory](/inventory/phases/phase7_inventory.md) - Final Review & Launch (33 files)

## Filename Normalization

Many files in the original documentation have problematic filenames with spaces, special characters, and unusual naming patterns. To address this, we've created a normalization mapping that can be used during the migration process.

The mapping file is stored at `/home/locotoki/alfred-docs-repo/inventory/mapping/filename_mapping.csv` and contains:
- Original file path
- Normalized file path
- Original filename
- Normalized filename

This mapping will be used to ensure consistent naming in the migrated documentation.