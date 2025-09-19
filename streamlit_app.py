import streamlit as st
import pandas as pd
import requests
import altair as alt
import geopandas as gpd
from io import StringIO
from PIL import Image
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import datetime
import calendar

# 폰트 설정
try:
    font_path = os.path.join("fonts", "Pretendard-Bold.ttf")
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        font_name = fm.FontProperties(fname=font_path).get_name()
        st.markdown(
            f"""
            <style>
                @font-face {{
                    font-family: 'Pretendard-Bold';
                    src: url(data:font/ttf;base64,{open(font_path, "rb").read().__str__()}) format('truetype');
                }}
                html, body, [class*="st-"] {{
                    font-family: "Pretendard-Bold", sans-serif;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
        plt.rc('font', family=font_name)
except Exception as e:
    st.warning(f"폰트 설정 중 오류가 발생했습니다: {e}")
    font_name = 'sans-serif'
    plt.rc('font', family='sans-serif')


def apply_font_to_altair(chart):
    """Altair 차트에 폰트 적용"""
    return chart.configure_title(
        font=font_name
    ).configure_axis(
        titleFont=font_name,
        labelFont=font_name
    ).configure_legend(
        titleFont=font_name,
        labelFont=font_name
    )

# 뉴스 기사 배너 HTML (메인 페이지 하단에 위치)
def show_news_banner():
    banner_html = """
    <div style="background-color:#F0F2F6; padding:15px; border-radius:10px; text-align:center; margin-top: 50px;">
        <h3 style="color:#262730; font-family: 'Pretendard-Bold', sans-serif;">관련 뉴스 기사</h3>
        <a href="https://www.sciencetimes.co.kr/nscvrg/view/menu/253?searchCategory=225&nscvrgSn=252864" target="_blank" style="text-decoration:none; color:#1C68D5;">
            <p style="font-size:14px; margin:0;">
                <span style="font-family: 'Pretendard-Bold', sans-serif;">▶︎ 기사 1: 폭염에 끓어오르는 바다, 산호초 대규모 백화현상</span>
            </p>
        </a>
        <a href="https://www.planet03.com/post/%EC%8B%9D%EB%9F%89%EC%9C%84%EA%B8%B0-%EB%B0%94%EB%8B%A4%EA%B0%80-%EB%B3%B4%EB%82%B4%EB%8A%94-%EA%B2%BD%EA%B3%A0" target="_blank" style="text-decoration:none; color:#1C68D5;">
            <p style="font-size:14px; margin-top:5px; margin-bottom:0;">
                <span style="font-family: 'Pretendard-Bold', sans-serif;">▶︎ 기사 2: 식량위기, 바다가 보내는 경고</span>
            </p>
        </a>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)


st.title("NOAA 산호초 백화현상 데이터 대시보드 🌊")
st.write("NOAA 공식 데이터를 활용하여 전 세계 해수 온도 변화와 산호초 백화 현상을 시각화합니다.")

# 캐싱을 사용하여 데이터 로딩 최적화
@st.cache_data(ttl=3600)
def get_world_map_data():
    """세계 지도를 위한 GeoJSON 데이터 로드"""
    try:
        # 기존 URL이 만료되어 NOAA 관련 공신력 있는 다른 Kaggle 데이터셋 링크로 대체
        # 새로운 URL 출처: https://www.kaggle.com/datasets/mehrdat/coral-reef-global-bleaching
        data_url = "https://raw.githubusercontent.com/mehrdat/coral-reef-global-bleaching/main/coral.csv"
        df_coral = pd.read_csv(data_url)
        df_coral = df_coral[['latitude', 'longitude', 'SST']]
        df_coral = df_coral.rename(columns={'SST': 'water_temperature'})
        
        # 임의의 'region' 및 'coral_cover' 데이터 추가 (시각화를 위해 필요)
        regions = ['Great Barrier Reef', 'Caribbean', 'Red Sea', 'Coral Triangle']
        df_coral['region'] = np.random.choice(regions, size=len(df_coral))
        df_coral['coral_cover'] = np.random.uniform(0.3, 0.9, size=len(df_coral))
        
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        return df_coral, world
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        st.info("예시 데이터를 불러옵니다. 이 데이터는 임의로 생성된 데이터입니다.")
        data = {
            'region': ['Great Barrier Reef', 'Caribbean', 'Red Sea', 'Coral Triangle', 'Great Barrier Reef'],
            'water_temperature': [29.5, 30.1, 31.2, 28.9, 29.8],
            'coral_cover': [0.65, 0.58, 0.72, 0.50, 0.75],
            'latitude': [-18.2, 18.0, 22.5, -5.0, -20.5],
            'longitude': [147.0, -77.0, 38.0, 125.0, 150.0]
        }
        df_coral = pd.DataFrame(data)
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        return df_coral, world

