from core.extract_data import UserProfile

from .open_account_page import OpenAccountServerError, open_account_user


# Paleidzia naujos saskaitos atidarymo veiksma
def run_open_account_for_user(page, user: UserProfile, settings) -> bool:
    return open_account_user(page, user, settings)
