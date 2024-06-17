import pickle
import os.path
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from chapter2.프로젝트.주소 import Address

class AddressBook:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)  # 창의 타이틀 설정
        self.parent.protocol("WM_DELETE_WINDOW", self.on_exit)  # 창 닫기 이벤트 처리

        self.initialization()  # GUI 초기화
        self.bind()  # 이벤트 바인딩
        self.set_listbox()  # 리스트박스 설정
        self.lbx_names.focus_set()  # 리스트박스에 포커스 설정

    def bind(self):
        self.lbx_names.bind('<ButtonRelease-1>', self.on_click_lb)  # 리스트박스 항목 클릭 이벤트
        self.lbx_names.bind('<KeyRelease>', self.on_click_lb)  # 리스트박스 키 릴리즈 이벤트

    def which_selected(self):
        return int(self.lbx_names.curselection()[0])  # 선택된 항목의 인덱스 반환

    def on_click_lb(self, event=None):
        self.set_data()  # 리스트박스 클릭 시 데이터 설정

    def set_data(self):
        self.name_var.set(self.lst_addresses[self.which_selected()].name)  # 선택된 주소의 이름 설정
        self.email_var.set(self.lst_addresses[self.which_selected()].email)  # 선택된 주소의 이메일 설정
        self.phone_var.set(self.lst_addresses[self.which_selected()].phone)  # 선택된 주소의 전화번호 설정

    def set_listbox(self):
        self.lbx_names.delete(0, END)  # 리스트박스 초기화
        for dat in range(len(self.lst_addresses)):
            self.lbx_names.insert(END, self.lst_addresses[dat].name)  # 주소 목록에서 이름으로 리스트박스 채우기
        self.lbx_names.selection_set(0)  # 첫 번째 항목 선택

    def initialization(self):
        main_frame = Frame(self.parent)
        main_frame.pack(fill=BOTH, expand=YES)  # 메인 프레임 설정

        self.name_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()

        self.status_bar = Label(main_frame, text="Felon -2016-", relief=SUNKEN, bd=1).pack(side=BOTTOM, fill=X)  # 상태 바 설정

        frame1 = Frame(main_frame, bd=10)
        frame1.pack(fill=BOTH, expand=YES, side=LEFT)

        scroll = ttk.Scrollbar(frame1, orient=VERTICAL)
        self.lbx_names = Listbox(frame1, width=30, yscrollcommand=scroll.set)  # 리스트박스 및 스크롤바 설정
        self.lbx_names.pack(fill=Y, side=LEFT)
        scroll.config(command=self.lbx_names.yview)
        scroll.pack(side=LEFT, fill=Y)

        frame2 = Frame(main_frame, bd=10)
        frame2.pack(fill=BOTH, expand=YES, side=RIGHT)

        frame3 = Frame(frame2)
        frame3.pack(side=TOP, expand=YES)

        Label(frame3, text='Full Name').grid(row=0, column=0, sticky=W)
        self.ent_name = Entry(frame3, textvariable=self.name_var, width=30)  # 이름 입력 필드
        self.ent_name.grid(row=0, column=1)

        Label(frame3, text='Email').grid(row=1, column=0, sticky=W)
        self.ent_email = Entry(frame3, textvariable=self.email_var, width=30)  # 이메일 입력 필드
        self.ent_email.grid(row=1, column=1)

        Label(frame3, text='Phone').grid(row=2, column=0, sticky=W)
        self.ent_phone = Entry(frame3, textvariable=self.phone_var, width=30)  # 전화번호 입력 필드
        self.ent_phone.grid(row=2, column=1)

        frame4 = Frame(frame2)
        frame4.pack(side=BOTTOM, expand=YES)

        self.btn_new = ttk.Button(frame4, text='New', command=self.on_new, width=5)
        self.btn_new.pack(side=LEFT)  # 새 항목 버튼

        self.btn_add = ttk.Button(frame4, text='Add', command=self.on_add, width=5)
        self.btn_add.pack(side=LEFT)  # 추가 버튼

        self.btn_mod = ttk.Button(frame4, text='Mod', command=self.on_mod, width=5)
        self.btn_mod.pack(side=LEFT)  # 수정 버튼

        self.btn_del = ttk.Button(frame4, text='Del', command=self.on_del, width=5)
        self.btn_del.pack(side=LEFT)  # 삭제 버튼

        self.lst_addresses = self.load_address()  # 주소 목록 로드

    def on_new(self, event=None):
        self.ent_name.delete(0, END)  # 이름 입력 필드 초기화
        self.ent_email.delete(0, END)  # 이메일 입력 필드 초기화
        self.ent_phone.delete(0, END)  # 전화번호 입력 필드 초기화

    def on_add(self, event=None):
        address = Address(self.name_var.get(), self.email_var.get(), self.phone_var.get())  # 새 주소 생성
        self.lst_addresses.append(address)  # 주소 목록에 추가
        self.set_listbox()  # 리스트박스 업데이트
        self.save_address()  # 주소 저장

    def on_mod(self, event=None):
        self.lst_addresses[self.which_selected()].name = self.name_var.get()  # 선택된 주소의 이름 수정
        self.lst_addresses[self.which_selected()].email = self.email_var.get()  # 선택된 주소의 이메일 수정
        self.lst_addresses[self.which_selected()].phone = self.phone_var.get()  # 선택된 주소의 전화번호 수정
        self.set_listbox()  # 리스트박스 업데이트
        self.modify_address()  # 주소 변경 사항 저장

    def on_del(self, event=None):
        del self.lst_addresses[self.which_selected()]  # 선택된 주소 삭제
        self.set_listbox()  # 리스트박스 업데이트
        self.on_new()  # 입력 필드 초기화
        self.delete_address()  # 주소 파일에서 삭제

    def save_address(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lst_addresses, outfile)  # 주소 목록을 파일에 저장
        tkinter.messagebox.showinfo("Address Saved", "A new address have been saved")  # 저장 완료 메시지
        outfile.close()

    def modify_address(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lst_addresses, outfile)  # 변경된 주소 목록을 파일에 저장
        tkinter.messagebox.showinfo("Address Changed", "The changes have been saved")  # 변경 완료 메시지
        outfile.close()

    def delete_address(self):
        outfile = open("address.dat", "wb")
        pickle.dump(self.lst_addresses, outfile)  # 변경된 주소 목록을 파일에 저장
        tkinter.messagebox.showinfo("Address Deleted", "The address has been deleted")  # 삭제 완료 메시지
        outfile.close()

    def load_address(self):
        if not os.path.isfile("address.dat"):
            return []  # 파일이 없으면 빈 리스트 반환
        try:
            infile = open("address.dat", "rb")
            lst_addresses = pickle.load(infile)  # 파일에서 주소 목록 로드
        except EOFError:
            lst_addresses = []  # 파일이 비어있으면 빈 리스트 반환
        infile.close()
        return lst_addresses  # 주소 목록 반환

    def on_exit(self, event=None):
        self.parent.destroy()  # 프로그램 종료
