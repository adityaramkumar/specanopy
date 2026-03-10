# generated_from: contracts/formats/json
# spec_hash: 6f8c71e4166cba93ef65b3fccd66c3d2590cae65d56f0cc1e5d06634c90717c4
# generated_at: 2026-03-10T09:02:24.170441+00:00
# agent: implementation-agent

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--detect-types', action='store_true')
    parser.add_argument('--compact', action='store_true')
    parser.add_argument('input', help='Input CSV file')
    parser.add_argument('output', help='Output JSON file')
    return parser.parse_args()