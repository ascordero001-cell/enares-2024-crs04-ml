import csv
from pathlib import Path

import pytest

from scripts.container_healthcheck import check_health, health_url
from scripts.release_diagnostic import diagnose_release, require_single_release

ROOT = Path(__file__).resolve().parents[1]
AUTHORIZED_EXTRACTS = (
    "v0_authorized_indicator_estimates.csv",
    "v0_authorized_etapa1_indicator_estimates.csv",
    "v0_authorized_d06_d07_indicator_estimates.csv",
)


class FakeResponse:
    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self) -> bytes:
        return self.body


def test_health_check_uses_local_tested_streamlit_route():
    calls = []

    def opener(url, timeout):
        calls.append((url, timeout))
        return FakeResponse(200, b"ok")

    check_health(opener=opener, port="8080")
    assert calls == [("http://127.0.0.1:8080/_stcore/health", 2)]


@pytest.mark.parametrize("port", ["0", "65536", "abc", "８０８０"])
def test_health_check_rejects_invalid_ports(port):
    with pytest.raises(ValueError, match="PORT"):
        health_url(port)


def test_health_check_rejects_non_ok_response():
    def opener(_url, timeout):
        assert timeout == 2
        return FakeResponse(200, b"not ready")

    with pytest.raises(RuntimeError, match="200/ok"):
        check_health(opener=opener)


def test_release_diagnostic_validates_all_modules_and_expected_release():
    result = diagnose_release("enares2024-crs04-v0-shadow-001")
    assert result["status"] == "ok"
    assert result["release_id"] == "enares2024-crs04-v0-shadow-001"
    assert set(result["modules"]) == {"3.1", "3.2", "3.3", "3.4", "3.5", "3.6"}
    assert all(count > 0 for count in result["modules"].values())
    assert result["cloud"] == "NOT_AUTHORIZED"


def test_release_diagnostic_fails_closed_on_wrong_release():
    with pytest.raises(RuntimeError, match="does not match"):
        diagnose_release("unexpected-release")


def test_release_diagnostic_fails_closed_on_multiple_authorized_release_ids():
    with pytest.raises(RuntimeError, match="exactly one release_id"):
        require_single_release(
            {
                "enares2024-crs04-v0-shadow-001",
                "enares2024-crs04-v0-shadow-etapa1-001",
            }
        )


def test_all_authorized_extracts_share_the_golden_release_id():
    release_ids: set[str] = set()
    for file_name in AUTHORIZED_EXTRACTS:
        path = ROOT / "app" / "data" / file_name
        with path.open(encoding="utf-8", newline="") as handle:
            release_ids.update(row["release_id"] for row in csv.DictReader(handle))
    assert release_ids == {"enares2024-crs04-v0-shadow-001"}


def test_container_contract_starts_pinned_streamlit_with_healthcheck():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    requirements = (ROOT / "requirements-runtime.txt").read_text(encoding="utf-8")
    assert "streamlit==1.63.0" in requirements
    assert "requirements-runtime.txt" in dockerfile
    assert "-r requirements.txt" not in dockerfile
    assert "EXPOSE 8080" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "scripts/container_healthcheck.py" in dockerfile
    assert "python -m streamlit run app/streamlit_app.py" in dockerfile
    assert 'CMD ["python", "-m", "compileall"' not in dockerfile


def test_runtime_dependencies_exclude_data_and_cloud_clients():
    requirements = {
        line.strip()
        for line in (ROOT / "requirements-runtime.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert requirements == {"streamlit==1.63.0"}
    assert not any(
        package in dependency
        for dependency in requirements
        for package in (
            "pyreadstat",
            "google-api-python-client",
            "google-auth-oauthlib",
            "google-cloud-bigquery",
        )
    )
