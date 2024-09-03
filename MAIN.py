import sqlite3 as sql
import tkinter as tk
import tkinter.font as tkfont
import random 
import smtplib
from tkinter import messagebox, PhotoImage,BooleanVar
from datetime import datetime
import json
import math
def help():
    root = tk.Tk()
    root.title("Help")
    root.geometry("500x500")
    default_font = tkfont.Font(family="Verdana", size=12)
    root.option_add("*Font", default_font)
    text_widget = tk.Text(root, wrap='word')
    text_widget.pack()
    text = """loginpage
    if you have been given an account, you should enter your username and password into the areas provided. If you do not have any account details to allow you to login in, you will need to ask a user with admin access to create an account for you.
    
    menu page 
    this is the page with 2 or 3 different options, depending on your current position. 
    First is the complete evaluation button, this will load another screen, which is referenced under complete evaluation.
    The second button is the view historical data button, this when pressed will load a page that will ask for the id of the child given when they were added to the system, after this is given their historical test data will be loaded to the screen.
    The final button is only available to admins and it is the add account button, this allows a new user to be added after their username, email and password are provided, note the password must be more than 8 characters. in order to create an account the user must give a code that will be sent to the email that they gave, if this email doesnt arrive quickly, please allow for a few minutes to make sure nothing arrives before starting again. Also be sure to check your spam/junk email folder so this can sometimes happen.
    complete evaluation
    when this button is clicked by the user it will load 2 buttons, the append to record button, will load a page that asks the user to enter the person for whom they are completing the evaluation id. 
    the other button is the create new record button, this will ask the user to enter a few details about the person who they are entering and them provides them with the new id number of the person.
    testing
    after the user has identifed the person they are testing, they can begin the evaluation. this will require being present with the person they are testing, each question is scored 0,1 or 2 and after the question is asked the child should be asked for their opinion and if you disagree, you should ask them to justify their position until a census can be reached.
    After all the questions have been asked the system will give 3 outputs. the first is the line graph will shows how the test score has changed over time, where smaller is better. the next is a nightingale chart which breaks the evaluation down into 5 different pieces and allows you to gain a better understanding of which of the 5 areas (behaviour, emotionial wellbeing, relationship, risk and indicators) are currently of the biggest concern
    the final output is the housing opinion output, this finds the best housing option for the person who took the test and gives a confidence score to give piece of mind of how sure the system is of its output.
    """
    text_widget.insert(tk.END, text)
    root.mainloop()

def basescreen():
    global root
    root = tk.Tk()
    root.geometry("500x500")
    default_font = tkfont.Font(family="Verdana", size=12)
    root.option_add("*Font", default_font)

    b0 = tk.Button(root, text="Help", command=help) 
    b0.place(x=425,y=50)
def logingui():
    basescreen()
    root.title("Login")
    img = PhotoImage(file="placeholder.png")
    img = img.subsample(2,2)
    label_image = tk.Label(root, image=img)
    label_image.pack()

    label_username = tk.Label(root, text="Username")
    label_username.pack()
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Password")
    label_password.pack()
    global entry_password
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    button_login = tk.Button(root, text="Login", command=login)
    button_login.pack()

    root.mainloop()
def login():
    global username
    username = entry_username.get()
    password = entry_password.get()
    con = sql.connect("project.db")
    cur = con.cursor()
    statement = f"SELECT username from users WHERE username='{username}' AND Password = '{password}';"
    cur.execute(statement)
    if not cur.fetchone():
        messagebox.showerror("Login Failed", "Incorrect username or password")
    else:
         root.destroy()
         menu()
def is_admin(username):
    con = sql.connect("project.db")
    cur = con.cursor()
    statement = f"SELECT admin from users WHERE username='{username}';"
    cur.execute(statement)
    global result 
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
def menu():
    basescreen()
    root.title("Menu")
    img = PhotoImage(file="placeholder.png")
    img = img.subsample(2,2)
    label_image = tk.Label(root, image=img)
    label_image.pack()
    b1 = tk.Button(root, text="Complete evaluation", command=completeevalgui)
    b1.place(x=150,y=150)
    b2 = tk.Button(root, text="View historical data", command=hdatagui)
    b2.place(x=160,y=250)
    result =is_admin(username)
    if result == 'True':
        b3 = tk.Button(root, text = "Add account",command=addaccountgui)
        b3.place(x=190,y=350)
    root.mainloop()
