from pathlib import Path
import pytest
from playwright.sync_api import Page, expect
import darkglass

file_url = (
    (Path(darkglass.__file__).parent / "static" / "webchat.html").resolve().as_uri()
)


@pytest.fixture
def root(page: Page):
    page.goto(file_url)
    return page


def test_widget_present_and_toggle(root):
    widget = root.locator("#darkglass")
    expect(widget).to_be_visible()

    assert widget.evaluate("el => el.classList.contains('closed')")
    pos = widget.evaluate("el => getComputedStyle(el).position")
    assert pos == "relative"
    closed_height = widget.evaluate("el => getComputedStyle(el).height")
    assert closed_height == "36px"

    header = widget.locator(".header")
    expect(header).to_have_text("Chat")

    body = widget.locator(".body")
    expect(body).not_to_be_visible()

    header.click()
    expect(body).to_be_visible()
    assert not widget.evaluate("el => el.classList.contains('closed')")

    header.click()
    expect(body).not_to_be_visible()
    assert widget.evaluate("el => el.classList.contains('closed')")

    header.click()
    expect(body).to_be_visible()
    body.click()
    expect(body).to_be_visible()
