import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'
import { loadStripe } from '@stripe/stripe-js'

// Get the Stripe key from environment variables
const getStripeKey = () => {
  const key = import.meta.env.VITE_STRIPE_PUBLIC_KEY
  if (!key) {
    throw new Error('Stripe public key is not configured. Please check your .env file.')
  }
  return key
}

export default function useCreateBooking() {
  const { get, post } = useAxios()
  const loading = ref(false)
  const error = ref(null)
  const bookingData = ref(null)
  const availability = ref(null)

  const checkAvailability = async (propertyId, checkInDate, checkOutDate) => {
    loading.value = true
    error.value = null

    try {
      // Format dates to YYYY-MM-DD
      const formattedCheckIn = new Date(checkInDate).toISOString().split('T')[0]
      const formattedCheckOut = new Date(checkOutDate).toISOString().split('T')[0]

      // Validate dates
      if (new Date(formattedCheckIn) >= new Date(formattedCheckOut)) {
        throw new Error('Check-out date must be after check-in date')
      }

      // Use URLSearchParams to properly format query parameters
      const params = new URLSearchParams({
        check_in_date: formattedCheckIn,
        check_out_date: formattedCheckOut
      })

      const response = await get(
        `booking/properties/${propertyId}/check-availability/?${params.toString()}`
      )

      availability.value = response.data
      return response.data
    } catch (err) {
      console.error('Availability check error:', err)
      error.value = err.response?.data?.message || err.response?.data?.detail || err.message || 'Failed to check availability'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const createNewBooking = async (bookingDetails) => {
    loading.value = true
    error.value = null
    bookingData.value = null

    try {
      // Enhanced validation
      const requiredFields = {
        property_id: 'Property ID',
        check_in_date: 'Check-in date',
        check_out_date: 'Check-out date',
        guests: 'Number of guests',
        total_price: 'Total price',
        payment_method: 'Payment method'
      }

      // Check all required fields
      for (const [field, label] of Object.entries(requiredFields)) {
        if (!bookingDetails[field]) {
          throw new Error(`${label} is required`)
        }
      }

      // Validate guests number
      if (bookingDetails.guests < 1) {
        throw new Error('Number of guests must be at least 1')
      }

      // Validate total price
      if (bookingDetails.total_price <= 0) {
        throw new Error('Total price must be greater than 0')
      }

      // Validate payment method
      if (!['card', 'ccp'].includes(bookingDetails.payment_method)) {
        throw new Error('Invalid payment method. Must be either "card" or "ccp"')
      }

      // Format dates to YYYY-MM-DD
      const formattedCheckIn = new Date(bookingDetails.check_in_date).toISOString().split('T')[0]
      const formattedCheckOut = new Date(bookingDetails.check_out_date).toISOString().split('T')[0]

      // Validate dates
      if (new Date(formattedCheckIn) >= new Date(formattedCheckOut)) {
        throw new Error('Check-out date must be after check-in date')
      }

      // Prepare the payload with proper data types
      const payload = {
        property: parseInt(bookingDetails.property_id, 10),
        check_in_date: formattedCheckIn,
        check_out_date: formattedCheckOut,
        number_of_guests: parseInt(bookingDetails.guests, 10),
        total_price: parseFloat(bookingDetails.total_price),
        payment_method: bookingDetails.payment_method
      }

      console.log('Sending booking payload:', payload)

      // First check availability again
      const availabilityCheck = await get(
        `booking/properties/${payload.property}/check-availability/`,
        {
          params: {
            check_in_date: payload.check_in_date,
            check_out_date: payload.check_out_date
          }
        }
      )

      if (!availabilityCheck.data.available) {
        throw new Error(availabilityCheck.data.message || 'Property is not available for these dates')
      }

      // Make the booking request
      const response = await post(
        `booking/properties/${payload.property}/book/`,
        payload
      )

      console.log('Booking response:', response.data)
      bookingData.value = response.data

      // Handle payment method specific logic
      if (bookingDetails.payment_method === 'card') {
        // For card payments, we need to create a Stripe session
        const stripeResponse = await post('booking/create-stripe-session/', {
          booking_id: response.data.id,
          amount: payload.total_price
        })

        if (!stripeResponse.data?.sessionId) {
          throw new Error('No Stripe session ID received from server')
        }

        const stripeKey = getStripeKey()
        const stripe = await loadStripe(stripeKey)
        if (!stripe) {
          throw new Error('Failed to initialize Stripe')
        }

        return {
          requiresPayment: true,
          booking: response.data,
          async processPayment() {
            try {
              const result = await stripe.redirectToCheckout({
                sessionId: stripeResponse.data.sessionId
              })
              if (result.error) {
                throw new Error(result.error.message)
              }
            } catch (err) {
              console.error('Stripe payment error:', err)
              throw new Error('Payment processing failed: ' + (err.message || 'Unknown error'))
            }
          }
        }
      } else if (bookingDetails.payment_method === 'ccp') {
        // For CCP payments, return the booking info for manual processing
        if (!response.data.ccp_payment_url) {
          throw new Error('No CCP payment URL received from server')
        }
        return {
          requiresPayment: true,
          booking: response.data,
          async processPayment() {
            window.location.href = response.data.ccp_payment_url
          }
        }
      } else {
        throw new Error('Invalid payment method')
      }

      return {
        requiresPayment: false,
        booking: response.data
      }
    } catch (err) {
      console.error('Booking error:', err)
      if (err.response?.data) {
        console.error('Server response:', err.response.data)
      }
      
      let errorMessage = 'Failed to create booking'
      
      if (err.response?.data) {
        if (typeof err.response.data === 'string') {
          errorMessage = err.response.data
        } else if (err.response.data.detail) {
          errorMessage = err.response.data.detail
        } else if (err.response.data.message) {
          errorMessage = err.response.data.message
        } else if (typeof err.response.data === 'object') {
          const errors = Object.entries(err.response.data)
            .map(([key, value]) => `${key}: ${value}`)
            .join(', ')
          errorMessage = `Validation errors: ${errors}`
        }
      } else if (err.message) {
        errorMessage = err.message
      }
      
      error.value = errorMessage
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    createNewBooking,
    checkAvailability,
    loading,
    error,
    bookingData,
    availability
  }
}
