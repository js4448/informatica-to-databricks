import os
from informatica_to_databricks.generator import generate_notebook


def test_generate(tmp_path):
    mapping = {
        'name': 'sample_mapping',
        'transformations': [
            {'name': 'src', 'type': 'Source', 'ports': []},
            {'name': 'expr', 'type': 'Expression', 'ports': []},
            {'name': 'tgt', 'type': 'Target', 'ports': []},
        ]
    }
    out = generate_notebook(mapping, templates_dir=os.path.join(os.path.dirname(__file__), '..', 'informatica_to_databricks', 'templates'), out_dir=str(tmp_path))
    assert os.path.exists(out)
    with open(out, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'Auto-generated' in content or 'Generated' in content or 'Auto-generated' in content
