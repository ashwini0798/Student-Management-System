from tkinter import *
from tkinter import Toplevel
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter.ttk import Treeview
import pandas
import pymysql
import time
import random

root = Tk()
root.title("Student Management System")
root.configure(bg='black')
root.geometry('1174x600+100+30')
root.iconbitmap('st_icon.ico')
root.resizable(False,False)


################functions############
colors = ['blue', 'pink', 'yellow']
def IntroLabelColors():
    fg = random.choice(colors)
    SliderLabel.config(fg=fg)
    SliderLabel.after(2,IntroLabelColors)

def IntroLabelTick():
    global text,count
    if(count>=len(ss)):
        count = 0
        text=''
        SliderLabel.config(text=text)
    else:
        text = text + ss[count]
        SliderLabel.config(text=text)
        count += 1
    SliderLabel.after(200,IntroLabelTick)

def tick():
    time_string = time.strftime("%H:%M:%S")
    date_string = time.strftime("%d/%m/%Y")
    clock.configure(text='Date : '+date_string+ "\n" + 'Time : '+time_string)
    clock.after(200,tick)

def Connectdb():
    def submitdb():
        global con, mycursor
        host = hostval.get()
        user = userval.get()
        password = passwordval.get()
        try:
            con = pymysql.connect(host=host,user=user, password=password)
            mycursor = con.cursor()
        except:
            messagebox.showerror('Notifications', 'Data is incorrect. Please try again', parent=dbroot)
            return
        try:
            strr = 'create database studentmanagementsystem'
            mycursor.execute(strr)
            strr1 = 'use studentmanagementsystem'
            mycursor.execute(strr1)
            strr2 = 'create table studentdata(id int, name varchar(20), mobile varchar(20), email varchar(30), address varchar(70), gender varchar(10), dob varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(strr2)
            strr4 = 'alter table studentdata modify column id int not null'
            mycursor.execute(strr4)
            strr5 = 'alter table studentdata modify column id int primary key'
            mycursor.execute(strr5)
            messagebox.showinfo('Notification', 'Database created and now you are connected to the database...', parent=dbroot)
        except:
            strr3= 'use studentmanagementsystem'
            mycursor.execute(strr3)
            messagebox.showinfo('Notification', 'Now you are connected to the database...', parent=dbroot)

        dbroot.destroy()


    dbroot= Toplevel()
    dbroot.grab_set()
    dbroot.geometry('470x250+800+230')
    dbroot.iconbitmap('st_icon.ico')
    dbroot.resizable(False, False)
    dbroot.config(bg='black')

