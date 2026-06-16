import pytest


@pytest.mark.skipif(
    'not any("PySide6" in m for m in __import__("sys").modules)'
    and 'not any("PySide6" in m for m in __import__("sys").builtin_module_names)',
    reason="PySide6 not available in headless environment",
)
def test_gui_imports():
    from basebender.gui.main_window import MainWindow, run_gui

    assert MainWindow is not None
    assert run_gui is not None
