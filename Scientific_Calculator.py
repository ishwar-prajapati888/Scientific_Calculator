
import tkinter as tk
from tkinter import ttk, messagebox
import math
import ast
import operator
from datetime import date, datetime, timedelta

# =====================================================
# ALL-IN-ONE ADVANCED CALCULATOR
# Scientific + History + Units + Age + Finance + Dates
# =====================================================

# -------------------- Main Window --------------------

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("650x760")
root.minsize(550, 650)
root.configure(bg="#1F2937")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#1F2937")
style.configure(
    "TNotebook.Tab",
    font=("Arial", 11, "bold"),
    padding=[12, 8]
)
style.configure(
    "TLabel",
    font=("Arial", 11),
    background="#F3F4F6",
    foreground="#111827"
)
style.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    padding=7
)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=8, pady=8)

calc_tab = tk.Frame(notebook, bg="#1F2937")
history_tab = tk.Frame(notebook, bg="#F3F4F6")
unit_tab = tk.Frame(notebook, bg="#F3F4F6")
age_tab = tk.Frame(notebook, bg="#F3F4F6")
finance_tab = tk.Frame(notebook, bg="#F3F4F6")
date_tab = tk.Frame(notebook, bg="#F3F4F6")

notebook.add(calc_tab, text="Calculator")
notebook.add(history_tab, text="History")
notebook.add(unit_tab, text="Unit Converter")
notebook.add(age_tab, text="Age Calculator")
notebook.add(finance_tab, text="Finance")
notebook.add(date_tab, text="Date Calculator")

# =====================================================
# 1. SCIENTIFIC CALCULATOR (ORIGINAL BUTTONS PRESERVED)
# =====================================================

expr = ""
display = tk.StringVar()
history = []

def safe_eval(expression):
    """Evaluate basic mathematical expressions safely."""

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv
    }

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid value")

        if isinstance(node, ast.Name):
            constants = {"pi": math.pi, "e": math.e}
            if node.id in constants:
                return constants[node.id]
            raise ValueError("Unknown name")

        if isinstance(node, ast.UnaryOp):
            value = calculate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return value
            if isinstance(node.op, ast.USub):
                return -value
            raise ValueError("Invalid operator")

        if isinstance(node, ast.BinOp):
            left = calculate(node.left)
            right = calculate(node.right)

            op_type = type(node.op)
            if op_type not in allowed_operators:
                raise ValueError("Invalid operator")

            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Power too large")

            result = allowed_operators[op_type](left, right)

            if isinstance(result, complex):
                raise ValueError("Complex numbers not supported")

            if isinstance(result, float) and not math.isfinite(result):
                raise ValueError("Invalid result")

            if abs(result) > 1e100:
                raise ValueError("Result too large")

            return result

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return calculate(tree)


def add_history(expression, result):
    history.append(f"{expression} = {result}")
    history_list.insert(tk.END, history[-1])


def press(key):
    global expr

    if display.get() == "Error":
        expr = ""

    expr += str(key)
    display.set(expr)


def equal():
    global expr

    try:
        original = expr
        result = safe_eval(expr)

        if isinstance(result, float):
            result = round(result, 12)

        display.set(str(result))
        add_history(original, result)
        expr = str(result)

    except Exception:
        display.set("Error")
        expr = ""


def clear():
    global expr
    expr = ""
    display.set("")


def backspace():
    global expr
    expr = expr[:-1]
    display.set(expr)


