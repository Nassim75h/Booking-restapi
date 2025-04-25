import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default function useWishlist() {
  const loading = ref(false)
  const error = ref(null)
  const wishlistItems = ref([])
  const { get, post, del } = useAxios()

  const addToWishlist = async (propertyId) => {
    if (!propertyId) {
      throw new Error('Property ID is required')
    }

    loading.value = true
    error.value = null

    try {
      const response = await post(
        `booking/properties/${propertyId}/add_to_wish_list/`,
        {} // Empty body since we don't need to send any data
      )
      return response.data
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to add to wishlist'
      error.value = message
      throw new Error(message)
    } finally {
      loading.value = false
    }
  }

  const removeFromWishlist = async (propertyId) => {
    if (!propertyId) {
      throw new Error('Property ID is required')
    }

    loading.value = true
    error.value = null

    try {
      const response = await del(
        `booking/properties/${propertyId}/add_to_wish_list/`
      )
      return response.data
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to remove from wishlist'
      error.value = message
      throw new Error(message)
    } finally {
      loading.value = false
    }
  }

  const confirmWishlist = async (propertyId, waitlistEntryId) => {
    if (!propertyId || !waitlistEntryId) {
      throw new Error('Property ID and waitlist entry ID are required')
    }

    loading.value = true
    error.value = null

    try {
      const response = await post(
        `booking/properties/${propertyId}/confirm_wishlist/${waitlistEntryId}/`
      )
      return response.data
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to confirm wishlist'
      error.value = message
      throw new Error(message)
    } finally {
      loading.value = false
    }
  }

  const getWishlist = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await get('booking/wishlist/')
      wishlistItems.value = response.data
      return response.data
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to load wishlist'
      error.value = message
      throw new Error(message)
    } finally {
      loading.value = false
    }
  }

  return {
    addToWishlist,
    removeFromWishlist,
    confirmWishlist,
    getWishlist,
    wishlistItems,
    loading,
    error
  }
}
