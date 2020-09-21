import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/login',
            name: 'login',
            component: require('@/components/Login').default,
        },
        {
            path: '/home',
            name: 'home',
            component: require('@/components/Home').default,
        },
        {
            path: '*',
            redirect: '/login',
        },
        {
            path: '/movie/:id',
            name: 'movie',
            component: require('@/components/Movie').default,
        },
        {
            path: '/tv/:id',
            name: 'tv',
            component: require('@/components/Tv').default,
        },
        {
            path: '/person/:id',
            name: 'person',
            component: require('@/components/Person').default,
        },
    ],
});
