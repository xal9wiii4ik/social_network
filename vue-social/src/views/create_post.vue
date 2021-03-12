<template>
  <div class="container">
    <div class="post__item">
      <!--    <div class="post__item__left__side">-->
      <!--      <img v-if="post.image" :src="`http://127.0.0.1:8000${post.image_url}`" />-->
      <!--      <img v-if="!post.image" :src="`http://127.0.0.1:8000/media/Python/image_title_xal9.Unknown.jpg`" />-->
      <!--    </div>-->
      <div class="post__item__right__side">
        <div class="post__item__info">
          <h5 class="post__item__title">Title: {{ title }}</h5>
          <h3 class="post__item__body">{{ body }}</h3>
        </div>
      </div>
    </div>
    <form class="create-post" @submit.prevent="submitHandler">
      <input type="text" v-model="title" placeholder="title">
      <textarea name="text" v-model="body" placeholder="Body"></textarea>
      <!--   TODO: <input type="file" v-model="file" placeholder="file">-->
      <select size="`${subjects.length}`" id="selected" v-model="subject">
        <option :value="`${subject.id}`" v-for="subject in subjects">{{subject.subject}}</option>
      </select>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
name: "create_post",
  data() {
    return {
      title: '',
      body: '',
      subject: '',
      // TODO: объявление после запроса
      subjects: '',
    }
  },
  methods: {
    async submitHandler() {
      const data = {
        title: this.title,
        body: this.body,
        subject: this.subject,
      }
      try {
        const response = await fetch('http://localhost:8000/posts/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(data)
        })
        console.log(response.status)
      // TODO: вывод статуса
      } catch (e) {
        console.log(e)
      }
    },
    async getSubjects() {
      try {
        const response = await fetch('http://localhost:8000/subjects/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          }
        })
        const subjects = await response.json()
        this.subjects = subjects
      } catch (e) {
        console.log(e)
      }
    },
    async isLogin() {
      if (!localStorage.getItem('username')) {
        await this.$router.push('/login')
      }
    }
  },
  async mounted() {
    await this.isLogin()
    await this.getSubjects()
  }
}
</script>

<style scoped>
.post__item {
  width: auto;
  height: auto;
  display: flex;
  flex-direction: row;
  text-align: center;
  align-items: center;
  background-color: deepskyblue;
  margin-top: 20px;
  margin-bottom: 20px;
}

.post__item__right__side {
  width: 70%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.post__item__left__side {
  width: 30%;
  padding: 20px;
}

.post__item__title {
  font-style: italic;
  font-size: 22px;
  padding-bottom: 20px;
}
</style>