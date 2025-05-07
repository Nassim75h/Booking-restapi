import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default function useWishlist() {
  const loading = ref(false)
  const error = ref(null)
  const wishlistItems = ref([])
  const isInWishlist = ref(false)
  const { get, post, del } = useAxios()

  const checkWishlistStatus = async (propertyId) => {
    loading.value = true
    try {
      const response = await get(`booking/properties/${propertyId}/check_wishlist_status/`)
      isInWishlist.value = response.data.is_in_wishlist
      return response.data
    } catch (err) {
      console.error('Failed to check wishlist status:', err)
      return { is_in_wishlist: false }
    } finally {
      loading.value = false
    }
  }

  const addToWishlist = async (propertyId) => {
    if (!propertyId) {
      throw new Error('Property ID is required')
    }

    loading.value = true
    error.value = null

    try {
      // First check if already in wishlist
      const status = await checkWishlistStatus(propertyId)
      if (status.is_in_wishlist) {
        error.value = 'Property is already in your wishlist'
        throw new Error('Property is already in your wishlist')
      }

      const response = await post(
        `booking/properties/${propertyId}/add_to_wish_list/`,
        {
          property_id: propertyId,
          confirmed: false // Adding this flag to indicate initial wishlist addition
        }
      )
      await getWishlist() // Refresh the wishlist after adding
      isInWishlist.value = true
      return response.data
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || err.message || 'Failed to add to wishlist'
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
      await getWishlist() // Refresh the wishlist after removing
      isInWishlist.value = false
      return response.data
    } catch (err) {
      console.error('Remove from wishlist error:', err.response?.data || err)
      const message = err.response?.data?.detail || err.response?.data?.message || err.response?.data || 'Failed to remove from wishlist'
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
        `booking/properties/${propertyId}/confirm_wishlist/${waitlistEntryId}/`,
        {
          property_id: propertyId,
          waitlist_entry_id: waitlistEntryId,
          confirmed: true
        }
      )
      await getWishlist() // Refresh the wishlist after confirming
      return response.data
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || 'Failed to confirm wishlist'
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
      const message = err.response?.data?.detail || err.response?.data?.message || 'Failed to load wishlist'
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
    checkWishlistStatus,
    wishlistItems,
    isInWishlist,
    loading,
    error
  }
}
