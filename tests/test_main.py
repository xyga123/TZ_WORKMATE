import os
import tempfile
import pytest
from logs.main import validate_files, main
from unittest.mock import patch, MagicMock
import subprocess


def test_validate_files_valid():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    assert validate_files([path]) == [path]
    os.unlink(path)


def test_validate_files_missing():
    with pytest.raises(SystemExit):
        validate_files(["nonexistent.log"])


def test_main_valid_execution(monkeypatch, capsys):
    with tempfile.NamedTemporaryFile(delete=False) as tmp1, tempfile.NamedTemporaryFile(
        delete=False
    ) as tmp2:
        tmp1.write(b"[INFO] django.request log message /api/v1/resource")
        tmp1.seek(0)
        tmp2.write(b"[ERROR] django.request log message /api/v1/resource")
        tmp2.seek(0)
        log_files = [tmp1.name, tmp2.name]

    monkeypatch.setattr("sys.argv", ["main.py"] + log_files)

    with patch("logs.main.HandlersReport") as MockReport, patch(
        "logs.main.parse_log_file"
    ) as mock_parse:
        mock_report_instance = MagicMock()
        MockReport.return_value = mock_report_instance

        mock_parse.side_effect = [
            {"/api/v1/resource": {"INFO": 1}},
            {"/api/v1/resource": {"ERROR": 1}},
        ]

        main()

        assert mock_parse.call_count == 2
        mock_parse.assert_any_call(log_files[0])
        mock_parse.assert_any_call(log_files[1])

        mock_report_instance.generate.assert_called_once()

    captured = capsys.readouterr()
    assert "Ъухзяьчи" in captured.out

    for file in log_files:
        os.unlink(file)


def test_main_as_script():
    result = subprocess.run(
        ["python", "-m", "logs.main", "tests/sample.log", "--report", "handlers"],
        capture_output=True,
        text=True,
    )
    assert "" in result.stdout
