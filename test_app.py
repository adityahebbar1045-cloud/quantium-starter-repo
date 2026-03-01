import os
import pytest
from dash.testing.composite import DashComposite
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from app import app  # Imports your Dash app object


# --- FIXTURE: Handles the ChromeDriver PATH and Headless mode ---
@pytest.fixture(scope="function")
def dash_duo(dash_thread_server, tmpdir):
    # 1. Ensure driver is installed and get the path
    driver_path = ChromeDriverManager().install()

    # 2. Inject the driver directory into the system PATH
    driver_dir = os.path.dirname(driver_path)
    os.environ["PATH"] += os.pathsep + driver_dir

    # 3. Chrome Options for a clean test run
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without browser window
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # 4. Initialize DashComposite
    with DashComposite(dash_thread_server, browser="chrome", options=options) as dc:
        yield dc


# --- TESTS: Verifying the Dashboard UI Components ---


def test_header_presence(dash_duo):
    """TC-1: Verify the header is present and visible."""
    dash_duo.start_server(app)
    # Most Dash headers use an <h1> tag
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsel" in header.text


def test_visualization_presence(dash_duo):
    """TC-2: Verify the line chart is rendered."""
    dash_duo.start_server(app)
    # This ID must match the id used in dcc.Graph in app.py
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    chart = dash_duo.find_element("#sales-line-chart")
    assert chart is not None


def test_region_picker_presence(dash_duo):
    """TC-3: Verify the region selection radio buttons/dropdown is present."""
    dash_duo.start_server(app)
    # This ID must match the id used in dcc.RadioItems or dcc.Dropdown
    dash_duo.wait_for_element("#region-filter", timeout=10)
    picker = dash_duo.find_element("#region-filter")
    assert picker is not None
