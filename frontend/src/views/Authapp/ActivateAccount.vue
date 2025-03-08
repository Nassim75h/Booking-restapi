<template>
  <div>
    <h1>Account verification</h1>
    <h2>Email confirmation</h2>
      <div v-if="responseStatus" class="container">
        <h2>{{responseMessage}}</h2>
      </div>
      <div v-else>
        {{responseMessage}}
      </div>
  </div>
</template>

<script>
import {useRouter,useRoute} from "vue-router";
import useAxios from "@/composables/fetchCredentials/axios"
import {computed,onMounted,ref} from "vue";

export default {
  name: 'ActivateAccount',
  props: [],
  components: {},
  setup(props, { emit }) {
    const router = useRouter();
    const route = useRoute();
    const {activateAccount,responseStatus,responseMessage} = useAxios()
    const activationToken = ref(route.params.token);

    const call = async () => {
      await activateAccount(activationToken);

    }
    onMounted(() =>{

    })
    call()
    return {
      responseStatus,
      responseMessage,
    }
  }
}
</script>

<style lang="scss" scoped>

</style>