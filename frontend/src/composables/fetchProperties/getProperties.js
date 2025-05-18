import {ref} from 'vue';
import useAxios from "@/composables/fetchCredentials/axios";

const getProperties = () => {
  const { get } = useAxios()
  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)

  const load = async () => {
    loading.value = true
    error.value = null
    data.value = null

    try {
      // Add timeout to prevent infinite loading
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout')), 15000)
      );
      
      console.log('Making request to: booking/properties/');
      const fetchPromise = get('booking/properties/');
      const response = await Promise.race([fetchPromise, timeoutPromise]);
      
      console.log('API Response:', response)
      
      if (!response || !response.data) {
        throw new Error('No response received')
      }

      // Normalize the data structure
      const properties = Array.isArray(response.data) ? response.data :
                     response.data.results ? response.data.results :
                     [response.data];
                  
      // Process each property
      data.value = properties.map(property => {
        // Process images if they exist
        if (property.images && property.images.length > 0) {
          property.images = property.images.map(img => {
            if (typeof img === 'string') {
              return img.startsWith('http') ? img : `http://localhost:8000${img}`;
            }
            return img && img.image ? 
              (img.image.startsWith('http') ? img.image : `http://localhost:8000${img.image}`) :
              null;
          }).filter(img => img); // Remove any null images
        }
        
        return {
          ...property,
          // Ensure all text fields are strings for searching
          title: String(property.title || ''),
          description: String(property.description || ''),
          city: String(property.city || ''),
          address: String(property.address || '')
        };
      });

      // Validate data structure
      if (!data.value.every(property => property.id && property.title)) {
        console.warn('Some properties may be missing required fields');
      }
    } catch (err) {
      console.error('Property loading error:', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response,
        status: err.response?.status,
        data: err.response?.data
      });
      
      error.value = err.message === 'Request timeout' ? 'Request timed out. Please try again.' :
                   err.response?.status === 404 ? 'Property listing not found. Please check if you are logged in.' :
                   err.response?.status === 403 ? 'You do not have permission to view properties' :
                   !navigator.onLine ? 'Please check your internet connection' :
                   'Failed to load properties. Please try again.'
    } finally {
      loading.value = false
    }
  }

  return { data, error, loading, load }
}

export default getProperties