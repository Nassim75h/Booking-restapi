<template>
  <div class="payment-success">
    <div class="success-card">
      <div class="success-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      <h1>Payment Successful!</h1>
      <p>Your payment has been processed successfully.</p>
      <div class="payment-details">
        <h2>Payment Details</h2>
        <div class="detail-row">
          <span>Status:</span>
          <span class="success">Completed</span>
        </div>
        <div class="detail-row">
          <span>Transaction ID:</span>
          <span>{{ transactionId }}</span>
        </div>
        <div v-if="bookingDetails" class="booking-summary">
          <h3>Booking Summary</h3>
          <div class="detail-row">
            <span>Check-in:</span>
            <span>{{ new Date(bookingDetails.check_in_date).toLocaleDateString() }}</span>
          </div>
          <div class="detail-row">
            <span>Check-out:</span>
            <span>{{ new Date(bookingDetails.check_out_date).toLocaleDateString() }}</span>
          </div>
          <div class="detail-row">
            <span>Guests:</span>
            <span>{{ bookingDetails.guests }}</span>
          </div>
          <div class="detail-row total">
            <span>Total Amount:</span>
            <span>€{{ bookingDetails.total_price }}</span>
          </div>
        </div>
      </div>
      <div class="actions">
        <router-link to="/" class="btn-primary">
          <i class="fas fa-home"></i>
          Return to Home
        </router-link>
        <router-link to="/my-bookings" class="btn-secondary">
          <i class="fas fa-list"></i>
          View My Bookings
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import useBookings from '@/composables/bookings/useBookings'

export default {
  name: 'PaymentSuccessView',
  setup() {
    const route = useRoute()
    const { fetchBookingById } = useBookings()
    const bookingDetails = ref(null)
    const loading = ref(true)
    const error = ref(null)

    onMounted(() => {
      // Get transaction details from query params
      const amount = route.query.amount
      const transactionId = route.query.transactionId
      
      if (amount) {
        bookingDetails.value = {
          total_price: amount,
          transactionId: transactionId
        }
      }
      loading.value = false
    })

    return {
      bookingDetails,
      loading,
      error,
      transactionId: 'TXN-' + Math.random().toString(36).substr(2, 9).toUpperCase()
    }
  }
}
</script>

<style scoped>
.payment-success {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #f8fafc;
}

.success-card {
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.success-icon {
  font-size: 4rem;
  color: #22c55e;
  margin-bottom: 1.5rem;
}

h1 {
  color: #1e293b;
  font-size: 2rem;
  margin-bottom: 1rem;
}

p {
  color: #64748b;
  margin-bottom: 2rem;
}

.payment-details {
  background-color: #f8fafc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  text-align: left;
}

.payment-details h2 {
  color: #1e293b;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #64748b;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.success {
  color: #22c55e;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #4A90E2;
  color: white;
}

.btn-primary:hover {
  background-color: #357ABD;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #1e293b;
}

.btn-secondary:hover {
  background-color: #cbd5e1;
}

@media (max-width: 640px) {
  .success-card {
    padding: 2rem;
  }

  .actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    text-align: center;
  }
}
</style>
