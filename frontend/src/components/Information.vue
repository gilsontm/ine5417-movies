<template>
    <div>
        <menu-header :title="$utils.title(model)" :isHome="false"> </menu-header>
        <template v-if="loaded">
            <b-overlay :show="overlay" no-wrap fixed> </b-overlay>
            <div :class="backdrop ? 'backdrop' : ''" :style="backdrop">
                <b-container class="bg-light pt-4">
                    <b-row class="no-gutters">
                        <b-col cols="2" class="text-center">
                            <img :src="$utils.poster(model)" class="w-100">
                            <b-button class="mt-3" block variant="dark" @click="setFavorite"> {{ is_favorite ? "Desfavoritar" : "Favoritar" }} </b-button>
                            <b-button class="mt-3" block variant="dark" @click="generateAnalysis"> Gerar análise </b-button>
                        </b-col>
                        <b-col cols="8" class="px-4">
                            <h4><b>{{$utils.title(model)}}</b></h4>
                            <hr>
                            <div class="text-justify">
                                <!-- MOVIE -->
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
                            </div>
                            <div class="mt-5">
                                <h5> <b> Comentários </b> </h5>
                                <template v-if="comments && comments.length > 0">
                                    <div v-for="comment in comments" :key="comment.id" class="mb-4 text-break">
                                        <p class="m-0">
                                            <b class="text-info"> {{comment.user.username}} </b>
                                        </p>
                                        <p class="m-0"> {{comment.text}} </p>
                                        <small class="text-info"> {{ comment.created_at }} </small>
                                    </div>
                                </template>
                                <template v-else>
                                    <p> Nenhum comentário disponível. </p>
                                </template>
                            </div>
                            <div class="mt-5">
                                <h5> <b> Adicione um comentário  </b> </h5>
                                <b-textarea v-model="new_comment"></b-textarea>
                                <b-button variant="dark" class="float-right my-2" @click="postComments"> Enviar </b-button>
                            </div>
                        </b-col>
                        <b-col cols="2">
                            <h4> <b> Tweets recentes </b> </h4>
                            <hr>
                            <div v-if="recent_tweets && recent_tweets.length > 0" class="overflow-auto" style="height: 100vh">
                                <div v-for="tweet in recent_tweets" :key="tweet.id" class="mb-4" style='font-size: 0.75em;'>
                                    <p class="m-0">
                                        <b class="text-info"> {{ tweet.author_name }} </b>
                                        <small> @{{ tweet.author_address }} </small>
                                    </p>
                                    <p class="m-0"> {{ tweet.text }} </p>
                                    <p class="m-0">
                                        <small class="text-info text-right"> {{ tweet.created_at }} </small>
                                    </p>
                                </div>
                            </div>
                            <template v-else>
                                <p> Indisponível. </p>
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
            recent_tweets: [],
            comments: [],
            new_comment: "",
            ISO6391: ISO6391,
            user_id: null,
            overlay: false,
        }
    },
    mounted() {
        if (!this.model_prop)
            this.$router.push('/home');
        else {
            this.model = this.model_prop;
            this.model.title = this.$utils.title(this.model);
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
                    query: this.$utils.original_title(this.model),
                }
            }).then(res => {
                console.log(res);
                this.info = res.data.info;
                this.related = res.data.related;
                this.is_favorite = res.data.is_favorite;
                this.recent_tweets = res.data.recent_tweets;
                this.refreshComments();
                this.loaded = true;
            }).catch(err => console.error(err));
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
            this.overlay = true;
            axios.post(this.backend + '/analysis', {
                user_id: this.user_id,
                entity: this.model,
                query: this.$utils.original_title(this.model),
            }).then(res => {
                console.log(res);
                this.overlay = false;
                this.$utils.showSuccess(this, 'Clique aqui para visualizar os resultados!', '/analysis');
            }).catch(err => {
                this.overlay = false;
                console.log(err)
                this.$utils.showError(this, 'Erro ao gerar análises.')
            });
        },
        refreshComments() {
            axios.get(this.backend + '/comments', {
                params: {
                    tmdb_id: this.model.id,
                }
            }).then(res => {
                this.comments = [];
                res.data.results.forEach(e => this.comments.push(e));
            }).catch(err => console.log(err));
        },
        postComments() {
            axios.post(this.backend + '/comments', {
                entity: this.model,
                user_id: this.user_id,
                text: this.new_comment,
            }).then(() => {
                this.refreshComments();}
            ).catch(err => console.log(err));
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