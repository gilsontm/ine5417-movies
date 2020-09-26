<template>
    <div>
        <h4> {{ title }} </h4>
        <hr/>
        <div class="horizontal-scroll">
            <template v-for="(result, index) in results">
                <b-link
                    :key="`scroll-${result.id}-${index}`"
                    @click="showResult(result)"
                    class="d-inline-block bg-light px-3 pt-3 mx-1 text-center">
                    <img class="poster" :src="$utils.poster(result)">
                    <p class="text-truncate" style="max-width: 185px;"> {{ $utils.title(result) }} </p>
                </b-link>
            </template>
            <p v-if="results.length === 0"> Nenhum resultado encontrado. </p>
        </div>
    </div>
</template>

<script>
export default {
    name: "horizontalScroll",
    props: ["title", "results"],
    data() {
        return {
            url: 'https://image.tmdb.org/t/p/w185',
            unavailable: require('../../assets/default_w185.jpg'),
        }
    },
    methods: {
        showResult(result) {
            this.$emit("clicked", result);
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