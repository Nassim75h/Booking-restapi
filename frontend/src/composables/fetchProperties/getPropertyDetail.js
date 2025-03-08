import useAxios from "@/composables/fetchCredentials/axios";
import { ref } from "vue"
const getPropertyDetails =(propertyId) =>{
    const property = ref(null)
    const {get} = useAxios()
    const load = async () => {
        try {
            const response = await get("booking/properties/"+propertyId)
            
            property.value =response.data
        }catch(err){
            console.log(err)
        }
    }
    return {property,load}
}

export default getPropertyDetails