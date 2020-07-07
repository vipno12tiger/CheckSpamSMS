# import re
#
# print(re.match('[a-z]', 'safasd065'))

class student:
    def __init__(self, name, score, gender):
        self.name = name
        self.score = score
        self.gender = gender

    def toString(self):
        return "[Name= " + self.name + ", Score= " + str(self.score) + ", Gender= " + self.gender +"]"

def key(student):
    return student.score

def main():
    student_list = []
    student1 = student("Dang", 7.4, "Male")
    student_list.append(student1)
    student2 = student("Hieu", 8.8, "Male")
    student_list.append(student2)
    student3 = student("Nhung", 8.4, "FeMale")
    student_list.append(student3)
    for std in student_list:
        print(std.toString())

    print("***********")

    test = sorted(student_list, key=key)
    for std in test:
        print(std.toString())

main()