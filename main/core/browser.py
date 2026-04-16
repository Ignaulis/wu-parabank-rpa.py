import subprocess
import time
from typing import Optional, Tuple

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from core.logger import (
    log_browser_killed,
    log_browser_opened,
    log_parabank_opened,
    log_retry_failed,
    log_retry_wait,
    log_stop_work,
)


def _map_browser(browser_name: str) -> str:
    normalized = browser_name.lower()
    if normalized == "chrome":
        return "chromium"
    if normalized == "edge":
        return "webkit"
    if normalized == "safari":
        return "webkit"
    return normalized


def _browser_process_name(browser_name: str) -> Optional[str]:
    normalized = browser_name.lower()
    if normalized in ("chrome", "chromium"):
        return "chrome.exe"
    if normalized == "edge":
        return "msedge.exe"
    if normalized == "firefox":
        return "firefox.exe"
    if normalized == "webkit":
        return "msedge.exe"
    return None


def kill_browser_process(browser_name: str) -> None:
    process_name = _browser_process_name(browser_name)
    if not process_name:
        return

    try:
        result = subprocess.run(
            ["taskkill", "/IM", process_name, "/F"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            log_browser_killed(browser_name)
    except Exception:
        pass


def _launch_browser(playwright: Playwright, mapped_browser: str, browser_visible: bool) -> Browser:
    headless = not browser_visible
    if mapped_browser == "chromium":
        return playwright.chromium.launch(headless=headless)
    if mapped_browser == "firefox":
        return playwright.firefox.launch(headless=headless)
    if mapped_browser == "webkit":
        return playwright.webkit.launch(headless=headless)
    raise ValueError(f"Unsupported browser: {mapped_browser}")


def _open_base_url_with_retry(page: Page, settings) -> None:
    for attempt in range(1, settings.max_retries + 1):
        try:
            page.goto(settings.base_url, timeout=settings.timeout_ms)
            log_parabank_opened()
            return
        except Exception as error:
            log_retry_failed(attempt, settings.max_retries, error)
            if attempt < settings.max_retries:
                log_retry_wait(settings.retry_delay_ms)
                time.sleep(settings.retry_delay_ms / 1000)
            else:
                raise


def _close_browser_session(browser: Browser, playwright: Playwright) -> None:
    browser.close()
    playwright.stop()


def validate_browser_preflight(settings) -> None:
    mapped_browser = _map_browser(settings.browser)
    if mapped_browser not in ("chromium", "firefox", "webkit"):
        raise ValueError(f"Unsupported browser option: {settings.browser}")

    playwright = sync_playwright().start()
    browser = None
    try:
        browser = _launch_browser(playwright, mapped_browser, settings.browser_visible)
    except Exception as error:
        raise RuntimeError(f"Cannot launch browser '{settings.browser}': {error}") from error
    finally:
        if browser:
            browser.close()
        playwright.stop()


def open_parabank(settings) -> Tuple[Playwright, Browser, Page]:
    mapped_browser = _map_browser(settings.browser)
    if settings.kill_on_start:
        kill_browser_process(settings.browser)

    playwright = sync_playwright().start()
    browser = _launch_browser(playwright, mapped_browser, settings.browser_visible)
    page = browser.new_page()
    log_browser_opened(settings.browser)

    try:
        _open_base_url_with_retry(page, settings)
        return playwright, browser, page
    except Exception:
        log_stop_work()
        _close_browser_session(browser, playwright)
        raise
