<template>
    <div>
        <menu-header :title="$utils.title(model)" :isHome="false" :isUser="false"> </menu-header>
        <template v-if="loaded">
            <div :class="backdrop ? 'backdrop' : ''" :style="backdrop">
                <b-container class="bg-light pt-4">
                    <b-row class="no-gutters">
                        <b-col cols="2" class="text-center">
                            <img :src="$utils.poster(model)" class="w-100">
                            <b-button class="mt-3" block variant="dark" @click="setFavorite"> {{ is_favorite ? "Desfavoritar" : "Favoritar" }} </b-button>
                            <b-button class="mt-3" block variant="dark" @click="generateAnalysis"> Gerar análise </b-button>
                        </b-col>
                        <b-col cols="10" class="text-justify px-5">
                            <h4><b>{{$utils.title(model)}}</b></h4>
                            <hr>
                            <template v-if="model.media_type === 'movie'">
                                <p><b>Título original:</b> {{info.original_title || 'indisponível'}}</p>
                                <p><b>Resumo:</b> {{info.overview || 'indisponível'}}</p>
                                <p><b>Duração:</b> {{info.runtime || 'indisponível'}}</p>
                                <p><b>Gêneros:</b> {{info.genres.map(e => e.name).join(', ') || 'indisponível'}}</p>
                                <p><b>Idiomas:</b> {{info.spoken_languages.map(e => ISO6391.getNativeName(e.iso_639_1)).join(', ') || 'indisponível'}}</p>
                                <p><b>Idioma original:</b> {{ISO6391.getNativeName(info.original_language) || 'indisponível'}}</p>
                                <p><b>Data de estreia:</b> {{info.release_date || 'indisponível'}}</p>
                                <p><b>Popularidade:</b> {{info.popularity || 'indisponível'}}</p>
                                <p><b>Orçamento:</b> {{info.budget || 'indisponível'}}</p>
                                <p><b>Bilheteria:</b> {{info.revenue || 'indisponível'}}</p>
                                <p><b>Status:</b> {{info.status || 'indisponível'}}</p>
                                <p><b>Tagline:</b> {{info.tagline || 'indisponível'}}</p>
                                <p><b>Média de votos:</b> {{info.vote_average || 'indisponível'}}</p>
                                <p><b>Número de votos:</b> {{info.vote_count || 'indisponível'}}</p>
                            </template>

                            <!-- TV -->
                            <template v-else-if="model.media_type === 'tv'">
                                <p><b>Nome original:</b> {{info.original_name || 'indisponível'}}</p>
                                <p><b>Resumo:</b> {{info.overview || 'indisponível'}}</p>
                                <p><b>Criado por:</b> {{info.created_by.map(e => e.name).join(', ') || 'indisponível'}}</p>
                                <p><b>Duração dos episódios:</b> {{info.episode_run_time[0] || 'indisponível'}}</p>
                                <p><b>Gêneros:</b> {{info.genres.map(e => e.name).join(', ') || 'indisponível'}}</p>
                                <p><b>Idiomas:</b> {{info.languages.map(e => ISO6391.getNativeName(e)).join(', ') || 'indisponível'}}</p>
                                <p><b>Idioma original:</b> {{ISO6391.getNativeName(info.original_language) || 'indisponível'}}</p>
                                <p><b>Estreou em:</b> {{info.first_air_date || 'indisponível'}}</p>
                                <p><b>Último episódio em:</b> {{info.last_air_date || 'indisponível'}}</p>
                                <p><b>Próximo episódio em:</b> {{info.next_episode_to_air ? info.next_episode_to_air.air_date : 'indisponível'}}</p>
                                <p><b>Emissora:</b> {{info.networks.map(e => e.name).join(', ') || 'indisponível'}}</p>
                                <p><b>Número de episódios:</b> {{info.number_of_episodes || 'indisponível'}}</p>
                                <p><b>Número de temporadas:</b> {{info.number_of_seasons || 'indisponível'}}</p>
                                <p><b>País de origem:</b> {{info.origin_country.join(', ') || 'indisponível'}}</p>
                                <p><b>Popularidade:</b> {{info.popularity || 'indisponível'}}</p>
                                <p><b>Status:</b> {{info.status || 'indisponível'}}</p>
                                <p><b>Tipo:</b> {{info.type || 'indisponível'}}</p>
                                <p><b>Média de votos:</b> {{info.vote_average || 'indisponível'}}</p>
                                <p><b>Número de votos:</b> {{info.vote_count || 'indisponível'}}</p>

                                <div class="accordion">
                                    <div v-for="season in info.seasons" :key="season.id">
                                        <b-button block v-b-toggle="''+season.id" variant="outline-dark" class="my-1"> {{ season.name }}</b-button>
                                        <b-collapse :id="''+season.id" accordion="seasons" class="text-justify">
                                            <b-row class="my-3">
                                                <b-col cols="3" class="text-center">
                                                    <img :src="$utils.season_poster(season)" class="w-100 px-2">
                                                </b-col>
                                                <b-col cols="9">
                                                    <p><b>Número de episódios:</b> {{season.episode_count || 'indisponível'}}</p>
                                                    <p><b>Data de estreia:</b> {{season.air_date || 'indisponível'}}</p>
                                                    <p><b>Resumo:</b> {{season.overview || 'indisponível'}}</p>
                                                </b-col>
                                            </b-row>
                                        </b-collapse>
                                    </div>
                                </div>
                            </template>

                            <!-- PERSON -->
                            <template v-else-if="model.media_type === 'person'">
                                <p><b>Biografia:</b> {{info.biography || 'indisponível'}}</p>
                                <p><b>Conhecido(a) por:</b> {{info.known_for_department || 'indisponível'}}</p>
                                <p><b>Local de nascimento:</b> {{info.place_of_birth || 'indisponível'}}</p>
                                <p><b>Data de nascimento:</b> {{info.birthday || 'indisponível'}}</p>
                                <p><b>Data de falecimento:</b> {{info.deathday || 'indisponível'}}</p>
                                <p><b>Gênero:</b> {{info.gender === 1 ? 'Feminino' : (info.gender === 2 ? 'Masculino' : 'Não especificado')}}</p>
                                <p><b>Popularidade:</b> {{info.popularity || 'indisponível'}}</p>
                                <p><b>Também conhecido(a) como:</b> {{info.also_known_as.join(', ') || 'indisponível'}}</p>
                            </template>
                        </b-col>
                    </b-row>
                    <horizontal-scroll
                        class="my-5"
                        v-on:clicked="showResult"
                        title="Relacionados"
                        :results="related">
                    </horizontal-scroll>
                </b-container>
            </div>
        </template>
        <template v-else> 
            <div class="d-flex justify-content-center mt-5">
                <b-spinner></b-spinner>
            </div>
        </template>
    </div>