def scientific(func):
    global expr

    try:
        value = float(safe_eval(expr))

        if func == "sin":
            result = math.sin(math.radians(value))
        elif func == "cos":
            result = math.cos(math.radians(value))
        elif func == "tan":
            result = math.tan(math.radians(value))
        elif func == "asin":
            result = math.degrees(math.asin(value))
        elif func == "acos":
            result = math.degrees(math.acos(value))
        elif func == "atan":
            result = math.degrees(math.atan(value))
        elif func == "sqrt":
            result = math.sqrt(value)
        elif func == "square":
            result = value ** 2
        elif func == "log":
            result = math.log10(value)
        elif func == "ln":
            result = math.log(value)
        elif func == "factorial":
            if value < 0 or not value.is_integer():
                raise ValueError()
            if value > 170:
                raise ValueError()
            result = math.factorial(int(value))
        elif func == "reciprocal":
            result = 1 / value
        elif func == "10power":
            result = 10 ** value
        elif func == "exp":
            result = math.exp(value)
        elif func == "percent":
            result = value / 100
        else:
            return

        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError()

        old_expr = expr
        result = round(result, 12)
        display.set(str(result))
        add_history(f"{func}({old_expr})", result)
        expr = str(result)

    except Exception:
        display.set("Error")
        expr = ""


def insert_constant(value):
    global expr

    if display.get() == "Error":
        expr = ""

    expr += str(value)
    display.set(expr)


def add_button(text, row, col, command, color="#374151",
               colspan=1):

    btn = tk.Button(
        calc_tab,
        text=text,
        command=command,
        width=8,
        height=2,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="white",
        activebackground="#6B7280",
        activeforeground="white",
        relief=tk.RAISED,
        bd=2
    )

    btn.grid(
        row=row,
        column=col,
        columnspan=colspan,
        padx=4,
        pady=4,
        sticky="nsew"
    )


screen = tk.Entry(
    calc_tab,
    textvariable=display,
    font=("Arial", 22, "bold"),
    justify="right",
    bd=8,
    relief=tk.SUNKEN,
    bg="#F9FAFB",
    fg="#111827"
)

screen.grid(
    row=0,
    column=0,
    columnspan=4,
    padx=10,
    pady=15,
    ipady=12,
    sticky="nsew"
)

# Original controls
add_button("Clear", 1, 0, clear, "#DC2626")
add_button("⌫", 1, 1, backspace, "#D97706")
add_button("π", 1, 2, lambda: insert_constant(math.pi), "#2563EB")
add_button("e", 1, 3, lambda: insert_constant(math.e), "#2563EB")

add_button("sin", 2, 0, lambda: scientific("sin"), "#059669")
add_button("cos", 2, 1, lambda: scientific("cos"), "#059669")
add_button("tan", 2, 2, lambda: scientific("tan"), "#059669")
add_button("√x", 2, 3, lambda: scientific("sqrt"), "#7C3AED")

add_button("asin", 3, 0, lambda: scientific("asin"), "#0D9488")
add_button("acos", 3, 1, lambda: scientific("acos"), "#0D9488")
add_button("atan", 3, 2, lambda: scientific("atan"), "#0D9488")
add_button("x²", 3, 3, lambda: scientific("square"), "#7C3AED")

add_button("log", 4, 0, lambda: scientific("log"), "#7C3AED")
add_button("ln", 4, 1, lambda: scientific("ln"), "#7C3AED")
add_button("n!", 4, 2, lambda: scientific("factorial"), "#7C3AED")
add_button("1/x", 4, 3, lambda: scientific("reciprocal"), "#7C3AED")

add_button("7", 5, 0, lambda: press("7"))
add_button("8", 5, 1, lambda: press("8"))
add_button("9", 5, 2, lambda: press("9"))
add_button("/", 5, 3, lambda: press("/"), "#D97706")

add_button("4", 6, 0, lambda: press("4"))
add_button("5", 6, 1, lambda: press("5"))
add_button("6", 6, 2, lambda: press("6"))
add_button("*", 6, 3, lambda: press("*"), "#D97706")

add_button("1", 7, 0, lambda: press("1"))
add_button("2", 7, 1, lambda: press("2"))
add_button("3", 7, 2, lambda: press("3"))
add_button("-", 7, 3, lambda: press("-"), "#D97706")

add_button("10ˣ", 8, 0, lambda: scientific("10power"), "#7C3AED")
add_button("eˣ", 8, 1, lambda: scientific("exp"), "#7C3AED")
add_button("%", 8, 2, lambda: scientific("percent"), "#7C3AED")
add_button("+", 8, 3, lambda: press("+"), "#D97706")

