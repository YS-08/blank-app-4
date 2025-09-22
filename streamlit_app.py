"""
Streamlit 대시보드 (한국어 UI)
- Allen Coral Atlas 지도 및 뉴스 링크 탭을 통합합니다.
- 사용자 입력(사전에 정의된 텍스트)을 기반으로 요약 및 시각화를 제공합니다.
- '백화현상 지수' 탭에 새로운 시각화 기능을 추가했습니다.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import datetime
import pytz

# ---------------------------
# 페이지 설정 및 스타일
# ---------------------------
st.set_page_config(
    page_title="산호초 백화 & 해수면 온도 대시보드",
    layout="wide"
)

st.markdown("<h1 style='color:black;'>🌊 산호초 백화현상 & 해수 온도 대시보드</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:black; font-size: 16px; font-weight: bold;'>😍 해수온이 올라가면 산호가 조말루치라는 조류를 잃어 ‘백화 현상’이 일어납니다. 산호는 색을 잃고 영양도 제대로 얻지 못해 약해집니다. 지구 온난화, 이상 기후, 오염 등이 원인이며, 백화가 오래 지속되면 산호와 그곳에 사는 해양 생물들 모두 위험해집니다. ❤️‍🩹</p>", unsafe_allow_html=True)

# ---------------------------
# 유틸리티: 시간/로컬 날짜 처리
# ---------------------------
LOCAL_TZ = pytz.timezone("Asia/Seoul")

def local_today_date() -> pd.Timestamp:
    return pd.Timestamp.now(tz=LOCAL_TZ).normalize()

TODAY = local_today_date().date()

# ---------------------------
# 사이드바 필터
# ---------------------------
with st.sidebar:
    st.header("필터")

    start_date = datetime.date(1980, 1, 1)
    end_date = datetime.date(2020, 8, 31)
    
    selected_date = st.date_input(
        "날짜 선택",
        datetime.date(2000, 1, 1),
        min_value=start_date,
        max_value=end_date
    )
    
    countries = ["전 지구", "대한민국", "호주", "인도네시아", "필리핀", "일본", "몰디브", "미국 하와이"]
    selected_country = st.selectbox("나라 선택", countries)

# ---------------------------
# Streamlit 앱 UI 구성
# ---------------------------
# 메인 콘텐츠 (탭으로 구성)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["메인", "보고서", "한겨레 뉴스", "플래닛 03 뉴스", "퀴즈"])

with tab1:
    st.subheader("Allen Coral Atlas (앨런 산호 지도)")
    embed_url = "https://allencoralatlas.org/atlas/#1.00/37.1744/-176.4983"
    try:
        components.html(
            f'<iframe src="{embed_url}" width="100%" height="850px" style="border:none;"></iframe>',
            height=870,
            scrolling=True
        )
    except Exception as e:
        st.error(f"웹페이지를 불러오는 데 실패했습니다: {e}")
        st.info("해당 웹사이트가 iframe 임베딩을 허용하지 않거나, 일시적인 오류일 수 있습니다.")
        st.markdown(f"**직접 방문하기:** [{embed_url}]({embed_url})")
    st.markdown("---")

    # ----- 백화현상 지수 탭에서 이동된 내용 -----
    
    # —————————————
    # 가짜 데이터 생성 (예시)
    # —————————————
    dates = pd.date_range("1980-01-01", "2020-08-31", freq="Y")
    data = {
        "날짜": np.tile(dates, len(countries)),
        "나라": np.repeat(countries, len(dates)),
        "백화현상지수": np.random.rand(len(dates) * len(countries)) * 100
    }
    df = pd.DataFrame(data)
    
    # —————————————
    # 선택된 나라 데이터 필터링
    # —————————————
    if selected_country == "전 지구":
        df_filtered = df.groupby("날짜")["백화현상지수"].mean().reset_index()
    else:
        df_filtered = df[df["나라"] == selected_country]
    
    # ---------------------------
    # 컬럼을 사용하여 차트를 나란히 배치
    # ---------------------------
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 연도별 백화현상 지수 변화")
        fig_line = px.line(df_filtered, x="날짜", y="백화현상지수", title=f"{selected_country} 백화현상 추세")
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.subheader("🌎 지도에서 보는 국가별 백화현상")
        latest_year = selected_date.year
        df_map = df[df["날짜"].dt.year == latest_year]
    
        country_map = {
            "대한민국": "South Korea",
            "호주": "Australia",
            "인도네시아": "Indonesia",
            "필리핀": "Philippines",
            "일본": "Japan",
            "몰디브": "Maldives",
            "미국 하와이": "United States",
            "전 지구": "World"
        }
        df_map["country_en"] = df_map["나라"].map(country_map)
    
        fig_map = px.choropleth(
            df_map,
            locations="country_en",
            locationmode="country names",
            color="백화현상지수",
            title=f"{latest_year}년 국가별 산호초 백화현상 지수",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown(
        """
        ### 📚 종합 보고서: 백화된 산호초와 지구 온난화
        
        <div style="font-size: medium;">
        <br>
        <b>📖 데이터 출처 및 참고 자료</b>
        <ul>
            <li>공식 해수면 데이터: NOAA Sea Level Change Portal / Allen Coral Atlas</li>
            <li>뉴스 출처:
                <ul>
                    <li>한겨레 뉴스 '산호가 보내는 SOS' 기사</li>
                    <li>플래닛 03 뉴스 '식량위기, 바다가 보내는 경고' 기사</li>
                </ul>
            </li>
        </ul>

        <b>🌍 주요 연구 결과 및 시사점</b>
        <ul>
            <li><b>주요 연구 결과</b><br>
                해수온 상승과 산호초 백화 현상은 밀접한 관계가 있습니다. 미국해양대기청(NOAA)의 자료에 따르면, 해수온이 평년보다 1~2℃ 이상 상승하면 산호초 백화 현상이 급격히 발생합니다. 특히 1998년과 2016년에는 전 지구적으로 광범위한 백화 현상이 관측되었는데, 이는 해수온 상승이 산호 생태계 붕괴의 핵심 원인임을 보여줍니다. 산호는 스트레스를 받으면 몸 밖으로 공생 조류를 내쫓아 하얗게 변하고, 백화 현상이 지속되면 결국 죽게 됩니다.
            </li>
            <li><b>해양 생태계에 미치는 영향</b><br>
                산호초가 사라지면 전 세계 해양 생물의 약 25%가 서식지를 잃어 생물 다양성이 크게 위협받습니다. 이는 해양 생태계 전체의 균형을 무너뜨립니다. 또한 산호초는 어업의 기반을 제공하고, 해안을 보호하며, 중요한 관광 자원이 되므로, 산호초가 붕괴되면 어업 자원 감소, 관광 산업 위축, 해안 침식 등 심각한 사회경제적 손실로 이어집니다.
            </li>
            <li><b>시사점 및 실천 방안</b><br>
                산호초 백화 현상의 근본적인 원인은 지구 온난화로 인한 해수온 상승이므로, 온실가스 배출량을 줄여 기후 변화를 늦추는 것이 가장 중요합니다. 플라스틱 쓰레기와 같은 해양 오염도 산호초에 스트레스를 주기 때문에, 해양 오염 문제를 해결하기 위한 노력도 필요합니다. 마지막으로, 기후 변화와 산호초 백화 현상의 심각성을 알리는 실질적인 환경 교육과 캠페인을 통해 사람들의 행동 변화를 이끌어내는 것이 중요합니다.
            </li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br><b>💡 해결 방안 및 실천 과제</b>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: medium;">
            <b>1. 온실가스 배출량 줄이기</b>
            <ul>
                <li>자가용 보다 대중교통 이용하기</li>
                <li>자전거 타고 이동하기</li>
                <li>불을 끄거나 어댑터를 뽑아 안 쓰는 전기 절약하기</li>
                <li>에너지 소비 효율 좋은 제품 사용하기</li>
            </ul>
            <b>2. 환경 개선하기</b>
            <ul>
                <li>플라스틱 사용 줄이기</li>
                <li>해양 봉사활동 (쓰레기 줍기)</li>
            </ul>
            <b>3. 인식 개선</b>
            <ul>
                <li>환경 교육과 캠페인</li>
                <li>SNS, TV 광고 등을 통한 문제 알리기</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
    ---
    <br>
    <p style='color:black; font-weight:bold;'>⚠️ 연구의 한계 및 주의사항</p>
    <p>이 대시보드의 일부 데이터는 교육 및 시각화 목적의 시뮬레이션을 포함하고 있습니다. 실제 학술 연구나 정책 결정에는 다음의 공식 데이터를 활용하시기 바랍니다:</p>
    <br>
    <ul>
        <li><a href="https://allencoralatlas.org/atlas/#4.55/-15.4730/149.1687" target="_blank">Allen Coral Atlas</a></li>
        <li><a href="https://kosis.kr/index/index.do" target="_blank">국가통계포털(KOSIS)</a></li>
    </ul>
    """,
    unsafe_allow_html=True
    )


with tab2:
    st.subheader("지구 온난화와 산호초 백화 현상에 관한 보고서")
    
    st.markdown("""