</template>

<script>
import axios from 'axios'
import ISO6391 from 'iso-639-1'
import menuHeader from './shared/Header.vue'
import horizontalScroll from './shared/HorizontalScroll.vue'

export default {
    props: ['model_prop'],
    components: {
        menuHeader,
        horizontalScroll,
    },
    computed: {
        backdrop() {
            if (this.model.backdrop_path)
                return `background-image: url(${this.$utils.backdrop(this.model)})`;
            return '';
        }
    },
    data() {
        return {
            loaded: false,
            model: {
                media_type: '',
                poster_path: '',
                profile_path: '',
                backdrop_path: '',
            },
            info: null,
            related: [],
            is_favorite: false,
            ISO6391: ISO6391,
            user_id: null,
        }
    },
    mounted() {
        if (!this.model_prop)
            this.$router.push('/home');
        else {
            this.model = this.model_prop;
            this.refresh();
        }
    },
    methods: {
        refresh() {
            this.loaded = false;
            this.user_id = this.$session.get("user_id");
            axios.get(this.backend + "/info", {
                params: {
                    user_id: this.user_id,
                    entity: this.model,
                }
            }).then(res => {
                console.log(res);
                this.info = res.data.info;
                this.related = res.data.related;
                this.is_favorite = res.data.is_favorite;
                this.loaded = true;
            }).catch(err => console.log(err));
        },
        setFavorite() {
            axios.put(this.backend + "/favorite", {
                user_id: this.user_id,
                entity: this.model,
                favorite: !this.is_favorite,
            }).then(res => {
                if (res.status === 200)
                    this.is_favorite = !this.is_favorite;
            }).catch(err => console.log(err));
        },
        showResult(result) {
            this.loaded = false;
            if (!result.media_type)
                result.media_type = this.model.media_type;
            this.model = result;
            this.refresh();
        },
        generateAnalysis() {
            axios.post(this.backend + "/analysis", {
                user_id: this.user_id,
                entity: this.model,
                query: this.$utils.original_title(this.model),
            }).then(res => {
                console.log(res);
            }).catch(err => console.log(err)); 
        },
    },
}
</script>

<style scoped>
.backdrop {
    background-position: center top;
    background-repeat: no-repeat;
    background-size: 100%;
    padding-top: 10%;

}

.poster {
    width: 185px;
    max-height: 278px;
}
</style>