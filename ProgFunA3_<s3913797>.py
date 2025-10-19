#Student Name - Su Myat Noe Yee
#Student ID   - s3913797
#The Highest part you have attempted - HD Level
#Any problems or requirements the program didn't meet - Validating Results.txt file from HD Level
'''
Reflection:
The provided code implements a system for managing and analyzing course results and student information. 
It consists of classes such as Main, Course, Student, and Results. Here's a brief overview of the system's functionality:
The Main class serves as the program's entry point, checking file existence and running the program.
The Course class represents a course, allowing for score tracking and calculations such as average score and number of students.
The Student class stores student information for further analysis.
The Results class is the core component, handling file reading, displaying results, and generating reports. It also includes GPA calculations and identifies difficult courses and outstanding students.
Overall, the system provides a comprehensive analysis of course results and student information, offering insights into course performance, pass rates, and individual student progress.
Different scenarios have been tested for the quality of code. 
'''

import sys
import os

class Main:
    def __init__(self, result_file, course_file, student_file):
        "Initialize the Main class with file paths"
        self.result_file = result_file
        self.course_file = course_file
        self.student_file = student_file

    def check_files(self):
        "Check if provided files exist. Print an error message and exit if any file is missing."
        files = [self.result_file, self.course_file, self.student_file]
        for file in files:
            if not os.path.isfile(file):
                print("File '{}' not found.".format(file))
                sys.exit(1)
        print("All files found.")

    def run_program(self):
        "Run the program by reading data from files"
        results = Results()
        results.read_courses(self.course_file)
        results.read_students(self.student_file)
        results.read_results(self.result_file)
        results.display_results()
        results.save_file("reports.txt")

class Course:
    """
    Attributes:
    - course_id (int): The unique identifier of the course.
    - course_type (str): The type of the course.
    - course_name (str): The name of the course.
    - credit_points (int): The credit points assigned to the course.
    - offered_semesters (list): The list of semesters in which the course is offered.
    - scores (list): The list of scores achieved by students in the course.

    Methods:
    - add_score(score): Adds a student's score to the scores list.
    - get_num_students_finished(): Returns the number of students who have finished the course.
    - get_num_students_ongoing(): Returns the number of students who are currently enrolled in the course.
    - get_average_score(): Returns the average score achieved by students who have finished the course.
    """

    def __init__(self, course_id, course_type, course_name, credit_points, offered_semesters):
        "Initialize Course object with the provided attributes"
        self.course_id = course_id
        self.course_type = course_type
        self.course_name = course_name
        self.credit_points = credit_points
        self.offered_semesters = offered_semesters
        self.scores = []

    def add_score(self, score):
        "Add student's score to the scores list."
        self.scores.append(score)

    def get_num_students_finished(self):
        "Returns the number of students who have finished the course."
        #If score is avaiable for the course, it's counted as finished. 
        return len([score for score in self.scores if score is not None])

    def get_num_students_ongoing(self):
        "Returns the number of students who are enrolled in  course but haven't received the score."
        #If score is unavaiable for the course, it's counted as ongoing.
        return len([score for score in self.scores if score is None])

    def get_average_score(self):
        "Returns the average score achieved by students who have finished the course."
        num_finished_students = self.get_num_students_finished()
        if num_finished_students > 0:
            #Calculate average GPA for each courses. Calculation is the sum of scores is divided by number of finished students.  
            return sum(score for score in self.scores if score is not None) / num_finished_students
        return 0

class Student:
    def __init__(self, student_id, student_name, student_type, mode=None):
        """
        Initialize a new Student object.
            student_id (int): The unique identifier of the student.
            student_name (str): The name of the student.
            student_type (str): The type of the student.
            mode (str): The mode of study for the student. Defaults to None.
        """
        self.student_id = student_id
        self.student_name = student_name
        self.student_type = student_type
        self.mode = mode