add_button("0", 9, 0, lambda: press("0"))
add_button(".", 9, 1, lambda: press("."))
add_button("=", 9, 2, equal, "#16A34A", colspan=2)

for col in range(4):
    calc_tab.grid_columnconfigure(col, weight=1)

for row in range(1, 10):
    calc_tab.grid_rowconfigure(row, weight=1)

# =====================================================
# 2. HISTORY
# =====================================================

tk.Label(
    history_tab,
    text="Calculation History",
    font=("Arial", 20, "bold"),
    bg="#F3F4F6"
).pack(pady=15)

history_frame = tk.Frame(history_tab)
history_frame.pack(fill="both", expand=True, padx=15, pady=10)

history_scroll = tk.Scrollbar(history_frame)
history_scroll.pack(side="right", fill="y")

history_list = tk.Listbox(
    history_frame,
    font=("Arial", 12),
    yscrollcommand=history_scroll.set,
    height=20
)
history_list.pack(fill="both", expand=True)

history_scroll.config(command=history_list.yview)


def use_history():
    global expr

    selected = history_list.curselection()
    if not selected:
        messagebox.showwarning("History", "Select a calculation first")
        return

    item = history_list.get(selected[0])
    result = item.split(" = ", 1)[1]

    expr = result
    display.set(result)
    notebook.select(calc_tab)


def clear_history():
    history.clear()
    history_list.delete(0, tk.END)


tk.Button(
    history_tab,
    text="Use Selected Result",
    command=use_history,
    bg="#2563EB",
    fg="white",
    font=("Arial", 11, "bold")
).pack(pady=5)

tk.Button(
    history_tab,
    text="Clear History",
    command=clear_history,
    bg="#DC2626",
    fg="white",
    font=("Arial", 11, "bold")
).pack(pady=5)

# =====================================================
# 3. UNIT CONVERTER
# =====================================================

tk.Label(
    unit_tab,
    text="Unit Converter",
    font=("Arial", 20, "bold"),
    bg="#F3F4F6"
).pack(pady=15)

unit_categories = {
    "Length": {
        "Meter": 1,
        "Kilometer": 1000,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.344,
        "Foot": 0.3048,
        "Inch": 0.0254
    },
    "Weight": {
        "Kilogram": 1,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.45359237,
        "Ounce": 0.0283495,
        "Ton": 1000
    },
    "Area": {
        "Square Meter": 1,
        "Square Kilometer": 1000000,
        "Square Foot": 0.092903,
        "Acre": 4046.856,
        "Hectare": 10000
    },
    "Volume": {
        "Liter": 1,
        "Milliliter": 0.001,
        "Cubic Meter": 1000,
        "Gallon (US)": 3.78541,
        "Cup (US)": 0.236588
    },
    "Speed": {
        "Meter/Second": 1,
        "Kilometer/Hour": 1 / 3.6,
        "Mile/Hour": 0.44704,
        "Foot/Second": 0.3048
    },
    "Time": {
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800
    }
}

unit_category = tk.StringVar(value="Length")
unit_value = tk.StringVar(value="1")
unit_from = tk.StringVar(value="Meter")
unit_to = tk.StringVar(value="Kilometer")
unit_result = tk.StringVar(value="Result will appear here")


def update_units(event=None):
    category = unit_category.get()
    units = list(unit_categories[category].keys())

    from_box["values"] = units
    to_box["values"] = units

    unit_from.set(units[0])
    unit_to.set(units[1] if len(units) > 1 else units[0])


def convert_unit():
    try:
        category = unit_category.get()
        value = float(unit_value.get())

        if category == "Temperature":
            source = unit_from.get()
            target = unit_to.get()

            if source == "Celsius":
                celsius = value
            elif source == "Fahrenheit":
                celsius = (value - 32) * 5 / 9
            else:
                celsius = value - 273.15

            if target == "Celsius":
                result = celsius
            elif target == "Fahrenheit":
                result = celsius * 9 / 5 + 32
            else:
                result = celsius + 273.15

        else:
            units = unit_categories[category]
            base_value = value * units[unit_from.get()]
            result = base_value / units[unit_to.get()]

        unit_result.set(f"{result:.8g} {unit_to.get()}")

    except Exception:
        unit_result.set("Invalid input")


