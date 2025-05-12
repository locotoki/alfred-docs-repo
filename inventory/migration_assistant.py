#!/usr/bin/python3
"""
Migration Assistant Script to help with the document migration process.
This script provides functionality to:
1. List documents to be migrated in a phase
2. Update migration status for a document
3. Generate progress reports
"""
import os
import sys
import json
import csv
import argparse
from datetime import datetime

def load_phase_data(phase_dir, phase_id):
    """Load phase data from JSON file."""
    json_file = os.path.join(phase_dir, f"{phase_id}_inventory.json")
    if not os.path.exists(json_file):
        print(f"Error: Phase file {json_file} not found.")
        sys.exit(1)
    
    with open(json_file, 'r') as f:
        return json.load(f)

def list_documents(phase_dir, phase_id, status=None, directory=None):
    """List documents in a phase, optionally filtered by status or directory."""
    phase_data = load_phase_data(phase_dir, phase_id)
    
    print(f"\n{phase_data['name']} - Document Listing\n")
    print(f"Total Documents: {phase_data['total_documents']}")
    print(f"Start Date: {phase_data['start_date']} | End Date: {phase_data['end_date']}\n")
    
    # Filter documents if needed
    filtered_docs = phase_data['documents']
    if status:
        filtered_docs = [doc for doc in filtered_docs if doc['status'] == status]
    if directory:
        filtered_docs = [doc for doc in filtered_docs if doc['directory'] == directory]
    
    print(f"Filtered Documents: {len(filtered_docs)}\n")
    
    print("| # | Source Path | Status | Processing Type |")
    print("|---|-------------|--------|----------------|")
    
    for i, doc in enumerate(filtered_docs, 1):
        print(f"| {i} | {doc['source_relpath']} | {doc['status']} | {doc['processing_type']} |")
    
    return filtered_docs

def update_document_status(phase_dir, phase_id, doc_index, new_status, processing_type=None, notes=None):
    """Update the status of a document in the phase inventory."""
    phase_data = load_phase_data(phase_dir, phase_id)
    
    if doc_index < 1 or doc_index > len(phase_data['documents']):
        print(f"Error: Document index {doc_index} out of range.")
        sys.exit(1)
    
    # Update document status
    doc = phase_data['documents'][doc_index - 1]
    doc['status'] = new_status
    if processing_type:
        doc['processing_type'] = processing_type
    if notes:
        doc['notes'] = notes
    
    # Save updated data
    json_file = os.path.join(phase_dir, f"{phase_id}_inventory.json")
    with open(json_file, 'w') as f:
        json.dump(phase_data, f, indent=2)
    
    # Update the markdown file too
    update_markdown_inventory(phase_dir, phase_id, phase_data)
    
    print(f"Updated document {doc['source_relpath']} status to {new_status}")
    return doc

