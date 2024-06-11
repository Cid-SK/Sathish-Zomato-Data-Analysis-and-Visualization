import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

data = pd.read_csv("zomato.csv")
df=data.copy()

#streamlit part
st.set_page_config(page_title="Zomato",layout="wide")
st.title("***:red[ZOMATO ANALYSIS]***")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>",unsafe_allow_html=True)
 
#option_menu
with st.sidebar:
    select = option_menu("Menu",["Home", "Analysis", "About"],
    icons=['house','activity','info-circle-fill'], menu_icon="cast", default_index=1)

if select == "Home":

    st.subheader(":blue[***Welcome to Zomato Analysis Dashboard!***]")

    st.write('''This dashboard allows you to explore various insights and trends within the Zomato 
             dataset. Use the sidebar to navigate between different sections.''')

    st.subheader(":blue[***About Zomato:***]")
    st.write('''Launched in 2010, Our technology platform connects customers, restaurant partners and delivery
    partners, serving their multiple needs. Customers use our platform to search and discover 
    restaurants, read and write customer generated reviews and view and upload photos, order food 
    delivery, book a table and make payments while dining-out at restaurants.''')
    st.write('''On the other hand, we provide restaurant partners with industry-specific marketing 
    tools which enable them to engage and acquire customers to grow their business while also 
    providing a reliable and efficient last mile delivery service.''')
    st.write('''We also operate a one-stop procurement solution, Hyperpure, which supplies 
    high quality ingredients and kitchen products to restaurant partners. We also provide our 
    delivery partners with transparent and flexible earning opportunities.''')

    
    st.write(":red[Start exploring the data by selecting a section from the sidebar!]")



