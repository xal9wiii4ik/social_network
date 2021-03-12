<template>
  <div class="container">
    <div class="post__item">
      <div class="post__item__left__side">
        <!--      TODO: проблема с image-->
        <img v-if="post.image" :src="`http://127.0.0.1:8000${post.image_url}`"/>
        <img v-if="!post.image" :src="`http://127.0.0.1:8000/media/Python/image_title_xal9.Unknown.jpg`"/>
        <div class="post__item__likes_dislikes">
          <h5 class="post__item__likes">Likes: {{ post.number_likes }}</h5>
          <a v-on:click="likeHandler">Лайкнуть</a>
          <h5 class="post__item__dislikes">Dislikes: {{ post.number_dislikes }}</h5>
          <a v-on:click="dislikeHandler">Дизлайкнуть</a>
        </div>
      </div>
      <div class="post__item__right__side">
        <div class="post__item__info">
          <h5 class="post__item__title">Title: {{ post.title }}</h5>
          <h3 class="post__item__body">{{ post.body }}</h3>
        </div>
      </div>
    </div>
    <form v-if="is_owner" @submit.prevent="deleteHandler">
      <button>Delete</button>
    </form>
    <form v-if="is_owner" @submit.prevent="updateHandler">
      <input type="text" v-model="post.title">
      <textarea name="text" v-model="post.body"></textarea>
      <!--   TODO: <input type="file" v-model="file" placeholder="file">-->
      <button type="submit">update</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "post_detail",
  data() {
    return {
      post: null,
      is_owner: false
    }
  },
  methods: {
    async fetchPost() {
      try {
        const response = await fetch(`http://localhost:8000/posts/${this.$route.params.id}`)
        this.post = await response.json()
        if (localStorage.getItem('username') === this.post.username) {
          this.is_owner = true
        }
      } catch (e) {
        console.log(e)
      }
    },
    async deleteHandler() {
      try {
        const response = await fetch(`http://localhost:8000/posts/${this.$route.params.id}`, {
          method: 'Delete',
          headers: {
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          }
        })
        if (response.status === 204) {
          console.log('deleted')
        } else {
          console.log('Something was wrong')
        }
      } catch (e) {
        console.log(e)
      }
    },
    async updateHandler() {
      try {
        const data = {
          title: this.post.title,
          body: this.post.body
        }
        const response = await fetch(`http://localhost:8000/posts/${this.$route.params.id}/`, {
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
    async likeHandler() {
      const body = {
        like: 1,
        dislike: 0,
        post: this.$route.params.id
      }
      const response = await fetch(`http://localhost:8000/likedislike/${this.$route.params.id}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(body)
      })
    },
    async dislikeHandler() {
      const body = {
        dislike: 1,
        like: 0,
        post: this.$route.params.id
      }
      const response = await fetch(`http://localhost:8000/likedislike/${this.$route.params.id}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(body)
      })
    }
  },
  async mounted() {
    await this.fetchPost()
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

.post__item__likes_dislikes {
  display: flex;
}

.post__item__likes {
  width: 50%;
  font-size: 17px;
}

.post__item__dislikes {
  width: 50%;
  font-size: 17px;
}

.post__item__title {
  font-style: italic;
  font-size: 22px;
  padding-bottom: 20px;
}

.post__item__owner {
  display: flex;
  flex-direction: row;
}

.post__item__owner__info {
  font-style: italic;
  font-size: 20px;
  padding-top: 20px;
}

.post__item__owner__info:last-child {
  padding-left: 10px;
}
</style>