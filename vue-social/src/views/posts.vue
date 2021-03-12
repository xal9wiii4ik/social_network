<template>
  <div v-if="!loading && isAuth">
    <div class="posts__title">
      <h1 class="posts__title__title">Posts</h1>
    </div>
    <div class="post__wrapper">
      <post-item
          v-for="post in posts"
          v-bind:key="post.id"
          v-bind:post="post">
      </post-item>
    </div>
  </div>
  <div v-else-if="!isAuth && !loading">
    No Permissions | uppercase
  </div>
</template>

<script>
import postItem from '@/components/post-item';
import {mapActions, mapGetters} from 'vuex';
export default {
  name: 'posts',
  components: {'post-item': postItem},
  data() {
    return {
      loading: true,
      isAuth: false,
      counter: 0,
      posts: [],
      token: null,
    }
  },
  methods: {
    //объявлем ф-ии но не вызываем
    ...mapActions(['fetchPosts']),
    updatePosts() {
      this.posts = this.getPosts;
      if (this.posts.length > 0) {
        this.loading = false;
        this.isAuth = true;
      }
    },
  },
  computed: {
    // вычисляемые свойства
    ...mapGetters(['getPosts'])
  },
  async mounted() {
    // вызываем ф-ии
    await this.fetchPosts();
    this.updatePosts();
  }
}
</script>
<style scoped lang="scss">

</style>