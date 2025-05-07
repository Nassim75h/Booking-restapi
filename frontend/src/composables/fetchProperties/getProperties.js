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
      
      // Make request to the correct endpoint without api/v0 prefix since it's in baseURL
      console.log('Making request to: booking/properties/');
      const fetchPromise = get('booking/properties/');
      const response = await Promise.race([fetchPromise, timeoutPromise]);
      
      // Log response for debugging
      console.log('API Response:', response)
      
      if (!response) {
        throw new Error('No response received')
      }

      if (response.data) {
        // Normalize the data structure
        const properties = Array.isArray(response.data) ? response.data :
                       response.data.results ? response.data.results :
                       [response.data];
                    
        // Process each property to ensure image URLs are absolute
        data.value = properties.map(property => {
          if (property.images && property.images.length > 0) {
            // Convert relative URLs to absolute URLs if needed
            const processedImages = property.images.map(img => {
              if (typeof img === 'string') {
                return img.startsWith('http') ? img : `http://localhost:8000${img}`;
              }
              // Handle case where img is an object with image property
              if (img && img.image) {
                const imageUrl = img.image;
                return imageUrl.startsWith('http') ? imageUrl : `http://localhost:8000${imageUrl}`;
              }
              return img;
            });
            return { ...property, images: processedImages };
          }
          return property;
        });
                    
        // Validate data structure
        if (!data.value.every(property => property.id && property.title)) {
          console.warn('Some properties may be missing required fields');
        }
      } else {
        throw new Error('No data received from server')
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