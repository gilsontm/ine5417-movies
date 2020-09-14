<template>
    <div>
        <menuHeader :title="'Página inicial'" :isHome="true"> </menuHeader>
        <h1 class="text-center"> Página inicial </h1>
    </div>
</template>

<script>

import menuHeader from './Header.vue'

export default {
    name: 'home',
    components: {
        menuHeader,
    },
}
</script>

<style scoped>

</style>