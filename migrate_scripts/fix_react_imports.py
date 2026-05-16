import os
import re

def fix_react_imports(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                    except UnicodeDecodeError:
                        continue
                
                # Regex to find imports from ../component/Something
                # We need to check if that file exists with .jsx or .js extension
                pattern = r'(import\s+.*\s+from\s+[\'"])(\.\.\/component\/)([^\'"]+)([\'"])'
                
                def replace_import(match):
                    prefix = match.group(1)
                    rel_path = match.group(2)
                    comp_name = match.group(3)
                    suffix = match.group(4)
                    
                    # Component directory is usually at the same level as 'src'
                    # If current file is in 'src/App.js', parent is root, then 'component/'
                    current_dir = os.path.dirname(file_path)
                    target_dir = os.path.abspath(os.path.join(current_dir, '..', 'component'))
                    
                    if os.path.exists(target_dir):
                        # Look for comp_name.jsx or comp_name.js
                        for ext in ['.jsx', '.js']:
                            if os.path.exists(os.path.join(target_dir, comp_name + ext)):
                                print(f"  Fixed import in {file_path}: {comp_name} -> {comp_name}{ext}")
                                return f"{prefix}{rel_path}{comp_name}{ext}{suffix}"
                    
                    return match.group(0)

                new_content = re.sub(pattern, replace_import, content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    fix_react_imports('component/react')
