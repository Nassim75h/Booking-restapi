<template>
    <div class="nav">
    <nav>
      <div  v-if="isAuthenticatedComputed"  class="nav-auth">
        <p class="user-details">user : {{userCredentials?.username}}</p>
        <router-link :to="{name : 'home' }" class="nav-link"> Home</router-link> |
        <a class="nav-link" @click="logout">Logout</a> |
        <router-link :to="{name : 'owned-properties'}" class="nav-link">Properties</router-link>
      </div>
      <div v-else class="nav-anon">
        <router-link  :to="{name :'login' }" class="nav-link">Login</router-link > |
        <router-link :to="{name : 'register'}" class="nav-link">Sign up</router-link>/

      </div>
    </nav>
    </div>
</template>

<script>
import useAxios from '../../composables/fetchCredentials/axios.js'
import {onMounted} from "vue";

export default {
  name : "NavBar",
  components: {},
  props:[],
  setup (props){

    const {logout,isAuthenticatedComputed,fetchUserDetails,userCredentials} = useAxios()
    onMounted( () => {
      fetchUserDetails()
    })

    return {
      logout,
      isAuthenticatedComputed,
      userCredentials,
    }
  }

}
</script>

<style>

.nav{
  display: flex;
  padding: 15px 10px;
  height: 50px;
  border-radius: 8px;
  align-items: center;
  justify-content: center;
}
nav{
  align-self: center;
}
.user-details{
  float: left;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: 0.9rem;
  padding: 1vh 2vh ;
  border-radius: 0.4rem;
  background: #26415e;
  color: rgb(236, 176, 63);
  margin: 0.5vh;
}
.nav-link {
  cursor: pointer;
  padding: 10px 20px;
  color: rgb(225, 200, 63);
  font-size: 1.2em;
  text-decoration: none;
  border-radius: 8px;
  background: #1a2e44;
  width: 100px;
  text-align: center;
  display: inline-block;
  transition: all 0.3s ease-in-out;
}

.nav-link:hover {
  background: #284b70;
  color: rgb(177, 160, 61);
  transform: scale(1.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.nav-link.router-link-exact-active {
  background: #0b1b32;
  font-weight: bold;
}
.nav-link:hover {
  background: #0b1b32;
}
</style>