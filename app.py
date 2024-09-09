#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

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
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines
    visualization = st.sidebar.selectbox("Choose a Visualization", ["Main Dashboard", "Product Type Analytics", "ABC Analysis", "Supplier Analytics", 
                                                               "Shipping Analytics",])


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
def make_donut(input_df, input_metric,):
    metric = input_df.mean()
    input_response = round(metric, 2)
    if input_response > .2:
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
        st.write('Defect Rate')
        donut_chart = make_donut(df['Defect rates'], 'Defect Rate')
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






#######################



# Product Type Analytics
elif visualization == "Product Type Analytics":
    st.title("Product Type Analytics")
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines  
    col = st.columns((1, 1, 1), gap='medium')

    with col[0]:
            #Number of products sold by Product Type
            pr_num_tot = df.groupby('Product type')['Number of products sold'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Product type'], 
                                y=pr_num_tot['Number of products sold']))
            fig.update_layout(title='Number of products sold by Product Type', 
                            xaxis_title='Product Type', 
                            yaxis_title='Number of products sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Sales Volume by Product Type
            pr_num_per = df.groupby('Product type')['Number of products sold'].sum().reset_index()
            pie_chart = px.pie(pr_num_per, values='Number of products sold', names='Product type', 
                        title='Sales Volume by Product Type', 
                        hover_data=['Number of products sold'],
                        hole=0.6,
                        color_discrete_sequence=px.colors.qualitative.Pastel)

            pie_chart.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(pie_chart)


    with col[1]:
            #Average Price by Product Type
            pr_pri = df.groupby('Product type')['Price'].mean().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=pr_pri['Product type'], 
                                y=pr_pri['Price']))
            fig.update_layout(title='Average Price by Product Type', 
                            xaxis_title='Product Type', 
                            yaxis_title='Average Price')
            st.plotly_chart(fig)

    with col[2]:
            #Revenue generated by Product Type
            pr_rev_tot = df.groupby('Product type')['Revenue generated'].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=pr_rev_tot['Product type'], 
                                y=pr_rev_tot['Revenue generated']))
            fig.update_layout(title='Revenue generated by Product Type', 
                            xaxis_title='Product Type', 
                            yaxis_title='Revenue generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Revenue Percentage by Product Type
            pr_rev_per = df.groupby('Product type')['Revenue generated'].sum().reset_index()
            pie_chart = px.pie(pr_rev_per, values='Revenue generated', names='Product type', 
                        title='Revenue Percentage by Product Type', 
                        hover_data=['Revenue generated'],
                        hole=0.6,
                        color_discrete_sequence=px.colors.qualitative.Pastel)

            pie_chart.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(pie_chart)
    
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines

    #Customer Demographics by Product Type
    pr_cos = pd.crosstab(df['Product type'], df['Customer demographics'])
    pr_cos = pr_cos.reset_index()

    melted_df = pd.melt(pr_cos, id_vars=['Product type'], 
                        var_name='Customer demographics', 
                        value_name='Count')
    fig = px.pie(melted_df, values='Count', names='Customer demographics', 
             facet_col='Product type', 
             title='Customer Demographics Distribution by Product Type',
             hole=0.6,
             color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)





#######################




elif visualization == "ABC Analysis":
    st.title("ABC Analysis")
    st.write("Under Development")





#######################



#Supplier Analytics
elif visualization == "Supplier Analytics":
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines  
    col = st.columns((1, 1, 1), gap='medium')

    with col[0]:
            #Number of products sold
            pr_num_tot = df.groupby('Supplier name')['Number of products sold'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Supplier name'], 
                                y=pr_num_tot['Number of products sold']))
            fig.update_layout(title='Number of Products Sold by Supplier', 
                            xaxis_title='Supplier', 
                            yaxis_title='Number of products sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #


    with col[1]:
            #Revenue generated
            pr_num_tot = df.groupby('Supplier name')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Supplier name'], 
                                y=pr_num_tot['Revenue generated']))
            fig.update_layout(title='Revenue Generated by Supplier', 
                            xaxis_title='Supplier', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

    with col[2]:
            #Manufacturing Lead Time
            pr_num_tot = df.groupby('Supplier name')['Manufacturing lead time'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Supplier name'], 
                                y=pr_num_tot['Manufacturing lead time']))
            fig.update_layout(title='Manufacturing Lead Time by Supplier', 
                            xaxis_title='Supplier', 
                            yaxis_title='Manufacturing Lead Time')
            st.plotly_chart(fig)
    
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines


    #Defect Rate
    defect_by_supplier = df.groupby('Supplier name')['Defect rates'].mean().reset_index()

    # Sort suppliers by defect rate for better visualization
    defect_by_supplier = defect_by_supplier.sort_values('Defect rates', ascending=False)

    # Create a horizontal bar chart
    fig = px.bar(defect_by_supplier, 
                x='Defect rates', 
                y='Supplier name', 
                orientation='h', 
                title='Defect Rate by Supplier',
                labels={'Defect rates': 'Average Defect Rate', 'Supplier name': 'Supplier'},
                text='Defect rates')

    # Customize the layout
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_xaxes(tickformat='..2f}%')

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines

    #Product Type by Supplier
    pr_cos = pd.crosstab(df['Supplier name'], df['Product type'])
    pr_cos = pr_cos.reset_index()

    melted_df = pd.melt(pr_cos, id_vars=['Supplier name'], 
                        var_name='Product type', 
                        value_name='Count')
    fig = px.pie(melted_df, values='Count', names='Product type', 
             facet_col='Supplier name', 
             title='Product Type by Supplier',
             hole=0.6,
             color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)





#######################




