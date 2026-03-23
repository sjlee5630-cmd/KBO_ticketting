import streamlit as st
import calendar
from datetime import date, timedelta

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="SSG 랜더스 2026 일정",
    page_icon="⚾",
    layout="wide",
)

# ── CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* 달력 전체 컨테이너 */
.cal-wrap { border-radius: 12px; overflow: hidden; border: 1px solid #e0e0e0; }

/* 요일 헤더 */
.cal-header {
    display: grid; grid-template-columns: repeat(7, 1fr);
    background: #CC0000; color: white; text-align: center;
    font-size: 13px; font-weight: 500;
}
.cal-header div { padding: 8px 4px; }

/* 날짜 그리드 */
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); background: #f5f5f5; gap: 1px; }

/* 개별 날짜 셀 */
.cal-cell {
    background: white; min-height: 80px; padding: 6px;
    font-size: 12px; position: relative; vertical-align: top;
}
.cal-cell.empty { background: #fafafa; }
.cal-cell.today { background: #fff8f0; }

/* 날짜 숫자 */
.day-num { font-size: 13px; font-weight: 500; color: #333; margin-bottom: 3px; }
.day-num.sun { color: #cc0000; }
.day-num.sat { color: #1a56db; }

/* 경기 뱃지 */
.game-badge {
    display: block; border-radius: 6px; padding: 3px 5px;
    font-size: 11px; line-height: 1.3; margin-bottom: 2px;
    text-decoration: none; color: inherit;
}
.badge-home {
    background: #fff0ee; border-left: 3px solid #CC0000; color: #7a0000;
}
.badge-away {
    background: #eef3ff; border-left: 3px solid #1a56db; color: #1a3a7a;
}
.badge-hot::after { content: " 🔥"; }
.badge-special {
    background: #f0f0f0; color: #555; font-style: italic;
    border-left: 3px solid #aaa;
}

/* 범례 */
.legend-wrap { display: flex; gap: 16px; align-items: center; font-size: 13px; }
.legend-dot { width: 14px; height: 14px; border-radius: 3px; display: inline-block; margin-right: 4px; vertical-align: middle; }

/* 팝업 정보 카드 */
.info-card {
    background: white; border-radius: 10px; padding: 16px;
    border: 1px solid #ddd; margin-top: 8px;
}
.info-title { font-size: 15px; font-weight: 700; color: #CC0000; margin-bottom: 6px; }
.info-row { font-size: 13px; margin-bottom: 4px; color: #333; }
.info-row b { color: #111; }

/* 사이드바 */
[data-testid="stSidebar"] { background: #1a1a2e; }
[data-testid="stSidebar"] * { color: white !important; }

/* 월 네비게이션 버튼 */
div[data-testid="column"] button {
    border-radius: 8px; font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ── 데이터 ───────────────────────────────────────────────────

TICKET_INFO = {
    "홈": {
        "venue": "인천 SSG 랜더스필드 (문학)",
        "선예매": "경기 7일 전 오전 10:00 (배티 회원)",
        "일반예매": "경기 5일 전 오전 10:00",
        "url": "https://ticket.ssg.com",
        "url_label": "SSG 공식 티켓",
    },
    "롯데": {
        "venue": "사직야구장 (부산)",
        "선예매": "경기 14일 전 오전 10:00 (클럽 회원)",
        "일반예매": "경기 14일 전 오후 14:00",
        "url": "https://www.giantsclub.com",
        "url_label": "롯데 자이언츠 공식",
    },
    "LG": {
        "venue": "잠실야구장 (서울)",
        "선예매": "경기 7~10일 전 오전 10:00 추정",
        "일반예매": "경기 7일 전 오전 10:00 추정",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "두산": {
        "venue": "잠실야구장 (서울)",
        "선예매": "경기 7~10일 전 오전 11:00 추정",
        "일반예매": "경기 7일 전 오전 11:00 추정",
        "url": "https://ticket.interpark.com",
        "url_label": "인터파크 티켓",
    },
    "키움": {
        "venue": "고척스카이돔 (서울)",
        "선예매": "경기 7~10일 전 오전 11:00 추정",
        "일반예매": "경기 7일 전 오전 11:00 추정",
        "url": "https://ticket.interpark.com",
        "url_label": "인터파크 티켓",
    },
    "kt": {
        "venue": "수원 KT위즈파크",
        "선예매": "경기 7~10일 전 오전 10:00 추정",
        "일반예매": "경기 7일 전 오전 10:00 추정",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "한화": {
        "venue": "한화생명이글스파크 (대전)",
        "선예매": "경기 7~10일 전 오전 10:00 추정",
        "일반예매": "경기 7일 전 오전 10:00 추정",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "삼성": {
        "venue": "라이온즈파크 (대구)",
        "선예매": "경기 7~10일 전 오전 10:00 추정",
        "일반예매": "경기 7일 전 오전 10:00 추정",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "KIA": {
        "venue": "기아 챔피언스 필드 (광주)",
        "선예매": "경기 7~10일 전 오전 10:00 추정",
        "일반예매": "경기 7일 전 오전 10:00 추정",
        "url": "https://www.ticketlink.co.kr",
        "url_label": "티켓링크",
    },
    "NC": {
        "venue": "창원 NC파크",
        "선예매": "경기 7~10일 전 오전 11:00 추정",
        "일반예매": "경기 7일 전 오전 11:00 추정",
        "url": "https://ticket.ncdinos.com",
        "url_label": "NC 다이노스 공식",
    },
}

# 경기 일정: (월, 일, 상대, 홈/원정, 빅매치여부)
SCHEDULE_RAW = [
    # 3월
    (3, 28, "KIA",  "홈",   True),
    (3, 29, "KIA",  "홈",   True),
    (3, 31, "키움", "홈",   False),
    # 4월
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
    # 5월
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
    # 6월
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
    # 7월
    (7,  1, "KIA",  "원정", False),
    (7,  2, "KIA",  "원정", False),
    (7,  3, "삼성", "홈",   False),
    (7,  4, "삼성", "홈",   True),
    (7,  5, "삼성", "홈",   True),
    (7,  7, "두산", "원정", False),
    (7,  8, "두산", "원정", False),
    (7,  9, "두산", "원정", False),
    # 올스타 휴식기 7/10~15 → special 처리
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
    # 8월
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
    # 9월
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
]

SPECIAL_DAYS = {
    (7, 10): "올스타 휴식기",
    (7, 11): "올스타 휴식기",
    (7, 12): "올스타 휴식기",
    (7, 13): "올스타 휴식기",
}

# 날짜 → 경기 목록 딕셔너리
def build_schedule_dict():
    d = {}
    for m, day, opp, loc, hot in SCHEDULE_RAW:
        key = (m, day)
        if key not in d:
            d[key] = []
        d[key].append({"opp": opp, "loc": loc, "hot": hot})
    return d

SCHEDULE = build_schedule_dict()

def get_ticket_info(game):
    """경기 딕셔너리에서 티켓팅 정보 반환"""
    if game["loc"] == "홈":
        return TICKET_INFO["홈"]
    else:
        return TICKET_INFO.get(game["opp"], None)

def calc_presale_date(m, d):
    """배티 선예매: 7일 전"""
    dt = date(2026, m, d) - timedelta(days=7)
    return dt.strftime("%-m월 %-d일")

def calc_away_presale_date(m, d, opp):
    """원정 선예매 날짜"""
    days = 14 if opp == "롯데" else 7
    dt = date(2026, m, d) - timedelta(days=days)
    return dt.strftime("%-m월 %-d일")


# ── 사이드바 ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚾ SSG 랜더스 2026")
    st.markdown("---")

    st.markdown("### 월 선택")
    month_names = ["3월", "4월", "5월", "6월", "7월", "8월", "9월"]
    month_map = {n: i + 3 for i, n in enumerate(month_names)}

    if "selected_month" not in st.session_state:
        st.session_state.selected_month = 3

    for name in month_names:
        active = st.session_state.selected_month == month_map[name]
        if st.button(name, key=f"btn_{name}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.selected_month = month_map[name]
            st.session_state.selected_game = None

    st.markdown("---")
    st.markdown("### 범례")
    st.markdown("""
<div style='font-size:13px;line-height:2'>
🔴 <b>홈경기</b> (인천 문학)<br>
🔵 <b>원정경기</b><br>
🔥 <b>주말 / 빅매치</b>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 배티 선예매 안내")
    st.info("경기 **7일 전** 오전 10:00\n\nSSG 공식 앱 / ticket.ssg.com")


# ── 메인 ────────────────────────────────────────────────────
sel_month = st.session_state.selected_month
month_label = {3:"3월",4:"4월",5:"5월",6:"6월",7:"7월",8:"8월",9:"9월"}

st.markdown(f"## ⚾ SSG 랜더스 2026 — {month_label[sel_month]} 경기 일정")

# 선택된 경기 초기화
if "selected_game" not in st.session_state:
    st.session_state.selected_game = None

# ── 달력 렌더링 ───────────────────────────────────────────
cal = calendar.monthcalendar(2026, sel_month)
weekdays = ["월", "화", "수", "목", "금", "토", "일"]

# 헤더
header_html = '<div class="cal-wrap"><div class="cal-header">'
for i, w in enumerate(weekdays):
    color = "#ffcccc" if i == 6 else ("#ccd9ff" if i == 5 else "white")
    header_html += f'<div style="color:{color}">{w}</div>'
header_html += '</div><div class="cal-grid">'

# 셀 생성
today = date.today()
cells_html = ""
game_buttons = []  # (cell_key, game_info) 저장

for week in cal:
    for wi, day in enumerate(week):
        if day == 0:
            cells_html += '<div class="cal-cell empty"></div>'
            continue

        is_today = (date(2026, sel_month, day) == today)
        is_sun = (wi == 6)
        is_sat = (wi == 5)
        cell_class = "cal-cell" + (" today" if is_today else "")

        # 날짜 숫자 색
        num_class = "day-num" + (" sun" if is_sun else (" sat" if is_sat else ""))
        cell_inner = f'<div class="{num_class}">{day}</div>'

        # 특별일정 (올스타 등)
        special = SPECIAL_DAYS.get((sel_month, day))
        if special:
            cell_inner += f'<span class="game-badge badge-special">{special}</span>'

        # 경기 뱃지
        games_today = SCHEDULE.get((sel_month, day), [])
        for g in games_today:
            hot_cls = " badge-hot" if g["hot"] else ""
            loc = g["loc"]
            opp = g["opp"]
            ti = get_ticket_info(g)
            url = ti["url"] if ti else "#"
            if loc == "홈":
                badge_cls = f"game-badge badge-home{hot_cls}"
                label = f"홈 vs {opp}"
            else:
                badge_cls = f"game-badge badge-away{hot_cls}"
                label = f"원정 @{opp}"
            cell_inner += (
                f'<a href="{url}" target="_blank" class="{badge_cls}" '
                f'title="{label} 티켓팅 →">{label}</a>'
            )

        cells_html += f'<div class="{cell_class}">{cell_inner}</div>'

full_html = header_html + cells_html + "</div></div>"
st.markdown(full_html, unsafe_allow_html=True)

# ── 이번 달 경기 요약 테이블 ────────────────────────────────
st.markdown("---")
st.markdown("### 📋 이번 달 경기 티켓팅 상세")

month_games = [
    (m, d, g)
    for (m, d), games in SCHEDULE.items()
    for g in games
    if m == sel_month
]
month_games.sort(key=lambda x: x[1])

if not month_games:
    st.info("이번 달 경기가 없습니다.")
else:
    col_headers = ["날짜", "홈/원정", "상대팀", "구장", "선예매 오픈", "예매 시간", "예매 링크"]
    rows = []
    for m, d, g in month_games:
        opp = g["opp"]
        loc = g["loc"]
        hot_mark = " 🔥" if g["hot"] else ""
        ti = get_ticket_info(g)
        dow = ["월","화","수","목","금","토","일"][date(2026, m, d).weekday()]
        date_str = f"{m}/{d}({dow}){hot_mark}"
        venue = ti["venue"] if ti else "-"
        url = ti["url"] if ti else "#"
        url_label = ti["url_label"] if ti else "-"

        if loc == "홈":
            presale = calc_presale_date(m, d) + " 오전 10:00"
            open_time = "오전 10:00"
        else:
            presale = calc_away_presale_date(m, d, opp)
            if opp == "롯데":
                presale += " 오전 10:00 (선예매)\n" + calc_away_presale_date(m, d, opp).replace("오전", "") + " 오후 14:00 (일반)"
                open_time = "선 10:00 / 일반 14:00"
                presale = calc_away_presale_date(m, d, opp) + " (오전 10:00)"
            else:
                presale += " (오전 10:00 추정)"
                open_time = "오전 10:00 추정"

        rows.append({
            "날짜": date_str,
            "홈/원정": loc,
            "상대팀": opp,
            "구장": venue,
            "선예매 오픈": presale,
            "예매 시간": open_time,
            "예매처": f"[{url_label}]({url})",
        })

    # 홈/원정 필터
    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 4])
    with filter_col1:
        show_home = st.checkbox("홈 경기", value=True)
    with filter_col2:
        show_away = st.checkbox("원정 경기", value=True)

    filtered = [r for r in rows if
                (r["홈/원정"] == "홈" and show_home) or
                (r["홈/원정"] == "원정" and show_away)]

    if filtered:
        import pandas as pd
        df = pd.DataFrame(filtered)
        # 홈/원정 열 스타일링
        def style_row(row):
            if row["홈/원정"] == "홈":
                return ["background-color: #fff0ee"] * len(row)
            else:
                return ["background-color: #eef3ff"] * len(row)

        st.dataframe(
            df.drop(columns=["홈/원정"]),
            use_container_width=True,
            hide_index=True,
            column_config={
                "예매처": st.column_config.LinkColumn("예매처", display_text="→ 예매하기"),
            }
        )
    else:
        st.info("선택한 필터에 해당하는 경기가 없습니다.")

# ── 구단별 예매처 안내 ────────────────────────────────────
with st.expander("🏟️ 구단별 원정 예매처 전체 안내"):
    cols = st.columns(3)
    teams_list = [t for t in TICKET_INFO.keys() if t != "홈"]
    for i, team in enumerate(teams_list):
        info = TICKET_INFO[team]
        with cols[i % 3]:
            st.markdown(f"""
**{team}** — {info['venue']}

- 선예매: {info['선예매']}
- 일반예매: {info['일반예매']}
- 예매: [{info['url_label']}]({info['url']})
""")

st.markdown("---")
st.caption("⚠️ 경기 일정은 우천 취소 등으로 변경될 수 있습니다. 티켓팅 오픈 시간은 롯데 외 구단의 경우 공식 공지 기준으로 변동될 수 있으니 각 구단 SNS를 확인하세요.")
