#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import itertools

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


        with st.expander('About the Developer', expanded=False):
            st.write('''
            - This Dashboard was developed by Abdullah Garatli''')

        st.write('\n\n')  # Adds two empty lines

        with st.expander('The Dataset', expanded=False):
            st.write(df)

        st.write('\n\n')  # Adds two empty lines

        with st.expander('About the Dataset', expanded=False):
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
            color_sequence = px.colors.qualitative.Vivid
            colors = list(itertools.islice(itertools.cycle(color_sequence), len(pr_num_tot)))
            fig = go.Figure()
            fig.add_trace(go.Bar(x=pr_num_tot['Product type'], 
                                y=pr_num_tot['Number of products sold'],
                                marker_color=colors,
                                name='Products Sold'))
            fig.update_layout(title='Products Sold by Product Type', 
                            xaxis_title='Product Type', 
                            yaxis_title='Products Sold')
            st.plotly_chart(fig)

            # Update layout if necessary
            fig.update_layout(
                legend_title_text='Product Type',
                xaxis_title='Product Type',
                yaxis_title='Number of Products Sold'
            )

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
            color_sequence = px.colors.qualitative.Vivid
            colors = list(itertools.islice(itertools.cycle(color_sequence), len(pr_pri)))
            fig = go.Figure()
            fig.add_trace(go.Bar(x=pr_pri['Product type'], 
                                y=pr_pri['Price'],
                                marker_color=colors,
                                name='Products Sold'))
            fig.update_layout(title='Average Price by Product Type', 
                            xaxis_title='Product Type', 
                            yaxis_title='Average Price')
            st.plotly_chart(fig)
    
    with col[2]:
            #Revenue generated by Product Type
            pr_rev_tot = df.groupby('Product type')['Revenue generated'].sum().reset_index()
            color_sequence = px.colors.qualitative.Vivid
            colors = list(itertools.islice(itertools.cycle(color_sequence), len(pr_rev_tot)))
            fig = go.Figure()
            fig.add_trace(go.Bar(x=pr_rev_tot['Product type'], 
                                y=pr_rev_tot['Revenue generated'],
                                marker_color=colors,
                                name='Products Sold'))
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



# ABC Analysis

