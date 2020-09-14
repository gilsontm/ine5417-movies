<template>
    <b-container class="vertical-center">
        <b-card class="w-50 mx-auto bg-light">
            <b-card-body class="p-2">
                <b-form-group label="Nome de usuário">
                    <b-form-input type="text" v-model="username"> </b-form-input>
                </b-form-group>
                <b-form-group label="Senha">
                    <b-form-input type="password" v-model="password"> </b-form-input>
                    <small v-if="error" class="text-danger"> Autenticação falhou. </small>
                </b-form-group>
                <b-button variant="success" @click="login">Entrar</b-button>
            </b-card-body>
        </b-card>
    </b-container>
</template>

<script>
import axios from 'axios'

export default {
    name: 'login',
    data() {
        return {
            username: null,
            password: null,
            error: false,
        }
    },
    beforeCreate() {
        // if (this.$session.exists()) this.$router.push('/home');
    },
    methods: {
        login() {
            this.error = false;
            axios.post(this.backend + '/login', {
                'username' : this.username,
                'password' : this.password,
            }).then(res => {
                if (res.status === 200) {
                    this.$session.start();
                    this.$session.set('user_id', res.data.id);
                    this.$session.set('user_name', res.data.name);
                    this.$session.set('user_email', res.data.email);
                    this.$session.set('user_username', res.data.username);
                    this.$router.push('/home');
                } else {
                    this.error = true;
                }
            }).catch(err => {
                this.error = true;
                console.log(err);
            });
        },
    }
}
</script>

<style scoped>

.vertical-center {
    min-height: 80%;
    min-height: 80vh;
    display: flex;
    align-items: center;
}

</style>
