<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="overlay"></div>
        <video autoplay loop muted playsinline class="hero-video">
          <source src="https://res.cloudinary.com/dezvaompa/video/upload/v1739816326/6195516-uhd_2560_1440_25fps_3_khusre.mp4" type="video/mp4">
        </video>
      </div>
      
      <div class="hero-content">
        <div class="badge">🏠 Home Services Made Easy</div>
        <h1>Your Home Deserves <span class="highlight">Expert Care</span></h1>
        <p>Connect with verified professionals for plumbing, electrical, cleaning, and repair services.</p>
        <div class="buttons">
          <router-link to="/login" class="btn-primary">Get Started →</router-link>
          <a href="#services" class="btn-secondary">Explore Services</a>
        </div>
        <div class="features">
          <span>✓ Verified Professionals</span>
          <span>✓ Same-Day Service</span>
          <span>✓ Affordable Pricing</span>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services" id="services">
      <div class="container">
        <h2>Popular Services</h2>
        <p class="subtitle">Professional solutions for every home need</p>
        
        <div class="grid">
          <div class="card" v-for="service in services" :key="service.id">
            <div class="icon">{{ service.icon }}</div>
            <h3>{{ service.title }}</h3>
            <p>{{ service.description }}</p>
            <ul class="service-features">
              <li v-for="feature in service.features" :key="feature">✓ {{ feature }}</li>
            </ul>
            <router-link to="/login" class="link">Book Now →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="steps">
      <div class="container">
        <h2>How Fixify Works</h2>
        <p class="subtitle">Get your service in three simple steps</p>
        
        <div class="grid">
          <div class="step">
            <div class="num">1</div>
            <div class="icon">📱</div>
            <h3>Choose Service</h3>
            <p>Select the service you need</p>
          </div>
          <div class="step">
            <div class="num">2</div>
            <div class="icon">👨‍🔧</div>
            <h3>Get Matched</h3>
            <p>Connect with verified professionals</p>
          </div>
          <div class="step">
            <div class="num">3</div>
            <div class="icon">✅</div>
            <h3>Job Done</h3>
            <p>Quality service guaranteed</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="why">
      <div class="container">
        <h2>Why Choose Fixify?</h2>
        <div class="grid">
          <div class="feature">
            <div class="icon">🛡️</div>
            <h3>Verified Professionals</h3>
            <p>Background-checked and certified</p>
          </div>
          <div class="feature">
            <div class="icon">💰</div>
            <h3>Transparent Pricing</h3>
            <p>No hidden fees</p>
          </div>
          <div class="feature">
            <div class="icon">⚡</div>
            <h3>Same-Day Service</h3>
            <p>Quick response times</p>
          </div>
          <div class="feature">
            <div class="icon">⭐</div>
            <h3>Quality Guarantee</h3>
            <p>100% satisfaction guaranteed</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact -->
    <section class="contact" id="contact">
      <div class="container">
        <div class="contact-grid">
          <div class="info">
            <h2>Get in Touch</h2>
            <p>Have questions? We're here to help!</p>
            <div class="items">
              <div class="item">
                <span>📧</span>
                <div>
                  <strong>Email</strong>
                  <p>support@fixify.com</p>
                </div>
              </div>
              <div class="item">
                <span>📞</span>
                <div>
                  <strong>Phone</strong>
                  <p>080-56119034, 080-22417321</p>
                </div>
              </div>
              <div class="item">
                <span>📍</span>
                <div>
                  <strong>Address</strong>
                  <p>202, MG Road, Shivaji Nagar<br>Bengaluru, Karnataka 560001</p>
                </div>
              </div>
            </div>
          </div>
          <div class="cta-box">
            <h3>Ready to Get Started?</h3>
            <p>Book your first service today</p>
            <router-link to="/login" class="btn-primary">Book Now →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer>
      <div class="container">
        <div class="footer-top">
          <div>
            <h3>Fixify</h3>
            <p>Your trusted partner for home services</p>
          </div>
          <div class="links">
            <a href="#services">Services</a>
            <a href="#contact">Contact</a>
            <router-link to="/login">Login</router-link>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 Fixify. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'HomeView',
  setup() {
    const store = useStore();
    const router = useRouter();
    
    const services = ref([
      { 
        id: 1, 
        icon: '🔧', 
        title: 'Plumbing', 
        description: 'Expert plumbing solutions for all your needs',
        features: ['Leak repairs', 'Pipe installation', 'Emergency service']
      },
      { 
        id: 2, 
        icon: '⚡', 
        title: 'Electrical', 
        description: 'Safe and certified electrical services',
        features: ['Wiring & rewiring', 'Fixture installation', 'Safety checks']
      },
      { 
        id: 3, 
        icon: '🧹', 
        title: 'Cleaning', 
        description: 'Professional cleaning for homes and offices',
        features: ['Deep cleaning', 'Regular maintenance', 'Eco-friendly products']
      },
      { 
        id: 4, 
        icon: '🔨', 
        title: 'Repairs', 
        description: 'Quick fixes for appliances and furniture',
        features: ['Appliance repair', 'Furniture assembly', 'Door & window fixes']
      }
    ]);

    onMounted(() => {
      const role = store.getters.userRole;
      if (role) {
        router.push(role === 'admin' ? '/admindashboard' : role === 'professional' ? '/professionaldashboard' : '/customerdashboard');
      }
    });

    return { services };
  }
});
</script>

