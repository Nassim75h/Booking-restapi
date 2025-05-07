<template>
  <div class="property-detail">
    <div v-if="property" class="details">
      <!-- Property Image Section -->
      <div class="property-image-section">
        <div class="main-image-container">
          <img 
            v-if="property.images && property.images.length > 0" 
            :src="getImageUrl(property.images[0])" 
            :alt="property.title"
            class="main-image"
            @error="handleImageError($event, 0)"
          >
          <div v-else class="no-image">
            <i class="fas fa-home"></i>
            <span>No image available</span>
          </div>
        </div>
        <div class="property-header">
          <h1>{{ property.title }}</h1>
          <p class="location">
            <i class="fas fa-map-marker-alt"></i>
            {{ property.address }}
          </p>
        </div>
      </div>

      <div class="content-wrapper">
        <div class="main-content">
          <!-- Property Info Card -->
          <div class="info-card">
            <div class="host-info">
              <div class="host-avatar">
                <i class="fas fa-user"></i>
              </div>
            </div>

            <div class="description">
              <h3>About this place</h3>
              <p>{{ property.description }}</p>
            </div>

            <div class="features">
              <h3>What this place offers</h3>
              <ul>
                <li><i class="fas fa-bed"></i> {{ property.beds }} beds</li>
                <li><i class="fas fa-bath"></i> {{ property.bathrooms }} bathrooms</li>
                <li><i class="fas fa-users"></i> Up to {{ property.max_guests }} guests</li>
              </ul>
            </div>

            <div v-if="isOwner" class="property-actions">
              <button @click="deleteProperty" class="delete-button">
                <i class="fas fa-trash"></i>
                Delete Property
              </button>
            </div>
          </div>

          <!-- Booking Card -->
          <div v-if="!isOwner" class="booking-sidebar">
            <div class="booking-card">
              <h3>Book this property</h3>
              <div class="price">
                <span class="amount">${{ property.price_per_night }}</span>
                <span class="period">per night</span>
              </div>
              <button @click="showBookingForm = true" class="book-button">
                <i class="fas fa-calendar-check"></i>
                Book Now
              </button>
              <button @click="showConversationForm = true" class="contact-host-button">
                <i class="fas fa-comment"></i>
                Contact Host
              </button>
            </div>
          </div>

          <!-- Conversation Modal -->
          <div v-if="showConversationForm" class="conversation-modal">
            <div class="modal-overlay" @click="showConversationForm = false"></div>
            <div class="modal-content">
              <button class="close-button" @click="showConversationForm = false">
                <i class="fas fa-times"></i>
              </button>
              <ConversationForm 
                :property-id="property.id"
                @message-sent="handleMessageSent"
              />
            </div>
          </div>

          <!-- Booking Modal -->
          <div v-if="showBookingForm" class="booking-modal">
            <div class="modal-overlay" @click="showBookingForm = false"></div>
            <div class="modal-content">
              <button class="close-button" @click="showBookingForm = false">
                <i class="fas fa-times"></i>
              </button>
              <BookingForm 
                :property="property" 
                @booking-completed="handleBookingCompleted"
              />
            </div>
          </div>

          <div class="property-actions">
            <WishListButton 
              :property-id="property.id" 
              :initial-in-wishlist="property.in_wishlist"
              @wishlist-updated="handleWishlistUpdate"
            />
          </div>
        </div>

        <!-- Upload section for property owner -->
        <div v-if="isOwner" class="upload-section">
          <h3>Add Photos</h3>
          <input
            type="file"
            @change="handleImageUpload"
            accept="image/*"
            :disabled="isUploading"
            ref="fileInput"
            style="display: none"
          >
          <button
            class="upload-button"
            @click="$refs.fileInput.click()"
            :disabled="isUploading"
          >
            <i class="fas fa-cloud-upload-alt"></i>
            {{ isUploading ? 'Uploading...' : 'Upload Image' }}
          </button>
          <p v-if="uploadMessage" :class="{ 'error-message': uploadError }">
            {{ uploadMessage }}
          </p>
        </div>
      </div>
    </div>
    <div v-else class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading property details...
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import uploadPropertyImage from '@/composables/fetchProperties/uploadPropertyImage';
import { getPropertyDetails } from '@/composables/fetchProperties/getPropertyDetail';
import BookingForm from '@/components/Booking/BookingForm.vue';
import useAxios from '@/composables/fetchCredentials/axios';
import WishListButton from '@/components/WishList/WishListButton.vue';
import ConversationForm from '@/components/Conversation/ConversationForm.vue';

