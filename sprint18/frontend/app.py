import select
import streamlit as st
import os
from utils.constants import Menu
from utils.api import get_movies

from dotenv import load_dotenv
import importlib

load_dotenv()


st.set_page_config(
    page_title="🎬 영화 관리 시스템",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS로 자동 페이지 메뉴 숨기기 ---
st.markdown("""
    <style>
    /* 기본적으로 pages 메뉴 숨기기 */
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# --- 메뉴 (key: 내부명 / value: 표시 이름) ---
menu_lists = {
    "movie_list": "🎞 영화 목록",
    "movie_write": "➕ 영화 추가",
    "review_list": "🗒 리뷰 전체 보기",
    "review_write": "✍ 리뷰 작성",
}

# --- 세션 상태 (기본 페이지: 영화 목록) ---
if "menu" not in st.session_state:
    st.session_state.menu = "movie_list"

# --- 사이드바 표시 ---
st.sidebar.title("🎬 영화 관리 시스템")

# value 기준으로 라디오 표시하되, 선택 시 key로 역변환
menu_key = st.sidebar.radio(
    "메뉴 선택",
    options=Menu.keys(),                            # ["movie_list", "movie_write", ...]
    format_func=lambda key: Menu.label_from_key(key),  # 한글 이름으로 표시
    index=Menu.keys().index(st.session_state.menu),
    label_visibility="collapsed",
)

if menu_key != st.session_state.menu:
    st.session_state.menu = menu_key
    st.rerun()

# --- 선택된 페이지 import ---
module = importlib.import_module(f"pages.{menu_key}")


if hasattr(module, "main"):  # pages.movie_list.main() 실행
    module.main()
else:
    st.error(f"❌ {menu_key} 페이지에 main() 함수가 없습니다.")
