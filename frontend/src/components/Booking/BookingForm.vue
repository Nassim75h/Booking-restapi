<template>
  <div class="booking-form">
    <!-- Back to Home button -->
    <div class="back-button-container">
      <button class="back-button" @click="goToHome">
        <span class="back-icon">←</span> Back to Home
      </button>
    </div>
    
    <h2>Book your stay</h2>
    
    <!-- Date Selection -->
    <div class="date-inputs">
      <div class="input-group">
        <label>
          <i class="fas fa-calendar-check"></i>
          Check-in
        </label>
        <input 
          type="date" 
          v-model="bookingData.check_in_date"
          :min="today"
          required
          @change="checkAvailabilityOnDateChange"
        >
      </div>
      
      <div class="input-group">
        <label>
          <i class="fas fa-calendar-times"></i>
          Check-out
        </label>
        <input 
          type="date" 
          v-model="bookingData.check_out_date"
          :min="bookingData.check_in_date || today"
          required
          @change="checkAvailabilityOnDateChange"
        >
      </div>
    </div>

    <!-- Form Status -->
    <div v-if="error" class="error-message" role="alert">
      <i class="fas fa-exclamation-circle"></i>
      {{ error }}
    </div>
    <div v-if="loading" class="loading-message">
      <i class="fas fa-circle-notch fa-spin"></i>
      Checking availability...
    </div>

    <!-- Guest Count -->
    <div class="guest-counter">
      <label>Number of guests</label>
      <div class="counter-controls">
        <button 
          type="button" 
          @click="decrementGuests"
          :disabled="bookingData.guests <= 1"
          class="counter-btn"
        >
          <i class="fas fa-minus"></i>
        </button>
        <span class="guest-count">
          {{ bookingData.guests }} {{ bookingData.guests === 1 ? 'Guest' : 'Guests' }}
        </span>
        <button 
          type="button" 
          @click="incrementGuests"
          :disabled="bookingData.guests >= property.max_guests"
          class="counter-btn"
        >
          <i class="fas fa-plus"></i>
        </button>
      </div>
    </div>

    <!-- Payment Method Selection -->
    <div class="payment-method">
      <label>Payment method</label>
      <div class="payment-options">
        <button 
          type="button"
          :class="['payment-option', { active: bookingData.payment_method === 'card' }]"
          @click="selectPaymentMethod('card')"
        >
          <i class="fas fa-credit-card"></i>
          Visa/Mastercard
        </button>
        <button 
          type="button"
          :class="['payment-option', { active: bookingData.payment_method === 'ccp' }]"
          @click="selectPaymentMethod('ccp')"
        >
          <i class="fas fa-money-check"></i>
          CCP Algerian Card
        </button>
      </div>
    </div>

    <!-- Price Summary -->
    <div class="price-summary" v-if="totalNights > 0">
      <div class="price-row">
        <span>DZ{{ property.price_per_night }} × {{ totalNights }} nights</span>
        <span>DZ{{ totalPrice }}</span>
      </div>
      <div class="total-price">
        <span>Total</span>
        <span>DZ{{ totalPrice }}</span>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Submit Button -->
    <button 
      class="submit-button" 
      @click="handleSubmit"
      :disabled="!isValidBooking || loading"
    >
      <span v-if="!loading">Book Now - DZ{{ totalPrice }}</span>
      <span v-else>
        <i class="fas fa-spinner fa-spin"></i>
        Processing...
      </span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import useCreateBooking from '@/composables/bookings/createBooking'
import useCheckAvailability from '@/composables/fetchProperties/checkAvailability'

