import mysql.connector

from CollageManagementSystem import CollageManagementSystem
from Student import Student


class StudentMgmt(CollageManagementSystem):
    student_details_list = []
    max_student_id = 0

    def get_conn(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="studentmgmtsys"
        )

    def list_students(self):
        print("student Id \t|\t student name \t|")
        print("_________________________________")
        mydb = self.get_conn()
        mycursor = mydb.cursor()
        mycursor.execute("select * from student_details")
        s_details = mycursor.fetchall()
        for student in s_details:
            print(student)
        mydb.close()

    def add_student(self):
        self.max_student_id += 1
        s = Student(input("please enter student Name"), self.max_student_id)
        mydb = self.get_conn()
        mycursor = mydb.cursor()
        sql = "INSERT INTO student_details ( student_name,attendance_present,attendance_total,fee_paid) VALUES ( %s," \
              "%s,%s,%s) "
        val = (s.student_name, 0, 0, 0)
        mycursor.execute(sql, val)
        mydb.commit()
        print(s.student_id)

    def add_attendance(self, student_id, is_present):
        mydb = self.get_conn()
        mycursor = mydb.cursor()
        mycursor.execute("select * from student_details where student_id=%s", [student_id])
        s_details = mycursor.fetchone()
        if len(s_details) > 0:
            attenadance_present = s_details[2]
            if (is_present):
                attenadance_present = attenadance_present + 1

            attenadance_total_days = int(s_details[3])
            attenadance_total_days = attenadance_total_days + 1
            mycursor.execute("update student_details set attendance_present=%s,attendance_total=%s where student_id=%s",
                             [attenadance_present, attenadance_total_days, student_id])
            mydb.commit()
        else:
            print("student not found in the database")

    def show_attendance(self, student_id=None):
        if (student_id == None):
            mydb = self.get_conn()
            mycursor = mydb.cursor()
            mycursor.execute(
                "select student_id,student_name,attendance_present,attendance_total,(attendance_present/attendance_total)*100   from student_details")
            self.s_details = mycursor.fetchall()
            print("student id", "student_name", "student present", "student total", "percentage", sep="\t")
            for student in self.s_details:
                print(student[0], student[1], student[2], student[3], student[4], sep="\t")
        else:
            mydb = self.get_conn()
            mycursor = mydb.cursor()
            mycursor.execute(
                "select student_id,student_name,attendance_present,attendance_total,"
                "(attendance_present/attendance_total)*100   from student_details where student_id=%s", [student_id])
            self.s_details = mycursor.fetchone()
            if self.s_details != None:
                print("student id", "student_name", "student present", "student total", "percentage", sep="\t")
                print(self.s_details[0], self.s_details[1], self.s_details[2], self.s_details[3], self.s_details[4],
                      sep="\t")
            else:
                print("student not found")

    def issue_book(self):
        book_id = input("please enter book id")
        studentid = int(input("please enter student_id"))
        mydb = self.get_conn()
        mycursor = mydb.cursor()
        mycursor.execute("select * from student_details where student_id=%s", [studentid])
        self.s_details = mycursor.fetchone()
        if self.s_details != None:
            mycursor.execute("insert into issued_books (bookid,student_id,is_returned) value(%s,%s,'N')",
                             [book_id, studentid]);
            mydb.commit()
        else:
            print("student not found!")

    def show_issued_books(self):
        studentid = int(input("please enter student_id"))
        index = None
        for i in range(len(self.student_details_list)):
            if self.student_details_list[i].student_id == studentid:
                index = i
        if index == None:
            print("student Not found!")
        else:
            print(self.student_details_list[index]._books_issued_)

    def return_book(self):
        studentid = int(input("please enter student_id"))
        bookId = input("please enter bookId")
        mydb = self.get_conn()
        mycursor = mydb.cursor()
        mycursor.execute("select * from issued_books where bookid=%s and student_id=%s and is_returned='N'",
                         [bookId, studentid])
        self.bookdetails = mycursor.fetchone()
        if self.bookdetails != None:
            issue_id = self.bookdetails[0]
            mycursor.execute("update issued_books set is_returned='Y' where issue_id=%s", [issue_id])
            mydb.commit()


def get_boolean_val(str):
    if str == "True":
        return True
    if str == "False":
        return False


if __name__ == "__main__":
    c = StudentMgmt()

    while (True):
        try:

            print("please choose the option", " 1. add student", " 2.list students", " 3. add attendance",
                  " 4. show all attendance", " 5. show student attendance,", " 6. issue books", " 7. show issued books",
                  " 8.retrun book", " 0. exit ", sep="\n")
            choice = int(input())
            if choice == 1:
                c.add_student()
            elif choice == 2:
                c.list_students()
            elif choice == 3:
                id = int(input("please enter student Id"))
                isPresent = get_boolean_val(input("please type True if present"))
                c.add_attendance(id, isPresent)
            elif choice == 4:
                c.show_attendance()
            elif choice == 5:
                studentId = int(input("please enter student id"))
                c.show_attendance(studentId)
            elif choice == 6:
                c.issue_book()
            elif choice == 7:
                c.show_issued_books()
            elif choice == 8:
                c.return_book()
            elif choice == 0:
                break

            else:
                print("wrong data!")

        except ValueError as e:
            print("invalid response", e)
        except TypeError as t:
            print("invalid response", t)
