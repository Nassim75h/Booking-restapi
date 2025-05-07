import { ref } from 'vue'
import useAxios from "@/composables/fetchCredentials/axios";

export default function useCheckAvailability() {
  const { get } = useAxios();
  const loading = ref(false);
  const error = ref(null);

  const checkAvailability = async (propertyId, checkInDate, checkOutDate) => {
    try {
      loading.value = true;
      error.value = null;
      
      if (!propertyId || !checkInDate || !checkOutDate) {
        throw new Error('Missing required parameters for availability check');
      }

      const url = `booking/properties/${propertyId}/check-availability/`;
      
      const response = await get(url, {
        params: {
          check_in_date: checkInDate,
          check_out_date: checkOutDate
        }
      });

      if (!response.data) {
        throw new Error('No response from availability check');
      }

      // Check for specific unavailability reasons
      if (!response.data.available) {
        let message = response.data.message || 'Property is not available';
        if (response.data.reason) {
          switch (response.data.reason) {
            case 'booked':
              message = 'Property is already booked for these dates';
              break;
            case 'maintenance':
              message = 'Property is under maintenance during these dates';
              break;
            case 'blocked':
              message = 'Property is not available for booking during these dates';
              break;
            default:
              message = response.data.message || 'Property is not available for these dates';
          }
        }
        return { available: false, message };
      }

      return {
        available: true,
        message: response.data.message || 'Property is available for these dates'
      };
    } catch (err) {
      console.error('Availability check error:', err);
      error.value = err.response?.data?.detail || 
                    err.response?.data?.message || 
                    err.message || 
                    'Failed to check availability';
      
      return {
        available: false,
        message: error.value
      };
    } finally {
      loading.value = false;
    }
  };

  return {
    checkAvailability,
    loading,
    error
  };
}
