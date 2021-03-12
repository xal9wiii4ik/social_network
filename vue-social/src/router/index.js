import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
    {
        path: '/posts',
        name: 'posts',
        component: () => import('@/views/posts'),
    },
    {
        path: '/create_post',
        name: 'create_post',
        component: () => import('@/views/create_post')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/login')
    },
    {
        path: '/registration',
        name: 'registration',
        component: () => import('@/views/registration')
    },
    {
        path: '/my_posts',
        name: 'my_posts',
        component: () => import('@/views/my_posts')
    },
    {
        path: '/posts/:id',
        name: 'posts_id',
        component: () => import('@/views/post_detail')
    },
    {
        path: '/my_profile/:id',
        name: 'my_profile',
        component: () => import('@/views/my_profile')
    },
    {
        path: '/guest_profile/:id',
        name: 'guest_profile',
        component: () => import('@/views/guest_profile')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
