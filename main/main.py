import time

from core.browser import open_parabank
from core.logger import log_error, log_robot_starting, log_workflow_finished, log_user_separator
from data.config.settings import settings
from workflows.workflow import run_workflow


def _safe_close(browser, playwright) -> None:
    if browser:
        browser.close()
    if playwright:
        playwright.stop()


def main() -> None:
    playwright = None
    browser = None
    started_at = time.monotonic()
    try:
        log_robot_starting()
        log_user_separator()
        playwright, browser, page = open_parabank(settings)
        success, failures_count = run_workflow(page, settings)
        elapsed_seconds = time.monotonic() - started_at
        log_workflow_finished(success, failures_count, elapsed_seconds)
    except Exception as error:
        log_error(error)
    finally:
        _safe_close(browser, playwright)


if __name__ == "__main__":
    main()