const props = defineProps({
  property: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['booking-completed'])
const router = useRouter()

// Composables
const { createBooking, loading: bookingLoading, error: bookingError } = useCreateBooking()
const { checkAvailability: checkPropertyAvailability, loading: availabilityLoading, error: availabilityError } = useCheckAvailability()

// State
const loading = ref(false)
const error = ref(null)
const showPaymentModal = ref(false)
const availabilityStatus = ref(null)
const isAvailable = ref(false)

// Form data
const bookingData = ref({
  property_id: props.property.id,
  check_in_date: '',
  check_out_date: '',
  guests: 1,
  payment_method: 'card'
})

// Computed
const today = computed(() => {
  const date = new Date()
  return date.toISOString().split('T')[0]
})

const totalNights = computed(() => {
  if (!bookingData.value.check_in_date || !bookingData.value.check_out_date) {
    return 0
  }
  const start = new Date(bookingData.value.check_in_date)
  const end = new Date(bookingData.value.check_out_date)
  return Math.ceil((end - start) / (1000 * 60 * 60 * 24))
})

const totalPrice = computed(() => {
  if (!totalNights.value || !props.property.price_per_night) return '0.00'
  const price = props.property.price_per_night * totalNights.value
  return price.toFixed(2)
})

const isValidBooking = computed(() => {
  return (
    bookingData.value.check_in_date &&
    bookingData.value.check_out_date &&
    bookingData.value.guests > 0 &&
    bookingData.value.guests <= props.property.max_guests &&
    bookingData.value.payment_method &&
    totalNights.value > 0 &&
    !error.value // Only check for errors, not availability
  )
})

// Methods
const checkAvailabilityOnDateChange = async () => {
  error.value = null
  
  if (!validateDates()) return

  try {
    availabilityStatus.value = null
    isAvailable.value = false

    const result = await checkPropertyAvailability(
      props.property.id,
      bookingData.value.check_in_date,
      bookingData.value.check_out_date
    )

    availabilityStatus.value = result
    isAvailable.value = result.available

    // Clear any previous error if available
    if (result.available) {
      error.value = null
    }
  } catch (err) {
    console.error('Availability check error:', err)
    error.value = err.message || 'Failed to check availability'
    availabilityStatus.value = {
      available: false,
      message: 'Property is not available for these dates'
    }
  }
}

const validateDates = () => {
  if (!bookingData.value.check_in_date || !bookingData.value.check_out_date) {
    error.value = 'Please select both check-in and check-out dates'
    return false
  }

  const checkIn = new Date(bookingData.value.check_in_date)
  const checkOut = new Date(bookingData.value.check_out_date)
  const today = new Date()

  // Reset time part to compare only dates
  today.setHours(0, 0, 0, 0)
  checkIn.setHours(0, 0, 0, 0)
  checkOut.setHours(0, 0, 0, 0)

  if (checkIn < today) {
    error.value = 'Check-in date cannot be in the past'
    return false
  }

  if (checkOut <= checkIn) {
    error.value = 'Check-out date must be after check-in date'
    return false
  }

  const maxStayDays = 30 // Maximum stay duration
  const daysDiff = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24))
  if (daysDiff > maxStayDays) {
    error.value = `Maximum stay duration is ${maxStayDays} days`
    return false
  }

  return true
}

const incrementGuests = () => {
  if (bookingData.value.guests < props.property.max_guests) {
    bookingData.value.guests++
  }
}

const decrementGuests = () => {
  if (bookingData.value.guests > 1) {
    bookingData.value.guests--
  }
}

const selectPaymentMethod = (method) => {
  bookingData.value.payment_method = method
}

const handleSubmit = async () => {
  error.value = null
  loading.value = true

  try {
    if (!validateDates()) {
      loading.value = false
      return
    }

    if (!bookingData.value.payment_method) {
      error.value = 'Please select a payment method'
      loading.value = false
      return
    }

    if (bookingData.value.guests < 1 || bookingData.value.guests > props.property.max_guests) {
      error.value = `Number of guests must be between 1 and ${props.property.max_guests}`
      loading.value = false
      return
    }

    // Check availability one final time before proceeding
    const availability = await checkPropertyAvailability(
      props.property.id,
      bookingData.value.check_in_date,
      bookingData.value.check_out_date
    )

    if (!availability.available) {
      error.value = availability.message || 'Selected dates are not available'
      loading.value = false
      return
    }

    // Format total price to 2 decimal places
    const formattedPrice = parseFloat(totalPrice.value).toFixed(2)

    // Proceed to payment directly
    router.push({
      name: 'payment',
      query: {
        propertyId: props.property.id,
        checkIn: bookingData.value.check_in_date,
        checkOut: bookingData.value.check_out_date,
        guests: bookingData.value.guests,
        paymentMethod: bookingData.value.payment_method,
        amount: formattedPrice
      }
    })


  } catch (err) {
    console.error('Booking error:', err)
    error.value = err.response?.data?.detail || 
                  err.response?.data?.message || 
                  err.message || 
                  'Failed to create booking'
  } finally {
    loading.value = false
  }
}

