<template>
  <h1>Sign up</h1>
  <NavBar></NavBar>
  <div class="register">
    <RegisterForm></RegisterForm>
  </div>
</template>

<script>
import {ref,computed,onMounted} from "vue";
import {useRouter} from "vue-router";
import RegisterForm from "@/components/Auth/RegisterForm.vue";
import useAxios from "@/composables/fetchCredentials/axios";
import NavBar from "@/components/Snippets/NavBar.vue";
export default {
  name: 'RegisterView',
  components: {NavBar, RegisterForm},
  props: [],
  setup(props) {
    const router = useRouter();
    const {isAuthenticatedComputed} = useAxios()

    onMounted(() => {
      if(isAuthenticatedComputed.value){
        router.push({name : "home"})
      }
    })

    return {
      isAuthenticatedComputed
    }
  }
}
</script>

<style  scoped>
.register {
  margin : 20px 10px ;
}
</style>