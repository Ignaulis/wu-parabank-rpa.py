from common.nav_page import open_register_page
from core.extract_data import UserProfile
from core.logger import log_register_failed, log_register_user_started

from .register_page import register_user


# Atidaro registracija ir paleidzia registravimo veiksma
def run_register_for_user(page, user: UserProfile, settings) -> bool:
    log_register_user_started(user.username)
    try:
        open_register_page(page, settings)
        return register_user(page, user, settings)
    except Exception as error:
        log_register_failed(user.username, str(error))
        return False
