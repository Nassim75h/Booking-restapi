<template>
  <div class="notification-container">
    <div class="notification-icon">
      <img src="@/assets/images/calendar-logo.svg" alt="Calendar Icon" class="calendar-icon">
    </div>
    <TransitionGroup name="notification">
      <PaymentNotification
        v-for="notification in notifications"
        :key="notification.id"
        :message="notification.message"
        :status="notification.status"
        @close="removeNotification(notification.id)"
      />
    </TransitionGroup>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import PaymentNotification from './PaymentNotification.vue';
import usePaymentNotification from '@/composables/usePaymentNotification';

export default defineComponent({
  name: 'NotificationContainer',
  components: {
    PaymentNotification
  },
  setup() {
    const { notifications, removeNotification } = usePaymentNotification();

    return {
      notifications,
      removeNotification
    };
  }
});
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
}

.notification-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
