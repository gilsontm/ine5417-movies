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
            path: '/information',
            name: 'information',
            component: require('@/components/Information').default,
            props: true,
        },
        {
            path: '*',
            redirect: '/login',
        },
    ],
});