elif visualization == "Shipping Analytics":
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines  
    col = st.columns((1, 1, 1, 1), gap='medium')

    with col[0]:
            #Number of products sold by Shipping Carrier
            pr_num_tot = df.groupby('Shipping carriers')['Number of products sold'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Shipping carriers'], 
                                y=pr_num_tot['Number of products sold']))
            fig.update_layout(title='Number of Products Sold by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='Number of Products Sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Number of products sold by Transportation modes
            pr_num_tot = df.groupby('Transportation modes')['Number of products sold'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Transportation modes'], 
                                y=pr_num_tot['Number of products sold']))
            fig.update_layout(title='Number of Products Sold by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Number of Products Sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Number of products sold by Routes
            pr_num_tot = df.groupby('Routes')['Number of products sold'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Routes'], 
                                y=pr_num_tot['Number of products sold']))
            fig.update_layout(title='Number of Products Sold by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Number of Products Sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

    with col[1]:
            #Revenue generated by Shipping Carrier
            pr_num_tot = df.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Shipping carriers'], 
                                y=pr_num_tot['Revenue generated']))
            fig.update_layout(title='Revenue Generated by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Revenue generated by Transportation modes
            pr_num_tot = df.groupby('Transportation modes')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Transportation modes'], 
                                y=pr_num_tot['Revenue generated']))
            fig.update_layout(title='Revenue Generated by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Revenue generated by Routes
            pr_num_tot = df.groupby('Routes')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Routes'], 
                                y=pr_num_tot['Revenue generated']))
            fig.update_layout(title='Revenue Generated by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

    with col[2]:
            #Shipping Times by Shipping Carrier
            pr_num_tot = df.groupby('Shipping carriers')['Shipping times'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Shipping carriers'], 
                                y=pr_num_tot['Shipping times']))
            fig.update_layout(title='Average Shipping Time by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='AverageShipping Time')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Shipping Costs by Transportation modes
            pr_num_tot = df.groupby('Transportation modes')['Shipping times'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Transportation modes'], 
                                y=pr_num_tot['Shipping times']))
            fig.update_layout(title='Average Shipping Time by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Average Shipping Time')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Shipping Times by Routes
            pr_num_tot = df.groupby('Routes')['Shipping times'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Routes'], 
                                y=pr_num_tot['Shipping times']))
            fig.update_layout(title='Average Shipping Time by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Average Shipping Time')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


    with col[3]:
            #Shipping Costs by Shipping Carrier
            pr_num_tot = df.groupby('Shipping carriers')['Shipping costs'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Shipping carriers'], 
                                y=pr_num_tot['Shipping costs']))
            fig.update_layout(title='Shipping Costs by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='Shipping Costs')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Shipping Costs by Transportation Modes
            pr_num_tot = df.groupby('Transportation modes')['Shipping costs'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Transportation modes'], 
                                y=pr_num_tot['Shipping costs']))
            fig.update_layout(title='Shipping Costs by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Shipping Costs')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Shipping Costs by Routes
            pr_num_tot = df.groupby('Routes')['Shipping costs'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tot['Routes'], 
                                y=pr_num_tot['Shipping costs']))
            fig.update_layout(title='Shipping Costs by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Shipping Costs')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

    #Defect Rate by Shipping Carrier
    defect_by_carrier = df.groupby('Shipping carriers')['Defect rates'].mean().reset_index()

    # Sort suppliers by defect rate for better visualization
    defect_by_supplier = defect_by_carrier.sort_values('Defect rates', ascending=False)

    # Create a horizontal bar chart
    fig = px.bar(defect_by_carrier, 
                x='Defect rates', 
                y='Shipping carriers', 
                orientation='h', 
                title='Defect Rate by Shipping Carrier',
                labels={'Defect rates': 'Average Defect Rate', 'Shipping carriers': 'Shipping Carriers'},
                text='Defect rates')

    # Customize the layout
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_xaxes(tickformat='..2f}%')

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines


    #Defect Rate by Transportation Modes
    defect_by_transport = df.groupby('Transportation modes')['Defect rates'].mean().reset_index()

    # Sort suppliers by defect rate for better visualization
    defect_by_transport = defect_by_transport.sort_values('Defect rates', ascending=False)

    # Create a horizontal bar chart
    fig = px.bar(defect_by_transport, 
                x='Defect rates', 
                y='Transportation modes', 
                orientation='h', 
                title='Defect Rate by Transportation Modes',
                labels={'Defect rates': 'Average Defect Rate', 'Transportation modes': 'Transportation Modes'},
                text='Defect rates')

    # Customize the layout
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_xaxes(tickformat='..2f}%')

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines

    #Product Type by Shipping Carrier
    pr_cos = pd.crosstab(df['Shipping carriers'], df['Product type'])
    pr_cos = pr_cos.reset_index()

    melted_df = pd.melt(pr_cos, id_vars=['Shipping carriers'], 
                        var_name='Product type', 
                        value_name='Count')
    fig = px.pie(melted_df, values='Count', names='Product type', 
             facet_col='Shipping carriers', 
             title='Product Type by Shipping Carrier',
             hole=0.6,
             color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)

    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines

    #Product Type by Transportation Modes
    pr_cos = pd.crosstab(df['Transportation modes'], df['Product type'])
    pr_cos = pr_cos.reset_index()

    melted_df = pd.melt(pr_cos, id_vars=['Transportation modes'], 
                        var_name='Product type', 
                        value_name='Count')
    fig = px.pie(melted_df, values='Count', names='Product type', 
             facet_col='Transportation modes', 
             title='Product Type by Transportation Modes',
             hole=0.6,
             color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)

    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines