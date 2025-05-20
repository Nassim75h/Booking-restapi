<template>
  <div class="search-page">
    <nav class="navbar">
      <router-link to="/" class="logo">BookingApp</router-link>
      <div class="nav-links">
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/register" class="nav-link register-btn">Register</router-link>
      </div>
    </nav>

    <div class="search-container">
      <div class="search-header">
        <h1>Search Results for "{{ query }}"</h1>
        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search properties..." 
            @keyup.enter="handleSearch"
          />
          <button @click="handleSearch" class="search-btn">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="properties.length === 0" class="no-results">
        <i class="fas fa-search"></i>
        <p>No properties found for "{{ query }}"</p>
        <p>Try adjusting your search terms or explore our popular destinations.</p>
      </div>

      <div v-else class="property-grid">
        <div v-for="property in properties" :key="property.id" class="property-card">
          <img :src="property.image" :alt="property.title" class="property-image" />
          <div class="property-info">
            <h3>{{ property.title }}</h3>
            <p class="location">
              <i class="fas fa-map-marker-alt"></i>
              {{ property.city }}
            </p>
            <p class="price">DZ{{ property.price_per_night }} / night</p>
            <div class="property-features">
              <span>
                <i class="fas fa-user"></i>
                {{ property.max_guests }} guests
              </span>
              <span>
                <i class="fas fa-tag"></i>
                {{ property.category }}
              </span>
            </div>
            <router-link :to="{ name: 'property-details', params: { id: property.id }}" class="view-btn">
              View Details
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import useAxios from '@/composables/fetchCredentials/axios'
import getProperties from '@/composables/fetchProperties/getProperties'

export default {
  name: 'SearchView',
  props: {
    query: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const router = useRouter()
    const searchQuery = ref(props.query)
    const properties = ref([])
    const loading = ref(false)
    const error = ref(null)
    const { get } = useAxios()
    const { load: loadProperties } = getProperties()

    const searchProperties = async (query) => {
      loading.value = true
      error.value = null
      try {
        const { data, load } = getProperties()
        await load()
        
        console.log('Loaded properties:', data.value)
        
        if (!data.value) {
          throw new Error('No properties loaded')
        }
        
        // Filter properties based on search query
        properties.value = query
          ? data.value.filter(p => 
              p.title?.toLowerCase().includes(query.toLowerCase()) ||
              p.city?.toLowerCase().includes(query.toLowerCase()) ||
              p.description?.toLowerCase().includes(query.toLowerCase()) ||
              p.address?.toLowerCase().includes(query.toLowerCase())
            )
          : data.value

        console.log('Filtered properties:', properties.value)
      } catch (err) {
        error.value = 'Failed to load properties. Please try again.'
        console.error('Search error:', err)
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      if (searchQuery.value) {
        router.push({ name: 'search', query: { q: searchQuery.value } })
        searchProperties(searchQuery.value)
      }
    }

    watch(() => props.query, (newQuery) => {
      searchQuery.value = newQuery
      if (newQuery) {
        searchProperties(newQuery)
      }
    })

    onMounted(() => {
      if (props.query) {
        searchProperties(props.query)
      } else {
        // Load all properties if no query
        searchProperties('')
      }
    })

    return {
      searchQuery,
      properties,
      loading,
      error,
      handleSearch
    }
  }
}
</script>

<style scoped>
.search-page {
  min-height: 100vh;
  background-color: #f8fafc;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4A90E2;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #64748b;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #4A90E2;
}

.register-btn {
  background-color: #4A90E2;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 9999px;
}

.register-btn:hover {
  background-color: #357ABD;
  color: white;
}

.search-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.search-header {
  margin-bottom: 2rem;
}

.search-header h1 {
  font-size: 2rem;
  color: #1e293b;
  margin-bottom: 1rem;
}

.search-bar {
  display: flex;
  gap: 0.5rem;
  max-width: 600px;
}

.search-bar input {
  flex: 1;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  font-size: 1rem;
}

.search-btn {
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 9999px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.2s;
}

.search-btn:hover {
  background-color: #357ABD;
}

.loading, .error, .no-results {
  text-align: center;
  padding: 4rem 0;
  color: #64748b;
}

.loading i, .no-results i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #4A90E2;
}

.error {
  color: #ef4444;
}

.property-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.property-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.property-card:hover {
  transform: translateY(-5px);
}

.property-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.property-info {
  padding: 1.5rem;
}

.property-info h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.location {
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.price {
  font-size: 1.25rem;
  font-weight: bold;
  color: #4A90E2;
  margin-bottom: 1rem;
}

.property-features {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #64748b;
}

.property-features span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-btn {
  display: block;
  text-align: center;
  background-color: #4A90E2;
  color: white;
  text-decoration: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
}

.view-btn:hover {
  background-color: #357ABD;
}

@media (max-width: 768px) {
  .search-bar {
    flex-direction: column;
  }

  .search-btn {
    width: 100%;
    padding: 1rem;
  }

  .property-grid {
    grid-template-columns: 1fr;
  }
}
</style>
