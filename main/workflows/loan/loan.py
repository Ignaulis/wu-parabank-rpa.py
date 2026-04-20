from core.extract_data import UserProfile

from .loan_page import LoanServerError, request_loan_user


# Paleidzia paskolos uzklausos veiksma
def run_loan_for_user(page, user: UserProfile, settings) -> bool:
    return request_loan_user(page, user, settings)