const handlePaymentCompleted = (paymentData) => {
  showPaymentModal.value = false
  emit('booking-completed', paymentData.booking)
  router.push('/bookings')
}

const handlePaymentFailed = (err) => {
  showPaymentModal.value = false
  error.value = err.message || 'Payment failed'
}

// Navigation function
const goToHome = () => {
  router.push('/home')  // Navigate to root/home page
}

// Watch for date changes
watch(
  () => [bookingData.value.check_in_date, bookingData.value.check_out_date],
  async () => {
    // Clear previous error
    error.value = null

    // Only check availability if both dates are set
    if (bookingData.value.check_in_date && bookingData.value.check_out_date) {
      await checkAvailabilityOnDateChange()
    }
    if (validateDates()) {
      checkAvailabilityOnDateChange()
    }
  }
)

// Add watch to update property_id if property changes
watch(() => props.property, (newProperty) => {
  if (newProperty?.id) {
    bookingData.value.property_id = newProperty.id
  }
}, { immediate: true })
</script>

<style scoped>
.booking-form {
  padding: 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
  color: #1a1a1a;
}

.date-inputs {
  background: transparent;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.input-group {
  background: transparent;
  margin-bottom: 1rem;
}

label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #4a5568;
}

label i {
  color: #4A90E2;
}

input[type="date"] {
  background: transparent;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(229, 231, 235, 0.5);
  padding: 0.75rem;
  border-radius: 8px;
  width: 100%;
  color: inherit;
}

input::placeholder {
  color: rgba(0, 0, 0, 0.5);
}

.guest-counter {
  margin-bottom: 1.5rem;
}

.counter-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.counter-btn {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(229, 231, 235, 0.5);
  border-radius: 50%;
  background: transparent;
  color: #4A90E2;
  cursor: pointer;
  transition: all 0.2s;
}

.counter-btn:disabled {
  color: #a0aec0;
  border-color: rgba(229, 231, 235, 0.5);
  cursor: not-allowed;
}

.counter-btn:not(:disabled):hover {
  background: #4A90E2;
  color: white;
  border-color: #4A90E2;
}

.guest-count {
  min-width: 100px;
  text-align: center;
  font-weight: 500;
}

.payment-method {
  margin-bottom: 1.5rem;
}

.payment-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 0.5rem;
}

.payment-option {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  border: 2px solid rgba(229, 231, 235, 0.5);
  border-radius: 0.5rem;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.payment-option.active {
  border-color: #4A90E2;
  background: rgba(74, 144, 226, 0.1);
}

.payment-option i {
  font-size: 1.5rem;
  color: #4A90E2;
}

.price-summary {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid rgba(229, 231, 235, 0.5);
  border-radius: 0.5rem;
}

.price-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #4a5568;
}

.total-price {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
  font-weight: 600;
  color: #1a1a1a;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  padding: 0.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.availability-status {
  margin-bottom: 1rem;
  padding: 0.75rem;
  border-radius: 0.375rem;
  text-align: center;
}

.availability-status.available {
  background: rgba(220, 252, 231, 0.1);
  color: #15803D;
}

.availability-status.unavailable {
  background: rgba(239, 68, 68, 0.1);
  color: #DC2626;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 0.5rem;
  background: #4A90E2;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-button:hover:not(:disabled) {
  background: #357ABD;
}

.submit-button:disabled {
  background: #A0AEC0;
  cursor: not-allowed;
}

.back-button-container {
  margin-bottom: 20px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #5B9BD5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #4A8BC2;
}

.back-icon {
  font-size: 18px;
}

@media (max-width: 640px) {
  .date-inputs {
    grid-template-columns: 1fr;
  }

  .payment-options {
    grid-template-columns: 1fr;
  }
}
</style>