def update_markdown_inventory(phase_dir, phase_id, phase_data):
    """Update the markdown inventory file with the latest data."""
    md_file = os.path.join(phase_dir, f"{phase_id}_inventory.md")
    
    # Create markdown content
    md_content = f"# {phase_data['name']} Inventory\n\n"
    md_content += f"**Phase:** {phase_id.capitalize()}\n"
    md_content += f"**Start Date:** {phase_data['start_date']}\n"
    md_content += f"**End Date:** {phase_data['end_date']}\n"
    md_content += f"**Total Documents:** {phase_data['total_documents']}\n\n"
    
    # Status summary
    status_counts = {}
    for doc in phase_data['documents']:
        status = doc['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    md_content += "## Status Summary\n\n"
    md_content += "| Status | Count | Percentage |\n"
    md_content += "|--------|-------|------------|\n"
    
    for status, count in sorted(status_counts.items()):
        percentage = round(count / phase_data['total_documents'] * 100, 2)
        md_content += f"| {status} | {count} | {percentage}% |\n"
    
    md_content += "\n## Documents to Process\n\n"
    md_content += "| Source Path | Directory | Status | Processing Type | Assigned To | Deadline |\n"
    md_content += "|-------------|-----------|--------|----------------|-------------|----------|\n"
    
    for doc in phase_data['documents']:
        md_content += f"| {doc['source_relpath']} | {doc['directory']} | {doc['status']} | {doc['processing_type']} | {doc['assigned_to']} | {doc['deadline']} |\n"
    
    # Write to file
    with open(md_file, 'w') as f:
        f.write(md_content)

def generate_progress_report(phase_dir, output_file):
    """Generate a progress report across all phases."""
    phases = ['phase3', 'phase4', 'phase5', 'phase6', 'phase7']
    
    report = "# Migration Progress Report\n\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Overall summary
    total_docs = 0
    completed_docs = 0
    
    phase_summaries = []
    
    for phase_id in phases:
        try:
            phase_data = load_phase_data(phase_dir, phase_id)
            
            # Count documents by status
            status_counts = {}
            for doc in phase_data['documents']:
                status = doc['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Calculate completion
            phase_total = phase_data['total_documents']
            phase_completed = status_counts.get('Completed', 0)
            completion_percentage = round(phase_completed / phase_total * 100, 2) if phase_total > 0 else 0
            
            phase_summaries.append({
                'phase_id': phase_id,
                'name': phase_data['name'],
                'total': phase_total,
                'completed': phase_completed,
                'percentage': completion_percentage,
                'status_counts': status_counts
            })
            
            total_docs += phase_total
            completed_docs += phase_completed
            
        except Exception as e:
            print(f"Warning: Could not process {phase_id}: {str(e)}")
    
    # Add Phase 2 (already completed)
    phase_summaries.insert(0, {
        'phase_id': 'phase2',
        'name': 'Core Documentation Migration',
        'total': 15,
        'completed': 15,
        'percentage': 100,
        'status_counts': {'Completed': 15}
    })
    
    total_docs += 15
    completed_docs += 15
    
    # Calculate overall completion
    overall_percentage = round(completed_docs / total_docs * 100, 2) if total_docs > 0 else 0
    
    # Create overall progress section
    report += "## Overall Progress\n\n"
    report += f"- Documents Completed: {completed_docs} / {total_docs}\n"
    report += f"- Overall Completion: {overall_percentage}%\n\n"
    
    # Create progress bar
    progress_bar = "[" + "=" * int(overall_percentage // 3) + ">" + "." * (33 - int(overall_percentage // 3)) + "] " + f"{overall_percentage}%"
    report += f"```\n{progress_bar}\n```\n\n"
    
    # Create phase summary section
    report += "## Phase Progress\n\n"
    report += "| Phase | Description | Completion | Status |\n"
    report += "|-------|-------------|-----------|--------|\n"
    
    for summary in phase_summaries:
        status = "Completed" if summary['percentage'] == 100 else "In Progress" if summary['percentage'] > 0 else "Not Started"
        report += f"| {summary['phase_id'].capitalize()} | {summary['name']} | {summary['percentage']}% | {status} |\n"
    
    # Create detailed phase sections
    report += "\n## Detailed Phase Status\n\n"
    
    for summary in phase_summaries:
        report += f"### {summary['phase_id'].capitalize()}: {summary['name']}\n\n"
        report += f"- Documents: {summary['completed']} / {summary['total']} ({summary['percentage']}%)\n"
        
        # Create status breakdown
        report += "- Status Breakdown:\n"
        for status, count in sorted(summary['status_counts'].items()):
            report += f"  - {status}: {count}\n"
        
        # Create progress bar
        phase_progress = "[" + "=" * int(summary['percentage'] // 3) + ">" + "." * (33 - int(summary['percentage'] // 3)) + "] " + f"{summary['percentage']}%"
        report += f"```\n{phase_progress}\n```\n\n"
    
    # Write report to file
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Progress report generated at {output_file}")
    return report

def main():
    parser = argparse.ArgumentParser(description='Document Migration Assistant')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List documents in a phase')
    list_parser.add_argument('phase', help='Phase ID (e.g., phase3)')
    list_parser.add_argument('--status', help='Filter by status (e.g., "Not Started")')
    list_parser.add_argument('--directory', help='Filter by directory')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update document status')
    update_parser.add_argument('phase', help='Phase ID (e.g., phase3)')
    update_parser.add_argument('doc_index', type=int, help='Document index (from list command)')
    update_parser.add_argument('status', help='New status (e.g., "In Progress", "Completed")')
    update_parser.add_argument('--type', dest='processing_type', help='Processing type (e.g., "Migrate", "Consolidate", "Archive")')
    update_parser.add_argument('--notes', help='Notes about the update')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate progress report')
    report_parser.add_argument('--output', default='migration_progress_report.md', help='Output file for the report')
    
    args = parser.parse_args()
    
    # Default phase directory
    phase_dir = '/home/locotoki/alfred-docs-repo/inventory/phases'
    
    if args.command == 'list':
        list_documents(phase_dir, args.phase, args.status, args.directory)
    elif args.command == 'update':
        update_document_status(phase_dir, args.phase, args.doc_index, args.status, args.processing_type, args.notes)
    elif args.command == 'report':
        generate_progress_report(phase_dir, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()