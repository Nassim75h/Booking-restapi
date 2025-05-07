<template>
  <div class="booking-success">
    <div class="success-card">
      <div class="success-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      <h1>Booking Successful!</h1>
      <p>Thank you for your booking. Your payment has been processed successfully.</p>
      <div class="booking-details">
        <h2>Booking Details</h2>
        <div class="detail-row">
          <span>Booking ID:</span>
          <span>{{ bookingId }}</span>
        </div>
        <div class="detail-row">
          <span>Amount Paid:</span>
          <span>€{{ amount }}</span>
        </div>
      </div>
      <div class="actions">
        <router-link to="/" class="btn-primary">Return to Home</router-link>
        <router-link to="/manage" class="btn-secondary">View My Bookings</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookingSuccessView',
  computed: {
    bookingId() {
      return this.$route.params.bookingId
    },
    amount() {
      return this.$route.params.amount
    }
  },
  mounted() {
    if (!this.bookingId) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.booking-success {
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

.booking-details {
  background-color: #f8fafc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  text-align: left;
}

.booking-details h2 {
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