class Results:
    def __init__(self):
        "Initialize an instance of the Results class."
        self.courses = []
        self.students = []
        self.scores = {}

    def read_courses(self, file_name):
        "Read the courses from a given file and populate the courses list."
        with open(file_name, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                course_id = values[0].strip()
                course_type = values[1].strip()
                course_name = values[2].strip()
                credit_points = int(values[3].strip())
                #If length of each row is greater than is 4, meaning, offered_semester is included in that row, strip white spaces and take that value.
                if len(values) > 4:
                    offered_semesters = values[4].strip()
                #If the length of each row is not greater than 4, meaning, offered_semester is included in that row, assign "All" for offered semester.
                else:
                    offered_semesters = "All"
                course = Course(course_id, course_type, course_name, credit_points, offered_semesters)
                self.courses.append(course)

    def read_students(self, file_name):
        "Read the students from a given file and populate the students list."
        with open(file_name, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                student_id = values[0].strip()
                student_name = values[1].strip()
                student_type = values[2].strip()
                #If student_type is PG, mode is included in that row. Then, strip white spaces and take that value. 
                if student_type == "PG":
                    mode = values[3].strip()
                #If not PG, meaning UG, assign "FT" for mode as only full time is avaiable for undergraduate.
                else:
                    mode = "FT"
                student = Student(student_id, student_name, student_type, mode)
                self.students.append(student)

    def read_results(self, file_name):
        "Read the results from a given file and populate the scores dictionary."
        with open(file_name, 'r') as file:
            for line in file:
                student_id, course_id, score = line.strip().split(',')
                student_id = student_id.strip()
                course_id = course_id.strip()
                score = score.strip()
                if score:
                    #If score is not included in that row, assign "None" for mode.
                    if score == "None":
                        score = None
                    #If score is avaible, assign that value. Need to use float() as score are in decimal format.
                    else:
                        score = float(score)
                else:
                    score = None
                self.scores[(student_id, course_id)] = score

    @staticmethod
    def score_to_gpa(score):
        """Convert a score to a GPA value.
        * Scores >= 79.5: GPA = 4.0
        * Scores >= 69.5 and < 79.5: GPA = 3.0
        * Scores >= 59.5 and < 69.5: GPA = 2.0
        * Scores >= 49.5 and < 59.5: GPA = 1.0
        * Scores < 49.5: GPA = 0.0
        """
        if score >= 79.5:
            return 4.0
        elif score >= 69.5 and score < 79.5:
            return 3.0
        elif score >= 59.5 and score < 69.5:
            return 2.0
        elif score >= 49.5 and score < 59.5:
            return 1.0
        else:
            return 0.0

    def display_results(self):
        print("RESULTS")
        print("--" * 30)

        # Display table header
        header = 'StudentID'.ljust(10)
        for course in self.courses:
            header += course.course_id.rjust(10)
        print(header)
        print("--" * 30)

        # Display table rows
        for student in self.students:
            row = student.student_id.ljust(10)
            for course in self.courses:
                #If score is available and has score value, print score. If score is available but score value is "None", print "--". It means it's still ongoing. 
                if (student.student_id, course.course_id) in self.scores:
                    score = self.scores[(student.student_id, course.course_id)]
                    row += '{:10}'.format(score) if score is not None else '--'.rjust(10)
                    course.add_score(score)
                #If not aviable, print nothing. It means student doesn't enroll for that course.
                else:
                    row += ' '.rjust(10)
            print(row)

        # Display total students and courses
        total_students = len(self.students)
        total_courses = len(self.courses)
        print("")
        print("RESULTS SUMMARY")
        print("There are {} students and {} courses.".format(total_students, total_courses))

        #Calculate and display pass rate
        total_count = 0.0
        pass_count = 0.0
        for score in self.scores.values():
            if score is not None:
                #If score is not none, increase 1 in total_count. 
                total_count += 1
                #If score is greater than 49.5, increase 1 in pass_count.
                if score >= 49.5:
                    pass_count += 1
        #Average pass rate will be calculated as pass_count divided by total_count, multiply with 100
        total_count = (pass_count / total_count) * 100 if total_count != 0 else 0
        print("The average pass rate is {:.2f}%.".format(total_count))

    #Generate Course Information Table 
    def generate_course_report(self):
        course_report = []

        #Finding Core and Elective Courses
        core_courses = []
        elective_courses = []
        for course in self.courses:
            if course.course_type == "C":
                core_courses.append(course)
            else:
                elective_courses.append(course)

        #Generating Core Course Table
        core_course_table = "\nCOURSE INFORMATION\n"
        core_course_table += "-" * 80 + "\n"
        core_course_table += "CourseID  Name                Type  Credit  Semester  Average  Nfinish  Nongoing\n"
        core_course_table += "-" * 80 + "\n"
        for course in core_courses:
            #Formatting each course information in a table row
            course_line = "{:<10} {:<20} {:<5} {:<8} {:<7} {:.2f} {:>8} {:>8}".format(
                course.course_id, course.course_name, course.course_type, str(course.credit_points),
                course.offered_semesters, course.get_average_score(), course.get_num_students_finished(),
                course.get_num_students_ongoing()
            )
            core_course_table += course_line + "\n"
        course_report.append(core_course_table)

        #Generating Elective Course Table
        elective_course_table = "-" * 80 + "\n"
        elective_course_table += "CourseID  Name                Type  Credit  Semester  Average  Nfinish  Nongoing\n"
        elective_course_table += "-" * 80 + "\n"
        for course in elective_courses:
            #Formatting each course information in a table row
            course_line = "{:<10} {:<20} {:<5} {:<8} {:<7} {:.2f} {:>8} {:>8}".format(
                course.course_id, course.course_name, course.course_type, str(course.credit_points),
                course.offered_semesters, course.get_average_score(), course.get_num_students_finished(),
                course.get_num_students_ongoing()
            )
            elective_course_table += course_line + "\n"
        course_report.append(elective_course_table)

        #Finding Most Difficult Core Course
        most_difficult_core_courses = []
        #Extract minimum average score among core courses
        min_average_score = min(course.get_average_score() for course in core_courses)
        for course in core_courses:
            if course.get_average_score() == min_average_score:
                #Extract mininum average score core course name
                most_difficult_core_courses.append(course.course_name)  
        most_difficult_core_courses_str = ', '.join(most_difficult_core_courses)
        course_report.append("COURSE SUMMARY\n")
        course_report.append("The most difficult core course is {} with an average score of {:.2f}.".format(most_difficult_core_courses_str, min_average_score))

        #Finding Most Difficult Elective Course
        most_difficult_elective_courses = []
        #Extract inimum average score among elective courses
        min_average_score = min(course.get_average_score() for course in elective_courses)
        for course in elective_courses:
            if course.get_average_score() == min_average_score:
                #Extract mininum average score elective course name
                most_difficult_elective_courses.append(course.course_name) 
        most_difficult_elective_courses_str = ', '.join(most_difficult_elective_courses)
        course_report.append("The most difficult elective course is {} with an average score of {:.2f}.".format(most_difficult_elective_courses_str, min_average_score))

        # Printing Student Information Table
        pg_student_table = [] 
        ug_student_table = []

        # Adding headers for PG student table
        pg_student_table += ["\nSTUDENT INFORMATION","-" * 80]
        pg_student_table += ["StudentID  Name                Type  Mode    GPA(100)  GPA(4)  Nfinish  Nongoing","-" * 80]

        # Adding headers for UG student table
        ug_student_table +=["-" * 80]
        ug_student_table += ["StudentID  Name                Type  Mode    GPA(100)  GPA(4)  Nfinish  Nongoing","-" * 80]

        best_pg_student = None
        best_ug_student = None
        best_pg_gpa_4 = 0
        best_ug_gpa_4 = 0

        # Iterate through each student
        for student in self.students:
            student_id = student.student_id
            student_name = student.student_name
            student_type = student.student_type
            mode = student.mode 
            total_score_100 = 0
            total_score_4 = 0
            num_scores = 0
            num_finished = 0
            num_ongoing = 0

            # Calculate GPA for each student
            for course in self.courses:
                if (student.student_id, course.course_id) in self.scores:
                    score = self.scores[(student.student_id, course.course_id)]

                    if score is not None:
                        total_score_100 += score #For GPA100
                        total_score_4 += self.score_to_gpa(score) #For GPA4
                        num_scores += 1
                        num_finished += 1
                    else:
                        num_ongoing += 1

            if num_scores > 0:
                gpa_100 = total_score_100 / num_scores
                gpa_4 = total_score_4 / num_scores
            else:
                gpa_100 = 0
                gpa_4 = 0

            # Modify student name based on enrollment requirements
            #For Undergrad full time student, total number of courses enrolled should be at least 4.
            if student_type == "UG" and mode == "FT":
                if num_finished + num_ongoing >= 4:
                    student_name += " "
                else:
                    student_name += " (!)"
            #For PostGrad full time studnet, total number of courses enrolled should be at least 4. 
            elif student_type == "PG" and mode == "FT":
                if num_finished + num_ongoing >= 4:
                    student_name += " "
                else:
                    student_name += " (!)"
            #For PostGrad part time studnet, total number of courses enrolled should be at least 2. 
            elif student_type == "PG" and mode == "PT":
                if num_finished + num_ongoing >= 2:
                    student_name += " "
                else:
                    student_name += " (!)"

            # Format student information as a table row
            student_info_line = "{:<10} {:<20} {:<5} {:<7} {:<10.2f} {:<8.2f} {:<8} {:<8}".format(student_id, student_name, student_type, mode, gpa_100, gpa_4, num_finished, num_ongoing)

            # Add student information to the respective tables
            #Finding the highest GPA among PG
            if student_type == "PG":
                pg_student_table += [student_info_line]
                if gpa_4 > best_pg_gpa_4:
                    best_pg_student = student
                    best_pg_gpa_4 = gpa_4
            #Finding the highest GPA among PG
            elif student_type == "UG":
                ug_student_table += [student_info_line]
                if gpa_4 > best_ug_gpa_4:
                    best_ug_student = student
                    best_ug_gpa_4 = gpa_4

        # Add the best PG student summary to the UG student table
        if best_pg_student:
            best_student_line = "The best PG student is {} with a GPA score of {:.2f}.".format(
                best_pg_student.student_id, best_pg_gpa_4)
            ug_student_table += ["\nSTUDENT SUMMARY"]
            ug_student_table += [best_student_line]

        # Add the best UG student summary to the UG student table
        if best_ug_student:
            best_student_line = "The best UG student is {} with a GPA score of {:.2f}.".format(
                best_ug_student.student_id, best_ug_gpa_4)
            ug_student_table += [best_student_line]

        # Combine the student tables with the course report
        course_report += pg_student_table
        course_report += ug_student_table

        # Display the course report in the terminal
        for line in course_report:
            print(line)

        return course_report

    def save_file(self, report_file_name):
        course_report = self.generate_course_report()
        with open(report_file_name, 'w') as file:
            for section in course_report:
                file.write(section + "\n")
        print("Course report has been saved to {}.".format(report_file_name))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Incorrect number of arguments. Usage: python program.py result_file course_file student_file")
    else:
        result_file = sys.argv[1]
        course_file = sys.argv[2]
        student_file = sys.argv[3]

        program = Main(result_file, course_file, student_file)
        program.check_files()
        program.run_program()


'''
References: 
W3 Schools., Python String join() Method., https://www.w3schools.com/python/ref_string_join.asp
Programiz., Python staticmethod()., https://www.programiz.com/python-programming/methods/built-in/staticmethod
W3 Schools., Python String format() Method., https://www.w3schools.com/python/ref_string_format.asp
GeeksforGeeks., Python | os.path.isfile() method., https://www.geeksforgeeks.org/python-os-path-isfile-method/
tutorialspoint., What does the if __name__ == "__main__": do in Python?., https://www.tutorialspoint.com/What-does-the-if-name-main-do-in-Python#:~:text=A%20Python%20programme%20uses%20the,is%20imported%20as%20a%20module.
'''