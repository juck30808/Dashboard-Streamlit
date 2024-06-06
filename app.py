import time
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px # zÍﬁpip install ploly-express

# Step0: Web_config (option)
st.set_page_config(
   page_title="Jerry's dashboard",    # 網頁標題：顯示在瀏覽器分頁的標籤上，預設是程式碼的檔名
   page_icon="blue_book",             # 網頁圖標：emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
   layout="wide",                     # 網頁寬度：預設是"centered"，還可以使用"wide"。
   initial_sidebar_state="expanded",  # 側邊欄顯示："expanded"打開或"collapsed"隱藏，預設是"auto"
   menu_items={                       # 右上角的菜單設定，共有以下三項可以設定：
        #'Get Help': '',
        #'Report a Bug':'',   
        #'About': ''
    }
)

# ## 打包成函數可以變成快取裝飾
# @st.cache
# def get_data_from_excel():
#     return df
# df = get_data_from_excel()


df = pd.read_excel("Supermarket.xlsx",
    engine="openpyxl",
    sheet_name="Sales",
    skiprows=3,
    usecols="B:R",
    nrows=1000, 
)
## BarChart Use Line:112
df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
#print(df)
#st.dataframe(df)

# ----- Status -------
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1, f'目前進度 {i+1} %')
    time.sleep(0.01)
bar.progress(100, '載入完成！')



# ----- Sidebar ----
st.sidebar.header("條件過濾")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(), #display all city name
    default=df["City"].unique()
)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)
df_selection = df.query( #@ 可以引用變數
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# ---- MAINPAGE ----
st.title(":bar_chart: Dashboard") #Dash
st.markdown("##")  #markdown spread

# TOP KPI's 總銷售額 平均評級 每單平均銷售額
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)    #
star_rating = ":star:" * int(round(average_rating, 0))      #rating by emogi 
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)  #total
# 將內容插入不同的欄目
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("總銷售額 (Sales):")
    st.subheader(f"USD $ {total_sales:,}")
with middle_column:
    st.subheader("平均評價 (Rating):")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("平均客單 (AveSales Per Trans):")
    st.subheader(f"USD $ {average_sale_by_transaction}")

st.markdown("""---""")   #markdown spread

# # Jupyter Test 
# #根據產品做分組
# df.groupby(by=["Product line"]).sum()          
# #根據產品做分組，只留下總銷售
# df.groupby(by=["Product line"]).sum()[["Total"]] 
# #根據產品做分組，只留下總銷售，並且排序以利圖表呈現
# df.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(                  # bar cahrt
    sales_by_product_line,                   # data
    x="Total",                               # x值
    y=sales_by_product_line.index,           # y值
    orientation="h",                         # 水平
    title="<b>產品銷售狀況</b>",    # 內部 title (HTML)為出體
    # 長條圖顏色，這邊利用16進位代碼與資料長度相乘
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line), 
    template="plotly_white",                 # 白色範本
)
# Advance Setting Bar Chart
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",         # 將背景改為透明
    xaxis=(dict(showgrid=False))          # 將x軸網格刪除
)
#st.plotly_chart(fig_product_sales)

# # Jupyter Test
# 查看資料格式
# df.info()
# 將 Object 資料格式轉換成時間
# df["hour"] = pd.to_datatime(df["Time"], format="%H:%M:%S").dt.hour

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.line(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>每小時銷售變化</b>",
    color_discrete_sequence=["#00B883"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),   # 將 x 變成限性
    plot_bgcolor="rgba(0,0,0,0)",    # 背景為透明 
    yaxis=(dict(showgrid=False)),    # 將 y 軸隔線刪除
)
#st.plotly_chart(fig_hourly_sales)

##  ---- Two Column ---
#st.title('雙重欄目')
left_column, right_column = st.columns(2)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)



# # ---- Show Raw data ---
st.title(":memo: RawData") #Dash
expander = st.expander("點擊查看 Raw Data")
expander.write("完整Rawdata")
expander.dataframe(df_selection) #Display the selection result;

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

    
# # ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
