import tempfile
from logs.parser import parse_log_file

sample_log = """
[INFO] django.request log message /api/v1/products/
[ERROR] django.request log message /api/v1/products/
[DEBUG] django.request log message /api/v1/orders/
"""


def test_parse_log_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(sample_log)
        tmp.seek(0)
        result = parse_log_file(tmp.name)

    assert result["/api/v1/products/"]["INFO"] == 1
    assert result["/api/v1/products/"]["ERROR"] == 1
    assert result["/api/v1/orders/"]["DEBUG"] == 1
