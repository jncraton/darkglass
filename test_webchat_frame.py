from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

# load the isolated frame html directly rather than the landing page
file_url = Path("static/widget_frame.html").resolve().as_uri()


@pytest.fixture
def root(page: Page):
    page.goto(file_url)
    return page


def test_widget_present_and_toggle(root):
    # the frame contains the widget container by default
    widget = root.locator("#darkglass")
    expect(widget).to_be_visible()

    # initial state should be "closed" with the class applied and a small
    # height; it is positioned relative within the frame rather than fixed.
    assert widget.evaluate("el => el.classList.contains('closed')")
    pos = widget.evaluate("el => getComputedStyle(el).position")
    assert pos == "relative"
    closed_height = widget.evaluate("el => getComputedStyle(el).height")
    assert closed_height == "40px"

    header = widget.locator(".header")
    expect(header).to_have_text("Chat")

    body = widget.locator(".body")
    expect(body).not_to_be_visible()

    # open and close by clicking the header
    header.click()
    expect(body).to_be_visible()
    assert not widget.evaluate("el => el.classList.contains('closed')")

    header.click()
    expect(body).not_to_be_visible()
    assert widget.evaluate("el => el.classList.contains('closed')")

    # clicking inside the body once open should not collapse it
    header.click()
    expect(body).to_be_visible()
    body.click()
    expect(body).to_be_visible()
