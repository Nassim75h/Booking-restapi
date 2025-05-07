<template>
  <div class="landing-page">
    <nav class="navbar">
      <div class="logo">BookingApp</div>
      <div class="nav-links">
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/register" class="nav-link register-btn">Register</router-link>
      </div>
    </nav>

    <header class="hero">
      <div class="hero-content">
        <h1>Find Your Perfect Stay</h1>
        <p>Discover amazing properties and book your dream vacation with ease.</p>
        <div class="search-bar">
          <input type="text" placeholder="Where do you want to go?" v-model="searchQuery" />
          <button @click="handleSearch" class="search-btn">Search</button>
        </div>
      </div>
    </header>

    <section class="features">
      <h2>Why Choose Us</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <i class="fas fa-home"></i>
          <h3>Unique Properties</h3>
          <p>Find one-of-a-kind places to stay.</p>
        </div>
        <div class="feature-card">
          <i class="fas fa-shield-alt"></i>
          <h3>Secure Booking</h3>
          <p>Book with confidence and peace of mind.</p>
        </div>
        <div class="feature-card">
          <i class="fas fa-clock"></i>
          <h3>24/7 Support</h3>
          <p>We're here to help anytime you need us.</p>
        </div>
      </div>
    </section>

    <section class="popular-destinations">
      <h2>Popular Destinations</h2>
      <div class="destination-grid">
        <div v-for="destination in popularDestinations" :key="destination.id" class="destination-card">
          <img :src="destination.image" :alt="destination.name" />
          <div class="destination-info">
            <h3>{{ destination.name }}</h3>
            <p>{{ destination.properties }} properties</p>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>About</h4>
          <ul>
            <li><a href="#">About Us</a></li>
            <li><a href="#">How it Works</a></li>
            <li><a href="#">Careers</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>Support</h4>
          <ul>
            <li><a href="#">Help Center</a></li>
            <li><a href="#">Contact Us</a></li>
            <li><a href="#">Privacy Policy</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 BookingApp. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LandingPage',
  setup() {
    const router = useRouter()
    const searchQuery = ref('')

    const popularDestinations = ref([
      {
        id: 1,
        name: 'Paris',
        image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34',
        properties: 1234
      },
      {
        id: 2,
        name: 'London',
        image: 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad',
        properties: 892
      },
      {
        id: 3,
        name: 'New York',
        image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9',
        properties: 1567
      },
      {
        id: 4,
        name: 'Tokyo',
        image: 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc',
        properties: 745
      }
    ])

    const handleSearch = () => {
      if (searchQuery.value) {
        router.push({
          name: 'search',
          query: { q: searchQuery.value }
        })
      }
    }

    return {
      searchQuery,
      handleSearch,
      popularDestinations
    }
  }
}
</script>

<style scoped>
.landing-page {
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

.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
              url('https://images.unsplash.com/photo-1566073771259-6a8506099945') center/cover;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
}

.hero-content {
  max-width: 800px;
  padding: 2rem;
}

.hero h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.search-bar {
  display: flex;
  gap: 0.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.search-bar input {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 9999px;
  font-size: 1rem;
}

.search-btn {
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.search-btn:hover {
  background-color: #357ABD;
}

.features {
  padding: 4rem 2rem;
  text-align: center;
}

.features h2 {
  font-size: 2rem;
  margin-bottom: 3rem;
  color: #1e293b;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 2rem;
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card i {
  font-size: 2rem;
  color: #4A90E2;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.feature-card p {
  color: #64748b;
}

.popular-destinations {
  padding: 4rem 2rem;
  background-color: white;
}

.popular-destinations h2 {
  font-size: 2rem;
  margin-bottom: 3rem;
  text-align: center;
  color: #1e293b;
}

.destination-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.destination-card {
  position: relative;
  border-radius: 1rem;
  overflow: hidden;
  aspect-ratio: 3/4;
  cursor: pointer;
}

.destination-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.destination-card:hover img {
  transform: scale(1.05);
}

.destination-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.5rem;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
}

.destination-info h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.footer {
  background-color: #1e293b;
  color: white;
  padding: 4rem 2rem 2rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section h4 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #334155;
  color: #94a3b8;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }

  .search-bar {
    flex-direction: column;
  }

  .search-btn {
    width: 100%;
  }
}
</style>
