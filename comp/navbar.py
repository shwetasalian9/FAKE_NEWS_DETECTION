# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

# Defining the navbar structure
def Navbar():

    layout = html.Div(children=[
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Overview", href="/Overview", className="nav-bar nav-bar:hover nav-bar:active", )),
                dbc.NavItem(dbc.NavLink("TestNews", href="/TestNews", className="nav-bar nav-bar:hover nav-bar:active")) ],
                color="black",
                brand="News Detection App",
                brand_href="/Overview",
                dark = True,
                style = {"height": "120px"}
        )
    ])

    return layout