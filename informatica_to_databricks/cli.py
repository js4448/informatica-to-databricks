"""Command-line interface for the converter."""
import argparse
import json
import os
from .parser import parse_informatica_xml
from .generator import generate_notebook


def cmd_generate(args):
    model = parse_informatica_xml(args.input)
    # support multiple mappings inside file
    for mapping in model.get('mappings', []):
        out = generate_notebook(mapping, templates_dir=args.templates, out_dir=args.out)
        print('Wrote', out)


def main():
    parser = argparse.ArgumentParser(prog='informatica-to-databricks')
    sub = parser.add_subparsers(dest='cmd')

    g = sub.add_parser('generate')
    g.add_argument('--input', '-i', required=True, help='Path to Informatica XML file')
    g.add_argument('--out', '-o', default='generated', help='Output directory')
    g.add_argument('--templates', default=None, help='Templates directory (optional)')
    g.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    args.func(args)


if __name__ == '__main__':
    main()
