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
    tab1, tab2, tab3 = st.tabs(["MAIN", "한겨레 뉴스", "플래닛 03 뉴스"])

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
            <div style="font-size: medium;">
                <b>1. 온실가스 배출량 줄이기</b><br>
                그렇기 때문에 환경 보호를 위해 실천하는 작고 사소한 것들을 실천하는 것이 좋다. 예를 들면 자가용 보다 대중교통을 이용하는 거나, 자전거를 타고 이동하는 것도 이산화탄소 배출과 온실가스를 줄이는 소소하지만 효과적인 방법 중 하나이다. 또한 불을 꺼 안 쓰는 전기를 절약하거나, 에너지 소비 효율이 좋은 제품을 사용해 전기 절약을 하는 것도 좋다.
                <br><br>
                <b>2. 플라스틱 사용 줄이기</b><br>
                바다에 있는 쓰레기의 약 70%정도가 모두 플라스틱 쓰레기이다. 이 플라스틱 쓰레기들은 계속되는 충격과 마찰로 인해 아주 조그만 플라스틱으로 계속해서 쪼개지는데, 우리는 이것을 미세플라스틱이라고 부른다. 미세플라스틱은 눈에 보이지 않아 산호와 바다 생물들에게 치명적인 위험으로 다가온다. 따라서 플라스틱 사용을 줄이거나 직접적인 해양 봉사활동(쓰레기 줍기 등 바다까지 못가더라도 강, 계곡 등에서 실천)을 통해 바다에 쓰레기 유입을 줄이는 것도 하나의 방법이다.
                <br><br>
                <b>3. 환경 교육과 캠페인</b><br>
                학교에서 외부강사나 교사들이 실시하는 환경 교육과 캠페인을 조금 더 사실적이고 심각성이 보이게 교육을 하는 것도 좋다. 지금 현재 환경 교육이나 캠페인은 지속되는 의무라는 틀 안에서 별로 심각해 보이지 않았다. 그냥 의무라서 하는 거지 라는 생각이 당연하게 드는 것이 이상하지 않은 지금의 교육은 조금 변화할 필요가 있다.
            </div>
            """,
            unsafe_allow_html=True
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
        planet_url = "https://www.planet03.com/post/%EC%8B%9D%EB%9F%89%EC%9C%84%EA%B8%B0-%EB%B0%94%EB%8B%A4%EA%B0%80-%EB%B3%B4%EB%82%B4%EB%8A%94-%EA%B2%BD%EA%B3%A0"
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