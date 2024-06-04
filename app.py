import time
import streamlit as st
import numpy as np
import pandas as pd

# Step0: Web_config (option)
st.set_page_config(
   page_title="Jerry's dashboard",    # 網頁標題：顯示在瀏覽器分頁的標籤上，預設是程式碼的檔名
   page_icon="random",                # 網頁圖標：st.image 或 Emoji，或者使用"random"讓它隨機產生
   layout="centered",                 # 網頁寬度：預設是"centered"，還可以使用"wide"。
   initial_sidebar_state="expanded",  # 側邊欄顯示："expanded"打開或"collapsed"隱藏，預設是"auto"
   menu_items={                       # 右上角的菜單設定，共有以下三項可以設定：
        #'Get Help': '',
        #'Report a Bug':'',   
        #'About': ''
    }
)


# Step1: st.write & Magic Commands

st.title('Dashboard Test')
st.write("Build **Table**：")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [55, 37, 42, 12]
})
df

# Step2:  Draw chart

st.write("利用 line_chart() 建立一個折線圖：")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['台北', '台中', '台南'])
st.line_chart(chart_data)

st.write("利用 map() 在地圖上隨機標註點：")
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [25.05, 121.5],
    columns=['lat', 'lon'])
st.map(map_data)

# Step3: Input Box

st.write("[建立可互動式工具]")
if st.button('重新整理'):
    st.text("重新整理成功")

if st.checkbox('查看台南地圖狀況'):
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [23.6, 120.4],
        columns=['lat', 'lon'])
    st.map(map_data)

option = st.selectbox(
    '你喜歡什麼動物？',
    ['狗', '貓', '海獺', '松鼠'])
st.text(f'你的答案：{option}')

# Step4: Layout

st.sidebar.text('[版面切割]')
option2 = st.sidebar.selectbox('你喜歡哪種動物？',['狗', '貓', '鸚鵡', '天竺鼠'])
st.sidebar.text(f'你的答案：{option2}')

## 列容器
st.write("[版面切割]")
left_column, right_column = st.columns(2)
left_column.write("這是左邊欄位。")
right_column.write("這是右邊欄位。")

A_column, B_column, C_column = st.columns(3)
A_column.write("這是A欄位。")
B_column.write("這是B欄位。")
C_column.write("這是C欄位。")

## 展開容器
expander = st.expander("點擊來展開...")
expander.write("如果你要顯示很多文字折疊起來")

## 分頁容器
tab1, tab2 = st.tabs(["Cat 介紹", "Dog 介紹"])
with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

# Step5: Status
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1, f'目前進度 {i+1} %')
    time.sleep(0.05)
bar.progress(100, '載入完成！')

if st.button('儲存ａ', type="primary"):
    st.toast(':rainbow[你編輯的內容已經保存]', icon='💾')
    st.toast('你編輯的內容已經保存')

st.success('Success!')
st.info('Info!')
st.warning('Warning!')
st.error('Error!', icon='🚨')
st.balloons()
st.snow()

# Step6: Chat
# method1
with st.chat_message("user"):
    st.write("Hi 👋，請問你是誰？")

# method2
message = st.chat_message("assistant", avatar="🦖" )
message.write("Hello！ I am ChatBot 🤖")
message.write("有什麼我可以幫助你的嗎？")
st.chat_input("Say something...")

# Step7: From

with st.form(key='my_form'):
    form_name = st.text_input(label='姓名', placeholder='請輸入姓名')
    form_gender = st.selectbox('性別', ['男', '女', '其他'])
    form_birthday = st.date_input("生日")
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.write(f'hello {form_name}, 性別:{form_gender}, 生日:{form_birthday}')






