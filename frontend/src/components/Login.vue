<template>
    <b-container class="mt-5">
        <b-card class="w-50 mx-auto bg-light">
            <b-card-body class="p-2">
                <div v-if="showLogin">
                    <h5> Login </h5>
                    <hr/>
                    <b-form-group label="Nome de usuário">
                        <b-form-input type="text" v-model="login.username"> </b-form-input>
                    </b-form-group>
                    <b-form-group label="Senha">
                        <b-form-input type="password" v-model="login.password"> </b-form-input>
                        <small v-show="login.fieldsError" class="text-danger"> Preencha todos os campos. </small>
                        <small v-show="login.serverError" class="text-danger"> Autenticação falhou. </small>
                    </b-form-group>
                    <b-button variant="success" @click="doLogin">Entrar</b-button>
                    <b-link class="float-right" @click="toggleView"> Ainda não possui uma conta? Registre-se! </b-link>
                </div>
                <div v-else>
                    <h5> Registro </h5>
                    <hr/>
                    <b-form-group label="Nome">
                        <b-form-input type="text" v-model="register.name"> </b-form-input>
                    </b-form-group>
                    <b-form-group label="E-mail">
                        <b-form-input type="email" v-model="register.email"> </b-form-input>
                    </b-form-group>
                    <b-form-group label="Nome de usuário">
                        <b-form-input type="text" v-model="register.username"> </b-form-input>
                    </b-form-group>
                    <b-form-group label="Senha">
                        <b-form-input type="password" v-model="register.password"> </b-form-input>
                        <small v-if="register.fieldsError" class="text-danger"> Preencha todos os campos. </small>
                        <small v-if="register.serverError" class="text-danger"> Falha ao registrar. </small>
                        <small v-if="register.serverSuccess" class="text-success"> Registrado com sucesso! </small>
                    </b-form-group>
                    <b-button variant="success" @click="doRegister">Registrar</b-button>
                    <b-link class="float-right" @click="toggleView"> Já possui uma conta? Faça login! </b-link>
                </div>
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
            login: {
                username: null,
                password: null,
                fieldsError: false,
                serverError: false,
            },
            register: {
                name: null,
                email: null,
                username: null,
                password: null,
                fieldsError: false,
                serverError: false,
                serverSuccess: false,
            },
            showLogin: true,
        }
    },
    beforeCreate() {
        if (this.$session.exists()) this.$router.push('/home');
    },
    methods: {
        doLogin() {
            this.login.fieldsError = this.login.serverError = false;
            if (!this.login.username || ! this.login.password) {
                this.login.fieldsError = true;
                return;
            }
            axios.post(this.backend + '/login', {
                'username' : this.login.username,
                'password' : this.login.password,
            }).then(res => {
                if (res.status === 200) {
                    this.$session.start();
                    this.$session.set('user_id', res.data.id);
                    this.$session.set('user_name', res.data.name);
                    this.$session.set('user_email', res.data.email);
                    this.$session.set('user_username', res.data.username);
                    this.$router.push('/home');
                } else {
                    this.login.serverError = true;
                }
            }).catch(err => {
                this.login.serverError = true;
                console.log(err);
            });
        },
        doRegister() {
            this.register.fieldsError = this.register.serverError = this.register.serverSuccess = false;
            if (!this.register.name || !this.register.email || !this.register.username || !this.register.password) {
                this.register.fieldsError = true;
                return;
            }
            axios.post(this.backend + '/register', {
                'name' : this.register.name,
                'email' : this.register.email,
                'username' : this.register.username,
                'password' : this.register.password,
            }).then(res => {
                if (res.status === 200) {
                    this.register.serverSuccess = true;
                } else {
                    this.register.serverError = true;
                }
            }).catch(err => {
                this.register.serverError = true;
                console.log(err);
            });
        },
        toggleView() {
            this.showLogin = !this.showLogin;
        },
    }
}
</script>

<style scoped>

</style>
