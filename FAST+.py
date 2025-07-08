### Fast Program Source code ###
### © 2023 All right reserved to FAST+ Team ###
### For more details please contact: kneprogram@gmail.com ###

##Stand by code if we have problem with main code##
##Last Update 7/8/2023 on 00:00##
##FAST+ !Development version! FAST+ #V.1.7.0 DV.7.0##
##This is standby code on competition##
##All Right reserved to FAST+ Team more detail www.fastknep.com##
##What this version update?##
## -Main file ##

############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
from tkinter import messagebox 
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import schedule
import threading
import webbrowser

########################################### Shortcuts CMD ###############################################

camera=0
BoxC='#dce5f4'
ButtonC='#5678bd'
FontA= 'SF Pro Display' 
TextC='#ffffff'

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    website_url = "https://web.facebook.com/messages/t/1300146376672959"
    webbrowser.open_new(website_url)

###################################################################################

def ourwebsite():
    website_url = "https://sites.google.com/kanlayanee.ac.th/fastplus/home"
    webbrowser.open_new(website_url)

###################################################################################

def student_detail():
    file_path = r"D:\Comproject\FAST+\StudentDetails"  # Update this path to the correct folder with student details files
    file_extension = ".csv"  # Update the file extension as needed

    # Get a list of all files in the specified path with the given extension
    files = [f for f in os.listdir(file_path) if f.endswith(file_extension)]

    # Ensure that at least one file with the specified extension exists in the folder
    if len(files) > 0:
        # Sort files by modification time (latest first)
        sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)

        # Get the full path of the latest file
        latest_file = os.path.join(file_path, sorted_files[0])

        # Open the latest file using the default associated program
        os.startfile(latest_file)
    else:
        # Display a message if no files with the specified extension are found
        import tkinter.messagebox as mess
        mess.showwarning("Student Details", f"No student detials found!")
        
###################################################################################

def read_csv_files(folder_path):
    files = os.listdir(folder_path)
    dataframes = []
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            dataframes.append(df)
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    return None

def find_attendance():
    student_id = student_id_entry.get()
    if not student_id:
        messagebox.showwarning("Warning", "Please enter a student ID.")
        return

    attendance_df = read_csv_files(r"D:\Comproject\FAST+\Attendance")
    if attendance_df is None or attendance_df.empty:
        messagebox.showinfo("No Data", "No attendance data found.")
        return

    student_attendance = attendance_df[attendance_df["Id"] == int(student_id)]
    if student_attendance.empty:
        messagebox.showinfo("No Data", f"No attendance data found for Student ID: {student_id}.")
    else:
        total_attendance = student_attendance.shape[0]
        messagebox.showinfo("Attendance Summary", f"Student ID: {student_id}\nTotal Attendance: {total_attendance}")

def studentid_attendance():
    root = tk.Toplevel()
    root.title("Student Attendance")
    root.geometry("400x150")
    root.configure(bg="#f4f8ff")  # Set the background color of the root window
    icon_path = r"D:\Comproject\FAST+\Images\fasticongui.ico"
    root.iconbitmap(icon_path)

    frame = tk.Frame(root, bg="#f4f8ff")  # Set the background color of the frame
    frame.pack(padx=20, pady=20)

    label = tk.Label(frame, text="Check Student Attendance", font=("FontA", 16, "bold"), bg="#f4f8ff")
    label.pack(side=tk.TOP, pady=10)

    global student_id_entry
    student_id_entry = tk.Entry(frame, font=("FontA", 12))
    student_id_entry.pack(side=tk.LEFT, padx=5)

    check_button = tk.Button(frame, text="Check!", font=("FontA", 12), command=find_attendance, bg="#f4f8ff")
    check_button.pack(side=tk.LEFT, padx=10)


###################################################################################

