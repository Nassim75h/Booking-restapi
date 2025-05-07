import { ref } from "vue"
import useAxios from '../fetchCredentials/axios'
const getOwnedProperties = () => {
    const properties = ref([])
    const error = ref(null)
    const loading = ref(false)
    const {get} = useAxios()
    
    const load = async () => {
        loading.value = true
        error.value = null
        properties.value = []
        
        try {
            // Use singular form 'owned-property' to match backend URL pattern
            const response = await get('booking/owned-property/')
            console.log('Owned properties response:', response)
            if (response && response.data) {
                properties.value = Array.isArray(response.data) ? response.data : 
                                 response.data.results ? response.data.results : 
                                 [response.data];
            }
        } catch (err) {
            console.error('Error loading owned properties:', err)
            error.value = err.response?.data?.message || err.message || 'Failed to load your properties'
        } finally {
            loading.value = false
        }
    }
    
    return {properties, error, loading, load}
}
export default getOwnedProperties