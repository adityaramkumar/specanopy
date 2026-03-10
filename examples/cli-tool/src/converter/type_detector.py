# generated_from: contracts/formats/json
# spec_hash: 6f8c71e4166cba93ef65b3fccd66c3d2590cae65d56f0cc1e5d06634c90717c4
# generated_at: 2026-03-10T09:02:24.170441+00:00
# agent: implementation-agent

import re

def detect_type(value):
    if value == "":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.match(r'^-?\d+$', value):
        return int(value)
    if re.match(r'^-?\d+\.\d+$', value):
        return float(value)
    return value