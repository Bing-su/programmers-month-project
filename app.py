import streamlit as st
import pandas as pd
import plots


st.set_page_config(page_title="프로그래머스 먼슬리 프로젝트")

with st.sidebar:
    st.image("./img/sundae-icon-21.jpg", width=300)
    st.header("프로그래머스 먼슬리 프로젝트 1")
    st.write("- 웹페이지를 만들어 EDA 결과 공유하기")
    st.write("[Github repo](https://github.com/Bing-su/programmers-month-project)")


raw_data = pd.read_csv("./android-games.csv")


def installs_to_num(s):
    if s.endswith("M"):
        s = int(s.split(".")[0]) * 1000
    else:
        s = int(s.split(".")[0])
    return s


data = raw_data.copy()
data["category"] = data["category"].map(lambda x: x[5:])
data["installs"] = data["installs"].map(installs_to_num)


st.title("Top Games on Google Play Store")

row1, row2 = st.beta_columns([3, 1])

with row1:
    st.write("플레이스토어의 장르별 Top 100 게임에 대한 데이터")

with row2:
    st.write("[kaggle](https://www.kaggle.com/dhruvildave/top-play-store-games)")

if st.checkbox("원본 데이터 보기"):
    raw_data

if st.checkbox("데이터 속성 설명 보기"):
    _1, row, _2 = st.beta_columns([1, 5, 1])
    with row:
        st.markdown(
            """|     열 이름      | 설명                             |
        | :--------------: | -------------------------------- |
        |       rank       | 해당 카테고리에서 앱의 순위      |
        |      title       | 앱의 이름                        |
        |  total ratings   | 받은 평가의 총 개수              |
        |     installs     | 대략적인 앱 설치 횟수            |
        |  average rating  | 평균 평점                        |
        | growth (30 days) | 30일 동안의 성장률 %             |
        | growth (60 days) | 60일 동안의 성장률 %             |
        |      price       | 가격(단위: 달러)                 |
        |     category     | 앱이 속한 카테고리(게임의 장르)  |
        | 5~1 star ratings | 평가에서 각각의 평점을 받은 횟수 |
        |       paid       | 앱의 유, 무료 여부               |"""
        )


st.header("1. 장르별 평점 평균")
chart_type1 = st.selectbox("사용할 차트 타입", ["altair", "seaborn"])
if chart_type1 == "altair":
    st.altair_chart(plots.rating_average(data, chart_type1), use_container_width=True)
else:
    st.pyplot(plots.rating_average(data, chart_type1))


st.header("2. 장르별 평가횟수의 평균")
chart_type2 = st.selectbox("사용할 차트 타입", ["altair ", "seaborn"])
if chart_type2 == "altair ":
    st.altair_chart(plots.rating_sum(data, chart_type2), use_container_width=True)
else:
    st.pyplot(plots.rating_sum(data, chart_type2))


st.header("3. 장르별 Top 10 게임")
genre = st.selectbox("장르", data["category"].unique())
col = st.selectbox("함께 볼 수치", ["total ratings", "average rating"])
st.altair_chart(plots.top10(data, genre, col), use_container_width=True)


st.header("4. 장르별 성장률")
days = st.selectbox("기준", ["30일", "60일"])
st.altair_chart(plots.growth(data, days), use_container_width=True)
