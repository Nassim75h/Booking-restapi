import { createRouter, createWebHistory } from 'vue-router'
import BookingSuccessView from '../views/Booking/BookingSuccessView.vue'
import PaymentSuccessView from '../views/Payment/PaymentSuccessView.vue'
import HomeView from '../views/Homeapp/HomeView.vue'
import PropertyDetailsView from '@/views/Homeapp/PropertyDetailView.vue'
import LoginView from '@/views/Authapp/LoginView.vue'
import OwnedPropertiesView from '@/views/Homeapp/OwnedPropertiesView.vue'
import ActivateAccount from "@/views/Authapp/ActivateAccount.vue";
import SignUpView from "@/views/Authapp/SignUpView.vue";
import LandingPage from '@/views/LandingPage.vue';
import ManageBookingsView from '@/views/Homeapp/ManageBookingsView.vue';
import PaymentSuccess from '@/components/Payment/PaymentSuccess.vue';

// Lazy load the search view
const SearchView = () => import('@/views/Homeapp/SearchView.vue');

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPage
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path : '/property/:id',
    name : "property-details",
    component : PropertyDetailsView,
    props :true,
  },
  {
    path : "/login",
    name : "login",
    component : LoginView,
    props : true ,
  },
  {
    path : "/owned-properties",
    name : "owned-properties",
    component : OwnedPropertiesView,
    props : true,
  },
  {
    path : "/register",
    name : "register",
    component : SignUpView,
    props : true,
  },
  {
    path : "/activate/:token",
    name : "activate",
    component: ActivateAccount,
    props : true,
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView,
    props: route => ({ query: route.query.q })
  },
  {
    path: '/manage',
    name: 'manage-bookings',
    component: ManageBookingsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-bookings',
    name: 'my-bookings',
    component: ManageBookingsView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/booking/success/:bookingId',
    name: 'booking-success',
    component: BookingSuccessView,
    props: true
  },
  {
    path: '/payment-success',
    name: 'payment-success',
    component: PaymentSuccessView,
    props: route => ({ ...route.query })
  },
  {
    path: '/payment',
    name: 'payment',
    component: () => import('@/views/Payment/PaymentView.vue'),
    props: route => ({ ...route.query })
  },
  {
    path: '/my-bookings',
    name: 'my-bookings',
    component: () => import('@/views/Booking/MyBookingsView.vue'),
    meta: { requiresAuth: true }
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