##############################Labels#########################
    hostlabel = Label(dbroot, text='Enter Host : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                    borderwidth=3, width=13, anchor='w')
    hostlabel.place(x=10, y=10)

    userlabel = Label(dbroot, text='Enter User : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                    borderwidth=3, width=13, anchor='w')
    userlabel.place(x=10, y=70)

    passwordlabel = Label(dbroot, text='Enter Password : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                    borderwidth=3, width=13, anchor='w')
    passwordlabel.place(x=10, y=130)

#######################################Textbox###################################
    hostval = StringVar()
    hostEntry = Entry(dbroot, font=('roman', 15, 'bold'),bd=5,textvariable=hostval)
    hostEntry.place(x=250,y=10)

    userval = StringVar()
    userEntry = Entry(dbroot, font=('roman', 15, 'bold'), bd=5, textvariable=userval)
    userEntry.place(x=250, y=70)

    passwordval = StringVar()
    passwordEntry = Entry(dbroot, font=('roman', 15, 'bold'), bd=5, textvariable=passwordval)
    passwordEntry.place(x=250, y=130)

    #######################button#####################
    submitbutton = Button(dbroot, text='Submit', font=('roman',15,'bold'),width=20, bd=5,
                          activebackground='grey', activeforeground='white', command=submitdb)
    submitbutton.place(x=150, y=190)

    dbroot.mainloop()

def addstudent():
    def submitadd():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob = dobval.get()
        addeddate = time.strftime("%d/%m/%Y")
        addedtime = time.strftime("%H:%M:%S")
        try:
            strr7 = 'insert into studentdata values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(strr7, (id, name, mobile, email, address, gender, dob, addeddate, addedtime))
            con.commit()
            res = messagebox.askyesnocancel('Notification','Id {} Name {} Added Succssfully... and want to clean the form'.format(id,name), parent=addroot)
            if(res == True):
                idval.set('')
                nameval.set('')
                mobileval.set('')
                emailval.set('')
                addressval.set('')
                genderval.set('')
                dobval.set('')
        except:
            messagebox.showerror('Notification', ' Id already exists, try another id...',
                                 parent=addroot)
        strr8 = 'select * from studentdata'
        mycursor.execute(strr8)
        datas = mycursor.fetchall()
        studenttable.delete(*studenttable.get_children())
        for i in datas:
            vv=[i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7],i[8]]
            studenttable.insert('', END, values= vv)


    addroot = Toplevel(master=DataEntryFrame)
    addroot.grab_set()
    addroot.geometry('470x470+220+200')
    addroot.iconbitmap('st_icon.ico')
    addroot.config(bg='black')
    addroot.resizable(False,False)

    ##########################label#####################################
    idlabel = Label(addroot, text='Enter Id : ', bg='white',font=('times',20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    idlabel.place(x=10, y=10)
    namelabel = Label(addroot, text='Enter Name : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    namelabel.place(x=10, y=70)
    mobilelabel = Label(addroot, text='Enter Mobile : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    mobilelabel.place(x=10, y=130)
    emaillabel = Label(addroot, text='Enter Email : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    emaillabel.place(x=10, y=190)
    addresslabel = Label(addroot, text='Enter Address : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    addresslabel.place(x=10, y=250)
    genderlabel = Label(addroot, text='Enter Gender : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    genderlabel.place(x=10, y=310)
    doblabel = Label(addroot, text='Enter D.O.B : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    doblabel.place(x=10, y=370)

    ######################Textarea############################
    idval=  StringVar()
    identry = Entry(addroot,font=('roman',15,'bold'),bd=5, textvariable= idval)
    identry.place(x=250,y=10)
    nameval = StringVar()
    nameentry = Entry(addroot, font=('roman', 15, 'bold'), bd=5, textvariable=nameval)
    nameentry.place(x=250, y=70)
    mobileval = StringVar()
    mobileentry = Entry(addroot, font=('roman', 15, 'bold'), bd=5, textvariable=mobileval)
    mobileentry.place(x=250, y=130)
    emailval = StringVar()
    emailentry = Entry(addroot, font=('roman', 15, 'bold'), bd=5, textvariable=emailval)
    emailentry.place(x=250, y=190)
    addressval = StringVar()
    addressentry = Entry(addroot, font=('roman', 15, 'bold'), bd=5, textvariable=addressval)
    addressentry.place(x=250, y=250)
    genderval = StringVar()
    genderentry = Entry(addroot, font=('roman', 15, 'bold'), bd=5, textvariable=genderval)
    genderentry.place(x=250, y=310)
    dobval = StringVar()
    dobentry = Entry(addroot, font=('roman', 15, 'bold'), bd=5, textvariable=dobval)
    dobentry.place(x=250, y=370)


    #########################button#######################
    submitbtn = Button(addroot, text='Submit', font=('roman',15,'bold'), width=20, bd=5,bg='white',
                       activebackground='grey', activeforeground='white', command=submitadd)
    submitbtn.place(x=150,y=420)



    addroot.mainloop()
def searchstudent():
    def search():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob = dobval.get()
        if(id != ''):
            strr = 'select * from studentdata where id=%s'
            mycursor.execute(strr, (id))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)
        elif (name != ''):
            strr = 'select * from studentdata where name=%s'
            mycursor.execute(strr, (name))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)
        elif (mobile != ''):
            strr = 'select * from studentdata where mobile=%s'
            mycursor.execute(strr, (mobile))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)
        elif (email != ''):
            strr = 'select * from studentdata where email=%s'
            mycursor.execute(strr, (email))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)
        elif (address != ''):
            strr = 'select * from studentdata where address=%s'
            mycursor.execute(strr, (address))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)
        elif (gender != ''):
            strr = 'select * from studentdata where gender=%s'
            mycursor.execute(strr, (gender))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)
        elif (dob != ''):
            strr = 'select * from studentdata where dob=%s'
            mycursor.execute(strr, (dob))
            datas = mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for i in datas:
                vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
                studenttable.insert('', END, values=vv)



    searchroot = Toplevel(master=DataEntryFrame)
    searchroot.grab_set()
    searchroot.geometry('470x470+220+100')
    searchroot.iconbitmap('st_icon.ico')
    searchroot.config(bg='black')
    searchroot.resizable(False, False)

    ##########################label#####################################
    idlabel = Label(searchroot, text='Enter Id : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE, borderwidth=3,
                    width=12, anchor='w')
    idlabel.place(x=10, y=10)
    namelabel = Label(searchroot, text='Enter Name : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                      borderwidth=3,
                      width=12, anchor='w')
    namelabel.place(x=10, y=70)
    mobilelabel = Label(searchroot, text='Enter Mobile : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                        borderwidth=3,
                        width=12, anchor='w')
    mobilelabel.place(x=10, y=130)
    emaillabel = Label(searchroot, text='Enter Email : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                       borderwidth=3,
                       width=12, anchor='w')
    emaillabel.place(x=10, y=190)
    addresslabel = Label(searchroot, text='Enter Address : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                         borderwidth=3,
                         width=12, anchor='w')
    addresslabel.place(x=10, y=250)
    genderlabel = Label(searchroot, text='Enter Gender : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                        borderwidth=3,
                        width=12, anchor='w')
    genderlabel.place(x=10, y=310)
    doblabel = Label(searchroot, text='Enter D.O.B : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                     borderwidth=3,
                     width=12, anchor='w')
    doblabel.place(x=10, y=370)

    ######################Textarea############################
    idval = StringVar()
    identry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=idval)
    identry.place(x=250, y=10)
    nameval = StringVar()
    nameentry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=nameval)
    nameentry.place(x=250, y=70)
    mobileval = StringVar()
    mobileentry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=mobileval)
    mobileentry.place(x=250, y=130)
    emailval = StringVar()
    emailentry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=emailval)
    emailentry.place(x=250, y=190)
    addressval = StringVar()
    addressentry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=addressval)
    addressentry.place(x=250, y=250)
    genderval = StringVar()
    genderentry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=genderval)
    genderentry.place(x=250, y=310)
    dobval = StringVar()
    dobentry = Entry(searchroot, font=('roman', 15, 'bold'), bd=5, textvariable=dobval)
    dobentry.place(x=250, y=370)

    #########################button#######################
    searchbtn = Button(searchroot, text='Submit', font=('roman', 15, 'bold'), width=20, bd=5, bg='white',
                       activebackground='grey', activeforeground='white', command=search)
    searchbtn.place(x=150, y=420)

    searchroot.mainloop()
