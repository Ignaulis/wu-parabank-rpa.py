import time

from core.logger import (
    log_register_failed,
    log_register_submit_clicked,
    log_register_success,
)
from core.page_errors import collect_visible_texts
from core.waits import wait_until

from .register_selectors import (
    ADDRESS_ERROR,
    ADDRESS_INPUT,
    CITY_ERROR,
    CITY_INPUT,
    FIRST_NAME_ERROR,
    FIRST_NAME_INPUT,
    GLOBAL_ERROR_BLOCK,
    LAST_NAME_INPUT,
    LAST_NAME_ERROR,
    PASSWORD_INPUT,
    PASSWORD_ERROR,
    PHONE_INPUT,
    ZIP_CODE_INPUT,
    REPEATED_PASSWORD_INPUT,
    REPEATED_PASSWORD_ERROR,
    REGISTER_BUTTON,
    SSN_ERROR,
    SSN_INPUT,
    SUCCESS_ACCOUNT_CREATED_TEXT,
    STATE_ERROR,
    STATE_INPUT,
    ZIP_CODE_ERROR,
    USERNAME_ERROR,
    USERNAME_INPUT,
    USERNAME_TAKEN_ERROR,
)

from core.extract_data import UserProfile


def fill_registration_form(page, user: UserProfile, settings) -> None:
    page.locator(FIRST_NAME_INPUT).fill(user.first_name)
    page.locator(LAST_NAME_INPUT).fill(user.last_name)
    page.locator(ADDRESS_INPUT).fill(user.address)
    page.locator(CITY_INPUT).fill(user.city)
    page.locator(STATE_INPUT).fill(user.state)
    page.locator(ZIP_CODE_INPUT).fill(user.zip_code)
    page.locator(PHONE_INPUT).fill(user.phone_number)
    page.locator(SSN_INPUT).fill(user.ssn)
    page.locator(USERNAME_INPUT).fill(user.username)
    page.locator(PASSWORD_INPUT).fill(user.password)
    page.locator(REPEATED_PASSWORD_INPUT).fill(user.password)


def collect_field_errors(page) -> str:
    mapping = [
        ("First Name", FIRST_NAME_ERROR),
        ("Last Name", LAST_NAME_ERROR),
        ("Address", ADDRESS_ERROR),
        ("City", CITY_ERROR),
        ("State", STATE_ERROR),
        ("Zip Code", ZIP_CODE_ERROR),
        ("SSN", SSN_ERROR),
        ("Username", USERNAME_ERROR),
        ("Username Taken", USERNAME_TAKEN_ERROR),
        ("Password", PASSWORD_ERROR),
        ("Repeated Password", REPEATED_PASSWORD_ERROR),
    ]
    return collect_visible_texts(page, mapping, global_selector_optional=GLOBAL_ERROR_BLOCK)


def register_user(page, user: UserProfile, settings) -> bool:
    fill_registration_form(page, user, settings)

    try:
        log_register_submit_clicked()
        page.locator(REGISTER_BUTTON).click()
        if settings.click_delay_ms:
            time.sleep(settings.click_delay_ms / 1000)
    except Exception as error:
        errors_text = collect_field_errors(page)
        combined = f"{errors_text} | Exception: {error}" if errors_text else str(error)
        log_register_failed(user.username, combined)
        return False

    def condition():
        if page.locator(SUCCESS_ACCOUNT_CREATED_TEXT).count() > 0:
            log_register_success(user.username)
            return True

        errors_text = collect_field_errors(page)
        if errors_text:
            log_register_failed(user.username, errors_text)
            return False

        return None

    result = wait_until(settings.timeout_ms, 0.2, condition)
    if result is not None:
        return result

    log_register_failed(user.username, "Timeout waiting register result")
    return False

