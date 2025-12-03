from graphics import *
import csv


# ------------- BASIC HELPERS -------------

def clicked(rect, point):
    """Return True if mouse click (point) is inside the rectangle rect."""
    p1 = rect.getP1()
    p2 = rect.getP2()
    return (p1.x <= point.x <= p2.x) and (p1.y <= point.y <= p2.y)


def load_csv(filename):
    """Try to load a CSV file. Return (rows, headers) or (None, None) on error."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
            headers = reader.fieldnames
        return rows, headers
    except:
        return None, None


def detect_numeric_columns(rows, headers, max_check_rows=50):
    """
    Look through the data and return a list of column names that
    appear to contain numeric values (ints OR floats), ignoring blanks.
    Works for ANY dataset (matches.csv or uploaded).
    """
    numeric_cols = []

    for h in headers:
        is_numeric = True
        saw_value = False

        for row in rows[:max_check_rows]:
            val = row.get(h, "")
            if val is None:
                continue
            val = val.strip()
            if val == "":
                continue

            saw_value = True
            try:
                float(val)   # allow 1, 0, 2.5, 1.0, etc.
            except:
                is_numeric = False
                break

        if is_numeric and saw_value:
            numeric_cols.append(h)

    return numeric_cols



# ------------- SCREEN 1: LOAD DATA -------------

def draw_load_screen(win):
    """
    First screen UI.
    User can upload their own dataset or use matches.csv.
    Returns a dict of UI objects.
    """
    ui = {}

    title = Text(Point(250, 30), "Bad Boy Tracker – Load Data")
    title.setSize(16)
    title.setStyle("bold")
    title.draw(win)
    ui["title"] = title

    label = Text(Point(160, 90), "Enter CSV filename:")
    label.draw(win)
    ui["label"] = label

    file_entry = Entry(Point(160, 120), 20)
    file_entry.setText("mydata.csv")
    file_entry.draw(win)
    ui["file_entry"] = file_entry

    upload_rect = Rectangle(Point(260, 100), Point(440, 140))
    upload_rect.setFill("lightgray")
    upload_rect.draw(win)
    Text(upload_rect.getCenter(), "Upload My Dataset").draw(win)
    ui["upload_rect"] = upload_rect

    default_rect = Rectangle(Point(120, 160), Point(380, 200))
    default_rect.setFill("lightgray")
    default_rect.draw(win)
    Text(default_rect.getCenter(), "Use matches.csv (default)").draw(win)
    ui["default_rect"] = default_rect

    status = Text(Point(250, 250), "Status: Waiting...")
    status.draw(win)
    ui["status"] = status

    return ui


def load_data_loop(win, ui):
    """
    Handles clicks on the load screen until data is loaded or user exits.
    Returns (rows, headers) or (None, None) if user exits.
    """
    status = ui["status"]
    file_entry = ui["file_entry"]

    while True:
        p = win.getMouse()

        # Custom dataset
        if clicked(ui["upload_rect"], p):
            filename = file_entry.getText().strip()
            rows, headers = load_csv(filename)
            if rows is None:
                status.setText("Status: ERROR - could not open file")
            else:
                status.setText(f"Status: Loaded {len(rows)} rows from {filename}")
                return rows, headers

        # Default dataset
        if clicked(ui["default_rect"], p):
            rows, headers = load_csv("matches.csv")
            if rows is None:
                status.setText("Status: ERROR - could not open matches.csv")
            else:
                status.setText(f"Status: Loaded {len(rows)} rows from matches.csv")
                return rows, headers

        # Exit by clicking bottom-right corner
        if p.x > 450 and p.y > 260:
            return None, None


# ------------- SCREEN 2: HOW MANY VARIABLES -------------

def ask_num_variables_page(win):
    """
    Show buttons: 1 variable, 2 variables, 3 variables.
    Returns 1, 2, 3 or None (if exit).
    """
    bg = Rectangle(Point(0, 0), Point(500, 300))
    bg.setFill("white")
    bg.draw(win)

    title = Text(Point(250, 40), "How many variables do you want?")
    title.setSize(14)
    title.setStyle("bold")
    title.draw(win)

    instr = Text(Point(250, 70), "Click one of the options below.")
    instr.draw(win)

    btn1_rect = Rectangle(Point(60, 110), Point(180, 150))
    btn1_rect.setFill("lightgray")
    btn1_rect.draw(win)
    Text(btn1_rect.getCenter(), "1 variable").draw(win)

    btn2_rect = Rectangle(Point(200, 110), Point(320, 150))
    btn2_rect.setFill("lightgray")
    btn2_rect.draw(win)
    Text(btn2_rect.getCenter(), "2 variables").draw(win)

    btn3_rect = Rectangle(Point(340, 110), Point(460, 150))
    btn3_rect.setFill("lightgray")
    btn3_rect.draw(win)
    Text(btn3_rect.getCenter(), "3 variables").draw(win)

    status = Text(Point(250, 260), "Click a button, or bottom-right to exit.")
    status.draw(win)

    while True:
        p = win.getMouse()

        if clicked(btn1_rect, p):
            return 1
        if clicked(btn2_rect, p):
            return 2
        if clicked(btn3_rect, p):
            return 3

        if p.x > 450 and p.y > 260:
            return None


# ------------- SCREEN 3: PICK X, Y, Z VARIABLES -------------

def choose_variables_screen(win, rows, headers, num_variables):
    """
    Show up to 25 integer-looking headers in 3 columns.
    Let the user pick 1–3 variables by index:
    - X always required
    - Y required if num_variables >= 2
    - Z required if num_variables == 3
    Returns (x_var, y_var, z_var) or (None, None, None) if exit.
    """

    # Detect integer-looking columns from this dataset
    # Detect numeric (int or float) columns from this dataset
    avail_headers = detect_numeric_columns(rows, headers)

    if not avail_headers:
        bg = Rectangle(Point(0, 0), Point(500, 300))
        bg.setFill("white")
        bg.draw(win)
        msg = Text(Point(250, 150), "No integer columns detected in dataset.")
        msg.setTextColor("red")
        msg.draw(win)
        win.getMouse()
        return None, None, None

    # Clear screen
    bg = Rectangle(Point(0, 0), Point(500, 300))
    bg.setFill("white")
    bg.draw(win)

    title = Text(Point(250, 30), f"Select {num_variables} Variable(s)")
    title.setSize(14)
    title.setStyle("bold")
    title.draw(win)

    max_headers = min(25, len(avail_headers))
    rows_per_col = (max_headers + 2) // 3  # split across 3 columns

    start_y = 60
    line_h = 15
    col_x_positions = [90, 210, 330]

    # Draw names in 3 columns
    for col in range(3):
        x = col_x_positions[col]
        for row in range(rows_per_col):
            idx = col * rows_per_col + row
            if idx >= max_headers:
                break
            name = avail_headers[idx]
            label = Text(Point(x, start_y + row * line_h), f"{idx + 1}. {name}")
            label.draw(win)

    # X index
    x_label = Text(Point(430, 80), "X index:")
    x_label.draw(win)
    x_entry = Entry(Point(470, 80), 3)
    x_entry.draw(win)

    # Y index
    y_entry = None
    if num_variables >= 2:
        y_label = Text(Point(430, 120), "Y index:")
        y_label.draw(win)
        y_entry = Entry(Point(470, 120), 3)
        y_entry.draw(win)

    # Z index
    z_entry = None
    if num_variables == 3:
        z_label = Text(Point(430, 160), "Z index:")
        z_label.draw(win)
        z_entry = Entry(Point(470, 160), 3)
        z_entry.draw(win)

    # Confirm button
    btn_rect = Rectangle(Point(340, 210), Point(470, 240))
    btn_rect.setFill("lightgray")
    btn_rect.draw(win)
    Text(btn_rect.getCenter(), "Confirm").draw(win)

    status = Text(Point(250, 270), "")
    status.draw(win)

    x_var = None
    y_var = None
    z_var = None

    while True:
        p = win.getMouse()

        if clicked(btn_rect, p):
            try:
                idx_x = int(x_entry.getText().strip())
                x_var = avail_headers[idx_x - 1]
            except:
                status.setText("Error: X must be a valid index.")
                continue

            if num_variables >= 2:
                try:
                    idx_y = int(y_entry.getText().strip())
                    y_var = avail_headers[idx_y - 1]
                except:
                    status.setText("Error: Y must be a valid index.")
                    continue

            if num_variables == 3:
                try:
                    idx_z = int(z_entry.getText().strip())
                    z_var = avail_headers[idx_z - 1]
                except:
                    status.setText("Error: Z must be a valid index.")
                    continue

            status.setText("Variables selected!")
            break

        if p.x > 450 and p.y > 250:
            return None, None, None

    return x_var, y_var, z_var


# ------------- SCREEN 4: CHOOSE GRAPH TYPE -------------

def choose_graph_type_screen(win, num_variables):
    """
    Let user choose graph type:
    - Always allow "Line (index vs X)"
    - If num_variables >= 2, allow "Scatter (X vs Y)".
    Returns "line", "scatter", or None.
    """

    bg = Rectangle(Point(0, 0), Point(500, 300))
    bg.setFill("white")
    bg.draw(win)

    title = Text(Point(250, 40), "Choose Graph Type")
    title.setSize(14)
    title.setStyle("bold")
    title.draw(win)

    instr = Text(Point(250, 70), "Click a graph type (bottom-right to exit).")
    instr.draw(win)

    line_rect = Rectangle(Point(80, 110), Point(220, 150))
    line_rect.setFill("lightgray")
    line_rect.draw(win)
    Text(line_rect.getCenter(), "Line (index vs X)").draw(win)

    scatter_rect = None
    if num_variables >= 2:
        scatter_rect = Rectangle(Point(280, 110), Point(420, 150))
        scatter_rect.setFill("lightgray")
        scatter_rect.draw(win)
        Text(scatter_rect.getCenter(), "Scatter (X vs Y)").draw(win)

    status = Text(Point(250, 260), "")
    status.draw(win)

    while True:
        p = win.getMouse()

        if clicked(line_rect, p):
            return "line"

        if scatter_rect is not None and clicked(scatter_rect, p):
            return "scatter"

        if p.x > 450 and p.y > 260:
            return None


# ------------- GRAPH HELPERS -------------

def extract_numeric_column(rows, colname, max_points=50):
    """Return a list of floats from the given column name, skipping non-numeric rows."""
    values = []
    for row in rows:
        if colname not in row:
            continue
        val = row[colname]
        if val is None:
            continue
        val = val.strip()
        if val == "":
            continue
        try:
            v = float(val)
            values.append(v)
        except:
            continue
        if len(values) >= max_points:
            break
    return values


def extract_numeric_xy(rows, x_name, y_name, max_points=100):
    """Return two lists (xs, ys) of floats for a scatter, skipping bad rows."""
    xs = []
    ys = []
    for row in rows:
        if x_name not in row or y_name not in row:
            continue
        vx = row[x_name]
        vy = row[y_name]
        if vx is None or vy is None:
            continue
        vx = vx.strip()
        vy = vy.strip()
        if vx == "" or vy == "":
            continue
        try:
            xv = float(vx)
            yv = float(vy)
        except:
            continue
        xs.append(xv)
        ys.append(yv)
        if len(xs) >= max_points:
            break
    return xs, ys


# ------------- SCREEN 5: DRAW GRAPH -------------

def draw_graph(win, graph_type, rows, x_var, y_var):
    """
    Clear the window and draw the selected graph type using the chosen variables.
    graph_type: "line" or "scatter"
    rows: list of CSV row dicts
    x_var, y_var: column names (strings)
    """

    bg = Rectangle(Point(0, 0), Point(500, 300))
    bg.setFill("white")
    bg.draw(win)

    title_text = f"{graph_type.capitalize()} using {x_var}"
    if graph_type == "scatter" and y_var is not None:
        title_text += f" vs {y_var}"

    title = Text(Point(250, 20), title_text)
    title.setSize(12)
    title.setStyle("bold")
    title.draw(win)

    left = 60
    right = 460
    top = 40
    bottom = 260

    x_axis = Line(Point(left, bottom), Point(right, bottom))
    x_axis.draw(win)
    y_axis = Line(Point(left, bottom), Point(left, top))
    y_axis.draw(win)

    x_label = Text(Point((left + right) / 2, bottom + 15), x_var)
    x_label.draw(win)

    if graph_type == "line":
        y_label = Text(Point(left - 30, (top + bottom) / 2), x_var)
        y_label.draw(win)

        values = extract_numeric_column(rows, x_var, max_points=50)
        if not values:
            err = Text(Point(250, 150), "ERROR: X column is not numeric or empty.")
            err.setTextColor("red")
            err.draw(win)
            win.getMouse()
            return

        n = len(values)
        vmin = min(values)
        vmax = max(values)
        if vmin == vmax:
            vmin -= 1
            vmax += 1

        prev_point = None
        for i, v in enumerate(values):
            if n == 1:
                x_pix = (left + right) / 2
            else:
                x_pix = left + (right - left) * i / (n - 1)
            y_pix = bottom - (v - vmin) / (vmax - vmin) * (bottom - top)

            pt = Point(x_pix, y_pix)
            circ = Circle(pt, 2)
            circ.setFill("black")
            circ.draw(win)

            if prev_point is not None:
                seg = Line(prev_point, pt)
                seg.draw(win)

            prev_point = pt

    elif graph_type == "scatter" and y_var is not None:
        y_label = Text(Point(left - 30, (top + bottom) / 2), y_var)
        y_label.draw(win)

        xs, ys = extract_numeric_xy(rows, x_var, y_var, max_points=100)
        if not xs or not ys:
            err = Text(Point(250, 150), "ERROR: X or Y not numeric/empty.")
            err.setTextColor("red")
            err.draw(win)
            win.getMouse()
            return

        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        if xmin == xmax:
            xmin -= 1
            xmax += 1
        if ymin == ymax:
            ymin -= 1
            ymax += 1

        for xv, yv in zip(xs, ys):
            x_pix = left + (xv - xmin) / (xmax - xmin) * (right - left)
            y_pix = bottom - (yv - ymin) / (ymax - ymin) * (bottom - top)
            pt = Point(x_pix, y_pix)
            circ = Circle(pt, 2)
            circ.setFill("black")
            circ.draw(win)

    msg = Text(Point(250, 280), "Click anywhere to close.")
    msg.draw(win)
    win.getMouse()


# ------------- MAIN -------------

def main():
    win = GraphWin("Bad boy tracker", 500, 300)
    win.setBackground("white")

    # Screen 1: load data
    ui = draw_load_screen(win)
    rows, headers = load_data_loop(win, ui)
    if rows is None:
        win.close()
        return

    # Remove old UI (including Entry box)
    for item in ui.values():
        try:
            item.undraw()
        except:
            pass

    # Screen 2: how many variables
    num_variables = ask_num_variables_page(win)
    if num_variables is None:
        win.close()
        return

    # Screen 3: choose X/Y/Z variables (only integer-looking columns)
    x_var, y_var, z_var = choose_variables_screen(win, rows, headers, num_variables)
    if x_var is None:
        win.close()
        return

    # Screen 4: choose graph type
    graph_type = choose_graph_type_screen(win, num_variables)
    if graph_type is None:
        win.close()
        return

    # Screen 5: draw graph
    draw_graph(win, graph_type, rows, x_var, y_var)

    win.close()


main()
