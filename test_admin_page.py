from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

# load the static admin page directly
file_url = Path("static/admin.html").resolve().as_uri()


@pytest.fixture
def root(page: Page):
    page.goto(file_url)
    return page


def test_page_title_and_header(root):
    expect(root).to_have_title("Admin - Darkglass")
    header = root.locator("header h1")
    expect(header).to_have_text("Admin - Darkglass")
