#!/usr/bin/python3
"""
Analyze the directory structure of the documentation to identify document categories
and count the number of documents in each category.
"""
import os
import csv
import sys
from collections import defaultdict
import json

def count_documents_by_directory(mapping_file, output_file):
    """Count the number of documents in each directory."""
    category_count = defaultdict(int)
    
    # Read the mapping file
    with open(mapping_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get directory from original_relpath
            rel_path = row['original_relpath']
            parts = rel_path.split('/')
            
            # Count by top-level directory
            if len(parts) > 1:
                category = parts[0]
            else:
                category = 'root'
            
            category_count[category] += 1
    
    # Create report with directory counts
    report = ["# Document Count by Directory\n"]
    report.append("| Directory | Document Count |")
    report.append("|-----------|---------------|")
    
    # Sort by directory name
    for category, count in sorted(category_count.items()):
        report.append(f"| {category} | {count} |")
    
    total_count = sum(category_count.values())
    report.append(f"\nTotal documents: {total_count}")
    
    # Write the report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"Created directory analysis report in {output_file}")
    
    # Create a JSON file with the counts
    json_file = output_file.replace('.md', '.json')
    with open(json_file, 'w') as f:
        json.dump(dict(category_count), f, indent=2)
    
    print(f"Created JSON data in {json_file}")
    
    return category_count

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <mapping_file> <output_file>")
        sys.exit(1)
    
    mapping_file = sys.argv[1]
    output_file = sys.argv[2]
    
    count_documents_by_directory(mapping_file, output_file)

if __name__ == "__main__":
    main()