export default {
  name: "PropertyDetail",
  components: {
    BookingForm,
    WishListButton,
    ConversationForm
  },
  props: {
    property: {
      type: Object,
      required: true
    },
    isOwner: {
      type: Boolean,
      default: false
    }
  },
  emits: ['property-updated'],

  setup(props, { emit }) {
    const { get, post } = useAxios();
    const selectedFile = ref(null);
    const uploadMessage = ref('');
    const uploadError = ref(false);
    const showBookingForm = ref(false);
    const showConversationForm = ref(false);
    const failedImages = ref({});
    const isUploading = ref(false);

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
        // Get base URL from axios instance but remove /api/v0/ since media URLs don't use it
        const baseURL = get.defaults.baseURL || '';
        const baseURLWithoutAPI = baseURL.replace('/api/v0/', '');
        
        // Remove leading slash if present to avoid double slashes
        const path = imageUrl.startsWith('/') ? imageUrl.substring(1) : imageUrl;
        imageUrl = `${baseURLWithoutAPI}${path}`;
      }
      
      return imageUrl;
    };

    // Handle image loading errors
    const handleImageError = (event, index) => {
      console.error(`Failed to load image at index ${index}`, event);
      failedImages.value[index] = true;
      event.target.src = '/placeholder-image.jpg';
    };

    // Handle file selection
    const handleImageUpload = async (event) => {
      if (!event.target.files.length) return;
      
      const file = event.target.files[0];
      uploadMessage.value = '';
      uploadError.value = false;

      try {
        const result = await post('/properties/' + props.property.id + '/images', file);
        if (result.success) {
          uploadMessage.value = 'Image uploaded successfully!';
          emit('property-updated');
        } else {
          uploadMessage.value = result.error || 'Failed to upload image';
          uploadError.value = true;
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        uploadMessage.value = error.message || 'Error uploading image';
        uploadError.value = true;
      }
    };

    const handleBookingCompleted = () => {
      showBookingForm.value = false;
    };

    const handleMessageSent = () => {
      showConversationForm.value = false;
    };

    const handleWishlistUpdate = (isInWishlist) => {
      // Update local property state to reflect wishlist change
      if (props.property) {
        emit('property-updated', {
          ...props.property,
          in_wishlist: isInWishlist
        });
      }
    };

    return {
      getImageUrl,
      handleImageError,
      handleImageUpload,
      handleBookingCompleted,
      handleMessageSent,
      handleWishlistUpdate,
      uploadMessage,
      uploadError,
      showBookingForm,
      showConversationForm,
      failedImages,
      isUploading
    };
  }
};
</script>

<style scoped>
.property-detail {
  background: transparent;
  padding: 2rem;
  border-radius: 10px;
  max-width: 1200px;
  margin: 0 auto;
}

.property-image-section {
  margin-bottom: 2rem;
}

.main-image-container {
  width: 100%;
  height: 300px;
  border-radius: 1rem;
  overflow: hidden;
  background-color: #f1f5f9;
  margin-bottom: 1rem;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background-color: #f8fafc;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.no-image i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.property-header {
  padding: 1rem;
}

.property-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
}

.location i {
  color: #4A90E2;
}

.content-wrapper {
  max-width: 1200px;
  margin: -2rem auto 0;
  padding: 0 2rem;
  position: relative;
  z-index: 2;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.info-card, .booking-card {
  background: transparent;
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.host-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.host-avatar {
  width: 4rem;
  height: 4rem;
  background-color: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.host-avatar i {
  font-size: 1.5rem;
  color: #64748b;
}

.description h3,
.features h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

.description p {
  color: #64748b;
  line-height: 1.6;
}

.features ul {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 1rem;
}

.features li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #64748b;
}

.features li i {
  color: #4A90E2;
  width: 1.5rem;
}

.booking-sidebar {
  position: sticky;
  top: 2rem;
}

.booking-card {
  background-color: transparent;
  padding: 1.5rem;
}

.price {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.period {
  color: #64748b;
}

.book-button {
  width: 100%;
  padding: 0.875rem;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.book-button:hover {
  background-color: #357ABD;
}

.contact-host-button {
  width: 100%;
  padding: 0.875rem;
  background-color: #10B981;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s;
  margin-top: 1rem;
}

.contact-host-button:hover {
  background-color: #059669;
}

.upload-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: transparent;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.upload-button {
  background-color: #4A90E2;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.upload-button:hover:not(:disabled) {
  background-color: #357ABD;
}

.upload-button:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  margin-top: 0.5rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 1rem;
  color: #64748b;
}

.loading i {
  font-size: 2rem;
  color: #4A90E2;
}

.conversation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 500px;
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  z-index: 1;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748B;
}

.close-button:hover {
  color: #1E293B;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .content-wrapper {
    padding: 0 1rem;
    margin-top: 0;
  }

  .booking-sidebar {
    position: static;
  }
}
</style>