# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

import os

class FilePartitioner:
    MAX_SIZE = 256 * 1024 * 1024
    
    def get_path(self, date: str, sequence: int = 0) -> str:
        dir_path = f"output/{date}"
        os.makedirs(dir_path, exist_ok=True)
        suffix = f"_{sequence}" if sequence > 0 else ""
        return f"{dir_path}/events{suffix}.ndjson"

    def check_size(self, file_path: str) -> bool:
        if not os.path.exists(file_path): return False
        return os.path.getsize(file_path) >= self.MAX_SIZE