from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_streamlit_app_runs_and_produces_prediction():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path), default_timeout=40)
    app.run()
    assert len(app.exception) == 0
    assert len(app.button) == 1

    app.button[0].click().run()
    assert len(app.exception) == 0
    labels = {metric.label for metric in app.metric}
    assert "Risk olasılığı" in labels
