import Vue from 'vue'
import VueSession from 'vue-session';
import App from './App.vue'
import router from './router'
import utils from './utils'
import { BootstrapVue } from 'bootstrap-vue'
import "leaflet/dist/leaflet.css"
import "leaflet.heat/dist/leaflet-heat.js"
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.prototype.$utils = utils;
Vue.use(BootstrapVue);
Vue.use(VueSession, { persist: true });
Vue.config.productionTip = false;

// const backend = process.env.NODE_ENV === 'development' ? 'http://localhost:8888' : '';
const backend = 'http://localhost:8888';

Vue.mixin({
    data() {
        return {
            get backend() { return backend; },
        }
    }
});

new Vue({
    components: { App },
    router,
    render: h => h(App),
}).$mount('#app')

