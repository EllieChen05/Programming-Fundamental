```markdown
# Programming Assignment 3 - Course Results Analysis System

**Student Name:** Su Myat Noe Yee  
**Student ID:** s3913797  
**Level Achieved:** HD  
**Program:** Master of Analytics / RMIT University  

---

## Assignment Overview

This assignment implements a system for managing and analyzing course results and student information.  
It includes features for reading files, calculating GPA, analyzing pass rates, and generating reports for students and courses.

**Key Features:**
- Reading `results.txt`, `courses.txt`, and `students.txt` files
- Calculating GPA in both 100-point and 4-point scales
- Analyzing course performance (average score, difficult courses)
- Identifying best students
- Generating detailed course and student reports in `reports.txt`
- Handling both undergraduate (UG) and postgraduate (PG) students

---

## Technologies Used

- Python 3
- Object-Oriented Programming (Classes: `Main`, `Course`, `Student`, `Results`)
- File I/O
- String formatting and static methods

---

## How to Run

```bash
python3 program.py results.txt courses.txt students.txt

---

## File Structure
Assignment 3/
│
├── program.py # Main program
├── results.txt # Student results file
├── courses.txt # Courses information file
├── students.txt # Students information file
├── reports.txt # Generated report
└── README.md # Project description (this file)

---

## Reflection

The program implements a system for managing and analyzing course results and student information.  

**Highlights:**
- The `Main` class handles file checking and program execution.  
- The `Course` class manages course data and calculates averages, finished/ongoing students.  
- The `Student` class stores student information for GPA calculations.  
- The `Results` class reads data files, calculates GPA, analyzes pass rates, identifies difficult courses, and generates reports.  

**Learnings and Challenges:**
- Implementing object-oriented programming concepts
- Handling file I/O and data validation
- Formatting reports with clean tables and calculations
- Converting scores to GPA in multiple scales
- Validating student enrollments and course completions

---

