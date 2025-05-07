<template>
  <button 
    class="wishlist-button" 
    :class="{ 'in-wishlist': isInWishlist }"
    @click="toggleWishlist"
    :disabled="loading"
  >
    <i class="fas" :class="isInWishlist ? 'fa-heart' : 'fa-heart-o'"></i>
    {{ isInWishlist ? 'Saved' : 'Save' }}
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useWishlist from '@/composables/wishlist/useWishlist'

const props = defineProps({
  propertyId: {
    type: [Number, String],
    required: true
  },
  initialInWishlist: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['wishlistUpdated'])

const { addToWishlist, removeFromWishlist, checkWishlistStatus, loading } = useWishlist()
const isInWishlist = ref(props.initialInWishlist)

onMounted(async () => {
  try {
    const status = await checkWishlistStatus(props.propertyId)
    isInWishlist.value = status.is_in_wishlist
  } catch (error) {
    console.error('Failed to check wishlist status:', error)
  }
})

const toggleWishlist = async () => {
  try {
    if (isInWishlist.value) {
      await removeFromWishlist(props.propertyId)
      isInWishlist.value = false
    } else {
      await addToWishlist(props.propertyId)
      isInWishlist.value = true
    }
    emit('wishlistUpdated', isInWishlist.value)
  } catch (error) {
    console.error('Failed to update wishlist:', error)
  }
}
</script>

<style scoped>
.wishlist-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  color: #4a5568;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.wishlist-button:hover:not(:disabled) {
  border-color: #4A90E2;
  color: #4A90E2;
}

.wishlist-button.in-wishlist {
  background: #EBF5FF;
  border-color: #4A90E2;
  color: #4A90E2;
}

.wishlist-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.wishlist-button i {
  font-size: 1.25rem;
}
</style>
