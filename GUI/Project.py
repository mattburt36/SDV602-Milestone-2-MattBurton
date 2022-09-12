"""
Ukrainian food price application
Designer: Matthew Burton 
Begin Date: 01/08/2022
End Date: N/A

This is my application for NMIT Semester 2 of 2022, SDV602 class tutored by Todd Cochrane. 
The intention of this application is to track the prices of food in the war torn country of the Ukraine. I do not personally agree with any form of war, I am just studying the effects
on the people in different areas of the Ukraine that are affected by the war. 

This application may take a dataset of any country and produce results to be displayed graphically on the prices of items, in the future I aim to make this application have the ability 
to adapt to different countries and different options datasets allow. 

This application's current state is a test state, having completed the skeleton and inserted test data to display on a graph inside of a GUI, in future it will work with a dataset 
provided to display actual food price records and a secondary dataset to convert currencies accurately

The application uses the libraries:
    - PySimpleGUI   (For layout and presentation of windows in graphical user interface)
    - Matplotlib    (For layout of graphs to insert into the windows generated by PySimpleGUI)
    - Tkinter       (To generate message boxes to display errors or unexpected results)

Enjoy! 
"""
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set the theme for the application 
sg.theme('DarkTeal10')

# Some test data 
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
prices = [15, 17, 19, 20, 16, 19, 22, 40, 45]

def generate_layout():
    """
    This function works as a state machine which returns a different object of "layout" for creating a screen based on the value of "window_flag",
    this allows the application to 're-use' layouts 
    """
    if window_flag == 0:
        layout = [
                    [sg.Text("Hello, welcome to the Ukrainian food price tracking application")],
                    [sg.Text("Please enter your login details")],
                    [sg.Text('Username'), sg.InputText(size=(20,1))],
                    [sg.Text('Password'), sg.InputText(size=(20,1), password_char="*")],
                    [sg.Submit(button_text="Login"), sg.Cancel(button_text="Exit")]
                ]
    elif window_flag == 1:        
        MainScreenColumn1 = [
                                [sg.Text("Region")],
                                [sg.Combo(["Kyiv","Dnipropetrovsk","Donetsk","Kharkiv","Kherson","Odesa","Sevastopol","Sumy","Zaporizhzhya"],default_value="Kyiv",size=(30,1))],
                                [sg.Text("Beginning date")],
                                [sg.Combo(["2014","2015","2016","2017","2018","2019","2020","2021","2022"],default_value="2014",size=(30,1))],
                                [sg.Text("Ending date")],
                                [sg.Combo(["2014","2015","2016","2017","2018","2019","2020","2021","2022"],default_value="2022",size=(30,1))],
                                [sg.Text("Currency")],
                                [sg.Combo(["NZD","USD","EUR","JPY","GBP","AUD","CAD","CHF","CNY","HKD","SEK","KRW","SGD","NOK","MXN","INR","RUB","ZAR","TRY","BRL","TWD","DKK","PLN","THB","IDR","HUF","CZK","ILS","CLP","PHP","AED","COP","SAR","MYR","RON"],default_value='NZD',size=(30,1))],
                                [sg.Text("Select foods below to display")],
                                [sg.Listbox(values=["Fuel(petrol)","Milk","Potatoes","Rice","Onions","Cabbage","Carrots","Beetroot","Apples","Sugar","Beef","Chicken","Fish","Pork","Eggs","Flour","Oil(sunflower)","Anti-biotics"], select_mode="multiple", key="food", size=(30,10))],
                                [sg.Button("Change graph")],
                                [sg.Button("Display region")]
                            ]
        MainScreenColumn2 = [   
                                # Graph goes here 
                                [sg.Canvas(size=(500, 300), key=("-CANVAS-"))]
                            ]
        layout = [
                                [sg.Column(MainScreenColumn1, element_justification='l'), sg.Column(MainScreenColumn2, element_justification='c')]
                            ]
    elif window_flag == 2:  
        layout = [ 
                                [sg.Button("Exit to main")],
                                [sg.Image(filename="Ukraine_map.png")]
                            ]

    return layout

def create_window():
    """
    Function for creating a screen based on the value of the 'window_flag' variable and the layout generated from 'generate_layout'
    """
    # First generate the object of the layout 
    layout = generate_layout()

    if window_flag == 0:
        # Center justify content, return the login screen 
        return sg.Window("Login", layout, element_justification='c')
    elif window_flag == 1:
        # Close any last screen populated and generate a new main screen 
        window.close()
        return sg.Window("Main", layout, size=(900,500), finalize=True)     
    elif window_flag == 2:
        # Generate the map screen 
        return sg.Window("Map", layout)

def create_plot(x, y, flag):
    """
    Function to plot graph values, switch between types of graph to be plotted 
    """
    # Dispose any past graphs that were plotted 
    plt.cla()

    # State machine to switch between bar graph plotting and line graph plotting 
    if flag == 0:
        plt.plot(x, y, color="blue", marker="o")
    elif flag == 1: 
        plt.bar(x,y,color="green")
        plt.plot()

    plt.title("Food prices")
    plt.xlabel("Year")
    plt.ylabel("Price ($)")
    plt.grid(True)
    return plt.gcf()

def draw_graph(canvas, figure):
    """
    Function to draw a graph 
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Set some initial conditions 
graph_flag = 0
window_flag = 0 
window = create_window()

if __name__ == "__main__":

    # Application's main event loop 
    while True:
        event, values = window.read()
        # For any state the machine is in, if the window is closed, exit the application entirely
        if event == sg.WIN_CLOSED:
            break
        # The system is in the login screen state, showing the first screen      
        if window_flag == 0:
            if event == "Exit":
                break
            if event == "Login":
                # check credentials, close last window, open the main screen
                window_flag = 1 
                window = create_window()
                draw_graph(window["-CANVAS-"].TKCanvas, create_plot(years, prices, graph_flag))
        # The system is in the main screen state, showing the secondarily generated screen  
        elif window_flag == 1:
            if event == "Change graph":
                # Switch the value of the graph that is plotted 
                if graph_flag == 0:
                    graph_flag = 1
                elif graph_flag == 1:
                    graph_flag = 0

                window = create_window()
                draw_graph(window["-CANVAS-"].TKCanvas, create_plot(years, prices, graph_flag))

            if event == "Display region":
                # Show map screen 
                # Keep the main screen open but not interactive 
                window_flag = 2
                window = create_window()
        # The system is in the map screen state, showing the thirdly generated screen  
        elif window_flag == 2:
            if event == "Exit to main" or event == sg.WIN_CLOSED():
                # Show the main screen
                window_flag = 1
                window = create_window()
                draw_graph(window["-CANVAS-"].TKCanvas, create_plot(years, prices, graph_flag))

    # Default state once conditions satisfied 
    window.close() 