<style scoped>
* { margin: 0; padding: 0; box-sizing: border-box; }

.home-view {
  font-family: 'Inter', -apple-system, sans-serif;
  overflow-x: hidden;
}

/* Hero */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.3;
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  padding: 2rem;
  text-align: center;
  color: white;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.hero-content h1 {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.highlight {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-content > p {
  font-size: clamp(1rem, 2vw, 1.25rem);
  max-width: 700px;
  margin: 0 auto 3rem;
  opacity: 0.95;
}

.buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 1rem 2.5rem;
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: #1a1a2e;
  text-decoration: none;
  font-weight: 600;
  border-radius: 50px;
  transition: transform 0.3s;
}

.btn-primary:hover { transform: translateY(-2px); }

.btn-secondary {
  padding: 1rem 2.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  text-decoration: none;
  font-weight: 600;
  border-radius: 50px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s;
}

.btn-secondary:hover { background: rgba(255, 255, 255, 0.2); }

.features {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.features span {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Common */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

section { padding: 6rem 0; }

h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  text-align: center;
  margin-bottom: 1rem;
}

.subtitle {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 4rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

/* Services */
.services { background: #f8f9fa; }

.card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s;
}

.card:hover { transform: translateY(-10px); }

.card .icon {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
}

.card h3 {
  font-size: 1.5rem;
  color: #1a1a2e;
  margin-bottom: 1rem;
}

.card p {
  color: #666;
  margin-bottom: 1.5rem;
}

.service-features {
  list-style: none;
  margin-bottom: 1.5rem;
}

.service-features li {
  color: #555;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.link {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}

.link:hover { color: #764ba2; }

/* Steps */
.steps { background: white; }

.step {
  text-align: center;
  position: relative;
  padding: 2rem;
}

.num {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
}

.step .icon {
  font-size: 4rem;
  margin: 2rem 0 1.5rem;
}

.step h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.step p { color: #666; }

/* Why Choose Us */
.why {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.why h2 { color: white; }

.feature {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s;
}

.feature:hover { transform: translateY(-5px); }

.feature .icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.feature h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.feature p { opacity: 0.9; }

/* Contact */
.contact { background: white; }

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
}

.info h2 {
  text-align: left;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.info > p {
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.item {
  display: flex;
  gap: 1rem;
}

.item span { font-size: 2rem; }

.item strong {
  display: block;
  color: #1a1a2e;
  margin-bottom: 0.25rem;
}

.item p {
  color: #666;
  line-height: 1.6;
}

.cta-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  padding: 3rem;
  text-align: center;
}

.cta-box h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.cta-box p {
  margin-bottom: 2rem;
  opacity: 0.9;
}

/* Footer */
footer {
  background: #1a1a2e;
  color: white;
  padding: 3rem 0 1.5rem;
}

.footer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 2rem;
}

.footer-top h3 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.footer-top p { opacity: 0.7; }

.links {
  display: flex;
  gap: 2rem;
}

.links a {
  color: white;
  text-decoration: none;
  opacity: 0.8;
}

.links a:hover { opacity: 1; }

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  opacity: 0.6;
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .features { gap: 1rem; }
  .grid { grid-template-columns: 1fr; }
  .contact-grid { grid-template-columns: 1fr; }
  .footer-top { flex-direction: column; text-align: center; }
  .links { justify-content: center; }
}
</style>