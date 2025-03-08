<template>
    <h1>Property Detail</h1>
    <NavBar></NavBar>
    <div v-if="property" class="details">
         <h1 >{{ property.title }}</h1>

        <p>Price : {{ property.price_per_night }}</p>
        <p> Owner : {{ property.host.username }}</p>
        <p> Address : {{ property.address}}</p>

        <div v-for="(images,index) in property.images.slice(0,5)" :key="index" class="images">
            <img :src="images.image" :alt="index">
        </div> 

     </div>
 </template>

<script>
import NavBar from '../Snippets/NavBar.vue';
export default {
    name : "PropertyDetail",
    components :{NavBar},
    props :['property'],
    setup (){
    return {}
    },
} 
</script>

<style>


</style>