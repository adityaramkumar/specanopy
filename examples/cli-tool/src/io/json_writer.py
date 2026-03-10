# generated_from: contracts/formats/json
# spec_hash: 6f8c71e4166cba93ef65b3fccd66c3d2590cae65d56f0cc1e5d06634c90717c4
# generated_at: 2026-03-10T09:02:24.170441+00:00
# agent: implementation-agent

import json

def write_json(data, output_path, compact=False):
    indent = None if compact else 2
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)