def deletestudent():
    cc = studenttable.focus()
    content = studenttable.item(cc)
    pp = content['values'][0]
    strr = 'delete from studentdata where id=%s'
    mycursor.execute(strr, (pp))
    con.commit()
    messagebox.showinfo("Notification", 'Id {} deleted successfully'.format(pp))
    strr = 'select * from studentdata'
    mycursor.execute(strr)
    datas = mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())
    for i in datas:
        vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        studenttable.insert('', END, values=vv)

def updatestudent():
    def update():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob = dobval.get()
        date = dateval.get()
        time = timeval.get()

        strr = 'update studentdata set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
        mycursor.execute(strr, (name,mobile,email,address,gender,dob,date,time,id))
        con.commit()
        messagebox.showinfo("Notification", 'Id {} modified successfully...'.format(id), parent=updateroot)
        strr = 'select * from studentdata'
        mycursor.execute(strr)
        datas = mycursor.fetchall()
        studenttable.delete(*studenttable.get_children())
        for i in datas:
            vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            studenttable.insert('', END, values=vv)


    updateroot = Toplevel(master=DataEntryFrame)
    updateroot.grab_set()
    updateroot.geometry('470x590+220+100')
    updateroot.iconbitmap('st_icon.ico')
    updateroot.config(bg='black')
    updateroot.resizable(False, False)

    ##########################label#####################################
    idlabel = Label(updateroot, text='Enter Id : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                    borderwidth=3,
                    width=12, anchor='w')
    idlabel.place(x=10, y=10)
    namelabel = Label(updateroot, text='Enter Name : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                      borderwidth=3,
                      width=12, anchor='w')
    namelabel.place(x=10, y=70)
    mobilelabel = Label(updateroot, text='Enter Mobile : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                        borderwidth=3,
                        width=12, anchor='w')
    mobilelabel.place(x=10, y=130)
    emaillabel = Label(updateroot, text='Enter Email : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                       borderwidth=3,
                       width=12, anchor='w')
    emaillabel.place(x=10, y=190)
    addresslabel = Label(updateroot, text='Enter Address : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                         borderwidth=3,
                         width=12, anchor='w')
    addresslabel.place(x=10, y=250)
    genderlabel = Label(updateroot, text='Enter Gender : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                        borderwidth=3,
                        width=12, anchor='w')
    genderlabel.place(x=10, y=310)
    doblabel = Label(updateroot, text='Enter D.O.B : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                     borderwidth=3,
                     width=12, anchor='w')
    doblabel.place(x=10, y=370)
    datelabel = Label(updateroot, text='Enter Date : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                      borderwidth=3,
                      width=12, anchor='w')
    datelabel.place(x=10, y=430)
    timelabel = Label(updateroot, text='Enter Time : ', bg='white', font=('times', 20, 'bold'), relief=GROOVE,
                      borderwidth=3,
                      width=12, anchor='w')
    timelabel.place(x=10, y=490)

    ######################Textarea############################
    idval = StringVar()
    identry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=idval)
    identry.place(x=250, y=10)
    nameval = StringVar()
    nameentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=nameval)
    nameentry.place(x=250, y=70)
    mobileval = StringVar()
    mobileentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=mobileval)
    mobileentry.place(x=250, y=130)
    emailval = StringVar()
    emailentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=emailval)
    emailentry.place(x=250, y=190)
    addressval = StringVar()
    addressentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=addressval)
    addressentry.place(x=250, y=250)
    genderval = StringVar()
    genderentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=genderval)
    genderentry.place(x=250, y=310)
    dobval = StringVar()
    dobentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=dobval)
    dobentry.place(x=250, y=370)
    dateval = StringVar()
    dateentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=dateval)
    dateentry.place(x=250, y=430)
    timeval = StringVar()
    timeentry = Entry(updateroot, font=('roman', 15, 'bold'), bd=5, textvariable=timeval)
    timeentry.place(x=250, y=490)

    #########################button#######################
    updatesbtn = Button(updateroot, text='Submit', font=('roman', 15, 'bold'), width=20, bd=5, bg='white',
                       activebackground='grey', activeforeground='white', command=update)
    updatesbtn.place(x=150, y=540)
    cc = studenttable.focus()
    content = studenttable.item(cc)
    pp = content['values']
    if(len(pp) != 0):
        idval.set(pp[0])
        nameval.set(pp[1])
        mobileval.set(pp[2])
        emailval.set(pp[3])
        addressval.set(pp[4])
        genderval.set(pp[5])
        dobval.set(pp[6])
        dateval.set(pp[7])
        timeval.set(pp[8])

    updateroot.mainloop()


