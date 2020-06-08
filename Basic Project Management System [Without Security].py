#The following code represents a project management system. It's a beginner project and consists of very basic features.
#The project's layout isn't responsive. So a long project title results in a choppy gui.
#You need to allow access to less secure apps in your gmail account for the sender using the following link if you intend to generate the report on your mail as well
#https://www.google.com/settings/security/lesssecureapps
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import smtplib
import mysql.connector
sel_proj=None
style=("Times New Roman",12,"bold")
con=mysql.connector.connect(user=input("Enter your MySQL username :\t"),password=input("Enter your MySQL password :\t"),database="proj1")
cur=con.cursor()

#scrolling
def scroll(msg,win,lab):
    global times
    msg=msg[1:]+msg[0]
    lab.config(text=msg,bg="deepskyblue")
    if (msg[0:5]=='.    '):
        times+=1
    if (times<2):
        win.after(100,lambda:scroll(msg,win,lab))
    else:
        win.after(100,lambda:clear(win,lab))

#clearing labels
def clear(win,lab):
    originalbg=win["bg"]
    lab.config(text="",bg=originalbg)

#switch tabs
def tab_switch(tab1,tab2,tab3,tab4,base,event):
    tab_id=event.widget.index("current")
    if (tab_id==0):
        newselproj(tab1,base)
        destruction(tab2)
        destruction(tab3)
        destruction(tab4)
    elif (tab_id==1):
        projprog(tab2,base)
    elif (tab_id==2):
        budgprog(tab3,base)
    elif (tab_id==3):
        activities(tab4,base)

#no project selected
def noprojsel(tab):
    tab.grid_columnconfigure(0,weight=1)
    l1=Label(tab,text="No Project Selected!",bg="black",fg="deeppink")
    l1.grid(row=0,column=0,padx=10,pady=(250,20))
    l1.config(font=("Snap ITC",40,"bold"))
    l2=Label(tab,text="Please select a project from the Create/Select Project Tab",bg="black",fg="orange")
    l2.grid(row=1,column=0,padx=10,pady=5)
    l2.config(font=("Times New Roman",20,"bold italic"))
    
#DESTRUCTION
def destruction(tab):
    allwid=tab.grid_slaves()
    for wid in allwid:
        wid.destroy()

#pie diag
def graphcan(projperc,tab,funcflag):
    projdeg=(projperc/100)*360
    can=Canvas(tab,height=500,width=700,bg="black",highlightthickness=0)
    can.grid(row=1,column=0)
    if (funcflag=="projprog"):
        legn1="Project Remaining";legn2="Completed Project"
    elif (funcflag=="budgprog"):
        legn1="Budget Remaining";legn2="Budget Consumed"
    #legend
    can.create_rectangle(450,2,475,23,fill="darkslateblue",outline="")
    can.create_rectangle(450,30,475,51,fill="turquoise",outline="")
    can.create_text(565,12,font="Times 16 bold",text=legn1,fill="mediumspringgreen")
    can.create_text(565,40,font="Times 16 bold ",text=legn2,fill="mediumspringgreen")
    #end of legend
    if (projdeg==360):
        can.create_oval(10,10,490,490,fill="turquoise",outline="")
    else:
        can.create_oval(10,10,490,490,fill="darkslateblue",outline="")
        can.create_arc(10,10,490,490,start=0,extent=projdeg,style="pieslice",fill="turquoise",outline="")
    #button
    genrep=Button(tab,text="Generate Report",bd=0,bg="black",fg="deeppink",command=lambda:gmail(legn1,legn2,projperc),activebackground="black",activeforeground="turquoise")
    genrep.grid(row=1,column=0,padx=(500,0),pady=(400,0))
    genrep.config(font=("Snap ITC",14))

#Generate report
def gmail(legn1,legn2,projperc):
    global undisplay;
    global projnamelab;
    global email;global pwd;
    proname=projnamelab["text"]
    msg=str("\n"+proname+"\n"+legn1+" : "+str(100-projperc)+"%\n"+legn2+" : "+str(projperc)+"%")
    user=undisplay["text"]
    cur.execute("select email from users where un='"+user+"'")
    data=cur.fetchall();rec=data[0][0]
    smtp=smtplib.SMTP("smtp.gmail.com",587)
    smtp.starttls()
    smtp.login(email,pwd)
    smtp.sendmail(email,rec,msg)
    messagebox.showinfo("Report Generated","Your gmail has recieved the report updates.")

#tab1
def prosel(lb,base,pre):
    global sel_proj
    global projnamelab
    sel_proj=lb.index("active")
    try:
        projnamelab.destroy()
    except NameError:
        pass
    cur.execute("select projname from projects where projid='"+str(sel_proj)+"'")
    data=cur.fetchall()
    projname=data[0][0]
    projnamelab=Label(base,text=projname,bg="black",fg="mediumspringgreen",anchor="nw")
    projnamelab.grid(row=1,column=1,sticky="nw")
    projnamelab.config(font=("Monotype Corsiva",17))
    pre.destroy()

def prodel(lb,base,pre):
    global sel_proj
    sel_proj=lb.index("active")
    try:
        projnamelab.destroy()
    except NameError:
        pass
    cur.execute("delete from projects where projid='"+str(sel_proj)+"'")
    con.commit()
    pre.destroy()

def delproj(base):
    pre=Tk()
    pre.title("Delete Project")
    pre.resizable(False,False)
    pre.config(bg="blueviolet")
    cur.execute("select * from projects")
    data=cur.fetchall()
    lbvar=StringVar()
    lb=Listbox(pre,activestyle="dotbox",bg="black",fg="turquoise",selectbackground="turquoise",selectforeground="black",bd=5)
    lb.grid(row=0,column=0,padx=40,pady=10)
    lb.config(font=("Monotype Corsiva",14))
    for record in data:
        lb.insert(int(record[4]),"    "+record[0])
    ok=Button(pre,text="Delete",bg="black",fg="turquoise",command=lambda:prodel(lb,base,pre),highlightthickness=10,highlightbackground="turquoise",activebackground="black",activeforeground="deeppink")
    ok.grid(row=1,column=0,padx=(40,0),pady=(0,20))
    ok.config(font=("Snap ITC",12))
    
def preproj(base):
    global projid
    pre=Tk()
    pre.title("Select Project")
    pre.resizable(False,False)
    pre.config(bg="blueviolet")
    cur.execute("select * from projects")
    data=cur.fetchall()
    lbvar=StringVar()
    lb=Listbox(pre,activestyle="dotbox",bg="black",fg="turquoise",selectbackground="turquoise",selectforeground="black",bd=5)
    lb.grid(row=0,column=0,padx=40,pady=10)
    lb.config(font=("Monotype Corsiva",14))
    for record in data:
        lb.insert(int(record[4]),"    "+record[0])
    ok=Button(pre,text="Okay!",bg="black",fg="turquoise",command=lambda:prosel(lb,base,pre),highlightthickness=10,highlightbackground="turquoise",activebackground="black",activeforeground="deeppink")
    ok.grid(row=1,column=0,padx=(40,0),pady=(0,20))
    ok.config(font=("Snap ITC",12))

def newprojcheck(ename,esub,estbuden,allbuden,new,lab):
    global times;times=0;
    global projid;
    newprojcheck=True
    cur.execute("select * from projects where projid=(select max(projid) from projects)")
    data=cur.fetchall()
    if ((ename.get()=="") or (esub.get()=="") or (estbuden.get()=="") or (allbuden.get()=="")):
        msg="Please fill all the fields.    "
        scroll(msg,new,lab)
        newprojcheck=False
    elif ((not estbuden.get().isdigit()) or (not allbuden.get().isdigit())):
        msg="Budgets should be integer values.    "
        scroll(msg,new,lab)
        newprojcheck=False
    if (data==list()):
        projid=0
    else:
        projid=int(data[0][4])+1
    if (newprojcheck==True):
        projname=ename.get();sub=esub.get();estbud=estbuden.get();allbud=allbuden.get();        
        cur.execute("insert into projects(projname,sub,estbud,allbud,projid) values('"+projname+"','"+sub+"','"+estbud+"','"+allbud+"','"+str(projid)+"')")
        con.commit()
        projid+=1
        messagebox.showinfo("Project Created","New Project Submitted! You can now select the project")
        new.destroy()
    
