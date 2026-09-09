def allocate_payment(

    amount,

    tuition_balance,

    transport_balance,

    library_balance

):

    allocation = {

        "tuition": 0,

        "transport": 0,

        "library": 0,

        "credit": 0

    }


    # FIRST PRIORITY: TUITION

    tuition_paid = min(
        amount,
        tuition_balance
    )

    allocation["tuition"] = tuition_paid

    amount -= tuition_paid


    # SECOND PRIORITY: TRANSPORT

    if amount > 0:

        transport_paid = min(
            amount,
            transport_balance
        )

        allocation["transport"] = transport_paid

        amount -= transport_paid


    # THIRD PRIORITY: LIBRARY

    if amount > 0:

        library_paid = min(
            amount,
            library_balance
        )

        allocation["library"] = library_paid

        amount -= library_paid


    # EXTRA MONEY BECOMES CREDIT

    if amount > 0:

        allocation["credit"] = amount


    return allocation