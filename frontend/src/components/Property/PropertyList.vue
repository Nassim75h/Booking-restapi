<template>
    <h1>Properties</h1>
    <div class="property-list">
      <div v-for="(property,index) in data" :key="index" v-if="data.length" class="post-list">
          <SingleProperty :property="property" />
      </div>
      <div  v-else>
          <h2  >You dont have any listed Properties</h2>
      </div>
    </div>
</template>

<script>
import getProperties from '@/composables/fetchProperties/getProperties';
import SingleProperty from './SingleProperty.vue';

export default {
    name: "PropertyList",
    components:{SingleProperty},
    props :['data','error'],
    setup(){


    return  {}
    },


}
</script>

<style scoped>
.property-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-auto-rows: minmax(150px, auto);
  grid-gap: 2vh;
  background: rgba(251, 245, 240, 0.9); /* Soft background with slight transparency */
  padding: 2vh;
  width: 100%;
  box-sizing: border-box;
  border-radius: 15px;
  backdrop-filter: blur(10px); /* Adds a blur effect */
  transition: all 0.3s ease-in-out;
}

.post-list {
  background: #a7c7ff;
  border-radius: 10px;
  padding: 15px;
  color:rgb(32, 43, 80);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

/* Hover effects */
.post-list:hover {
  transform: translateY(-5px);
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
}

/* Subtle pulse animation */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

/* Apply animation */
.property-list {
  animation: pulse 3s infinite ease-in-out;
}

/* Responsive design */
@media (max-width: 300px) {
  .property-list {
    background: red;
    min-width: 300px;
    backdrop-filter: blur(5px);
  }
}
</style>
