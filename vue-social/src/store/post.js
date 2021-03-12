import router from '../router'

export default {
    actions: {
        async fetchPosts({commit, dispatch, state}) {
            try {
                const response = await fetch('http://localhost:8000/posts/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${localStorage.getItem('access_token')}`
                    }
                });
                if (response.status === 200) {
                    const posts = await response.json();
                    commit('updatePosts', posts);
                }
                if (response.status === 401) {
                    await router.push('/login')
                }
            } catch (e) {
                console.log(e);
            }
        },
        async fetchMyPosts({commit, dispatch, state}) {
            try {
                const response = await fetch('http://localhost:8000/posts/my_posts/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${localStorage.getItem('access_token')}`
                    }
                });
                if (response.status === 200) {
                    const posts = await response.json();
                    commit('updatePosts', posts);
                }
                if (response.status === 401) {
                    await router.push('/login')
                }
            } catch (e) {
                console.log(e);
            }
        },
        async fetchToken({commit, state}, data) {
            const loginData = {
                username: data?.username,
                password: data?.password,
            }
            try {
                const response = await fetch(`http://localhost:8000/auth/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(loginData)
                })
                const token = await response.json();
                if (Object.keys(token).length > 1) {
                    localStorage.setItem('access_token', token.access)
                    localStorage.setItem('refresh_token', token.refresh)
                    localStorage.setItem('username', loginData.username)
                    localStorage.setItem('user_id', token.user_id)
                    return true
                } else {
                    return false
                }
            } catch (e) {
                console.log(e);
            }
        }
    },
    mutations: {
        // во время выполнения функции деламе изменения
        updatePosts(state, posts) {
            state.posts = posts;
        }
    },
    getters: {
        // отправляем то что после мутации (данные store)
        getPosts(state) {
            return state.posts;
        }
    },
    state: {
        // изначально
        posts: []
    },
}