def today_attendance():
    file_path = r"D:\Comproject\FAST+\Attendance"

    # Get a list of all files in the specified path
    files = os.listdir(file_path)

    # Sort files by modification time (latest first)
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)

    # Ensure that at least one file exists in the folder
    if len(sorted_files) > 0:
        # Get the full path of the latest file
        latest_file = os.path.join(file_path, sorted_files[0])

        # Get the date from the latest file's name
        file_date_str = os.path.splitext(sorted_files[0])[0].split("_")[1]
        file_date = datetime.datetime.strptime(file_date_str, "%d-%m-%Y").date()

        # Get the current date
        current_date = datetime.date.today()

        # Check if the latest file matches the current date
        if file_date == current_date:
            # Open the latest file using the default associated program
            os.startfile(latest_file)
        else:
            # Display a message in a new UI window saying "No data for today, please record data first."
            import tkinter as tk
            from tkinter import messagebox as mess

            root = tk.Tk()
            root.withdraw()  # Hide the main window

            mess.showinfo("Attendance", "You are not record attendance today yet!")
            root.destroy()

    else:
        print("No attendance files found for today.")
        
###################################################################################
stop_tracking_time = None

def TrackImagesSchedule():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(camera)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    attendance = []  # Initialize empty list for attendance records
    recognized_ids = set()  # Initialize a set to keep track of recognized IDs

    global stop_tracking_time
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                if serial not in recognized_ids:  # Check if the face ID is not already recognized
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance.append([str(ID), '', bb, '', str(date), '', str(timeStamp)])  # Append to attendance list
                    recognized_ids.add(serial)  # Add the recognized ID to the set
                    cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)  # Display the name inside the rectangle
                    cv2.putText(im, "Record ready", (x, y - 20), font, 0.8, (0, 255, 0), 2)  # Display "Record ready" for new faces
                else:
                    cv2.putText(im, "Attendance Check", (x, y - 20), font, 0.8, (0, 255, 0), 2)  # Display "Recorded" for already recognized faces

            else:
                Id = 'Come Closer'
                bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)  # Display 'Unknown' inside the rectangle

        cv2.imshow('Taking Attendance', im)

        current_time = datetime.datetime.now().time()
        if stop_tracking_time is not None and current_time >= stop_tracking_time:
            print("Attendance tracking stopped.")
            break

        if (cv2.waitKey(1) == ord('q')):
            break
        if (cv2.waitKey(1) == ord('f')):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            for record in attendance:
                writer.writerow(record)  # Write each attendance record
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            for record in attendance:
                writer.writerow(record)  # Write each attendance record
        csvFile1.close()

    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

