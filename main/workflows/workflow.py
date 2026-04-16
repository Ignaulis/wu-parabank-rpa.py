from common.nav_page import logout, open_loan_page, open_open_account_page
from core.extract_data import load_users
from core.logger import log_user_separator
from workflows.loan.loan import run_loan_for_user
from workflows.open_account.open_account import run_open_account_for_user
from workflows.register.register import run_register_for_user


def run_workflow(page, settings) -> tuple[bool, int]:
    users = load_users()
    any_failed = False
    failed_users_count = 0

    for index, user in enumerate(users):
        is_last = index == len(users) - 1
        user_failed = False

        register_ok = run_register_for_user(page, user, settings)
        if not register_ok:
            any_failed = True
            failed_users_count += 1
            log_user_separator()
            continue

        user_ok = True
        try:
            open_open_account_page(page, settings)
            if not run_open_account_for_user(page, user, settings):
                user_ok = False
            else:
                open_loan_page(page, settings)
                if not run_loan_for_user(page, user, settings):
                    user_ok = False
        except Exception:
            user_ok = False

        if not user_ok:
            any_failed = True
            user_failed = True

        if page and not page.is_closed():
            try:
                logout(page, settings)
            except Exception:
                if not is_last:
                    any_failed = True
                    user_failed = True
        elif not is_last:
            any_failed = True
            user_failed = True

        if user_failed:
            failed_users_count += 1
        log_user_separator()

    success = not any_failed
    return success, failed_users_count
