<template>
    <div class="property-details">
      <div class="image-container">
        <img
          v-if="propertyImage && !imageError"
          :src="propertyImage"
          class="property-image"
          @error="handleImageError"
          alt="Property Image"
        />
        <div v-else class="image-placeholder">
          No image available
        </div>
      </div>
      <router-link :to="{ name: 'property-details', params: {id: property.id}}">
        <h2>Name: {{ property.title }}</h2>
      </router-link>
      <h2>Price: {{ property.price_per_night }}</h2>
      <h2>Owner: {{ property.host.username }}</h2>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import uploadPropertyImage from '@/composables/fetchProperties/uploadPropertyImage';
  
  export default {
    name: "SinglePost",
    components: {},
    props: ['property'],
    setup(props) {
      const propertyImage = ref(null);
      const imageError = ref(false);
      const { fetchImages } = uploadPropertyImage(); // Changed from fetchImage to fetchImages
      
      const loadImage = async () => {
        if (props.property && props.property.id) {
          try {
            // Determine if this is an owned property based on your logic
            // You might need to adjust this check based on your data structure
            const isOwnedProperty = props.property.is_owned || false;
            
            const response = await fetchImages(props.property.id, isOwnedProperty);
            console.log("Image API response:", response);
            
            if (response.success && response.data && response.data.length > 0) {
              // Handle different possible response formats
              const imageData = response.data[0];
              
              // Try to get the image URL from different possible properties
              if (typeof imageData === 'string') {
                propertyImage.value = imageData;
              } else if (imageData.image) {
                propertyImage.value = imageData.image;
              } else if (imageData.url) {
                propertyImage.value = imageData.url;
              } else {
                console.error("Unexpected image data format:", imageData);
                imageError.value = true;
              }
              
              // Add API base URL if it's a relative path
              if (propertyImage.value && !propertyImage.value.startsWith('http')) {
                // Check if it starts with a slash
                if (!propertyImage.value.startsWith('/')) {
                  propertyImage.value = '/' + propertyImage.value;
                }
                
                // Get base URL from your API configuration
                const apiBase = import.meta.env.VITE_API_BASE_URL || '';
                if (apiBase && !propertyImage.value.includes(apiBase)) {
                  propertyImage.value = apiBase + propertyImage.value;
                }
              }
              
              console.log("Final image URL:", propertyImage.value);
            } else {
              console.warn("No images found for property:", props.property.id);
              imageError.value = true;
            }
          } catch (error) {
            console.error("Failed to load property image:", error);
            imageError.value = true;
          }
        }
      };
      
      const handleImageError = (event) => {
        console.error("Image failed to load:", event);
        console.error("Image URL that failed:", propertyImage.value);
        imageError.value = true;
      };
      
      // Load image when component is mounted
      onMounted(loadImage);
      
      return {
        propertyImage,
        imageError,
        handleImageError
      };
    }
  }
  </script>
  
  <style scoped>
  .property-details {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    transition: transform 0.2s;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .property-details:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .image-container {
    margin-bottom: 15px;
    text-align: center;
  }
  
  .property-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .image-placeholder {
    background-color: #f3f4f6;
    border: 2px dashed #bbb;
    border-radius: 8px;
    padding: 80px 0;
    color: #999;
    font-weight: bold;
  }
  </style>