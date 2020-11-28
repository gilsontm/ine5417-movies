<template>
    <div>
        <menu-header title="Análises"></menu-header>
        <b-container v-if="loaded">
            <b-card no-body class="my-5">
                <b-card-header> <h4 class="mb-0"> Selecione uma análise </h4> </b-card-header> 
                <template v-if="analysis.length > 0">
                    <b-list-group>
                        <b-list-group-item
                            button
                            :active="instance.id === selected.id"
                            v-for="instance in analysis"
                            :key="instance.id"
                            @click="selected = instance">
                            {{ instance.entity.title }}
                            <small class="text-dark float-right"> {{instance.created_at}} </small>
                            <b-badge v-if="instance.is_new" variant="success"> Novo! </b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </template>
                <template v-else>
                    <p class="p-4 mb-0"> Nenhuma análise encontrada. </p>
                </template>
            </b-card>
            <div v-if="selected.id" class="my-5">
                <analysis-data :title="selected.entity.title" :analysis_id="selected.id"> </analysis-data>
            </div>
        </b-container>
        <div v-else class="d-flex justify-content-center mt-5">
            <b-spinner></b-spinner>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import menuHeader from './shared/Header.vue'
import analysisData from './shared/AnalysisData.vue'

export default {
    name: 'analysis',
    components: {
        menuHeader,
        analysisData
    },
    data() {
        return {
            loaded: false,
            analysis: [],
            selected: {id: null},
        }
    },
    mounted() {
        this.refresh();
    },
    methods: {
        refresh() {
            this.loaded = false;
            this.user_id = this.$session.get("user_id");
            axios.get(this.backend + '/analysis/list', {
                params: {
                    user_id: this.user_id,
                },
            }).then(res => {
                this.analysis = res.data.analysis;
                this.loaded = true;
            }).catch(err => console.log(err));
        },
    }
}
</script>

<style scoped>

</style>