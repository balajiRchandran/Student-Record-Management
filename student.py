from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from sqlite3 import *
import re
import datetime
from fpdf import *
import sys
c=connect("student.db")
cur=c.cursor()
#to check if table already exist
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='STUDENT' ''')
if cur.fetchone()[0]==0 : {
	cur.execute('''CREATE TABLE STUDENT(
                name text not null,
                roll varchar(6) primary key,
                dob date not null,
                doa date not null,
                city text,
                phonenum varchar(10),
                dept text)''')
}                   
   

def on(checkbox,value):
    if value:
        print("yes")
    else:
        print("no")
def checkdate(date):
        chk=re.match('[0-9]{2}/[0-9]{2}/[1-2][0-9][0-9][0-9]',date)
        if chk:
                return True
        else:
                return False

def roll_exist(roll):
        cur.execute("SELECT * FROM STUDENT")
        data = cur.fetchall()
        flag=0
        for i in data:
              if roll in i:
                    flag=1
                    break
        return True if flag==1 else False
                
def checkphone(num):
        chk=re.match('[0-9]{10}',num)
        if chk and len(num)==10:
                return True
        else:
                return False
class abc(ScrollView):
    def __init__(self,**kwargs):
        super(abc,self).__init__(**kwargs)
        Window.fullscreen=True
        self.size_hint=(1,None)
        self.size=(Window.width,Window.height)
        self.stud=['','','','','','','']
        self.a=''
        self.b=''
        self.c=''
        self.login()
    def login(self,dummy=0):
        self.clear_widgets()
        root1=StackLayout(spacing=10,size_hint_y=None)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=40,size_hint_x=1,size_hint_y=None,markup=True))
        root1.add_widget(Label(text="[size=30][color=#2361c4]LOGIN",height=40,size_hint_x=1,size_hint_y=None,markup=True))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None,markup=True))
        root1.add_widget(Label(text="ADMIN/STUDENT",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.who=TextInput(text=self.a,size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.who)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="USERNAME",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.user=TextInput(text=self.b,size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.user)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="PASSWORD",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.passwd=TextInput(text=self.c,size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.passwd)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        root1.add_widget(Button(text="LOGIN",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.check_log))
        root1.add_widget(Button(text="CLEAR",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.l_c))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        self.add_widget(root1)

    #for admin, the username is admin and the password is *****
    #for students the user name is roll num and the password is their DOB
    def check_log(self,dummy=0):
        who=self.who.text.upper()
        user=self.user.text.upper()
        passwd=self.passwd.text.upper()
        self.a=who
        self.b=user
        self.c=passwd
        if who=="ADMIN":
            if user=="ADMIN" and passwd=="*****":
                self.first()
            elif user=="ADMIN":
                self.c="Wrong Password!!"
                self.login()
            elif passwd=="*****":
                self.b="Wrong Username!!"
                self.login()
            else:
                self.c="Wrong Password!!"
                self.b="Wrong Username!!"
                self.login()
        elif who=="STUDENT":
            if roll_exist(user):
                cur.execute("SELECT to_char(dob,'dd/mm/yyyy') FROM STUDENT WHERE roll = '"+user+"'")
                d=cur.fetchall()
                d=d[0][0]
                if d==passwd:
                    self.first1()
                else:
                    self.c="Wrong Password!!"
                    self.login()
            else:
                self.b="Roll num not yet registered!!"
                self.login()
        else:
            self.a="Invalid input!!"
            self.login()

    #student menu with only view options
    def first1(self,dummy=0):
        roll=self.user.text.upper()
        cur.execute("SELECT * FROM STUDENT WHERE ROLL = '"+roll+"'")
        rows = cur.fetchall()
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=30,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='EXIT',height=50,on_press=self.e))
        root1.add_widget(Label(text="[size=25]RECORD",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='LOG OUT',height=50,on_press=self.log))
        root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
        li=["[b][color=#A06114]NAME","[b][color=#A06114]ROLL NUM","[b][color=#A06114]DOB","[b][color=#A06114]DOA","[b][color=#A06114]CITY","[b][color=#A06114]MOBILE NUM","[b][color=#A06114]DEPT"]
        for i in range(7):
            root1.add_widget(Label(text="",height=50,size_hint_x=0.15,size_hint_y=None))
            root1.add_widget(Label(text=str(li[i]),height=50,size_hint_x=0.35,size_hint_y=None,markup=True))
            root1.add_widget(Label(text=str(rows[0][i]),height=50,size_hint_x=0.35,size_hint_y=None,markup=True))
            root1.add_widget(Label(text="",height=50,size_hint_x=0.15,size_hint_y=None))
        self.add_widget(root1)
    def l_c(self,dummy=0):
        self.a=''
        self.b=''
        self.c=''
        self.login()

    #admin menu screen with view and edit options
    def first(self,dummy=0):
        self.clear_widgets()
        self.a=''
        self.stud=['','','','','','','']
        root=StackLayout(spacing=10,size_hint_y=None)
        root.bind(minimum_height=root.setter('height'))
        root.add_widget(Label(text="",height=30,size_hint_x=1,size_hint_y=None))
        root.add_widget(Label(text="[size=30][color=#B8860B]STUDENT'S RECORDS[/size][/font]",size_hint_y=None,height=80,markup=True))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Button(text="ADD RECORDS",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.add))
        root.add_widget(Button(text="UPDATE RECORDS",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.update))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Button(text="DELETE RECORDS",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.delete))
        root.add_widget(Button(text="DISPLAY RECORDS",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.table))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Button(text="SEARCH RECORD",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.search))
        root.add_widget(Button(text="GENERATE PDF",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.generate))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Button(text="SAVE",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.commit))
        root.add_widget(Button(text="EXIT",height=50,size_hint_x=0.4,size_hint_y=None,on_press=self.e))
        root.add_widget(Label(text="",height=50,size_hint_x=0.1,size_hint_y=None))
        root.add_widget(Label(text="",height=50,size_hint_x=0.35,size_hint_y=None))
        root.add_widget(Button(text="LOG OUT",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.log))
        root.add_widget(Label(text="",height=50,size_hint_x=0.35,size_hint_y=None))
        self.add_widget(root)
    def log(self,dummy=0):
        self.a=''
        self.b=''
        self.c=''
        self.login()
    def e(self,dummy):
        Window.close()
        sys.exit()
    def generate(self,dummy=0):
        cur.execute("SELECT * FROM STUDENT")
        rows = cur.fetchall()
        header=["Name ","Roll no.","Date of Birth","Admission date","City ","Phone No ","Department"]
        pdf=FPDF(orientation='L')
        pdf.set_font('times','bi',16)
        col_width=pdf.w/7.5
        row_height=pdf.font_size*2
        pdf.add_page()
        pdf.cell(pdf.w,pdf.font_size,"STUDENTS RECORDS",align="C")
        pdf.ln(row_height)
        pdf.set_font('times','b',14)
        for col in header:
                pdf.cell(col_width,row_height,str(col),border=1)
        pdf.ln(row_height)
        pdf.set_font('times','',12)
        for row in rows:
                for col in row:
                        pdf.cell(col_width,row_height,str(col),border=1)
                pdf.ln(row_height)
        t=str(datetime.datetime.now())
        t=t[0:16]
        t=t.replace(' ','')
        t=t.replace('-','')
        t=t.replace(':','')
        pdf.output(t+'.pdf')
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="GENERATED SUCCESSFULLY!!!",height=30,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        self.add_widget(root1)
    def search(self,dummy=0):
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="[size=30][b][color=#FF0000][u]SEARCH RECORDS[/b]",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="ROLL NUM",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.roll1=TextInput(text=self.a,size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.roll1)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        root1.add_widget(Button(text="SEARCH",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.search_s))
        root1.add_widget(Button(text="CLEAR",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.s_c))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        self.add_widget(root1)
    def search_s(self,dummy=0):
        roll=self.roll1.text.upper()
        if roll_exist(roll):
            self.a=''
            cur.execute("SELECT * FROM STUDENT WHERE ROLL = '"+roll+"'")
            rows = cur.fetchall()
            self.clear_widgets()
            root1=StackLayout(size_hint_y=None,spacing=0)
            root1.bind(minimum_height=root1.setter('height'))
            root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
            root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
            root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.search))
            root1.add_widget(Label(text="[size=20]RECORD",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
            root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
            root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
            li=["[b][color=#A06114]NAME","[b][color=#A06114]ROLL NUM","[b][color=#A06114]DOB","[b][color=#A06114]DOA","[b][color=#A06114]CITY","[b][color=#A06114]MOBILE NUM","[b][color=#A06114]DEPT"]
            for i in range(7):
                root1.add_widget(Label(text="",height=50,size_hint_x=0.15,size_hint_y=None))
                root1.add_widget(Label(text=str(li[i]),height=50,size_hint_x=0.35,size_hint_y=None,markup=True))
                root1.add_widget(Label(text=str(rows[0][i]),height=50,size_hint_x=0.35,size_hint_y=None,markup=True))
                root1.add_widget(Label(text="",height=50,size_hint_x=0.15,size_hint_y=None))
            self.add_widget(root1)
        else:
            self.a="Invalid Roll Number"
            self.search()
    def s_c(self,dummy=0):
        self.a=''
        self.search()
    def delete(self,dummy=0):
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="[size=30][b][color=#FF0000][u]DELETE RECORDS[/b]",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="ROLL NUM",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.roll1=TextInput(text=self.a,size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.roll1)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        root1.add_widget(Button(text="DELETE",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.delete_s))
        root1.add_widget(Button(text="CLEAR",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.d_c))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        self.add_widget(root1)
    def delete_s(self,dummy=0):
        roll=self.roll1.text.upper()
        if roll_exist(roll):
            self.a=''
            cur.execute("DELETE FROM STUDENT WHERE roll='"+roll+"'")
            self.clear_widgets()
            root1=StackLayout(size_hint_y=None,spacing=0)
            root1.bind(minimum_height=root1.setter('height'))
            root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
            root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
            root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.delete))
            root1.add_widget(Label(text="",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
            root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
            root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
            root1.add_widget(Label(text="DELETED SUCCESSFULLY!!!",height=30,size_hint_x=1,size_hint_y=None))
            root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
            self.add_widget(root1)
        else:
            self.a="Invalid Roll Number"
            self.delete()
    def d_c(self,dummy=0):
        self.a=''
        self.delete()
    def table(self,dummy=0):
        self.clear_widgets()
        cur.execute("SELECT * FROM STUDENT")
        rows = cur.fetchall()
        rows.insert(0,["[b][color=#A06114]S NO","[b][color=#A06114]NAME","[b][color=#A06114]ROLL NUM","[b][color=#A06114]DOB","[b][color=#A06114]DOA","[b][color=#A06114]CITY","[b][color=#A06114]MOBILE NUM","[b][color=#A06114]DEPT"])
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=30,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="[size=30]RECORDS",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
        i=0
        for row in rows:
            if i!=0:
                root1.add_widget(Label(text=str(i)+")",height=30,size_hint_x=1/8,size_hint_y=None,markup=True))
            for col in row:
                    root1.add_widget(Label(text=str(col),height=30,size_hint_x=1/8,size_hint_y=None,markup=True))
            i=i+1
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.35,size_hint_y=None))
        root1.add_widget(Button(text="SORT DATA",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.sort))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.35,size_hint_y=None))
        self.add_widget(root1)
    def sort(self,dummy=0):
        self.clear_widgets()
        cur.execute("SELECT * FROM STUDENT ORDER BY ROLL")
        rows = cur.fetchall()
        rows.insert(0,["[b][color=#A06114]S NO","[b][color=#A06114]NAME","[b][color=#A06114]ROLL NUM","[b][color=#A06114]DOB","[b][color=#A06114]DOA","[b][color=#A06114]CITY","[b][color=#A06114]MOBILE NUM","[b][color=#A06114]DEPT"])
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=30,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="[size=30]RECORDS",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
        i=0
        for row in rows:
            if i!=0:
                root1.add_widget(Label(text=str(i)+")",height=30,size_hint_x=1/8,size_hint_y=None,markup=True))
            for col in row:
                    root1.add_widget(Label(text=str(col),height=30,size_hint_x=1/8,size_hint_y=None,markup=True))
            i=i+1
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.35,size_hint_y=None))
        root1.add_widget(Button(text="SORT DATA",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.sort))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.35,size_hint_y=None))
        self.add_widget(root1)
    def commit(self,dummy=0):
        c.commit()
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="DATA SAVED SUCCESSFULLY!!!",height=30,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        self.add_widget(root1)
    def add(self,dummy=0):
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="[size=30][b][color=#FF0000][u]NEW RECORDS[/b]",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="NAME",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.name=TextInput(text=self.stud[0],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.name)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="ROLL NUM",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.roll=TextInput(text=self.stud[1],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.roll)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="DOB(dd/mm/yyyy)",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.dob=TextInput(text=self.stud[2],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.dob)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="ADMISSION DATE(dd/mm/yyyy)",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.ad=TextInput(text=self.stud[3],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.ad)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="CITY",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.city=TextInput(text=self.stud[4],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.city)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="MOBILE NUMBER",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.mob=TextInput(text=self.stud[5],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.mob)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="DEPARTMENT",height=50,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.dept=TextInput(text=self.stud[6],size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.dept)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        root1.add_widget(Button(text="ADD",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.check))
        root1.add_widget(Button(text="CLEAR",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.clear))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        self.add_widget(root1)
    def check(self,dummy=0):
        f=0
        self.stud[0]=self.name.text.upper()
        self.stud[1]=self.roll.text.upper()
        self.stud[2]=self.dob.text.upper()
        self.stud[3]=self.ad.text.upper()
        self.stud[4]=self.city.text.upper()
        self.stud[5]=self.mob.text
        self.stud[6]=self.dept.text.upper()
        for i in range(7):
            if len(self.stud[i])==0:
                self.stud[i]="Invalid Entry"
                f=1
        if len(self.stud[1])!=6 or roll_exist(self.stud[1]):
                if roll_exist(self.stud[1]):
                        self.stud[1]='Roll Num already exists'
                else:
                        self.stud[1]='Invalid Roll Num!'
                f=1
        if not checkdate(self.stud[2]):
                self.stud[2]='Invalid date format!'
                f=1
        if not checkdate(self.stud[3]):
                self.stud[2]='Invalid date format!'
                f=1
        if not checkphone(self.stud[5]):
                self.stud[5]='Invalid Mobile Number'
                f=1
        if f==1:
            self.add()
        else:
            entry="INSERT INTO STUDENT VALUES('"+self.stud[0]+"','"+self.stud[1]+"','"+self.stud[2]+"','"+self.stud[3]+"','"+self.stud[4]+"','"+self.stud[5]+"','"+self.stud[6]+"')"
            cur.execute(entry)
            self.stud=['','','','','','','']
            self.insert_s()
    def insert_s(self):
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.add))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=70,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="DATA INSERTED SUCCESSFULLY!!!",height=30,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        self.add_widget(root1)
    def clear(self,dummy=0):
        self.stud=['','','','','','','']
        self.add()
    def update(self,dummy=0):
        self.clear_widgets()
        root1=StackLayout(size_hint_y=None,spacing=0)
        root1.bind(minimum_height=root1.setter('height'))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.first))
        root1.add_widget(Label(text="[size=30][b][color=#FF0000][u]UPDATE RECORDS[/b]",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
        root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
        root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
        root1.add_widget(Label(text="ROLL NUM",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.roll1=TextInput(text=self.a,size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.roll1)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="COLUMN NAME",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="[NAME,ROLL NUM,DOB,ADMISSION DATE",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="CITY,MOB NUM,DEPT]",height=25,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.col=TextInput(size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.col)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="NEW VALUE",height=40,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        self.val=TextInput(size_hint_y=None,size_hint_x=0.8,multiline=False,height=40)
        root1.add_widget(self.val)
        root1.add_widget(Label(text="",height=40,size_hint_x=0.1,size_hint_y=None))
        root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        root1.add_widget(Button(text="UPDATE",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.update_s))
        root1.add_widget(Button(text="CLEAR",height=50,size_hint_x=0.3,size_hint_y=None,on_press=self.u_c))
        root1.add_widget(Label(text="",height=50,size_hint_x=0.2,size_hint_y=None))
        self.add_widget(root1)
    def u_c(self,dummy=0):
        self.a=''
        self.update()
    def update_s(self,dummy=0):
        f=0
        roll=self.roll1.text.upper()
        if roll_exist(roll):
            self.a=''
            if (len(self.val.text)!=6 or roll_exist(self.val.text.upper()) )and self.col.text.upper()=="ROLL NUM":
                f=1
            if not checkdate(self.val.text.upper()) and self.col.text.upper()=="ADMISSION DATE":
                f=1
            if not checkdate(self.val.text.upper()) and self.col.text.upper()=="DOB":
                f=1
            if not checkphone(self.val.text) and self.col.text.upper()=="MOB NUM":
                f=1
            if self.col.text.upper() not in "NAME ROLL NUM DOB ADMISSION DATE CITY MOB NUM DEPT":
                f=1
            if f==1:
                self.update()
            else:
                li=['name','roll','dob','doa','city','phonenum','dept']
                if self.col.text.upper()=="NAME":
                    entry=0
                elif self.col.text.upper()=="ROLL NUM":
                    entry=1
                elif self.col.text.upper()=="DOB":
                    entry=2
                elif self.col.text.upper()=="ADMISSION DATE":
                    entry=3
                elif self.col.text.upper()=="CITY":
                    entry=4
                elif self.col.text.upper()=="MOB NUM":
                    entry=5
                else:
                    entry=6
                cur.execute('UPDATE STUDENT SET '+li[entry]+" = '"+self.val.text.upper()+"' WHERE roll ='"+roll+"'")
                print("abc")
                self.clear_widgets()
                root1=StackLayout(size_hint_y=None,spacing=0)
                root1.bind(minimum_height=root1.setter('height'))
                root1.add_widget(Label(text="",height=20,size_hint_x=1,size_hint_y=None))
                root1.add_widget(Label(text="",height=50,size_hint_x=0.05,size_hint_y=None))
                root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='BACK',height=50,on_press=self.update))
                root1.add_widget(Label(text="",height=50,size_hint_x=0.6,size_hint_y=None,markup=True))
                root1.add_widget(Button(size_hint_y=None,size_hint_x=0.15,text='HOME',height=50,on_press=self.first))
                root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
                root1.add_widget(Label(text="DATA UPDATED SUCCESSFULLY!!!",height=30,size_hint_x=1,size_hint_y=None))
                root1.add_widget(Label(text="",height=30,size_hint_x=0.05,size_hint_y=None))
                self.add_widget(root1)
        else:
            self.a="Invalid Roll Num"
            self.update()
class StudentApp(App):
    def build(self):
        return abc()
if __name__=='__main__':
    StudentApp().run()
        
