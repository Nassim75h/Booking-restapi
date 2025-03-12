<template>
  <div>
      <h1>Property Detail</h1>
      <div v-if="property" class="details">
          <h1>{{ property.title }}</h1>
          <p>Price: {{ property.price_per_night }}</p>
          <p>Owner: {{ property.host?.username }}</p>
          <p>Address: {{ property.address }}</p>
          
          <!-- Image gallery with error handling -->
          <div class="image-gallery">
              <div v-if="property.images && property.images.length > 0" class="images-container">
                  <div v-for="(image, index) in property.images.slice(0, 5)" :key="index" class="image-item">
                      <img
                          :src="getImageUrl(image)"
                          :alt="`Property image ${index + 1}`"
                          @error="handleImageError($event, index)"
                          class="property-image"
                      />
                  </div>
              </div>
              <div v-else class="no-images">
                  No images available for this property
              </div>
          </div>
      </div>
      <div v-else class="loading">
          Loading property details...
      </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: "PropertyDetail",
  props: {
      property: {
          type: Object,
          required: true
      }
  },
  setup() {
      const failedImages = ref({});
      
      // Function to get proper image URL
      const getImageUrl = (image) => {
          // Handle different possible image data structures
          let imageUrl = '';
          
          if (typeof image === 'string') {
              imageUrl = image;
          } else if (image && image.image) {
              imageUrl = image.image;
          } else if (image && image.url) {
              imageUrl = image.url;
          } else if (image && typeof image === 'object') {
              // Try to find an image URL in the object
              for (const key in image) {
                  if (typeof image[key] === 'string' && 
                      (image[key].includes('/media/') || 
                      image[key].endsWith('.jpg') || 
                      image[key].endsWith('.jpeg') || 
                      image[key].endsWith('.png') || 
                      image[key].endsWith('.webp'))) {
                      imageUrl = image[key];
                      break;
                  }
              }
          }
          
          // Ensure the URL is absolute if it's a relative path
          if (imageUrl && !imageUrl.startsWith('http') && !imageUrl.startsWith('data:')) {
              // Remove leading slash if present to avoid double slashes
              const path = imageUrl.startsWith('/') ? imageUrl.substring(1) : imageUrl;
              imageUrl = `${window.location.origin}/${path}`;
          }
          
          return imageUrl;
      };
      
      // Handle image loading errors
      const handleImageError = (event, index) => {
          console.error(`Failed to load image at index ${index}`, event);
          failedImages.value[index] = true;
          // Add a placeholder or fallback image
          event.target.src = '/placeholder-image.jpg';
          // Or hide the image
          // event.target.style.display = 'none';
      };
      
      return {
          failedImages,
          getImageUrl,
          handleImageError
      };
  }
}
</script>

<style scoped>
.details {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.image-gallery {
  margin-top: 20px;
}

.images-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.image-item {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.property-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.property-image:hover {
  transform: scale(1.05);
}

.no-images {
  padding: 40px;
  background-color: #f3f4f6;
  border: 2px dashed #ccc;
  border-radius: 8px;
  text-align: center;
  color: #666;
  margin-top: 20px;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #666;
}
</style>