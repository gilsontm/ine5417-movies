<template>
    <div>
        <menuHeader :isHome="true"> </menuHeader>
        <b-row class="center mt-2 mx-0">
            <b-col cols="6" offset="2" class="px-1">
                <b-form-input type="text" v-model="query"> </b-form-input>
            </b-col>
            <b-col cols="2" class="px-1">
                <b-button variant="success" class="btn btn-block" @click="search"> Pesquisar </b-button>
            </b-col>
        </b-row>
        <b-container v-if="searched">
            <div class="my-2 horizontal-scroll">
                <h4> Filmes </h4>
                <hr/>
                <template v-for="result in movies">
                    <b-link
                        :key="result.id"
                        @click="showResult(result)"
                        class="d-inline-block bg-light px-3 pt-3 mx-1 text-center">
                        <img class="poster" :src="result.poster_path ? (url + result.poster_path) : unavailable">
                        <p class="text-truncate" style="max-width: 185px;"> {{ result.title }} </p>
                    </b-link>
                </template>
                <p v-if="movies.length === 0"> Nenhum resultado encontrado. </p>
            </div>
            <div class="my-2 horizontal-scroll">
                <h4> TV </h4>
                <hr/>
                <template v-for="result in series">
                    <b-link
                        :key="result.id"
                        @click="showResult(result)"
                        class="d-inline-block bg-light px-3 pt-3 mx-1 text-center">
                        <img class="poster" :src="result.poster_path ? (url + result.poster_path) : unavailable">
                        <p class="text-truncate" style="max-width: 185px;"> {{ result.name }} </p>
                    </b-link>
                </template>
                <p v-if="series.length === 0"> Nenhum resultado encontrado. </p>
            </div>
            <div class="my-2 horizontal-scroll">
                <h4> Pessoas </h4>
                <hr/>
                <template v-for="result in people">
                    <b-link
                        :key="result.id"
                        @click="showResult(result)"
                        class="d-inline-block bg-light px-3 pt-3 mx-1 text-center">
                        <img class="poster" :src="result.profile_path ? (url + result.profile_path) : unavailable">
                        <p class="text-truncate" style="max-width: 185px;"> {{ result.name }} </p>
                    </b-link>
                </template>
                <p v-if="people.length === 0"> Nenhum resultado encontrado. </p>
            </div>
        </b-container>
    </div>
</template>

<script>
import axios from 'axios'
import menuHeader from './Header.vue'

export default {
    name: 'home',
    components: {
        menuHeader,
    },
    data() {
        return {
            url: 'https://image.tmdb.org/t/p/w185',
            unavailable: require('../assets/default_w185.jpg'),
            query: '',
            movies: [],
            series: [],
            people: [],
            searched: false,
        }
    },
    methods: {
        search() {
            this.searched = true;
            if (!this.query) {
                this.clear();
                return;
            }
            axios.get(this.backend + '/search', {
                params: {
                    query: this.query,
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
            }).catch(err => {
                console.log(err);
            })
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
                    'model': result,
                }
            });
        }
    }
}
</script>

<style scoped>

.horizontal-scroll {
    overflow-x: auto;
    white-space: nowrap;
}
.horizontal-scroll > .d-inline-block {
    float: none;
}

.poster {
    width: 185px;
    max-height: 278px;
    object-fit: none;
    object-position: center;
}

</style>