def newproj(base):
    new=Toplevel(base)
    new.title("Create A Project")
    new.geometry("580x290")
    new.config(bg="black")
    new.resizable(False,False)
    labsty=("Times New Roman",14,"bold")
    projname=Label(new,text="Project Name : ",bg="black",fg="yellow")
    projname.grid(row=0,column=0,padx=(10,0),pady=(10,0))
    projname.config(font=labsty)
    ename=Entry(new,width=50,highlightthickness=5,highlightbackground="deeppink",bg="black",fg="turquoise")
    ename.grid(row=0,column=1,padx=(10,0),pady=(10,0))
    ename.config(insertbackground="turquoise")
    subtitle=Label(new,text="Project Subtitles\n(Separated by semicolon(;))",bg="black",fg="yellow")
    subtitle.grid(row=1,column=0,padx=(10,0),pady=(10,0))
    subtitle.config(font=labsty)
    esub=Entry(new,width=50,highlightthickness=5,highlightbackground="deeppink",bg="black",fg="turquoise")
    esub.grid(row=1,column=1,padx=(10,0),pady=(10,0))
    esub.config(insertbackground="turquoise")
    estbud=Label(new,text="Estimated Budget : ",bg="black",fg="yellow")
    estbud.grid(row=2,column=0,padx=(10,0),pady=(10,0))
    estbud.config(font=labsty)
    estbuden=Entry(new,width=50,highlightthickness=5,highlightbackground="deeppink",bg="black",fg="turquoise")
    estbuden.grid(row=2,column=1,padx=(10,0),pady=(10,0))
    estbuden.config(insertbackground="turquoise")
    allbud=Label(new,text="Allocated Budget : ",bg="black",fg="yellow")
    allbud.grid(row=3,column=0,padx=(10,0),pady=(10,10))
    allbud.config(font=labsty)
    allbuden=Entry(new,width=50,highlightthickness=5,highlightbackground="deeppink",bg="black",fg="turquoise")
    allbuden.grid(row=3,column=1,padx=(10,0),pady=(10,0))
    allbuden.config(insertbackground="turquoise")
    lab=Label(new,text="",bg="black",width=47)
    lab.grid(row=5,column=0,columnspan=2,sticky="e")
    lab.config(font=labsty)
    submit=Button(new,text="Submit",command=lambda:newprojcheck(ename,esub,estbuden,allbuden,new,lab),bg="deeppink",activebackground="black",activeforeground="turquoise")
    submit.grid(row=6,column=1,pady=(10,10))
    submit.config(font=("Snap ITC",15))

def newselproj(tab1,base):
    tab1.grid_columnconfigure(0,weight=3)
    photo=PhotoImage(file="Aurora_2.pgm")
    backlab=Label(tab1,image=photo,height=620,width=855)
    backlab.image=photo
    backlab.grid(row=0,column=0,rowspan=6,columnspan=4,pady=(15,10),padx=20)
    heading=Label(tab1,text="Select/Delete a project\nOR\nSubmit a new project",bg="black",fg="cyan")
    heading.grid(row=0,column=0,pady=(150,20))
    heading.config(font=("Cooper Black",30))
    sel=Button(tab1,text="Select Project",command=lambda:preproj(base),bg="mediumspringgreen",activebackground="black",activeforeground="mediumspringgreen",width=13)
    sel.grid(row=1,column=0)
    newpro=Button(tab1,text="Create Project",command=lambda:newproj(base),bg="mediumspringgreen",activebackground="black",activeforeground="mediumspringgreen",width=13)
    newpro.grid(row=2,column=0)
    delpro=Button(tab1,text="Delete Project",command=lambda:delproj(base),bg="mediumspringgreen",activebackground="black",activeforeground="mediumspringgreen",width=13)
    delpro.grid(row=3,column=0)
    sel.config(font=("Broadway",22))
    newpro.config(font=("Broadway",22))
    delpro.config(font=("Broadway",22))

