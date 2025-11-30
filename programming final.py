from graphics import *
import csv


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


def draw_load_screen(win):
    """
    Draw the initial 'load data' UI and return a dictionary
    with all the important GUI elements.
    """
    ui = {}

    # Label for file entry (left label)
    file_label = Text(Point(87, 50), "CSV file")
    file_label.draw(win)
    ui["file_label"] = file_label

    # Entry box for file name (left inpur)
    file_entry = Entry(Point(87, 70), 10)
    file_entry.setText("mydata.csv")
    file_entry.draw(win)
    ui["file_entry"] = file_entry

    # LEFT button: load CSV from what the user typed
    load_rect_left = Rectangle(Point(55, 80), Point(110, 110))
    load_rect_left.setFill("lightgray")
    load_rect_left.draw(win)
    load_text_left = Text(load_rect_left.getCenter(), "Load")
    load_text_left.draw(win)
    ui["load_rect_left"] = load_rect_left

    # RIGHT button: always load matches.csv
    load_rect_right = Rectangle(Point(200, 60), Point(360, 80))
    load_rect_right.setFill("lightgray")
    load_rect_right.draw(win)
    load_text_right = Text(load_rect_right.getCenter(), "Load matches.csv")
    load_text_right.draw(win)
    ui["load_rect_right"] = load_rect_right

    # Status text
    status = Text(Point(250, 250), "Status: Waiting...")
    status.draw(win)
    ui["status"] = status

    return ui


def ask_num_variables_page(win):
    
   
     """
    Replace the current contents of 'win' with a new page asking
    'How many variables (1–3)?'.
    Returns the chosen integer, or None if the user exits.
    """

    # "Clear" the old page by drawing a big white rectangle on top
    bg = Rectangle(Point(0, 0), Point(500, 300))
    bg.setFill("white")
    bg.draw(win)

    # Question label
    label = Text(Point(250, 80), "How many variables (1–3)?")
    label.draw(win)

    # Entry box
    entry = Entry(Point(250, 110), 3)
    entry.setText("2")
    entry.draw(win)

    # Confirm button
    btn_rect = Rectangle(Point(200, 140), Point(300, 180))
    btn_rect.setFill("lightgray")
    btn_rect.draw(win)
    btn_text = Text(btn_rect.getCenter(), "Set # variables")
    btn_text.draw(win)

    # Status text for this page
    status2 = Text(Point(250, 220), "")
    status2.draw(win)

    num_variables = None

    while True:
        p = win.getMouse()

        # Click on button?
        if clicked(btn_rect, p):
            txt = entry.getText().strip()
            try:
                n = int(txt)
                if 1 <= n <= 3:
                    num_variables = n
                    status2.setText(f"Number of variables set to {n}")
                    break
                else:
                    status2.setText("ERROR: enter 1, 2, or 3")
            except:
                status2.setText("ERROR: not a valid integer")

        # Exit by clicking bottom-right corner of this page
        if p.x > 450 and p.y > 260:
            break

    return num_variables


def event_loop(win, ui):
    """
    Handle user interaction on the load screen.
    Returns (rows, headers, num_variables) for the last successfully loaded file,
    or (None, None, None) if user exits without loading.
    """
    rows = None
    headers = None
    num_variables = None

    file_entry = ui["file_entry"]
    load_rect_left = ui["load_rect_left"]
    load_rect_right = ui["load_rect_right"]
    status = ui["status"]

    while True:
        click_point = win.getMouse()

        # LEFT button: load CSV typed in entry
        if clicked(load_rect_left, click_point):
            filename = file_entry.getText().strip()
            rows, headers = load_csv(filename)
            if rows is None:
                status.setText("Status: ERROR - could not open file")
            else:
                status.setText(f"Status: Loaded {len(rows)} rows from {filename}")

                # --- hide everything from the first page ---
                for item in ui.values():
                    item.undraw()

                # now show the "how many variables" page
                num_variables = ask_num_variables_page(win)
                return rows, headers, num_variables

        # RIGHT button: always load matches.csv
        if clicked(load_rect_right, click_point):
            rows, headers = load_csv("matches.csv")
            if rows is None:
                status.setText("Status: ERROR - could not open matches.csv")
            else:
                status.setText(
                    "Status: Loaded " + str(len(rows)) + " rows from matches.csv"
                )

                # --- hide everything from the first page ---
                for item in ui.values():
                    item.undraw()

                # now show the "how many variables" page
                num_variables = ask_num_variables_page(win)
                return rows, headers, num_variables

        # Exit condition from the load screen (bottom-right click)
        if click_point.x > 450 and click_point.y > 260:
            return None, None, None

def main():
    win = GraphWin("Bad boy tracker", 500, 300)
    win.setBackground("white")

    ui = draw_load_screen(win)
    rows, headers, num_variables = event_loop(win, ui)

    # Later you will use rows, headers, num_variables to select X/Y and plot.

    win.close()



main()



