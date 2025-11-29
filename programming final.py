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
    file_label = Text(Point(87, 50), "CSV file")
    file_label.draw(win)

    # Entry box for file name (left side)
    file_entry = Entry(Point(87, 70), 10)  # centre x=180
    file_entry.setText("mydata.csv")        # default suggestion
    file_entry.draw(win)

    # LEFT button: load CSV from what the user typed
    load_rect_left = Rectangle(Point(55, 80), Point(110, 110))
    load_rect_left.setFill("lightgray")
    load_rect_left.draw(win)
    load_text_left = Text(load_rect_left.getCenter(), "Load ")
    load_text_left.draw(win)

    # RIGHT button: always load matches.csv
    load_rect_right = Rectangle(Point(200, 60), Point(360, 80))
    load_rect_right.setFill("lightgray")
    load_rect_right.draw(win)
    load_text_right = Text(load_rect_right.getCenter(), "Load Matches.csv")
    load_text_right.draw(win)

    # ---- Status text ----
    status = Text(Point(250, 250), "Status: Waiting...")
    status.draw(win)

    # We'll store loaded rows here
    rows = None

    # Event loop
    while True:
        click_point = win.getMouse()
        while True:
            click_point = win.getMouse()

            # LEFT button: load CSV typed in entry
            if clicked(load_rect_left, click_point):
                filename = file_entry.getText().strip()
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        rows = [row for row in reader]
                    status.setText(f"Status: Loaded {len(rows)} rows from {filename}")
                except:
                    status.setText("Status: ERROR - could not open file")

            # RIGHT button: always load matches.csv
            if clicked(load_rect_right, click_point):
                try:
                    with open("Matches.csv", "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        rows = [row for row in reader]
                        headers = reader.fieldnames
                    status.setText(f"Status: Loaded {len(rows)} rows from matches.csv")
                except:
                    status.setText("Status: ERROR - could not open matches.csv")

            # Exit condition (bottom-right click)
            if click_point.x > 450 and click_point.y > 260:
                break

    win.close()


main()