지구 온난화로 인한 해수온 상승은 생태계 전반에 심각한 영향을 미치고 있으며, 그중에서도 산호초 백화 현상은 가장 대표적이고 우려되는 문제로 지적되고 있습니다. 산호초는 해양 생물의 약 25%가 서식하는 중요한 생태계로서, 생물 다양성과 생산성을 유지하는 핵심적 역할을 수행합니다. 그러나 해수온이 일정 수준 이상으로 상승하면 산호의 색소가 소실되고, 장기적으로는 산호 사멸로 이어지는 백화 현상이 발생합니다.

이러한 산호초의 붕괴는 어업 자원의 감소, 연안 지역의 해양 관광 산업 위축, 해안 방파 효과 상실 등 다양한 사회/경제적 피해를 초래할 수 있습니다. 특히 전 지구적으로 산호초가 빠른 속도로 감소하고 있다는 점은 인류의 지속 가능한 발전에도 직접적인 위협으로 작용합니다. 따라서 단순히 해수온 상승이라는 단일 요인에 그치지 않고, 해양 산성화, 수질 오염, 빛과 영양염류 조건 등 다양한 환경적 요인이 복합적으로 작용할 수 있음을 고려해야 합니다. 이에 본 보고서는 해수온 상승으로 인한 산호초 백화 현상의 원인을 체계적으로 탐구하고, 이를 통해 효과적인 보존 및 관리 방안을 마련하는 데 기초 자료를 제공하고자 합니다.