def showstudent():
    strr = 'select * from studentdata'
    mycursor.execute(strr)
    datas = mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())
    for i in datas:
        vv = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
        studenttable.insert('', END, values=vv)


def exportstudent():
    ff = filedialog.asksaveasfilename()
    gg = studenttable.get_children()
    id, name, mobile, email, address, gender, dob, addeddate, addedtime = [],[],[],[],[],[],[],[],[]
    for i in gg:
        content = studenttable.item(i)
        pp = content['values']
        id.append(pp[0]),
        name.append(pp[1]),
        mobile.append(pp[2]),
        email.append(pp[3]),
        address.append(pp[4]),
        gender.append(pp[5]),
        dob.append(pp[6]),
        addeddate.append(pp[7]),
        addedtime.append(pp[8])
    dd = ['Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time']
    df = pandas.DataFrame(list(zip(id, name, mobile, email, address, gender, dob, addeddate, addedtime)), columns=dd)
    paths = r'{}.csv'.format(ff)
    df.to_csv(paths, index=False)
    messagebox.showinfo('Notifications', 'Student Data is saved {}'.format(paths))


def exitstudent():
    res = messagebox.askyesnocancel('Notification', 'Do you want to exit?')
    if (res==True):
        root.destroy()







########frames#############
DataEntryFrame = Frame(root, bg='white', relief=GROOVE, borderwidth =5)
DataEntryFrame.place(x=10,y=80, width=500, height=500)

