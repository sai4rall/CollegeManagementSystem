class Student:
    def __init__(self, student_name,student_Id):
        self.student_id = student_Id
        self.student_name=student_name
        self.attendance_present=0
        self.attendance_total=0
        self._books_issued_=[]
        self.fee_paid = 0
        self.marks_details = {}

    def issue_book(self,book_id):
        self.books_issued.append(book_id)

    def return_book(self,book_id):
        self._books_issued_.remove(book_id)




