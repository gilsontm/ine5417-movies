<template>
    <div>
        <b-overlay :show="!loaded"> 
            <h3>
                <b> {{ title }} </b>
                <b-button variant="dark" @click="$bvModal.show('export-modal')" class="float-right">
                    Exportar
                </b-button>
            </h3>
            <hr>
            <div ref="analysis" class="bg-white">
                <b-row class="mb-3 mx-0" no-gutter>
                    <b-col cols="4" class="px-0">
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
                    <b-col cols="8" class="pr-0">
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
            </div>
        </b-overlay>

        <a class="d-none" ref="link"> </a>

        <b-modal
            id="export-modal"
            ok-title="Exportar"
            ok-variant="dark"
            cancel-title="Cancelar"
            @ok="exportAnalysis">
            <template v-slot:modal-title>
                Exportar análise
            </template>
            <b-form-group label="Escolha o formato:">
                <b-form-radio v-model="format" value="png"> Imagem (.png) </b-form-radio>
                <b-form-radio v-model="format" value="csv"> Documento de texto (.csv) </b-form-radio>
            </b-form-group>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios'
import * as htmlToImage from 'html-to-image'
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
            format: 'png',
        }
    },
    mounted() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.loaded = false;
            axios.get(this.backend + '/analysis/data', {
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
        },
        exportAnalysis() {
            if (this.format == 'png')
                htmlToImage.toPng(this.$refs.analysis).then(res => this.downloadAnalysis(res));
            else
                this.downloadAnalysis();
        },
        downloadAnalysis(data) {
            axios.post(this.backend + '/analysis/export', {
                image: data ? data : '',
                format: this.format,
                analysis_id: this.analysis_id,
            }, {
                responseType: 'blob',
            }).then(res => {
                const blob = new Blob([res.data], {type: res.headers['content-type']});
                this.$refs.link.href = window.URL.createObjectURL(blob);
                this.$refs.link.download = `analysis.${this.format}`;
                this.$refs.link.click();
                this.$utils.showSuccess(this, 'Sucesso ao exportar arquivo.');
            }).catch(err => {
                console.log(err);
                this.$utils.showError(this, 'Erro ao exportar arquivo.');
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