unit_categories["Temperature"] = {
    "Celsius": 1,
    "Fahrenheit": 2,
    "Kelvin": 3
}

unit_category_box = ttk.Combobox(
    unit_tab,
    textvariable=unit_category,
    values=list(unit_categories.keys()),
    state="readonly",
    width=25
)
unit_category_box.pack(pady=12)
unit_category_box.bind("<<ComboboxSelected>>", update_units)

tk.Label(unit_tab, text="Enter Value").pack(pady=5)
tk.Entry(
    unit_tab,
    textvariable=unit_value,
    font=("Arial", 13),
    justify="center"
).pack(pady=5)

tk.Label(unit_tab, text="From Unit").pack(pady=5)
from_box = ttk.Combobox(
    unit_tab,
    textvariable=unit_from,
    state="readonly",
    width=25
)
from_box.pack(pady=5)

tk.Label(unit_tab, text="To Unit").pack(pady=5)
to_box = ttk.Combobox(
    unit_tab,
    textvariable=unit_to,
    state="readonly",
    width=25
)
to_box.pack(pady=5)

ttk.Button(
    unit_tab,
    text="Convert",
    command=convert_unit
).pack(pady=15)

tk.Label(
    unit_tab,
    textvariable=unit_result,
    font=("Arial", 15, "bold"),
    fg="#047857",
    bg="#F3F4F6"
).pack(pady=15)

update_units()

# =====================================================
# 4. AGE CALCULATOR
# =====================================================

tk.Label(
    age_tab,
    text="Date of Birth Calculator",
    font=("Arial", 20, "bold"),
    bg="#F3F4F6"
).pack(pady=20)

tk.Label(
    age_tab,
    text="Enter Date of Birth (DD-MM-YYYY)",
    bg="#F3F4F6"
).pack(pady=10)

dob_entry = tk.Entry(
    age_tab,
    font=("Arial", 14),
    justify="center"
)
dob_entry.pack(pady=10)
dob_entry.insert(0, "01-01-2000")

age_result = tk.StringVar(value="Your age will appear here")


def calculate_age():
    try:
        dob = datetime.strptime(
            dob_entry.get(), "%d-%m-%Y"
        ).date()

        today = date.today()

        if dob > today:
            raise ValueError("Future date")

        years = today.year - dob.year
        months = today.month - dob.month
        days = today.day - dob.day

        if days < 0:
            months -= 1
            previous_month = today.month - 1 or 12
            previous_year = today.year if today.month > 1 else today.year - 1
            days += (
                date(previous_year, previous_month + 1, 1)
                - date(previous_year, previous_month, 1)
            ).days

        if months < 0:
            years -= 1
            months += 12

        total_days = (today - dob).days

        # Next birthday
        next_year = today.year
        try:
            next_birthday = dob.replace(year=next_year)
        except ValueError:
            next_birthday = date(next_year, 2, 28)

        if next_birthday <= today:
            next_year += 1
            try:
                next_birthday = dob.replace(year=next_year)
            except ValueError:
                next_birthday = date(next_year, 2, 28)

        days_left = (next_birthday - today).days

        age_result.set(
            f"Age: {years} Years, {months} Months, {days} Days\n\n"
            f"Total Days Lived: {total_days}\n"
            f"Next Birthday: {next_birthday.strftime('%d-%m-%Y')}\n"
            f"Days Until Birthday: {days_left}"
        )

    except Exception:
        messagebox.showerror(
            "Error",
            "Please enter a valid DOB in DD-MM-YYYY format."
        )


ttk.Button(
    age_tab,
    text="Calculate Age",
    command=calculate_age
).pack(pady=15)

tk.Label(
    age_tab,
    textvariable=age_result,
    font=("Arial", 13, "bold"),
    bg="#F3F4F6",
    justify="center"
).pack(pady=20)

# =====================================================
# 5. FINANCE CALCULATOR
# =====================================================

