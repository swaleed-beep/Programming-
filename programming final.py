import graphics
from graphics import *
import csv


def clicked(rect, point):
    """Return True if mouse click (point) is inside the rectangle rect."""
    p1 = rect.getP1()
    p2 = rect.getP2()
    return (p1.x <= point.x <= p2.x) and (p1.y <= point.y <= p2.y)


def main():
    win = GraphWin("Bad boy tracker", 500, 300)
    win.setBackground("white")

    # Label for file entry (left side)
    file_label = Text(Point(87, 80), "CSV file")
    file_label.draw(win)

    # Entry box for file name (left side)
    file_entry = Entry(Point(87, 100), 10)  # centre x=180
    file_entry.setText("mydata.csv")        # default suggestion
    file_entry.draw(win)

    # LEFT button: load CSV from what the user typed
    load_rect_left = Rectangle(Point(60, 120), Point(110, 150))
    load_rect_left.setFill("lightgray")
    load_rect_left.draw(win)
    load_text_left = Text(load_rect_left.getCenter(), "Load ")
    load_text_left.draw(win)

    # RIGHT button: always load matches.csv
    load_rect_right = Rectangle(Point(280, 80), Point(460, 120))
    load_rect_right.setFill("lightgray")
    load_rect_right.draw(win)
    load_text_right = Text(load_rect_right.getCenter(), "Load matches.csv")
    load_text_right.draw(win)

    # Status text at the bottom
    status = Text(Point(250, 250), "Status: Waiting...")
    status.draw(win)

    # We'll store loaded rows here
    rows = None

    # Event loop
    while True:
        click_point = win.getMouse()

        # If user clicks inside the LEFT button (load from input)
        if clicked(load_rect_left, click_point):
            filename = file_entry.getText().strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    rows = [row for row in reader]
                status.setText(f"Status: Loaded {len(rows)} rows from {filename}")
            except:
                status.setText("Status: ERROR - could not open file from input")

        # If user clicks inside the RIGHT button (always matches.csv)
        if clicked(load_rect_right, click_point):
            filename = "matches.csv"
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    rows = [row for row in reader]
                status.setText(f"Status: Loaded {len(rows)} rows from {filename}")
            except:
                status.setText("Status: ERROR - could not open matches.csv")

        # Simple way to exit: click in bottom-right corner area
        if click_point.x > 450 and click_point.y > 260:
            break

    win.close()


main()

