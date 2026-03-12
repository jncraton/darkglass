from pathlib import Path
import pytest
from playwright.sync_api import Page, expect
import darkglass

# load the static admin page directly; assets live next to the package
file_url = (
    (Path(darkglass.__file__).parent / "static" / "admin.html").resolve().as_uri()
)


@pytest.fixture
def root(page: Page):
    page.goto(file_url)
    return page


def test_page_title_and_header(root):
    expect(root).to_have_title("Chat Log")
    header = root.locator("header h1")
    expect(header).to_have_text("Chat Log")
