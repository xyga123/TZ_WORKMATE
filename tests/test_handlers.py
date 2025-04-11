from logs.handlers import HandlersReport


def test_generate_handler_report(capsys):
    logs = [
        {"/test/": {"DEBUG": 1, "INFO": 2}},
        {"/test/": {"ERROR": 1}, "/api/": {"INFO": 3}},
    ]
    report = HandlersReport()
    report.generate(logs)

    captured = capsys.readouterr()
    assert "Всего логов: 7" in captured.out
    assert "/test/" in captured.out
    assert "/api/" in captured.out
