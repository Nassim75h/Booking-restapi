<template>
    <h1>Single Property</h1>
    <div v-for="(property,index) in data" :key="index" v-if="data.length" class="post-list">
        <SingleProperty :property="property" />
    </div>
    <div  v-else>
        <h2 >Loading.....</h2>
    </div>
</template>

<script>
import getProperties from '@/composables/fetchProperties/getProperties';
import SingleProperty from './SingleProperty.vue';
export default {
    name: "PostList",
    components:{SingleProperty,},
    props :[],
    setup(){

        const {data,error,load} = getProperties() 
        load()

    return  {data,error}
    },


}
</script>

<style scoped>
.post-list{
  display: grid;
  color : white;
  background: #93bad9;
  border: 5px solid #2c3e50;
}


</style>