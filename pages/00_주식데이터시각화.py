import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# --- 앱 기본 설정 ---
st.set_page_config(page_title="글로벌 Top 10 주가 대시보드", layout="wide")

# --- 앱 제목 및 설명 ---
st.title("글로벌 시가총액 Top 10 기업 주가 변화")
st.write(
    "이 앱은 글로벌 시가총액 상위 10개 기업의 최근 3년간의 주가 변화를 보여줍니다. "
    "주가는 첫 날을 100으로 기준삼아 정규화되어, 기업 간의 성과를 쉽게 비교할 수 있습니다."
)

# --- 데이터 정의 ---
# yfinance에서 사용할 티커 심볼 (2024년 기준, 변동 가능)
# Apple, Microsoft, Alphabet(Google), Amazon, NVIDIA, Meta, Berkshire Hathaway, Eli Lilly, Tesla, Visa
TICKERS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Meta Platforms": "META",
    "Berkshire Hathaway": "BRK-B",
    "Eli Lilly": "LLY",
    "Tesla": "TSLA",
    "Visa": "V"
}

# --- 데이터 로딩 (Streamlit 캐시 사용) ---
@st.cache_data
def load_stock_data(tickers_dict):
    """
    yfinance를 사용하여 지정된 티커의 최근 3년치 주가 데이터를 다운로드합니다.
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=3 * 365)
    
    # yfinance는 티커 리스트를 받습니다.
    ticker_symbols = list(tickers_dict.values())
    
    # 종가('Close') 데이터만 다운로드
    data = yf.download(ticker_symbols, start=start_date, end=end_date)['Close']
    
    # 컬럼 이름을 회사 이름으로 변경
    company_names = {v: k for k, v in tickers_dict.items()}
    data.rename(columns=company_names, inplace=True)
    
    return data.dropna()

# 데이터 로드 실행
try:
    stock_data = load_stock_data(TICKERS)

    # --- 인터랙티브 위젯 ---
    st.sidebar.header("표시할 기업 선택")
    all_companies = sorted(TICKERS.keys())
    selected_companies = st.sidebar.multiselect(
        "기업을 선택하세요:",
        options=all_companies,
        default=all_companies  # 기본으로 모든 기업 선택
    )

    if not selected_companies:
        st.warning("사이드바에서 하나 이상의 기업을 선택해주세요.")
    else:
        # --- 데이터 정규화 ---
        # 선택된 기업의 데이터만 필터링
        filtered_data = stock_data[selected_companies]
        
        # 첫 번째 날의 주가로 나누어 정규화 (시작점을 100으로 설정)
        normalized_data = (filtered_data / filtered_data.iloc[0] * 100)

        # --- 차트 시각화 (Plotly) ---
        st.subheader("주가 성과 비교 (3년간, 시작일 = 100)")
        fig = px.line(
            normalized_data,
            title="정규화된 주가 추이",
            labels={"value": "주가 (정규화)", "variable": "기업", "index": "날짜"}
        )
        fig.update_layout(
            legend_title_text='기업',
            yaxis_title="주가 (시작일 기준 100)",
            xaxis_title="날짜"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- 데이터 테이블 표시 ---
        st.subheader("데이터 보기")
        tab1, tab2 = st.tabs(["정규화된 데이터", "원본 데이터 (종가, $)"])

        with tab1:
            st.dataframe(normalized_data.style.format("{:.2f}"))

        with tab2:
            st.dataframe(filtered_data.style.format("{:.2f}"))

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("네트워크 연결을 확인하거나 잠시 후 다시 시도해주세요.")
