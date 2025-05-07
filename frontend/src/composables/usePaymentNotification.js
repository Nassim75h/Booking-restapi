import { ref } from 'vue';

const notifications = ref([]);

export default function usePaymentNotification() {
  const showNotification = (message, status = 'error', duration = 5000) => {
    const id = Date.now();
    const notification = {
      id,
      message,
      status,
      show: true
    };
    
    notifications.value.push(notification);
    
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }
    
    return id;
  };

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  };

  const showPaymentError = (message = 'Payment failed. Please try again.') => {
    return showNotification(message, 'error');
  };

  const showPaymentSuccess = (message = 'Payment successful!') => {
    return showNotification(message, 'success');
  };

  const showPaymentWarning = (message) => {
    return showNotification(message, 'warning');
  };

  return {
    notifications,
    showNotification,
    removeNotification,
    showPaymentError,
    showPaymentSuccess,
    showPaymentWarning
  };
}
