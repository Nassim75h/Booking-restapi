<template>
  <div class="my-bookings">
    <div class="container">
      <h1>My Bookings</h1>
      
      <div v-if="loading" class="loading-overlay">
        <div class="loading-content">
          <i class="fas fa-spinner fa-spin"></i>
          <span>Loading your bookings...</span>
        </div>
      </div>

      <div v-else-if="error" class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        {{ error }}
      </div>

      <div v-else-if="bookings.length === 0" class="no-bookings">
        <i class="fas fa-calendar-times"></i>
        <p>You don't have any bookings yet.</p>
        <router-link to="/" class="btn-primary">Browse Properties</router-link>
      </div>

      <div v-else class="bookings-list">
        <div v-for="booking in bookings" :key="booking.id" class="booking-card">
          <div class="booking-image">
            <img :src="booking.property.image_url" :alt="booking.property.title">
          </div>
          
          <div class="booking-details">
            <h2>{{ booking.property.title }}</h2>
            
            <div class="booking-info">
              <div class="info-row">
                <i class="fas fa-calendar"></i>
                <span>Check-in: {{ formatDate(booking.check_in_date) }}</span>
              </div>
              <div class="info-row">
                <i class="fas fa-calendar"></i>
                <span>Check-out: {{ formatDate(booking.check_out_date) }}</span>
              </div>
              <div class="info-row">
                <i class="fas fa-moon"></i>
                <span>{{ calculateNights(booking.check_in_date, booking.check_out_date) }} nights</span>
              </div>
              <div class="info-row">
                <i class="fas fa-users"></i>
                <span>{{ booking.guests }} guests</span>
              </div>
            </div>

            <div class="booking-status" :class="booking.status.toLowerCase()">
              <span>{{ booking.status }}</span>
            </div>

            <div class="booking-price">
              <span class="total-label">Total:</span>
              <span class="price">€{{ booking.total_price }}</span>
            </div>

            <div class="booking-actions">
              <button 
                v-if="booking.status === 'PENDING'"
                @click="cancelBooking(booking.id)"
                class="btn-danger"
              >
                Cancel Booking
              </button>
              <router-link 
                :to="{ name: 'property-details', params: { id: booking.property.id }}"
                class="btn-secondary"
              >
                View Property
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import useBookings from '@/composables/bookings/useBookings'

const { 
  bookings,
  loading,
  error,
  fetchUserBookings,
  cancelBooking,
  formatDate,
  calculateNights
} = useBookings()

onMounted(async () => {
  try {
    loading.value = true
    await fetchUserBookings()
  } catch (err) {
    console.error('Failed to fetch bookings:', err)
    error.value = err.message || 'Failed to fetch bookings'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.my-bookings {
  padding: 2rem;
  background-color: #f8fafc;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #1e293b;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #64748b;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.loading-content i {
  font-size: 2rem;
  color: #0ea5e9;
}

.no-bookings {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.loading i, .no-bookings i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.booking-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
  display: flex;
  overflow: hidden;
}

.booking-image {
  width: 300px;
  height: 200px;
}

.booking-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.booking-details {
  flex: 1;
  padding: 1.5rem;
}

.booking-details h2 {
  color: #1e293b;
  margin-bottom: 1rem;
}

.booking-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
}

.booking-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.booking-status.confirmed {
  background-color: #dcfce7;
  color: #16a34a;
}

.booking-status.pending {
  background-color: #fef9c3;
  color: #ca8a04;
}

.booking-status.cancelled {
  background-color: #fee2e2;
  color: #dc2626;
}

.booking-price {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.total-label {
  color: #64748b;
  margin-right: 0.5rem;
}

.price {
  font-weight: 600;
  color: #0ea5e9;
}

.booking-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary, .btn-secondary, .btn-danger {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #0ea5e9;
  color: white;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #475569;
}

.btn-danger {
  background-color: #dc2626;
  color: white;
}

.btn-primary:hover {
  background-color: #0284c7;
}

.btn-secondary:hover {
  background-color: #cbd5e1;
}

.btn-danger:hover {
  background-color: #b91c1c;
}

@media (max-width: 768px) {
  .booking-card {
    flex-direction: column;
  }

  .booking-image {
    width: 100%;
  }

  .booking-info {
    grid-template-columns: 1fr;
  }
}
</style>
