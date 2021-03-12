<template>
  <div class="post__item">
    <div class="post__item__left__side">
        <img v-if="post.image" :src="`http://127.0.0.1:8000${post.image_url}`" />
        <img v-if="!post.image" :src="`http://127.0.0.1:8000/media/Python/image_title_xal9.Unknown.jpg`" />
      <div class="post__item__likes_dislikes">
        <h5 class="post__item__likes">Likes: {{ post.number_likes }}</h5>
        <h5 class="post__item__dislikes">Dislikes: {{ post.number_dislikes }}</h5>
      </div>
    </div>
    <div class="post__item__right__side">
      <div class="post__item__info">
        <h5 class="post__item__title">Title: {{ post.title }}</h5>
        <router-link :to="`/posts/${post.id}`">Перейти к посту</router-link>
      </div>
      <div class="post__item__owner">
        <h5 class="post__item__owner__info">Username: {{ post.username }}</h5>
        <h5 class="post__item__owner__info">Count of posts: {{ post.post_count }}</h5>
        <router-link :to="`/guest_profile/${post.user_id}`">Перейти к пользователю</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "post-item",
  props: {
    post: {
      type: Object,
      required: true,
      default: () => {
      },
    }
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