########framebuttons##############
frontlabel = Label(DataEntryFrame, text='--------------Welcome-------------', width=30, font=('arial',22,'italic bold'),bg='white')
frontlabel.pack(side=TOP, expand=True)
addbtn = Button(DataEntryFrame, text='1. Add Student', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE, command=addstudent)
addbtn.pack(side=TOP, expand=True)
searchbtn = Button(DataEntryFrame, text='2. Search Student', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE,command=searchstudent)
searchbtn.pack(side=TOP, expand=True)
deletebtn = Button(DataEntryFrame, text='3. Delete Student', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE, command=deletestudent)
deletebtn.pack(side=TOP, expand=True)
updatebtn = Button(DataEntryFrame, text='4. Update Student', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE, command=updatestudent)
updatebtn.pack(side=TOP, expand=True)
showbtn = Button(DataEntryFrame, text='5. Show All', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE, command=showstudent)
showbtn.pack(side=TOP, expand=True)
exportbtn = Button(DataEntryFrame, text='6. Export Data', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE, command=exportstudent)
exportbtn.pack(side=TOP, expand=True)
exitbtn = Button(DataEntryFrame, text='7. Exit', width=25, font=('chiller',20,'bold'),bd=6,
                activebackground='grey', activeforeground='white', relief=RIDGE, command=exitstudent)
exitbtn.pack(side=TOP, expand=True)


ShowDataFrame = Frame(root, bg='white', relief=GROOVE, borderwidth=5)
ShowDataFrame.place(x=550, y=80, width=610, height=500)

style = ttk.Style()
style.configure('Treeview.Heading', font=('chiller',20, 'bold'), foreground='black')
style.configure('Treeview', font=('times',15, 'bold'), foreground='white', background='black')


scroll_x = Scrollbar(ShowDataFrame, orient=HORIZONTAL)
scroll_y = Scrollbar(ShowDataFrame, orient=VERTICAL)

studenttable = Treeview(ShowDataFrame,columns=('Id', 'Name', 'Mobile No.', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date',
                                               'Added Time'), yscrollcommand=scroll_y.set,
                        xscrollcommand=scroll_x.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=studenttable.xview)
scroll_y.config(command=studenttable.yview)
studenttable.heading('Id', text='Id')
studenttable.heading('Name', text='Name')
studenttable.heading('Mobile No.', text='Mobile No.')
studenttable.heading('Email', text='Email')
studenttable.heading('Address', text='Address')
studenttable.heading('Gender', text='Gender')
studenttable.heading('D.O.B', text='D.O.B')
studenttable.heading('Added Date', text='Added Date')
studenttable.heading('Added Time', text='Added Time')
studenttable['show'] = 'headings'
studenttable.column('Id', width=100)
studenttable.column('Name', width=200)
studenttable.column('Mobile No.', width=200)
studenttable.column('Email', width=300)
studenttable.column('Address', width=200)
studenttable.column('Gender', width=100)
studenttable.column('D.O.B', width=150)
studenttable.column('Added Date', width=150)
studenttable.column('Added Time', width=150)
studenttable.pack(fill=BOTH, expand =1)

###########Slider############
count = 0
text = ''
ss= 'Welcome To Student Management System'
SliderLabel = Label(root,text=ss,font=("chiller",30,'italic bold'), relief=RIDGE, borderwidth =5, bg= 'white', width=35)
SliderLabel.place(x=260, y=0)
IntroLabelTick()
IntroLabelColors()


###########Clock##############
clock = Label(root,font=("times",15,'bold'), relief=RIDGE, borderwidth =4, bg='white')
clock.place(x=0,y=0)
tick()

##############Button#################
connectbutton = Button(root, text='Connect to Database',width=23, font=("chiller",19,'italic bold'), relief=RIDGE,
                       borderwidth =4, bg='white', activebackground='grey', activeforeground='white',
                       command=Connectdb)
connectbutton.place(x=930, y=0)
root.mainloop()