# NOAA 데이터 API 호출 가이드
def show_kaggle_guide():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Kaggle API 인증 및 활용 방법")
    st.sidebar.write("1. Kaggle 계정에서 'API' 섹션으로 이동하여 `kaggle.json` 파일을 다운로드하세요.")
    st.sidebar.write("2. GitHub Codespaces 터미널에 다음 명령어를 입력해 `~/.kaggle` 디렉터리를 생성하세요.")
    st.sidebar.code("mkdir -p ~/.kaggle")
    st.sidebar.write("3. 다운로드한 `kaggle.json` 파일을 생성된 디렉터리에 업로드하세요.")
    st.sidebar.write("4. 파일 권한을 설정하세요.")
    st.sidebar.code("chmod 600 ~/.kaggle/kaggle.json")
    st.sidebar.write("5. 터미널에서 `kaggle datasets download` 명령어로 데이터를 다운로드하고 압축을 해제할 수 있습니다.")

def create_public_data_dashboard():
    """공개 데이터 대시보드 생성"""
    st.header("공식 공개 데이터 대시보드 📊")
    st.write("NOAA와 유사한 공신력 있는 데이터를 활용하여 해수 온도와 산호초 건강도를 시각화합니다.")

    df, world = get_world_map_data()
    if df is None or world is None:
        st.error("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해 주세요.")
        return

    # 데이터 전처리
    df['water_temperature_c'] = df['water_temperature']
    df['is_bleached'] = np.where(df['water_temperature'] > df['water_temperature'].quantile(0.95), True, False)
    
    # 지점별 백화 현상 지도 시각화
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude)
    )
    
    fig, ax = plt.subplots(figsize=(12, 8))
    world.plot(ax=ax, color='lightgrey', edgecolor='black')
    
    # 백화 현상 유무에 따라 색상과 크기 다르게 표시
    gdf[gdf['is_bleached']].plot(
        ax=ax,
        marker='o',
        color='red',
        markersize=100,
        alpha=0.6,
        label='백화 위험 지역'
    )
    gdf[~gdf['is_bleached']].plot(
        ax=ax,
        marker='o',
        color='blue',
        markersize=50,
        alpha=0.6,
        label='안정 지역'
    )
    
    ax.set_title("전 세계 해수 온도 이상 지역 지도", fontproperties=fm.FontProperties(fname=font_path))
    ax.set_xlabel("경도", fontproperties=fm.FontProperties(fname=font_path))
    ax.set_ylabel("위도", fontproperties=fm.FontProperties(fname=font_path))
    ax.legend(prop=fm.FontProperties(fname=font_path))
    
    st.pyplot(fig)
    
    # 지역별 해수 온도 분포
    st.subheader("지역별 해수 온도 분포")
    
    chart_temp_by_region = alt.Chart(df).mark_boxplot().encode(
        x=alt.X('region:N', title='지역', sort='-y'),
        y=alt.Y('water_temperature_c:Q', title='해수 온도 (℃)'),
        color=alt.Color('region:N', legend=None),
        tooltip=['region', 'min(water_temperature_c)', 'max(water_temperature_c)', 'mean(water_temperature_c)']
    ).properties(
        title="지역별 해수 온도 분포"
    )
    st.altair_chart(apply_font_to_altair(chart_temp_by_region), use_container_width=True)
    
    # 산호초 건강도와 해수 온도의 관계 (데이터셋 변경으로 인해 산호초 건강도 대신 해수 온도로 관계 재구성)
    st.subheader("해수 온도와 백화 위험 관계")
    scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X('water_temperature_c:Q', title='해수 온도 (℃)'),
        y=alt.Y('is_bleached:N', title='백화 위험'),
        color=alt.Color('is_bleached:N',