def set_attendance_times():

    def start_attendance_tracking():
        print("Start Attendance Tracking")
        TrackImagesSchedule()

    def stop_attendance_tracking():
        print("Stop Attendance Tracking")
        
    def save_times():
        start_hour = start_hour_var.get()
        start_minute = start_minute_var.get()
        end_hour = end_hour_var.get()
        end_minute = end_minute_var.get()
        global stop_tracking_time
        stop_tracking_time = datetime.time(end_hour, end_minute)
        # Validate the start and end time format
        try:
            start_time = f"{start_hour:02d}:{start_minute:02d}"
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            datetime.datetime.strptime(start_time, "%H:%M")
            datetime.datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Time Format", "Please enter valid time values.")
            return

        print("Start Time:", start_time)
        print("End Time:", end_time)

        schedule.every().day.at(f"{start_hour:02d}:{start_minute:02d}").do(start_attendance_tracking)

        schedule.every().day.at(f"{end_hour:02d}:{end_minute:02d}").do(stop_attendance_tracking)

        top.destroy()

        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(1)

        threading.Thread(target=run_schedule).start()

    top = tk.Toplevel()
    top.title("Set Attendance Times")
    top.geometry("500x300")
    top.resizable(False,False)
    icon_path = r"D:\Comproject\FAST+\Images\fasticongui.ico"
    top.iconbitmap(icon_path)
    top.configure(bg="#f4f8ff")

    label = tk.Label(top, text="Set Start Time and End Time", font=("FontA", 16, "bold"), bg="#f4f8ff")
    label.pack(pady=10)

    # Start Time Inputs
    start_frame = tk.Frame(top, bg="#f4f8ff")
    start_frame.pack(pady=5)

    start_label = tk.Label(start_frame, text="Start Time", font=("FontA", 12, "bold"), bg="#f4f8ff")
    start_label.grid(row=0, column=0, padx=5, pady=5)

    start_hour_var = tk.IntVar()
    start_hour_var.set(0)  # Default value for start hour

    start_hour_combobox = ttk.Combobox(start_frame, font=("FontA", 12), values=[f"{hour:02d}" for hour in range(24)], width=3, textvariable=start_hour_var)
    start_hour_combobox.grid(row=1, column=1, padx=5, pady=5)

    start_minute_var = tk.IntVar()
    start_minute_var.set(0)  # Default value for start minute

    start_minute_combobox = ttk.Combobox(start_frame, font=("FontA", 12), values=[f"{minute:02d}" for minute in range(60)], width=3, textvariable=start_minute_var)
    start_minute_combobox.grid(row=1, column=2, padx=5, pady=5)

    start_hour_label = tk.Label(start_frame, text="Hours", font=("FontA", 10), bg="#f4f8ff")
    start_hour_label.grid(row=1, column=0)

    start_minute_label = tk.Label(start_frame, text="Minutes", font=("FontA", 10), bg="#f4f8ff")
    start_minute_label.grid(row=1, column=3)

    # End Time Inputs
    end_frame = tk.Frame(top, bg="#f4f8ff")
    end_frame.pack(pady=5)

    end_label = tk.Label(end_frame, text="End Time", font=("FontA", 12, "bold"), bg="#f4f8ff")
    end_label.grid(row=0, column=0, padx=5, pady=5)

    end_hour_var = tk.IntVar()
    end_hour_var.set(0)  # Default value for end hour

    end_hour_combobox = ttk.Combobox(end_frame, font=("FontA", 12), values=[f"{hour:02d}" for hour in range(24)], width=3, textvariable=end_hour_var)
    end_hour_combobox.grid(row=1, column=1, padx=5, pady=5)

    end_minute_var = tk.IntVar()
    end_minute_var.set(0)  # Default value for end minute

    end_minute_combobox = ttk.Combobox(end_frame, font=("FontA", 12), values=[f"{minute:02d}" for minute in range(60)], width=3, textvariable=end_minute_var)
    end_minute_combobox.grid(row=1, column=2, padx=5, pady=5)

    end_hour_label = tk.Label(end_frame, text="Hours", font=("FontA", 10), bg="#f4f8ff")
    end_hour_label.grid(row=1, column=0)

    end_minute_label = tk.Label(end_frame, text="Minutes", font=("FontA", 10), bg="#f4f8ff")
    end_minute_label.grid(row=1, column=3)

    save_button = tk.Button(top, text="Save", font=("FontA", 12), command=save_times, bg="#f4f8ff")
    save_button.pack(pady=10)

###################################################################################


def open_file(file_path):
    os.startfile(file_path)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def show_files(file_list, page_num, files_per_page, file_path):
    clear_frame(frame)  # Clear the previous file entries

    start_idx = (page_num - 1) * files_per_page
    end_idx = min(start_idx + files_per_page, len(file_list))

    for idx in range(start_idx, end_idx):
        file = file_list[idx]
        file_full_path = os.path.join(file_path, file)

        file_label = tk.Label(frame, text=file, font=(FontA, 14), bg="#f4f8ff")
        file_label.pack(side=tk.TOP, anchor=tk.W)

        view_button = tk.Button(frame, text="View", font=("FontA", 12), command=lambda path=file_full_path: open_file(path), bg="#f4f8ff")
        view_button.pack(side=tk.TOP, anchor=tk.E, pady=5)

    if end_idx < len(file_list) and not hasattr(show_files, "next_page_button"):
        show_files.next_page_button = tk.Button(navigation_frame, text="Next Page", font=("FontA", 12), command=lambda: next_page(file_list, files_per_page, file_path), bg="#f4f8ff")
        show_files.next_page_button.pack(side=tk.RIGHT)

    if page_num > 1 and not hasattr(show_files, "prev_page_button"):
        show_files.prev_page_button = tk.Button(navigation_frame, text="Previous Page", font=("FontA", 12), command=lambda: prev_page(file_list, files_per_page, file_path), bg="#f4f8ff")
        show_files.prev_page_button.pack(side=tk.LEFT)

    update_page_label(page_num, files_per_page, file_list)

def update_page_label(current_page, files_per_page, file_list):
    total_pages = (len(file_list) + files_per_page - 1) // files_per_page
    page_label.config(text=f"Page {current_page}/{total_pages}")

def next_page(file_list, files_per_page, file_path):
    global current_page
    current_page += 1
    show_files(file_list, current_page, files_per_page, file_path)

