from datetime import datetime


def log_event(event_name: str, message: str) -> None:
    del event_name
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def log_info(message: str) -> None:
    log_event("info", message)


def log_browser_killed(browser_name: str) -> None:
    log_info(f"Browser {browser_name} killed")


def log_browser_opened(browser_name: str) -> None:
    log_info(f"Browser {browser_name} opened")


def log_parabank_opened() -> None:
    log_info("Parabank opened")


def log_error(error: Exception) -> None:
    log_info(f"Error: {error}")


def log_robot_starting() -> None:
    log_info("--> ParaBank Robot starting")


def get_stop_prompt() -> str:
    return "Press Enter to stop..."


def log_retry_failed(current_attempt: int, max_retries: int, error: Exception) -> None:
    log_info(f"Retry {current_attempt}/{max_retries} failed: {error}")


def log_retry_wait(delay_ms: int) -> None:
    log_info(f"Retrying in {delay_ms} ms...")


def log_stop_work() -> None:
    log_info("All retries failed. Stop work.")


def log_opening_register_page() -> None:
    log_info("Opening register page")


def log_register_page_opened() -> None:
    log_info("Register page opened")


def log_register_page_open_failed(error: Exception) -> None:
    log_info(f"Register page open failed: {error}")


def log_register_user_started(username: str) -> None:
    log_info(f"Register user started: {username}")


def log_register_submit_clicked() -> None:
    log_info("Register submit clicked")


def log_register_success(username: str) -> None:
    log_info(f"Register success: {username}")


def log_register_failed(username: str, errors_text: str) -> None:
    if errors_text:
        log_info(f"Register failed: {username}. Errors: {errors_text}")
    else:
        log_info(f"Register failed: {username}. Errors: (none)")


def log_opening_open_account_page() -> None:
    log_info("Opening open account page")


def log_open_account_page_opened() -> None:
    log_info("Open account page opened")


def log_open_account_page_open_failed(error: Exception) -> None:
    log_info(f"Open account page open failed: {error}")


def log_logout_started() -> None:
    log_info("Logout started")


def log_logout_success() -> None:
    log_info("Logout success")


def log_logout_failed(error: Exception) -> None:
    log_info(f"Logout failed: {error}")


def log_open_account_started(username: str) -> None:
    log_info(f"Open account started: {username}")


def log_open_account_submit_clicked() -> None:
    log_info("Open account submit clicked")


def log_open_account_success(username: str) -> None:
    log_info(f"Open account success: {username}")


def log_open_account_failed(username: str, errors_text: str) -> None:
    if errors_text:
        log_info(f"Open account failed: {username}. Errors: {errors_text}")
    else:
        log_info(f"Open account failed: {username}. Errors: (none)")


def log_opening_loan_page() -> None:
    log_info("Opening loan page")


def log_loan_page_opened() -> None:
    log_info("Loan page opened")


def log_loan_page_open_failed(error: Exception) -> None:
    log_info(f"Loan page open failed: {error}")


def log_loan_started(username: str) -> None:
    log_info(f"Loan started: {username}")


def log_loan_submit_clicked() -> None:
    log_info("Loan submit clicked")


def log_loan_success(username: str) -> None:
    log_info(f"Loan success: {username}")


def log_loan_failed(username: str, errors_text: str) -> None:
    if errors_text:
        log_info(f"Loan failed: {username}. Errors: {errors_text}")
    else:
        log_info(f"Loan failed: {username}. Errors: (none)")


def log_workflow_finished(success: bool, failures_count: int, elapsed_seconds: float) -> None:
    elapsed_text = f"{elapsed_seconds:.2f}s"
    if success:
        log_info(f"--> ParaBank Robot finished. Failures: {failures_count}. Duration: {elapsed_text}")
    else:
        log_info(
            f"--> ParaBank Robot finished with failures. Failures: {failures_count}. Duration: {elapsed_text}"
        )


def log_user_separator() -> None:
    log_info(".......................")


def log_currency_rate(rate: float, source: str) -> None:
    log_info(f"Currency rate USD->EUR: {rate:.4f} ({source})")


def log_report_saved(report_path: str) -> None:
    log_info(f"Report saved: {report_path}")


def log_startup_options(mode: str, settings) -> None:
    log_info(
        "Startup options: "
        f"mode={mode}, "
        f"kill_on_start={settings.kill_on_start}, "
        f"browser={settings.browser}, "
        f"browser_visible={settings.browser_visible}, "
        f"desktop_report={settings.desktop_report}, "
        f"report_type={settings.report_type}"
    )
