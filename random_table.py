import os
import random as r

import pandas as pd
from get_codes import get_codes

students = get_codes()
students_len = len(students)


assigned = {}

for student in students:
    assigned[student] = []

def assign_different(given):
    other_student = r.randint(0, students_len - 1)
    other_student = other_student if other_student != given else assign_different(given)
    return other_student

def assign_other_different(given, given2):
    other_student = r.randint(0, students_len - 1)
    other_student = other_student if (other_student != given and other_student != given2) else assign_other_different(given, given2)
    return other_student

def assign_other_different3(given, given2, given3):
    other_student = r.randint(0, students_len - 1)
    if not (other_student != given and other_student != given2 and other_student != given3):
        other_student = assign_other_different3(given, given2, given3)
    return other_student

def assign(given, current, second):
    if (len(assigned[given]) < 2):
        assigned[given] = assigned[given] + [students[current]]
    else:
        if assigned[given] != []:
            assign(students[assign_other_different3(current, second, students.index(assigned[given][0]))], current, second)
        else:
            assign(students[assign_other_different(current, second)], current, second)


def randomize_student_codes():
    for student in range(students_len):
        other_student = assign_different(student)
        other_student2 = assign_other_different(student, other_student)
        assign(students[other_student], student, other_student2)
        assign(students[other_student2], student, other_student)

    return assigned

if __name__ == '__main__':
    assigned = randomize_student_codes()

    with open('results.csv', 'w') as f:
        f.write('Student grading,Student to grade 1,Student to grade 2\n')
        for student in students:
            f.write(str(student) + ',' + str(assigned[student][0]) + ','+ str(assigned[student][1]) + '\n')
            print(student, end='\t')
            print(assigned[student])

    # Check 

    for student in students:
        print(student != assigned[student][0] and student != assigned[student][1] and assigned[student][0] != assigned[student][1])



    read_file = pd.read_csv (os.getcwd() + os.sep + 'results.csv')
    read_file.to_excel (os.getcwd() + os.sep + 'results.xlsx', index = None, header=False)