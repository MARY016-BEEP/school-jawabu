# ==========================================
# CBC SUBJECTS BY LEVEL
# ==========================================


CBC_SUBJECTS = {

    "Play Group": [

        "Language Activities",

        "Mathematical Activities",

        "Environmental Activities",

        "Creative Activities",

        "Psychomotor Activities"
    ],


    "PP1": [

        "Language Activities",

        "Mathematical Activities",

        "Environmental Activities",

        "Creative Activities",

        "Psychomotor Activities"
    ],


    "PP2": [

        "Language Activities",

        "Mathematical Activities",

        "Environmental Activities",

        "Creative Activities",

        "Psychomotor Activities"
    ],


    "Grade 1": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Environmental Activities",

        "Creative Activities",

        "Religious Education"
    ],


    "Grade 2": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Environmental Activities",

        "Creative Activities",

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

        "Agriculture",

        "Social Studies",

        "Creative Arts",

        "Religious Education"
    ],


    "Grade 5": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Science and Technology",

        "Agriculture",

        "Social Studies",

        "Creative Arts",

        "Religious Education"
    ],


    "Grade 6": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Science and Technology",

        "Agriculture",

        "Social Studies",

        "Creative Arts",

        "Religious Education"
    ],


    "Grade 7": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Integrated Science",

        "Health Education",

        "Pre-Technical Studies",

        "Social Studies",

        "Religious Education",

        "Creative Arts",

        "Agriculture"
    ],


    "Grade 8": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Integrated Science",

        "Health Education",

        "Pre-Technical Studies",

        "Social Studies",

        "Religious Education",

        "Creative Arts",

        "Agriculture"
    ],


    "Grade 9": [

        "English",

        "Kiswahili",

        "Mathematics",

        "Integrated Science",

        "Health Education",

        "Pre-Technical Studies",

        "Social Studies",

        "Religious Education",

        "Creative Arts",

        "Agriculture"
    ]
def calculate_grade(mark):

    if mark >= 80:

        return "EE"

    elif mark >= 70:

        return "ME"

    elif mark >= 50:

        return "AE"

    elif mark >= 30:

        return "BE"

    else:

        return "BELOW EXPECTATION"
        def calculate_results(marks):

    total = sum(marks)

    if len(marks) == 0:

        mean = 0

    else:

        mean = total / len(marks)

    return total, round(mean, 2)
  
}PROMOTION_MAP = {

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


def promote_student(student):

    current_class = student.class_name

    if current_class in PROMOTION_MAP:

        student.class_name = PROMOTION_MAP[
            current_class
        ]

        return True

    return False
    def promote_class(students):

    for student in students:

        promote_student(student)

    return students