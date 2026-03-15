from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from specdiff.agents.swarm import run_swarm
from specdiff.graph import build_graph
from specdiff.llm import extract_json, generate_content
from specdiff.types import EvalResult, RunMetrics, SpecdiffConfig, SpecNode

BASELINE_PROMPT = """You are a code generation agent. Given the following source code,
generate the complete source code files as a JSON object where keys are file paths
and values are file contents.

Task: {task}

--- SOURCE CODE ---
{source_code}
--- END SOURCE ---

Return ONLY a JSON object mapping file paths to file contents. No explanation."""

AGENTS_PER_NODE = 4  # architect, implementation, testing, review


def run_baseline(
    task: str,
    source_code: str,
    model: str,
) -> tuple[RunMetrics, dict[str, str]]:
    """Run a single LLM call with raw source code as one prompt."""
    prompt = BASELINE_PROMPT.format(task=task, source_code=source_code)

    start = time.monotonic()
    response = generate_content(model=model, contents=prompt)
    elapsed = time.monotonic() - start

    metrics = RunMetrics(
        llm_calls=1,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        wall_clock_seconds=round(elapsed, 2),
    )

    try:
        files = extract_json(response.text)
    except Exception:
        files = {"raw_output.txt": response.text}

    return metrics, files


def run_specdiff_eval(
    nodes: list[SpecNode],
    config: SpecdiffConfig,
    specs_dir: Path,
) -> tuple[RunMetrics, dict[str, str]]:
    """Run the specdiff swarm pipeline and capture metrics."""
    graph = build_graph(nodes)
    all_files: dict[str, str] = {}
    total_input_chars = 0
    total_output_chars = 0

    start = time.monotonic()
    for node in nodes:
        dep_specs = [graph.nodes[d] for d in node.depends_on if d in graph.nodes]
        result = run_swarm(node, config, specs_dir, dep_specs=dep_specs)
        all_files.update(result.generated_files)
        all_files.update(result.generated_tests)

        input_text = node.content + "".join(d.content for d in dep_specs)
        total_input_chars += len(input_text)
        for content in result.generated_files.values():
            total_output_chars += len(content)
        for content in result.generated_tests.values():
            total_output_chars += len(content)

    elapsed = time.monotonic() - start

    metrics = RunMetrics(
        llm_calls=len(nodes) * AGENTS_PER_NODE,
        input_tokens=total_input_chars // 4,
        output_tokens=total_output_chars // 4,
        wall_clock_seconds=round(elapsed, 2),
    )
    return metrics, all_files


def _write_files_to_dir(files: dict[str, str], target: Path, language: str) -> None:
    """Write generated files to a directory, adding go.mod if needed."""
    if language == "go" and not any(f.endswith("go.mod") for f in files):
        (target / "go.mod").write_text("module eval_output\n\ngo 1.21\n")

    for rel_path, content in files.items():
        full = target / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)


def check_compiles(files: dict[str, str], language: str) -> bool:
    """Write files to a temp dir and try to compile."""
    if language != "go":
        return True  # Only Go for now

    with tempfile.TemporaryDirectory() as tmpdir:
        _write_files_to_dir(files, Path(tmpdir), language)
        result = subprocess.run(
            ["go", "build", "./..."],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0


def check_tests(files: dict[str, str], language: str) -> tuple[bool | None, int, int]:
    """Run tests on generated files. Returns (passed, total, num_passed)."""
    has_tests = any(_is_test_file(f, language) for f in files)
    if not has_tests:
        return None, 0, 0

    if language != "go":
        return None, 0, 0  # Only Go for now

    with tempfile.TemporaryDirectory() as tmpdir:
        _write_files_to_dir(files, Path(tmpdir), language)

        # First make sure it compiles
        build = subprocess.run(
            ["go", "build", "./..."],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )
        if build.returncode != 0:
            return False, 0, 0

        result = subprocess.run(
            ["go", "test", "-v", "./..."],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout + result.stderr

        passed = len(re.findall(r"--- PASS:", output))
        failed = len(re.findall(r"--- FAIL:", output))
        total = passed + failed

        return result.returncode == 0, total, passed


def _is_test_file(path: str, language: str) -> bool:
    """Check if a file path looks like a test file."""
    if language == "go":
        return path.endswith("_test.go")
    if language in ("typescript", "javascript"):
        return any(path.endswith(ext) for ext in (".test.ts", ".spec.ts", ".test.js", ".spec.js"))
    if language == "python":
        return path.startswith("test_") or path.endswith("_test.py") or "/test_" in path
    return False


def write_eval_output(
    output_dir: Path,
    specdiff_files: dict[str, str],
    baseline_files: dict[str, str],
) -> None:
    """Write both runs' generated files to disk for inspection. Clears previous output first."""
    if output_dir.exists():
        shutil.rmtree(output_dir)

    for label, files in [("specdiff", specdiff_files), ("baseline", baseline_files)]:
        target = output_dir / label
        target.mkdir(parents=True, exist_ok=True)
        for rel_path, content in files.items():
            full = target / rel_path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content, "utf-8")


def format_comparison(result: EvalResult) -> str:
    """Format a side-by-side comparison table."""

    def _compile_str(val: bool | None) -> str:
        if val is None:
            return "—"
        return "YES" if val else "NO"

    def _fmt(n: int) -> str:
        return f"{n:,}"

    def _test_str(m: RunMetrics) -> str:
        if m.tests_pass is None:
            return "No tests"
        label = "PASS" if m.tests_pass else "FAIL"
        return f"{label} ({m.tests_passed}/{m.tests_total})"

    rows = [
        ("Files", str(result.specdiff.files_generated), str(result.baseline.files_generated)),
        ("LLM Calls", str(result.specdiff.llm_calls), str(result.baseline.llm_calls)),
        ("Tokens (in)", _fmt(result.specdiff.input_tokens), _fmt(result.baseline.input_tokens)),
        ("Tokens (out)", _fmt(result.specdiff.output_tokens), _fmt(result.baseline.output_tokens)),
        (
            "Latency",
            f"{result.specdiff.wall_clock_seconds}s",
            f"{result.baseline.wall_clock_seconds}s",
        ),
        (
            "Compiles?",
            _compile_str(result.specdiff.compiles),
            _compile_str(result.baseline.compiles),
        ),
        ("Tests?", _test_str(result.specdiff), _test_str(result.baseline)),
    ]

    col1_w = max(len(r[0]) for r in rows) + 2
    col2_w = max(len(r[1]) for r in rows) + 2
    col3_w = max(len(r[2]) for r in rows) + 2

    header_label = ("Metric", "With Specs", "Without Specs")
    col1_w = max(col1_w, len(header_label[0]) + 2)
    col2_w = max(col2_w, len(header_label[1]) + 2)
    col3_w = max(col3_w, len(header_label[2]) + 2)

    sep = f"+{'-' * col1_w}+{'-' * col2_w}+{'-' * col3_w}+"
    lines = [sep]
    lines.append(
        f"|{header_label[0]:^{col1_w}}|{header_label[1]:^{col2_w}}|{header_label[2]:^{col3_w}}|"
    )
    lines.append(sep)
    for label, v1, v2 in rows:
        lines.append(f"|{label:^{col1_w}}|{v1:^{col2_w}}|{v2:^{col3_w}}|")
    lines.append(sep)

    return "\n".join(lines)
