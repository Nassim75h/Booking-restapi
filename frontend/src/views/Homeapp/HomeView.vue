<template>
  <NavBar />
  <div class="home">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading properties...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        {{ error }}
      </div>
      <button @click="retryLoading" class="retry-button">
        <i class="fas fa-redo"></i>
        Try Again
      </button>
    </div>

    <PropertyList v-else-if="data" :data="data" />
  </div>
</template>

<script>
import { ref ,onMounted } from 'vue';
import getProperties from '@/composables/fetchProperties/getProperties';
import PropertyList from '@/components/Property/PropertyList.vue';
import NavBar from '@/components/Snippets/NavBar.vue';
export default  {
  name: 'HomeView',
  components :{PropertyList,NavBar},
  setup() {
    const { data, error, loading, load } = getProperties()

    onMounted(() => {
      load()
    })

    const retryLoading = () => {
      load()
    }

    return { data, error, loading, retryLoading }
  },

}
</script>
<style scoped>
.home {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4A90E2;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.error-message {
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.retry-button {
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background-color: #357ABD;
}
</style>