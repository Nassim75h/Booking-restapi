import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default function useCheckAvailability() {
  const loading = ref(false)
  const error = ref(null)
  const { get } = useAxios()

  const checkPropertyAvailability = async (propertyId, checkInDate, checkOutDate) => {
    if (!propertyId || !checkInDate || !checkOutDate) {
      error.value = 'Please provide all required dates'
      return {
        success: false,
        available: false,
        message: 'Please provide all required dates'
      }
    }

    loading.value = true
    error.value = null

    try {
      // Format dates to YYYY-MM-DD
      const formattedCheckIn = new Date(checkInDate).toISOString().split('T')[0]
      const formattedCheckOut = new Date(checkOutDate).toISOString().split('T')[0]

      // Use URLSearchParams to properly format query parameters
      const params = new URLSearchParams({
        check_in_date: formattedCheckIn,
        check_out_date: formattedCheckOut
      })

      const response = await get(
        `booking/properties/${propertyId}/check-availability/?${params.toString()}`
      )

      return {
        success: true,
        available: response.data.available,
        message: response.data.available 
          ? 'Property is available for these dates!'
          : response.data.message || 'Property is not available for these dates'
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.response?.data?.detail || 'Failed to check availability'
      error.value = errorMessage
      return {
        success: false,
        available: false,
        message: errorMessage
      }
    } finally {
      loading.value = false
    }
  }

  const calculatePrice = (property, checkInDate, checkOutDate) => {
    if (!property || !checkInDate || !checkOutDate) return 0

    const start = new Date(checkInDate)
    const end = new Date(checkOutDate)
    const nights = Math.ceil((end - start) / (1000 * 60 * 60 * 24))

    return nights * property.price_per_night
  }

  return {
    loading,
    error,
    checkPropertyAvailability,
    calculatePrice
  }
}
