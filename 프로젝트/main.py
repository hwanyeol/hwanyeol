from tkinter import Tk
from 프로젝트.주소록 import AddressBook

if __name__ == '__main__':
    root = Tk()  # Tkinter의 Tk 클래스를 사용하여 루트 윈도우 생성
    application = AddressBook(root, "Demo Application - Objects in Python")  # AddressBook 클래스의 인스턴스 생성
    root.mainloop()  # Tkinter 이벤트 루프 시작
