# 삭제할 부분
import matplotlib.font_manager as fm

# 폰트 설정 (이 부분을 통째로 삭제)
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
except Exception as e:
    st.warning(f"폰트 설정 중 오류가 발생했습니다: {e}")
    font_name = 'sans-serif'