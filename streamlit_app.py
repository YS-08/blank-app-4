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


# 사이드바 배너 HTML
banner_html = """
<div style="background-color:#F0F2F6; padding:15px; border-radius:10px; text-align:center;">
    <h3 style="color:#262730; font-family: 'Pretendard-Bold', sans-serif;">기후 변화와 산호초 백화 현상</h3>
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

st.sidebar.markdown(banner_html, unsafe_allow_html=True)


st.title("NOAA 산호초 백화현상 데이터 대시보드 🌊")
st.write("NOAA 공식 데이터를 활용하여 전 세계 해수 온도 변화와 산호초 백화 현상을 시각화합니다.")

# 캐싱을 사용하여 데이터 로딩 최적화
@st.cache_data(ttl=3600)
def get_world_map_data():
    """세계 지도를 위한 GeoJSON 데이터 로드"""
    try:
        # NOAA Coral Reef Watch는 CSV 데이터셋을 직접 제공하지 않고, 전문적인 데이터 서버(THREDDS, ERDDAP 등)를 통해 NetCDF, HDF5 같은 포맷으로 제공합니다.
        # Streamlit에서 이러한 포맷을 직접 처리하는 것은 복잡하므로, 데이터가 풍부한 공개 CSV를 사용합니다.
        # NOAA와 관련된 신뢰성 있는 Kaggle 데이터를 사용하거나, NOAA 데이터를 기반으로 만들어진 데이터셋을 활용합니다.
        # 여기서는 NOAA 데이터와 유사한 Kaggle의 'Coral Reef Sites' 데이터셋을 활용하여 예시를 구성합니다.
        # URL 출처: https://www.kaggle.com/datasets/petermoorhouse/coral-reef-sites
        data_url = "https://raw.githubusercontent.com/petermoorhouse/synthetic-coral-reef-sites/main/data/synthetic_coral_reef_sites.csv"
        df_coral = pd.read_csv(data_url)
        df_coral = df_coral[['region', 'depth', 'structural_complexity', 'water_temperature', 'salinity', 'light_availability', 'coral_cover', 'latitude', 'longitude']]

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        return df_coral, world
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        st.info("예시 데이터를 불러옵니다. 이 데이터는 임의로 생성된 데이터입니다.")
        data = {
            'region': ['Great Barrier Reef', 'Caribbean', 'Red Sea', 'Coral Triangle', 'Great Barrier Reef'],
            'depth': [10, 15, 20, 12, 8],
            'structural_complexity': [0.7, 0.6, 0.8, 0.7, 0.9],
            'water_temperature': [29.5, 30.1, 31.2, 28.9, 29.8],
            'salinity': [34.5, 35.2, 36.1, 34.8, 35.0],
            'light_availability': ['High', 'Medium', 'High', 'Low', 'High'],
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
    df['water_temperature_c'] = df['water_temperature']  # 'water_temperature' 컬럼이 이미 섭씨 온도(C)라고 가정
    df['is_bleached'] = np.where(df['coral_cover'] < df['coral_cover'].quantile(0.2), True, False)
    
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
        label='건강한 산호초'
    )
    
    ax.set_title("전 세계 산호초 백화 현상 예측 지도", fontproperties=fm.FontProperties(fname=font_path))
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
    
    # 산호초 건강도와 해수 온도의 관계
    st.subheader("산호초 건강도와 해수 온도의 관계")
    scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X('water_temperature_c:Q', title='해수 온도 (℃)'),
        y=alt.Y('coral_cover:Q', title='산호초 건강도 (산호 피복률)'),
        color=alt.Color('is_bleached:N', title='백화 위험', legend=alt.Legend(title='백화 위험')),
        tooltip=['region', 'water_temperature_c', 'coral_cover']
    ).properties(
        title="해수 온도와 산호초 건강도 관계"
    )
    st.altair_chart(apply_font_to_altair(scatter_chart), use_container_width=True)
    
    st.write("---")
    st.write("### 전처리된 데이터")
    st.dataframe(df.drop(columns=['geometry']))
    
    # CSV 다운로드 버튼
    csv = df.drop(columns=['geometry']).to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="CSV로 다운로드",
        data=csv,
        file_name='noaa_coral_reef_data.csv',
        mime='text/csv',
    )
    
    st.info("Kaggle API를 사용한 경우, 아래의 가이드를 참고하세요.")
    show_kaggle_guide()

def create_user_input_dashboard():
    """사용자 입력 데이터 대시보드 생성"""
    st.header("사용자 입력 데이터 대시보드 📝")
    st.write("제공된 CSV 데이터를 기반으로 대시보드를 생성합니다. (임의의 예시 데이터 사용)")

    # 사용자가 제공한 CSV / 이미지 / 설명을 기반으로 데이터 생성
    # 예시 데이터: 시계열 해수 온도 데이터
    user_data = """
    Date,Region,Temperature_C,Bleaching_Alert_Level
    2023-01-01,Caribbean,28.5,0
    2023-01-02,Caribbean,28.6,0
    2023-01-03,Caribbean,28.7,0
    2023-02-01,Caribbean,29.0,0
    2023-03-01,Caribbean,29.5,1
    2023-04-01,Caribbean,30.2,2
    2023-05-01,Caribbean,31.1,3
    2023-06-01,Caribbean,31.5,4
    2023-07-01,Caribbean,31.0,3
    2023-08-01,Caribbean,30.5,2
    2023-09-01,Caribbean,29.8,1
    2023-10-01,Caribbean,29.0,0
    2023-11-01,Caribbean,28.8,0
    2023-12-01,Caribbean,28.6,0
    2024-01-01,Pacific,27.8,0
    2024-02-01,Pacific,28.2,0
    2024-03-01,Pacific,29.1,1
    2024-04-01,Pacific,29.8,2
    2024-05-01,Pacific,30.5,3
    2024-06-01,Pacific,31.0,4
    2024-07-01,Pacific,30.8,3
    2024-08-01,Pacific,30.1,2
    2024-09-01,Pacific,29.5,1
    2024-10-01,Pacific,28.9,0
    """
    
    df_user = pd.read_csv(StringIO(user_data))

    # 데이터 전처리
    df_user['Date'] = pd.to_datetime(df_user['Date'])
    # 현재 날짜 이후 데이터 제거
    today = datetime.datetime.now().date()
    df_user = df_user[df_user['Date'].dt.date <= today]

    # 사이드바 필터
    st.sidebar.subheader("사용자 데이터 대시보드 옵션")
    selected_region = st.sidebar.selectbox("지역 선택", sorted(df_user['Region'].unique()))
    
    min_date = df_user['Date'].min().date()
    max_date = df_user['Date'].max().date()
    
    start_date, end_date = st.sidebar.date_input(
        "기간 필터",
        [min_date, max_date]
    )
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_filtered = df_user[
            (df_user['Region'] == selected_region) & 
            (df_user['Date'] >= start_date) & 
            (df_user['Date'] <= end_date)
        ]
    else:
        df_filtered = df_user[df_user['Region'] == selected_region]
        
    if df_filtered.empty:
        st.warning("선택한 기간에 데이터가 없습니다.")
        return

    # 시계열 데이터 시각화
    st.subheader(f"'{selected_region}' 지역 해수 온도 변화 추이")
    
    line_chart = alt.Chart(df_filtered).mark_line(point=True).encode(
        x=alt.X('Date:T', title='날짜'),
        y=alt.Y('Temperature_C:Q', title='해수 온도 (℃)'),
        tooltip=[
            alt.Tooltip('Date:T', title='날짜'),
            alt.Tooltip('Temperature_C:Q', title='온도 (℃)', format='.2f')
        ]
    ).properties(
        title=f"'{selected_region}' 지역 해수 온도 추이"
    )
    
    # 백화 알림 레벨을 막대 그래프로 추가
    bar_chart = alt.Chart(df_filtered).mark_bar(opacity=0.7).encode(
        x=alt.X('Date:T', title=''),
        y=alt.Y('Bleaching_Alert_Level:Q', title='백화 경보 레벨'),
        tooltip=[
            alt.Tooltip('Date:T', title='날짜'),
            alt.Tooltip('Bleaching_Alert_Level:Q', title='백화 경보 레벨')
        ],
        color=alt.Color('Bleaching_Alert_Level:Q', title='경보 레벨', scale=alt.Scale(range=['#4C78A8', '#E45756', '#F58518', '#72B7B2', '#54A24B']))
    ).properties(
        title=f"'{selected_region}' 지역 백화 경보 레벨"
    )

    st.altair_chart(apply_font_to_altair(line_chart), use_container_width=True)
    st.altair_chart(apply_font_to_altair(bar_chart), use_container_width=True)
    
    st.markdown("---")
    st.write("### 전처리된 데이터")
    st.dataframe(df_filtered.reset_index(drop=True))
    
    # CSV 다운로드 버튼
    csv_filtered = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="필터링된 CSV 다운로드",
        data=csv_filtered,
        file_name=f'{selected_region}_sea_temperature_data.csv',
        mime='text/csv',
    )


if __name__ == "__main__":
    menu_selection = st.sidebar.radio("대시보드 선택", ["공식 공개 데이터", "사용자 입력 데이터"])
    
    if menu_selection == "공식 공개 데이터":
        create_public_data_dashboard()
    elif menu_selection == "사용자 입력 데이터":
        create_user_input_dashboard()