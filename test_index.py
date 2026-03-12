import re
from playwright.sync_api import Page, expect
import pytest

from pathlib import Path
import darkglass

# static assets are installed alongside the package
file_url = (
    (Path(darkglass.__file__).parent / "static" / "index.html").resolve().as_uri()
)


@pytest.fixture
def root(page: Page):
    page.goto(f"{file_url}#")
    return page


def test_page_title(root):
    expect(root).to_have_title("Example University")
