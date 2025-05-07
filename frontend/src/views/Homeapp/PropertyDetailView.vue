<template>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading property details...
    </div>
    <PropertyDetail 
      v-else
      :property="property" 
      :isOwner="isOwner"
      @property-updated="handlePropertyUpdated"
    />
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import PropertyDetail from '@/components/Property/PropertyDetail.vue';
  import getPropertyDetails from '@/composables/fetchProperties/getPropertyDetail';
  import uploadPropertyImage from '@/composables/fetchProperties/uploadPropertyImage';
  import useAxios from '@/composables/fetchCredentials/axios';
  
  export default {
    name: "PropertyDetailsView",
    components: {
      PropertyDetail
    },
    props: ['id'],
    setup(props) {
      const loading = ref(true);
      const error = ref(null);
      const property = ref(null);
      const currentUser = ref(null);
      
      // Import image upload functionality for potential use
      const { fetchImages } = uploadPropertyImage();
      
      // Initialize axios client with auth handling
      const { fetchUserDetails, userCredentials, get } = useAxios();
      
      // Load property details
      const load = async () => {
        loading.value = true;
        error.value = null;
        
        try {
          const response = await get(`booking/properties/${props.id}/`);
          property.value = response.data;
        } catch (err) {
          console.error('Error loading property:', err);
          error.value = err.response?.data?.message || 'Failed to load property details';
          property.value = null;
        } finally {
          loading.value = false;
        }
      };
      
      // Fetch current user data
      const fetchCurrentUser = async () => {
        try {
          const userData = await fetchUserDetails();
          currentUser.value = userData;
        } catch (err) {
          console.error('Error fetching current user:', err);
          currentUser.value = null;
        }
      };
      
      // Determine if current user is the owner of this property
      const isOwner = computed(() => {
        if (!property.value?.host || !currentUser.value?.id) return false;
        return (
          property.value.host.id === currentUser.value.id || 
          currentUser.value.isAdmin === true
        );
      });
      
      // Handle property updates from the child component
      const handlePropertyUpdated = async (updatedProperty) => {
        console.log('Property updated:', updatedProperty);
        
        // Refresh property data to ensure we have the latest
        await load();
        
        // You could also update images specifically if needed
        if (props.id) {
          const result = await fetchImages(props.id, isOwner.value);
          if (result.success && result.data && property.value) {
            property.value.images = result.data;
          }
        }
      };
      
      // Load property data and current user when component mounts
      onMounted(async () => {
        await fetchCurrentUser();
        await load();
      });
      
      return {
        property,
        isOwner,
        handlePropertyUpdated
      };
    }
  }
  </script>
  
  <style scoped>
  .loading,
  .error-message {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    text-align: center;
    padding: 2rem;
    border-radius: 8px;
    margin: 2rem auto;
    max-width: 600px;
  }

  .loading {
    background-color: #f8fafc;
    color: #64748b;
  }

  .loading i {
    margin-right: 0.5rem;
    font-size: 1.25rem;
  }

  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    border: 1px solid #fee2e2;
  }
  </style>