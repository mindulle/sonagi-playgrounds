import re
import os

def split_sql_chunk(input_path, output_dir):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the prefix: INSERT INTO examples (columns) VALUES 
    match = re.search(r'(INSERT\s+INTO\s+examples\s*\([^)]+\)\s*VALUES\s*)', content, re.IGNORECASE)
    if not match:
        print(f"Prefix not found in {input_path}")
        return
    
    prefix = match.group(1)
    values_raw = content[match.end():].strip()
    
    # Remove trailing semicolon if present
    if values_raw.endswith(';'):
        values_raw = values_raw[:-1].strip()
        
    # Split by '), (' which separates value tuples
    # This is a bit naive if '), (' appears inside strings, but usually SQL chunks are formatted safely.
    # A more robust way would be to find the closing ')' of each tuple.
    
    items = []
    current_item = []
    depth = 0
    in_string = False
    escape = False
    
    i = 0
    while i < len(values_raw):
        char = values_raw[i]
        
        if char == "'" and not escape:
            in_string = not in_string
        
        if not in_string:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    current_item.append(')')
                    items.append("".join(current_item))
                    current_item = []
                    # Skip the comma and space: , (
                    i += 1
                    while i < len(values_raw) and values_raw[i] in [',', ' ', '\n', '\r']:
                        i += 1
                    continue
        
        current_item.append(char)
        
        if char == '\\':
            escape = not escape
        else:
            escape = False
        i += 1
    
    base_name = os.path.basename(input_path).replace('.sql', '')
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, item in enumerate(items):
        output_path = os.path.join(output_dir, f"{base_name}_part_{idx:03d}.sql")
        query = f"{prefix} {item} ON CONFLICT (name) DO NOTHING;"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(query)
    
    print(f"Split {len(items)} items from {input_path} into {output_dir}")

if __name__ == "__main__":
    split_sql_chunk('/mnt/d/_develop-projects/projects/@hotssi/sandbox/migrate_scripts/chunk_16.sql', '/tmp/split_chunks')
    split_sql_chunk('/mnt/d/_develop-projects/projects/@hotssi/sandbox/migrate_scripts/chunk_18.sql', '/tmp/split_chunks')
