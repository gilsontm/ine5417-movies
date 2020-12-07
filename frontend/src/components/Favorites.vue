<template>
    <div>
        <menu-header title="Favoritos" :isFavorites="true"></menu-header>
        <b-container v-if="loaded">
            <horizontal-scroll
                class="my-2"
                v-on:clicked="showResult"
                title="Filmes favoritos"
                :results="movies">
            </horizontal-scroll>
            <horizontal-scroll
                class="my-2"
                v-on:clicked="showResult"
                title="Programas de TV favoritos"
                :results="series">
            </horizontal-scroll>
            <horizontal-scroll
                class="my-2"
                v-on:clicked="showResult"
                title="Pessoas favoritas"
                :results="people">
            </horizontal-scroll>
        </b-container>
        <div v-else class="d-flex justify-content-center mt-5">
            <b-spinner></b-spinner>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import menuHeader from './shared/Header.vue'
import horizontalScroll from './shared/HorizontalScroll.vue'

export default {
    name: 'favorites',
    components: {
        menuHeader,
        horizontalScroll,
    },
    data() {
        return {
            movies: [],
            series: [],
            people: [],
            loaded: false,
        }
    },
    mounted() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.loaded = false;
            this.user_id = this.$session.get("user_id");
            axios.get(this.backend + '/favorite', {
                params: {
                    user_id: this.user_id,
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
        }
    }
}
</script>

<style scoped>

</style>