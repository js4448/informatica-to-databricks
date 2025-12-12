"""Generator that renders a Jinja2 template into a PySpark file."""
from jinja2 import Environment, FileSystemLoader
import os
from typing import Dict


def generate_notebook(mapping: Dict, templates_dir: str = None, out_dir: str = 'generated') -> str:
    """Render mapping to a .py file and return output path."""
    templates_dir = templates_dir or os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('notebook.py.j2')
    rendered = template.render(mapping=mapping)
    os.makedirs(out_dir, exist_ok=True)
    safe_name = mapping.get('name', 'mapping').replace(' ', '_')
    out_path = os.path.join(out_dir, f"{safe_name}.py")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    return out_path


if __name__ == '__main__':
    # simple demo runner for manual invocation
    import json, sys
    if len(sys.argv) < 2:
        print('Usage: generator.py <mapping-json-file>')
        sys.exit(1)
    mapping = json.load(open(sys.argv[1]))
    print('Generating...', generate_notebook(mapping))
