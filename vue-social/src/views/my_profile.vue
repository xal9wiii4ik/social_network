<template>
  <div class="container">
    <div class="user">
      <h3 class="user__info">{{user_profile.first_name}}</h3>
      <h3 class="user__info">{{user_profile.last_name}}</h3>
      <h3 class="user__info">{{user_profile.phone}}</h3>
      <h3 class="user__info">{{user_profile.username}}</h3>
    </div>
    <form class="registration-form" @submit.prevent="submitHandler">
      <h1 class="registration">My Profile</h1>
      <input type="text" v-model="user_profile.first_name" placeholder="first_name">
      <input type="text" v-model="user_profile.last_name" placeholder="last_name">
      <input type="text" v-model="user_profile.phone" placeholder="phone">
      <input type="email" v-model="user_profile.email" placeholder="email">
      <input type="text" v-model="user_profile.username" placeholder="username">
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
name: "my_profile",
  data() {
    return {
      user_profile: ''
    }
  },
  methods: {
    async submitHandler() {
      try {
        const data = {
          first_name: this.user_profile.first_name,
          last_name: this.user_profile.last_name,
          phone: this.user_profile.phone,
          email: this.user_profile.email,
          username: this.user_profile.username,
        }
        console.log(data)
        const response = await fetch(`http://localhost:8000/user_profile/${this.$route.params.id}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(data)
        })
        if (response.status === 200) {
          console.log('updated')
        } else {
          console.log('Something was wrong')
        }
      }catch (e) {
        console.log(e)
      }
    },
    async fetchUser() {
      const response = await fetch(`http://localhost:8000/user_profile/${this.$route.params.id}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${localStorage.getItem('access_token')}`
        }
      })
      this.user_profile = await response.json()
    }
  },
  async mounted() {
    await this.fetchUser()
  }
}
</script>

<style scoped>

</style>