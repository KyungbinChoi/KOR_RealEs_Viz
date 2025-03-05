# all code 
import xmltodict
import json
import requests
import pandas as pd
import itertools
import time, os, sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from urllib.parse import unquote

base_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
update_date = sys.argv[1]

file_path = "/opt/airflow/dataset/results.pkl"
print(f"Checking file path: {file_path}")
if os.path.exists(f"/opt/airflow/dataset/results.pkl"):
    start_date = update_date
else:
    start_date = "2020-01-01"

serviceKey = os.getenv("API_KEY")

API_KEY = unquote(serviceKey)
if not API_KEY:
    raise ValueError("API Key is missing. Please set the API_KEY environment variable.")

def get_month_list(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Initialize list to hold the months
    month_list = []

    # Iterate from start to end date by month
    current = start
    while current <= end:
        month_list.append(current.strftime("%Y%m"))
        # Move to the next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return month_list

def get_df(lawd_cd, deal_ymd, max_retries=5, sleep_time=1):
    """ 특정 지역과 날짜의 아파트 거래 데이터를 요청하고 DataFrame으로 반환 """
    base_url = f"http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?serviceKey={API_KEY}&LAWD_CD={lawd_cd}&DEAL_YMD={deal_ymd}&pageNo=1&numOfRows=9999"

    for attempt in range(max_retries):
        try:
            res = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

            # HTTP 상태 코드 확인
            if res.status_code == 200:
                data = json.loads(json.dumps(xmltodict.parse(res.text)))

                # 데이터 존재 여부 확인
                if (
                    "response" not in data or
                    "body" not in data["response"] or
                    "items" not in data["response"]["body"] or
                    "item" not in data["response"]["body"]["items"]
                ):
                    print(f"🚨 No data for LAWD_CD={lawd_cd}, DEAL_YMD={deal_ymd} - Skipping")
                    return pd.DataFrame()  # 빈 데이터프레임 반환

                item = data["response"]["body"]["items"]["item"]

                # 🔹 데이터가 단일 객체(딕셔너리)일 경우 리스트로 변환
                if isinstance(item, dict):
                    item = [item]

                df = pd.DataFrame(item)
                return df

            else:
                print(f"⚠️ API 요청 실패 (HTTP {res.status_code}), 재시도 {attempt + 1}/{max_retries}")

        except (requests.exceptions.RequestException, KeyError, TypeError, ValueError) as e:
            print(f"⚠️ 요청 오류 발생: {e}, 재시도 {attempt + 1}/{max_retries}")

        time.sleep(sleep_time * (attempt + 1))  # 지수적 백오프 (점점 긴 대기 시간)

    print(f"🚨 최종 요청 실패: LAWD_CD={lawd_cd}, DEAL_YMD={deal_ymd}")
    return pd.DataFrame()  # 최종적으로 실패하면 빈 데이터프레임 반환

def get_multiregion_timeseries_df(lawd_cd_list, deal_ymd_list, sleep_time=1):
    """ 여러 지역과 여러 개월 데이터를 수집하여 하나의 DataFrame으로 반환 """
    df_list = []
    total_requests = len(lawd_cd_list) * len(deal_ymd_list)

    for idx, (cd, month) in enumerate(itertools.product(lawd_cd_list, deal_ymd_list)):
        print(f"[{idx+1}/{total_requests}] Fetching: region={cd}, month={month}")

        smp_df = get_df(cd, month)

        if not smp_df.empty:
            df_list.append(smp_df)

        time.sleep(sleep_time)  # 요청 간 대기 (서버 부하 방지)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()  # 모든 요청이 실패하면 빈 DataFrame 반환


if __name__ == "__main__":

    
    print(start_date, update_date)
    deal_ymd_list = get_month_list(start_date, update_date)

    # 지역 코드 목록 (서울, 경기)
    region_codes = [
        "11110", "11140", "11170", "11200", "11215", "11230", "11260", "11290", "11305", "11320",
        "11350", "11380", "11410", "11440", "11470", "11500", "11530", "11545", "11560", "11590",
        "11620", "11650", "11680", "11710", "11740",  # 서울특별시
    ]
    region_codes2 = ["41111", "41113", "41115", "41117", "41131", "41133", "41135", "41150", "41171", "41173",
        "41192", "41194", "41196", "41210", "41220", "41250", "41271", "41273", "41281", "41285", "41287", "41290",
        "41310", "41360", "41370", "41390", "41410", "41430", "41450", "41461", "41463", "41465",
        # 경기도 (일부 지역 제외)
    ]

    # API 요청 실행
    smp_timeseries_seoul = get_multiregion_timeseries_df(region_codes, deal_ymd_list)
    smp_timeseries_gyg = get_multiregion_timeseries_df(region_codes2, deal_ymd_list)

    results_df = pd.concat([smp_timeseries_seoul,smp_timeseries_gyg]).reset_index(drop=True)
    results_df.to_pickle(f"/opt/airflow/dataset/results.pkl")
    print('End Data Fetching & Saving raw data set')