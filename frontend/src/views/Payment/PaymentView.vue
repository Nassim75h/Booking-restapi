<template>
  <div class="payment-view">
    <div class="payment-container">
      <h1>Complete Your Booking</h1>
      
      <div class="payment-steps">
        <div class="step completed">
          <span class="step-label">Booking Details</span>
        </div>
        <div class="step active">
          <span class="step-label">Payment</span>
        </div>
      </div>

      <div class="card-information">
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>
        <h2>Card Information</h2>
        <form @submit.prevent="handlePayment">
          <div class="form-group">
            <label>Card Number</label>
            <div class="card-input-wrapper">
              <input 
                type="text" 
                v-model="cardNumber"
                placeholder="4648 4846 5846 8546"
                maxlength="19"
                @input="formatCardNumber"
              >
              <div class="card-icons">
                <i class="fab fa-cc-visa"></i>
                <i class="fab fa-cc-mastercard"></i>
                <i class="fas fa-money-check"></i>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Expiry Date</label>
              <input 
                type="text" 
                v-model="expiryDate"
                placeholder="02/27"
                maxlength="5"
                @input="formatExpiryDate"
              >
            </div>
            <div class="form-group">
              <label>CVV</label>
              <input 
                type="text" 
                v-model="cvv"
                placeholder="465"
                maxlength="3"
              >
            </div>
          </div>

          <div class="form-group">
            <label>Cardholder Name</label>
            <input 
              type="text" 
              v-model="cardholderName"
              placeholder="MOHAMED BRAHIMI"
            >
          </div>

          <div class="payment-summary">
            <div class="summary-row">
              <span>Total Amount:</span>
              <span class="amount">DZ{{ amount }}</span>
            </div>
          </div>

          <button 
            type="submit" 
            class="pay-button"
            :disabled="!isFormValid || loading"
          >
            <span v-if="loading">
              <i class="fas fa-spinner fa-spin"></i>
              Processing...
            </span>
            <span v-else>
              Pay DZ{{ amount }}
            </span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import useAxios from '@/composables/fetchCredentials/axios'

const route = useRoute()
const router = useRouter()
const { post } = useAxios()

// Payment form data
const cardNumber = ref('')
const expiryDate = ref('')
const cvv = ref('')
const cardholderName = ref('')
const loading = ref(false)
const error = ref(null)

// Get booking details from route query
const amount = ref(route.query.amount || 0)
const propertyId = ref(route.query.propertyId)
const checkIn = ref(route.query.checkIn)
const checkOut = ref(route.query.checkOut)
const guests = ref(route.query.guests)
const paymentMethod = ref(route.query.paymentMethod)

// Validate required fields
if (!propertyId.value || !checkIn.value || !checkOut.value || !guests.value || !amount.value) {
  error.value = 'Missing required booking information'
  console.error('Missing fields:', { propertyId: propertyId.value, checkIn: checkIn.value, checkOut: checkOut.value, guests: guests.value, amount: amount.value })
}

// Format card number with spaces
const formatCardNumber = (e) => {
  let value = e.target.value.replace(/\s/g, '')
  value = value.replace(/\D/g, '')
  value = value.replace(/(\d{4})/g, '$1 ').trim()
  cardNumber.value = value
}

// Format expiry date with slash
const formatExpiryDate = (e) => {
  let value = e.target.value.replace(/\D/g, '')
  if (value.length >= 2) {
    value = value.slice(0, 2) + '/' + value.slice(2)
  }
  expiryDate.value = value
}

// Validate form
const isFormValid = computed(() => {
  return cardNumber.value.replace(/\s/g, '').length === 16 &&
         expiryDate.value.length === 5 &&
         cvv.value.length === 3 &&
         cardholderName.value.length > 0
})

// Handle payment submission
const handlePayment = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  error.value = null

  try {
    // Simulate payment processing
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // For now, just redirect to success page
    await router.push({
      name: 'payment-success',
      query: { 
        amount: amount.value,
        transactionId: 'TXN-' + Math.random().toString(36).substr(2, 9).toUpperCase()
      }
    })
  } catch (err) {
    console.error('Payment error:', err)
    console.error('Response data:', err.response?.data)
    error.value = err.response?.data?.detail || 
                  err.response?.data?.message ||
                  err.message || 
                  'Payment failed. Please try again.'
    loading.value = false
  }
}
</script>

<style scoped>
.payment-view {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  padding: 20px;
}

.payment-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 500px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.payment-steps {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.step {
  display: flex;
  align-items: center;
  margin: 0 15px;
  color: #6c757d;
}

.step.completed {
  color: #28a745;
}

.step.active {
  color: #007bff;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #495057;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
}

.card-input-wrapper {
  position: relative;
}

.card-icons {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 10px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.payment-summary {
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
}

.amount {
  font-weight: bold;
  color: #007bff;
}

.pay-button {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pay-button:hover:not(:disabled) {
  background: #0056b3;
}

.pay-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
