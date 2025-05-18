<template>
  <div class="property-details" v-if="mounted">
    <div class="image-container">
      <div v-if="imageLoading" class="loading-spinner">
        Loading...
      </div>
      <img
        v-else-if="propertyImage && !imageError"
        :src="propertyImage"
        class="property-image"
        @error="handleImageError"
        alt="Property Image"
      />
      <div v-else class="image-placeholder">
        No image available
      </div>
    </div>
    <router-link 
      :to="{ name: 'property-details', params: {id: property.id}}" 
      class="property-link"
      v-if="property && property.id"
    >
      <h2 class="property-title">{{ property.title }}</h2>
    </router-link>
    <div class="property-info" v-if="property">
      <p class="property-location" v-if="property.city">
        <i class="fas fa-map-marker-alt"></i> {{ property.city }}
      </p>
      <p class="property-price" v-if="property.price_per_night">
        DZ{{ formatPrice(property.price_per_night) }} <span>per night</span>
      </p>
      <p class="property-host" v-if="property.host">
        <i class="fas fa-user"></i> {{ property.host.username }}
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import uploadPropertyImage from '@/composables/fetchProperties/uploadPropertyImage';
import { useRouter } from 'vue-router';

export default {
  name: "SingleProperty",
  components: {},
  props: {
    property: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const router = useRouter();
    const propertyImage = ref(null);
    const imageError = ref(false);
    const imageLoading = ref(true);
    const mounted = ref(false);
    const { fetchImages } = uploadPropertyImage();
    let unmounted = false;

    const loadImage = async () => {
      if (!props.property?.id || unmounted) {
        imageError.value = true;
        imageLoading.value = false;
        return;
      }

      try {
        // Check if property already has images
        if (props.property.images && props.property.images.length > 0) {
          const imageUrl = props.property.images[0];
          propertyImage.value = imageUrl.startsWith('http') ? imageUrl : `http://localhost:8000${imageUrl}`;
          if (!unmounted) imageLoading.value = false;
          return;
        }

        // If no images in property, try to fetch them
        const isOwnedProperty = props.property.is_owned || false;
        const response = await fetchImages(props.property.id, isOwnedProperty);
        
        if (unmounted) return;

        if (!response?.success || !response?.data?.length) {
          throw new Error('No images found');
        }

        const imageData = response.data[0];
        let imageUrl = '';

        // Extract image URL from response
        if (typeof imageData === 'string') {
          imageUrl = imageData;
        } else if (imageData.image || imageData.url) {
          imageUrl = imageData.image || imageData.url;
        } else {
          throw new Error('Invalid image data format');
        }

        // Add base URL if needed
        if (!unmounted) {
          propertyImage.value = imageUrl.startsWith('http') ? imageUrl : `http://localhost:8000${imageUrl}`;
        }
      } catch (error) {
        if (!unmounted) {
          console.error("Failed to load property image:", error);
          imageError.value = true;
        }
      } finally {
        if (!unmounted) {
          imageLoading.value = false;
        }
      }
    };
    
    const handleImageError = (event) => {
      if (!unmounted) {
        console.error("Image failed to load:", event);
        imageError.value = true;
        propertyImage.value = null;
      }
    };

    const formatPrice = (price) => {
      if (!price) return '0.00';
      return Number(price).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    const goBack = () => {
      router.go(-1); // This will go back to the previous page
    };

    onMounted(() => {
      mounted.value = true;
      loadImage();
    });

    onBeforeUnmount(() => {
      unmounted = true;
      mounted.value = false;
    });

    return {
      propertyImage,
      imageError,
      imageLoading,
      mounted,
      handleImageError,
      formatPrice,
      goBack
    };
  }
}
</script>

<style scoped>
.property-details {
  position: relative;
  background: transparent;
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
  position: relative;
  min-height: 200px;
}

.property-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.image-placeholder,
.loading-spinner {
  background-color: #f3f4f6;
  border: 2px dashed #bbb;
  border-radius: 8px;
  padding: 80px 0;
  color: #999;
  font-weight: bold;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  border: none;
  background-color: rgba(243, 244, 246, 0.8);
}

.property-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.property-title {
  font-size: 1.5rem;
  margin: 0.5rem 0;
  color: #2c3e50;
}

.property-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.property-location,
.property-price,
.property-host {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
}

.property-price {
  font-size: 1.25rem;
  color: #2c5282;
  font-weight: bold;
}

.property-price span {
  font-size: 0.875rem;
  color: #718096;
  font-weight: normal;
}
</style>