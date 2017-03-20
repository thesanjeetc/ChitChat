#!/usr/bin/python3

import smtplib
import getpass
import imaplib
import email
import time
import _thread
from tkinter import *
import tkinter.messagebox
import py_compile

global username
global password

#################################################
                                                
#Just put in your username and password below   
                                                                                                
username = "Your Gmail Username"         
password = "Your Password"                        
                                                
#################################################

global last_checked
last_checked = -1

class Main:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid()
        self.welcome = Label(self.frame, text="Welcome to", font=("Courier", 22),width=23)
        self.welcome.grid(row=0, column=1, pady=(70,0), padx=10, sticky=W)
        c = u"\u2122"
        l = Text(self.frame, width=30, height=2, borderwidth=0, font=("Courier",46), fg="blue", background=self.frame.cget("background"))
        l.tag_configure("subscript", offset=20)
        l.insert("insert", "ChitChat", "")
        l.configure(state="disabled")
        l.grid(row=1, column=1, pady=20, padx=58)
        self.credits = Label(self.frame, text="Created by Sanjeet Chatterjee", font=("Courier", 14),width=35)
        self.credits.grid(row=2, column=1, pady=(0,0), padx=10, sticky=W)
        self.frame.after(2500, lambda: self.change())
        

    def change(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.message1 = Label(self.frame, text="Loading...", font=150)
        self.message1.grid(row=0, column=1, pady=(22,12), padx=10, sticky=W)
        self.message2 = Label(self.frame, text="", font=150)
        self.message2.grid(row=1, column=1, pady=12, padx=10, sticky=W)
        self.message3 = Label(self.frame, text="", font=150)
        self.message3.grid(row=2, column=1, pady=12, padx=10, sticky=W)
        self.message4 = Label(self.frame, text="", font=150)
        self.message4.grid(row=3, column=1, pady=12, padx=10, sticky=W)
        self.message5 = Label(self.frame, text="", font=150, fg="red")
        self.message5.grid(row=4, column=1, pady=12, padx=10, sticky=W)
        self.user = getpass.getuser()
        self.smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtpserver.ehlo()
        self.smtpserver.starttls()
        self.smtpserver.ehlo()
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        global username
        global password
        try:
            mail.login(username, password)
            mail.list()
            mail.select("Inbox")
            result, uidlist = mail.search(None, "ALL")
            try:
                id1 = uidlist[0].split()[-1]
                id2 = uidlist[0].split()[-2]
                id3 = uidlist[0].split()[-3]
                id4 = uidlist[0].split()[-4]
                id5 = uidlist[0].split()[-5]
                result, uidlist = mail.search(None, "ALL")
                result, data = mail.fetch(id1, "(RFC822)")
                t1 = email.message_from_string(data[0][1].decode('utf-8'))
                self.text1 = str(t1.get_payload()).strip()
                result, data = mail.fetch(id2, "(RFC822)")
                t2 = email.message_from_string(data[0][1].decode('utf-8'))
                self.text2 = str(t2.get_payload()).strip()
                result, data = mail.fetch(id3, "(RFC822)")
                t3 = email.message_from_string(data[0][1].decode('utf-8'))
                self.text3 = str(t3.get_payload()).strip()
                result, data = mail.fetch(id4, "(RFC822)")
                t4 = email.message_from_string(data[0][1].decode('utf-8'))
                self.text4 = str(t4.get_payload()).strip()
                result, data = mail.fetch(id5, "(RFC822)")
                t5 = email.message_from_string(data[0][1].decode('utf-8'))
                self.text5 = str(t5.get_payload()).strip()
                _thread.start_new_thread(self.fetch,())
            except IndexError:
                self.text5 = ""
                self.text4 = ""
                self.text3 = ""
                self.text2 = ""
                self.text1 = ""
                _thread.start_new_thread(self.fetch,())
            self.send = Button(text="Send", command = self.chat, width= 25)
            self.send.grid(row=6,columnspan=100, sticky=W, padx = 115, pady=10)
            self.t = Entry(width=60)
            self.t.grid(row=5, columnspan=100, sticky=W,padx=30, pady=(20,0))
            self.t.bind('<Return>', self.chat)
        except imaplib.IMAP4.error as abc:
            if(username == "Your Gmail Username" and password ==  "Your Password"):
                tkinter.messagebox.showerror("Error", "You will need to edit the script and add your username and password")
                self.message1.configure(text="Error!",fg="red")
            else:
                tkinter.messagebox.showerror("Error", abc)
                self.message1.configure(text="Error!",fg="red")
    
    def fetch_command(self, mail):
        global last_checked
        mail.list()
        mail.select("Inbox")
        result, uidlist = mail.search(None, "ALL")
        try:
            latest_email_id = uidlist[0].split()[-1]
            if latest_email_id == last_checked:
                return False
            self.text5 = self.text4
            self.text4 = self.text3
            self.text3 = self.text2
            self.text2 = self.text1
            last_checked = latest_email_id
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            t1 = email.message_from_string(data[0][1].decode('utf-8'))
            self.text1 = str(t1.get_payload()).strip()
            self.message1.configure(text=self.text5, fg="black")
            self.message2.configure(text=self.text4, fg="black")
            self.message3.configure(text=self.text3)
            self.message4.configure(text=self.text2)
            self.message5.configure(text=self.text1)
            return True
        except IndexError:
            self.message1.configure(text="You have no messages yet.",fg="green")
            self.message2.configure(text="Try it out by sending one below.",fg="green")
            self.message3.configure(text="")
            self.message4.configure(text="")
            self.message5.configure(text="")
            
    def fetch(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        global username
        global password
        mail.login(username, password)
        while True:
            try:
                global c
                c = self.fetch_command(mail)
            except Exception as exc:
                print("Received an exception while running: {exc}"
                      "\nRestarting...".format(**locals()))
            time.sleep(1)

    def chat(self, *args):
        global username
        global password
        self.smtpserver.login(username,password)
        self.message = self.t.get()
        if(self.message):
            self.msg = "\n" + self.user + ": " + self.message
            self.smtpserver.sendmail(username, username,self.msg)
            self.t.delete(0, 'end')
            self.prevm = self.message

def run():
    root = Tk()
    root.wm_title("ChitChat")

    w = 420
    h = 360
    x = str(int((root.winfo_screenwidth() - w) / 2))
    y = str(int((root.winfo_screenheight() - h) / 2))
    root.geometry("%sx%s+%s+%s" % (w, h, x, y))

    Main(root)
    root.mainloop()
    root.destroy()
    
if __name__ == '__main__':
    run()

    

