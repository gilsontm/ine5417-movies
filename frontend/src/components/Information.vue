<template>
    <div>
        <menuHeader :title="Informação" :isHome="false"> </menuHeader>

        <!-- MOVIE -->
        <template v-if="model.media_type === 'movie'">

        </template>

        <!-- TV -->
        <template v-else-if="model.media_type === 'tv'">

        </template>

        <!-- PERSON -->
        <template v-else-if="model.media_type === 'person'">

        </template>
    </div>
</template>

<script>
export default {
    props: ['model'],
    data() {
        return {
            test: null,
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

</style>