tk.Label(
    finance_tab,
    text="Finance Calculator",
    font=("Arial", 20, "bold"),
    bg="#F3F4F6"
).pack(pady=12)

finance_mode = tk.StringVar(value="Simple Interest")

finance_modes = [
    "Simple Interest",
    "Compound Interest",
    "EMI Calculator",
    "FD Maturity",
    "RD Maturity"
]

ttk.Combobox(
    finance_tab,
    textvariable=finance_mode,
    values=finance_modes,
    state="readonly",
    width=25
).pack(pady=8)

finance_entries = {}

finance_fields = [
    ("Principal / Amount", "amount"),
    ("Annual Interest Rate (%)", "rate"),
    ("Time (Years)", "years"),
    ("Monthly Deposit (RD only)", "monthly")
]

for label, key in finance_fields:
    tk.Label(
        finance_tab,
        text=label,
        bg="#F3F4F6"
    ).pack(pady=3)

    entry = tk.Entry(
        finance_tab,
        font=("Arial", 11),
        justify="center",
        width=25
    )
    entry.pack(pady=3)
    finance_entries[key] = entry

finance_result = tk.StringVar(
    value="Your financial calculation will appear here"
)


def calculate_finance():
    try:
        mode = finance_mode.get()

        amount = float(finance_entries["amount"].get())
        rate = float(finance_entries["rate"].get())
        years = float(finance_entries["years"].get())
        monthly = float(finance_entries["monthly"].get() or 0)

        if amount < 0 or rate < 0 or years <= 0 or monthly < 0:
            raise ValueError("Invalid values")

        r = rate / 100

        if mode == "Simple Interest":
            interest = amount * r * years
            total = amount + interest

            result = (
                f"Principal: ₹{amount:,.2f}\n"
                f"Interest: ₹{interest:,.2f}\n"
                f"Total Amount: ₹{total:,.2f}"
            )

        elif mode == "Compound Interest":
            total = amount * (1 + r) ** years
            interest = total - amount

            result = (
                f"Principal: ₹{amount:,.2f}\n"
                f"Compound Interest: ₹{interest:,.2f}\n"
                f"Maturity Amount: ₹{total:,.2f}"
            )

        elif mode == "EMI Calculator":
            n = years * 12
            monthly_rate = r / 12

            if monthly_rate == 0:
                emi = amount / n
            else:
                emi = (
                    amount * monthly_rate *
                    (1 + monthly_rate) ** n /
                    ((1 + monthly_rate) ** n - 1)
                )

            total = emi * n
            interest = total - amount

            result = (
                f"Loan Amount: ₹{amount:,.2f}\n"
                f"Monthly EMI: ₹{emi:,.2f}\n"
                f"Total Interest: ₹{interest:,.2f}\n"
                f"Total Payment: ₹{total:,.2f}"
            )

        elif mode == "FD Maturity":
            # Quarterly compounding approximation
            total = amount * (1 + r / 4) ** (4 * years)
            interest = total - amount

            result = (
                f"FD Principal: ₹{amount:,.2f}\n"
                f"Interest Earned: ₹{interest:,.2f}\n"
                f"Maturity Amount: ₹{total:,.2f}"
            )

        elif mode == "RD Maturity":
            # Monthly deposits, monthly compounding.
            n = int(round(years * 12))
            monthly_rate = r / 12

            if n <= 0:
                raise ValueError()

            if monthly_rate == 0:
                total = monthly * n
            else:
                total = (
                    monthly *
                    (((1 + monthly_rate) ** n - 1) / monthly_rate)
                )

            invested = monthly * n
            interest = total - invested

            result = (
                f"Monthly Deposit: ₹{monthly:,.2f}\n"
                f"Total Invested: ₹{invested:,.2f}\n"
                f"Interest Earned: ₹{interest:,.2f}\n"
                f"Maturity Amount: ₹{total:,.2f}"
            )

        finance_result.set(result)

    except Exception:
        messagebox.showerror(
            "Finance Error",
            "Enter valid numbers in all required fields."
        )


