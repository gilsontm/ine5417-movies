<template>
    <div>
        <b-overlay :show="!loaded"> 
            <h3> <b> {{ title }} </b> </h3>
            <hr>
            <b-row class="my-3" no-gutter>
                <b-col cols="4">
                    <b-card class="h-100" no-body>
                        <b-card-header> <h4 class="mb-0"> Sentimento </h4> </b-card-header>
                        <div class="text-center py-3">
                            <p
                                class="mb-0"
                                style="font-size: 16vh;"
                                :class="sentiment >= 50 ? 'text-success' : 'text-danger'"> 
                                {{ Math.round(sentiment) }}%
                            </p>
                            <small class="text-center"> dos tweets demonstram sentimento positivo. </small>
                         </div>
                    </b-card>
                </b-col>
                <b-col cols="8">
                    <b-card class="h-100" no-body>
                        <b-card-header> <h4 class="mb-0"> Nuvem de palavras </h4> </b-card-header>
                        <div class="h-100 py-3">
                            <vue-word-cloud
                                :words="words"
                                :animation-duration="0">
                            </vue-word-cloud>
                        </div>
                    </b-card>
                </b-col>
            </b-row>
            <div v-if="coordinates" class="my-3">
                <b-card no-body> 
                    <b-card-header> <h4 class="mb-0"> Mapa de calor </h4> </b-card-header>
                    <heatmap
                        style="height: 72vh;"
                        class="w-100"
                        :coordinates="coordinates">
                    </heatmap>
                </b-card>
            </div>
        </b-overlay>
    </div>
</template>

<script>
import axios from 'axios'
import VueWordCloud from 'vuewordcloud'
import heatmap from './Heatmap.vue'

export default {
    name: 'analysisData',
    props: ['title', 'analysis_id'],
    components: {
        [VueWordCloud.name]: VueWordCloud,
        heatmap,
    },
    data() {
        return {
            loaded: false,
            sentiment: 0,
            coordinates: [],
            words: [],
        }
    },
    mounted() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.loaded = false;
            axios.get(this.backend + "/analysis/data", {
                params: {
                    analysis_id: this.analysis_id,
                }
            }).then(res => {
                this.sentiment = res.data.sentiment;
                this.coordinates = res.data.coordinates;
                this.words = [];
                res.data.words.forEach(word => {
                    this.words.push([word.text, word.quantity]);
                });
                this.loaded = true;
            }).catch(err => {
                console.log(err);
            });
        }
    },
    watch: {
        analysis_id() {
            this.refresh();
        }
    }
}
</script>

<style scoped>

</style>