---

### 해수온 상승과 산호초 백화 현상 간의 상관관계

미국해양대기청(NOAA)의 자료에 따르면, 열대 태평양, 인도양, 카리브 해역 등 주요 산호초 분포 지역에서 해수면 온도가 꾸준히 상승하고 있으며, 특정 시기에는 급격한 고온 현상이 관측되었습니다. 이러한 변화는 대규모 백화 사건과 밀접하게 연결되는데, 실제로 1998년과 2016년에 발생한 전 지구적 백화 현상은 평균 해수온이 평년보다 1~2℃ 높게 유지된 시기와 일치합니다. 이는 해수온 변화 추이가 산호초 백화 현상의 발생 시기와 강도를 설명하는 중요한 지표임을 보여줍니다. 더 나아가 자료 분석 결과, 해수온 상승과 산호초 백화 현상 사이에는 뚜렷한 상관관계가 확인됩니다. 해수온이 임계 수준(약 30℃ 전후)을 초과하거나 평년 대비 1℃ 이상의 고온이 일정 기간 지속될 경우, 산호는 공생조류를 방출하며 급격히 백화됩니다. NOAA 지도의 시각적 증거 역시 이를 뒷받침하는데, 해수온이 높은 지역일수록 산호초의 백화 피해가 집중되는 양상이 뚜렷하게 나타났습니다. 따라서 해수온 상승은 단순한 기후 지표를 넘어, 산호 생태계 붕괴를 직접적으로 설명하는 핵심 요인으로 이해할 수 있습니다.

바다의 온도가 상승할수록 산호초의 백화현상도 빠르게 진행됩니다. 밑은 2016년 부터 2017년까지 1년 동안의 산호초 변화 현상입니다.

