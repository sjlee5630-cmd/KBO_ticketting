import streamlit as st
import calendar
from datetime import date, timedelta
import pandas as pd

st.set_page_config(
    page_title="SSG 랜더스 2026",
    page_icon="⚾",
    layout="wide",
)

# ── 전역 CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

/* 사이드바 배경 */
[data-testid="stSidebar"] {
    background: #12131f !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 사이드바 내부 패딩 줄이기 */
[data-testid="stSidebarContent"] {
    padding: 0 12px !important;
}

/* Streamlit 버튼 기본 스타일 완전 덮어쓰기 */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    margin-bottom: 5px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    text-align: left !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.05) !important;
    color: #b0b8cc !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
    letter-spacing: 0.3px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    cursor: pointer !important;
    line-height: 1.3 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.10) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: #ffffff !important;
    transform: translateX(2px) !important;
}

[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* 활성(primary) 버튼 */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #CC0000 !important;
    border-color: #CC0000 !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    box-shadow: 0 4px 14px rgba(204,0,0,0.35) !important;
    transform: none !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #e60000 !important;
    border-color: #e60000 !important;
    transform: translateX(2px) !important;
}
</style>
""", unsafe_allow_html=True)

# ── 티켓팅 정보 ──────────────────────────────────────────────
TICKET_INFO = {
    "홈": {
        "venue": "인천 SSG 랜더스필드 (문학)",
        "presale_days": 7,
        "presale_time": "오전 10:00 (배티 선예매)",
        "general_time": "오전 10:00 (일반예매, 경기 5일 전)",
        "url": "https://ticket.ssg.com",
        "url_label": "SSG 공식 티켓",
    },
    "롯데": {
        "venue": "사직야구장 (부산)",
        "presale_days": 14,
        "presale_time": "오전 10:00 (선예매) / 오후 14:00 (일반)",
        "general_time": "오후 14:00",
        "url": "https://www.giantsclub.com",
        "url_label": "롯데 자이언츠 공식",
    },
    "LG": {
        "venue": "잠실야구장 (서울)",
        "presale_days": 7,
        "presale_time": "오전 10:00 (추정)",
        "general_time": "오전 10:00 (추정)",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "두산": {
        "venue": "잠실야구장 (서울)",
        "presale_days": 7,
        "presale_time": "오전 11:00 (추정)",
        "general_time": "오전 11:00 (추정)",
        "url": "https://ticket.interpark.com",
        "url_label": "인터파크 티켓",
    },
    "키움": {
        "venue": "고척스카이돔 (서울)",
        "presale_days": 7,
        "presale_time": "오전 11:00 (추정)",
        "general_time": "오전 11:00 (추정)",
        "url": "https://ticket.interpark.com",
        "url_label": "인터파크 티켓",
    },
    "kt": {
        "venue": "수원 KT위즈파크",
        "presale_days": 7,
        "presale_time": "오전 10:00 (추정)",
        "general_time": "오전 10:00 (추정)",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "한화": {
        "venue": "한화생명이글스파크 (대전)",
        "presale_days": 7,
        "presale_time": "오전 10:00 (추정)",
        "general_time": "오전 10:00 (추정)",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "삼성": {
        "venue": "라이온즈파크 (대구)",
        "presale_days": 7,
        "presale_time": "오전 10:00 (추정)",
        "general_time": "오전 10:00 (추정)",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "KIA": {
        "venue": "기아 챔피언스 필드 (광주)",
        "presale_days": 7,
        "presale_time": "오전 10:00 (추정)",
        "general_time": "오전 10:00 (추정)",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "NC": {
        "venue": "창원 NC파크",
        "presale_days": 7,
        "presale_time": "오전 11:00 (추정)",
        "general_time": "오전 11:00 (추정)",
        "url": "https://ticket.ncdinos.com",
        "url_label": "NC 다이노스 공식",
    },
}

# ── 경기 일정 (3월~10월 전체) ────────────────────────────────
SCHEDULE_RAW = [
    # ── 3월 ──
    (3, 28, "KIA",  "홈",   True),
    (3, 29, "KIA",  "홈",   True),
    (3, 31, "키움", "홈",   False),
    # ── 4월 ──
    (4,  1, "키움", "홈",   False),
    (4,  2, "키움", "홈",   False),
    (4,  3, "롯데", "원정", False),
    (4,  4, "롯데", "원정", True),
    (4,  5, "롯데", "원정", True),
    (4,  7, "한화", "홈",   False),
    (4,  8, "한화", "홈",   False),
    (4,  9, "한화", "홈",   False),
    (4, 10, "LG",   "원정", False),
    (4, 11, "LG",   "원정", True),
    (4, 14, "삼성", "원정", False),
    (4, 15, "삼성", "원정", False),
    (4, 16, "삼성", "원정", False),
    (4, 17, "KIA",  "원정", False),
    (4, 18, "KIA",  "원정", True),
    (4, 19, "KIA",  "원정", True),
    (4, 21, "한화", "홈",   False),
    (4, 22, "한화", "홈",   False),
    (4, 23, "한화", "홈",   False),
    (4, 24, "LG",   "홈",   False),
    (4, 25, "LG",   "홈",   True),
    (4, 26, "LG",   "홈",   True),
    (4, 28, "키움", "홈",   False),
    (4, 29, "키움", "홈",   False),
    (4, 30, "키움", "홈",   False),
    # ── 5월 ──
    (5,  1, "삼성", "홈",   False),
    (5,  2, "삼성", "홈",   True),
    (5,  3, "삼성", "홈",   True),
    (5,  5, "두산", "원정", False),
    (5,  6, "두산", "원정", False),
    (5,  7, "두산", "원정", False),
    (5,  8, "NC",   "홈",   False),
    (5,  9, "NC",   "홈",   True),
    (5, 10, "NC",   "홈",   True),
    (5, 12, "kt",   "홈",   False),
    (5, 13, "kt",   "홈",   False),
    (5, 14, "kt",   "홈",   False),
    (5, 15, "롯데", "홈",   False),
    (5, 16, "롯데", "홈",   True),
    (5, 17, "롯데", "홈",   True),
    (5, 19, "두산", "홈",   False),
    (5, 20, "두산", "홈",   False),
    (5, 21, "두산", "홈",   False),
    (5, 22, "kt",   "원정", False),
    (5, 23, "kt",   "원정", True),
    (5, 24, "kt",   "원정", True),
    (5, 26, "NC",   "원정", False),
    (5, 27, "NC",   "원정", False),
    (5, 28, "NC",   "원정", False),
    (5, 29, "KIA",  "홈",   False),
    (5, 30, "KIA",  "홈",   True),
    (5, 31, "KIA",  "홈",   True),
    # ── 6월 ──
    (6,  2, "롯데", "원정", False),
    (6,  3, "롯데", "원정", False),
    (6,  4, "롯데", "원정", False),
    (6,  5, "삼성", "홈",   False),
    (6,  6, "삼성", "홈",   True),
    (6,  7, "삼성", "홈",   True),
    (6,  9, "두산", "홈",   False),
    (6, 10, "두산", "홈",   False),
    (6, 11, "두산", "홈",   False),
    (6, 12, "키움", "원정", False),
    (6, 13, "키움", "원정", True),
    (6, 16, "LG",   "원정", False),
    (6, 17, "LG",   "원정", False),
    (6, 18, "LG",   "원정", False),
    (6, 19, "한화", "원정", False),
    (6, 20, "한화", "원정", True),
    (6, 21, "한화", "원정", True),
    (6, 23, "NC",   "홈",   False),
    (6, 24, "NC",   "홈",   False),
    (6, 25, "NC",   "홈",   False),
    (6, 26, "kt",   "홈",   False),
    (6, 27, "kt",   "홈",   True),
    (6, 28, "kt",   "홈",   True),
    (6, 30, "KIA",  "원정", False),
    # ── 7월 ──
    (7,  1, "KIA",  "원정", False),
    (7,  2, "KIA",  "원정", False),
    (7,  3, "삼성", "홈",   False),
    (7,  4, "삼성", "홈",   True),
    (7,  5, "삼성", "홈",   True),
    (7,  7, "두산", "원정", False),
    (7,  8, "두산", "원정", False),
    (7,  9, "두산", "원정", False),
    # 7/10~13 올스타 휴식기
    (7, 14, "KIA",  "홈",   False),
    (7, 15, "KIA",  "홈",   False),
    (7, 16, "KIA",  "홈",   False),
    (7, 17, "KIA",  "홈",   False),
    (7, 21, "롯데", "원정", False),
    (7, 22, "롯데", "원정", False),
    (7, 23, "롯데", "원정", False),
    (7, 24, "NC",   "홈",   False),
    (7, 25, "NC",   "홈",   True),
    (7, 26, "NC",   "홈",   True),
    (7, 28, "두산", "홈",   False),
    (7, 29, "두산", "홈",   False),
    (7, 30, "두산", "홈",   False),
    (7, 31, "키움", "원정", False),
    # ── 8월 ──
    (8,  1, "키움", "원정", True),
    (8,  4, "한화", "홈",   False),
    (8,  5, "한화", "홈",   False),
    (8,  6, "한화", "홈",   False),
    (8,  7, "LG",   "홈",   False),
    (8,  8, "LG",   "홈",   True),
    (8,  9, "LG",   "홈",   True),
    (8, 11, "kt",   "홈",   False),
    (8, 12, "kt",   "홈",   False),
    (8, 13, "kt",   "홈",   False),
    (8, 14, "NC",   "원정", False),
    (8, 15, "NC",   "원정", True),
    (8, 16, "NC",   "원정", True),
    (8, 18, "키움", "홈",   False),
    (8, 19, "키움", "홈",   False),
    (8, 20, "키움", "홈",   False),
    (8, 21, "롯데", "홈",   False),
    (8, 22, "롯데", "홈",   True),
    (8, 23, "롯데", "홈",   True),
    (8, 25, "삼성", "원정", False),
    (8, 26, "삼성", "원정", False),
    (8, 27, "삼성", "원정", False),
    (8, 28, "LG",   "원정", False),
    (8, 29, "LG",   "원정", True),
    (8, 30, "LG",   "원정", True),
    # ── 9월 ──
    (9,  1, "kt",   "원정", False),
    (9,  2, "kt",   "원정", False),
    (9,  3, "kt",   "원정", False),
    (9,  4, "두산", "홈",   False),
    (9,  5, "두산", "홈",   True),
    (9,  6, "두산", "홈",   True),
    (9,  8, "한화", "원정", False),
    (9,  9, "한화", "원정", False),
    (9, 10, "한화", "원정", False),
    (9, 11, "KIA",  "홈",   False),
    (9, 12, "KIA",  "홈",   True),
    (9, 13, "KIA",  "홈",   True),
    (9, 15, "롯데", "홈",   False),
    (9, 16, "롯데", "홈",   False),
    (9, 17, "롯데", "홈",   False),
    (9, 18, "NC",   "원정", False),
    (9, 19, "NC",   "원정", True),
    (9, 22, "키움", "원정", False),
    (9, 23, "키움", "원정", False),
    (9, 24, "키움", "원정", False),
    (9, 25, "LG",   "홈",   False),
    (9, 26, "LG",   "홈",   True),
    (9, 27, "LG",   "홈",   True),
    (9, 29, "kt",   "홈",   False),
    (9, 30, "kt",   "홈",   False),
    # ── 10월 (포스트시즌 전 잔여 정규시즌) ──
    (10,  1, "kt",   "홈",   False),
    (10,  2, "한화", "원정", False),
    (10,  3, "한화", "원정", True),
    (10,  4, "한화", "원정", True),
]

SPECIAL = {
    (7, 10): "⭐ 올스타 휴식기",
    (7, 11): "⭐ 올스타 휴식기",
    (7, 12): "⭐ 올스타 휴식기",
    (7, 13): "⭐ 올스타 휴식기",
}

MONTHS = {
    3:  "3월",
    4:  "4월",
    5:  "5월",
    6:  "6월",
    7:  "7월",
    8:  "8월",
    9:  "9월",
    10: "10월",
}

DOW_KR = ["월", "화", "수", "목", "금", "토", "일"]


def build_sched():
    d = {}
    for m, day, opp, loc, hot in SCHEDULE_RAW:
        d.setdefault((m, day), []).append({"opp": opp, "loc": loc, "hot": hot})
    return d


SCHEDULE = build_sched()


def count_games(month_num):
    return sum(1 for (m, _), gs in SCHEDULE.items() for _ in gs if m == month_num)


def fmt_date(dt):
    return "{0}월 {1}일".format(dt.month, dt.day)


def presale_date_str(m, d, ti_key):
    days = TICKET_INFO.get(ti_key, {}).get("presale_days", 7)
    dt = date(2026, m, d) - timedelta(days=days)
    return fmt_date(dt)


# ── 달력 HTML ────────────────────────────────────────────────
def make_sunday_first_cal(year, month):
    """일요일 시작 달력 생성 (calendar.monthcalendar는 월요일 시작이므로 변환)"""
    import datetime
    cal_mon = calendar.monthcalendar(year, month)
    # 각 주를 [일,월,화,수,목,금,토] 순으로 재배열
    # monthcalendar: [월,화,수,목,금,토,일] -> 마지막(일)을 맨 앞으로
    weeks_sun = []
    for week in cal_mon:
        sun = week[6]  # 일요일
        new_week = [sun] + week[:6]  # 일,월,화,수,목,금,토
        weeks_sun.append(new_week)
    # 첫 주 앞에 일요일이 없는데 이전 달 날짜로 채워진 경우 처리
    # 마지막 주도 동일하게 확인
    return weeks_sun

def render_calendar_html(month):
    cal = make_sunday_first_cal(2026, month)
    # 일요일 시작 헤더: 일,월,화,수,목,금,토
    dow_labels_sun = ["일", "월", "화", "수", "목", "금", "토"]

    header_cells = ""
    for i, label in enumerate(dow_labels_sun):
        txt_color = "#ffaaaa" if i == 0 else ("#aaccff" if i == 6 else "white")
        header_cells += (
            '<th style="background:#CC0000;color:{c};padding:10px 4px;'
            'font-size:13px;font-weight:600;text-align:center;letter-spacing:1px;">'
            "{l}</th>"
        ).format(c=txt_color, l=label)

    body_rows = ""
    for week in cal:
        cells = ""
        for wi, day in enumerate(week):
            if day == 0:
                cells += (
                    '<td style="background:#f5f5f5;min-height:80px;'
                    'border:1px solid #e8e8e8;padding:6px;"></td>'
                )
                continue

            is_sun = wi == 0
            is_sat = wi == 6
            num_color = "#cc0000" if is_sun else ("#1a56db" if is_sat else "#1a1a1a")
            cell_bg = "#fffaf9" if is_sun else ("#f5f8ff" if is_sat else "#ffffff")

            inner = (
                '<div style="font-size:14px;font-weight:700;'
                'color:{c};margin-bottom:4px;">{d}</div>'
            ).format(c=num_color, d=day)

            sp = SPECIAL.get((month, day))
            if sp:
                inner += (
                    '<div style="font-size:10px;background:#ffe8b2;color:#7a5000;'
                    'border-radius:4px;padding:2px 5px;margin-bottom:3px;'
                    'font-weight:600;">{s}</div>'
                ).format(s=sp)

            for g in SCHEDULE.get((month, day), []):
                opp = g["opp"]
                loc = g["loc"]
                ti_key = "홈" if loc == "홈" else opp
                url = TICKET_INFO.get(ti_key, {}).get("url", "#")

                # 강조 조건 판별
                is_weekend_home = loc == "홈" and (is_sat or is_sun)
                is_jamsil = loc == "원정" and opp in ("LG", "두산")

                if is_weekend_home:
                    bg = "#fff8e1"
                    border = "#f59e0b"
                    color = "#7a4f00"
                    label = "⭐ 홈 vs {o}  주말홈".format(o=opp)
                elif is_jamsil:
                    bg = "#f3e8ff"
                    border = "#7c3aed"
                    color = "#4c1d95"
                    label = "🗼 원정 @{o}  잠실".format(o=opp)
                elif loc == "홈":
                    bg = "#fff0ee"
                    border = "#CC0000"
                    color = "#7a0000"
                    label = "홈 vs {o}".format(o=opp)
                else:
                    bg = "#eef3ff"
                    border = "#1a56db"
                    color = "#1a3a7a"
                    label = "원정 @{o}".format(o=opp)

                inner += (
                    '<a href="{url}" target="_blank" '
                    'style="display:block;background:{bg};'
                    'border-left:3px solid {brd};'
                    'color:{c};text-decoration:none;font-size:11px;'
                    'padding:3px 5px;border-radius:3px;margin-bottom:3px;'
                    'line-height:1.4;font-weight:500;">'
                    "{lbl}</a>"
                ).format(url=url, bg=bg, brd=border, c=color, lbl=label)

            cells += (
                '<td style="background:{bg};vertical-align:top;padding:6px;'
                'min-height:80px;border:1px solid #e8e8e8;width:14.28%;">'
                "{inner}</td>"
            ).format(bg=cell_bg, inner=inner)

        body_rows += "<tr>{cells}</tr>".format(cells=cells)

    return (
        '<div style="border-radius:10px;overflow:hidden;'
        'box-shadow:0 2px 8px rgba(0,0,0,0.10);margin-bottom:4px;">'
        '<table style="width:100%;border-collapse:collapse;table-layout:fixed;">'
        "<thead><tr>{hdr}</tr></thead>"
        "<tbody>{body}</tbody>"
        "</table></div>"
    ).format(hdr=header_cells, body=body_rows)


# ── Session State 초기화 ─────────────────────────────────────
if "sel_month" not in st.session_state:
    st.session_state.sel_month = 3


# ── 사이드바 ────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:20px 0 10px;">'
        '<div style="font-size:36px;line-height:1;">⚾</div>'
        '<div style="font-size:18px;font-weight:900;color:#ffffff;margin-top:6px;letter-spacing:1px;">'
        "SSG 랜더스</div>"
        '<div style="font-size:11px;color:#888;margin-top:3px;letter-spacing:2px;">2026 SEASON</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.10);margin:6px 0 14px;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:10px;color:#666;letter-spacing:2px;'
        'margin-bottom:8px;padding-left:2px;text-transform:uppercase;">월 선택</div>',
        unsafe_allow_html=True,
    )

    for month_num, month_name in MONTHS.items():
        gc = count_games(month_num)
        is_active = st.session_state.sel_month == month_num

        # 버튼 텍스트: 월 이름 왼쪽, 경기수 오른쪽 (공백 패딩으로 구분)
        btn_label = "{mn}   {gc}경기".format(mn=month_name, gc=gc)

        clicked = st.button(
            btn_label,
            key="sidebar_btn_{m}".format(m=month_num),
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )
        if clicked:
            st.session_state.sel_month = month_num
            st.rerun()

    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.15);margin:14px 0 12px;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:12px;color:#aaaaaa;line-height:1.8;padding:0 4px;">'
        '<div style="color:#ffffff;font-weight:600;margin-bottom:6px;">배티 선예매 안내</div>'
        "경기 <b style='color:#ffcccc;'>7일 전</b> 오전 10:00<br>"
        "SSG 공식 앱 / ticket.ssg.com<br>"
        '<br><div style="color:#ffffff;font-weight:600;margin-bottom:4px;">범례</div>'
        '<span style="display:inline-block;width:10px;height:10px;'
        'background:#fff0ee;border-left:3px solid #CC0000;'
        'vertical-align:middle;margin-right:4px;"></span>홈경기<br>'
        '<span style="display:inline-block;width:10px;height:10px;'
        'background:#eef3ff;border-left:3px solid #1a56db;'
        'vertical-align:middle;margin-right:4px;"></span>원정경기<br>'
        '<span style="display:inline-block;width:10px;height:10px;'
        'background:#fffbe6;border-left:3px solid #f59e0b;'
        'vertical-align:middle;margin-right:4px;"></span>주말홈경기<br>'
        '<span style="display:inline-block;width:10px;height:10px;'
        'background:#f5f0ff;border-left:3px solid #7c3aed;'
        'vertical-align:middle;margin-right:4px;"></span>잠실원정(LG·두산)'
        "</div>",
        unsafe_allow_html=True,
    )


# ── 메인 컨텐츠 ──────────────────────────────────────────────
sel = st.session_state.sel_month
sel_label = MONTHS[sel]

st.markdown(
    '<h1 style="color:#CC0000;margin-bottom:2px;font-size:26px;">'
    "⚾ SSG 랜더스 2026 — {m} 경기 일정</h1>"
    '<p style="color:#888;font-size:13px;margin-top:0;">'
    "경기 뱃지를 클릭하면 티켓팅 사이트로 이동합니다 | 배티 회원 기준</p>".format(m=sel_label),
    unsafe_allow_html=True,
)

# 달력
cal_html = render_calendar_html(sel)
num_weeks = len(calendar.monthcalendar(2026, sel))
cal_height = 60 + num_weeks * 95
st.components.v1.html(cal_html, height=cal_height, scrolling=False)

# ── 티켓팅 상세 테이블 ────────────────────────────────────────
st.markdown("---")
st.markdown("#### 📋 {m} 티켓팅 상세".format(m=sel_label))

col_f1, col_f2, _ = st.columns([1, 1, 6])
with col_f1:
    show_home = st.checkbox("홈", value=True, key="fh_{m}".format(m=sel))
with col_f2:
    show_away = st.checkbox("원정", value=True, key="fa_{m}".format(m=sel))

month_games = sorted(
    [
        (d, g)
        for (mm, d), gs in SCHEDULE.items()
        for g in gs
        if mm == sel
    ],
    key=lambda x: x[0],
)

rows = []
for day, g in month_games:
    loc = g["loc"]
    opp = g["opp"]
    if loc == "홈" and not show_home:
        continue
    if loc == "원정" and not show_away:
        continue

    weekday_num = date(2026, sel, day).weekday()
    is_weekend = weekday_num >= 5
    dow = DOW_KR[weekday_num]
    date_str = "{m}/{d}({w})".format(m=sel, d=day, w=dow)
    ti_key = "홈" if loc == "홈" else opp
    ti = TICKET_INFO.get(ti_key, {})
    presale = presale_date_str(sel, day, ti_key)

    is_weekend_home = loc == "홈" and is_weekend
    is_jamsil = loc == "원정" and opp in ("LG", "두산")

    if is_weekend_home:
        highlight = "⭐ 주말홈"
    elif is_jamsil:
        highlight = "🗼 잠실"
    else:
        highlight = ""

    rows.append({
        "날짜":         date_str,
        "홈/원정":      loc,
        "상대팀":       opp,
        "강조":         highlight,
        "구장":         ti.get("venue", "-"),
        "선예매 오픈일": presale,
        "오픈 시간":    ti.get("presale_time", "-"),
        "예매 링크":    ti.get("url", "#"),
    })

if rows:
    df = pd.DataFrame(rows)

    def highlight_rows(row):
        if row["강조"] == "⭐ 주말홈":
            return ["background-color: #fffbe6; color: #7a4f00"] * len(row)
        elif row["강조"] == "🗼 잠실":
            return ["background-color: #f5f0ff; color: #4c1d95"] * len(row)
        return [""] * len(row)

    styled_df = df.style.apply(highlight_rows, axis=1)

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "예매 링크": st.column_config.LinkColumn(
                "예매 링크", display_text="→ 예매하기"
            )
        },
    )
else:
    st.info("선택한 필터에 해당하는 경기가 없습니다.")

# ── 원정 구단별 예매처 ──────────────────────────────────────
st.markdown("---")
with st.expander("🏟️ 구단별 원정 예매처 전체 안내"):
    cols = st.columns(3)
    away_teams = [t for t in TICKET_INFO if t != "홈"]
    for i, team in enumerate(away_teams):
        ti = TICKET_INFO[team]
        with cols[i % 3]:
            st.markdown(
                "**{t}** | {v}\n\n"
                "- 예매 오픈: `{pt}`\n"
                "- [{ul}]({url})\n".format(
                    t=team,
                    v=ti["venue"],
                    pt=ti["presale_time"],
                    ul=ti["url_label"],
                    url=ti["url"],
                )
            )

st.caption(
    "⚠️ 경기 일정은 우천 등으로 변경될 수 있습니다. "
    "롯데 외 구단의 예매 오픈 시간은 추정값이며, 각 구단 공식 SNS를 반드시 확인하세요."
)
