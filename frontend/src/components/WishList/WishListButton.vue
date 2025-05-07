<template>
  <div class="wishlist-button">
    <button 
      @click="toggleWishlist"
      :class="{ 'in-wishlist': isInWishlist }"
      :disabled="loading || isLoading"
    >
      <i 
        :class="[
          'fas', 
          isInWishlist ? 'fa-heart' : 'fa-heart',
          { 'fa-spin': loading || isLoading }
        ]"
      ></i>
      {{ isInWishlist ? 'In Wishlist' : 'Add to Wishlist' }}
    </button>

    <div v-if="errorMessage" class="error-tooltip">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { ref, onBeforeUnmount } from 'vue'
import useWishlist from '@/composables/wishlist/useWishlist'

export default {
  name: 'WishListButton',
  props: {
    propertyId: {
      type: [Number, String],
      required: true
    },
    initialInWishlist: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const { addToWishlist, removeFromWishlist } = useWishlist()
    const isInWishlist = ref(props.initialInWishlist)
    const errorMessage = ref(null)
    const isLoading = ref(false)
    let errorTimeout = null

    const clearError = () => {
      if (errorTimeout) {
        clearTimeout(errorTimeout)
        errorTimeout = null
      }
      errorMessage.value = null
    }

    const setError = (message) => {
      clearError()
      errorMessage.value = message
      errorTimeout = setTimeout(() => {
        if (errorMessage.value) {
          errorMessage.value = null
        }
      }, 3000)
    }

    const toggleWishlist = async () => {
      if (isLoading.value) return

      clearError()
      isLoading.value = true

      try {
        if (isInWishlist.value) {
          await removeFromWishlist(props.propertyId)
          isInWishlist.value = false
          emit('wishlist-updated', false)
        } else {
          await addToWishlist(props.propertyId)
          isInWishlist.value = true
          emit('wishlist-updated', true)
        }
      } catch (err) {
        console.error('Wishlist operation failed:', err)
        setError(err.message || 'Failed to update wishlist')
      } finally {
        isLoading.value = false
      }
    }

    onBeforeUnmount(() => {
      clearError()
    })

    return {
      isInWishlist,
      errorMessage,
      isLoading,
      toggleWishlist
    }
  }
}
</script>

<style scoped>
.wishlist-button {
  position: relative;
}

button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #4A90E2;
  border-radius: 9999px;
  background-color: white;
  color: #4A90E2;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

button:hover:not(:disabled) {
  background-color: #4A90E2;
  color: white;
}

button.in-wishlist {
  background-color: #4A90E2;
  color: white;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ef4444;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  white-space: nowrap;
  margin-bottom: 0.5rem;
  z-index: 10;
}

.error-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: #ef4444 transparent transparent transparent;
}
</style>
