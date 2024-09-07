#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Beauty Store Supply Chain",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
df = pd.read_csv('data/supply_chain_data.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('💄 Visualization Options')
    
    visualization = st.sidebar.selectbox("Choose a Visualization", ["Main Dashboard", "Product Type Analytics", "ABC Analysis", "Supplier Analytics", 
                                                               "Shipper Analytics", "Customer Analytics"])


#######################
# Plots

# Choropleth map
def make_choropleth(df):
    city_to_state = {
    'Kolkata': 'West Bengal',
    'Mumbai': 'Maharashtra',
    'Chennai': 'Tamil Nadu',
    'Bangalore': 'Karnataka',
    'Delhi': 'Delhi'}

    # Add the new 'State' column using the map function
    df['State'] = df['Location'].map(city_to_state)
    state_column = 'State'
    value_column = 'Revenue generated'
    # Group by state and sum the revenue
    state_revenue = df.groupby(state_column)[value_column].sum().reset_index()

    choropleth = px.choropleth(
        state_revenue,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        locations=state_column,
        featureidkey="properties.ST_NM",
        color=value_column,
        range_color=(0, state_revenue[value_column].max()),
        scope="asia",
        labels={value_column: 'Total Revenue Generated'}
    )

    choropleth.update_geos(
        fitbounds="locations",
        visible=True,
        resolution=50,
        showcoastlines=True,
        showsubunits=True,
        showland=True,
        showcountries=True,
        countrycolor="White",
        subunitcolor="White"
    )

    choropleth.update_layout(

        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )

    return choropleth


# Donut chart
def make_donut(input_df, input_metric):
    metric = input_df.mean()
    input_response = round(metric, 2)

    if input_response > 2:
        input_color = 'red'
    else:
        input_color = 'green'
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']
    
    source = pd.DataFrame({
        "Topic": ['', input_metric],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_metric],
        "% value": [100, 0]
    })
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_metric, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    text = plot.mark_text(align='center', color="#29b5e8", fontSize=26, fontStyle="italic").encode(text=alt.value(f'{input_response}%'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_metric, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text






#######################






# Dashboard Main Panel
if visualization == "Main Dashboard":
    st.title("Beauty Store Supply Chain Dashboard")
    col = st.columns((1, 4.5, 2), gap='medium')

    with col[0]:
        st.write('\n\n')  # Adds two empty lines
        st.write('\n\n')  # Adds two empty lines

        st.markdown('##### Key Metrics')
        
        st.write('\n\n')  # Adds two empty lines

        #Total Revenue
        total_revenue = df['Revenue generated'].sum()
        formatted_revenue = f"$ {total_revenue:,.0f}"
        st.metric(label = "Total Revenue", value = formatted_revenue, delta='$ 153,524')
                
        st.write('\n\n')  # Adds two empty lines
        
        #Products Sold
        product_sold = df['Number of products sold'].sum()
        formatted_product = f"{product_sold:,.0f}"
        st.metric(label = "Items Sold", value = formatted_product, delta='17,093')
                
        st.write('\n\n')  # Adds two empty lines

        #Average Lead Time
        avr_lead = df['Lead times'].mean()
        formatted_lead = f"{avr_lead:,.0f}"
        st.metric(label = "Average Lead Time (Days)", value = formatted_lead, delta='-3')
                
        st.write('\n\n')  # Adds two empty lines
        
        #Defect Rate
        st.write('Defect Rates')
        donut_chart = make_donut(df['Defect rates'], 'Defect Rates')
        st.altair_chart(donut_chart)

    with col[1]:
        st.write('\n\n')  # Adds two empty lines
        st.write('\n\n')  # Adds two empty lines

        st.markdown('<h5 style="text-align: center;">Supplier Geography by Revenue</h5>', unsafe_allow_html=True)
        
        choropleth = make_choropleth(df)
        st.plotly_chart(choropleth, use_container_width=True)

        st.write('\n\n')  # Adds two empty lines
        st.write('\n\n')  # Adds two empty lines
        st.write('\n\n')  # Adds two empty lines
        st.write('\n\n')  # Adds two empty lines

        with st.expander('About the Data', expanded=True):
            st.write('''
            - Data: [Beauty Startup Supply Chain Dataset](https://www.kaggle.com/datasets/amirmotefaker/supply-chain-dataset/data).
            - This dataset contains information about the supply chain of a beauty startup. It includes data about the products, suppliers, and customers.
            - The dataset is cleaned and ready for analysis.
            ''')

    with col[2]:
        st.write('\n\n')  # Adds two empty lines
        st.write('\n\n')  # Adds two empty lines

        st.markdown('##### Top Selling Products')

        st.dataframe(
            df.sort_values(by='Number of products sold', ascending=False),
            column_order=("SKU", "Number of products sold"),
            hide_index=True,
            width=None,
            column_config={
                "SKU": st.column_config.TextColumn(
                    "SKU",
                    ),
                    "Number of products sold": st.column_config.ProgressColumn(
                        "Number of products sold",
                        format="%f",
                        min_value=0,
                        max_value=max(df['Number of products sold']),
                        )}
                    )


elif visualization == "Product Type Analytics":
    st.title("Product Type Analytics")
    st.write("Under Development")

elif visualization == "ABC Analysis":
    st.title("ABC Analysis")
    st.write("Under Development")

elif visualization == "Supplier Analytics":
    st.title("Supplier Analytics")
    st.write("Under Development")

elif visualization == "Shipper Analytics":
    st.title("Shipper Analytics")
    st.write("Under Development")

elif visualization == "Customer Analytics":
    st.title("Customer Analytics")
    st.write("Under Development")