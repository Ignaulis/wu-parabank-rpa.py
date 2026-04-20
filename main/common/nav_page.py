import time

from core.logger import (
    log_logout_failed,
    log_logout_started,
    log_logout_success,
    log_loan_page_open_failed,
    log_loan_page_opened,
    log_loan_page_sidebar_timeout_fallback,
    log_opening_loan_page,
    log_open_account_page_open_failed,
    log_open_account_page_opened,
    log_opening_open_account_page,
    log_opening_register_page,
    log_register_page_open_failed,
    log_register_page_opened,
)
from workflows.loan.loan_page import LoanServerError
from workflows.register.register_selectors import FIRST_NAME_INPUT, REGISTER_LINK
from workflows.open_account.open_account_selectors import (
    OPEN_NEW_ACCOUNT_FORM,
    OPEN_NEW_ACCOUNT_LINK,
)
from workflows.loan.loan_selectors import LOAN_AMOUNT_INPUT, REQUEST_LOAN_LINK

LOGOUT_LINK = "a[href*='logout.htm']"
POST_LOGOUT_MARKER = "input[name='username']"


# Atidaro registracijos puslapi
def open_register_page(page, settings) -> None:
    try:
        log_opening_register_page()
        page.locator(REGISTER_LINK).click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)
        page.locator(FIRST_NAME_INPUT).wait_for(timeout=settings.timeout_ms)
        log_register_page_opened()
    except Exception as error:
        log_register_page_open_failed(error)
        raise


# Atidaro naujos saskaitos puslapi
def open_open_account_page(page, settings) -> None:
    try:
        log_opening_open_account_page()
        page.locator(OPEN_NEW_ACCOUNT_LINK).click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)
        page.locator(OPEN_NEW_ACCOUNT_FORM).wait_for(timeout=settings.timeout_ms)
        log_open_account_page_opened()
    except Exception as error:
        log_open_account_page_open_failed(error)
        raise


# Atsijungia is sistemos
def logout(page, settings) -> None:
    try:
        log_logout_started()
        page.locator(LOGOUT_LINK).click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)
        page.locator(POST_LOGOUT_MARKER).wait_for(timeout=settings.timeout_ms)
        log_logout_success()
    except Exception as error:
        log_logout_failed(error)
        raise


# Atidaro paskolos puslapi
def open_loan_page(page, settings) -> None:
    try:
        log_opening_loan_page()
        short_timeout_ms = min(settings.timeout_ms, 4000)
        page.locator(REQUEST_LOAN_LINK).click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)
        if page.get_by_text("An internal error has occurred", exact=False).first.is_visible():
            raise LoanServerError("Parabank server internal error: negalejo testi darbo.")
        try:
            page.locator(LOAN_AMOUNT_INPUT).wait_for(timeout=short_timeout_ms)
            log_loan_page_opened()
            return
        except Exception:
            log_loan_page_sidebar_timeout_fallback()

        loan_url = str(settings.base_url).replace("index.htm", "requestloan.htm")
        page.goto(loan_url)
        if page.get_by_text("An internal error has occurred", exact=False).first.is_visible():
            raise LoanServerError("Parabank server internal error: negalejo testi darbo.")
        page.locator(LOAN_AMOUNT_INPUT).wait_for(timeout=settings.timeout_ms)
        log_loan_page_opened()
    except Exception as error:
        log_loan_page_open_failed(error)
        raise
