<template>
  <div class="container">
    <div class="user">
      <h3 class="user__info">{{ user_profile.first_name }}</h3>
      <h3 class="user__info">{{ user_profile.last_name }}</h3>
      <h3 class="user__info">{{ user_profile.phone }}</h3>
      <h3 class="user__info">{{ user_profile.username }}</h3>
      <a v-on:click="followHandler">Подписаться</a>
      <a v-on:click="unfollowHandler">Отписаться</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "guest_profile",
  data() {
    return {
      user_profile: ''
    }
  },
  methods: {
    async fetchUser() {
      const response = await fetch(`http://localhost:8000/guest_user_profile/${this.$route.params.id}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${localStorage.getItem('access_token')}`
        }
      })
      this.user_profile = await response.json()
    },
    async followHandler() {
      try {
        const data = {
          follower: this.$route.params.id
        }
        const response = await fetch(`http://localhost:8000/followers/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(data)
        })
        if (response.status === 201) {
          console.log('follow')
        } else {
          console.log('No follow')
        }
      } catch (e) {
        console.log(e)
      }
    },
    async unfollowHandler() {
      try {
        const data = {
          follower: this.$route.params.id
        }
        const response = await fetch(`http://localhost:8000/followers/${this.$route.params.id}/`, {
          method: 'Delete',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          }
        })
        if (response.status === 204) {
          console.log('un follow')
        } else {
          console.log('No unfollow')
        }
      } catch (e) {
        console.log(e)
      }
    }
  },
  async mounted() {
    await this.fetchUser()
  }
}
</script>

<style scoped>

</style>