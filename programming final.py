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

    # Label for file entry (left side)
    file_label = Text(Point(87, 50), "CSV file")
    file_label.draw(win)
    ui["file_label"] = file_label

    # Entry box for file name (left side)
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


def event_loop(win, ui):
    """
    Handle user interaction on the load screen.
    Returns (rows, headers) for the last successfully loaded file,
    or (None, None) if user exits without loading.
    """
    rows = None
    headers = None

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
                status.setText(f"Status: Loaded {len(rows)} rows from " + filename)

        # RIGHT button: always load matches.csv
        if clicked(load_rect_right, click_point):
            rows, headers = load_csv("matches.csv")
            if rows is None:
                status.setText("Status: ERROR - could not open matches.csv")
            else:
                status.setText("Status: Loaded " + str(len(rows)) + " rows from matches.csv")

        # Exit condition (bottom-right click)
        if click_point.x > 450 and click_point.y > 260:
            break

    return rows, headers


def main():
    win = GraphWin("Bad boy tracker", 500, 300)
    win.setBackground("white")

    ui = draw_load_screen(win)
    rows, headers = event_loop(win, ui)

    # later you will pass rows/headers into the next part of the app, e.g. graph screen

    win.close()


main()


