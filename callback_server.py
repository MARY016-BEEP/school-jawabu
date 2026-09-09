from flask import Flask, request, jsonify

from database import SessionLocal
from models import Payment

app = Flask(__name__)


@app.route(
    "/mpesa/callback",
    methods=["POST"]
)
def mpesa_callback():

    data = request.get_json()

    print("M-PESA CALLBACK:", data)

    try:

        callback = (
            data["Body"]["stkCallback"]
        )

        checkout_id = callback[
            "CheckoutRequestID"
        ]

        result_code = callback[
            "ResultCode"
        ]

        db = SessionLocal()

        payment = db.query(Payment).filter(
            Payment.checkout_request_id
            == checkout_id
        ).first()


        if result_code == 0:

            metadata = callback[
                "CallbackMetadata"
            ]["Item"]

            receipt = None
            amount = None

            for item in metadata:

                if item["Name"] == "MpesaReceiptNumber":

                    receipt = item.get(
                        "Value"
                    )

                if item["Name"] == "Amount":

                    amount = item.get(
                        "Value"
                    )


            if payment:

                payment.status = "SUCCESS"

                payment.mpesa_receipt = receipt

                payment.amount = amount

                db.commit()


        else:

            if payment:

                payment.status = "FAILED"

                db.commit()


        db.close()

        return jsonify({

            "ResultCode": 0,

            "ResultDesc": "Accepted"

        })


    except Exception as e:

        print(e)

        return jsonify({

            "ResultCode": 1,

            "ResultDesc": str(e)

        })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )