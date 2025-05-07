<template>
  <div class="payment-success-container">
    <div class="payment-success-card">
      <div class="success-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      
      <h1>Payment Successful!</h1>
      <p class="success-message">Your payment has been processed successfully.</p>

      <div class="payment-details">
        <h2>Payment Details</h2>
        <div class="details-grid">
          <div class="detail-row">
            <span class="label">Status:</span>
            <span class="value success">Completed</span>
          </div>
          <div class="detail-row">
            <span class="label">Transaction ID:</span>
            <span class="value">{{ transactionId }}</span>
          </div>
          <div v-if="booking" class="booking-details">
            <div class="detail-row">
              <span class="label">Property:</span>
              <span class="value">{{ booking.property?.title }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Check-in:</span>
              <span class="value">{{ formatDate(booking.check_in_date) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Check-out:</span>
              <span class="value">{{ formatDate(booking.check_out_date) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Total Amount:</span>
              <span class="value">${{ formatPrice(booking.total_price) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <router-link to="/" class="btn home-btn">
          <i class="fas fa-home"></i> Return to Home
        </router-link>
        <router-link to="/my-bookings" class="btn bookings-btn">
          <i class="fas fa-list"></i> View My Bookings
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import usePaymentNotification from '@/composables/usePaymentNotification';
import useBooking from '@/composables/fetchBookings/useBooking';

export default defineComponent({
  name: 'PaymentSuccess',
  props: {
    transactionId: {
      type: String,
      default: ''
    },
    bookingId: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const { showPaymentSuccess } = usePaymentNotification();
    const { getBookingById } = useBooking();
    const booking = ref(null);

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    const formatPrice = (price) => {
      return Number(price).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    onMounted(async () => {
      showPaymentSuccess('Payment processed successfully!');
      
      if (props.bookingId) {
        try {
          booking.value = await getBookingById(props.bookingId);
        } catch (error) {
          console.error('Failed to fetch booking details:', error);
        }
      }
    });

    return {
      booking,
      formatDate,
      formatPrice,
      transactionId: props.transactionId || route.query.transaction_id || 'TXN-W12IOGGQ4'
    };
  }
});
</script>

<style scoped>
.payment-success-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #f8fafc;
}

.payment-success-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.success-icon {
  font-size: 48px;
  color: #22c55e;
  margin-bottom: 20px;
}

h1 {
  color: #1e293b;
  margin-bottom: 12px;
  font-size: 28px;
}

.success-message {
  color: #64748b;
  margin-bottom: 32px;
}

.payment-details {
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 32px;
  text-align: left;
}

.payment-details h2 {
  font-size: 20px;
  color: #334155;
  margin-bottom: 16px;
}

.details-grid {
  display: grid;
  gap: 12px;
}

.booking-details {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.label {
  color: #64748b;
  font-size: 14px;
}

.value {
  font-weight: 500;
  color: #334155;
}

.value.success {
  color: #22c55e;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.home-btn {
  background-color: #e2e8f0;
  color: #475569;
}

.bookings-btn {
  background-color: #3b82f6;
  color: white;
}

.home-btn:hover {
  background-color: #cbd5e1;
}

.bookings-btn:hover {
  background-color: #2563eb;
}

@media (max-width: 640px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
