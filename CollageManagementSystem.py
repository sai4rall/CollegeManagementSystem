from abc import ABC, abstractmethod


class CollageManagementSystem(ABC):
    @abstractmethod
    def add_student(self):
        None

    @abstractmethod
    def show_attendance(self):
        None

    @abstractmethod
    def add_attendance(self, student_id, is_resent):
        None

    @abstractmethod
    def list_students(self):
        None

    @abstractmethod
    def issue_book(self):
        None

    @abstractmethod
    def show_issued_books(self):
        None


    @abstractmethod
    def return_book(self):
        None

