# =========================================
# SCHOOL FEE STRUCTURE
# =========================================

FEE_STRUCTURE = {

    "Play Group": 5000,

    "PP1": 7000,

    "PP2": 7000,

    "Grade 1": 10000,

    "Grade 2": 10000,

    "Grade 3": 10000,

    "Grade 4": 10000,

    "Grade 5": 10000,

    "Grade 6": 10000,

    "Grade 7": 12000,

    "Grade 8": 12000,

    "Grade 9": 12000
}


def get_class_fee(class_name):

    return FEE_STRUCTURE.get(
        class_name,
        0
    )


def get_minimum_admission_fee(class_name):

    fee = get_class_fee(class_name)

    return fee * 0.5


def calculate_balance(total_bill, amount_paid):

    return max(
        total_bill - amount_paid,
        0
    )


def allocate_payment(
    amount,
    outstanding_balance
):

    if amount >= outstanding_balance:

        return {
            "allocated": outstanding_balance,
            "credit": amount - outstanding_balance
        }

    return {
        "allocated": amount,
        "credit": 0
    }