ttk.Button(
    finance_tab,
    text="Calculate Finance",
    command=calculate_finance
).pack(pady=12)

tk.Label(
    finance_tab,
    textvariable=finance_result,
    font=("Arial", 11, "bold"),
    bg="#F3F4F6",
    justify="center"
).pack(pady=10)

# =====================================================
# 6. DATE CALCULATOR
# =====================================================

tk.Label(
    date_tab,
    text="Date Calculator",
    font=("Arial", 20, "bold"),
    bg="#F3F4F6"
).pack(pady=15)

tk.Label(
    date_tab,
    text="Start Date (DD-MM-YYYY)",
    bg="#F3F4F6"
).pack(pady=5)

start_entry = tk.Entry(
    date_tab,
    font=("Arial", 12),
    justify="center"
)
start_entry.pack(pady=5)
start_entry.insert(0, date.today().strftime("%d-%m-%Y"))

tk.Label(
    date_tab,
    text="End Date (DD-MM-YYYY)",
    bg="#F3F4F6"
).pack(pady=5)

end_entry = tk.Entry(
    date_tab,
    font=("Arial", 12),
    justify="center"
)
end_entry.pack(pady=5)
end_entry.insert(0, date.today().strftime("%d-%m-%Y"))

date_result = tk.StringVar(value="Date difference will appear here")


def calculate_date_difference():
    try:
        start = datetime.strptime(
            start_entry.get(), "%d-%m-%Y"
        ).date()

        end = datetime.strptime(
            end_entry.get(), "%d-%m-%Y"
        ).date()

        difference = abs((end - start).days)

        years = difference // 365
        remaining = difference % 365
        months = remaining // 30
        days = remaining % 30

        date_result.set(
            f"Total Difference: {difference} Days\n\n"
            f"Approximate Difference: {years} Years, "
            f"{months} Months, {days} Days"
        )

    except Exception:
        messagebox.showerror(
            "Date Error",
            "Please enter valid dates in DD-MM-YYYY format."
        )


ttk.Button(
    date_tab,
    text="Calculate Date Difference",
    command=calculate_date_difference
).pack(pady=15)

tk.Label(
    date_tab,
    text="Add or Subtract Days",
    font=("Arial", 14, "bold"),
    bg="#F3F4F6"
).pack(pady=12)

days_entry = tk.Entry(
    date_tab,
    font=("Arial", 12),
    justify="center"
)
days_entry.pack(pady=5)
days_entry.insert(0, "30")

future_result = tk.StringVar(value="Future/Past date will appear here")


def add_subtract_days():
    try:
        start = datetime.strptime(
            start_entry.get(), "%d-%m-%Y"
        ).date()

        days = int(days_entry.get())
        result = start + timedelta(days=days)

        future_result.set(
            f"Result Date: {result.strftime('%d-%m-%Y')}"
        )

    except Exception:
        messagebox.showerror(
            "Date Error",
            "Please enter a valid date and number of days."
        )


ttk.Button(
    date_tab,
    text="Calculate New Date",
    command=add_subtract_days
).pack(pady=10)

ttk.Button(
    date_tab,
    text="Calculate Difference",
    command=calculate_date_difference
).pack(pady=5)

tk.Label(
    date_tab,
    textvariable=date_result,
    font=("Arial", 11, "bold"),
    bg="#F3F4F6"
).pack(pady=8)

tk.Label(
    date_tab,
    textvariable=future_result,
    font=("Arial", 12, "bold"),
    fg="#047857",
    bg="#F3F4F6"
).pack(pady=8)

# =====================================================
# KEYBOARD SUPPORT
# =====================================================

def keyboard_input(event):
    global expr

    # Only handle keyboard shortcuts on Calculator tab.
    if notebook.select() != str(calc_tab):
        return

    if event.char in "0123456789.+-*/()%":
        press(event.char)

    elif event.keysym == "Return":
        equal()

    elif event.keysym == "BackSpace":
        backspace()

    elif event.keysym == "Escape":
        clear()


root.bind_all("<Key>", keyboard_input)

# -------------------- RUN APPLICATION --------------------

root.mainloop()
