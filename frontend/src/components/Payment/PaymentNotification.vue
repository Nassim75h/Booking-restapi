<template>
  <div v-if="show" :class="['payment-notification', status]">
    <div class="notification-content">
      <i :class="['fas', iconClass]"></i>
      <span>{{ message }}</span>
    </div>
    <button class="close-button" @click="close">
      <i class="fas fa-times"></i>
    </button>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';

export default {
  name: 'PaymentNotification',
  props: {
    status: {
      type: String,
      default: 'error',
      validator: (value) => ['error', 'success', 'warning'].includes(value)
    },
    message: {
      type: String,
      required: true
    },
    autoClose: {
      type: Boolean,
      default: true
    },
    duration: {
      type: Number,
      default: 5000
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const show = ref(true);

    const close = () => {
      show.value = false;
      emit('close');
    };

    const iconClass = computed(() => ({
      'error': 'fa-exclamation-circle',
      'success': 'fa-check-circle',
      'warning': 'fa-exclamation-triangle'
    }[props.status]));

    onMounted(() => {
      if (props.autoClose) {
        setTimeout(close, props.duration);
      }
    });

    return {
      show,
      close,
      iconClass
    };
  }
}
</script>

<style scoped>
.payment-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  min-width: 300px;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

.notification-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.payment-notification.error {
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  color: #991b1b;
}

.payment-notification.success {
  background-color: #dcfce7;
  border: 1px solid #22c55e;
  color: #166534;
}

.payment-notification.warning {
  background-color: #fef3c7;
  border: 1px solid #f59e0b;
  color: #92400e;
}

.close-button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 4px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.close-button:hover {
  opacity: 1;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}
</style>
