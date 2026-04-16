from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    base_url: str = "https://parabank.parasoft.com/parabank/index.htm"
    kill_on_start: bool = True
    browser: str = "chrome"
    timeout_ms: int = 15000
    max_retries: int = 3
    retry_delay_ms: int = 2000
    click_delay_ms: int = 150
    loan_amount: int = 10000
    down_payment_pct: float = 0.2
    desktop_report: bool = True


settings = AppSettings()
