from tkinter import *
from tkinter import messagebox
from prettytable import PrettyTable
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import math

root = Tk()
root.geometry("1500x700")
root.title("PROFIT AND LOSS")
bg = PhotoImage(file="bep index.png")

canvas = Canvas(root, width=1600, height=300)
canvas.pack(fill=BOTH, expand=True)
# Add Image inside the Canvas
canvas.create_image(0, 0, image=bg, anchor='nw')


# Function to resize the window
def resize_image(e):
  global image, resized, image2
  # open image to resize it
  image = Image.open("bep index.png")
  # resize the image with width and height of root
  resized = image.resize((e.width, e.height), Image.LANCZOS)
  image2 = ImageTk.PhotoImage(resized)
  canvas.create_image(0, 0, image=image2, anchor='nw')


# Bind the function to configure the parent window
root.bind("<Configure>", resize_image)
# Create a canvas to display the animated text
text_canvas = Canvas(root,
                     width=1600,
                     height=70,
                     highlightthickness=0,
                     bd=0,
                     bg="lightpink")
text_canvas.place(relx=0, rely=0, anchor=NW)
# Define the text to be animated and create a text object on the canvas
text = text_canvas.create_text(400,
                               50,
                               text="Break Even Analysis",
                               font=("Arial", 20, "bold"),
                               fill="maroon")


def animate():
  x, y = text_canvas.coords(text)
  text_canvas.move(text, 5, 0)
  if x > text_canvas.winfo_width():
    text_canvas.coords(text, -200, y)
  root.after(50, animate)


animate()


def open():
  global fixed_cost_label, variable_cost_label, sales_price_label, units_label, product_label, result_label
  global F, V, P, N

  def submit():
    F = float(fixed_cost_entry.get())
    V = float(variable_cost_entry.get())
    P = float(sales_price_entry.get())
    N = int(units_entry.get())
    table = PrettyTable(["Star", "UNITS", "TC", "TR", "TP/TL", "P/L"])
    result_text.insert(END, "Star\tUNITS\tTC\tTR\tTPorTL\tPorL\n")
    result_text.insert(END, "-" * 90 + "\n")
    if (N % 25 == 0):
      k = N // 25
    else:
      for k in range(1, 25):
        if ((k * N) % 25 == 0):
          t = k * N // 25
          break
    for i in range(1, (N + 1), k):
      C = F + V * i
      P_ = i * P
      profit = P_ - C
      profit_per_unit = profit // i
      B_E_P = math.ceil((F / (P - V)))
      if (profit_per_unit == 0):
        star = " "
      else:
        if (B_E_P == i):
          star = "*"
          #continue
        elif ((abs(B_E_P - i) == k)):
          star = "*"
        elif ((i > B_E_P) and ((i - B_E_P) <= k)):
          star = "*"
        else:
          star = " "
      if profit >= 0:
        # set the foreground color to green
        result_text.tag_config("green", foreground="green")
        table.add_row([
          star,
          i,
          C,
          P_,
          profit,
          f"{profit_per_unit:.2f}",
        ])
        row = table._rows[-1]
        for cell in row:
          if cell == profit:
            result_text.insert(END, cell, "green")
          else:
            result_text.insert(END, cell)
          result_text.insert(END, "\t")
        result_text.insert(END, "\n")
      else:
        # set the foreground color to red
        result_text.tag_config("red", foreground="red")
        table.add_row([star, i, C, P_, profit, f"{profit_per_unit:.2f}"])
        row = table._rows[-1]
        for cell in row:
          if cell == profit:
            result_text.insert(END, cell, "red")
          else:
            result_text.insert(END, cell)
          result_text.insert(END, "\t")
        result_text.insert(END, "\n")
      table.add_row([star, i, C, P_, profit, profit_per_unit])
    product = product_entry.get()
    messagebox.showinfo("Break Even Analysis Results",
                        f"Product Name: {product}\nBreak Even Point: {B_E_P}")
    messagebox.showinfo(
      "NOTE",
      "* SHOULD BE PRINTED NEAR TO THE BREAKEVEN POINT\nIN THE TABLE\nTC = TOTAL COST\nTR = TOTAL REVENUE\nTP/TL = TOTAL PROFIT/TOTAL LOSS\nP/L = PROFIT/LOSS PER UNIT\n"
    ) 
        
  top = Toplevel()
  top.title("Break Even Analysis")
  top.geometry("1600x1600")
  top.configure(bg="lightblue")
  menubar = Menu(top)
  top.config(menu=menubar)

  def open_pl_window():
    pl_window = Toplevel(root)
    pl_window.title("Profit and Loss Window")
    pl_window.geometry("1600x1600")
    pl_window.configure(bg="lightblue")
    #pl_window.resizable(False,False)
    global F, V, P, N

    def graph():
      F = float(fixed_cost_entry.get())
      V = float(variable_cost_entry.get())
      P = float(sales_price_entry.get())
      N = int(units_entry.get())

      x = range(1, N)
      y = [P * i - (F + V * i) for i in x]
      plt.plot(x, y)
      plt.xlabel("Number of Units Sold")
      plt.ylabel("Profit/Loss")
      plt.axhline(y=0, color='r', linestyle='-')
      plt.text(x[10],
               0,
               "Break Even Point",
               ha='left',
               va='bottom',
               color='red')
      plt.title("Break Even Analysis")
      plt.show()
      exit_bn = Button(pl_window,
                       text="exit",
                       command=pl_window.destroy,
                       bg="coral")
      exit_bn.pack()

    txt = '''\n\nThis function calculates and displays a graph of the profit and loss\n based on the user input values:\n fixed operating cost(F)\n variable cost per unit(V)\n sales price per unit(P)\n and number of units sold(N)\n\n The graph shows the Break-Even point \nwhere the profit and loss is zero,\n indicated by a horizontal red line\n\n Click on the Graph to start the analysis'''
    profit_label = Label(pl_window,
                         text="This is the Profit and Loss window",
                         font=("times", 15, "bold italic"),
                         bg="lightblue")
    txt_label = Label(pl_window,
                      text=txt,
                      bg="light blue",
                      fg="purple",
                      font=("times", 15, "italic"))
    profit_label.pack()
    txt_label.pack()
    my_button = Button(pl_window,
                       text="Graph",
                       fg="white",
                       bg="Salmon",
                       command=graph)
    my_button.pack()

  def open_about_window():
    abt_window = Toplevel(root)
    abt_window.title("About Window")
    abt_window.geometry("1600x1600")
    abt_window.configure(bg="lightblue")
    #abt_window.resizable(False, False)
    txt1 = '''\n\nInputs needed to be given by the user:'''
    txt2 = '''* Fixed Operating Cost(F): The actual cost that does not change with an increase \n or decrease in the number of goods
    * Variable Operating Cost(V): The cost that changes with the amount of output produced. 
    * Sales per Unit(P): The cost of a unit product
    * Range(N): number of units of  product to be considered
    * Product Name: Name of the product produced'''

    txt3 = '''Outputs produced: '''
    txt4 = '''* Star: This symbol is used to show the equidistant profit and losses or the profit if not equidistant
    * UNITS: No.of untis of the product to be considered
    * TC: Total cost( F +V *N)
    * TR: Total revenue obtained by the firm(P * N)
    * TPorTL:Total profit or Total loss obtained for the range of units\n(red colour represents losses obtained \n green colour represents the profits obtained by the firm)
    * PorL: Profit or Loss of the respective unit of the product
'''
    abt_label = Label(abt_window,
                      text="This is the about window",
                      font=("times", 13, "bold italic"),
                      bg="lightblue")
    abt_txt1 = Label(abt_window,
                     text=txt1,
                     bg="light blue",
                     font=("times", 13, "bold italic"))
    abt_txt2 = Label(abt_window,
                     text=txt2,
                     bg="light blue",
                     fg="purple",
                     font=("times", 13, "bold italic"))
    abt_txt3 = Label(abt_window,
                     text=txt3,
                     bg="light blue",
                     font=("times", 13, "bold italic"))
    abt_txt4 = Label(abt_window,
                     text=txt4,
                     bg="light blue",
                     fg="purple",
                     font=("times", 13, "bold italic"))
    abt_label.pack()
    abt_txt1.pack()
    abt_txt2.pack()
    abt_txt3.pack()
    abt_txt4.pack()
    exit_btn = Button(abt_window,
                      text="Exit",
                      command=abt_window.destroy,
                      bg="coral")
    exit_btn.pack()

  def graph_window():
    grph_window = Toplevel(root)
    grph_window.title("Break Even Point Graph")
    grph_window.geometry("1600x1600")
    grph_window.configure(bg="lightblue")
    #grph_window.resizable(False,False)
    global F, V, P, N, B_E_P

    def graph1():
      F = float(fixed_cost_entry.get())
      V = float(variable_cost_entry.get())
      P = float(sales_price_entry.get())
      N = int(units_entry.get())
      B_E_P = math.ceil((F / (P - V)))

      x = range(1, N)
      y1 = [F + (V * i) for i in x]
      y2 = [P * i for i in x]
      plt.scatter(x, y1, label='Revenue')
      plt.scatter(x, y2, label='Cost')
      plt.legend(loc='upper right')
      plt.axvline(x=B_E_P,
                  linestyle='--',
                  color='gray',
                  label='Break Even Point')
      plt.text(B_E_P - 5,
               F + (V * B_E_P),
               "Break Even Point",
               ha='right',
               va='bottom',
               color='gray')
      plt.xlabel("Number of Units Sold")
      plt.ylabel("Revenue")
      plt.title("Break Even Analysis")
      plt.show()
      exit_button = Button(grph_window,
                           text="exit",
                           command=grph_window.destroy,
                           bg="coral")
      exit_button.pack()

    graph_label = Label(grph_window,
                        text="This is the Graph window",
                        font=("times", 15, "bold italic"),
                        bg="lightblue")
    graph_label.pack()
    tt = '''
      This function calculates and displays a graph of the  Break Even Point\n based on user input values:\n fixed cost (F)\n variable cost (V)\n sales price (P)\n numberof units sold (N)\n\n
      The Break Even Point is plotted as a vertical line\n on the graph at x=B_E_P,\n and a legend is added to indicate the Revenue and Cost.\n\nclick the graph to start the analysis'''
    text6_label = Label(grph_window,
                        text=tt,
                        font=("times", 15, "bold italic"),
                        fg="purple",
                        bg="light blue")
    text6_label.pack()

    my_button1 = Button(grph_window,
                        text="Graph",
                        command=graph1,
                        fg="white",
                        bg="salmon")
    my_button1.pack()


# Create a file menu

  filemenu = Menu(menubar, tearoff=0)
  filemenu.add_command(label="Profit/loss", command=open_pl_window)
  filemenu.add_command(label="break-even graph", command=graph_window)
  filemenu.add_separator()
  filemenu.add_command(label="Exit", command=top.destroy)
  menubar.add_cascade(label="File", menu=filemenu)

  # Create a help menu
  helpmenu = Menu(menubar, tearoff=0)
  helpmenu.add_command(label="About...", command=open_about_window)
  menubar.add_cascade(label="Help", menu=helpmenu)

  fixed_cost_label = Label(top,
                           text="Fixed Operating Cost:",
                           fg="Teal",
                           bg="lightblue",
                           font=("times", 15))
  fixed_cost_entry = Entry(top, width=10)
  fixed_cost_label.grid(row=0, column=0)
  fixed_cost_entry.grid(row=0, column=1)
  fixed_cost_entry.configure(bg="lightpink")

  variable_cost_label = Label(top,
                              text="Variable Cost per Unit:",
                              fg="Teal",
                              bg="lightblue",
                              font=("times", 15))
  variable_cost_entry = Entry(top, width=10)
  variable_cost_label.grid(row=1, column=0)
  variable_cost_entry.grid(row=1, column=1)
  variable_cost_entry.configure(bg="lightpink")

  sales_price_label = Label(top,
                            text="Sales Price per Unit:",
                            fg="Teal",
                            bg="lightblue",
                            font=("times", 15))
  sales_price_entry = Entry(top, width=10)
  sales_price_label.grid(row=2, column=0)
  sales_price_entry.grid(row=2, column=1)
  sales_price_entry.configure(bg="lightpink")
  units_label = Label(top,
                      text="Units to be Considered:",
                      fg="Teal",
                      bg="lightblue",
                      font=("times", 15))
  units_entry = Entry(top, width=10)
  units_label.grid(row=3, column=0)
  units_entry.grid(row=3, column=1)
  units_entry.configure(bg="lightpink")

  product_label = Label(top,
                        text="Product Name:",
                        fg="Teal",
                        bg="lightblue",
                        font=("times", 15))
  product_entry = Entry(top, width=30)
  product_label.grid(row=4, column=0)
  product_entry.grid(row=4, column=1)
  product_entry.configure(bg="lightpink")

  calculate_button = Button(top,
                            text="Submit",
                            bg="coral",
                            fg="white",
                            command=submit)
  calculate_button.grid(row=5, column=0)

  result_label = Label(top,
                       text="Results:",
                       fg="Teal",
                       bg="lightblue",
                       font=("times", 15))
  result_label.grid(row=6, column=0)
  result_text = Text(top, width=100, height=50)
  result_text.grid(row=7, column=1)
  result_text.configure(bg="lemon chiffon")

btn = Button(root, text="Lets Go", fg="yellow", bg="Navy", command=open)
btn.pack(side=BOTTOM)
btn1 = canvas.create_window(10, 10, anchor="nw", window=btn)

mainloop()
