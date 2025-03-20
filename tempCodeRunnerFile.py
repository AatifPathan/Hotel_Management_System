import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("850x500")
        
        # Initialize Database
        self.conn = sqlite3.connect("hotel_management.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Create Heading
        self.heading = tk.Label(self.root, text="HOTEL MANAGEMENT SYSTEM", font=("Arial", 16, "bold"))
        self.heading.pack(pady=10)

        # Create Main Buttons
        self.create_main_buttons()
        # At the end of your __init__ method, add the following code
        self.initials_label = tk.Label(self.root, text="@ap", font=("Arial", 10, "italic"))
        self.initials_label.pack(side="bottom", pady=10)

    def create_tables(self):
        # Creating the Guest table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Guest (
                                guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                age INTEGER,
                                gender TEXT,
                                phone_no TEXT,
                                room_type TEXT,
                                room_no TEXT,
                                check_in TEXT,
                                check_out TEXT)
                            ''')

        # Creating the Department table with ID, Name, Phone No, and Head
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Department (
                                dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                dept_name TEXT,
                                dept_phone_no TEXT,
                                dept_head TEXT)
                            ''')

        # Creating the Staff table with Staff ID, Name, Gender, Position, Phone No, and Salary
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Staff (
                                staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                staff_name TEXT,
                                staff_gender TEXT,
                                staff_position TEXT,
                                staff_phone_no TEXT,
                                staff_salary REAL)
                            ''')
        self.conn.commit()

    def create_main_buttons(self):
        self.clear_frame()
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        management_btn = ttk.Button(btn_frame, text="Management", command=self.show_management)
        management_btn.grid(row=0, column=0, padx=20, pady=10)

        guest_btn = ttk.Button(btn_frame, text="Guest", command=self.show_guest)
        guest_btn.grid(row=0, column=1, padx=20, pady=10)

    def show_management(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.create_main_buttons)
        back_btn.pack(anchor='w', padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Room Reservation", command=self.show_room_reservation).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Manage Department", command=self.show_manage_department).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(btn_frame, text="Manage Staff", command=self.show_manage_staff).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Guest Information", command=self.show_guest_information).grid(row=1, column=1, padx=10, pady=5)

    def show_manage_staff(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_management)
        back_btn.pack(anchor='w', padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Add Staff", command=self.show_add_staff_form).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="View Staff", command=self.show_staff).grid(row=0, column=1, padx=10, pady=5)

    def show_add_staff_form(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_manage_staff)
        back_btn.pack(anchor='w', padx=10, pady=5)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        # Staff name input
        ttk.Label(form_frame, text="Staff Name:").grid(row=0, column=0, padx=5, pady=5)
        staff_name_entry = ttk.Entry(form_frame)
        staff_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Staff gender input
        ttk.Label(form_frame, text="Staff Gender:").grid(row=1, column=0, padx=5, pady=5)
        staff_gender_var = tk.StringVar()
        gender_male = ttk.Radiobutton(form_frame, text="Male", variable=staff_gender_var, value="Male")
        gender_female = ttk.Radiobutton(form_frame, text="Female", variable=staff_gender_var, value="Female")
        gender_male.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        gender_female.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # Staff position input
        ttk.Label(form_frame, text="Staff Position:").grid(row=2, column=0, padx=5, pady=5)
        staff_position_entry = ttk.Entry(form_frame)
        staff_position_entry.grid(row=2, column=1, padx=5, pady=5)

        # Staff phone number input
        ttk.Label(form_frame, text="Staff Phone No:").grid(row=3, column=0, padx=5, pady=5)
        staff_phone_entry = ttk.Entry(form_frame)
        staff_phone_entry.grid(row=3, column=1, padx=5, pady=5)

        # Staff salary input
        ttk.Label(form_frame, text="Staff Salary:").grid(row=4, column=0, padx=5, pady=5)
        staff_salary_entry = ttk.Entry(form_frame)
        staff_salary_entry.grid(row=4, column=1, padx=5, pady=5)

        # Submit button to add staff
        ttk.Button(form_frame, text="Submit", command=lambda: self.add_staff(
            staff_name_entry.get(), staff_gender_var.get(), staff_position_entry.get(),
            staff_phone_entry.get(), staff_salary_entry.get())).grid(row=5, column=0, columnspan=2, pady=10)

    def add_staff(self, name, gender, position, phone, salary):
        if not name or not gender or not position or not phone or not salary:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid salary")
            return

        # Insert staff into the database
        self.cursor.execute("INSERT INTO Staff (staff_name, staff_gender, staff_position, staff_phone_no, staff_salary) VALUES (?, ?, ?, ?, ?)", 
                            (name, gender, position, phone, salary))
        self.conn.commit()
        messagebox.showinfo("Success", "Staff added successfully!")

    def show_staff(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_manage_staff)
        back_btn.pack(anchor='w', padx=10, pady=5)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20, fill="both", expand=True)

        # Staff table columns
        columns = ("Staff ID", "Staff Name", "Gender", "Position", "Phone No", "Salary")

        # Adding Scrollbars
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

        staff_table = ttk.Treeview(
            table_frame, columns=columns, show="headings", 
            xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set
        )

        tree_scroll_x.config(command=staff_table.xview)
        tree_scroll_y.config(command=staff_table.yview)

        for col in columns:
            staff_table.heading(col, text=col)
            staff_table.column(col, width=100)

        staff_table.grid(row=0, column=0, sticky="nsew")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Fetch all staff from the database
        self.cursor.execute("SELECT * FROM Staff")
        for row in self.cursor.fetchall():
            staff_table.insert("", "end", values=row)
    def show_manage_department(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_management)
        back_btn.pack(anchor='w', padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Add Department", command=self.show_add_department_form).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="View Departments", command=self.show_departments).grid(row=0, column=1, padx=10, pady=5)

    def show_add_department_form(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_manage_department)
        back_btn.pack(anchor='w', padx=10, pady=5)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        # Department name input
        ttk.Label(form_frame, text="Department Name:").grid(row=0, column=0, padx=5, pady=5)
        dept_name_entry = ttk.Entry(form_frame)
        dept_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Department phone number input
        ttk.Label(form_frame, text="Department Phone No:").grid(row=1, column=0, padx=5, pady=5)
        dept_phone_no_entry = ttk.Entry(form_frame)
        dept_phone_no_entry.grid(row=1, column=1, padx=5, pady=5)

        # Department head input
        ttk.Label(form_frame, text="Department Head:").grid(row=2, column=0, padx=5, pady=5)
        dept_head_entry = ttk.Entry(form_frame)
        dept_head_entry.grid(row=2, column=1, padx=5, pady=5)

        # Submit button to add the department
        ttk.Button(form_frame, text="Submit", command=lambda: self.add_department(
            dept_name_entry.get(), dept_phone_no_entry.get(), dept_head_entry.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def add_department(self, dept_name, dept_phone_no, dept_head):
        if not dept_name or not dept_phone_no or not dept_head:
            messagebox.showerror("Error", "Please fill all fields")
            return

        # Insert department into the database
        self.cursor.execute("INSERT INTO Department (dept_name, dept_phone_no, dept_head) VALUES (?, ?, ?)", 
                            (dept_name, dept_phone_no, dept_head))
        self.conn.commit()
        messagebox.showinfo("Success", "Department added successfully!")

    def show_departments(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_manage_department)
        back_btn.pack(anchor='w', padx=10, pady=5)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20, fill="both", expand=True)

        # Department table columns
        columns = ("Dept ID", "Dept Name", "Dept Phone No", "Dept Head")

        # Adding Scrollbars
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

        department_table = ttk.Treeview(
            table_frame, columns=columns, show="headings", 
            xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set
        )

        tree_scroll_x.config(command=department_table.xview)
        tree_scroll_y.config(command=department_table.yview)

        for col in columns:
            department_table.heading(col, text=col)
            department_table.column(col, width=100)

        department_table.grid(row=0, column=0, sticky="nsew")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Fetch all departments from the database
        self.cursor.execute("SELECT * FROM Department")
        for row in self.cursor.fetchall():
            department_table.insert("", "end", values=row)
    def show_guest(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.create_main_buttons)
        back_btn.pack(anchor='w', padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Book Your Reservation", command=self.show_reservation_form).grid(row=0, column=0, padx=10, pady=5)

    def show_reservation_form(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_guest)
        back_btn.pack(anchor='w', padx=10, pady=5)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        age_entry = ttk.Entry(form_frame)
        age_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
        gender_var = tk.StringVar()
        gender_male = ttk.Radiobutton(form_frame, text="Male", variable=gender_var, value="Male")
        gender_female = ttk.Radiobutton(form_frame, text="Female", variable=gender_var, value="Female")
        gender_male.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        gender_female.grid(row=2, column=2, padx=5, pady=5, sticky='w')

        ttk.Label(form_frame, text="Phone No:").grid(row=3, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(form_frame)
        phone_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Room Type:").grid(row=4, column=0, padx=5, pady=5)
        room_var = tk.StringVar()
        room_type = ttk.Combobox(form_frame, textvariable=room_var, values=["Normal Room", "Exquisite Room"])
        room_type.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Check-in Date:").grid(row=5, column=0, padx=5, pady=5)
        check_in_entry = DateEntry(form_frame, date_pattern='dd-mm-yyyy')
        check_in_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Check-out Date:").grid(row=6, column=0, padx=5, pady=5)
        check_out_entry = DateEntry(form_frame, date_pattern='dd-mm-yyyy')
        check_out_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Submit", command=lambda: self.book_room(
            name_entry.get(), age_entry.get(), gender_var.get(), phone_entry.get(), 
            room_var.get(), check_in_entry.get(), check_out_entry.get())).grid(row=7, column=0, columnspan=2, pady=10)

    def generate_room_number(self, room_type):
        self.cursor.execute("SELECT COUNT(*) FROM Guest WHERE room_type=?", (room_type,))
        count = self.cursor.fetchone()[0]
        return f"{'N' if room_type == 'Normal Room' else 'E'}{count + 1}"

    def book_room(self, name, age, gender, phone, room_type, check_in, check_out):
        if not name or not age or not gender or not phone or not room_type or not check_in or not check_out:
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not age.isdigit() or int(age) < 18:
            messagebox.showerror("Error", "Age must be a number greater than 18")
            return
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return

        room_no = self.generate_room_number(room_type)

        self.cursor.execute("INSERT INTO Guest (name, age, gender, phone_no, room_type, room_no, check_in, check_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                            (name, age, gender, phone, room_type, room_no, check_in, check_out))
        self.conn.commit()
        messagebox.showinfo("Success", f"Room Reserved Successfully! Room No: {room_no}")

    def show_room_reservation(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_management)
        back_btn.pack(anchor='w', padx=10, pady=5)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20, fill="both", expand=True)

        columns = ("Guest ID", "Name", "Age", "Gender", "Phone", "Room Type", "Room No", "Check-in", "Check-out")

        # Adding Scrollbars
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

        self.guest_table = ttk.Treeview(
            table_frame, columns=columns, show="headings", 
            xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set
        )

        tree_scroll_x.config(command=self.guest_table.xview)
        tree_scroll_y.config(command=self.guest_table.yview)

        for col in columns:
            self.guest_table.heading(col, text=col)
            self.guest_table.column(col, width=100)

        self.guest_table.grid(row=0, column=0, sticky="nsew")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.cursor.execute("SELECT * FROM Guest")
        for row in self.cursor.fetchall():
            self.guest_table.insert("", "end", values=row)

    def show_guest_information(self):
        self.clear_frame()

        back_btn = ttk.Button(self.root, text="← Back", command=self.show_management)
        back_btn.pack(anchor='w', padx=10, pady=5)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=20, fill="both", expand=True)

        # Columns to display: Name, Age, Gender, Phone
        columns = ("Name", "Age", "Gender", "Phone")

        # Adding Scrollbars
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

        guest_table = ttk.Treeview(
            table_frame, columns=columns, show="headings", 
            xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set
        )

        tree_scroll_x.config(command=guest_table.xview)
        tree_scroll_y.config(command=guest_table.yview)

        # Set up column headings
        for col in columns:
            guest_table.heading(col, text=col)
            guest_table.column(col, width=100)

        guest_table.grid(row=0, column=0, sticky="nsew")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Fetch only the necessary columns from the database
        self.cursor.execute("SELECT name, age, gender, phone_no FROM Guest")
        for row in self.cursor.fetchall():
            guest_table.insert("", "end", values=row)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.heading = tk.Label(self.root, text="HOTEL MANAGEMENT SYSTEM", font=("Arial", 16, "bold"))
        self.heading.pack(pady=10)

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()
