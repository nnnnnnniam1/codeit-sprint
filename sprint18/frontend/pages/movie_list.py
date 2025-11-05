import streamlit as st
from utils.constants import Menu
from utils.api import create_review, delete_movie, get_movies, get_reviews



def main():
    st.title(Menu.MOVIE_LIST.label)
    
    # ✅ 세션 상태 초기화
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "selected_movie" not in st.session_state:
        st.session_state.selected_movie = None
    if "review_page" not in st.session_state:
            st.session_state.review_page = 1



    # ✅ 백엔드에서 페이지 기반 목록 가져오기
    res = get_movies(page=st.session_state.page)
    movies = res.get("data", [])
    pagination = res.get("pagination", {})

    if not movies:
        st.warning("❌ 영화 데이터가 없습니다.")
        return

    total = pagination.get("total_count", len(movies))
    total_pages = pagination.get("total_pages", 1)
    current_page = pagination.get("page", 1)

    # ✅ 상단 요약
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("🎞 영화 목록")
    with col2:
        st.markdown(f"<p style='text-align:right;color:gray;'>총 {total}개</p>", unsafe_allow_html=True)

    # ✅ CSS Grid Layout
    st.markdown("""
        <style>
        .movie-grid {
            display: grid;grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));gap: 2rem;justify-items: center;}
        .movie-card {
            width: 230px;height: 350px;border-radius: 10px;overflow: hidden;background: #111;display: flex;justify-content: center;align-items: center;cursor: pointer;margin: 10px 5px;
        }
        .movie-card img {
            width: 100%;height: 100%;object-fit: cover;border-radius: 10px;transition: transform 0.3s ease;
        }
        .movie-card:hover img {
            transform: scale(1.05);
        }
        .movie-title {
            font-weight: 600;margin-top: 8px;text-align: center;
        }
        .movie-year {
            color: gray;
            font-size: 14px;
        }
        </style>
        <script>
        function selectMovie(id) {
            window.parent.postMessage({movie_id: id}, "*");
        }
        </script>
    """, unsafe_allow_html=True)

    # ✅ 영화 카드 목록 표시
    cols = st.columns(3)
    for idx, movie in enumerate(movies):
        with cols[idx % 3]:
            year = movie["release_date"].split("-")[0]
            if st.button(f"{movie['title']} ({year})", key=f"movie_btn_{movie['id']}", use_container_width=True):
                st.session_state.selected_movie = movie
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{movie['poster']}" alt="{movie['title']} 포스터">
                </div>
                """,
                unsafe_allow_html=True
            )
    
    
    # clicked_movie_id = st.components.v1.html(html, height=450, scrolling=True)
    # if clicked_movie_id:
    #     st.success(clicked_movie_id)
    #     print(clicked_movie_id)
        

    # ✅ 페이지네이션 버튼
    st.markdown("---")
    col_prev, col_info, col_next = st.columns([1, 3, 1])
    with col_prev:
        if st.button("⬅️ 이전") and current_page > 1:
            st.session_state.page = current_page - 1
            st.session_state.selected_movie = None
            st.rerun()
    with col_next:
        if st.button("다음 ➡️") and current_page < total_pages:
            st.session_state.page = current_page + 1
            st.session_state.selected_movie = None
            st.rerun()
    with col_info:
        st.markdown(
            f"<p style='text-align:center;'>페이지 {current_page} / {total_pages}</p>",
            unsafe_allow_html=True
        )

    # ✅ 영화 상세 보기
    if st.session_state.selected_movie:
        st.divider()
        movie = st.session_state.selected_movie
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"## 🎥 {movie['title']}")
        with col2:
            delete_clicked = st.button("🗑️ 삭제")
        
        if delete_clicked:
            res = delete_movie(movie["id"])
            if res and res.status_code == 200:
                st.success("🎉 영화가 삭제되었습니다!")
                st.session_state.clear()
                st.rerun()
            else:
                st.error(f"❌ 삭제 실패: {res.text}")
                
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(movie["poster"], width=250)
        with col2:
            st.markdown(f"**감독:** {movie['director']}")
            st.markdown(f"**개봉일:** {movie['release_date']}")
            st.markdown(
                f"**장르:** {', '.join([g['genre'] for g in movie.get('genres', [])]) or '정보 없음'}"
            )
            
        st.markdown("### ✏️ 리뷰 작성")
        with st.form(key="review_form", clear_on_submit=True):
            col1, col2 = st.columns([1, 3])
            with col1:
                nickname = st.text_input("닉네임", placeholder="닉네임 입력")
            with col2:
                content = st.text_input("리뷰", placeholder="리뷰를 작성해주세요")

            submitted = st.form_submit_button("등록", use_container_width=True)
        
        if submitted:
            if not nickname.strip() or not content.strip():
                st.warning("⚠️ 닉네임과 리뷰 내용을 모두 입력해주세요.")
            else:
                payload = {
                    "movie_id": movie["id"],
                    "reviewer_name": nickname,
                    "content": content,
                }
                res = create_review(payload)

                if res and res.status_code == 201:
                    st.success("🎉 리뷰가 등록되었습니다!")
                    st.rerun()  # 🔁 새 리뷰 목록 즉시 반영
                else:
                    st.error("❌ 리뷰 등록에 실패했습니다.")
                    
        
        
        REVIEWS_PER_PAGE = 10

        data = get_reviews(movie["id"], page=st.session_state.review_page).json()
        reviews_data = data["data"]
        pagination = data["pagination"]
        
        if not reviews_data:
            st.info("📝 아직 등록된 리뷰가 없습니다.")
        else:
            avg = reviews_data.get("average_score", 0)
            reviews = reviews_data.get("reviews", [])
            
            # 리뷰 데이터 페이지네이션 처리
            start_idx = (st.session_state.review_page - 1) * REVIEWS_PER_PAGE
            end_idx = start_idx + REVIEWS_PER_PAGE
            paged_reviews = reviews[start_idx:end_idx]
            

            if not reviews:
                st.info("📝 아직 등록된 리뷰가 없습니다.")
            else:
                sentiment_colors = {
                    "VERY_NEGATIVE": "#ff4c4c",  # 진한 빨강
                    "NEGATIVE": "#ff7b7b",       # 연한 빨강
                    "NEUTRAL": "#cccccc",        # 회색
                    "POSITIVE": "#7ed957",       # 연두
                    "VERY_POSITIVE": "#4cd964",  # 밝은 초록
                }

                # 🎯 평균 점수 헤더
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### ⭐ 평균 평점: **{avg:.2f}**")
                with col2:
                    total = pagination['total_count']
                    st.markdown(f"<p style='text-align:right;color:gray;'>총 {pagination['total_count']}개</p>", unsafe_allow_html=True)

                for r in reviews:
                    color = sentiment_colors.get(r["sentiment"], "#ccc")  # 기본 회색
                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #444;
                            border-radius: 10px;
                            padding: 12px 16px;
                            margin-bottom: 10px;
                            background-color: #222;
                            color: #f1f1f1;
                            font-family: 'Pretendard', sans-serif;
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="font-weight: 600; font-size: 1rem;">{r['reviewer_name']}</div>
                                <div style="font-size: 0.9rem; color: #aaa;">{r['created_at'][:10]}</div>
                            </div>
                            <p style="margin-top: 6px; font-size: 0.95rem; color: #eee;">{r['content']}</p>
                            <div style="font-size: 0.9rem; color: #ddd;">
                                감정:
                                <span style="color:{color}; font-weight:600;">
                                    {r['sentiment_label']}
                                </span>
                                · 평점:
                                <b style="color:#faca2f;">{r['score']:.2f}</b>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                total_pages = pagination['total_pages']
                st.markdown("---")
                col_prev, col_info, col_next = st.columns([1, 3, 1])

                with col_prev:
                    if st.button("⬅️ 이전", key="review_prev") and st.session_state.review_page > 1:
                        st.session_state.review_page -= 1
                        st.rerun()

                with col_next:
                    if st.button("다음 ➡️", key="review_next") and st.session_state.review_page < total_pages:
                        st.session_state.review_page += 1
                        st.rerun()

                with col_info:
                    st.markdown(
                        f"<p style='text-align:center;'>페이지 {st.session_state.review_page} / {total_pages}</p>",
                        unsafe_allow_html=True,
                    )
            