#tab2
def projprog(tab2,base):
    global sel_proj
    tab2.columnconfigure(0,weight=2)
    if (sel_proj==None):
        noprojsel(tab2)
    else:
        cur.execute("select * from projects where projid='"+str(sel_proj)+"'")
        data=cur.fetchall()
        fullsubs=len((data[0][1]).split(';'))
        if (data[0][5]==None):
            halfsubs=0
        else:
            halfsubs=len((data[0][5]).split(';'))
        projperc=int((halfsubs/fullsubs)*100)
        try:
            proglab.destroy()
        except NameError:
            pass
        proglab=Label(tab2,text="Project Progress : "+str(projperc)+"%",bg="black",fg="blue")
        proglab.grid(row=0,column=0,padx=30,pady=40)
        proglab.config(font=("Elephant",40))
        funcflag="projprog"
        graphcan(projperc,tab2,funcflag)

#tab3
def budgprog(tab3,base):
    global sel_proj
    tab3.columnconfigure(0,weight=2)
    if (sel_proj==None):
        noprojsel(tab3)
    else:
        cur.execute("select * from projects where projid='"+str(sel_proj)+"'")
        data=cur.fetchall()
        fullbudg=int(data[0][3])
        if (data[0][6]==None):
            halfbudg=0
        else:
            halfbudg=int(data[0][6])
        projperc=int((halfbudg/fullbudg)*100)
        try:
            proglab.destroy()
        except NameError:
            pass
        proglab=Label(tab3,text="Budget Utilized : "+str(projperc)+"%",bg="black",fg="blue")
        proglab.grid(row=0,column=0,padx=30,pady=40)
        proglab.config(font=("Elephant",40))
        funcflag="budgprog"
        graphcan(projperc,tab3,funcflag)

#tab4
def actcheck(tab4,cb,cbvar,budspent,data,lab):
    complsubs=list()
    complsubrec=""
    actflag=True
    if (budspent.get()==""):
        msg="Progress report requires budget to be submitted for the completed subitles.    "
        scroll(msg,tab4,lab)
        actflag=False
    elif (not budspent.get().isdigit()):
        msg="Budget should be integer value.    "
        scroll(msg,tab4,lab)
        actflag=False
    elif (int(budspent.get())>int(data[0][3])):
        msg="Budget spent is more than budget allocated.    "
        scroll(msg,tab4,lab)
        actflag=False
    if (data[0][6]!=None):
        if (int(data[0][6])==int(data[0][3])):
            msg="Allocated budget used up.    "
            scroll(msg,tab4,lab)
            actflag=False
        elif (int(data[0][3])<int(budspent.get())+int(data[0][6])):
            msg="Budget spent is more than budget allocated.    "
            scroll(msg,tab4,lab)
            actflag=False
    if (actflag==True):
        for s in range(len(cb)):
            if ((cbvar[s]).get()==1):
                complsubs.append(cb[s]["text"])
        for s in range(len(complsubs)):
            if (complsubs!=[]):
                if (s==len(complsubs)-1):
                    complsubrec=complsubrec+complsubs[s]
                else:
                    complsubrec=complsubrec+complsubs[s]+';'
        if (data[0][5]==None):
            finalsubs=complsubrec
        else:
            finalsubs=complsubrec+';'+data[0][5]
        if (complsubrec!=""):
            if (data[0][6]==None):
                totbudg=budspent.get()
            else:
                totbudg=(data[0][6])+int(budspent.get())
            cur.execute("update projects set complsubs='"+finalsubs+"',complbudg='"+str(totbudg)+"' where projid='"+str(data[0][4])+"'")
            con.commit()
            messagebox.showinfo("Updates Submitted!","Your progress has been submitted")
            destruction(tab4)

