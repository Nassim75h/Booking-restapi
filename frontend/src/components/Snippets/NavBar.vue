<template>
    <div class="nav">
    <nav>
      <div v-if="isAuthenticatedComputed" class="nav-auth">
        <p v-if="userCredentials" class="user-details">
          <i class="fas fa-user"></i> {{ userCredentials.username }}
        </p>
        <router-link :to="{name: 'home'}" class="nav-link">
          <i class="fas fa-home"></i> Home
        </router-link>
        <router-link :to="{name: 'owned-properties'}" class="nav-link">
          <i class="fas fa-building"></i> My Properties
        </router-link>
        <router-link :to="{name: 'manage-bookings'}" class="nav-link">
          <i class="fas fa-calendar-alt"></i> My Bookings
        </router-link>
        <a href="#" class="nav-link" @click.prevent="handleLogout">
          <i class="fas fa-sign-out-alt"></i> Logout
        </a>
      </div>
      <div v-else class="nav-anon">
        <router-link :to="{name: 'login'}" class="nav-link">Login</router-link> |
        <router-link :to="{name: 'register'}" class="nav-link">Sign up</router-link>
      </div>
    </nav>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default {
  name: 'NavBar',
  setup() {
    const loading = ref(false)
    const error = ref(null)
    const { logout, isAuthenticatedComputed, fetchUserDetails, userCredentials } = useAxios()

    const loadUserDetails = async () => {
      try {
        loading.value = true
        error.value = null
        await fetchUserDetails()
      } catch (err) {
        console.error('Error loading user details:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handleLogout = () => {
      if (confirm('Are you sure you want to log out?')) {
        logout()
      }
    }

    onMounted(() => {
      loadUserDetails()
    })

    return {
      loading,
      error,
      userCredentials,
      isAuthenticatedComputed,
      handleLogout
    }
  }
}
</script>

<style>
.nav {
  display: flex;
  padding: 15px 10px;
  height: 50px;
  border-radius: 8px;
  align-items: center;
  justify-content: center;
}

nav {
  align-self: center;
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-details {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 0.9rem;
  padding: 10px 20px;
  border-radius: 8px;
  background: #26415e;
  color: rgb(236, 176, 63);
  margin: 0;
  min-width: 120px;
  text-align: center;
}

.nav-link {
  cursor: pointer;
  padding: 10px 20px;
  color: rgb(225, 200, 63);
  font-size: 1.2em;
  text-decoration: none;
  border-radius: 8px;
  background: #1a2e44;
  min-width: 120px;
  text-align: center;
  display: inline-block;
  margin: 0;
  transition: all 0.3s ease-in-out;
}

.nav-link:hover {
  background: #284b70;
}

.nav-link.router-link-active {
  background: #284b70;
  transform: scale(1.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.nav-link.router-link-exact-active {
  color: rgb(236, 176, 63);
  font-weight: bold;
}

.nav-link:hover {
  background: #0b1b32;
}

.nav-link.router-link-exact-active {
  background: #0b1b32;
  font-weight: bold;
}
</style>