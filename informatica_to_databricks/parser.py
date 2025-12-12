"""Simple Informatica XML parser (starter).

This is a minimal parser that extracts mappings and transformations into a
Python dict. Informatica export XML schemas vary; adapt XPath expressions
to your exported files.
"""
from lxml import etree
from typing import Dict, List


def parse_informatica_xml(path: str) -> Dict:
    """Parse an Informatica XML and return a structured model.

    Returns a dict:{"mappings": [ {"name": str, "transformations": [...]}, ... ]}
    """
    tree = etree.parse(path)
    root = tree.getroot()

    mappings = []
    # The common Informatica tag for mappings is MAPPING, but check your files
    for mapping in root.findall('.//MAPPING'):
        mp_name = mapping.get('NAME') or mapping.get('name') or 'mapping'
        transformations = []
        for trans in mapping.findall('.//TRANSFORMATION'):
            t_name = trans.get('NAME') or trans.get('name')
            t_type = trans.get('TYPE') or trans.get('type')
            ports = []
            # Ports/fields sometimes appear as TRANSFORMFIELD or PORT
            for port in trans.findall('.//TRANSFORMFIELD') + trans.findall('.//PORT'):
                p = {
                    'name': port.get('NAME') or port.get('name'),
                    'datatype': port.get('DATATYPE') or port.get('datatype'),
                    'precision': port.get('PRECISION'),
                    'scale': port.get('SCALE'),
                    'porttype': port.get('PORTTYPE') or port.get('porttype')
                }
                ports.append(p)
            transformations.append({'name': t_name, 'type': t_type, 'ports': ports})
        mappings.append({'name': mp_name, 'transformations': transformations})

    return {'mappings': mappings}


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: parser.py <path-to-xml>')
        sys.exit(1)
    model = parse_informatica_xml(sys.argv[1])
    import json
    print(json.dumps(model, indent=2))
