import time

from core.extract_data import UserProfile
from core.logger import (
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


def collect_open_account_errors(page) -> str:
    return collect_visible_texts(page, [], global_selector_optional=GLOBAL_ERROR_BLOCK)


def fill_open_account_form(page, user: UserProfile, settings) -> None:
    page.locator(OPEN_NEW_ACCOUNT_FORM).wait_for(timeout=settings.timeout_ms)
    from_select = page.locator(FROM_ACCOUNT_SELECT)
    from_select.wait_for(timeout=settings.timeout_ms)

    if user.account_type:
        account_type = user.account_type.strip().lower()
        try:
            if account_type == "checking":
                page.locator(ACCOUNT_TYPE_SELECT).select_option(value="0")
            elif account_type == "savings":
                page.locator(ACCOUNT_TYPE_SELECT).select_option(value="1")
            else:
                page.locator(ACCOUNT_TYPE_SELECT).select_option(label=user.account_type)
        except Exception:
            if account_type == "checking":
                page.locator(ACCOUNT_TYPE_SELECT).select_option(label="CHECKING")
            elif account_type == "savings":
                page.locator(ACCOUNT_TYPE_SELECT).select_option(label="SAVINGS")
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


def open_account_user(page, user: UserProfile, settings) -> bool:
    log_open_account_started(user.username)
    try:
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
                log_open_account_failed(user.username, errors_text)
                return False

            return None

        result = wait_until(settings.timeout_ms, 0.2, condition)
        if result is not None:
            return result

        log_open_account_failed(user.username, "Timeout waiting open account result")
        return False
    except Exception as error:
        log_open_account_failed(user.username, str(error))
        return False
