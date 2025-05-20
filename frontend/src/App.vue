<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/" class="logo-link">
          <img src="@/assets/logoo.png" alt="Booking Logo" class="logo-img">
          <span class="brand-name">EasyStayDZ</span>
        </router-link>
      </div>
      <NotificationContainer />
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import NotificationContainer from '@/components/Payment/NotificationContainer.vue';

export default defineComponent({
  name: 'App',
  components: {
    NotificationContainer
  }
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #191438;
}
body{
  background: url('@/assets/h.png') no-repeat center center/cover;

}
.navbar-brand {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 0.5rem;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #4A90E2;
}
</style>
