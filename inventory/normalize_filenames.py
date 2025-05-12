#!/usr/bin/python3
"""
Normalize filenames in the docs directory to make them suitable for processing.
This script creates a mapping file that relates original filenames to normalized ones.
"""
import os
import re
import csv
import sys

def normalize_filename(filename):
    """Normalize a filename by replacing problematic characters."""
    # Remove ID sequences (like '1eab4fd21ff080558d86c62ddca38268')
    filename = re.sub(r'\s+\w{32}\.md$', '.md', filename)
    
    # Replace spaces, dashes, and special characters
    normalized = filename.lower()
    normalized = re.sub(r'[^a-z0-9_/.]', '_', normalized)
    normalized = re.sub(r'_+', '_', normalized)  # Replace multiple underscores with one
    normalized = re.sub(r'_\.md$', '.md', normalized)  # Remove trailing underscore before extension
    
    return normalized

def create_normalization_mapping(source_dir, output_file):
    """Create a mapping between original and normalized filenames."""
    mapping = []
    
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                original_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(original_path, source_dir)
                
                # Normalize the relative path
                normalized_filename = normalize_filename(os.path.basename(rel_path))
                normalized_dir = os.path.dirname(rel_path)
                normalized_path = os.path.join(normalized_dir, normalized_filename)
                
                mapping.append({
                    'original_path': original_path,
                    'original_relpath': rel_path,
                    'normalized_path': os.path.join(source_dir, normalized_path),
                    'normalized_relpath': normalized_path,
                    'filename': filename,
                    'normalized_filename': normalized_filename
                })
    
    # Write the mapping to a CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'original_path', 'original_relpath', 'normalized_path', 
            'normalized_relpath', 'filename', 'normalized_filename'
        ])
        writer.writeheader()
        writer.writerows(mapping)
    
    print(f"Created normalization mapping with {len(mapping)} files in {output_file}")
    return mapping

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_file>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    create_normalization_mapping(source_dir, output_file)

if __name__ == "__main__":
    main()