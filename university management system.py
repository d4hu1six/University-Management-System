import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Theme Colors
PRIMARY_COLOR = "#C8102E"  # NIET Red
BG_COLOR = "#FFFFFF"       # White

# --- Data Storage ---
# In-memory "database" dictionaries to store students, faculty, courses, and hostel info
database = {
    'students': {},  # key: student ID, value: dict with student details
    'faculty': {},   # key: faculty ID, value: dict with faculty details
    'courses': {     # predefined courses with fields: name, enrolled students list, assigned faculty, prerequisites
        'BTECH':   {'name': 'B.Tech',      'students': [], 'faculty': None, 'prereq': []},
        'BPHARMA': {'name': 'B.Pharmacy',  'students': [], 'faculty': None, 'prereq': []},
        'MBA':     {'name': 'MBA',         'students': [], 'faculty': None, 'prereq': []},
        'BUSINESS':{'name': 'Business',    'students': [], 'faculty': None, 'prereq': []},
        'BCA':     {'name': 'BCA',         'students': [], 'faculty': None, 'prereq': []},
        'BCOM':    {'name': 'B.Com',       'students': [], 'faculty': None, 'prereq': []},
    },
    'hostel': {}  # key: student ID, value: dict with hostel_name and room_no
}

# Mapping from course ID to fee amount
course_fee_map = {
    'BTECH':   180000,
    'BPHARMA': 120000,
    'MBA':     300000,
    'BUSINESS':160000,
    'BCOM':    125000,
    'BCA':     130000,
}

# --- Main Functions ---

def launch_main_app():
    """
    Called after successful login.
    Destroys the login window and builds the main application GUI.
    """
    login_win.destroy()  # close login window
    build_main_gui()     # open main GUI

