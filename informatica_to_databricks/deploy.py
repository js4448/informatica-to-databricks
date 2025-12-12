"""Simple Databricks deploy helper (uses databricks-sdk if available).

This provides a minimal upload function. It expects DATABRICKS_HOST and
DATABRICKS_TOKEN env vars to be set for authentication.
"""
import os
import base64
import json
import requests
from typing import Optional


def _get_auth_headers():
    host = os.environ.get('DATABRICKS_HOST')
    token = os.environ.get('DATABRICKS_TOKEN')
    if not host or not token:
        raise RuntimeError('DATABRICKS_HOST and DATABRICKS_TOKEN environment variables must be set')
    return host.rstrip('/'), {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


def _mkdirs(target_path: str) -> None:
    host, headers = _get_auth_headers()
    url = f"{host}/api/2.0/workspace/mkdirs"
    resp = requests.post(url, headers=headers, data=json.dumps({'path': target_path}))
    if resp.status_code not in (200, 201, 204):
        # mkdirs returns 200/204 on success; if folder exists it may also be OK.
        raise RuntimeError(f'mkdirs failed: {resp.status_code} {resp.text}')


def upload_notebook(local_file: str, target_path: str, language: str = 'PYTHON') -> None:
    """Upload a local file to Databricks workspace path using REST API.

    This will ensure the target folder exists (creates it if needed) and then
    call the workspace import endpoint with base64 content.
    """
    host, headers = _get_auth_headers()

    # Ensure parent folder exists
    parent = os.path.dirname(target_path)
    try:
        _mkdirs(parent)
    except RuntimeError as e:
        # If mkdirs fails with 403/401, surface a helpful message
        print('Warning: could not create parent folder:', e)

    with open(local_file, 'r', encoding='utf-8') as f:
        content = f.read()

    b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
    payload = {
        'path': target_path,
        'format': 'SOURCE',
        'language': language,
        'content': b64
    }

    url = f"{host}/api/2.0/workspace/import"
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    if resp.status_code not in (200, 201, 204):
        raise RuntimeError(f'import failed: {resp.status_code} {resp.text}')
    print('Uploaded', local_file, 'to', target_path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', required=True)
    parser.add_argument('--target', required=True)
    args = parser.parse_args()
    # If src is a directory, upload all .py files
    if os.path.isdir(args.src):
        for fname in os.listdir(args.src):
            if fname.endswith('.py'):
                upload_notebook(os.path.join(args.src, fname), os.path.join(args.target, fname))
    else:
        upload_notebook(args.src, args.target)
