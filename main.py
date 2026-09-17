import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 처리: 세로막대 기호(|)로 분리된 경우 첫 번째 장르만 사용
    df['primary_genre'] = df['genre'].fillna('기타').astype(str).apply(lambda x: x.split('|')[0].strip())
    
    return df

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 든 한국 개봉 영화 216편의 데이터 분석")

st.markdown("---")

# ----------------------------------------------------
# 1. 장르별 영화 편수 (도넛 차트)
# ----------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df['primary_genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 편수']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 편수',
    hole=0.4,
    title='장르별 영화 비율 및 편수',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 마우스오버 툴팁 설정 (편수 + 비율)
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}'
)

fig1.update_layout(
    margin=dict(t=50, b=20, l=20, r=20),
    legend_title_text='장르'
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 박스오피스 상위권 영화 중 주요 장르가 차지하는 비중과 장르별 영화 편수 분포를 확인할 수 있습니다.")

st.markdown("---")

# ----------------------------------------------------
# 2. 장르 및 영화별 총 관객수 (트리맵)
# ----------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포 (트리맵)")

# Plotly 트리맵 그래프 생성 (계층 구조: primary_genre -> movieNm, 크기: total_audi)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'primary_genre', 'movieNm'],
    values='total_audi',
    color='primary_genre',
    color_discrete_sequence=px.colors.qualitative.Set3,
    title='장르 및 영화별 총 관객수 분포'
)

# 마우스오버 툴팁 설정 (영화명 + 총 관객)
fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객수: %{value:,}명'
)

fig2.update_layout(
    margin=dict(t=50, b=20, l=20, r=20)
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 많은 총 관객수를 기록하며 흥행을 이끌었는지 직관적으로 비교할 수 있습니다.")

st.markdown("---")

# ----------------------------------------------------
# 3. 총 관객수(total_audi) 히스토그램
# ----------------------------------------------------
st.subheader("3. 총 관객수 히스토그램 분포")

# 히스토그램 생성
fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title='총 관객수(total_audi) 분포 히스토그램',
    labels={'total_audi': '총 관객수 (명)', 'count': '영화 편수'},
    color_discrete_sequence=['#4C72B0']
)

fig3.update_traces(
    hovertemplate='<b>관객수 구간: %{x}명</b><br>영화 편수: %{y}편'
)

fig3.update_layout(
    yaxis_title="영화 편수",
    margin=dict(t=50, b=20, l=20, r=20)
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 관객이 많은 영화 및 데이터 연산
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 시각화 해석 및 섹션 구분
with st.container():
    st.info(f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 총 관객수 **200만 명 이하(주로 50만~100만 명 구간)**에 집중되어 있는 오른쪽 꼬리가 긴 분포를 보이며, 가장 관객 수가 많은 영화는 **'{top_movie_name}'**(약 {top_movie_audi:,}명)입니다.")

st.markdown("---")

# 데이터 목록 확인 기능
with st.expander("📄 원본 데이터 살펴보기"):
    st.dataframe(df[['movieCd', 'movieNm', 'openDt', 'primary_genre', 'nation', 'first_scrn', 'first_show', 'first_week_audi', 'total_audi', 'days_in_top10']])
