import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="time",layout="wide",page_icon="📅")

# 2022년 데이터로 데이터셋을 로드합니다
df = pd.read_csv('./data/시계열분석용데이터.csv')

  # 실제 데이터 파일의 경로로 바꿔주세요

# Streamlit 애플리케이션 제목
col1, col2, col3 = st.columns([1,5,2])
with col2:
    st.markdown("""
    <style>
    .big-font {
        font-size:35px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<b><p class="big-font">📅 2023년 시도-시군별 민원 건수 예측 그래프</p></b>', unsafe_allow_html=True)
    
    
    sido_options = ["선택","서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",  "경기도", "강원도",
                "충청북도", "충청남도", "전라북도", "전라남도", "경상북도",  "경상남도", "제주특별자치도"]

    sigun_list = {
        "서울특별시": ["선택", "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
        "부산광역시": ["선택", "강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
        "대구광역시": ["선택", "남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구"],
        "인천광역시": ["선택", "강화군", "계양구", "미추홀구", "남동구", "동구", "부평구", "서구", "연수구", "옹진군", "중구"],
        "광주광역시": ["선택", "광산구", "남구", "동구", "북구", "서구"],
        "대전광역시": ["선택", "대덕구", "동구", "서구", "유성구", "중구"],
        "울산광역시": ["선택", "남구", "동구", "북구", "울주군", "중구"],
        "세종특별자치시": ["선택", "세종시"],
        "경기도": ["선택", "가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"],
        "강원도": ["선택", "강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
        "충청북도": ["선택", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "증평군", "진천군", "청주시", "충주시"],
        "충청남도": ["선택", "계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "예산군", "천안시", "청양군", "태안군", "홍성군"],
        "전라북도": ["선택", "고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
        "전라남도": ["선택", "강진군", "고흥군", "곡성군", "광양시", "구례군", "나주시", "담양군", "목포시", "무안군", "보성군", "순천시", "신안군", "여수시", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"],
        "경상북도": ["선택", "경산시", "경주시", "고령군", "구미시", "군위군", "김천시", "문경시", "봉화군", "상주시", "성주군", "안동시", "영덕군", "영양군", "영주시", "영천시", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군"],
        "경상남도": ["선택", "거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
        "제주특별자치도": ["선택", "서귀포시", "제주시"]
    }

    
    col4,col5 = st.columns([1,1])
    with col4:
        selected_sido = st.selectbox("시도명을 선택하세요", sido_options)
        sigun = sigun_list.get(selected_sido, [])
    with col5:
        selected_sigun = st.selectbox("시군구를 선택하세요", sigun)
    # 드롭다운으로 지역을 선택합니다
    

    # 선택한 지역에 기반하여 데이터프레임을 필터링합니다
    filtered_df = df[(df['시군구_시도명'] == selected_sido) & (df['시군구_시군명'] == selected_sigun)]
    filtered_df['날짜'] = pd.to_datetime(filtered_df['날짜'], format='%Y-%m')
    filtered_df.set_index('날짜', inplace=True)

    # 월별 민원 건수 계산
    #monthly_data = filtered_df['민원_전체건수'].resample('M').sum()
    # 날짜를 같은 월끼리 묶어서 민원 건수를 카운트
    monthly_counts = filtered_df.groupby('날짜')['민원_전체건수'].sum()

    # 결과를 출력
    
    # 월별 민원 건수 시각화
    st.write('### 월별 민원 건수(2022년)')
    st.line_chart(monthly_counts)

    if not monthly_counts.empty:  # monthly_counts가 비어있지 않다면
    # ARIMA 모델 생성 및 훈련
        model = ARIMA(monthly_counts, order=(5, 1, 0))  # 필요에 따라 order를 조절
        model_fit = model.fit()

    # 2023년 예측
        n_forecast = 12  # 2023년 1월부터 12월까지 예측
        forecast = model_fit.forecast(steps=n_forecast)

        # 2023년 예측 데이터를 데이터프레임으로 생성
        forecast_dates = pd.date_range(start='2023-01', periods=n_forecast, freq='M')
        forecast_df = pd.DataFrame({'날짜': forecast_dates, '예측된_민원_전체건수_2023': forecast})

        # 2023년 예측 데이터 시각화
        st.write('# 2023년 민원 건수 예측')
        st.line_chart(forecast_df.set_index('날짜'))

        # 2023년 예측 데이터 표시
        st.write('## 2023년 민원 건수 예측 데이터')
        st.dataframe(forecast_df)