def prev_page(file_list, files_per_page, file_path):
    global current_page
    current_page -= 1
    show_files(file_list, current_page, files_per_page, file_path)

def other():
    root = tk.Toplevel()
    root.title("Attendance History")
    root.geometry("700x700")
    root.configure(bg="#f4f8ff")  # Set the background color of the root window
    icon_path = r"D:\Comproject\FAST+\Images\fasticongui.ico"
    root.iconbitmap(icon_path)

    global frame
    frame = tk.Frame(root, bg="#f4f8ff")  # Set the background color of the frame
    frame.pack(padx=20, pady=20)

    label = tk.Label(frame, text="Attendance History", font=("FontA", 20, "bold"), bg="#f4f8ff")
    label.pack(side=tk.TOP, pady=10)

    global navigation_frame
    navigation_frame = tk.Frame(root, bg="#f4f8ff")
    navigation_frame.pack(pady=10)

    global page_label
    page_label = tk.Label(root, text="", font=("FontA", 12), bg="#f4f8ff")
    page_label.pack()

    file_path = r"D:\Comproject\FAST+\Attendance"
    files = os.listdir(file_path)

    global current_page
    current_page = 1
    files_per_page = 5
    show_files(files, current_page, files_per_page, file_path)

    
###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please FAST+ Team for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("570x200")
    icon_path = r"D:\Comproject\FAST+\Images\fasticongui.ico"
    master.iconbitmap(icon_path)
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=(FontA, 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=(FontA, 12, ' bold '),show='*')
    old.place(x=230,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=(FontA, 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=(FontA, 12, ' bold '),show='*')
    new.place(x=230, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=(FontA, 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=(FontA, 12, ' bold '),show='*')
    nnew.place(x=230, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=(FontA, 10, ' bold '))
    cancel.place(x=290, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=(FontA, 10, ' bold '))
    save1.place(x=18, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(camera)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(camera)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    attendance = []  # Initialize empty list for attendance records
    recognized_ids = set()  # Initialize a set to keep track of recognized IDs

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                if serial not in recognized_ids:  # Check if the face ID is not already recognized
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance.append([str(ID), '', bb, '', str(date), '', str(timeStamp)])  # Append to attendance list
                    recognized_ids.add(serial)  # Add the recognized ID to the set
                    cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)  # Display the name inside the rectangle
                    cv2.putText(im, "Record ready", (x, y - 20), font, 0.8, (0, 255, 0), 2)  # Display "Record ready" for new faces
                else:
                    cv2.putText(im, "Attendance Check", (x, y - 20), font, 0.8, (0, 255, 0), 2)  # Display "Recorded" for already recognized faces

            else:
                Id = 'Come Closer'
                bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)  # Display 'Unknown' inside the rectangle
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
        if (cv2.waitKey(1) == ord('f')):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            for record in attendance:
                writer.writerow(record)  # Write each attendance record
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            for record in attendance:
                writer.writerow(record)  # Write each attendance record
        csvFile1.close()

    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()



######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1920x1080")
window.resizable(True,True)
window.title("FAST+")
window.configure(background='#f4f8ff')
icon_path = r"D:\Comproject\FAST+\Images\fasticongui.ico"
window.iconbitmap(icon_path)

frame1 = tk.Frame(window, bg=BoxC)
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg=BoxC)
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Facial Attendance and Student Tracking" ,fg="#4868a8",bg="#f4f8ff" ,width=55 ,height=1,font=(FontA, 29, ' bold '))
message3.place(x=150, y=20)

