<template>
    <div>
        <menu-header title="" :isHome="true"> </menu-header>
        <b-row class="center mt-2 mx-0">
            <b-col cols="4" offset="3" class="px-1">
                <b-form-input list="history" type="text" v-model="query" autocomplete="off"> </b-form-input>
                <datalist id="history">
                    <option v-for="recent of history" :key="recent.id">{{ recent }}</option>
                </datalist>
            </b-col>
            <b-col cols="2" class="px-1">
                <b-button variant="dark" class="w-75" block @click="search"> Pesquisar </b-button>
            </b-col>
        </b-row>
        <template v-if="searched">
            <b-container v-if="loaded">
                <horizontal-scroll
                    class="my-2"
                    v-on:clicked="showResult"
                    title="Filmes"
                    :results="movies">
                </horizontal-scroll>
                <horizontal-scroll
                    class="my-2"
                    v-on:clicked="showResult"
                    title="Programas de TV"
                    :results="series">
                </horizontal-scroll>
                <horizontal-scroll
                    class="my-2"
                    v-on:clicked="showResult"
                    title="Pessoas"
                    :results="people">
                </horizontal-scroll>
            </b-container>
            <div v-else class="d-flex justify-content-center mt-5">
                <b-spinner></b-spinner>
            </div>
        </template>
    </div>
</template>

<script>
import axios from 'axios'
import menuHeader from './shared/Header.vue'
import horizontalScroll from './shared/HorizontalScroll.vue'

export default {
    name: 'home',
    components: {
        menuHeader,
        horizontalScroll,
    },
    data() {
        return {
            query: '',
            movies: [],
            series: [],
            people: [],
            searched: false,
            loaded: false,
            history: [],
        }
    },
    mounted() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.user_id = this.$session.get("user_id");
            this.loadHistory();
        },
        search() {
            this.searched = true;
            this.loaded = false;
            if (!this.query) {
                this.clear();
                this.loaded = true;
                return;
            }
            this.user_id = this.$session.get("user_id");
            axios.get(this.backend + '/search', {
                params: {
                    query: this.query,
                    user_id: this.user_id
                },
            }).then(res => {
                this.clear();
                res.data.results.forEach(result => {
                    if (result.media_type === 'movie')
                        this.movies.push(result);
                    else if (result.media_type === 'tv')
                        this.series.push(result);
                    else
                        this.people.push(result);
                });
                this.refresh();
                this.loaded = true;
            }).catch(err => console.log(err));
        },
        clear() {
            this.movies = [];
            this.series = [];
            this.people = [];
        },
        showResult(result) {
            this.$router.push({
                name: 'information',
                params: {
                    'model_prop': result,
                }
            });
        },
        loadHistory() {
            axios.get(this.backend + '/history', {
                params: {
                    user_id: this.user_id,
                },
            }).then(res => {
                if (res.data)
                    this.history = res.data.results;
            }).catch(err => console.log(err));
        }
    }
}
</script>

<style scoped>

</style>