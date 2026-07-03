import json
import os

DATA_FILE = 'examples_data.json'

def escape_sql(val):
    if val is None:
        return 'NULL'
    return "'" + json.dumps(val).replace("'", "''") + "'"

def generate_inserts():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    batch_size = 20
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        values = []
        for item in batch:
            v = f"({escape_sql(item['name'])}, {escape_sql(item['category'])}, {escape_sql(item['framework'])}, {escape_sql(item['files'])}, {escape_sql(item['dependencies'])}, {escape_sql({'original_path': item['original_path']})})"
            values.append(v)
        
        sql = f"INSERT INTO examples (name, category, framework, files, dependencies, metadata) VALUES {', '.join(values)};"
        
        chunk_file = f'migrate_scripts/chunk_{i//batch_size}.sql'
        with open(chunk_file, 'w', encoding='utf-8') as f_out:
            f_out.write(sql)
        print(f"Generated {chunk_file}")

if __name__ == "__main__":
    generate_inserts()