elif select == "Analysis":
    tab1,tab2,tab3,tab4,tab5,tab6= st.tabs(["***Currency Comparison***","***Restaurant***","***Costly Cuisine***","***Famous cuisine***","***Rating***","***Online vs Dine-in***"])
    with tab1:
        st.subheader(":blue[Currency Comparison]")
        with st.container(border=True):
            col1,col2=st.columns([3,2])
            with col1:
                price_c=df.groupby('Currency')['Exchange_rates'].first().reset_index()
                fig_price = px.bar(price_c,x='Currency',y='Exchange_rates',
                            color_discrete_sequence=px.colors.sequential.Redor_r,
                            title="Comparison of Indian Rupee with Other Currencies",
                            height=400,width=600)
                st.plotly_chart(fig_price)
            with col2:
                st.write("")
                st.write("")
                st.write("")
                
                max_rate_index = df[df['Currency'] != 'Rupee']['Exchange_rates'].idxmax()
                min_rate_index = df[df['Currency'] != 'Rupee']['Exchange_rates'].idxmin()

                max_currency = df.loc[max_rate_index, 'Currency']
                min_currency = df.loc[min_rate_index, 'Currency']

                max_rate = df.loc[max_rate_index, 'Exchange_rates']
                min_rate = df.loc[min_rate_index, 'Exchange_rates']
                with st.container(border=True):
                    st.subheader(":blue[Highest value against Rupee ]")
                    st.write(f":red[{max_currency}: {max_rate}]")
                with st.container(border=True):
                    st.subheader(":blue[Lowest value against Rupee ]")
                    st.write(f":red[{min_currency}: {min_rate}]")

    with tab2:
        st.subheader(":blue[Restaurant]")
        with st.container(border=True):
            selected_country_count = st.selectbox("Select Country", df['Country'].unique(), key="re_count", index=7)
            country_data_count = df[df['Country'] == selected_country_count]

            re_count = country_data_count.groupby('City')['Restaurant Name'].count().reset_index()

            fig_restaurant = px.bar(re_count, x='City', y='Restaurant Name',
                        color='Restaurant Name',
                        color_continuous_scale=px.colors.sequential.Redor_r,
                        labels={"City": 'City', 'Restaurant Name': 'Restaurant Count'},
                        title=f"Number of Restaurants in each City ({selected_country_count})")
            st.plotly_chart(fig_restaurant)

            st.subheader(f"Restaurant Count in {selected_country_count}")
            map_df = df[df['Country'] == selected_country_count].copy()
            map_df['Restaurant Count'] = map_df.groupby('City')['Restaurant Name'].transform('count')

            fig_map_rc = px.scatter_mapbox(map_df, 
                                        lat='Latitude', 
                                        lon='Longitude', 
                                        color='Restaurant Count',
                                        size='Restaurant Count', 
                                        hover_name='City',
                                        hover_data=['Cuisines', 'Country', 'Locality', 'Address'],
                                        zoom=2)

            fig_map_rc.update_layout(width=900, height=350, mapbox_style="open-street-map")
            fig_map_rc.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig_map_rc)

    with tab3:
        st.subheader(":blue[Costly Cuisine]")
        with st.container(border=True):
            col1,col2=st.columns(2)
            with col1:
                selected_country_costly = st.selectbox("Select the Country", df['Country'].unique(),index=7)
                country_data_costly= df[df['Country'] == selected_country_costly]
            with col2:
                selected_city = st.selectbox("Select the City",country_data_costly['City'].unique())
                city_data = country_data_costly[country_data_costly['City'] == selected_city]

            st.subheader(f":blue[Costlier Cuisine in {selected_city}]")
            costliest_cuisine = city_data.loc[city_data['Average Cost for two in INR'].idxmax()]['Cuisines']
            st.write(f"The costliest cuisine in {selected_city} is: :red[{costliest_cuisine}]")

            costly_cuisines = city_data.groupby('Cuisines')[['Average Cost for two in INR','Aggregate rating']].mean().reset_index().sort_values(by='Average Cost for two in INR',ascending=True)
            costly_cuisines['Aggregate rating'] = costly_cuisines['Aggregate rating'].apply(lambda x: round(x, 2))
            fig_costly = px.bar(costly_cuisines,x='Average Cost for two in INR',y='Cuisines',
                                color='Average Cost for two in INR',
                                color_continuous_scale=px.colors.sequential.Redor_r,
                                hover_data='Aggregate rating',hover_name='Cuisines',
                                title=f'Average Cost for Two in {selected_city}',
                                height=500,width=700)
            st.plotly_chart(fig_costly)

        with st.container(border=True):
            st.subheader("Restaurant Cost Distribution Across Locations")
            fig_map_costly= px.scatter_mapbox(df, 
                                    lat='Latitude', 
                                    lon='Longitude', 
                                    color='Average Cost for two in INR',
                                    size='Average Cost for two in INR',
                                    hover_name='Restaurant Name',
                                    hover_data=['Country','City','Locality','Address'],
                                    zoom=2)
            fig_map_costly.update_layout(width=900,height=350,mapbox_style="open-street-map")
            fig_map_costly.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map_costly)
    
    with tab4:
        st.subheader(":blue[Famous cuisine]")
        with st.container(border=True):
            c1,c2=st.columns(2)
            with c1:
                selected_country_fav = st.selectbox("Select Country", df['Country'].unique(),key="fav_c",index=7)
                country_data_fav= df[df['Country'] == selected_country_fav]
            with c2:
                selected_city_fav = st.selectbox("Select City",country_data_fav['City'].unique(),key="fav_city")
                city_data_fav = df[df['City'] == selected_city_fav]
            st.subheader(f":blue[Famous Cuisine in {selected_city_fav}]")
            cuisine_votes = city_data_fav.groupby('Cuisines')['Votes'].sum().reset_index().sort_values(by='Votes',ascending=True)
            most_famous_cuisine = cuisine_votes.loc[cuisine_votes['Votes'].idxmax()]['Cuisines']

            st.write(f"The most famous cuisine in {selected_city_fav} is: :red[{most_famous_cuisine}]")

            fig_fb = px.bar(cuisine_votes,x='Votes', y='Cuisines', labels={'x':'Cuisine', 'y':'Votes'},
                            color='Votes',color_continuous_scale=px.colors.sequential.Redor_r,
                            height=500,width=700,
                            title=f"Top Cuisines in {selected_city} based on Votes")
            st.plotly_chart(fig_fb)

        with st.container(border=True):
            st.subheader("Famous Cuisines Across Locations")
            fig_map = px.scatter_mapbox(df, 
                                    lat='Latitude', 
                                    lon='Longitude', 
                                    color='Votes',
                                    size='Votes',
                                    hover_name='Restaurant Name',
                                    hover_data=['Cuisines','Country','City','Locality','Address'],
                                    zoom=2)
            fig_map.update_layout(width=900,height=350,mapbox_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map)
    
    with tab5:
        st.subheader(":blue[Rating]")
        c1,c2=st.columns(2)
        with c1:
            selected_country_rating = st.selectbox("Select Country", df['Country'].unique(),key="rating_c",index=7)
            country_data_rating= df[df['Country'] == selected_country_rating]
        with c2:
            selected_rating = st.selectbox('Select Rating Text', country_data_rating['Rating text'].unique(), index=0,key='rating_count')
            rating_data = country_data_rating[country_data_rating['Rating text'] == selected_rating ]

        rating_count = rating_data.groupby('City')['Restaurant Name'].count().reset_index()
        rating_count.columns = ['City', 'Rating Count']
        with st.container(border=True):
            st.subheader(":blue[Analysis By City :]")
        
            fig_rating_city= px.bar(rating_count, x='City', y='Rating Count',
                        title=f'Rating Count in each City for {selected_rating}', 
                        color='Rating Count',color_continuous_scale=px.colors.sequential.Redor_r,
                        labels={'City':'City', 'Rating Count':'Rating Count'})
            st.plotly_chart(fig_rating_city)

        rating_count = rating_data.groupby('Cuisines')['Restaurant Name'].count().reset_index()
        rating_count.columns = ['Cuisines', 'Rating Count']

        with st.container(border=True):
            st.subheader(":blue[By Cuisines :]")
            fig_rating_cuisine = px.bar(rating_count,x='Rating Count', y='Cuisines', 
                        title=f'Rating Count in each City for {selected_rating}', 
                        color='Rating Count',color_continuous_scale=px.colors.sequential.Redor_r,
                        labels={'City':'City', 'Rating Count':'Rating Count'})
            st.plotly_chart(fig_rating_cuisine)

        rating_count = country_data_rating.groupby('Rating text')['Restaurant Name'].count().reset_index()
        rating_count.columns = ['Rating text', 'Rating Count']

        with st.container(border=True):
            st.subheader(":blue[Overview :]")
            fig_rating_overview = px.pie(rating_count,values='Rating Count', names='Rating text',
                        title=f"Exploring Restaurant Ratings in {selected_country_rating}",
                        labels={"Rating text": 'Rating', 'Rating Count': 'Count'},
                        hole=0.5,width=600,height=500)
            fig_rating_overview.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_rating_overview)


    with tab6:
        st.subheader(":blue[Online Delivery vs Dine-in]")
        col=['Cuisines','Votes','Price range','Average Cost for two in INR','Has Online delivery','Latitude','Longitude','Restaurant Name','Country','City','Locality','Address']
        spend_df=df[col].copy()

        spend_df['Total Spending'] = spend_df['Average Cost for two in INR'] * spend_df['Votes']

        spend_df['Has Online delivery'] = spend_df['Has Online delivery'].replace({'Yes': 'Online Delivery', 'No': 'Dine-in'})

        selected_country_spend = st.selectbox("Select Country", df['Country'].unique(), key="spend", index=7)
        country_data_spend = spend_df[spend_df['Country'] == selected_country_spend]

        city_spending = country_data_spend.groupby(['City', 'Has Online delivery'])['Total Spending'].sum().reset_index()

        # Sorting data by total spending
        #city_spending = city_spending.sort_values(by='Total Spending')

        with st.container(border=True):
            fig_area_od = px.area(city_spending, x='City', y='Total Spending', color='Has Online delivery', 
                            labels={'City': 'City', 'Total Spending': 'Total Spending (INR)', 
                                    'Has Online delivery': 'Delivery Type'}, 
                            title=f"Online vs Dine-in Spending Trends in {selected_country_spend}'s Cities",
                            width=900, height=500)
            fig_area_od.update_layout(xaxis_title='City', yaxis_title='Total Spending (INR)', hovermode="x unified")
            st.plotly_chart(fig_area_od)

        spend_more_online = country_data_spend[country_data_spend['Has Online delivery']=='Online Delivery']
        spend_more_dinein = country_data_spend[country_data_spend['Has Online delivery']=='Dine-in']

        with st.container(border=True):
            st.subheader(f"{selected_country_spend}'s Online Delivery Spendings ")
            fig_map_on_de = px.scatter_mapbox(spend_more_online, 
                                    lat='Latitude', 
                                    lon='Longitude', 
                                    color='Total Spending',
                                    size='Total Spending',
                                    hover_name='Restaurant Name',
                                    hover_data=['Cuisines','Country','City','Locality','Address'],
                                    zoom=2)
            fig_map_on_de.update_layout(width=900,height=350,mapbox_style="open-street-map")
            fig_map_on_de.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map_on_de)

        with st.container(border=True):
            st.subheader(f"{selected_country_spend}'s Dine-in Spendings")
            fig_map_dine= px.scatter_mapbox(spend_more_dinein, 
                                    lat='Latitude', 
                                    lon='Longitude', 
                                    color='Total Spending',
                                    size='Total Spending',
                                    hover_name='Restaurant Name',
                                    hover_data=['Cuisines','Country','City','Locality','Address'],
                                    zoom=2)
            fig_map_dine.update_layout(width=900,height=350,mapbox_style="open-street-map")
            fig_map_dine.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map_dine)

elif select == "About":

        st.subheader(":blue[***About Zomato Analysis Dashboard***]")

        st.write('''This Zomato Analysis Dashboard is a project aimed at analyzing and visualizing data
        from the Zomato platform.''')
        
        st.subheader(":blue[***Purpose:***]")
        st.write('''The purpose of this project is to gain insights into customer preferences, 
        restaurant trends, and industry dynamics using data analysis and visualization techniques.''')
        st.markdown(
        """
        ### :blue[***Technologies Used:***]
        - **Python:** For data manipulation, analysis, and visualization.
        - **Pandas:** For data manipulation and analysis.
        - **Plotly:** For interactive data visualization.
        - **Streamlit:** For building interactive web applications.
        
        ### :blue[***Project Tasks:***]
        - **Data Engineering:** Perform data preprocessing and feature engineering.
        - **Dashboard Development:** Create interactive visualizations and analysis tools.
        - **Dashboard Deployment:** Host and deploy the dashboard online.
        """ )