def activities(tab4,base):
    global sel_proj
    global budspentlab
    global cb;global cbvar
    cb=[];cbvar=[]
    if (sel_proj==None):
        noprojsel(tab4)
    else:
        cur.execute("select * from projects where projid='"+str(sel_proj)+"'")
        data=cur.fetchall()
        subs=(data[0][1]).split(';')
        bud1=data[0][2];bud2=data[0][3]
        lcb=Label(tab4,text="Check the SUBTITLES that are COMPLETED",bg="black",fg="blueviolet")
        lcb.grid(row=0,column=0,padx=(0,5),pady=(20,10),sticky="ws")
        lcb.config(font=("Times New Roman",20,"bold underline"))
        if (data[0][5]==None):
            for i in range(len(subs)):
                a="cb"+str(i)
                b="cbvar"+str(i)
                b=IntVar()
                a=Checkbutton(tab4,text=subs[i],variable=b,bg="black",fg="mediumspringgreen",selectcolor="blueviolet",activebackground="black",activeforeground="deeppink")
                a.grid(row=i+1,column=0,padx=30,sticky="w")
                a.config(font=("Monotype Corsiva",17))
                cb.append(a);cbvar.append(b)
        else:
            complsubs=(data[0][5]).split(';')
            if (len(complsubs)==len(subs)):
                destruction(tab4)
                return
            for i in range(len(subs)):
                com=False
                for j in range(len(complsubs)):
                    if (subs[i]==complsubs[j]):
                        com=True
                if (com==False):
                    a="cb"+str(i)
                    b="cbvar"+str(i)
                    b=IntVar()
                    a=Checkbutton(tab4,text=subs[i],variable=b,bg="black",fg="mediumspringgreen",selectcolor="blueviolet",activebackground="black",activeforeground="deeppink")
                    a.grid(row=i+1,column=0,padx=30,sticky="w")
                    a.config(font=("Monotype Corsiva",17))
                    cb.append(a);cbvar.append(b)
        bud1lab=Label(tab4,text="Estimated Budget : "+str(bud1),bg="black",fg="turquoise")
        bud1lab.grid(row=0,column=1,padx=(20,0),sticky="w")
        bud1lab.config(font=("Times",15,"bold"))
        bud2lab=Label(tab4,text="Allocated Budget : "+str(bud2),bg="black",fg="turquoise")
        bud2lab.grid(row=1,column=1,padx=(20,0),sticky="w")
        bud2lab.config(font=("Times",15,"bold"))
        lab=Label(tab4,text="",width=60,bg="black")
        lab.grid(row=len(subs)+2,column=0,columnspan=2)
        lab.config(font=("Times",15,"bold"))
        if (data[0][6]==None):
            spentdis=str(0)
        elif (data[0][6]==bud2):
            destruction(tab4)
            return
        else:
            spentdis=str(data[0][6])
        try:
            budspentlab.destroy()
        except NameError:
            pass
        budspentlab=Label(tab4,text="Budget Spent : "+spentdis,bg="black",fg="turquoise")
        budspentlab.grid(row=2,column=1,padx=(20,0),pady=15,sticky="w")
        budspentlab.config(font=("Times",15,"bold"))
        budup=Label(tab4,text="Update Budget : ",bg="black",fg="turquoise")
        budup.grid(row=3,column=1,padx=(20,0),sticky="ws")
        budup.config(font=("Times",15,"bold"))
        budspent=Entry(tab4,width=33,bg="black",fg="turquoise",highlightthickness=3,highlightbackground="deeppink")
        budspent.grid(row=4,column=1,padx=(20,0),pady=10,sticky="n")
        budspent.config(insertbackground="turquoise",font=("Helvetica",10,"bold"))
        submit=Button(tab4,text="Submit",bg="mediumspringgreen",command=lambda:actcheck(tab4,cb,cbvar,budspent,data,lab),activebackground="black",activeforeground="turquoise")
        submit.grid(row=5,column=1,pady=(0,10))
        submit.config(font=("Snap ITC",14))

#main window
def base(username):
    global undisplay;
    global favcom;
    base=Tk()
    base.title(favcom+" Project System Management")
    base.config(bg="black")
    base.grid_columnconfigure(0,weight=2)
    welcome=Label(base,text="Welcome To The Project System Management",bg="black",fg="mediumspringgreen")
    welcome.grid(row=0,column=0,columnspan=2)
    welcome.config(font=("Cooper Black",15))
    nb=ttk.Notebook(base,style="lefttab.TNotebook")
    tab1=Frame(nb,height=670,width=970,bg="black",highlightbackground="mediumspringgreen",highlightthickness=5)
    tab2=Frame(nb,height=670,width=970,bg="black",highlightbackground="mediumspringgreen",highlightthickness=5)
    tab3=Frame(nb,height=670,width=970,bg="black",highlightbackground="mediumspringgreen",highlightthickness=5)
    tab4=Frame(nb,height=670,width=970,bg="black",highlightbackground="mediumspringgreen",highlightthickness=5)
    nb.add(tab1,text="Select/Create/Delete\n            Project")
    nb.add(tab2,text="Project Progress")
    nb.add(tab3,text="Project Budget")
    nb.add(tab4,text="Activities")
    nb.grid(row=1,column=0)
    nb.bind("<ButtonRelease-1>",lambda event:tab_switch(tab1,tab2,tab3,tab4,base,event))
    tabsty=ttk.Style()
    alltab="#00BFFF"
    seltab="#8A2BE2"
    tabsty.theme_create("try", parent="clam", settings={"lefttab.TNotebook": {"configure": {"tabmargins": 0, "tabposition": "w", "background": "mediumspringgreen"}}, "lefttab.TNotebook.Tab": {"configure": {"padding": [10,60], "background": alltab, "foreground": "black", "font": "Elephant 25", "width":15, "height": 100},"map": {"background": [("selected",seltab)], "expand": [("selected",[5,5,5,0])]}}})
    tabsty.configure("lefttab.TNotebook",tabposition="w")
    tabsty.theme_use("try")
    undisplay=Label(base,text=username,bg="black",fg="mediumspringgreen",anchor="w")
    undisplay.grid(row=0,column=1,padx=(0,30),sticky="w")
    undisplay.config(font=("comic sans",14))
    base.mainloop()

