from informatica_to_databricks.parser import parse_informatica_xml
import os


def test_parse_sample(tmp_path):
    sample = os.path.join(os.path.dirname(__file__), 'samples', 'sample_mapping.xml')
    model = parse_informatica_xml(sample)
    assert 'mappings' in model
    assert len(model['mappings']) >= 1
    mp = model['mappings'][0]
    assert mp['name'] == 'sample_mapping'
    assert any(t['type'] == 'Source' for t in mp['transformations'])
