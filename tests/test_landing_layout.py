import pytest
from playwright.sync_api import Page

VIEWPORT_HEIGHT = 844


@pytest.mark.parametrize("width", [320, 390, 768, 1280])
def test_landing_page_does_not_scroll_horizontally(
    page: Page, live_server_url: str, width: int
) -> None:
    page.set_viewport_size({"width": width, "height": VIEWPORT_HEIGHT})

    page.goto(f"{live_server_url}/")

    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    inner_width = page.evaluate("window.innerWidth")
    assert scroll_width <= inner_width, (
        f"page is {scroll_width}px wide in a {inner_width}px viewport"
    )
