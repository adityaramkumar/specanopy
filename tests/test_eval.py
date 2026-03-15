from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from specdiff.cli import cli
from specdiff.eval import run_baseline, run_specdiff_eval
from specdiff.types import (
    EvalResult,
    FilePlan,
    RunMetrics,
    SpecdiffConfig,
    SpecNode,
    SwarmResult,
)


def test_run_metrics_defaults():
    m = RunMetrics()
    assert m.llm_calls == 0
    assert m.input_tokens == 0
    assert m.output_tokens == 0
    assert m.wall_clock_seconds == 0.0
    assert m.compiles is None


def test_eval_result_holds_both_runs():
    spec = RunMetrics(
        llm_calls=4,
        input_tokens=12000,
        output_tokens=8000,
        wall_clock_seconds=14.2,
        compiles=True,
    )
    base = RunMetrics(
        llm_calls=1,
        input_tokens=45000,
        output_tokens=38000,
        wall_clock_seconds=22.8,
        compiles=False,
    )
    result = EvalResult(task="Port to Go", specdiff=spec, baseline=base)
    assert result.task == "Port to Go"
    assert result.specdiff.llm_calls == 4
    assert result.baseline.compiles is False


def test_run_baseline_returns_metrics():
    mock_response = MagicMock()
    mock_response.text = '{"main.go": "package main"}'
    mock_response.usage_metadata = MagicMock()
    mock_response.usage_metadata.prompt_token_count = 100
    mock_response.usage_metadata.candidates_token_count = 50

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    with patch("specdiff.eval.get_gemini_client", return_value=mock_client):
        metrics, files = run_baseline(
            task="Port to Go",
            spec_content="## My Spec\nDo stuff",
            model="gemini-2.5-flash",
        )

    assert metrics.llm_calls == 1
    assert metrics.input_tokens == 100
    assert metrics.output_tokens == 50
    assert metrics.wall_clock_seconds >= 0
    assert isinstance(files, dict)


def test_run_specdiff_eval_returns_metrics():
    nodes = [
        SpecNode(
            id="a",
            version="1.0",
            status="approved",
            hash="abc",
            content="spec a",
            file_path="a.spec.md",
        ),
        SpecNode(
            id="b",
            version="1.0",
            status="approved",
            hash="def",
            content="spec b",
            file_path="b.spec.md",
            depends_on=["a"],
        ),
    ]
    config = SpecdiffConfig()
    mock_result = SwarmResult(
        file_plan=FilePlan(files={"main.go": "package main"}),
        generated_files={"main.go": "package main"},
        generated_tests={},
        review_passed=True,
    )

    with patch("specdiff.eval.run_swarm", return_value=mock_result):
        metrics, files = run_specdiff_eval(nodes, config, Path(".specdiff"))

    assert metrics.llm_calls == 8  # 4 agents x 2 nodes
    assert metrics.wall_clock_seconds >= 0
    assert "main.go" in files


def test_format_comparison_table():
    from specdiff.eval import format_comparison

    result = EvalResult(
        task="Port to Go",
        specdiff=RunMetrics(
            llm_calls=4,
            input_tokens=12000,
            output_tokens=8000,
            wall_clock_seconds=14.2,
            compiles=True,
        ),
        baseline=RunMetrics(
            llm_calls=1,
            input_tokens=45000,
            output_tokens=38000,
            wall_clock_seconds=22.8,
            compiles=False,
        ),
    )
    table = format_comparison(result)
    assert "With Specs" in table
    assert "Without Specs" in table
    assert "12,000" in table
    assert "45,000" in table


def test_eval_command_no_specs(tmp_path):
    config_dir = tmp_path / ".specdiff"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text(
        "model: gemini-2.5-flash\nspecs_dir: .specdiff\nlanguage: go\n"
    )

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, ["eval", "--task", "Port to Go"])
    assert "No spec files found" in result.output


def test_eval_command_full_flow(tmp_path):
    """End-to-end: eval command with mocked swarm + baseline."""
    mock_swarm = SwarmResult(
        file_plan=FilePlan(files={"main.go": "desc"}),
        generated_files={"main.go": "package main\n\nfunc main() {}"},
        generated_tests={},
        review_passed=True,
    )

    mock_response = MagicMock()
    mock_response.text = '{"main.go": "package main\\n\\nfunc main() {}"}'
    mock_response.usage_metadata = MagicMock()
    mock_response.usage_metadata.prompt_token_count = 200
    mock_response.usage_metadata.candidates_token_count = 100

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        config_dir = Path(".specdiff")
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text(
            "model: gemini-2.5-flash\nspecs_dir: .specdiff\nlanguage: go\n"
        )

        skills_dir = config_dir / "skills"
        skills_dir.mkdir()
        for skill in ("architect", "implementation", "testing", "review"):
            (skills_dir / f"{skill}.skill.md").write_text(f"# {skill}\nDo {skill} things.")

        spec = config_dir / "hello.spec.md"
        spec.write_text(
            "---\nid: hello\nversion: '1.0'\nstatus: approved\n"
            "---\n\n## Hello\nPrint hello world in Go.\n"
        )

        with (
            patch("specdiff.eval.run_swarm", return_value=mock_swarm),
            patch("specdiff.eval.get_gemini_client", return_value=mock_client),
            patch("specdiff.eval.check_compiles", return_value=True),
        ):
            result = runner.invoke(cli, ["eval", "--task", "Port to Go"])

    assert result.exit_code == 0
    assert "With Specs" in result.output
    assert "Without Specs" in result.output
