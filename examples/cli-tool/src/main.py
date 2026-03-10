# generated_from: contracts/formats/json
# spec_hash: 6f8c71e4166cba93ef65b3fccd66c3d2590cae65d56f0cc1e5d06634c90717c4
# generated_at: 2026-03-10T09:02:24.170441+00:00
# agent: implementation-agent

import csv
from cli.args_parser import parse_args
from converter.json_transformer import transform_rows
from io.json_writer import write_json

def main():
    args = parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    data = transform_rows(header, rows, args.detect_types)
    write_json(data, args.output, args.compact)

if __name__ == '__main__':
    main()