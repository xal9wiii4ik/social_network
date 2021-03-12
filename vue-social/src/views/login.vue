<template>
  <div>
    <form class="login-form" @submit.prevent="submitLoginHandler">
      <h1 class="log">Login</h1>
      <input type="text" v-model="login" placeholder="login">
      <input type="password" v-model="password" placeholder="password">
      <button type="submit">Войти</button>
      <router-link to="/registration">registration</router-link>
    </form>
    <form class="remember-form" @submit.prevent="submitRememberHandler">
      <h1>Remember</h1>
      <input type="email" v-model="email" placeholder="email">
      <button type="submit">Отправить</button>
    </form>
  </div>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "login",
  data() {
    return {
      login: '',
      password: '',
      email: ''
    }
  },
  methods: {
    ...mapActions(['fetchToken']),
    async submitLoginHandler() {
      try {
        const data = {
          username: this.login,
          password: this.password
        }
        if (await this.fetchToken(data)) {
          await this.$router.push('/posts')
          location.reload()
        } else {
          console.log('False login')
        }
      } catch (e) {
        alert(e);
      }
    },
    async submitRememberHandler() {
      try {
        const data = {
          email: this.email
        }
        const response = await fetch(`http://localhost:8000/auth/reset_password/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        })
        if (response.status === 200) {
          console.log('200')
        } else {
          console.log('400')
        }
      } catch (e) {
        console.log(e)
      }
    }
  },
}
</script>

<style scoped>

</style>