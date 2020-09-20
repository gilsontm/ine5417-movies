<template>
    <div>
        <b-navbar class="header navbar bg-light">
            <b-navbar-brand>
                <b-button
                    v-if="!isHome"
                    variant="dark"
                    class="mx-1"
                    size="sm"
                    @click="toHome">
                    Home
                </b-button>
            </b-navbar-brand>
            <b-navbar-brand v-if="title" class="ml-auto">
                {{ title }}
            </b-navbar-brand>
            <b-navbar-nav class="ml-auto">
                <b-button
                    variant="danger"
                    class="ml-1"
                    size="sm"
                    @click="logout">
                    Sair
                </b-button>
            </b-navbar-nav>
        </b-navbar>
    </div>
</template>

<script>
export default {
    name: 'menuHeader',
    props: ['title', 'isHome'],
    data() {
        return { }
    },
    beforeCreate() {
        if (!this.$session.exists()) this.$router.push('/login');
    },
    methods: {
        toHome() {
            this.$router.push('/home');
        },
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