message4 = tk.Label(window, text="Standby Version FAST+ V.1.7.0 DV.7.0" ,fg="#4868a8",bg="#f4f8ff" ,width=55 ,height=1,font=(FontA, 10, ' bold '))
message4.place(x=1470, y=140)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.54, rely=0.07, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.38, rely=0.07, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="#4868a8",bg="#f4f8ff" ,width=55 ,height=1,font=(FontA, 20, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="#4868a8",bg="#f4f8ff" ,width=55 ,height=1,font=(FontA, 20, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#dce5f4" ,font=(FontA, 17, ' bold ') )
head2.grid(row=0,column=0)
head2.place(x=0,y=0, width=750)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#dce5f4" ,font=(FontA, 17, ' bold ') )
head1.place(x=0,y=0, width=750)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg=BoxC ,font=(FontA, 17, ' bold '), )
lbl.place(x=150, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=(FontA, 15, ' bold '))
txt.place(x=60, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg=BoxC ,font=(FontA, 17, ' bold '))
lbl2.place(x=150, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=(FontA, 15, ' bold ')  )
txt2.place(x=60, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg=BoxC ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=(FontA, 15, ' bold '))
message1.place(x=25, y=230)

message = tk.Label(frame2, text="" ,bg=BoxC ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=(FontA, 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg=BoxC  ,height=1 ,font=(FontA, 17, ' bold '))
lbl3.place(x=180, y=115)

#images
photo1 = tk.PhotoImage(file="D:/Comproject/FAST/Images/FASTLOGO1.png")
resized_photo1 = photo1.subsample(3, 3)
image_label1 = tk.Label(window, image=resized_photo1)
image_label1.place(x=1600, y=20)
image_label1.config(borderwidth=0, highlightthickness=0)
image_label1.lift()  # Bring the label to the front

# Load the second image
photo2 = tk.PhotoImage(file="D:\Comproject\FAST\Images\kanlayanee.png")
resized_photo2 = photo2.subsample(6, 6)
image_label2 = tk.Label(window, image=resized_photo2)
image_label2.place(x=5, y=5)
image_label2.config(borderwidth=0, highlightthickness=0)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

menubar = tk.Menu(window, relief='ridge')

# Create the 'Help' cascade menu and add commands to it
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label='Change Password', command=change_pass)
help_menu.add_command(label='Our Website', command=ourwebsite)
help_menu.add_command(label='Contact Us', command=contact)
help_menu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=(FontA, 29, 'bold'), menu=help_menu)

# Create the 'Test' cascade menu and add commands from 'Help' cascade to it



Attendance_menu = tk.Menu(menubar, tearoff=0)
Attendance_menu.add_command(label='Today Attendance ', command=today_attendance)
Attendance_menu.add_command(label='Student Attendance ', command=studentid_attendance)
Attendance_menu.add_command(label='View Attendance History', command=other)
menubar.add_cascade(label='Attendance', font=(FontA, 29, 'bold'), menu=Attendance_menu)

Student_menu = tk.Menu(menubar, tearoff=0)
Student_menu.add_command(label='Student Detials  ', command=student_detail)
menubar.add_cascade(label='Student', font=(FontA, 29, 'bold'), menu=Student_menu)

# schedule

Schedule_menu = tk.Menu(menubar, tearoff=0)
Schedule_menu.add_command(label='Set Attendance Times  ', command=set_attendance_times)
menubar.add_cascade(label='Schedule', font=(FontA, 29, 'bold'), menu=Schedule_menu)

window.config(menu=menubar)

################## TREEVIEW ATTENDANCE TABLE ####################
widthvolume=190

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=widthvolume)
tv.column('name',width=widthvolume)
tv.column('date',width=widthvolume)
tv.column('time',width=widthvolume)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

##
clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg=TextC  ,bg=ButtonC  ,width=11 ,activebackground = "white" ,font=(FontA, 11, ' bold '))
clearButton.place(x=450, y=86)
##
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg=TextC  ,bg=ButtonC  ,width=11 , activebackground = "white" ,font=(FontA, 11, ' bold '))
clearButton2.place(x=450, y=172)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg=ButtonC  ,width=34  ,height=1, activebackground = "white" ,font=(FontA, 15, ' bold '))
takeImg.place(x=100, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg=ButtonC  ,width=34  ,height=1, activebackground = "white" ,font=(FontA, 15, ' bold '))
trainImg.place(x=100, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg=TextC  ,bg=ButtonC  ,width=35  ,height=1, activebackground = "white" ,font=(FontA, 15, ' bold '))
trackImg.place(x=100,y=50)
quitWindow = tk.Button(frame1, text="Exit", command=window.destroy  ,fg=TextC  ,bg=ButtonC  ,width=35 ,height=1, activebackground = "white" ,font=(FontA, 15, ' bold '))
quitWindow.place(x=100, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
### © 2023 All right reserved to FAST+ Team ###
## Lead Programmer Thanakorn Morasilp ##
## Support Programmer Sirapath Rattanarat ##
## Graphic Designer Eric Holmegaard ##