그렇다면 바다 온도와 산호초는 실제로 어떤 관련이 있을까요? 결론부터 말하자면, 밀접한 연관이 있습니다. 산호초는 산호충의 석회질 외골격이 오랜 세월 쌓여 형성된 암초로, 전 세계 해양 생물의 약 25%가 서식하는 중요한 생태계입니다. 겉보기에 식물처럼 보이지만 실제로는 촉수를 이용해 먹이를 잡는 동물입니다. 산호는 체내에 공생 조류(조류의 일종인 ‘조류성 미세조류, 조산소를 가지고 있는데, 이 미세조류가 광합성을 통해 산호에게 에너지를 공급합니다. 하지만 바다의 수온이 평소보다 1~2℃ 이상 오르면, 산호는 스트레스를 받아 이 공생 조류를 몸 밖으로 내쫓게 됩니다. 그 결과 산호는 에너지원과 색을 잃어 흰색으로 변하는데, 이것이 바로 산호초 백화현상입니다. 이 현상이 중요한 이유는 단순히 산호의 죽음 때문만이 아닙니다. 산호초는 바다 생태계의 ‘집’이자 ‘어머니’라 불릴 만큼 수많은 해양 생물이 의존하는 터전이기 때문입니다. 작은 물고기들은 산호초를 은신처로 삼고, 갑각류와 말미잘 같은 무척추동물도 산호에 붙어 살아갑니다. 실제로 연구에 따르면, 건강한 산호초는 해양 생물 다양성을 유지하는 핵심 기반이며, 인간에게도 어업과 해안 보호(방파제 역할), 관광 자원을 제공합니다. 하지만 백화현상이 심해지면 산호는 회복하지 못하고 죽게 됩니다. 산호가 사라지면 해양 생물들의 서식지가 붕괴되고, 이는 곧 생태계 균형의 붕괴로 이어집니다. 예를 들어 2016년 호주 그레이트 배리어 리프에서는 해수 온도 상승으로 전체 산호초의 약 30% 이상이 백화되었으며, 일부 지역은 사실상 회복 불가능한 상태에 이르렀습니다. 즉, 산호초 백화현상은 단순히 바닷속 풍경이 사라지는 문제가 아니라, 지구 해양 생태계 전체의 위기와 직결된 현상이라 할 수 있습니다.

---

### 우리의 실천 방안

우리는 산호초 백화현상이 줄어들 수 있도록 노력해야 합니다. 적어도 이 상황이 악화되지 않도록 노력 해야 합니다. 그렇다면 어떤 실천 방법을 실천할 수 있을까요?

<ul style="list-style-type:none;">
    <li><b>온실가스 배출량 줄이기</b>: 자가용보다 대중교통 이용하기, 자전거 타고 이동하기, 안 쓰는 전기 절약하기, 에너지 효율 좋은 제품 사용하기.</li>
    <li><b>플라스틱 사용 줄이기</b>: 바다 쓰레기의 약 70%가 플라스틱입니다. 플라스틱 사용을 줄이거나 해양 봉사활동을 통해 쓰레기 유입을 줄이는 것도 좋은 방법입니다.</li>
    <li><b>환경 교육과 캠페인</b>: 학교에서 진행되는 환경 교육과 캠페인을 좀 더 사실적이고 심각성이 보이게 교육할 필요가 있습니다. 의무적인 교육이 아닌, 실제로 변화를 만들어낼 수 있는 교육이 필요합니다.</li>
</ul>

이러한 방법들은 모두 실천하기 쉽지만 그만큼 가볍게 생각하게 되는 사소한 방법입니다. 하지만 이 사소한 행동들이 모여 거대한 하나를 만들고 그 거대한 하나가 세상을 바꾸는 것입니다. 사소한 실천을 같이 수업시간에 해보거나 봉사활동으로 참여하는 것도 좋은 방법이라고 생각합니다.
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("한겨레: '산호가 보내는 SOS' 기사")
    hani_url = "https://www.hani.co.kr/arti/society/environment/1194115.html"
    st.info("아래 기사는 한겨레 웹사이트에서 제공됩니다.")
    try:
        components.html(
            f'<iframe src="{hani_url}" width="100%" height="800px" style="border:none;"></iframe>',
            height=820,
            scrolling=True
        )
    except Exception as e:
        st.error(f"뉴스 기사를 불러오는 데 실패했습니다: {e}")
        st.markdown(f"**직접 방문하기:** [{hani_url}]({hani_url})")

with tab4:
    st.subheader("플래닛 03: '식량위기, 바다가 보내는 경고' 기사")
    planet_url = "https://www.planet03.com/post/%EC%8B%9D%EB%9F%89%EC%9C%84%EA%B8%B0-%EB%B0%94%EB%8B%A4%EA%B0%80-%EB%B3%B4%EB%8B%A4%EA%B0%80-%EB%B3%B4%EB%82%B4%EB%8A%94-%EA%B2%BD%EA%B3%A0"
    st.info("아래 기사는 플래닛 03 웹사이트에서 제공됩니다.")
    try:
        components.html(
            f'<iframe src="{planet_url}" width="100%" height="800px" style="border:none;"></iframe>',
            height=820,
            scrolling=True
        )
    except Exception as e:
        st.error(f"뉴스 기사를 불러오는 데 실패했습니다: {e}")
        st.markdown(f"**직접 방문하기:** [{planet_url}]({planet_url})")

with tab5:
    st.title("산호초 백화현상 퀴즈")
    st.write("사진을 보고 산호의 상태를 맞춰보세요!")

    # 문제와 정답 (이미지 URL 사용)
    quiz = [
        {
            "question": "1. 이 산호의 상태는 무엇일까요?",
            "image": "https://cdn.greenpostkorea.co.kr/news/photo/201704/75294_62473_art_1491801757.jpg",  # 정상 산호 이미지
            "options": ["정상", "백화", "죽은 산호", "조류 과다"],
            "answer": "정상"
        },
        {
            "question": "2. 산호초 백화현상의 주요 원인은 무엇일까요?",
            "image": None,
            "options": ["해수온 상승", "조류 활동 증가", "바닷물 염도 감소", "산소 과다"],
            "answer": "해수온 상승"
        },
        {
            "question": "3. 산호초가 건강할 때 주로 공생하는 생물은 무엇인가요?",
            "image": None,
            "options": ["조류(산호 조류)", "해파리", "상어", "펭귄"],
            "answer": "조류(산호 조류)"
        },
        {
            "question": "4. 백화된 산호초를 보호하기 위해 할 수 있는 활동으로 적절한 것은?",
            "image": None,
            "options": ["해수온 조절", "해양 오염 감소", "산호 채집", "인공 조류 제거"],
            "answer": "해수온 조절"
        }
    ]

    # 사용자의 답변을 저장할 상태 변수
    if 'quiz_answers' not in st.session_state:
        st.session_state['quiz_answers'] = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state['quiz_submitted'] = False

    # 퀴즈 문제 표시 및 답변 받기
    for i, q in enumerate(quiz, 1):
        st.markdown(f"**{q['question']}**")
    
        if q["image"]:
            st.image(q["image"], use_container_width=True)
    
        # 사용자 답변을 session_state에 저장
        st.session_state['quiz_answers'][i] = st.radio("선택하세요", q["options"], key=i, index=None)
        
        st.markdown("---")

    # 제출 버튼
    if st.button("최종 채점"):
        st.session_state['quiz_submitted'] = True

    # 채점 결과 표시
    if st.session_state['quiz_submitted']:
        score = 0
        st.subheader("🌟 채점 결과")
        for i, q in enumerate(quiz, 1):
            user_answer = st.session_state['quiz_answers'].get(i)
            correct_answer = q['answer']
            
            # 사용자 답변이 없을 경우 처리
            if user_answer is None:
                st.markdown(f"**문제 {i}:** 응답이 없습니다.")
                continue

            if user_answer == correct_answer:
                score += 1
                st.markdown(f"✅ **문제 {i}:** 정답입니다! (선택: **{user_answer}**)")
            else:
                st.markdown(f"❌ **문제 {i}:** 오답입니다. (선택: **{user_answer}**, 정답: **{correct_answer}**)")

        st.subheader(f"🏆 최종 점수: {score}/{len(quiz)}")
        st.session_state['quiz_submitted'] = False

# ---------------------------
# 하단: 메타/저작권/주의
# ---------------------------
st.markdown("---")
st.caption(
    "주의: 본 대시보드는 교육/설명 목적입니다. 공식 관측/정책 근거가 필요할 경우 원출처(NOAA, NCEI, NASA 등) 데이터와 원문 레퍼런스를 직접 확인하세요."
)
