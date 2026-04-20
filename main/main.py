import time

from core.browser import open_parabank, validate_browser_preflight
from core.cmd_prompt import prompt_runtime_settings
from core.logger import (
    log_error,
    log_robot_starting,
    log_startup_options,
    log_workflow_finished,
    log_user_separator,
)
from data.config.settings import settings
from workflows.workflow import run_workflow


# Saugiai uzdaro browser ir playwright resursus
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
        # 1 Surenka paleidimo nustatymus
        resolved_settings, mode = prompt_runtime_settings(settings)

        # 2 Uzlogina paleidimo informacija
        log_robot_starting()
        log_startup_options(mode, resolved_settings)

        # 3 Patikrina ar narsykle gali pasileisti
        validate_browser_preflight(resolved_settings)
        log_user_separator()

        # 4 Atidaro Parabank ir paleidzia visa workflow
        playwright, browser, page = open_parabank(resolved_settings)
        success, failures_count, _report_path = run_workflow(page, resolved_settings)

        # 5 Uzfiksuoja galutini rezultata ir trukme
        elapsed_seconds = time.monotonic() - started_at
        log_workflow_finished(success, failures_count, elapsed_seconds)
    except Exception as error:
        # Klaidos atveju uzlogina exception
        log_error(error)
    finally:
        # Visada tvarkingai uzdaro resursus
        _safe_close(browser, playwright)


if __name__ == "__main__":
    main()
