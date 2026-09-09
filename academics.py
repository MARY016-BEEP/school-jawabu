CBC_SUBJECTS = {

    "Play Group": [
        "Language Activities",
        "Mathematical Activities",
        "Environmental Activities",
        "Creative Activities"
    ],

    "PP1": [
        "Language Activities",
        "Mathematical Activities",
        "Environmental Activities",
        "Creative Activities"
    ],

    "PP2": [
        "Language Activities",
        "Mathematical Activities",
        "Environmental Activities",
        "Creative Activities"
    ],

    "Grade 1": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Environmental Activities",
        "Creative Arts",
        "Religious Education"
    ],

    "Grade 2": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Environmental Activities",
        "Creative Arts",
        "Religious Education"
    ],

    "Grade 3": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Science and Technology",
        "Social Studies",
        "Creative Arts",
        "Religious Education"
    ],

    "Grade 4": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Science and Technology",
        "Social Studies",
        "Creative Arts",
        "Religious Education"
    ],

    "Grade 5": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Science and Technology",
        "Social Studies",
        "Creative Arts",
        "Religious Education"
    ],

    "Grade 6": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Science and Technology",
        "Social Studies",
        "Creative Arts",
        "Religious Education"
    ],

    "Grade 7": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Integrated Science",
        "Social Studies",
        "Pre-Technical Studies",
        "Creative Arts",
        "Agriculture"
    ],

    "Grade 8": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Integrated Science",
        "Social Studies",
        "Pre-Technical Studies",
        "Creative Arts",
        "Agriculture"
    ],

    "Grade 9": [
        "English",
        "Kiswahili",
        "Mathematics",
        "Integrated Science",
        "Social Studies",
        "Pre-Technical Studies",
        "Creative Arts",
        "Agriculture"
    ]
}


EXAMS = [
    "Opening Exam",
    "Mid Term Exam",
    "End Term Exam"
]


PROMOTION_MAP = {

    "Play Group": "PP1",
    "PP1": "PP2",
    "PP2": "Grade 1",
    "Grade 1": "Grade 2",
    "Grade 2": "Grade 3",
    "Grade 3": "Grade 4",
    "Grade 4": "Grade 5",
    "Grade 5": "Grade 6",
    "Grade 6": "Grade 7",
    "Grade 7": "Grade 8",
    "Grade 8": "Grade 9"
}


def calculate_grade(mark):

    if mark >= 80:
        return "EE - Exceeding Expectation"

    elif mark >= 60:
        return "ME - Meeting Expectation"

    elif mark >= 40:
        return "AE - Approaching Expectation"

    else:
        return "BE - Below Expectation"


def calculate_results(marks):

    if not marks:
        return 0, 0

    total = sum(marks)

    mean = total / len(marks)

    return total, round(mean, 2)
