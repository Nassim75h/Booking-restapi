import {ref }from 'vue';
import useAxios from "@/composables/fetchCredentials/axios";
const getProperties =() => {
  
  const {get} = useAxios()
    const data = ref([])
    const load = async  () =>{
      try{
        const response = await get('booking/properties/')
        data.value =  response.data
      }catch (err){
        
        console.log(err.message)
      }
    }
    return {data,load}
}

export default getProperties