import useAxios from "@/composables/fetchCredentials/axios";
import { ref } from "vue";

const uploadPropertyImage = () => {
  const uploadResponse = ref(null);
  const isUploading = ref(false);
  const { post, get } = useAxios();
  
  // Upload image function
  const upload = async (propertyId, imageFile, isOwnedProperty = false) => {
    isUploading.value = true;
    
    try {
      // Create FormData to send the file
      const formData = new FormData();
      formData.append('image', imageFile);
      
      // Determine the correct endpoint based on whether it's an owned property or not
      const endpoint = isOwnedProperty 
        ? `/booking/owned-property/${propertyId}/images/` 
        : `/booking/properties/${propertyId}/images/`;
      
      const response = await post(
        endpoint,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      uploadResponse.value = response.data;
      console.log('Image uploaded successfully:', response.data);
      
      return { success: true, data: response.data };
    } catch (err) {
      console.error('Error uploading image:', err.response?.data || err.message);
      return { success: false, error: err.response?.data || 'Unknown error' };
    } finally {
      isUploading.value = false;
    }
  };
  
  // Fetch image function
  const fetchImages = async (propertyId, isOwnedProperty = false) => {
    try {
      // Use the correct endpoint based on property type
      const endpoint = isOwnedProperty 
        ? `/booking/owned-property/${propertyId}/images/` 
        : `/booking/properties/${propertyId}/images/`;
      
      const response = await get(endpoint);
      
      console.log('Images fetched successfully:', response.data);
      return { success: true, data: response.data };
    } catch (err) {
      console.error('Error fetching images:', err.response?.data || err.message);
      return { success: false, error: err.response?.data || 'Unknown error' };
    }
  };
  
  return { upload, fetchImages, uploadResponse, isUploading };
};

export default uploadPropertyImage;