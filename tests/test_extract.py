from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from specdiff.extract import _collect_source_files, _extract_auto, _extract_file_by_file


def _mock_response(text: str) -> MagicMock:
    resp = MagicMock()
    resp.text = text
    return resp


class TestCollectSourceFiles:
    def test_finds_python_files(self, tmp_path):
        (tmp_path / "main.py").write_text("print('hello')")
        (tmp_path / "utils.py").write_text("def util(): pass")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "main.py" in paths
        assert "utils.py" in paths

    def test_finds_js_and_ts_files(self, tmp_path):
        (tmp_path / "app.js").write_text("console.log('hi')")
        (tmp_path / "types.ts").write_text("type T = string")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "app.js" in paths
        assert "types.ts" in paths

    def test_finds_yaml_and_json_files(self, tmp_path):
        (tmp_path / "config.yaml").write_text("key: value")
        (tmp_path / "schema.json").write_text('{"key": "value"}')

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "config.yaml" in paths
        assert "schema.json" in paths

    def test_ignores_non_matching_extensions(self, tmp_path):
        (tmp_path / "main.py").write_text("x = 1")
        (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        (tmp_path / "binary.bin").write_bytes(b"\x00\x01\x02")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "main.py" in paths
        assert "image.png" not in paths
        assert "binary.bin" not in paths

    def test_ignores_node_modules(self, tmp_path):
        nm = tmp_path / "node_modules"
        nm.mkdir()
        (nm / "lib.js").write_text("module.exports = {}")
        (tmp_path / "app.js").write_text("const x = 1")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "app.js" in paths
        assert not any("node_modules" in p for p in paths)

    def test_ignores_git_directory(self, tmp_path):
        git = tmp_path / ".git"
        git.mkdir()
        (git / "config").write_text("[core]")
        (tmp_path / "main.py").write_text("x = 1")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "main.py" in paths
        assert not any(".git" in p for p in paths)

    def test_ignores_pycache(self, tmp_path):
        cache = tmp_path / "__pycache__"
        cache.mkdir()
        (cache / "module.py").write_text("cached")
        (tmp_path / "module.py").write_text("real")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "module.py" in paths
        assert not any("__pycache__" in p for p in paths)

    def test_ignores_venv_directory(self, tmp_path):
        venv = tmp_path / "venv"
        venv.mkdir()
        (venv / "activate.py").write_text("# venv")
        (tmp_path / "app.py").write_text("x = 1")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert not any("venv" in p for p in paths)

    def test_handles_unicode_decode_error(self, tmp_path):
        bad_file = tmp_path / "bad.py"
        bad_file.write_bytes(b"\xff\xfe\x80\x81invalid utf-8")
        (tmp_path / "good.py").write_text("x = 1")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert "good.py" in paths
        assert "bad.py" not in paths

    def test_empty_directory_returns_empty_list(self, tmp_path):
        result = _collect_source_files(tmp_path)
        assert result == []

    def test_returns_relative_paths(self, tmp_path):
        subdir = tmp_path / "src" / "module"
        subdir.mkdir(parents=True)
        (subdir / "logic.py").write_text("x = 1")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert any(os.path.join("src", "module", "logic.py") in p for p in paths)
        assert not any(str(tmp_path) in p for p in paths)

    def test_result_contains_content(self, tmp_path):
        (tmp_path / "main.py").write_text("x = 42")

        result = _collect_source_files(tmp_path)
        entry = next(f for f in result if f["path"] == "main.py")
        assert entry["content"] == "x = 42"

    def test_ignores_specdiff_directory(self, tmp_path):
        sd = tmp_path / ".specdiff"
        sd.mkdir()
        (sd / "config.yaml").write_text("model: gemini-2.5-flash")
        (tmp_path / "app.py").write_text("x = 1")

        result = _collect_source_files(tmp_path)
        paths = [f["path"] for f in result]
        assert not any(".specdiff" in p for p in paths)


class TestExtractAuto:
    def test_writes_contracts_and_behaviors(self, tmp_path):
        contracts = [{"path": "contracts/users", "content": "---\nid: contracts/users\n---"}]
        behaviors = [
            {"path": "behaviors/auth/login", "content": "---\nid: behaviors/auth/login\n---"}
        ]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response(json.dumps(contracts)),
                _mock_response(json.dumps(behaviors)),
            ]
            _extract_auto("gemini-2.5-flash", "code text", tmp_path)

        assert (tmp_path / "contracts" / "users.spec.md").exists()
        assert (tmp_path / "behaviors" / "auth" / "login.spec.md").exists()

    def test_does_not_double_add_spec_md_extension(self, tmp_path):
        contracts = [
            {"path": "contracts/users.spec.md", "content": "---\nid: contracts/users\n---"}
        ]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response(json.dumps(contracts)),
                _mock_response("[]"),
            ]
            _extract_auto("gemini-2.5-flash", "code text", tmp_path)

        assert (tmp_path / "contracts" / "users.spec.md").exists()
        assert not (tmp_path / "contracts" / "users.spec.md.spec.md").exists()

    def test_contract_parse_failure_raises(self, tmp_path):
        from click import ClickException

        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response("not json at all")
            with pytest.raises(ClickException, match="Failed to parse contracts"):
                _extract_auto("gemini-2.5-flash", "code text", tmp_path)

    def test_contract_wrong_type_raises(self, tmp_path):
        from click import ClickException

        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response('{"not": "a list"}')
            with pytest.raises(ClickException, match="unexpected structure for contracts"):
                _extract_auto("gemini-2.5-flash", "code text", tmp_path)

    def test_contract_missing_path_field_raises(self, tmp_path):
        from click import ClickException

        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response('[{"content": "no path field"}]')
            with pytest.raises(ClickException, match="unexpected structure for contracts"):
                _extract_auto("gemini-2.5-flash", "code text", tmp_path)

    def test_behavior_parse_failure_raises(self, tmp_path):
        from click import ClickException

        contracts = [{"path": "contracts/users", "content": "---\nid: contracts/users\n---"}]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response(json.dumps(contracts)),
                _mock_response("not json"),
            ]
            with pytest.raises(ClickException, match="Failed to parse behaviors"):
                _extract_auto("gemini-2.5-flash", "code text", tmp_path)

    def test_behavior_wrong_type_raises(self, tmp_path):
        from click import ClickException

        contracts = [{"path": "contracts/users", "content": "---\nid: contracts/users\n---"}]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response(json.dumps(contracts)),
                _mock_response('"just a string"'),
            ]
            with pytest.raises(ClickException, match="unexpected structure for behaviors"):
                _extract_auto("gemini-2.5-flash", "code text", tmp_path)

    def test_makes_exactly_two_llm_calls(self, tmp_path):
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [_mock_response("[]"), _mock_response("[]")]
            _extract_auto("my-model", "code text", tmp_path)
        assert mock_gen.call_count == 2

    def test_contract_paths_included_in_behavior_prompt(self, tmp_path):
        contracts = [{"path": "contracts/users", "content": "---\nid: contracts/users\n---"}]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response(json.dumps(contracts)),
                _mock_response("[]"),
            ]
            _extract_auto("my-model", "code text", tmp_path)
        behavior_prompt = mock_gen.call_args_list[1].kwargs["contents"]
        assert "contracts/users" in behavior_prompt

    def test_writes_file_content_verbatim(self, tmp_path):
        body = "---\nid: contracts/users\n---\n# Users spec body"
        contracts = [{"path": "contracts/users", "content": body}]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [_mock_response(json.dumps(contracts)), _mock_response("[]")]
            _extract_auto("gemini-2.5-flash", "code text", tmp_path)
        assert (tmp_path / "contracts" / "users.spec.md").read_text() == body


