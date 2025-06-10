import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 기본 설정
st.set_page_config(
    page_title="스페인 여행 가이드",
    page_icon="🇪🇸",
    layout="wide",
)

# 각 도시에 대한 정보 (좌표, 이미지, 설명, 명소, 음식)를 딕셔너리로 저장
CITIES = {
    '마드리드': {
        'info': """
        스페인의 심장이자 수도인 마드리드는 활기찬 에너지와 예술, 문화가 넘치는 도시입니다.
        세계적인 수준의 미술관부터 아름다운 공원, 맛있는 음식까지 모든 것을 즐길 수 있습니다.
        낮에는 왕궁과 프라도 미술관을 거닐고, 밤에는 타파스 바에서 현지인처럼 즐겨보세요!
        """,
        'image': 'https://images.unsplash.com/photo-1578305698059-9337151a6291?q=80&w=2070&auto=format&fit=crop',
        'coords': [40.4168, -3.7038],
        'attractions': {
            '프라도 미술관': [40.4138, -3.6921],
            '마드리드 왕궁': [40.4179, -3.7141],
            '산 미겔 시장': [40.4155, -3.7099],
            '레티로 공원': [40.4140, -3.6800],
            '푸에르타 델 솔': [40.4167, -3.7033]
        },
        'food': ['하몬 이베리코 (Jamón Ibérico)', '보카디요 데 칼라마레스 (Bocadillo de Calamares)', '츄러스와 초콜라테 (Churros con Chocolate)']
    },
    '바르셀로나': {
        'info': """
        가우디의 도시, 바르셀로나는 지중해의 햇살과 독특한 건축물이 어우러진 매력적인 곳입니다.
        사그라다 파밀리아의 경이로움에 감탄하고, 구엘 공원의 동화 같은 분위기를 느껴보세요.
        고딕 지구의 좁은 골목길을 탐험하며 과거로의 시간 여행을 떠날 수도 있습니다.
        """,
        'image': 'https://images.unsplash.com/photo-1523531294919-427425db6e5a?q=80&w=2070&auto=format&fit=crop',
        'coords': [41.3851, 2.1734],
        'attractions': {
            '사그라다 파밀리아': [41.4036, 2.1744],
            '구엘 공원': [41.4145, 2.1527],
            '고딕 지구': [41.3830, 2.1760],
            '카사 바트요': [41.3916, 2.1650],
            '보케리아 시장': [41.3818, 2.1714]
        },
        'food': ['파에야 (Paella)', '판 콘 토마테 (Pan con Tomate)', '크레마 카탈라나 (Crema Catalana)']
    },
    '세비야': {
        'info': """
        정열적인 플라멩코와 투우의 본고장, 세비야는 안달루시아 지방의 정수를 느낄 수 있는 곳입니다.
        유럽에서 가장 큰 고딕 성당인 세비야 대성당의 웅장함과 스페인 광장의 아름다움은 잊을 수 없는 추억을 선사합니다.
        오렌지 나무가 가득한 거리를 걸으며 세비야의 낭만을 만끽해 보세요.
        """,
        'image': 'https://images.unsplash.com/photo-1563722238495-28828b493036?q=80&w=2070&auto=format&fit=crop',
        'coords': [37.3891, -5.9845],
        'attractions': {
            '세비야 대성당': [37.3858, -5.9931],
            '스페인 광장': [37.3772, -5.9869],
            '알카사르': [37.3833, -5.9904],
            '메트로폴 파라솔': [37.3931, -5.9903],
            '황금의 탑': [37.3822, -5.9961]
        },
        'food': ['가스파초 (Gazpacho)', '살모레호 (Salmorejo)', '에스피나카스 콘 가르반소스 (Espinacas con Garbanzos)']
    },
    '그라나다': {
        'info': """
        이슬람 문화의 마지막 보석, 그라나다는 알함브라 궁전으로 가장 잘 알려져 있습니다.
        나스르 궁의 정교한 아라베스크 장식과 헤네랄리페의 아름다운 정원은 마치 천국을 거니는 듯한 기분을 느끼게 합니다.
        알바이신 지구의 언덕에 올라 노을 지는 알함브라를 바라보는 것은 최고의 경험입니다.
        """,
        'image': 'https://images.unsplash.com/photo-1579961376152-3c5963f23789?q=80&w=1974&auto=format&fit=crop',
        'coords': [37.1773, -3.5986],
        'attractions': {
            '알함브라 궁전': [37.1761, -3.5881],
            '알바이신 지구': [37.1824, -3.5962],
            '그라나다 대성당': [37.1765, -3.5991],
            '사크로몬테': [37.1833, -3.5858],
            '산 니콜라스 전망대': [37.1821, -3.5931]
        },
        'food': ['타파스 (Tapas - 특히 무료 타파스!)', '피오노노 (Pionono)', '하바스 콘 하몬 (Habas con Jamón)']
    }
}


# --- 앱 UI 구성 ---

# 제목
st.title("🇪🇸 스페인 주요 관광지 가이드")
st.markdown("---")

# 사이드바
st.sidebar.header("✈️ 도시를 선택하세요")
selected_city = st.sidebar.selectbox(
    '가고 싶은 도시는 어디인가요?',
    list(CITIES.keys())
)

# 선택된 도시에 대한 정보 가져오기
city_data = CITIES[selected_city]

# 메인 화면 구성
st.header(f"✨ {selected_city}에 오신 것을 환영합니다!")
st.image(city_data['image'], caption=f'{selected_city}의 아름다운 풍경')

st.info(city_data['info'])

st.markdown("---")

# 주요 명소와 추천 음식을 두 개의 컬럼으로 나누어 표시
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 추천 명소")
    for attraction in city_data['attractions'].keys():
        st.markdown(f"- {attraction}")

with col2:
    st.subheader("🍴 꼭 먹어봐야 할 음식")
    for food in city_data['food']:
        st.markdown(f"- {food}")

st.markdown("---")

# Folium을 사용한 지도 생성
st.subheader("📍 주요 관광지 지도")
map_center = city_data['coords']
m = folium.Map(location=map_center, zoom_start=14)

# 지도에 명소 마커 추가
for name, coords in city_data['attractions'].items():
    folium.Marker(
        location=coords,
        popup=folium.Popup(name, max_width=200),
        tooltip=name,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=1200, height=500)

st.sidebar.markdown("---")
st.sidebar.info("이 가이드는 Streamlit과 Folium을 사용하여 제작되었습니다.")