def build_main_gui():
    """
    Builds and displays the main University Management System GUI.
    Contains tabs for adding/viewing students and faculty, enrolling students,
    hostel details, enquiries, etc.
    """
    root = tk.Tk()
    root.title("University Management System")
    # Reduced window size for cleaner display
    root.geometry("720x400")
    # Set root background color to PRIMARY_COLOR so that any blank space shows red
    root.configure(bg=PRIMARY_COLOR)

    # ---------- STYLING ----------
    style = ttk.Style()
    style.theme_use("clam")  # use a clean theme

    # Style for Notebook (tab container)
    style.configure("TNotebook", background=BG_COLOR)
    style.configure("TNotebook.Tab",
                    background=PRIMARY_COLOR,
                    foreground="white",
                    padding=(8, 4))
    style.map("TNotebook.Tab",
              background=[("selected", PRIMARY_COLOR)],
              foreground=[("selected", "white")])

    # Style for Buttons
    style.configure("TButton",
                    background=PRIMARY_COLOR,
                    foreground="white",
                    font=("Arial", 9, "bold"))
    # Change background slightly when button is active
    style.map("TButton",
              background=[("active", "#a50f24")])

    # Style for Labels
    style.configure("TLabel",
                    background=BG_COLOR,
                    foreground="black")
    # Style for LabelFrame
    style.configure("TLabelFrame",
                    background=BG_COLOR,
                    borderwidth=2,
                    relief="groove")
    style.configure("TLabelFrame.Label",
                    font=("Arial", 11, "bold"),
                    foreground=PRIMARY_COLOR)

    # ---------- HEADER SECTION ----------
    header_frame = tk.Frame(root, bg=BG_COLOR)
    header_frame.pack(pady=8, fill='x', padx=10)

    # Left: NIET title
    tk.Label(header_frame,
             text="NIET",
             font=("Arial", 28, "bold"),
             fg=PRIMARY_COLOR,
             bg=BG_COLOR).pack(side='left')

    # Left: Subtitle
    tk.Label(header_frame,
             text="UNIVERSITY MANAGEMENT SYSTEM",
             font=("Arial", 14, "bold"),
             fg=PRIMARY_COLOR,
             bg=BG_COLOR).pack(side='left', padx=8)

    # Right: Info frame (contact, slogan)
    info_frame = tk.Frame(header_frame, bg=BG_COLOR)
    info_frame.pack(side='right')
    tk.Label(info_frame,
             text="GET FUTURE READY!",
             font=("Arial", 12, "bold"),
             fg=PRIMARY_COLOR,
             bg=BG_COLOR).pack()
    tk.Label(info_frame,
             text="Contact: +91 4445556667",
             font=("Arial", 8),
             fg="black",
             bg=BG_COLOR).pack()

    # Also place a bold "GET FUTURE READY!" label on top-right corner of root
    root.update_idletasks()  # ensure geometry is calculated
    tk.Label(root,
             text="GET FUTURE READY!",
             font=("Arial", 16, "bold"),
             fg="white",
             bg=PRIMARY_COLOR).place(relx=1.0, rely=0.0,
                                     anchor='ne', x=-10, y=10)

    # Separator line below header
    tk.Frame(root, bg=PRIMARY_COLOR, height=2).pack(fill='x', padx=10)

    # ---------- CONTENT FRAME ----------
    content_frame = tk.Frame(root, bg=BG_COLOR)
    content_frame.pack(expand=True, fill='both', padx=10, pady=5)

    # ---------- TAB CONTROL ----------
    tab_control = ttk.Notebook(content_frame)

    def make_tab(title):
        """
        Helper to create a new tab with given title.
        Returns the frame for placing widgets in that tab.
        """
        frame = tk.Frame(tab_control, bg=BG_COLOR)
        tab_control.add(frame, text=title)
        return frame

    # ----- Add Student Tab -----
    student_tab = make_tab("Add Student")
    student_frame = ttk.LabelFrame(student_tab, text="Add New Student")
    student_frame.pack(padx=5, pady=5, fill='x')

    # Variables for student input fields
    student_id = tk.StringVar()
    student_name = tk.StringVar()
    student_email = tk.StringVar()
    student_phone = tk.StringVar()
    student_course = tk.StringVar()
    student_fees = tk.StringVar()

    # Labels and associated StringVar list
    labels = ["Student ID", "Name", "Email", "Phone", "Course", "Fees (INR)"]
    vars = [student_id, student_name, student_email, student_phone, student_course, student_fees]

    # Loop to create label+entry/combobox for each field
    for i, (lbl, var) in enumerate(zip(labels, vars)):
        ttk.Label(student_frame, text=lbl + ":").grid(row=i, column=0, sticky='w', padx=8, pady=4)
        if lbl == "Course":
            # Course selection via Combobox; values from course_fee_map keys
            cb = ttk.Combobox(student_frame,
                              textvariable=var,
                              values=list(course_fee_map.keys()),
                              state="readonly",
                              width=15)
            cb.grid(row=i, column=1, padx=8, pady=4)
            # When course selected, update fee field
            def on_course(e=None):
                fee = course_fee_map.get(student_course.get(), 0)
                # Format fee with commas
                student_fees.set(f"{fee:,}")
            cb.bind("<<ComboboxSelected>>", on_course)
        elif lbl == "Fees (INR)":
            # Read-only entry for fees
            ttk.Entry(student_frame,
                      textvariable=var,
                      state="readonly",
                      width=17).grid(row=i, column=1, padx=8, pady=4)
        else:
            # Regular entry for other fields
            ttk.Entry(student_frame,
                      textvariable=var,
                      width=17).grid(row=i, column=1, padx=8, pady=4)

    def save_student():
        """
        Handler for "Add Student" button.
        Validates inputs, checks duplicate ID, then saves student info and updates database.
        """
        sid = student_id.get().strip()
        name = student_name.get().strip()
        email = student_email.get().strip()
        phone = student_phone.get().strip()
        course = student_course.get()
        # Check all fields filled
        if sid and name and email and phone and course:
            # Check if student ID already exists
            if sid in database['students']:
                messagebox.showerror("Error", "Student ID already exists.")
                return
            # Save student data
            database['students'][sid] = {
                'name': name,
                'email': email,
                'phone': phone,
                'courses': [course]
            }
            # Add student to course's student list
            database['courses'][course]['students'].append(sid)
            messagebox.showinfo("Success", f"Student {name} added.")
            # Clear input fields
            for v in vars:
                v.set("")
        else:
            messagebox.showerror("Error", "Fill all fields!")

    # Button to add student
    ttk.Button(student_frame,
               text="Add Student",
               command=save_student).grid(row=6, columnspan=2, pady=6)

    # ----- Add Faculty Tab -----
    faculty_tab = make_tab("Add Faculty")
    faculty_frame = ttk.LabelFrame(faculty_tab, text="Add New Faculty")
    faculty_frame.pack(padx=5, pady=5, fill='x')

    # Variables for faculty input fields
    faculty_id = tk.StringVar()
    faculty_name = tk.StringVar()

    # Faculty ID label+entry
    ttk.Label(faculty_frame, text="Faculty ID:").grid(row=0, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(faculty_frame, textvariable=faculty_id, width=17).grid(row=0, column=1, padx=8, pady=4)

    # Faculty Name label+entry
    ttk.Label(faculty_frame, text="Name:").grid(row=1, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(faculty_frame, textvariable=faculty_name, width=17).grid(row=1, column=1, padx=8, pady=4)

    def save_faculty():
        """
        Handler for "Add Faculty" button.
        Validates inputs, checks duplicate ID, then saves faculty info.
        """
        fid = faculty_id.get().strip()
        name = faculty_name.get().strip()
        if fid and name:
            # Check if faculty ID exists
            if fid in database['faculty']:
                messagebox.showerror("Error", "Faculty ID exists.")
                return
            # Save faculty data
            database['faculty'][fid] = {'name': name, 'courses': []}
            messagebox.showinfo("Success", "Faculty added.")
            # Clear fields
            faculty_id.set("")
            faculty_name.set("")
        else:
            messagebox.showerror("Error", "Fill all fields!")

    # Button to add faculty
    ttk.Button(faculty_frame,
               text="Add Faculty",
               command=save_faculty).grid(row=2, columnspan=2, pady=6)

    # ----- Enroll Student Tab -----
    enroll_tab = make_tab("Enroll Student")
    enroll_frame = ttk.LabelFrame(enroll_tab, text="Enroll Student in Course")
    enroll_frame.pack(padx=5, pady=5, fill='x')

    # Variables for enrollment
    enroll_student_id = tk.StringVar()
    enroll_course_id = tk.StringVar()

    # Student ID label+entry
    ttk.Label(enroll_frame, text="Student ID:").grid(row=0, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(enroll_frame, textvariable=enroll_student_id, width=17).grid(row=0, column=1, padx=8, pady=4)
    # Course ID label+entry
    ttk.Label(enroll_frame, text="Course ID:").grid(row=1, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(enroll_frame, textvariable=enroll_course_id, width=17).grid(row=1, column=1, padx=8, pady=4)

    def enroll_student():
        """
        Handler for "Enroll" button.
        Checks if student and course IDs exist; if not already enrolled, adds enrollment.
        """
        sid = enroll_student_id.get().strip()
        cid = enroll_course_id.get().strip()
        # Validate existence
        if sid in database['students'] and cid in database['courses']:
            # Check if already enrolled
            if cid not in database['students'][sid]['courses']:
                # Add course to student's list
                database['students'][sid]['courses'].append(cid)
                # Add student to course's list
                database['courses'][cid]['students'].append(sid)
                messagebox.showinfo("Success", f"Enrolled {sid} in {cid}.")
                # Clear fields
                enroll_student_id.set("")
                enroll_course_id.set("")
            else:
                messagebox.showinfo("Info", "Already enrolled.")
        else:
            messagebox.showerror("Error", "Invalid IDs.")

    # Button to enroll student
    ttk.Button(enroll_frame,
               text="Enroll",
               command=enroll_student).grid(row=2, columnspan=2, pady=6)

    # ----- View Student Details Tab -----
    details_tab = make_tab("View Student Details")
    details_frame = ttk.LabelFrame(details_tab, text="Student Details")
    details_frame.pack(padx=5, pady=5, fill='x')

    # Variable for student ID to view
    detail_student_id = tk.StringVar()

    # Label+entry for student ID
    ttk.Label(details_frame, text="Student ID:").grid(row=0, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(details_frame, textvariable=detail_student_id, width=17).grid(row=0, column=1, padx=8, pady=4)

    def show_student_details():
        """
        Handler for "Show Details" button.
        Retrieves and displays student info in a messagebox, including courses and hostel if any.
        """
        sid = detail_student_id.get().strip()
        if sid in database['students']:
            s = database['students'][sid]
            # Build info string
            courses = ', '.join(s['courses'])
            info = (
                f"ID: {sid}\n"
                f"Name: {s['name']}\n"
                f"Email: {s['email']}\n"
                f"Phone: {s['phone']}\n"
                f"Courses: {courses}"
            )
            # If hostel info exists for this student, append it
            if sid in database['hostel']:
                h = database['hostel'][sid]
                info += f"\nHostel: {h.get('hostel_name')} Room: {h.get('room_no')}"
            # Show info
            messagebox.showinfo("Details", info)
        else:
            messagebox.showerror("Error", "Not found.")

    # Button to show student details
    ttk.Button(details_frame,
               text="Show Details",
               command=show_student_details).grid(row=1, columnspan=2, pady=6)

    # ----- Enquiry Tab -----
    enquiry_tab = make_tab("Enquiry")
    enquiry_frame = ttk.LabelFrame(enquiry_tab, text="Submit Enquiry")
    enquiry_frame.pack(padx=5, pady=5, fill='x')

    # Variables and Text widget for enquiry
    enquiry_name = tk.StringVar()
    enquiry_email = tk.StringVar()

    # Name label+entry
    ttk.Label(enquiry_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(enquiry_frame, textvariable=enquiry_name, width=17).grid(row=0, column=1, padx=8, pady=4)
    # Email label+entry
    ttk.Label(enquiry_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(enquiry_frame, textvariable=enquiry_email, width=17).grid(row=1, column=1, padx=8, pady=4)
    # Query label+text area
    ttk.Label(enquiry_frame, text="Query:").grid(row=2, column=0, sticky='nw', padx=8, pady=4)
    enquiry_query = tk.Text(enquiry_frame, width=30, height=4)
    enquiry_query.grid(row=2, column=1, padx=8, pady=4)

    def submit_enquiry():
        """
        Handler for "Submit" button in Enquiry tab.
        Validates fields and shows confirmation. No storage in this version.
        """
        name = enquiry_name.get().strip()
        email = enquiry_email.get().strip()
        query = enquiry_query.get("1.0", tk.END).strip()
        if name and email and query:
            messagebox.showinfo("Received", "Enquiry submitted.")
            # Clear fields after submission
            enquiry_name.set("")
            enquiry_email.set("")
            enquiry_query.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Fill all fields.")

    # Button to submit enquiry
    ttk.Button(enquiry_frame,
               text="Submit",
               command=submit_enquiry).grid(row=3, columnspan=2, pady=6)

    # ----- Hostel Details Tab -----
    hostel_tab = make_tab("Hostel Details")
    hostel_frame = ttk.LabelFrame(hostel_tab, text="Hostel Info")
    hostel_frame.pack(padx=5, pady=5, fill='x')

    # Variables for hostel assignment
    hostel_student_id = tk.StringVar()
    hostel_name_var = tk.StringVar()
    room_no_var = tk.StringVar()

    # Student ID label+entry
    ttk.Label(hostel_frame, text="Student ID:").grid(row=0, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(hostel_frame, textvariable=hostel_student_id, width=17).grid(row=0, column=1, padx=8, pady=4)
    # Hostel Name label+entry
    ttk.Label(hostel_frame, text="Hostel Name:").grid(row=1, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(hostel_frame, textvariable=hostel_name_var, width=17).grid(row=1, column=1, padx=8, pady=4)
    # Room No label+entry
    ttk.Label(hostel_frame, text="Room No:").grid(row=2, column=0, sticky='w', padx=8, pady=4)
    ttk.Entry(hostel_frame, textvariable=room_no_var, width=17).grid(row=2, column=1, padx=8, pady=4)

    def save_hostel():
        """
        Handler for "Save" button in Hostel Details tab.
        Validates student exists, then saves hostel info.
        """
        sid = hostel_student_id.get().strip()
        hname = hostel_name_var.get().strip()
        rno = room_no_var.get().strip()
        if sid and hname and rno:
            # Check student exists
            if sid not in database['students']:
                messagebox.showerror("Error", "Invalid Student ID.")
                return
            # Save hostel info
            database['hostel'][sid] = {'hostel_name': hname, 'room_no': rno}
            messagebox.showinfo("Saved", "Hostel details saved.")
            # Clear fields
            hostel_student_id.set("")
            hostel_name_var.set("")
            room_no_var.set("")
        else:
            messagebox.showerror("Error", "Fill all fields.")

    # Button to save hostel info
    ttk.Button(hostel_frame,
               text="Save",
               command=save_hostel).grid(row=3, columnspan=2, pady=6)

    # ----- View Faculty Tab -----
    view_faculty_tab = make_tab("View Faculty")
    vf_frame = ttk.LabelFrame(view_faculty_tab, text="Faculty List")
    vf_frame.pack(padx=5, pady=5, fill='both', expand=True)

    # Listbox to display faculty entries
    faculty_listbox = tk.Listbox(vf_frame)
    faculty_listbox.pack(fill='both', expand=True, padx=8, pady=4)

    def refresh_faculty_list():
        """
        Clears and repopulates the faculty listbox with current faculty data.
        """
        faculty_listbox.delete(0, tk.END)
        for fid, data in database['faculty'].items():
            faculty_listbox.insert(tk.END, f"ID: {fid} | Name: {data['name']}")

    # Button to refresh faculty list display
    ttk.Button(vf_frame,
               text="Refresh",
               command=refresh_faculty_list).pack(pady=5)

    # ----- View Students Tab -----
    view_students_tab = make_tab("View Students")
    vs_frame = ttk.LabelFrame(view_students_tab, text="Student List")
    vs_frame.pack(padx=5, pady=5, fill='both', expand=True)

    # Listbox to display student entries
    student_listbox = tk.Listbox(vs_frame)
    student_listbox.pack(fill='both', expand=True, padx=8, pady=4)

    def refresh_student_list():
        """
        Clears and repopulates the student listbox with current student data.
        """
        student_listbox.delete(0, tk.END)
        for sid, data in database['students'].items():
            student_listbox.insert(tk.END, f"ID: {sid} | Name: {data['name']}")

    # Button to refresh student list display
    ttk.Button(vs_frame,
               text="Refresh",
               command=refresh_student_list).pack(pady=5)

    # Pack the tab control into content frame
    tab_control.pack(expand=True, fill='both')

    # ---------- FOOTER ----------
    footer = tk.Frame(root, bg=BG_COLOR)
    footer.pack(fill='x', padx=10, pady=4)
    # Footer label on right
    tk.Label(footer,
             text="© NIET University Management System",
             bg=BG_COLOR,
             fg=PRIMARY_COLOR,
             font=("Arial", 8)).pack(side='right')
    # Logout button on left: destroys main window and re-shows login
    tk.Button(footer,
              text="Logout",
              command=lambda: [root.destroy(), show_login()],
              bg=PRIMARY_COLOR,
              fg='white',
              font=("Arial", 9, "bold")).pack(side='left')

    # Start the Tkinter main loop for the main app window
    root.mainloop()

# --- Login Window ---
def show_login():
    """
    Builds and displays the login window.
    On successful login (ID "123", password "admin"), launches main app.
    """
    global login_win
    login_win = tk.Tk()
    login_win.title("Login")
    # Slightly smaller login window
    login_win.geometry("280x180")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)

    # Label and entry for Login ID
    tk.Label(login_win,
             text="Login ID:",
             bg=BG_COLOR,
             fg=PRIMARY_COLOR,
             font=("Arial", 10, "bold")).pack(pady=5)
    login_id_entry = tk.Entry(login_win)
    login_id_entry.pack()

    # Label and entry for Password
    tk.Label(login_win,
             text="Password:",
             bg=BG_COLOR,
             fg=PRIMARY_COLOR,
             font=("Arial", 10, "bold")).pack(pady=5)
    login_pass_entry = tk.Entry(login_win, show='*')
    login_pass_entry.pack()

    def check_login():
        """
        Handler for Login button.
        Checks credentials and either launches main app or shows error.
        """
        uid = login_id_entry.get()
        pwd = login_pass_entry.get()
        # Only valid combination: ID "123", password "admin"
        if uid == "123" and pwd == "admin":
            launch_main_app()
        else:
            messagebox.showerror("Login Failed", "Incorrect ID or Password")

    # Login button
    tk.Button(login_win,
              text="Login",
              command=check_login,
              bg=PRIMARY_COLOR,
              fg='white').pack(pady=10)

    # Start Tkinter loop for login window
    login_win.mainloop()

# Start the application by showing login window first
show_login()