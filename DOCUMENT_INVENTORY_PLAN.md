# Complete Document Inventory and Migration Plan

**Date:** 2025-05-14  
**Status:** Active

## Overview

This document outlines the comprehensive approach to inventorying and migrating all markdown files from the original project folder (`/home/locotoki/projects/alfred-agent-platform-v2/docs`) to the new documentation repository. An initial analysis shows there are approximately 331 markdown files that need to be accounted for in the migration process.

## Document Inventory Process

### 1. Create Complete Inventory File

We will generate a comprehensive inventory of all markdown files in the original project directory:

```bash
# Create a directory for inventory files if it doesn't exist
mkdir -p /home/locotoki/alfred-docs-repo/inventory

# Generate complete inventory with metadata
find /home/locotoki/projects/alfred-agent-platform-v2/docs -type f -name "*.md" | \
  xargs -I{} bash -c 'echo "{} $(stat -c "%y" {})" | \
  sed "s|/home/locotoki/projects/alfred-agent-platform-v2/docs/|/docs/|g"' \
  > /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt
```

### 2. Categorize Documents

We'll categorize all documents based on their content and location:

```bash
# Create category-specific inventory files
mkdir -p /home/locotoki/alfred-docs-repo/inventory/categories

# Agent documentation
grep -i "agent" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/agent_docs.txt

# Workflow documentation
grep -i "workflow\|process" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/workflow_docs.txt

# Architecture documentation
grep -i "architect\|structure\|design" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/architecture_docs.txt

# API documentation
grep -i "api\|protocol\|interface" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/api_docs.txt

# Infrastructure documentation
grep -i "infra\|deploy\|container" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/infrastructure_docs.txt

# Operations documentation
grep -i "operat\|monitor\|maintain" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/operations_docs.txt

# Project documentation
grep -i "project\|plan\|timeline" /home/locotoki/alfred-docs-repo/inventory/complete_document_inventory.txt > \
  /home/locotoki/alfred-docs-repo/inventory/categories/project_docs.txt
```

### 3. Map to Target Structure

For each document, we'll determine:
- Target location in new repository
- Migration status
- Consolidation candidates (for duplicate content)
- Archiving decision (for outdated content)

This mapping will be stored in a structured format:

```
/home/locotoki/alfred-docs-repo/inventory/document_mapping.csv
```

With columns:
- Source path
- Target path
- Category
- Migration status
- Migration date
- Processing decision (migrate/consolidate/archive)
- Assigned to
- Notes

### 4. Create Migration Tracking Dashboard

We'll generate a real-time dashboard showing:
- Total documents: 331
- Documents processed: [count]
- Documents migrated: [count]
- Documents consolidated: [count]
- Documents archived: [count]
- Documents pending: [count]
- Overall completion: [percentage]

## Automated Tools

To ensure no documents are missed, we'll enhance the existing migration tools:

### 1. Document Scanner

```python
#!/usr/bin/python3
"""
Document scanner that analyzes all markdown files and
extracts metadata, links, content structure, and keywords.
"""
import os
import re
import sys
import pandas as pd
from collections import defaultdict

def scan_directory(root_dir):
    """Scan directory for markdown files and analyze them."""
    documents = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                doc_info = analyze_document(filepath)
                documents.append(doc_info)
    
    return pd.DataFrame(documents)

def analyze_document(filepath):
    """Extract metadata and content information from document."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract basic info
    doc_info = {
        'filepath': filepath,
        'filename': os.path.basename(filepath),
        'size_bytes': os.path.getsize(filepath),
        'last_modified': os.path.getmtime(filepath),
    }
    
    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    doc_info['title'] = title_match.group(1) if title_match else None
    
    # Extract metadata
    doc_info['updated'] = re.search(r'Last Updated: ([\d-]+)', content) is not None
    doc_info['has_owner'] = re.search(r'Owner: (.+)', content) is not None
    doc_info['has_status'] = re.search(r'Status: (.+)', content) is not None
    
    # Count sections and links
    doc_info['section_count'] = len(re.findall(r'^## (.+)$', content, re.MULTILINE))
    doc_info['internal_links'] = len(re.findall(r'\[.+?\]\((?!http).+?\)', content))
    doc_info['external_links'] = len(re.findall(r'\[.+?\]\(http.+?\)', content))
    
    # Extract keywords based on content
    keywords = extract_keywords(content)
    doc_info['keywords'] = ', '.join(keywords)
    
    return doc_info

def extract_keywords(content):
    """Extract keywords from document content."""
    # Simplified keyword extraction - can be enhanced with NLP
    common_tech_terms = ['agent', 'workflow', 'api', 'architecture', 'infrastructure', 
                         'deploy', 'monitor', 'test', 'integration', 'security']
    
    keywords = []
    for term in common_tech_terms:
        if re.search(r'\b' + term + r'\b', content, re.IGNORECASE):
            keywords.append(term)
    
    return keywords

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python doc_scanner.py <root_directory>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    docs_df = scan_directory(root_dir)
    docs_df.to_csv("document_analysis.csv", index=False)
    print(f"Analyzed {len(docs_df)} documents.")
```

