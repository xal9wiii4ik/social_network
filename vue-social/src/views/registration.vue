<template>
  <form class="registration-form" @submit.prevent="submitHandler">
    <h1 class="registration">Registration</h1>
    <input type="text" v-model="first_name" placeholder="first_name">
    <input type="text" v-model="last_name" placeholder="last_name">
    <input type="email" v-model="email" placeholder="email">
    <input type="text" v-model="username" placeholder="username">
    <input type="password" v-model="password" placeholder="password">
    <input type="password" v-model="repeat_password" placeholder="repeat_password">
    <button type="submit">Submit</button>
  </form>
</template>

<script>
export default {
  name: "registration",
  data() {
    return {
      first_name: '',
      last_name: '',
      email: '',
      username: '',
      password: '',
      repeat_password: '',
    }
  },
  methods: {
    async submitHandler() {
      try {
        const data = {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          username: this.username,
          password: this.password,
          repeat_password: this.repeat_password
        }
        const response = await fetch('http://localhost:8000/auth/registration/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        if (response.status === 200) {
          console.log('ok')
        }else {
          console.log(response.json())
          // TODO: добавить отображение ошибки
        }
      }catch (e) {
        console.log(e)
      }
    }
  }
}
</script>

<style scoped>

</style>