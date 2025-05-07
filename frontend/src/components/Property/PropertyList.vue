<template>
  <div class="property-list">
    <div class="header-container">
      <button class="back-button" @click="goBack">
        <i class="fas fa-arrow-left"></i> Back to Home
      </button>
      <h1>Properties</h1>
    </div>
    <div v-if="!loading">
      <div v-if="data && data.length > 0" class="property-grid">
        <transition-group name="property-list" tag="div" class="property-grid-inner">
          <div v-for="property in data" :key="property.id" class="post-list">
            <SingleProperty :property="property" />
          </div>
        </transition-group>
      </div>
      <div v-else class="no-properties">
        <h2>You don't have any listed Properties</h2>
      </div>
    </div>
    <div v-else class="loading">
      Loading properties...
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import SingleProperty from './SingleProperty.vue'
import { useRouter } from 'vue-router'

export default {
  name: "PropertyList",
  components: { SingleProperty },
  props: {
    data: {
      type: Array,
      required: true,
      default: () => []
    },
    error: {
      type: [String, Error],
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const router = useRouter()
    
    const goBack = () => {
      router.push('/')
    }

    return {
      goBack
    }
  }
}
</script>

<style scoped>
.property-list {
  padding: 2vh;
  width: 100%;
  box-sizing: border-box;
}

.property-grid {
  margin-top: 2vh;
}

.property-grid-inner {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-auto-rows: minmax(150px, auto);
  grid-gap: 2vh;
  background: rgba(251, 245, 240, 0.9);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  padding: 2vh;
}

.post-list {
  position: relative;
  transition: all 0.3s ease;
}

.no-properties {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}

.header-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #609ab6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #4a7a91;
}

/* Vue transition classes */
.property-list-enter-active,
.property-list-leave-active {
  transition: all 0.5s ease;
}

.property-list-enter-from,
.property-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.property-list-move {
  transition: transform 0.5s ease;
}

@media (max-width: 600px) {
  .property-grid-inner {
    grid-template-columns: 1fr;
  }
}
</style>
