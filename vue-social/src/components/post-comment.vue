<template>
  <div class="container">
    <div class="comment">
      <h2>{{ comment.text }}</h2>
      <h3>{{ comment.id }}</h3>
      <form class="answer-form" @submit.prevent="submitHandler">
        <h4 class="registration">Reply to comment</h4>
        <input type="text" v-model="text" placeholder="text">
        <button type="submit">Submit</button>
      </form>
    </div>
    <post-comment
        v-if="comment.child"
        v-for="comment in comment.child"
        v-bind:key="comment.id"
        v-bind:comment="comment">
    </post-comment>
  </div>
</template>

<script>
export default {
  name: "post-comment",
  props: {
    comment: {
      type: Object,
      required: true,
      default: () => {
      },
    }
  },
  data() {
    return {
      st: true,
      text: ''
    }
  },
  methods: {
    async submitHandler() {
      try {
        const data = {
          text: this.text,
          parent: this.comment.id,
          post: this.comment.post
        }
        const response = await fetch(`http://localhost:8000/comments/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify(data)
        })
        const response_data = await response.json()
        if (response.status === 201) {
          location.reload()
          console.log('yes')
        }else {
          console.log('no')
        }
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>

<style scoped>
.container {
  width: 660px;
  padding: 20px;
}

.comment {
  display: flex;
  min-height: 100px;
  width: 555px;
  padding-top: 7px;
  padding-left: 20px;
}
</style>