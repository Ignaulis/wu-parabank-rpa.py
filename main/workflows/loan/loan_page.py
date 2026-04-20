import time

from core.extract_data import UserProfile
from core.logger import (
    log_loan_failed,
    log_loan_started,
    log_loan_submit_clicked,
    log_loan_success,
)
from core.page_errors import collect_visible_texts
from core.waits import wait_until

from .loan_selectors import (
    APPLY_LOAN_BUTTON,
    DOWN_PAYMENT_INPUT,
    GLOBAL_ERROR_BLOCK,
    LOAN_AMOUNT_INPUT,
    LOAN_APPROVED_BLOCK,
    LOAN_DENIED_BLOCK,
)


class LoanServerError(RuntimeError):
    pass


def _raise_if_internal_server_error(errors_text: str) -> None:
    if "an internal error has occurred" in errors_text.lower():
        raise LoanServerError("Parabank server internal error: negalejo testi darbo.")


# Surenka matomas paskolos klaidas
def collect_loan_errors(page) -> str:
    mapping = [("Denied", LOAN_DENIED_BLOCK)]
    base_errors = collect_visible_texts(page, mapping, global_selector_optional=GLOBAL_ERROR_BLOCK)
    internal_error_loc = page.get_by_text("An internal error has occurred", exact=False)
    if internal_error_loc.count() > 0 and internal_error_loc.first.is_visible():
        internal_error_text = (internal_error_loc.first.text_content() or "").strip()
        if base_errors:
            if internal_error_text and internal_error_text not in base_errors:
                return f"{base_errors} | Global: {internal_error_text}"
            return base_errors
        return f"Global: {internal_error_text or 'An internal error has occurred'}"
    return base_errors


# Uzpildo paskolos formos laukus
def fill_loan_form(page, user: UserProfile, settings) -> None:
    loan_amount = settings.loan_amount
    down_payment = 0.0
    if user.initial_deposit is not None:
        down_payment = round(user.initial_deposit * settings.down_payment_pct, 2)

    page.locator(LOAN_AMOUNT_INPUT).fill(str(loan_amount))
    page.locator(DOWN_PAYMENT_INPUT).fill(str(down_payment))


# Issiuncia paskolos uzklausa ir patikrina rezultata
def request_loan_user(page, user: UserProfile, settings) -> bool:
    log_loan_started(user.username)
    try:
        initial_errors = collect_loan_errors(page)
        if initial_errors:
            _raise_if_internal_server_error(initial_errors)
            log_loan_failed(user.username, initial_errors)
            return False

        fill_loan_form(page, user, settings)
        log_loan_submit_clicked()
        page.locator(APPLY_LOAN_BUTTON).click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)

        def condition():
            approved = page.locator(LOAN_APPROVED_BLOCK)
            if approved.count() > 0 and approved.first.is_visible():
                approved_text = (approved.first.text_content() or "").strip()
                if approved_text:
                    log_loan_success(user.username)
                    return True

            errors_text = collect_loan_errors(page)
            if errors_text:
                _raise_if_internal_server_error(errors_text)
                log_loan_failed(user.username, errors_text)
                return False

            return None

        result = wait_until(settings.timeout_ms, 0.2, condition)
        if result is not None:
            return result

        final_errors = collect_loan_errors(page)
        if final_errors:
            _raise_if_internal_server_error(final_errors)
            log_loan_failed(user.username, final_errors)
            return False

        log_loan_failed(user.username, "Timeout waiting loan result")
        return False
    except LoanServerError:
        raise
    except Exception as error:
        errors_text = collect_loan_errors(page)
        if errors_text:
            _raise_if_internal_server_error(errors_text)
        combined_errors = f"{errors_text} | Exception: {error}" if errors_text else str(error)
        log_loan_failed(user.username, combined_errors)
        return False
