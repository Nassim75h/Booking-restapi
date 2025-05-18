<template>
  <div class="payment-modal-overlay" v-if="show">
    <div class="payment-modal" :class="{ 'is-loading': loading }">
      <div class="modal-content">
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>
        <div class="payment-header">
          <h1>Complete Your Booking</h1>
        </div>

        <div class="payment-steps">
          <div class="step completed">
            <div class="step-icon">
              <i class="fas fa-check"></i>
            </div>
            <span>Booking Details</span>
          </div>
          <div class="step active">
            <div class="step-icon">
              <i class="fas fa-credit-card"></i>
            </div>
            <span>Payment</span>
          </div>
        </div>

        <div class="payment-form">
          <h2>Card Information</h2>
          <form @submit.prevent="handlePayment">
            <div class="form-group">
              <label>Card Number</label>
              <div class="card-input-wrapper">
                <input 
                  type="text" 
                  v-model="cardNumber"
                  placeholder="1234 5678 9012 3456"
                  maxlength="19"
                  @input="formatCardNumber"
                >
                <div class="card-icons">
                  <img src="/images/visa.svg" alt="Visa">
                  <img src="/images/mastercard.svg" alt="Mastercard">
                  <img src="/images/ccp.svg" alt="CCP">
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Expiry Date</label>
                <input 
                  type="text" 
                  v-model="expiryDate"
                  placeholder="MM/YY"
                  maxlength="5"
                  @input="formatExpiryDate"
                >
              </div>
              <div class="form-group">
                <label>CVV</label>
                <input 
                  type="text" 
                  v-model="cvv"
                  placeholder="123"
                  maxlength="3"
                >
              </div>
            </div>

            <div class="form-group">
              <label>Cardholder Name</label>
              <input 
                type="text" 
                v-model="cardholderName"
                placeholder="John Doe"
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
              {{ loading ? 'Processing...' : `Pay DZ${amount}` }}
            </button>
          </form>
        </div>
      </div>
      <div v-if="loading" class="loading-overlay">
        <i class="fas fa-spinner fa-spin"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  amount: {
    type: Number,
    required: true
  },
  booking: {
    type: Object,
    required: true
  },
  processPayment: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['payment-completed', 'payment-failed'])

const cardNumber = ref('')
const expiryDate = ref('')
const cvv = ref('')
const cardholderName = ref('')
const loading = ref(false)
const error = ref(null)

const formatCardNumber = (e) => {
  let value = e.target.value.replace(/\s/g, '').replace(/\D/g, '')
  let formattedValue = ''
  for (let i = 0; i < value.length; i++) {
    if (i > 0 && i % 4 === 0) {
      formattedValue += ' '
    }
    formattedValue += value[i]
  }
  cardNumber.value = formattedValue
}

const formatExpiryDate = (e) => {
  let value = e.target.value.replace(/\D/g, '')
  if (value.length > 2) {
    value = value.slice(0, 2) + '/' + value.slice(2)
  }
  expiryDate.value = value
}

const isFormValid = computed(() => {
  return (
    cardNumber.value.replace(/\s/g, '').length === 16 &&
    expiryDate.value.length === 5 &&
    cvv.value.length === 3 &&
    cardholderName.value.length > 0
  )
})

const validateCard = () => {
  // Card number validation (Luhn algorithm)
  const cardDigits = cardNumber.value.replace(/\s/g, '')
  if (!/^\d{16}$/.test(cardDigits)) {
    throw new Error('Invalid card number')
  }

  // Expiry date validation
  const [month, year] = expiryDate.value.split('/')
  const now = new Date()
  const expiry = new Date(2000 + parseInt(year), parseInt(month) - 1)
  if (expiry < now) {
    throw new Error('Card has expired')
  }

  // CVV validation
  if (!/^\d{3}$/.test(cvv.value)) {
    throw new Error('Invalid CVV')
  }

  // Cardholder name validation
  if (cardholderName.value.trim().length < 3) {
    throw new Error('Invalid cardholder name')
  }
}

const handlePayment = async () => {
  if (!isFormValid.value) return
  error.value = ''
  loading.value = true

  try {
    validateCard()
    await props.processPayment({
      cardNumber: cardNumber.value,
      expiryDate: expiryDate.value,
      cvv: cvv.value,
      cardholderName: cardholderName.value
    })
    emit('payment-completed', props.booking)
  } catch (err) {
    error.value = err.message || 'Payment failed'
    emit('payment-failed', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.payment-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.payment-modal {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.payment-header {
  text-align: center;
  margin-bottom: 2rem;
}

.payment-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.payment-steps {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.step {
  display: flex;
  align-items: center;
  margin: 0 1rem;
  color: #94a3b8;
}

.step.completed {
  color: #22c55e;
}

.step.active {
  color: #4A90E2;
}

.step-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: currentColor;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
}

.payment-form h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #1e293b;
}

input:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.card-input-wrapper {
  position: relative;
}

.card-icons {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 0.5rem;
}

.card-icons img {
  height: 24px;
}

.payment-summary {
  background-color: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 2rem 0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #1e293b;
  font-weight: 500;
}

.amount {
  font-size: 1.25rem;
  color: #4A90E2;
}

.pay-button {
  width: 100%;
  padding: 1rem;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.pay-button:hover:not(:disabled) {
  background-color: #357ABD;
}

.pay-button:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .payment-modal {
    margin: 1rem;
    padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
