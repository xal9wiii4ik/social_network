<template>
  <div id="app">
    <div id="nav">
      <nav class="header__nav">
        <ul class="header__list">
          <li class="header__list__item">
            <router-link to="/posts">Posts</router-link>
          </li>
          <li class="header__list__item">
            <router-link to="/create_post">Create post</router-link>
          </li>
          <li class="header__list__item">
            <router-link to="/my_posts">My posts</router-link>
          </li>
          <li class="header__list__item">
            <router-link v-if="!is_login"  class="header__list__link" to="/login">Login</router-link>
            <router-link v-if="is_login"  class="header__list__link" :to="`/my_profile/${user_id}`">Me</router-link>
            <a v-if="is_login" v-on:click="logout"  class="header__list__link">logout</a>
          </li>
        </ul>
      </nav>
    </div>
    <div class="app__content">
      <router-view>

      </router-view>
    </div>
    <div class="container">
      <h1>Hi)</h1>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from "vuex";

  export default {
    name: 'App',
    data() {
      return {
        is_login: false,
        user_id: ''
      }
    },
    computed: {
      ...mapGetters(['getLoginInfo'])
    },
    methods: {
      async getLogin() {
        if (localStorage.getItem('user_id')) {
          this.is_login = true
          this.user_id = localStorage.getItem('user_id')
        }else {
          this.is_login = false
        }
      },
      async logout() {
        localStorage.clear()
        this.is_login = false
        await this.$router.push('/login')
      }
    },
    async mounted() {
      await this.getLogin()
    }
  }
</script>

<style>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: sans-serif;
}

html {
  scroll-behavior: smooth;
  overflow-x: hidden;
}

body {
  min-height: 100vh;
  background-attachment: fixed;
  overflow-x: hidden;
}

img {
  max-width: 100%;
  height: auto;
  vertical-align: middle;
}

a {
  text-decoration: none;
}

button {
  text-decoration: none;
  cursor: pointer;
  border: none;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav {
  display: flex;
  justify-content: space-between;
  background-color: rgba(10, 247, 247, .125);
}

.header__nav {
  width: 40%;
  text-transform: uppercase;
  padding-top: 5px;
  padding-right: 5px;
  padding-bottom: 5px;
}

.header__list {
  list-style-type: none;
  text-decoration: none;
  display: flex;
}

.header__list__item {
  padding-left: 50px;
}

.header__list__link {
  font-weight: bold;
  opacity: .7;
  color: black;
}

.header__list__item {
  padding-left: 50px;
}

.header__list__link:last-child {
  padding-left: 50px;
}

.header__list__link:hover {
  opacity: 1;
}
</style>