class TestExtractFileByFile:
    def test_writes_spec_for_each_file(self, tmp_path):
        code_files = [{"path": "src/auth.py", "content": "def login(): pass"}]
        spec = {"path": "behaviors/auth.spec.md", "content": "---\nid: behaviors/auth\n---"}
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response(json.dumps(spec))
            _extract_file_by_file("gemini-2.5-flash", code_files, tmp_path)
        assert (tmp_path / "behaviors" / "auth.spec.md").exists()

    def test_one_call_per_file(self, tmp_path):
        code_files = [
            {"path": "a.py", "content": "x = 1"},
            {"path": "b.py", "content": "y = 2"},
        ]
        spec_a = {"path": "behaviors/a.spec.md", "content": "---\nid: behaviors/a\n---"}
        spec_b = {"path": "behaviors/b.spec.md", "content": "---\nid: behaviors/b\n---"}
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response(json.dumps(spec_a)),
                _mock_response(json.dumps(spec_b)),
            ]
            _extract_file_by_file("gemini-2.5-flash", code_files, tmp_path)
        assert mock_gen.call_count == 2
        assert (tmp_path / "behaviors" / "a.spec.md").exists()
        assert (tmp_path / "behaviors" / "b.spec.md").exists()

    def test_failed_file_is_skipped_others_continue(self, tmp_path):
        code_files = [
            {"path": "bad.py", "content": "x = 1"},
            {"path": "good.py", "content": "y = 2"},
        ]
        spec_good = {"path": "behaviors/good.spec.md", "content": "---\nid: behaviors/good\n---"}
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.side_effect = [
                _mock_response("not json"),
                _mock_response(json.dumps(spec_good)),
            ]
            _extract_file_by_file("gemini-2.5-flash", code_files, tmp_path)
        assert (tmp_path / "behaviors" / "good.spec.md").exists()

    def test_list_response_unwrapped_to_first_element(self, tmp_path):
        code_files = [{"path": "auth.py", "content": "def login(): pass"}]
        spec = [{"path": "behaviors/auth.spec.md", "content": "---\nid: behaviors/auth\n---"}]
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response(json.dumps(spec))
            _extract_file_by_file("gemini-2.5-flash", code_files, tmp_path)
        assert (tmp_path / "behaviors" / "auth.spec.md").exists()

    def test_missing_path_field_skips_file_without_raising(self, tmp_path):
        code_files = [{"path": "auth.py", "content": "def login(): pass"}]
        bad_data = {"content": "no path field"}
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response(json.dumps(bad_data))
            _extract_file_by_file("gemini-2.5-flash", code_files, tmp_path)

    def test_all_file_paths_included_in_every_prompt(self, tmp_path):
        code_files = [
            {"path": "src/auth.py", "content": "def login(): pass"},
            {"path": "src/models.py", "content": "class User: pass"},
        ]
        spec = {"path": "behaviors/auth.spec.md", "content": "---\nid: behaviors/auth\n---"}
        with patch("specdiff.extract.generate_content") as mock_gen:
            mock_gen.return_value = _mock_response(json.dumps(spec))
            _extract_file_by_file("gemini-2.5-flash", code_files, tmp_path)
        prompt = mock_gen.call_args_list[0].kwargs["contents"]
        assert "src/auth.py" in prompt
        assert "src/models.py" in prompt
