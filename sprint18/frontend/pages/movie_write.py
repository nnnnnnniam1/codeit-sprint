import datetime
import streamlit as st
from utils.api import get_genres, create_movie
from utils.constants import Menu


@st.cache_data(ttl=30)
def fetch_genres():
    return get_genres()

def main():
    st.title(Menu.MOVIE_WRITE.label)
    st.markdown("### 🎬 새 영화 추가")

    # --- 장르 데이터 로드 ---
    genres_data = get_genres()
    options = [(g["genre"], g["id"]) for g in genres_data] if genres_data else []

    # --- 세션 상태 초기화 ---
    if "new_genres" not in st.session_state:
        st.session_state.new_genres = []
    if "new_genre_input" not in st.session_state:
        st.session_state.new_genre_input = ""

    # --- 엔터로 장르 추가하는 함수 ---
    def add_new_genre():
        new_g = st.session_state.new_genre_input.strip()
        if new_g and new_g not in st.session_state.new_genres:
            st.session_state.new_genres.append(new_g)
        st.session_state.new_genre_input = ""  # 입력칸 비우기

    # --- 입력 필드 ---
    title = st.text_input("🎞 영화제목", placeholder="영화 제목을 입력하세요.", key="movie_title")
    director = st.text_input("🎬 감독", placeholder="감독 이름을 입력하세요.", key="movie_director")
    release_date = st.date_input("📅 개봉일", format="YYYY-MM-DD", min_value=datetime.date(1900, 1, 1), key="movie_release")
    poster = st.text_input("🖼 포스터 URL", placeholder="포스터 URL을 입력하세요.", key="movie_poster")

    st.markdown("### 🎭 장르 선택")
    if st.button("🔄 최신 장르 불러오기"):
        fetch_genres.clear()  # 캐시 초기화

    genres_data = fetch_genres()
    options = [(g["genre"], g["id"]) for g in genres_data] if genres_data else []

    selected_ids = st.multiselect(
        "기존 장르 선택",
        options=options,
        format_func=lambda opt: opt[0],
        key="selected_genres"
)

    # --- 새 장르 입력 ---
    st.text_input(
        "새 장르 입력 (엔터)",
        key="new_genre_input",
        placeholder="예: 스릴러",
        on_change=add_new_genre,  # ✅ 엔터 누르면 자동 추가
    )

    # --- 추가된 장르 표시 및 삭제 ---
    if st.session_state.new_genres:
        st.markdown("### 🆕 추가된 장르:")
        for g in st.session_state.new_genres:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(
                    f"<span style='background:#4a4a4a;color:white;padding:6px 10px;border-radius:10px;margin:2px;display:inline-block'>{g}</span>",
                    unsafe_allow_html=True
                )
            with col2:
                if st.button(f"❌", key=f"remove_{g}"):
                    st.session_state.new_genres.remove(g)
                    st.rerun()

    # --- 등록 버튼 ---
    if st.button("✅ 영화 등록"):
        existing_genre_names = [g[0] for g in selected_ids]  # ex: ['액션', '드라마']
        new_genres = st.session_state.new_genres

        duplicates = [g for g in new_genres if g in existing_genre_names]
        if duplicates:
            st.warning(f"⚠️ 중복된 장르가 있습니다: {', '.join(duplicates)}")
            st.stop() 
            
        genre_payload = [{"id": g[1]} for g in selected_ids]
        genre_payload += [{"genre": g} for g in st.session_state.new_genres]

        payload = {
            "title": title,
            "director": director,
            "release_date": str(release_date),
            "poster": poster,
            "genres": genre_payload,
        }


        res = create_movie(payload)
        if res and res.status_code == 201:
            st.success("🎉 영화가 성공적으로 등록되었습니다!")
            st.session_state.clear()

            st.rerun()
        else:
            st.error(f"❌ 등록 실패: {res.text}")
