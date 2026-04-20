import time

from core.extract_data import UserProfile
from core.logger import (
    log_open_account_awaiting_result,
    log_open_account_failed,
    log_open_account_started,
    log_open_account_submit_clicked,
    log_open_account_success,
)
from core.page_errors import collect_visible_texts
from core.waits import wait_until

from .open_account_selectors import (
    ACCOUNT_TYPE_SELECT,
    FROM_ACCOUNT_SELECT,
    GLOBAL_ERROR_BLOCK,
    NEW_ACCOUNT_ID_LINK,
    NEW_ACCOUNT_RESULT,
    OPEN_NEW_ACCOUNT_FORM,
    OPEN_NEW_ACCOUNT_BUTTON,
)


class OpenAccountServerError(RuntimeError):
    pass


def _raise_if_internal_server_error(errors_text: str) -> None:
    if "an internal error has occurred" in errors_text.lower():
        raise OpenAccountServerError("Parabank server internal error: could not continue execution.")


# Surenka matomas open account klaidas
def collect_open_account_errors(page) -> str:
    base_errors = collect_visible_texts(page, [], global_selector_optional=GLOBAL_ERROR_BLOCK)
    internal_error_loc = page.get_by_text("An internal error has occurred", exact=False)
    if internal_error_loc.count() > 0 and internal_error_loc.first.is_visible():
        internal_error_text = (internal_error_loc.first.text_content() or "").strip()
        if base_errors:
            if internal_error_text and internal_error_text not in base_errors:
                return f"{base_errors} | Global: {internal_error_text}"
            return base_errors
        return f"Global: {internal_error_text or 'An internal error has occurred'}"
    return base_errors


# Uzpildo naujos saskaitos forma
def fill_open_account_form(page, user: UserProfile, settings) -> None:
    fast_timeout_ms = min(settings.timeout_ms, 4000)
    page.locator(OPEN_NEW_ACCOUNT_FORM).wait_for(timeout=settings.timeout_ms)
    from_select = page.locator(FROM_ACCOUNT_SELECT)
    from_select.wait_for(timeout=fast_timeout_ms)
    account_type_select = page.locator(ACCOUNT_TYPE_SELECT)
    account_type_select.wait_for(timeout=fast_timeout_ms)

    if user.account_type:
        account_type = user.account_type.strip().lower()
        try:
            if account_type == "checking":
                account_type_select.select_option(value="0", timeout=fast_timeout_ms)
            elif account_type == "savings":
                account_type_select.select_option(value="1", timeout=fast_timeout_ms)
            else:
                account_type_select.select_option(label=user.account_type, timeout=fast_timeout_ms)
        except Exception:
            if account_type == "checking":
                account_type_select.select_option(label="CHECKING", timeout=fast_timeout_ms)
            elif account_type == "savings":
                account_type_select.select_option(label="SAVINGS", timeout=fast_timeout_ms)
            else:
                raise

    def select_first_value():
        options = from_select.locator("option")
        if options.count() == 0:
            return None
        first_value = (options.first.get_attribute("value") or "").strip()
        if not first_value:
            return None
        from_select.select_option(value=first_value)
        return True

    result = wait_until(settings.timeout_ms, 0.2, select_first_value)
    if result is None:
        raise RuntimeError("fromAccountId options are not ready")


# Issiuncia open account uzklausa ir patikrina rezultata
def open_account_user(page, user: UserProfile, settings) -> bool:
    log_open_account_started(user.username)
    try:
        initial_errors = collect_open_account_errors(page)
        if initial_errors:
            _raise_if_internal_server_error(initial_errors)
            log_open_account_failed(user.username, initial_errors)
            return False

        fill_open_account_form(page, user, settings)
        log_open_account_submit_clicked()
        button = page.locator(OPEN_NEW_ACCOUNT_BUTTON).first
        button.wait_for(timeout=settings.timeout_ms)
        button.scroll_into_view_if_needed()
        if not button.is_enabled():
            raise RuntimeError("Open New Account button is disabled")

        selected_from_account = (
            page.locator(FROM_ACCOUNT_SELECT).locator("option:checked").first.get_attribute("value") or ""
        ).strip()
        if not selected_from_account:
            raise RuntimeError("fromAccountId has no selected value")

        button.click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)

        # Greitas terminalinis kelias: jei iskart matoma globali klaida, nebelaukiame pilno timeout
        immediate_errors = collect_open_account_errors(page)
        if immediate_errors:
            _raise_if_internal_server_error(immediate_errors)
            log_open_account_failed(user.username, immediate_errors)
            return False

        def condition():
            new_account_id = page.locator(NEW_ACCOUNT_ID_LINK)
            if new_account_id.count() > 0 and new_account_id.first.is_visible():
                account_id = (new_account_id.first.text_content() or "").strip()
                if account_id:
                    log_open_account_success(user.username)
                    return True

            result_block = page.locator(NEW_ACCOUNT_RESULT)
            if result_block.count() > 0 and result_block.first.is_visible():
                result_text = (result_block.first.text_content() or "").strip()
                if result_text:
                    log_open_account_success(user.username)
                    return True

            errors_text = collect_open_account_errors(page)
            if errors_text:
                _raise_if_internal_server_error(errors_text)
                log_open_account_failed(user.username, errors_text)
                return False

            return None

        log_open_account_awaiting_result()
        open_account_timeout_ms = min(settings.timeout_ms, 6000)
        result = wait_until(open_account_timeout_ms, 0.2, condition)
        if result is not None:
            return result

        timeout_message = "Timeout waiting open account result"
        log_open_account_failed(user.username, timeout_message)
        return False
    except OpenAccountServerError:
        raise
    except Exception as error:
        error_text = str(error)
        log_open_account_failed(user.username, error_text)
        return False
