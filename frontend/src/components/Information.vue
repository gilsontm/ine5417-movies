<template>
    <div>
        <menuHeader :title="'Informação'" :isHome="false"> </menuHeader>

        <!-- MOVIE -->
        <template v-if="model.media_type === 'movie'">
            <b-row>
                <b-col>
                    <img class="poster" :src="model.poster_path ? (url + model.poster_path) : unavailable">
                </b-col>
                <b-col cols="10">
                    <h1 style="max-width: 500px">{{model.title}}</h1>
                    <hr>
                    <p>Resumo: {{model.overview}}</p>
                    <p>Título original: {{model.original_title}}</p>
                    <p>Lingua original: {{model.original_language}}</p>
                    <p>Popularidade: {{model.popularity}}</p>
                    <!-- <p>Tempo de duração: {{model.runtime}}</p> -->
                    <!-- <p>: {{model.spoken_languages.names}}</p> -->
                    <p>Data de lançamento: {{model.release_date}}</p>
                    <!-- <p>Status: {{model.status}}</p> -->
                    <!-- <p>: {{model.production_companies}}</p> -->
                    <!-- <p>: {{model.production_countries}}</p> -->
                    <!-- <p>: {{model.revenue}}</p> -->
                    <!-- <p>: {{model.runtime}}</p> -->
                    <!-- <p>Tagline: {{model.tagline}}</p> -->
                    <p>Média de votos: {{model.vote_average}}</p>
                    <p>Quantidade de votos: {{model.vote_count}}</p>
                    <!-- <p>Generos: {{model.genres}}</p> -->
                </b-col>
            </b-row>
        </template>

        <!-- TV -->
        <template v-else-if="model.media_type === 'tv'">
            <b-row>
                <b-col>
                    <img class="poster" :src="model.poster_path ? (url + model.poster_path) : unavailable">
                </b-col>
                <b-col cols="10">
                <h1 style="max-width: 500px">{{model.name}}</h1>
                <hr>
                <p>Resumo: {{model.overview}}</p>
                <!-- <p>Criada por: {{model.created_by}}</p> -->
                <!-- <p>: {{model.credit_id}}</p> -->
                <!-- <p>Tempo de duração de um episodio: {{model.episode_run_time}}</p> -->
                <p>Estreou em: {{model.first_air_date}}</p>
                <!-- <p>Generos: {{model.genres}}</p> -->
                <!-- <p>Em produção: {{model.in_production}}</p>
                <p>Linguas: {{model.languages}}</p> -->
                <!-- <p>Lançado por último em: {{model.last_air_date}}</p> -->
                <!-- <p>: {{model.networks}}</p> -->
                <p>Número de episodios: {{model.number_of_episodes}}</p>
                <p>Número de temporadas: {{model.number_of_seasons}}</p>
                <p>País de origem: {{model.origin_country}}</p>
                <p>Popularidade: {{model.popularity}}</p>
                <!-- <p>produção: {{model.production_companies}}</p> -->
                <!-- <p>: {{model.seasons}}</p> -->
                <!-- <p>: {{model.status}}</p> -->
                <p>Média de votos: {{model.vote_average}}</p>
                <p>Quantidade de votos: {{model.vote_count}}</p>
                </b-col>
            </b-row>
        </template>

        <!-- PERSON -->
        <template v-else-if="model.media_type === 'person'">
            <b-row>
                <b-col>
                    <img class="poster" :src="model.profile_path ? (url + model.profile_path) : unavailable">
                </b-col>
                <b-col cols="10">
                <h1 style="max-width: 500px">{{model.name}}</h1>
                <hr>
                <p>Data de nascimento: {{model.birthday}}</p>
                <p>Conhecido(a) por: {{model.known_for_department}}</p>
                <p>Dia de falecimento: {{model.deathday}}</p>
                <p>Também conhecido(a) como: {{model.also_known_as}}</p>
                <p>Biografia: {{model.biography}}</p>
                <p>Lugar de nascimento: {{model.place_of_birth}}</p>
                </b-col>
            </b-row>
        </template>
    </div>
</template>

<script>
import menuHeader from './Header.vue'

export default {
    props: ['model'],
    components: {
        menuHeader,
    },
    data() {
        return {
            test: null,
            url: 'https://image.tmdb.org/t/p/w185',
            unavailable: require('../assets/default_w185.jpg'),
        }
    },
    mounted() {
        if (!this.model) this.$router.push('/home');
    },
    methods: {

    },
}
</script>

<style scoped>
.poster {
    /* width: 185px;
    max-height: 278px; */
    width: 266px;
    max-height: 400px;
    object-fit: none;
    object-position: center;
}
</style>