from reportlab.lib.pagesizes import A4

from reportlab.pdfgen import canvas


def generate_report_card(

    student,

    results,

    filename

):

    pdf = canvas.Canvas(

        filename,

        pagesize=A4
    )


    width, height = A4


    # SCHOOL NAME

    pdf.setFont(

        "Helvetica-Bold",

        20
    )

    pdf.drawCentredString(

        width / 2,

        height - 60,

        "JAWABU LEARNING CENTRE"
    )


    pdf.setFont(

        "Helvetica-Bold",

        14
    )

    pdf.drawCentredString(

        width / 2,

        height - 90,

        "STUDENT REPORT CARD"
    )


    # STUDENT DETAILS

    pdf.setFont(

        "Helvetica",

        11
    )

    pdf.drawString(

        50,

        height - 130,

        f"Student Name: {student.student_name}"
    )


    pdf.drawString(

        50,

        height - 150,

        f"Registration Number: {student.registration_number}"
    )


    pdf.drawString(

        50,

        height - 170,

        f"Class: {student.class_name}"
    )


    y = height - 220


    # TABLE HEADERS

    pdf.setFont(

        "Helvetica-Bold",

        11
    )

    pdf.drawString(50, y, "Subject")

    pdf.drawString(250, y, "Marks")

    pdf.drawString(350, y, "Grade")


    y -= 25


    # RESULTS

    pdf.setFont(

        "Helvetica",

        10
    )


    total = 0


    for result in results:

        pdf.drawString(

            50,

            y,

            result["subject"]
        )

        pdf.drawString(

            250,

            y,

            str(result["marks"])
        )

        pdf.drawString(

            350,

            y,

            result["grade"]
        )


        total += result["marks"]

        y -= 22


    # TOTAL

    pdf.setFont(

        "Helvetica-Bold",

        11
    )

    pdf.drawString(

        50,

        y - 20,

        f"TOTAL MARKS: {total}"
    )


    if results:

        mean = total / len(results)

    else:

        mean = 0


    pdf.drawString(

        250,

        y - 20,

        f"MEAN SCORE: {mean:.2f}"
    )


    pdf.save()