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
    
    # 장르 및 국가 결측치 처리
    df['primary_genre'] = df['genre'].fillna('기타').astype(str).apply(lambda x: x.split('|')[0].strip())
    df['nation'] = df['nation'].fillna('기타').astype(str)
    
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
    st.info("💡 **이 그래프로 알 수 있는 것:** 드라마, 애니메이션 영화가 많은 것을 알 수 있다.")

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
    st.info("💡 **이 그래프로 알 수 있는 것:** 각 영화의 관객수를 한눈에 볼 수 있다.")

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

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 관객수 100만명 이하의 영화가 매우 많은것을 알수있다.")

st.markdown("---")

# ----------------------------------------------------
# 4. 개봉일 스크린수(first_scrn) vs 총 관객수(total_audi) 산점도
# ----------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='primary_genre',
    hover_name='movieNm',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'primary_genre': '장르'
    },
    title='개봉일 스크린수 vs 총 관객수 산점도'
)

# 마우스오버 툴팁 커스텀 설정
fig4.update_traces(
    hovertemplate='<b>영화명: %{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명'
)

fig4.update_layout(
    margin=dict(t=50, b=20, l=20, r=20),
    legend_title_text='장르'
)

st.plotly_chart(fig4, use_container_width=True)

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 스크린수와 관객수는 비례하는것을 알 수 있다.")

st.markdown("---")

# ----------------------------------------------------
# 5. 주요 장르별 총 관객수 박스플롯 (상자 그림)
# ----------------------------------------------------
st.subheader("5. 주요 장르별(10편 이상) 총 관객수 박스플롯")

# 영화 편수가 10편 이상인 장르 필터링
genre_counts_series = df['primary_genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major_genres = df[df['primary_genre'].isin(major_genres)]

fig5 = px.box(
    df_major_genres,
    x='primary_genre',
    y='total_audi',
    color='primary_genre',
    hover_name='movieNm',
    points='outliers',
    labels={
        'primary_genre': '장르',
        'total_audi': '총 관객수 (명)'
    },
    title='주요 장르별 총 관객수 분포 및 아웃라이어(상자 그림)'
)

# 마우스오버 툴팁 커스텀 설정
fig5.update_traces(
    hovertemplate='<b>영화명: %{hovertext}</b><br>총 관객수: %{y:,}명'
)

fig5.update_layout(
    margin=dict(t=50, b=20, l=20, r=20),
    showlegend=False
)

st.plotly_chart(fig5, use_container_width=True)

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객수의 중앙값 및 범위를 비교할 수 있으며, 상자 밖의 아웃라이어 점을 통해 해당 장르 내에서 대흥행을 거둔 극단적 흥행작들을 확인할 수 있습니다.")

st.markdown("---")

# ----------------------------------------------------
# 6. 개봉일 스크린수 vs 총 관객수 버블 차트 (점 크기: 개봉 첫 주 관객수)
# ----------------------------------------------------
st.subheader("6. 개봉일 스크린수 vs 총 관객수 (버블 차트)")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='primary_genre',
    hover_name='movieNm',
    size_max=40,
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객수 (명)',
        'first_week_audi': '개봉 첫 주 관객수 (명)',
        'primary_genre': '장르'
    },
    title='개봉일 스크린수 vs 총 관객수 버블 차트 (버블 크기: 개봉 첫 주 관객수)'
)

# 마우스오버 툴팁 커스텀 설정
fig6.update_traces(
    hovertemplate='<b>영화명: %{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>개봉 첫 주 관객수: %{marker.size:,}명'
)

fig6.update_layout(
    margin=dict(t=50, b=20, l=20, r=20),
    legend_title_text='장르'
)

st.plotly_chart(fig6, use_container_width=True)

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 첫 주 관객수(버블 크기)도 대체로 크며, 최종 총 관객수까지 이어지는 3개 지표 간의 다차원적 흥행 메커니즘을 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ----------------------------------------------------
# 7. 제작 국가(nation) -> 장르(primary_genre) 계층 선버스트 차트
# ----------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

# 제작 국가와 장르별 영화 편수 집계
df_nation_genre = df.groupby(['nation', 'primary_genre']).size().reset_index(name='count')

fig7 = px.sunburst(
    df_nation_genre,
    path=['nation', 'primary_genre'],
    values='count',
    color='nation',
    color_discrete_sequence=px.colors.qualitative.Pastel1,
    title='제작 국가 및 장르별 영화 편수 분포 (선버스트)'
)

# 마우스오버 툴팁 커스텀 설정
fig7.update_traces(
    hovertemplate='<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}'
)

fig7.update_layout(
    margin=dict(t=50, b=20, l=20, r=20)
)

st.plotly_chart(fig7, use_container_width=True)

# 시각화 해석 및 섹션 구분
with st.container():
    st.info("💡 **이 그래프로 알 수 있는 것:** 국가별(안쪽 고리)로 어떤 장르(바깥쪽 고리)의 영화가 얼마나 다양하게 제작되고 개봉했는지 계층적 비중과 영화 편수를 한눈에 비교할 수 있습니다.")

st.markdown("---")

# 데이터 목록 확인 기능
with st.expander("📄 원본 데이터 살펴보기"):
    st.dataframe(df[['movieCd', 'movieNm', 'openDt', 'primary_genre', 'nation', 'first_scrn', 'first_show', 'first_week_audi', 'total_audi', 'days_in_top10']])
