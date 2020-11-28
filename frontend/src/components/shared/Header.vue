<template>
    <div>
        <b-navbar class="header navbar bg-light">
            <b-navbar-brand>
                <b-button
                    v-if="!isHome"
                    variant="outline-dark"
                    class="mx-1"
                    @click="$router.push('/home')">
                    Voltar
                </b-button>
            </b-navbar-brand>
            <b-navbar-brand v-if="title" class="ml-auto">
                {{ title }}
            </b-navbar-brand>
            <b-navbar-nav class="ml-auto">
                <b-dropdown :text="`Olá, ${username}!`" right class="m-2" variant="outline-dark">
                    <b-dropdown-item @click="$router.push('/favorites')" :disabled="isFavorites">Ver favoritos</b-dropdown-item>
                    <b-dropdown-item @click="$router.push('/analysis')" :disabled="isAnalysis">Ver análises</b-dropdown-item>
                    <b-dropdown-divider></b-dropdown-divider>
                    <b-dropdown-item @click="logout" variant="danger">Sair</b-dropdown-item>
                </b-dropdown>
            </b-navbar-nav>
        </b-navbar>
    </div>
</template>

<script>
export default {
    name: 'menu-header',
    props: ['title', 'isHome', 'isFavorites', 'isAnalysis'],
    data() {
        return {
            username: '',
        }
    },
    beforeCreate() {
        if (!this.$session.exists())
            this.$router.push('/login');
    },
    mounted() {
        this.username = this.$session.get("user_username");
    },
    methods: {
        logout() {
            this.$session.destroy();
            this.$router.push("/login");
        },
    }
}
</script>

<style scoped>

.header {
    min-height: 7%;
    min-height: 7vh;
    max-height: 7%;
    max-height: 7vh;
    height: 7%;
}

</style>
