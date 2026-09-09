def payment_confirmation_message(

    parent_name,

    student_name,

    amount,

    receipt,

    balance

):

    return f"""
JAWABU LEARNING CENTRE

Dear {parent_name},

We have received KES {amount:,.2f}
for {student_name}.

M-Pesa Receipt:
{receipt}

Remaining Fee Balance:
KES {balance:,.2f}

Thank you.
"""


def fee_balance_message(

    parent_name,

    student_name,

    balance

):

    return f"""
JAWABU LEARNING CENTRE

Dear {parent_name},

This is a reminder that
{student_name} has an outstanding
school fee balance of:

KES {balance:,.2f}

Thank you.
"""


def announcement_message(message):

    return f"""
JAWABU LEARNING CENTRE

SCHOOL ANNOUNCEMENT

{message}
"""