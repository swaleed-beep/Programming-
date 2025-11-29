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


    # Label for file entry
    file_label = Text(Point(80, 90), "CSV file:")
    file_label.draw(win)

    # Entry box for file name
    file_entry = Entry(Point(240, 90), 25)  # center x=240, width=25 chars
    file_entry.setText("matches.csv")       # default suggestion
    file_entry.draw(win)

    # Load CSV button (rectangle + text)
    load_rect = Rectangle(Point(360, 70), Point(460, 110))
    load_rect.setFill("lightgray")
    load_rect.draw(win)
    load_text = Text(load_rect.getCenter(), "Load CSV")
    load_text.draw(win)

    # Status message at the bottom
    status = Text(Point(250, 250), "Status: Waiting...")
    status.draw(win)

    # We'll store loaded rows here
    rows = None

    # Event loop
    while True:
        click_point = win.getMouse()

        # If user clicks inside the Load CSV button
        if clicked(load_rect, click_point):
            filename = file_entry.getText().strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    rows = [row for row in reader]
                status.setText(f"Status: Loaded {len(rows)} rows from {filename}")
            except:
                status.setText("Status: ERROR - could not open file")

        # Simple way to exit: click in bottom-right corner area
        if click_point.x > 450 and click_point.y > 260:
            break

    win.close()

main()
