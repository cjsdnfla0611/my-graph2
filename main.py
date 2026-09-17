import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 처리: '|' 기호로 연결된 여러 장르 중 첫 번째 장르만 추출
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

# Plotly 도넛 그래프 생성 (hole 파라미터로 도넛 형태 구현)
fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 편수',
    hole=0.4,
    title='장르별 영화 비율 및 편수',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 마우스오버 툴팁 설정 (편수와 비율 표시)
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

# '이 그래프로 알 수 있는 것' 영역
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 박스오피스 상위권 영화 중 주요 장르가 차지하는 비중과 장르별 편수 분포를 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ----------------------------------------------------
# 2. 개봉 첫 주 관객수 vs 총 관객수 (산점도 그래프 예시)
# ----------------------------------------------------
st.subheader("2. 개봉 첫 주 관객수와 총 관객수의 관계")

fig2 = px.scatter(
    df,
    x='first_week_audi',
    y='total_audi',
    color='primary_genre',
    size='days_in_top10',
    hover_name='movieNm',
    labels={
        'first_week_audi': '개봉 첫 주 관객수 (명)',
        'total_audi': '총 관객수 (명)',
        'primary_genre': '장르',
        'days_in_top10': 'Top 10 유지 일수'
    },
    title='개봉 첫 주 관객수 vs 총 관객수 (점 크기: Top10 유지 일수)'
)

fig2.update_layout(margin=dict(t=50, b=20, l=20, r=20))
st.plotly_chart(fig2, use_container_width=True)

# '이 그래프로 알 수 있는 것' 영역
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 첫 주 관객수가 높은 영화일수록 최종 총 관객수도 높게 나타나는 강한 양의 상관관계를 확인할 수 있습니다.")

st.markdown("---")

# 원본 데이터 확인용 (Expander)
with st.expander("📄 원본 데이터 살펴보기"):
    st.dataframe(df)
