"""
Name:       Ezra Hamoui
CS230:      Section 6
Data:       Parking_Meters.csv
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program ... (a few sentences about your program and the queries and charts)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

st.set_page_config(page_title="Parking Meters",
                   page_icon=":car:")


def read_data():
    df = pd.read_csv("/Users/zury/PycharmProjects/pythonProject/FINAL PROJECT/Parking_Meters.csv")

    # Group by street
    df['STREET'] = df['STREET'].str.extract(r'([^\d]+) ST')

    return df


def filter_data(selected_streets, selected_blok, selected_direction, selected_vendors):
    df = read_data()

    if selected_streets:
        df = df.loc[df['STREET'].isin(selected_streets)]

    if selected_blok is not None:
        df = df.loc[df['BLK_NO'] == selected_blok]

    if selected_direction:
        if selected_direction == 'NORTH':
            df = df.loc[df['DIR'] == 'N']
        elif selected_direction == 'SOUTH':
            df = df.loc[df['DIR'] == 'S']
        elif selected_direction == 'EAST':
            df = df.loc[df['DIR'] == 'E']
        elif selected_direction == 'WEST':
            df = df.loc[df['DIR'] == 'W']
        elif selected_direction == 'ALL DIRECTIONS':
            pass

    if selected_vendors:
        # filter vendors
        if selected_vendors == 'BOTH':
            pass
        else:
            df = df.loc[df['VENDOR'] == selected_vendors]

    return df


def all_streets():
    df = read_data()
    df = df['STREET'].unique()
    return df


def all_bloks():
    df = read_data()
    df = df['BLK_NO'].unique()
    return df


def all_directions():
    # A list comprehension
    dir = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'ALL DIRECTIONS']
    return dir


def all_vendors():
    # A list comprehension
    dir = ['IPS', 'BOTH', 'Parkeon']
    return dir


def generate_map(df):
    map_df = df.filter(['STREET', 'LATITUDE', 'LONGITUDE'])

    view_state = pdk.ViewState(
        latitude=map_df['LATITUDE'].mean(),
        longitude=map_df['LONGITUDE'].mean(),
        zoom=16,
    )
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=map_df,
        get_position=['LONGITUDE', 'LATITUDE'],
        get_color=[20, 175, 250],
        get_radius=5,
        pickable=True
    )
    tool_tip = {
        'html': 'STREET: <b>{STREET}</b>',
        'style': {'backgroundColor': 'grey', 'color': 'white'}
    }
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tool_tip

    )

    st.pydeck_chart(map, use_container_width=True)


def generate_pie_chart(df):
    df = df['STREET'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(df, labels=df.index, autopct='%1.1f%%')
    ax.axis('equal')
    # title
    ax.set_title('Streets')
    # legend
    ax.legend(df.index, loc="upper right")
    st.pyplot(fig)


def generate_bar_chart(df):
    df = df['VENDOR'].value_counts()
    fig, ax = plt.subplots()

    colormap = plt.cm.get_cmap('viridis', len(df))
    bars = ax.bar(df.index, df, color=colormap(range(len(df))))

    plt.xticks(range(len(df.index)), df.index, rotation=30)

    # set label
    ax.set_xlabel('Vendor')
    ax.set_ylabel('Total')

    # title
    ax.set_title('Vendors')
    # legend
    ax.legend(bars, df.index, loc="upper right")

    st.pyplot(fig)


def generate_line_chart(df):
    df = df['STREET'].value_counts()

    fig, ax = plt.subplots()
    ax.plot(df.index, df, marker='o')

    plt.xticks(range(len(df.index)), df.index, rotation=30)

    ax.set_xlabel('Street')
    ax.set_ylabel('Total')
    ax.set_title('STREET')
    st.pyplot(fig)


def main():
    st.image("/Users/zury/PycharmProjects/pythonProject/FINAL PROJECT/cover.png", width=200)
    st.title("Parking Meters")

    # sidebar
    st.sidebar.write("Please choose option to display data")

    # default value
    selected_streets = ['NEWBURY', 'BROAD']
    selected_blok = ''
    selected_directions = ['NORTH', 'SOUTH']

    # multiselect street
    selected_streets = st.sidebar.multiselect(
        "Select Streets",
        all_streets(),
        default=selected_streets
    )

    # selectbox block
    selected_blok = st.sidebar.selectbox(
        "Select Block",
        all_bloks(),
        index=None,
    )

    # radio direction
    selected_directions = st.sidebar.radio(
        "Select Directions",
        all_directions()
    )

    # slider vendor
    selected_vendors = st.sidebar.select_slider(
        "Select Vendors",
        all_vendors()
    )

    # filter data
    data = filter_data(selected_streets, selected_blok,
                       selected_directions, selected_vendors)

    # display data
    if selected_streets or selected_blok or selected_directions:
        # display table
        st.subheader("Table Data")
        st.dataframe(data)

        # display map
        st.subheader("Parkings Map")
        generate_map(data)

        # display pie chart
        st.subheader("Street Percentage Pie Chart")
        generate_pie_chart(data)

        # display bar chart
        st.subheader("Vendors Bar Chart")
        generate_bar_chart(data)

        # display area chart
        st.subheader("Streets Quantity Line Chart")
        generate_line_chart(data)


main()