#new account
def check1(entries,req,signwin):
    global times
    times=0
    checkflag=True
    a=entries[0].get();b=entries[1].get();c=entries[2].get();d=entries[3].get();e=entries[4].get();f=entries[5].get();g=entries[6].get()
    for i in range(0,7):
        if (entries[i].get()==""):
            msg="Please fill out all the fields.    "
            scroll(msg,signwin,req)
            checkflag=False
            return
    if (not entries[1].get().isdigit()):
        msg="Unique I.D. should be digits.    "
        scroll(msg,signwin,req)
        checkflag=False
    if ((g)[-10:]!="@gmail.com"):
        g+="@gmail.com"
    cur.execute("select * from users")
    data=cur.fetchall()
    for record in data:
        if (b==str(record[1])):
            msg="Unique I.D. already exists. It should be unique.    "
            scroll(msg,signwin,req)
            checkflag=False
        elif (e==record[4]):
            msg="User Name already EXISTS. Please pick another User Name.    "
            scroll(msg,signwin,req)
            checkflag=False
        elif (f==record[5]):
            msg="Password already EXISTS. Please pick another Password.    "
            scroll(msg,signwin,req)
            checkflag=False
    if (checkflag==True):
        cur.execute("insert into users values('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"')")
        con.commit()
        messagebox.showinfo("New Account Created","You have successfully created a new account.\nLogin NOW to start EXPLORING")
        signwin.destroy()        

def signfun(text):
    signwin=Toplevel(root)
    signwin.title(text)
    signwin.geometry("330x280")
    label=["lname","lid","ldept","ldoj","lun","lpw","lmail"]
    write=["Name : ","Unique I.D. : ","Current Department : ","Date Of Join (mm/dd/yyyy) : ","User Name : ","PassWord : ","Email : "]
    for i in range(0,7):
        label[i]=Label(signwin,text=write[i])
        label[i].grid(row=i,column=0,padx=10,pady=(10,0))
    entries=["name","idn","dept","doj","un","pw","mail"]
    for i in range(0,7):
        entries[i]=Entry(signwin)
        entries[i].grid(row=i,column=1,padx=10,pady=(10,0))
    ca=Button(signwin,text="Create Account",bg="skyblue",command=lambda:check1(entries,req,signwin))
    ca.grid(row=8,column=1,pady=(0,10))
    req=Label(signwin,text="",width=33)
    req.grid(row=7,column=0,columnspan=2)
    req.configure(font=("Times New Roman",12,"bold italic"))

#loggin into an account
def check2(logwin,un,pw,lerror):
    global times;
    times=0
    logged=False
    username=un.get()
    password=pw.get()
    unflag=False;pwflag=False;
    cur.execute("select * from users")
    data=cur.fetchall()
    for record in data:
        if (record[4]==username):
            unflag=True
        if (record[5]==password):
            pwflag=True
    if (unflag==False and pwflag==True):
        msg="User Name doesn't exist.    "
        scroll(msg,logwin,lerror)
    elif (unflag==True and pwflag==False):
        msg="Invalid Password.    "
        scroll(msg,logwin,lerror)
    elif (unflag==False and pwflag==False):
        msg="Invalid Username and Password.    "
        scroll(msg,logwin,lerror)
    elif (unflag==True and pwflag==True):
        messagebox.showinfo("Logged In","Successfully logged into your account.")
        logwin.destroy()
        root.destroy()
        base(username)

def logfun(text):
    logwin=Toplevel(root)
    logwin.title(text)
    lun=Label(logwin,text="User Name : ")
    lun.grid(row=0,column=0,padx=(10,0),pady=(10,0))
    un=Entry(logwin)
    un.grid(row=0,column=1,padx=(0,10),pady=(10,0))
    lpw=Label(logwin,text="Password : ")
    lpw.grid(row=1,column=0,padx=(10,0),pady=(10,0))
    pw=Entry(logwin,show="*")
    pw.grid(row=1,column=1,padx=(0,10),pady=(10,0))
    lerror=Label(logwin,text="")
    lerror.grid(row=2,column=0,columnspan=2,pady=(10,0))
    lerror.config(font=style)
    ok=Button(logwin,text="Okay!",command=lambda:check2(logwin,un,pw,lerror),height=1,width=5,bg="lawn green",fg="darkgreen")
    ok.grid(row=3,column=1,pady=(0,10))
    ok.configure(font=("Snap ITC",12))
    logwin.bind("<Return>",lambda event:check2(logwin,un,pw,lerror))

#start window
global email;global pwd;
favcom=input("Insert Company Name Here :\t")
email=input("Enter E-Mail ID :\t")
pwd=input("Enter Password :\t")
root=Tk()
root.title(favcom+" Project Management System")
warning=Label(root,bg="red2",text="NOTE : YOU CAN VIEW THE PROJECT'S MANAGED BY "+favcom+" ONLY IF YOU ARE A PART OF THIS ORGANISTAION")
warning.configure(font=style)
warning.grid(row=0,column=0)
sign1=Label(root,text="If you are new to this organisation, click the SignUp button for creating a new account")
sign1.grid(row=2,column=0,pady=(20,0))
sign=Button(root,text="SignUp",command=lambda:signfun(sign["text"]))
sign.grid(row=3,column=0)
log1=Label(root,text="Account already exists? Click the Login button for logging into your account")
log1.grid(row=4,column=0,pady=(30,0))
log=Button(root,text="Login",command=lambda:logfun(log["text"]))
log.grid(row=5,column=0,pady=(0,10))
root.mainloop()
