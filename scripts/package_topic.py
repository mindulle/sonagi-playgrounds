import os
import re
from datetime import datetime

WIKI_ROOT = "20_Wiki"
EXPORT_DIR = "00_System/_exports"

# Role Configuration: Mapping roles to wiki paths
ROLE_MAP = {
    "ui_ux_designer": [
        "20_Wiki/Design",
        "20_Wiki/_concepts/Cognitive Bias.md",
        "20_Wiki/_concepts/Cognitive-Bias.md",
        "20_Wiki/_concepts/Gestalt Principles.md",
        "20_Wiki/_concepts/Gestalt-Principles.md"
    ],
    "product_manager": [
        "20_Wiki/Business",
        "20_Wiki/Develop/Processes/Code_Review",
        "20_Wiki/Computing/software-design-architecture.md",
        "20_Wiki/Principles"
    ],
    "ds_manager_design": [
        "20_Wiki/Design",
        "20_Wiki/_concepts/Atomic Design.md",
        "10_Sources/assets/branding"
    ],
    "ds_manager_tech_react": [
        "20_Wiki/Develop/Frontend",
        "20_Wiki/Develop/References/react"
    ],
    "ds_manager_tech_js_rest": [
        "20_Wiki/Develop/References/javascript/classes",
        "20_Wiki/Develop/References/javascript/concepts",
        "20_Wiki/Develop/References/javascript/errors",
        "20_Wiki/Develop/References/javascript/functions",
        "20_Wiki/Develop/References/javascript/internals",
        "20_Wiki/Develop/References/javascript/operators",
        "20_Wiki/Develop/References/javascript/regular_expressions",
        "20_Wiki/Develop/References/javascript/statements",
        "20_Wiki/Develop/References/javascript/index.md",
        "20_Wiki/Develop/References/javascript/iteration_protocols.md",
        "20_Wiki/Develop/References/javascript/lexical_grammar.md",
        "20_Wiki/Develop/References/javascript/strict_mode.md",
        "20_Wiki/Develop/References/javascript/template_literals.md",
        "20_Wiki/Develop/References/javascript/trailing_commas.md"
    ],
    "ds_manager_tech_js_globals_1": [
        "20_Wiki/Develop/References/javascript/global_objects/array",
        "20_Wiki/Develop/References/javascript/global_objects/arraybuffer",
        "20_Wiki/Develop/References/javascript/global_objects/asyncfunction",
        "20_Wiki/Develop/References/javascript/global_objects/asyncgenerator",
        "20_Wiki/Develop/References/javascript/global_objects/asynciterator",
        "20_Wiki/Develop/References/javascript/global_objects/atomics",
        "20_Wiki/Develop/References/javascript/global_objects/bigint",
        "20_Wiki/Develop/References/javascript/global_objects/boolean",
        "20_Wiki/Develop/References/javascript/global_objects/dataview",
        "20_Wiki/Develop/References/javascript/global_objects/date",
        "20_Wiki/Develop/References/javascript/global_objects/error",
        "20_Wiki/Develop/References/javascript/global_objects/function",
        "20_Wiki/Develop/References/javascript/global_objects/intl"
    ],
    "ds_manager_tech_js_globals_2": [
        "20_Wiki/Develop/References/javascript/global_objects/json",
        "20_Wiki/Develop/References/javascript/global_objects/map",
        "20_Wiki/Develop/References/javascript/global_objects/math",
        "20_Wiki/Develop/References/javascript/global_objects/number",
        "20_Wiki/Develop/References/javascript/global_objects/object",
        "20_Wiki/Develop/References/javascript/global_objects/promise",
        "20_Wiki/Develop/References/javascript/global_objects/proxy",
        "20_Wiki/Develop/References/javascript/global_objects/reflect",
        "20_Wiki/Develop/References/javascript/global_objects/regexp",
        "20_Wiki/Develop/References/javascript/global_objects/set",
        "20_Wiki/Develop/References/javascript/global_objects/sharedarraybuffer",
        "20_Wiki/Develop/References/javascript/global_objects/string",
        "20_Wiki/Develop/References/javascript/global_objects/symbol",
        "20_Wiki/Develop/References/javascript/global_objects/typedarray",
        "20_Wiki/Develop/References/javascript/global_objects/weakmap",
        "20_Wiki/Develop/References/javascript/global_objects/weakref",
        "20_Wiki/Develop/References/javascript/global_objects/weakset"
    ]
}

def package_role(role_id):
    if role_id not in ROLE_MAP:
        print(f"Error: Role '{role_id}' not found.")
        return

    targets = ROLE_MAP[role_id]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"Package_{role_id}_{timestamp}.md"
    output_path = os.path.join(EXPORT_DIR, output_filename)

    os.makedirs(EXPORT_DIR, exist_ok=True)

    print(f"--- Packaging for Role: {role_id} ---")
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Header
        outfile.write(f"# Knowledge Package: {role_id.replace('_', ' ').title()}\n")
        outfile.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        outfile.write("> This is a consolidated knowledge pack for NotebookLM. All sources are attributed below.\n\n---\n")

        for target in targets:
            full_target_path = os.path.abspath(target)
            if not os.path.exists(full_target_path):
                print(f"  Warning: Target path not found: {target}")
                continue

            if os.path.isfile(full_target_path):
                process_file(full_target_path, outfile)
            else:
                for root, dirs, files in os.walk(full_target_path):
                    for file in sorted(files):
                        if file.endswith(".md"):
                            process_file(os.path.join(root, file), outfile)

    print(f"\n✅ Successfully created package: {output_path}")
    print(f"You can now upload this file to your {role_id} NotebookLM.")

def process_file(file_path, outfile):
    rel_path = os.path.relpath(file_path, WIKI_ROOT)
    print(f"  Adding {rel_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean YAML frontmatter
    content = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    
    outfile.write(f"\n\n## Source: {rel_path}\n")
    outfile.write(content)
    outfile.write("\n\n---\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 package_topic.py <role_id>")
        print("Roles: ui_ux_designer, product_manager, design_system_manager")
    else:
        package_role(sys.argv[1])
