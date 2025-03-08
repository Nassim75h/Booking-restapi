<template>
    <PropertyDetail :property="property"/>
    </template>

<script>
import PropertyDetail from '@/components/Property/PropertyDetail.vue';
import getPropertyDetails from '@/composables/fetchProperties/getPropertyDetail';

export default {
    name :"PropertyDetailsView",
    components:{PropertyDetail},
    props: ['id'],
    setup(props){
        const {property,load} = getPropertyDetails(props.id)
        load()


    return {property}
    },
}
</script>

<style>

</style>