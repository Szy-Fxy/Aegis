"""Tests for utils/fs.py — 文件系统辅助函数"""

import pytest

from aegis_toolchain.utils.fs import ensure_dir, safe_path, atomic_write


class TestEnsureDir:
    def test_creates_dir(self, tmp_path):
        p = tmp_path / "new" / "dir"
        ensure_dir(p)
        assert p.exists()
        assert p.is_dir()

    def test_existing_dir_ok(self, tmp_path):
        ensure_dir(tmp_path)  # already exists, no error

    def test_deep_nesting(self, tmp_path):
        p = tmp_path / "a" / "b" / "c" / "d"
        ensure_dir(p)
        assert p.exists()


class TestSafePath:
    def test_normal_path(self, tmp_path):
        result = safe_path(tmp_path, "sub/file.txt")
        assert str(result).startswith(str(tmp_path.resolve()))

    def test_rejects_traversal(self, tmp_path):
        with pytest.raises(ValueError, match="路径穿越"):
            safe_path(tmp_path, "../escape.txt")

    def test_nested_ok(self, tmp_path):
        result = safe_path(tmp_path, "a/b/c/file.txt")
        assert result.name == "file.txt"


class TestAtomicWrite:
    def test_write_and_read(self, tmp_path):
        path = tmp_path / "test.json"
        atomic_write(path, '{"key": "value"}')
        assert path.exists()
        assert path.read_text() == '{"key": "value"}'

    def test_no_tmp_leftover(self, tmp_path):
        path = tmp_path / "test.json"
        atomic_write(path, "content")
        tmp = tmp_path / "test.json.tmp"
        assert not tmp.exists()

    def test_overwrite(self, tmp_path):
        path = tmp_path / "test.json"
        path.write_text("old")
        atomic_write(path, "new")
        assert path.read_text() == "new"

    def test_create_parent_dirs(self, tmp_path):
        path = tmp_path / "deep" / "dir" / "test.txt"
        atomic_write(path, "hello")
        assert path.read_text() == "hello"
