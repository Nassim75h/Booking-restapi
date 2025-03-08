import { ref } from "vue"
import useAxios from '../fetchCredentials/axios'
const getOwnedProperties = () => {
    const properties = ref([])
    const {get} = useAxios()
    
    const load = async () => {
        try {
            const response = await  get('booking/owned-property/')
            properties.value = response.data
        }catch (err){
            console.log(err.message);
            
        }
    }
    return {properties,load}
}
export default getOwnedProperties