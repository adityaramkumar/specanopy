# generated_from: contracts/formats/json
# spec_hash: 6f8c71e4166cba93ef65b3fccd66c3d2590cae65d56f0cc1e5d06634c90717c4
# generated_at: 2026-03-10T09:02:24.170441+00:00
# agent: implementation-agent

from converter.type_detector import detect_type

def transform_rows(header, rows, detect_types=False):
    transformed = []
    for row in rows:
        obj = {}
        for i, val in enumerate(row):
            key = header[i]
            obj[key] = detect_type(val) if detect_types else val
        transformed.append(obj)
    return transformed