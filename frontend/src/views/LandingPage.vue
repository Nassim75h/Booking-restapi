<template>
  <div class="landing-page">
    <nav class="navbar">
      <div class="nav-left">
        <div class="user-info">
          <i class="fas fa-user"></i>
          <span class="username">nassim75</span>
        </div>
      </div>
      <div class="logo">EasyStayDZ</div>
      <div class="nav-right">
        <router-link to="/login" class="nav-link login-btn">Login</router-link>
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

    <section class="team">
      <div class="team-container">
        <h2 class="team-title">Meet Our Team</h2>
        <div class="team-grid">
          <div class="team-card">
            <div class="team-card-inner">
              <img src="@/assets/nas.jpg" alt="Developer" class="team-image">
              <h3>Nassim</h3>
              <p class="role">Frontend Developer</p>
              <p class="description">Lead developer specializing in Vue.js and Node.js</p>
              <div class="social-links">
                <a href="https://github.com/Nassim75h" class="social-link"><i class="fab fa-github"></i></a>
                <a href="#" class="social-link"><i class="fab fa-linkedin"></i></a>
              </div>
            </div>
          </div>
          <div class="team-card">
            <div class="team-card-inner">
              <img src="@/assets/AAD.jpg" alt="Developer" class="team-image">
              <h3>Yassine</h3>
              <p class="role">Backend Developer</p>
              <p class="description">Lead developer specializing in Django and Python, MySQL</p>
              <div class="social-links">
                <a href="https://gitlab.com/YacineBettir/Booking-restapi" class="social-link"><i class="fab fa-github"></i></a>
                <a href="#" class="social-link"><i class="fab fa-linkedin"></i></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="popular-destinations">
      <h2>Popular Destinations</h2>
      <div class="destination-grid">
        <a 
          v-for="destination in popularDestinations" 
          :key="destination.id" 
          :href="destination.link"
          target="_blank"
          class="destination-card"
        >
          <img :src="destination.image" :alt="destination.name" />
          <div class="destination-info">
            <h3>{{ destination.name }}</h3>
            <p>{{ destination.properties }} properties</p>
          </div>
        </a>
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
        name: 'Oran',
        image: require('@/assets/Oran.jpg'),
        properties: 1534,
        link:'https://fr.wikipedia.org/wiki/Oran'
      },
      {
        id: 2,
        name: 'Alger',
        image: require('@/assets/Alger.jpg'),
        properties: 2092,
        link:'https://fr.wikipedia.org/wiki/Alger'
      },
      {
        id: 3,
        name: 'Annaba',
        image: require('@/assets/Annaba.jpg'),
        properties: 1567,
        link:'https://fr.wikipedia.org/wiki/Annaba'
      },
      {
        id: 4,
        name: 'Béjaïa',
        image: require('@/assets/beijaa.jpg'),
        properties: 1245,
        link:'https://fr.wikipedia.org/wiki/B%C3%A9ja%C3%AFa'
      },
       {
        id: 5,
        name: 'Constantine',
        image: require('@/assets/Constantine.jpg'),
        properties: 1545,
        link:'https://fr.wikipedia.org/wiki/Constantine_(Alg%C3%A9rie)'
      }, {
        id: 6,
        name: 'Adrar',
        image: require('@/assets/adrar.jpg'),
        properties: 745,
        link:'https://fr.wikipedia.org/wiki/Adrar_(Alg%C3%A9rie)'
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
  padding: 1rem 2rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1e293b;
  font-weight: 500;
}

.user-info i {
  color: #4A90E2;
  font-size: 1.2rem;
}

.username {
  font-size: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4A90E2;
}

.nav-right {
  display: flex;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.login-btn {
  background-color: #4A90E2;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 9999px;
  font-size: 0.95rem;
}

.login-btn:hover {
  background-color: #357abd;
  transform: translateY(-1px);
}

.register-btn:hover {
  background-color: #357ABD;
  color: white;
}

.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
              url('@/assets/Constantine.jpg') center/cover;
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

.team {
  background-color: white;
  padding: 5rem 0;
}

.team-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.team-title {
  text-align: center;
  font-size: 2.5rem;
  color: #1e293b;
  margin-bottom: 3rem;
  position: relative;
}

.team-title:after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background-color: #4A90E2;
  border-radius: 3px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
  margin-top: 2rem;
}

.team-card {
  perspective: 1000px;
}

.team-card-inner {
  background-color: white;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.team-card:hover .team-card-inner {
  transform: translateY(-10px);
}

.team-image {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  margin-bottom: 1.5rem;
  object-fit: cover;
  border: 4px solid #4A90E2;
  padding: 4px;
}

.team-card h3 {
  color: #1e293b;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.team-card .role {
  color: #4A90E2;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.team-card .description {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.social-link {
  color: #4A90E2;
  font-size: 1.25rem;
  transition: color 0.3s ease;
}

.social-link:hover {
  color: #1e293b;
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
