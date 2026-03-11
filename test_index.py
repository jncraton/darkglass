import re
from playwright.sync_api import Page, expect
import pytest

from pathlib import Path

file_url = Path("static/index.html").resolve().as_uri()


@pytest.fixture
def root(page: Page):
    page.goto(f"{file_url}#")
    return page


def test_page_title(root):
    expect(root).to_have_title("Example University")


def test_widget_present_and_toggle(root):
    # the widget should inject a container with id `darkglass` and a header
    widget = root.locator("#darkglass")
    expect(widget).to_be_visible()

    # basic style checks; should be fixed in the viewport
    # use evaluate to read computed style properties
    pos = widget.evaluate("el => getComputedStyle(el).position")
    assert pos == "fixed"
    bot = widget.evaluate("el => getComputedStyle(el).bottom")
    assert bot in ("20px", "20px")

    header = widget.locator(".header")
    expect(header).to_have_text("Chat")

    # initial state is closed; body should not be visible
    body = widget.locator(".body")
    expect(body).not_to_be_visible()

    # clicking header should expand and show body
    header.click()
    expect(body).to_be_visible()

    # clicking again should collapse
    header.click()
    expect(body).not_to_be_visible()
