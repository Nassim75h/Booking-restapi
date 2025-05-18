<template>
  <button class="back-button" @click="goToHome">
    <span class="back-icon">←</span> Back to Home
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToHome = () => {
  router.push('/home')
}
</script>

<style scoped>
.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #5B9BD5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #4A8BC2;
}

.back-icon {
  font-size: 18px;
}
</style>
