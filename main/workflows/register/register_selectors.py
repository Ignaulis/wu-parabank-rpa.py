

# Nuoroda i registracijos puslapi
REGISTER_LINK = "a[href*='register.htm']"

# Registracijos formos ivesties laukai
FIRST_NAME_INPUT = "input#customer\\.firstName"
LAST_NAME_INPUT = "input#customer\\.lastName"
ADDRESS_INPUT = "input#customer\\.address\\.street"
CITY_INPUT = "input#customer\\.address\\.city"
STATE_INPUT = "input#customer\\.address\\.state"
ZIP_CODE_INPUT = "input#customer\\.address\\.zipCode"
PHONE_INPUT = "input#customer\\.phoneNumber"
SSN_INPUT = "input#customer\\.ssn"
USERNAME_INPUT = "input#customer\\.username"
PASSWORD_INPUT = "input#customer\\.password"
REPEATED_PASSWORD_INPUT = "input#repeatedPassword"

# Registracijos patvirtinimas
REGISTER_BUTTON = "input[value='Register']"


SUCCESS_TITLE = "h1.title"
SUCCESS_MESSAGE = "div#rightPanel p"
SUCCESS_ACCOUNT_CREATED_TEXT = "div#rightPanel p:has-text('Your account was created successfully')"

# Klaidu zinutes prie konkreciu lauku
FIRST_NAME_ERROR = "#customer\\.firstName\\.errors"
LAST_NAME_ERROR = "#customer\\.lastName\\.errors"
ADDRESS_ERROR = "#customer\\.address\\.street\\.errors"
CITY_ERROR = "#customer\\.address\\.city\\.errors"
STATE_ERROR = "#customer\\.address\\.state\\.errors"
ZIP_CODE_ERROR = "#customer\\.address\\.zipCode\\.errors"
SSN_ERROR = "#customer\\.ssn\\.errors"
USERNAME_ERROR = "#customer\\.username\\.errors"
PASSWORD_ERROR = "#customer\\.password\\.errors"
REPEATED_PASSWORD_ERROR = "#repeatedPassword\\.errors"


USERNAME_TAKEN_ERROR = "#customer\\.username\\.errors"

GLOBAL_ERROR_BLOCK = "div.error"
