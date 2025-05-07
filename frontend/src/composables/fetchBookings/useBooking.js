import { ref } from 'vue';
import useAxios from '../fetchCredentials/axios';

export default function useBooking() {
  const { get, post } = useAxios();
  const loading = ref(false);
  const error = ref(null);

  const getBookingById = async (bookingId) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await get(`booking/bookings/${bookingId}/`);
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to fetch booking details';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getMyBookings = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await get('booking/bookings/');
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to fetch bookings';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateBookingStatus = async (bookingId, status) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await post(`booking/bookings/${bookingId}/update-status/`, { status });
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to update booking status';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    getBookingById,
    getMyBookings,
    updateBookingStatus
  };
}