elif visualization == "ABC Analysis":
    st.title("ABC Analysis")
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines  

    # Perform ABC Analysis
    total_revenue = df['Revenue generated'].sum()
    df_sorted = df.sort_values(by='Revenue generated', ascending=False)
    df_sorted['Cumulative Revenue'] = df_sorted['Revenue generated'].cumsum()
    df_sorted['Cumulative Revenue Percentage'] = 100 * df_sorted['Cumulative Revenue'] / total_revenue

    def assign_abc_category(percentage):
        if percentage <= 70:
            return 'A'
        elif percentage <= 90:
            return 'B'
        else:
            return 'C'

    df_sorted['ABC_category'] = df_sorted['Cumulative Revenue Percentage'].apply(assign_abc_category)

    # Compute Cumulative Percentage of Items
    df_sorted['Item Number'] = range(1, len(df_sorted) + 1)
    df_sorted['Cumulative Items Percentage'] = 100 * df_sorted['Item Number'] / len(df_sorted)

    # Sidebar Filters
    st.sidebar.header('🔎 Filters')

    # Filter by Product Type
    product_types = df['Product type'].unique()
    selected_product_types = st.sidebar.multiselect('Product Type', product_types, default=product_types)

    # Filter by ABC Category
    abc_categories = ['A', 'B', 'C']
    selected_abc_categories = st.sidebar.multiselect('ABC Category', abc_categories, default=abc_categories)

    # Apply Filters
    df_filtered = df_sorted[
        (df_sorted['Product type'].isin(selected_product_types)) &
        (df_sorted['ABC_category'].isin(selected_abc_categories))
    ]

    # Update Summary Data
    abc_summary_filtered = df_filtered.groupby('ABC_category').agg({
        'Revenue generated': 'sum',
        'Stock levels': 'sum'
    }).reset_index()

    abc_summary_filtered['Revenue Percentage'] = 100 * abc_summary_filtered['Revenue generated'] / df_filtered['Revenue generated'].sum()

    
    # Cumulative Percentage Curve Visualization

    # Actual Cumulative Curve
    actual_curve = df_sorted[['Cumulative Items Percentage', 'Cumulative Revenue Percentage']].copy()

    # Theoretical Curve Data
    theoretical_curve = pd.DataFrame({
        'Cumulative Items Percentage': [0, 20, 50, 100],
        'Cumulative Revenue Percentage': [0, 70, 90, 100]
    })

    # Ensure both 'Cumulative Items Percentage' are float
    actual_curve['Cumulative Items Percentage'] = actual_curve['Cumulative Items Percentage'].astype(float)
    theoretical_curve['Cumulative Items Percentage'] = theoretical_curve['Cumulative Items Percentage'].astype(float)

    # Create a Plotly Graph Object Figure
    fig_curve = go.Figure()

    # Add Actual Curve
    fig_curve.add_trace(
        go.Scatter(
            x=actual_curve['Cumulative Items Percentage'],
            y=actual_curve['Cumulative Revenue Percentage'],
            mode='lines+markers',
            name='Actual Curve',
            line=dict(color='#636EFA'),
            marker=dict(size=8)
        )
    )

    # Add Theoretical Curve
    fig_curve.add_trace(
        go.Scatter(
            x=theoretical_curve['Cumulative Items Percentage'],
            y=theoretical_curve['Cumulative Revenue Percentage'],
            mode='lines+markers',
            name='Theoretical Curve',
            line=dict(color='#EF553B', dash='dash'),
            marker=dict(symbol='circle-open', size=8)
        )
    )

    # Create a merged dataframe with sorted unique x-values
    merged_x = pd.concat([actual_curve['Cumulative Items Percentage'], theoretical_curve['Cumulative Items Percentage']]).drop_duplicates().sort_values()

    # Interpolate y-values for actual and theoretical curves
    actual_y_interp = actual_curve.set_index('Cumulative Items Percentage').reindex(merged_x).interpolate(method='linear').reset_index()
    theoretical_y_interp = theoretical_curve.set_index('Cumulative Items Percentage').reindex(merged_x).interpolate(method='linear').reset_index()

    # Add the shaded area using a filled trace
    fig_curve.add_trace(
        go.Scatter(
            x=merged_x,
            y=theoretical_y_interp['Cumulative Revenue Percentage'],
            mode='lines',
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False,
            hoverinfo='none'
        )
    )

    fig_curve.add_trace(
        go.Scatter(
            x=merged_x,
            y=actual_y_interp['Cumulative Revenue Percentage'],
            mode='lines',
            line=dict(color='rgba(0,0,0,0)'),
            fill='tonexty',
            fillcolor='rgba(128, 128, 128, 0.2)',
            showlegend=False,
            hoverinfo='none'
        )
    )

    # Update layout
    fig_curve.update_layout(
        title='Cumulative Revenue Curve (Actual vs. Theoretical)',
        xaxis_title='Cumulative Percentage of Items (%)',
        yaxis_title='Cumulative Percentage of Revenue (%)',
        xaxis=dict(range=[0, 100]),
        yaxis=dict(range=[0, 100]),
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        hovermode='x unified'
    )

    st.plotly_chart(fig_curve, use_container_width=True)



    col = st.columns((1, 1, 1), gap='medium')
    with col[0]:
        # Revenue Distribution Bar Chart
        fig_revenue = px.bar(
            abc_summary_filtered,
            x='ABC_category',
            y='Revenue generated',
            color='ABC_category',
            text='Revenue Percentage',
            labels={'Revenue generated': 'Revenue Generated', 'ABC_category': 'ABC Category'},
            title='Revenue Distribution by ABC Category',
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_revenue.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_revenue.update_layout(showlegend=False)
        st.plotly_chart(fig_revenue, use_container_width=True)

    with col[1]:
        # Stock Levels Pie Chart
        fig_stock = px.pie(
            abc_summary_filtered,
            names='ABC_category',
            values='Stock levels',
            color='ABC_category',
            hole=0.6,
            labels={'Stock levels': 'Stock Levels', 'ABC_category': 'ABC Category'},
            title='Stock Levels Distribution by ABC Category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_stock.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_stock, use_container_width=True)



    with col[2]:
        # Average Lead Time Line Chart
        lead_time_data = df_filtered.groupby('ABC_category')['Lead times'].mean().reset_index()
        fig_lead_time = px.line(
            lead_time_data,
            x='ABC_category',
            y='Lead times',
            markers=True,
            labels={'Lead times': 'Average Lead Time', 'ABC_category': 'ABC Category'},
            title='Average Lead Time by ABC Category',
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        st.plotly_chart(fig_lead_time, use_container_width=True)

    # Revenue vs Stock Levels Scatter Plot
    fig_scatter = px.scatter(
        df_filtered,
        x='Stock levels',
        y='Revenue generated',
        color='ABC_category',
        size='Revenue generated',
        hover_data=['SKU', 'Product type'],
        labels={'Stock levels': 'Stock Levels', 'Revenue generated': 'Revenue Generated'},
        title='Revenue vs Stock Levels',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    
    # Detailed ABC Analysis Table
    st.markdown('###### Detailed ABC Analysis Table')
    st.dataframe(
        df_filtered[['SKU', 'Product type', 'Revenue generated', 'Stock levels', 'ABC_category']],
        height=300,
    )

#######################



#Supplier Analytics
elif visualization == "Supplier Analytics":
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines  
    col = st.columns((1, 1, 1), gap='medium')

    with col[0]:
            #Number of products sold
            pr_num_sup = df.groupby('Supplier name')['Number of products sold'].sum().reset_index()
            color_sequence = px.colors.qualitative.Vivid
            colors = list(itertools.islice(itertools.cycle(color_sequence), len(pr_num_sup)))

            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_sup['Supplier name'], 
                                y=pr_num_sup['Number of products sold'],
                                marker_color=colors))
            fig.update_layout(title='Number of Products Sold by Supplier', 
                            xaxis_title='Supplier', 
                            yaxis_title='Number of products sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #


    with col[1]:
            #Revenue generated
            rev_sup = df.groupby('Supplier name')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=rev_sup['Supplier name'], 
                                y=rev_sup['Revenue generated'],
                                marker_color=colors))
            fig.update_layout(title='Revenue Generated by Supplier', 
                            xaxis_title='Supplier', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

    with col[2]:
            #Manufacturing Lead Time
            mlt_sup = df.groupby('Supplier name')['Manufacturing lead time'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=mlt_sup['Supplier name'], 
                                y=mlt_sup['Manufacturing lead time'],
                                marker_color=colors))
            fig.update_layout(title='Manufacturing Lead Time by Supplier', 
                            xaxis_title='Supplier', 
                            yaxis_title='Manufacturing Lead Time')
            st.plotly_chart(fig)
    
    st.write('\n\n')  # Adds two empty lines
    st.write('\n\n')  # Adds two empty lines


    #Defect Rate
    defect_by_supplier = df.groupby('Supplier name')['Defect rates'].mean().reset_index()

    # Sort suppliers by defect rate for better visualization
    defect_by_supplier = defect_by_supplier.sort_values('Defect rates', ascending=True)

    # Create a horizontal bar chart
    fig = px.bar(defect_by_supplier, 
                x='Defect rates', 
                y='Supplier name', 
                orientation='h', 
                color = 'Supplier name',
                color_discrete_sequence = px.colors.qualitative.Vivid,
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
            pr_num_ship = df.groupby('Shipping carriers')['Number of products sold'].sum().reset_index()
            color_sequence = px.colors.qualitative.Vivid
            colors = list(itertools.islice(itertools.cycle(color_sequence), len(pr_num_ship)))
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_ship['Shipping carriers'], 
                                y=pr_num_ship['Number of products sold'],
                                marker_color=colors))
            fig.update_layout(title='Number of Products Sold by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='Number of Products Sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Number of products sold by Transportation modes
            pr_num_tr = df.groupby('Transportation modes')['Number of products sold'].sum().reset_index()
            colors = list(itertools.islice(itertools.cycle(color_sequence), len(pr_num_tr)))
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_tr['Transportation modes'], 
                                y=pr_num_tr['Number of products sold'],
                                marker_color=colors))
            fig.update_layout(title='Number of Products Sold by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Number of Products Sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Number of products sold by Routes
            pr_num_rt = df.groupby('Routes')['Number of products sold'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=pr_num_rt['Routes'], 
                                y=pr_num_rt['Number of products sold'],
                                marker_color=colors))
            fig.update_layout(title='Number of Products Sold by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Number of Products Sold')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

    with col[1]:
            #Revenue generated by Shipping Carrier
            rv_sh = df.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=rv_sh['Shipping carriers'], 
                                y=rv_sh['Revenue generated'],
                                marker_color=colors))
            fig.update_layout(title='Revenue Generated by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Revenue generated by Transportation modes
            rv_tr = df.groupby('Transportation modes')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=rv_tr['Transportation modes'], 
                                y=rv_tr['Revenue generated'],
                                marker_color=colors))
            fig.update_layout(title='Revenue Generated by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Revenue generated by Routes
            rv_rt = df.groupby('Routes')['Revenue generated'].sum().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=rv_rt['Routes'], 
                                y=rv_rt['Revenue generated'],
                                marker_color=colors))
            fig.update_layout(title='Revenue Generated by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Revenue Generated')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

    with col[2]:
            #Shipping Times by Shipping Carrier
            st_sp = df.groupby('Shipping carriers')['Shipping times'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=st_sp['Shipping carriers'], 
                                y=st_sp['Shipping times'],
                                marker_color=colors))
            fig.update_layout(title='Average Shipping Time by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='AverageShipping Time')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Shipping Costs by Transportation modes
            st_tr = df.groupby('Transportation modes')['Shipping times'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=st_tr['Transportation modes'], 
                                y=st_tr['Shipping times'],
                                marker_color=colors))
            fig.update_layout(title='Average Shipping Time by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Average Shipping Time')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Shipping Times by Routes
            st_rt = df.groupby('Routes')['Shipping times'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=st_rt['Routes'], 
                                y=st_rt['Shipping times'],
                                marker_color=colors))
            fig.update_layout(title='Average Shipping Time by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Average Shipping Time')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


    with col[3]:
            #Shipping Costs by Shipping Carrier
            sc_sc = df.groupby('Shipping carriers')['Shipping costs'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=sc_sc['Shipping carriers'], 
                                y=sc_sc['Shipping costs'],
                                marker_color=colors))
            fig.update_layout(title='Shipping Costs by Shipping Carrier', 
                            xaxis_title='Shipping Carrier', 
                            yaxis_title='Shipping Costs')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines


            #Shipping Costs by Transportation Modes
            sc_tr = df.groupby('Transportation modes')['Shipping costs'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=sc_tr['Transportation modes'], 
                                y=sc_tr['Shipping costs'],
                                marker_color=colors))
            fig.update_layout(title='Shipping Costs by Transportation Modes', 
                            xaxis_title='Transportation Modes', 
                            yaxis_title='Shipping Costs')
            st.plotly_chart(fig)
    
            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

            #Shipping Costs by Routes
            sc_rt = df.groupby('Routes')['Shipping costs'].mean().reset_index()
            fig = go.Figure()   
            fig.add_trace(go.Bar(x=sc_rt['Routes'], 
                                y=sc_rt['Shipping costs'],
                                marker_color=colors))
            fig.update_layout(title='Shipping Costs by Routes', 
                            xaxis_title='Routes', 
                            yaxis_title='Shipping Costs')
            st.plotly_chart(fig)

            st.write('\n\n')  # Adds two empty lines
            st.write('\n\n')  # Adds two empty lines

    #Defect Rate by Shipping Carrier
    defect_by_carrier = df.groupby('Shipping carriers')['Defect rates'].mean().reset_index()

    # Sort carriers by defect rate for better visualization
    defect_by_carrier = defect_by_carrier.sort_values('Defect rates', ascending=False)

    # Create a horizontal bar chart
    fig = px.bar(defect_by_carrier, 
                x='Defect rates', 
                y='Shipping carriers', 
                orientation='h', 
                color='Shipping carriers',
                color_discrete_sequence = px.colors.qualitative.Vivid, 
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
                color='Transportation modes',
                color_discrete_sequence = px.colors.qualitative.Vivid, 
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