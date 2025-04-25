from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context

"""
==========================================================================
Markdown Text
"""

datasource_text = dcc.Markdown(
    """
    [Data source:](https://www.kaggle.com/code/syedanwarafridi/mental-health-trends-in-the-age-of-social-media/input)
     A dataset from Kaggle and posted by Syed Anwar, a data scientist at Alpha Squad
    """
)

asset_allocation_text = dcc.Markdown(
    """
> **Asset allocation** is one of the main factors that drive portfolio risk and returns.   Play with the app and see for yourself!

> Change the allocation to cash, bonds and stocks on the sliders and see how your portfolio performs over time in the graph.
  Try entering different time periods and dollar amounts too.
"""
)

play_text = dcc.Markdown(
    """
> Use the inputs below to measure how your social media habits affect productivity-related traits like '
           'concentration, distraction, and sleep! 
> You will get some advice too!
"""
)

learn_text = dcc.Markdown(
    """
    The goal of this Project is to visually analyze the impact of social media on different stages of occupation status 
    such as University students, Salaried Workers and retired people. The visualizations examines if social media 
    has an effect on people's productivity on a scale of 1 to 5. It will also assess the type of social media's that 
    mostly increase or decrease one's productivity. Hope you enjoy the visualizations in the next tabs!
    
    This project was inspired by my boarding experience and also by a book that I am currently reading this semester 
    called “Think fast and slow” where the author navigates how our minds think and process information and how that 
    can be easily influenced and distracted by tools like social media. 

    """
)


footer = html.Div(
    dcc.Markdown(
        """
        © 2025 Nice Teta Hirwa - CS150 - Professor Mike Ryu | Data collected from survey responses   
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)
