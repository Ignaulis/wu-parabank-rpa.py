from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class UserProfile:
    # Registracijai
    first_name: str = ""
    last_name: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    phone_number: str = ""
    ssn: str = ""
    username: str = ""
    password: str = ""
    account_type: str = ""
    initial_deposit: Optional[float] = None

    dob: str = ""
    debit_card: str = ""
    cvv: str = ""


def _clean(value: object) -> str:

    if value is None:
        return ""
    return str(value).strip()


def _to_optional_float(value: object) -> Optional[float]:
    s = _clean(value)
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_users(csv_path: str | None = None) -> list[UserProfile]:

    if csv_path is None:
        csv_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "input"
            / "ParaBank users.csv"
        ).as_posix()

    path = Path(csv_path)

    users: list[UserProfile] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            user = UserProfile(
                first_name=_clean(row.get("First Name")),
                last_name=_clean(row.get("Last Name")),
                address=_clean(row.get("Address")),
                city=_clean(row.get("City")),
                state=_clean(row.get("State")),
                zip_code=_clean(row.get("Zip Code")),
                phone_number=_clean(row.get("Phone Number")),
                ssn=_clean(row.get("SSN")),
                username=_clean(row.get("Username")),
                password=_clean(row.get("Password")),
                account_type=_clean(row.get("Account Type")),
                initial_deposit=_to_optional_float(row.get("Initial Deposit")),
                dob=_clean(row.get("DOB")),
                debit_card=_clean(row.get("Debit Card")),
                cvv=_clean(row.get("CVV")),
            )
            users.append(user)

    return users
