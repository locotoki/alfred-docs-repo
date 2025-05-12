#!/usr/bin/python3
"""
Create detailed inventory files for each phase of the migration.
"""
import os
import csv
import sys
import json
from datetime import datetime

# Define the phases and their directories
PHASES = {
    "phase3": {
        "name": "Agent Documentation",
        "directories": ["agents", "agent-orchestrator", "alfred_assistant_implementation"],
        "start_date": "2025-06-12",
        "end_date": "2025-06-19"
    },
    "phase4": {
        "name": "Workflow & API Documentation",
        "directories": ["workflows", "api", "integrations", "interfaces"],
        "start_date": "2025-06-20",
        "end_date": "2025-06-27"
    },
    "phase5": {
        "name": "Service & Operations Documentation",
        "directories": ["services", "operations", "monitoring", "infrastructure-crew", "llm"],
        "start_date": "2025-06-30",
        "end_date": "2025-07-04"
    },
    "phase6": {
        "name": "Verification & Gap Filling",
        "directories": ["staging-area", "architecture", "project", "development", "tools", 
                        "governance", "examples", "templates", "family-user-management"],
        "start_date": "2025-07-07",
        "end_date": "2025-07-11"
    },
    "phase7": {
        "name": "Final Review & Launch",
        "directories": ["root"],
        "start_date": "2025-07-14",
        "end_date": "2025-07-18"
    }
}

def create_phase_inventories(mapping_file, output_dir):
    """Create inventory files for each phase."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the mapping file
    with open(mapping_file, 'r', newline='') as f:
        rows = list(csv.DictReader(f))
    
    # Create inventory for each phase
    for phase_id, phase_info in PHASES.items():
        phase_files = []
        
        # Filter files for this phase
        for row in rows:
            rel_path = row['original_relpath']
            parts = rel_path.split('/')
            
            # Determine directory
            if len(parts) > 1:
                directory = parts[0]
            else:
                directory = 'root'
            
            # Check if file belongs to this phase
            if directory in phase_info['directories']:
                # Add to phase files
                phase_files.append({
                    "source_path": row['original_path'],
                    "source_relpath": row['original_relpath'],
                    "target_path": "",  # To be determined
                    "normalized_name": row['normalized_filename'],
                    "directory": directory,
                    "filename": row['filename'],
                    "status": "Not Started",
                    "processing_type": "Migrate",  # Default
                    "assigned_to": "Documentation Team",
                    "deadline": phase_info['end_date'],
                    "notes": ""
                })
        
        # Create inventory file
        phase_md = f"# {phase_info['name']} Inventory\n\n"
        phase_md += f"**Phase:** {phase_id.capitalize()}\n"
        phase_md += f"**Start Date:** {phase_info['start_date']}\n"
        phase_md += f"**End Date:** {phase_info['end_date']}\n"
        phase_md += f"**Total Documents:** {len(phase_files)}\n\n"
        
        phase_md += "## Documents to Process\n\n"
        phase_md += "| Source Path | Directory | Status | Processing Type | Assigned To | Deadline |\n"
        phase_md += "|-------------|-----------|--------|----------------|-------------|----------|\n"
        
        for file in phase_files:
            phase_md += f"| {file['source_relpath']} | {file['directory']} | {file['status']} | {file['processing_type']} | {file['assigned_to']} | {file['deadline']} |\n"
        
        # Write to file
        output_file = os.path.join(output_dir, f"{phase_id}_inventory.md")
        with open(output_file, 'w') as f:
            f.write(phase_md)
        
        # Also save as JSON for programmatic use
        json_file = os.path.join(output_dir, f"{phase_id}_inventory.json")
        with open(json_file, 'w') as f:
            json.dump({
                "phase_id": phase_id,
                "name": phase_info['name'],
                "start_date": phase_info['start_date'],
                "end_date": phase_info['end_date'],
                "total_documents": len(phase_files),
                "documents": phase_files
            }, f, indent=2)
        
        print(f"Created {phase_id} inventory with {len(phase_files)} documents in {output_file}")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <mapping_file> <output_dir>")
        sys.exit(1)
    
    mapping_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    create_phase_inventories(mapping_file, output_dir)

if __name__ == "__main__":
    main()