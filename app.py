import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


def create_plot(df, x_axis, y_axis):
    # Set random seed for reproducible jitter
    np.random.seed(42)
    
    category_order = df['BLS Category'].unique()
    
    # Create a copy of the dataframe to add jitter
    plot_df = df.copy()
    
    # Add random jitter to both categorical axes
    # Convert categories to numeric values first
    x_categories = plot_df[x_axis].unique()
    
    # Define specific order for BWC Familiarity categories
    y_categories = [
        "Newcomers",
        "Moderately Aware",
        "Informed Users", 
        "Active Users",
    ]
    
    # Define specific order for MSI Adjacency categories
    x_categories = [
        "Far Adjacency",
        "Mid Adjacency",
        "Near Adjacency", 
        "Core Market"
    ]
    
    x_map = {cat: i for i, cat in enumerate(x_categories)}
    y_map = {cat: i for i, cat in enumerate(y_categories)}
    
    # Convert categories to numbers and add jitter
    plot_df['x_jittered'] = plot_df[x_axis].map(x_map) + np.random.normal(0.1, 0.15, len(plot_df))
    plot_df['y_jittered'] = plot_df[y_axis].map(y_map) + np.random.normal(0.1, 0.15, len(plot_df))
    
    fig = px.scatter(
        plot_df,
        x='x_jittered',
        y='y_jittered',
        size="Employment",
        size_max=40,
        color="BLS Category",
        category_orders={"BLS Category": list(category_order) + ['Reference Bubble']},
        custom_data=['Occupation', x_axis, y_axis, 'Employment', 'Form Factor'],
        title="BWC Familiarity of Occupation vs MSI Adjacency to Occupation by BLS Category",
        labels={
            'BLS Category': 'Occupational Category',
            'Employment': 'Total Employment',
            'x_jittered': 'MSI Adjacency to Occupation',
            'y_jittered': 'BWC Familiarity of Occupation'
        }
    )
    
    # Customize hover template with ordered fields
    fig.update_traces(
        hovertemplate=(
            "<b>Occupation:</b> %{customdata[0]}<br>"
            "<b>Employment:</b> %{customdata[3]:,.0f}<br>"
            "<b>MSI Adjacency:</b> %{customdata[1]}<br>"
            "<b>BWC Familiarity:</b> %{customdata[2]}<br>"
            "<b>Form Factor:</b> %{customdata[4]}<br>"
            "<extra></extra>"  # This removes the secondary box in the hover
        )
    )

    # Add vertical and horizontal lines for category boundaries
    for i in range(len(x_categories) - 1):
        fig.add_vline(x=i + 0.5, line_dash="dash", line_color="gray", opacity=0.5)
    for i in range(len(y_categories) - 1):
        fig.add_hline(y=i + 0.5, line_dash="dash", line_color="gray", opacity=0.5)

    # Update axes to remove all grid lines
    fig.update_xaxes(
        ticktext=list(x_categories),
        tickvals=list(range(len(x_categories))),
        showgrid=False,
        zeroline=False  # Remove zero line
    )
    fig.update_yaxes(
        ticktext=list(y_categories),  # Use ordered categories
        tickvals=list(range(len(y_categories))),
        showgrid=False,
        zeroline=False  # Remove zero line
    )

    fig.update_layout(
        width=1200,
        height=800,
        title_font_size=16,
        showlegend=True,
        legend=dict(
            orientation="h",
            title=None,
        ),
        # plot_bgcolor='white',  # Make plot background white
        # paper_bgcolor='white'  # Make paper background white
    )

    return fig

def main():
    st.set_page_config(layout="wide")
    
    st.title("Occupation Familiarity Analysis")
    
    # Load data
    df = pd.read_csv('data/familiarity_form_factor_final.csv')
    
    # Basic description
    st.markdown("""
    This dashboard shows the relationship between MSI Adjacency and BWC Familiarity across different occupational categories.
    The size of each bubble represents the employment numbers in that occupation.
    """)
    
    # Add metrics explanation in a collapsible container
    with st.expander("Understanding the Metrics"):
        st.markdown("""
        ### BWC Familiarity of Occupation:  
        Measures how familiar an occupation is with Body-Worn Camera technology:
        - **Active Users**: High familiarity or awareness, and perhaps already using BWCs
        - **Informed Users**: High familiarity or awareness, even if not a current user
        - **Moderately Aware**: Moderate familiarity or awareness, but not a current user
        - **Newcomers**: Low familiarity or awareness, not a current user
        
        ### MSI Adjacency to Occupation:  
        Indicates Motorola Solutions' familiarity with the occupation's market segment:
        - **Core Market**: Motorola Solutions is already serving this market
        - **Near Adjacency**: Motorola Solutions is familiar with this market through industry trends, research, or adjacent fields
        - **Mid Adjacency**: Motorola Solutions is potentially familiar with this market, but not currently serving
        - **Far Adjacency**: Motorola Solutions is not familiar with this market, and not currently serving
                    
        ### Form Factor:  
        Indicates the form factor need for the occupation:
        - **High Need**: Significantly impacts functionality
        - **Moderate Need**: Beneficial but not critical to core functionality
        - **Low Need**: Size and shape is irrelevant to the purpose
        """)
    

    # Add multiselect for Form Factor filtering
    form_factor_options = ['High Need', 'Moderate Need', 'Low Need']
    selected_form_factors = st.multiselect(
        'Filter by Form Factor Need:',
        options=form_factor_options,
        default=form_factor_options  # Initially show all
    )
    
    # Filter the dataframe based on selection
    if selected_form_factors:
        df = df[df['Form Factor'].isin(selected_form_factors)]

    st.markdown("""
    Each point represents an individual occupation, colored by its BLS Category.
    Hover over points to see specific occupation details.
    """)
    st.plotly_chart(create_plot(df, y_axis='BWC Familiarity of Occupation', x_axis='MSI Adjacency to Occupation'), use_container_width=True)
        

if __name__ == "__main__":
    main()