### 2. Migration Status Tracker

```python
#!/usr/bin/python3
"""
Migration status tracker that compares the source and target repositories
to identify documents that haven't been migrated yet.
"""
import os
import pandas as pd
import sys
from datetime import datetime

def create_status_report(source_dir, target_dir, output_dir):
    """Create migration status report by comparing source and target directories."""
    # Get list of markdown files in source directory
    source_files = []
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                source_files.append(os.path.join(dirpath, filename))
    
    # Get list of markdown files in target directory
    target_files = []
    for dirpath, _, filenames in os.walk(target_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                target_files.append(os.path.join(dirpath, filename))
    
    # Create dataframe with source files
    source_df = pd.DataFrame({
        'source_path': source_files,
        'filename': [os.path.basename(f) for f in source_files],
        'processed': False
    })
    
    # Check which files have been migrated (exact filename match)
    target_filenames = [os.path.basename(f) for f in target_files]
    source_df['exact_match'] = source_df['filename'].isin(target_filenames)
    
    # Check for migrated files (with -migrated suffix)
    source_df['migrated_match'] = source_df['filename'].apply(
        lambda f: f.replace('.md', '-migrated.md') in target_filenames
    )
    
    # Mark processed files
    source_df['processed'] = source_df['exact_match'] | source_df['migrated_match']
    
    # Calculate statistics
    stats = {
        'total_documents': len(source_df),
        'processed_documents': source_df['processed'].sum(),
        'unprocessed_documents': (~source_df['processed']).sum(),
        'completion_percentage': round(source_df['processed'].sum() / len(source_df) * 100, 2),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save reports
    os.makedirs(output_dir, exist_ok=True)
    source_df.to_csv(os.path.join(output_dir, 'migration_status_detailed.csv'), index=False)
    
    # Create summary report
    with open(os.path.join(output_dir, 'migration_status_summary.md'), 'w') as f:
        f.write(f"# Migration Status Summary\n\n")
        f.write(f"Generated: {stats['timestamp']}\n\n")
        f.write(f"## Progress\n\n")
        f.write(f"- Total Documents: {stats['total_documents']}\n")
        f.write(f"- Processed Documents: {stats['processed_documents']}\n")
        f.write(f"- Unprocessed Documents: {stats['unprocessed_documents']}\n")
        f.write(f"- Completion: {stats['completion_percentage']}%\n\n")
        f.write(f"## Unprocessed Documents\n\n")
        
        # List unprocessed documents
        unprocessed = source_df[~source_df['processed']]
        for _, row in unprocessed.iterrows():
            f.write(f"- {row['source_path']}\n")
    
    print(f"Migration status report generated in {output_dir}")
    return stats

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python migration_tracker.py <source_dir> <target_dir> <output_dir>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    output_dir = sys.argv[3]
    stats = create_status_report(source_dir, target_dir, output_dir)
    print(f"Completion: {stats['completion_percentage']}%")
```

## Integration with Migration Process

To ensure every document is processed, we'll modify the migration process to:

1. **Check Against Inventory**: Before each migration phase, check documents against the inventory
2. **Track Progress**: Update tracking files after each document is processed
3. **Verify Completion**: Run verification at end of each phase to ensure all targeted documents were processed

## Decision Process for Document Handling

For each document, we'll follow this decision tree:

```
START
|
+-- Is the document still relevant? 
|   |
|   +-- NO --> Is it needed for historical reference?
|   |           |
|   |           +-- YES --> Archive it in /archive directory
|   |           |
|   |           +-- NO --> Mark as "Not Required" in tracking
|   |
|   +-- YES --> Does similar document exist?
|               |
|               +-- NO --> Migrate as standalone document
|               |
|               +-- YES --> Is there unique content to preserve?
|                           |
|                           +-- YES --> Consolidate with existing document
|                           |
|                           +-- NO --> Mark as "Duplicate" in tracking
```

## Implementation Schedule

| Task | Target Date | Description |
|------|-------------|-------------|
| Generate Complete Inventory | 2025-05-15 | Create full inventory of all markdown files |
| Create Categorization | 2025-05-16 | Sort documents into categories |
| Develop Migration Map | 2025-05-18 | Map source files to target structure |
| Implement Enhanced Tools | 2025-05-20 | Deploy document scanner and tracker |
| Complete Phase 3 Planning | 2025-05-25 | Prepare detailed plan for Agent Documentation migration |
| Phase 3 Execution | 2025-06-12 - 2025-06-19 | Execute migration according to plan |

## Conclusion

By implementing this inventory and tracking approach, we'll ensure that every document is accounted for and processed appropriately. The enhanced tools will provide visibility into document status, helping us maintain high-quality documentation throughout the migration process.

The resulting inventory will serve as a master reference for the documentation team, ensuring nothing falls through the cracks as we progress through the migration phases.