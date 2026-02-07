import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\stran\Desktop\DS\Python\Project\Startup\startup_cleaned.xls")

st.set_page_config(layout="wide",page_title="Startup Analysis")

df["date"]=pd.to_datetime(df["date"],errors="coerce")
df["month"]=df["date"].dt.month
df["year"]=df["date"].dt.year  

# st.dataframe(df)
st.sidebar.title("Startup Funding Analysis")
option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

def load_oveall_analysis():
    st.title("Overall Analysis")
    # total investment amount
    total=round(df["amount"].sum())
    

    # Max amount infused in startup
    max_funding=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    
    # Mean Investment
    avg_funding=round(df.groupby("startup")["amount"].sum().mean())
    
    # Total Funded Startup
    num_startup=df["startup"].nunique()
    
    col1,col2,col3,col4=st.columns(4)
    
    with col1:
        st.metric("Total ",str(total)+" Cr")
    
    with col2:
        st.metric("Max ",str(max_funding)+" Cr")
    
    with col3:
        st.metric("Average ",str(avg_funding)+" Cr")
    
    with col4:
        st.metric("Funded Startups",str(num_startup))
        
    st.header("MoM graph")
    
    selected_option=st.selectbox("Select Type",["Total","Count"])
    if selected_option=="Total":
        temp_df=df.groupby(["year","month"])["amount"].sum().reset_index()
    elif selected_option=="Count":
        temp_df=df.groupby(["year","month"])["amount"].count().reset_index()
    
    temp_df["x-axis"]=temp_df["month"].astype("str")+"-"+temp_df["year"].astype("str")
    
    fig, ax=plt.subplots()
    ax.plot(temp_df["x-axis"],temp_df["amount"])
    st.pyplot(fig)


def load_investors_details(investor):
    st.title(investor)
    # Most Recent Investments
    last5_df=df[df["investors"].str.contains(investor)].head()[["date","startup","city","round","amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    
    col1,col2,col3,col4=st.columns(4)
    with col1:
        # Biggest Investments
        big_series=df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        fig, ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    
    with col2:
        vertical_series=df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Sectors Invested in")
        
        fig1, ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
        
    with col3:
        stage_series=df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        st.subheader("Rounds of Investment")
        
        fig2, ax2=plt.subplots()
        ax2.pie(stage_series,labels=stage_series.index)
        st.pyplot(fig2)

    with col4:
        city_series=df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        st.subheader("City Of Investments")
        
        fig3, ax3=plt.subplots()
        ax3.pie(city_series,labels=city_series.index)
        st.pyplot(fig3)
        
    df["year"]=df["date"].dt.year    
    year_series=df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    st.subheader("Year On Year Investment")
    
    fig5, ax=plt.subplots()
    ax.plot(year_series.index,year_series.values)
    st.pyplot(fig5)
        
        
if option=="Overall Analysis":
    
    
    load_oveall_analysis()
    
    
elif option =="Startup":
    st.sidebar.selectbox("Select Startup",sorted(df["startup"].unique().tolist()))
    btn1=st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")
else:
    selected_investor=st.sidebar.selectbox("Select Startup",sorted(set(df["investors"].str.split(",").sum())))
    btn2=st.sidebar.button("Find Investors Details")
    if btn2:
        load_investors_details(selected_investor)
        
              
    # st.title("Investor Analysis")