def completeevalgui():
    basescreen()
    root.title("Complete evalution")
    b6 = tk.Button(root, text="Append to record",command= appendgui)
    b6.place(x=200,y=50)
    b7 = tk.Button(root,text='Add new record',command= newrecordgui)
    b7.place(x=200,y=150)
def appendgui():
    root.destroy()
    basescreen()
    root.title("Load record")
    label_id = tk.Label(root, text="Enter the persons id")
    label_id.pack()
    global entry_id
    entry_id = tk.Entry(root)
    entry_id.pack()
    b8 = tk.Button(root, text="Begin evaluation",command=pcheck)
    b8.place(x=200,y=50)
def pcheck():
    con = sql.connect('project.db')
    cur = con.cursor()
    global id
    id = entry_id.get()
    statement = f"SELECT idnum from persons WHERE idnum = '{id}'"
    cur.execute(statement)
    if cur.fetchone():
        loadquestion()
    else:
        messagebox.showerror("Error in creating account",'This ID doesnt exist')
def loadquestion():
    root.withdraw()
    con = sql.connect('project.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM questions")
    rows = cur.fetchall()
    global questions
    questions = []
    for row in rows:
        questiontext = row[1]
        answertexts = row[2].split(';')
        question = {'text': questiontext, 'answers': answertexts}
        questions.append(question)
    displayquestions(questions)

def displayquestions(questions):
    basescreen()
    root.title("Questions")
    global useranswers
    useranswers = []
    def displayquestion(index):
        question = questions[index]
        questiontext = question['text']
        var = tk.IntVar(value=-1)
        frame = tk.Frame(root)
        frame.pack()

        questionlabel = tk.Label(frame, text=questiontext)
        questionlabel.pack()

        def zero(): 
            var.set(0)

        def one(): 
            var.set(1)

        def two(): 
            var.set(2)
        r4 = tk.Radiobutton(frame, text='4', variable=var, command=zero,value=0)
        r0 = tk.Radiobutton(frame, text='0', variable=var, command=zero,value=0)
        r1 = tk.Radiobutton(frame, text='1', variable=var, command=one,value=1)
        r2 = tk.Radiobutton(frame, text='2', variable=var, command=two,value=2)
        r0.pack()
        r1.pack()
        r2.pack()



            

        def nextquestion():
            answer = var.get()
            if answer!=-1:
                useranswers.append(var.get())
                
                frame.destroy()
                if index < len(questions) - 1:
                    displayquestion(index + 1)
                else:
                    displayresults()
            else:
                messagebox.showerror('Error','Please pick an answer')

        nextbutton = tk.Button(frame, text="Next", command=nextquestion)
        nextbutton.pack()

        if index > 0:
            def prevquestion():
                useranswers.pop()
                frame.destroy()
                displayquestion(index - 1)
            prevbutton = tk.Button(frame, text="Back", command=prevquestion)
            prevbutton.pack()

    displayquestion(0)
    root.mainloop()
def displayresults():
    id = entry_id.get()
    total = 0
    btotal = 0
    etotal = 0
    r1total = 0
    r2total = 0
    itotal = 0
    for i in range(0,5):
        btotal = btotal + useranswers[i]
    for i in range(5,10):
        etotal = etotal + useranswers[i]
    for i in range(10,15):
        r1total = r1total +useranswers[i]
    for i in range(15,20):
        r2total = r2total + useranswers[i]
    for i in range(20,25):
        itotal = itotal + useranswers[i]
    global tarray
    tarray = [btotal,etotal,r1total,r2total,itotal]
    for i in range(0,len(tarray)):
        total = total + tarray[i]
    con = sql.connect("project.db")
    cur = con.cursor()
    id = int(id)
    statement = f"SELECT MAX(test_num) FROM tests WHERE idnum = '{id}'"
    cur.execute(statement)
    result  = cur.fetchone()
    if  result is None or result[0] is None :
        testnum = 1
    else:
        testnum = result[0] + 1
    statement = f"SELECT MAX(testid) FROM tests"
    cur.execute(statement)
    result =  cur.fetchone()
    if result is not None and result[0] is not None:
        resultf = result[0]
        testid = resultf + 1
    else:
        testid = 1
        
    root.destroy()
    CHART = NightingaleChart(tarray)
    CHART.draw_chart()
    knn()
    statement = f"INSERT INTO tests(testid, test_array, test_num, completed_by, idnum, total, outcome) VALUES ('{testid}','{tarray}','{testnum}','{username}','{id}','{total}','{fvalue}')"
    cur.execute(statement)
    con.commit()
    linegraphload()

def linegraphload():
    con = sql.connect('project.db')
    cur = con.cursor()
    statement = f"SELECT total FROM tests where idnum = '{id}'"
    cur.execute(statement)
    aresult = cur.fetchall()
    global flist
    flist = [x[0] for x in aresult]
    linegraph()

def linegraph():
    basescreen()
    root.title("Line Graph")
    root.configure(bg='white')
    canvas = tk.Canvas(root, width=500, height=400)
    canvas.pack()
    canvas.create_line(50, 350, 450, 350)
    canvas.create_line(50, 50, 50, 350)
    
    maxvalue = 50

    xscale = 400 / (len(flist)-1)
    yscale = 300 / maxvalue

    for i in range(0, maxvalue+1, 5):
        y = 300 - (i * yscale)+50
        canvas.create_text(40, y, text=str(i))
        canvas.create_line(50, y, 450, y, dash=(2, 5))
    
    for i in range(0,len(flist)):
        x = i * xscale +50 
        i=i+1
        canvas.create_text(x,360, text=str(i))
    for i, value in enumerate(flist[:-1]):
        x1 = i * xscale + 50
        y1 = 300 - value * yscale + 50
        x2 = (i + 1) * xscale + 50
        y2 = 300 - flist[i+1] * yscale + 50
        canvas.create_line(x1, y1, x2, y2, fill="blue")

    canvas.create_text(250, 380, text="Test number")
    canvas.create_text(20, 200, text="Score", angle=90)


def knn():
    con = sql.connect("project.db")
    cur = con.cursor()
    statement = f"SELECT test_array FROM tests"
    cur.execute(statement)
    result = cur.fetchall()
    flist = [x[0] for x in result]
    nlist = [json.loads(x) for x in flist]
    total = 0
    weightlist =[]
    acount = 0
    bcount = 0
    ccount = 0
    for i in range(0,len(nlist)-1):
        for j in range(0,4):
            temp = nlist[i][j] - tarray[j]
            temp = temp *temp
            total = total+temp
        distance = math.sqrt(total)
        total = 0
        if distance ==0:
            distance = 0.0001
        else:
            pass
        weight = 1/distance
        weightlist.append(weight)
    statement = f"SELECT outcome FROM tests"
    cur.execute(statement)
    result = cur.fetchall()
    rflist = [x[0] for x in result]
    global fvalue
    fvalue = ''
    for i in range(0,len(rflist)-1):
        if rflist[i] == 'A':
            acount = acount+weightlist[i]
        elif rflist[i] =='B':
            bcount = bcount+weightlist[i]
        else:
            ccount = ccount+weightlist[i]
    if acount>=bcount and acount>=ccount:
        fvalue = 'A'
        temp = 'Care home'
        wcount= acount
    if bcount>acount and bcount>=ccount:
        fvalue = 'B'
        temp = 'Foster care'
        wcount = bcount
    if ccount>acount and ccount>bcount:
        fvalue = 'C'
        temp = 'Supervised living home'
        wcount = ccount
    conscore = str(wcount/(acount+bcount+ccount))
    conscore = "Confidence level:"+conscore
    basescreen()
    root.title('Recommended outcome')
    textu = tk.Label(root, text = temp)
    textu.pack()
    texty = tk.Label(root, text =conscore)
    texty.pack()


            
def namevai(name):
     allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -')
     if not set(name).issubset(allowed_chars):
        return False
     if not name:
        return False
     if not any(char.isalpha() for char in name):
        return False
     return True
def newrecordgui():
    root.destroy()
    basescreen()
    root.title('Add record')
    label_firstname = tk.Label(root, text = "Firstname(s)")
    label_firstname.pack()

    global entry_firstname
    entry_firstname = tk.Entry(root)
    entry_firstname.pack()

    label_surname = tk.Label(root, text="Surname")
    label_surname.pack()

    global entry_surname
    entry_surname = tk.Entry(root)
    entry_surname.pack()

    label_dob = tk.Label(root, text="Date of birth (YYYY-MM-DD)")
    label_dob.pack()

    global entry_dob
    entry_dob = tk.Entry(root)
    entry_dob.pack()

    b8 = tk.Button(root,text='Add new record',command=newrecord)
    b8.place(x=200, y=150)
def newrecord():
    con = sql.connect("project.db")
    cur = con.cursor()
    firstname = entry_firstname.get()
    if namevai(firstname):
        surname = entry_surname.get()
        if namevai(surname):
            dob = entry_dob.get()
            try:
                date = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror("Invaild date","This date does not exist")
            if date < date.today():
                statement = f"SELECT MAX(idnum) FROM persons"
                cur.execute(statement)
                result = cur.fetchone()
                global id
                id = result[0]
                id = id + 1
                statement = f"INSERT INTO persons(idnum, firstname,surnames,dob) VALUES ('{id}', '{firstname}','{surname}','{date}');"
                cur.execute(statement)
                con.commit()
                id = str(id)
                message = ('ID is '+id)
                messagebox.showinfo("New record created", message)
                root.destroy()
            else:
                messagebox.showerror("Error in creating record",'That date is in the future')
        else:
            messagebox.showerror("Invaild surname",'Please correct the surname')
    else:
        messagebox.showerror("Invaild firstname",'Please correct the firstname')
def hdatagui():
    basescreen()
    root.title("View historical data")
    label_id = tk.Label(root, text="Enter the persons id")
    label_id.pack()
    global entry_id
    entry_id = tk.Entry(root)
    entry_id.pack()
    b5 = tk.Button(root, text="Load data",command=loaddata)
    b5.place(x=200,y=50)
def loaddata():
    idnum = entry_id.get()
    con = sql.connect("project.db")
    cur = con.cursor()
    statement = f"SELECT test_array from tests WHERE idnum='{idnum}'"
    result = cur.execute(statement)
    aresult = [x[0] for x in result]
    bresult = [json.loads(s) for s in aresult]
    if len(bresult) ==0:
        messagebox.showerror('Error','This id has no records')
    else:
        root.destroy()
        basescreen()
        root.title("Data")
        for i, array_1d in enumerate(bresult):
            array_label = tk.Label(root, text=str(array_1d))

            array_label_title = "Test " + str(i+1) +":"
            array_label.config(text=array_label_title +" " + array_label.cget("text"))
            array_label.pack()
def addaccountgui():
    basescreen()
    root.title("Add account")
    label_email = tk.Label(root, text = "Email")
    label_email.pack()

    global entry_email
    entry_email = tk.Entry(root)
    entry_email.pack()

    label_username = tk.Label(root, text="Username")
    label_username.pack()

    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Password min 8 characters")
    label_password.pack()

    global entry_password
    entry_password = tk.Entry(root)
    entry_password.pack()
    
    label_is_admin = tk.Label(root, text="Is Admin")
    label_is_admin.pack()
    global entryadmin
    entryadmin= BooleanVar()
    entry_admin = tk.Checkbutton(root,variable=entryadmin)
    entry_admin.pack()
    
    button_add_account = tk.Button(root, text="Add Account", command=uandechecker)
    button_add_account.pack()
def uandechecker():
    con = sql.connect("project.db")
    cur = con.cursor()
    username = entry_username.get()
    if username.isalnum():
        email = entry_email.get()
        statement = f"SELECT username from users WHERE username='{username}'"
        cur.execute(statement)
        if cur.fetchone():
            messagebox.showerror("error in creating account",'please pick a unique username')
        else:
            statement = f"SELECT email from users WHERE email ='{email}'"
            cur.execute(statement)
            if cur.fetchone():
                messagebox.showerror("error in creating account",'please use a unique email')
            else:
                emailcheck()
    else:
        messagebox.showerror("Error in creating account",'Usernames can only contain alphanumberic characters')
def emailcheck():
    receiver_address = entry_email.get()
    root.withdraw()
    basescreen()
    root.title("Verify email")
    sender_address = "CESS.SOFTWARE@gmail.com" 
    account_password = "zbtstzajwtrucoso" 
    subject = "Welcome to CESS"
    global code
    code = str(random.randint(1000,9999))
    body = ("Your code is ")
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(sender_address, account_password)
    message = f"Subject: {subject}\n\n{body}{code}"
    smtp_server.sendmail(sender_address, receiver_address, message)
    smtp_server.close()
    label_code = tk.Label(root, text = "Enter code sent to your email")
    label_code.pack()

    global entry_code
    entry_code = tk.Entry(root)
    entry_code.pack()
    b4 = tk.Button(root, text="Verify email",command=verify)
    b4.place(x=200,y=50)
def verify():
    ucode = entry_code.get()
    if code == ucode:
       add_account()
    else:
        messagebox.showerror("Incorrect code",'Please try again')
def add_account():
    con = sql.connect("project.db")
    cur = con.cursor()
    username = entry_username.get()
    password = entry_password.get()
    email =  entry_email.get()
    if len(password)<8:
        messagebox.showerror('Error when creating account','Please ensure that password is greater than 8 characters')
    else:
        admin= entryadmin.get()
        statement = f"INSERT INTO users (username, password,admin,email) VALUES ('{username}', '{password}','{admin}','{email}');"
        cur.execute(statement)
        con.commit()
        messagebox.showinfo("Account Created", "Account created successfully.")
        root.destroy()
class NightingaleChart:
    def __init__(self, tarray, width=400, height=400):
        self.tarray = tarray
        self.width = width
        self.height = height
        self.cx = width / 2
        self.cy= height / 2
        self.max_radius = 180
        self.colours = ['red', 'blue', 'green', 'yellow', 'purple']
        self.labels = ['Behaviour', 'Emotional wellbeing', 'Risk', 'Relationships', 'Indicators']
        self.N = len(self.tarray)

    def draw_sector(self, canvas, radius, start_angle, end_angle, fill_colour):
        points = [self.cx, self.cy]
        for angle in range(int(start_angle), int(end_angle) + 1):
            rad = math.radians(angle)
            x = self.cx + radius * math.cos(rad)
            y = self.cy + radius * math.sin(rad)
            points.extend([x, y])
        canvas.create_polygon(points, fill=fill_colour, outline='black')

    def draw_dotted_circle(self, canvas, radius):
        for angle in range(0, 360, 3):
            rad = math.radians(angle)
            x = self.cx + radius * math.cos(rad)
            y = self.cy + radius * math.sin(rad)
            canvas.create_oval(x, y, x + 1, y + 1, outline='black', width=0.5)

    def draw_axes(self, canvas):
        for i in range(6):
            self.draw_dotted_circle(canvas, i*36)
            for j in range(self.N):
                rad = (2 * math.pi / self.N) * j
                x = self.cx + (i / 5) * self.max_radius * math.cos(rad)
                y = self.cy + (i / 5) * self.max_radius * math.sin(rad)
                canvas.create_text(x, y, text=str(i * 2), anchor="center")

    def draw_chart(self):
        root = tk.Tk()
        root.title("Nightingale chart")
        canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        canvas.pack()
        self.draw_axes(canvas)

        for i, value in enumerate(self.tarray):
            radius = (value / 10) * self.max_radius
            start_angle = 72*i
            end_angle = 72*(i + 1)
            self.draw_sector(canvas, radius, start_angle, end_angle, self.colours[i])
            averrad = math.radians((start_angle + end_angle)/2)
            label_x = self.cx + self.max_radius * math.cos(averrad)
            label_y = self.cy + self.max_radius * math.sin(averrad)
            canvas.create_text(label_x, label_y, text=self.labels[i])


logingui()
