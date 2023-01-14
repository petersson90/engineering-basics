# pylint: disable=missing-docstring
# pylint: disable=fixme
# pylint: disable=unused-argument

RATES = {
    'USDEUR': 0.85,
    'GBPEUR': 1.13,
    'CHFEUR': 0.86
}

# `amount` is a `tuple` like (100, EUR). `currency` is a `string`
def convert(amount, currency):
    from_amount, from_currency = amount
    # print(amount, from_amount, from_currency)

    conversion_rate = RATES.get(from_currency + currency)
    # print(conversion_rate)

    if conversion_rate is None:
        return None

    return round(from_amount * conversion_rate, 2)
