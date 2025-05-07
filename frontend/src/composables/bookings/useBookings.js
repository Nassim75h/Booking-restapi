import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default function useBookings() {
  const { get, post, patch, del } = useAxios()
  const bookings = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Fetch all bookings for the current user
  const fetchUserBookings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await get('booking/bookings/')
      bookings.value = response.data
      return response.data
    } catch (err) {
      console.error('Error fetching bookings:', err)
      error.value = err.response?.data?.message || 
                    err.response?.data?.detail ||
                    'Failed to fetch bookings'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Fetch a specific booking by ID
  const fetchBookingById = async (bookingId) => {
    loading.value = true
    error.value = null

    try {
      const response = await get(`booking/bookings/${bookingId}/`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 
                    err.response?.data?.detail ||
                    'Failed to fetch booking'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Update booking status
  const updateBookingStatus = async (bookingId, status) => {
    loading.value = true
    error.value = null

    try {
      const response = await patch(`booking/bookings/${bookingId}/`, {
        status: status
      })
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 
                    err.response?.data?.detail ||
                    'Failed to update booking status'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Cancel booking
  const cancelBooking = async (bookingId) => {
    loading.value = true
    error.value = null

    try {
      const response = await del(`booking/bookings/${bookingId}/`)
      // Remove the cancelled booking from the local list
      bookings.value = bookings.value.filter(booking => booking.id !== bookingId)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 
                    err.response?.data?.detail ||
                    'Failed to cancel booking'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  // Calculate total nights between two dates
  const calculateNights = (checkIn, checkOut) => {
    const start = new Date(checkIn)
    const end = new Date(checkOut)
    const diffTime = Math.abs(end - start)
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  }

  return {
    bookings,
    loading,
    error,
    fetchUserBookings,
    fetchBookingById,
    updateBookingStatus,
    cancelBooking,
    formatDate,
    calculateNights
  }
}
