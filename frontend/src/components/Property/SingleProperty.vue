<template>
        <div class="property-details" >
            <router-link :to="{ name :'property-details' , params :{id :property.id }}">
                <h2>Name :{{ property.title }}</h2>
            </router-link>
            <h2>Price :{{ property.price_per_night }}</h2>
            <h2>Owner :{{ property.host.username }}</h2>
        </div>
</template>

<script>
import { computed, onMounted } from 'vue';
export default {
    name:"SinglePost",
    components :{},
    props : ['property'],
    setup(){
        return {}
    }
}
</script>

<style scoped>

.property-details{
}
</style>