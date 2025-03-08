<template>
  <h1>Home</h1>
  <NavBar /> 
  <div class="home">
    <PropertyList v-if="data" :data="data" :error="error"/>
  </div>
</template>

<script>
import { ref ,onMounted } from 'vue';
import getProperties from '@/composables/fetchProperties/getProperties';
import PropertyList from '@/components/Property/PropertyList.vue';
import NavBar from '@/components/Snippets/NavBar.vue';
export default  {
  name: 'HomeView',
  components :{PropertyList,NavBar},
  setup(){
        const {data,error,load} = getProperties() 
        load()
    
    return{data,error}
  },

}
</script>
<style>
.h1{
  color: rgb(158, 142, 54);
}
</style>