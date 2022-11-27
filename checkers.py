def people(text):
    if not "landlord" in text:
        return "landlord"
    if not "tenant" in text:
        return "tenant"
    return "Included"


def starting_date(text):
    synonyms = ["starting date", "move in date", "starts on:"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "starting_date"


def address(text):
    return "Included"


def end_date(text):
    synonyms = ["continues on a month-to-month basis",
                "continues on another periodic basis", "a fixed term ending on"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "ending_date"


def rent_price(text):
    synonyms = ["$", "pay the rent", "price"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "rent_price"


def pay_day(text):
    synonyms = ["first day", "day of the month"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "pay_day"


def notice_before_rent_increase(text):
    synonyms = ["rent increase"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "rent_increase"


def security_deposit(text):
    if "security deposit" in text:
        return "Included"
    return "sec_dep"


def smoking(text):
    synonyms = ["smoking", "cigarette", "vape",
                "marijuana", "weed", "hemp", "cannabis"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "smoking"


def pet(text):
    if "pet" in text or "pets" in text:
        return "Included"
    return "pets"


def utilities(text):
    synonyms = ["utilities", "water bills", "electricity bills"]
    for synonym in synonyms:
        if synonym in text:
            return "Included"
    return "utilities"


checkers = [people, end_date, starting_date, address, rent_price, pay_day,
            notice_before_rent_increase, security_deposit, smoking, pet, utilities]
