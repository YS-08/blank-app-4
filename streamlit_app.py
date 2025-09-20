import streamlit as st
import streamlit.components.v1 as components
import os

# Streamlit 페이지 설정을 'wide' 레이아웃으로 변경
st.set_page_config(layout="wide")

# 사이드바 내용 추가 (모두 비워둠)
with st.sidebar:
    st.markdown("")

def create_dashboard():
    st.title("산호초 : 나 지금 과로사 중 🫠")
    
    st.markdown(
        """
        ### 📖 문제 제기

        지구 온난화로 인한 해수온 상승은 생태계 전반에 심각한 영향을 미치고 있습니다.
        그 중에서도 산호초 백화 현상은 가장 대표적이고 우려되는 문제로 지적되고 있죠.
        해양 생물의 약 25%가 서식하는 중요한 바다속 생태계로서 이러한 산호초의 붕괴는 다양한 사회/경제적 피해 또한 초래합니다.

        이미 전 세계 산호 84%가 하얗게 죽어가고 있으며 34만8천㎢에 달하는 세계 최대 산호초 군락지인 그레이트 배리어 리프의 산호들 또한 대량의 백화 현상을 보이고 있습니다.
        """
    )
    
    # 총 3개의 탭 생성
    tab1, tab2, tab3 = st.tabs(["메인", "한겨레 뉴스", "플래닛 03 뉴스"])

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

        st.subheader("💡 해결 방안 및 실천 과제")
        st.markdown(
            """
            **1. 온실가스 배출량 줄이기**
            * 자가용 보다 대중교통 이용하기
            * 자전거 타고 이동하기
            * 불을 끄거나 어댑터를 뽑아 안 쓰는 전기 절약하기
            * 에너지 소비 효율 좋은 제품 사용하기

            **2. 환경 개선하기**
            * 플라스틱 사용 줄이기
            * 해양 봉사활동 (쓰레기 줍기)

            **3. 인식 개선**
            * 환경 교육과 캠페인
            * SNS, TV 광고 등을 통한 문제 알리기
            """
        )

    with tab2:
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
            

    with tab3:
        st.subheader("플래닛 03: '식량위기, 바다가 보내는 경고' 기사")
        planet_url = "https://www.planet03.com/post/%EC%8B%9D%EB%9F%89%EC%9C%84%EA%B8%B0-%EB%B0%94%EB%8B%A4%EA%B0%80-%EB%B3%B4%EB%84%B4%EB%8A%94-%EA%B2%BD%EA%B3%A0"
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

if __name__ == "__main__":
    create_dashboard()