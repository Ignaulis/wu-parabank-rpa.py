from datetime import datetime

from common.nav_page import logout, open_loan_page, open_open_account_page
from core.extract_data import load_users
from core.logger import log_currency_rate, log_fatal_user_flow_stop, log_report_saved, log_user_separator
from core.report_writer import write_report
from data.api.currency_rates import get_usd_to_eur_rate
from workflows.loan.loan import LoanServerError, run_loan_for_user
from workflows.open_account.open_account import OpenAccountServerError, run_open_account_for_user
from workflows.register.register import run_register_for_user


# Grazina statuso svarba palyginimui
def _status_rank(status: str) -> int:
    if status == "ERROR":
        return 3
    if status == "FAIL":
        return 2
    return 1


# Apskaiciuoja bendra vartotojo statusa
def _overall_status(*statuses: str) -> str:
    worst = "PASS"
    for status in statuses:
        if _status_rank(status) > _status_rank(worst):
            worst = status
    return worst


# Vykdo visa scenariju visiems vartotojams ir sukuria ataskaita
def run_workflow(page, settings) -> tuple[bool, int, str]:
    # Uzsikrauna vartotojus ir valiutos kursa vienam paleidimui
    users = load_users()
    usd_to_eur_rate, rate_source = get_usd_to_eur_rate(settings)
    log_currency_rate(usd_to_eur_rate, rate_source)
    any_failed = False
    failed_users_count = 0
    report_rows: list[dict] = []
    fatal_stop = False

    # Apdoroja kiekviena vartotoja atskirai
    for index, user in enumerate(users):
        is_last = index == len(users) - 1
        register_status = "PASS"
        open_account_status = "PASS"
        loan_status = "PASS"
        logout_status = "PASS"
        failed_step = ""
        error_message = ""

        # Pasiruosia finansines reiksmes ataskaitai
        loan_amount_usd = float(settings.loan_amount)
        initial_deposit = user.initial_deposit if user.initial_deposit is not None else 0.0
        down_payment_usd = round(initial_deposit * settings.down_payment_pct, 2)
        loan_amount_eur = round(loan_amount_usd * usd_to_eur_rate, 2)
        down_payment_eur = round(down_payment_usd * usd_to_eur_rate, 2)

        # 1 zingsnis registracija
        try:
            register_ok = run_register_for_user(page, user, settings)
            if not register_ok:
                register_status = "FAIL"
                failed_step = "register"
        except Exception as error:
            register_status = "ERROR"
            failed_step = "register"
            error_message = str(error)

        # Jei registracija nepraeina tolesni zingsniai zymimi kaip nepraeje
        if register_status != "PASS":
            open_account_status = "FAIL"
            loan_status = "FAIL"
            logout_status = "FAIL"
        else:
            user_ok = True
            stop_current_user_flow = False
            # 2 zingsnis naujos saskaitos atidarymas
            try:
                open_open_account_page(page, settings)
                open_account_ok = run_open_account_for_user(page, user, settings)
                if not open_account_ok:
                    open_account_status = "FAIL"
                    failed_step = "open_account"
                    error_message = "open_account step failed"
            except OpenAccountServerError as error:
                open_account_status = "ERROR"
                failed_step = "open_account"
                error_message = f"{error} Robot could not continue execution."
                user_ok = False
                stop_current_user_flow = True
                fatal_stop = True
                log_fatal_user_flow_stop(user.username, failed_step)
            except Exception as error:
                open_account_status = "ERROR"
                failed_step = "open_account"
                error_message = str(error)

            # 3 zingsnis paskolos uzklausa (vykdomas ir po open account FAIL)
            if not stop_current_user_flow:
                try:
                    open_loan_page(page, settings)
                    loan_ok = run_loan_for_user(page, user, settings)
                    if not loan_ok:
                        loan_status = "FAIL"
                        if not failed_step:
                            failed_step = "loan"
                        if not error_message:
                            error_message = "loan step failed"
                        user_ok = False
                except LoanServerError as error:
                    loan_status = "ERROR"
                    failed_step = "loan"
                    error_message = f"{error} Robot could not continue execution."
                    user_ok = False
                    stop_current_user_flow = True
                    fatal_stop = True
                    log_fatal_user_flow_stop(user.username, failed_step)
                except Exception as error:
                    loan_status = "ERROR"
                    if not failed_step:
                        failed_step = "loan"
                    if not error_message:
                        error_message = str(error)
                    user_ok = False

            # 4 zingsnis atsijungimas po veiksmu
            if not stop_current_user_flow and page and not page.is_closed():
                try:
                    logout(page, settings)
                except Exception as error:
                    logout_status = "ERROR"
                    if not failed_step:
                        failed_step = "logout"
                        error_message = str(error)
                    user_ok = False
            elif not is_last:
                logout_status = "FAIL"
                if not failed_step:
                    failed_step = "logout"
                    error_message = "Page closed before logout"
                user_ok = False

            if not user_ok and logout_status == "PASS":
                logout_status = "FAIL"

        # Jei nera konkretaus exception teksto suformuoja bendra zinute
        if not error_message and failed_step:
            error_message = f"{failed_step} step failed"

        # Suskaiciuoja bendra statusa ir kaupia nesekmiu statistika
        overall_status = _overall_status(register_status, open_account_status, loan_status, logout_status)
        if overall_status != "PASS":
            any_failed = True
            failed_users_count += 1

        # Prideda vartotojo eilute i galutine ataskaita
        report_rows.append(
            {
                "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "dob": user.dob,
                "debit_card": user.debit_card,
                "cvv": user.cvv,
                "account_type": user.account_type,
                "initial_deposit": initial_deposit,
                "loan_amount_usd": loan_amount_usd,
                "down_payment_usd": down_payment_usd,
                "loan_amount_eur": loan_amount_eur,
                "down_payment_eur": down_payment_eur,
                "usd_to_eur_rate": usd_to_eur_rate,
                "rate_source": rate_source,
                "report_currency": "EUR",
                "register_status": register_status,
                "open_account_status": open_account_status,
                "loan_status": loan_status,
                "logout_status": logout_status,
                "overall_status": overall_status,
                "failed_step": failed_step,
                "error_message": error_message,
            }
        )

        log_user_separator()
        if fatal_stop:
            break

    # Issaugo ataskaita ir grazina paleidimo suvestine
    report_path = write_report(report_rows, settings)
    log_report_saved(report_path)
    success = not any_failed
    return success, failed_users_count, report_path
