import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeapp/HomeView.vue'
import PropertyDetailsView from '@/views/Homeapp/PropertyDetailView.vue'
import LoginView from '@/views/Authapp/LoginView.vue'
import OwnedPropertiesView from '@/views/Homeapp/OwnedPropertiesView.vue'
import ActivateAccount from "@/views/Authapp/ActivateAccount.vue";
import SignUpView from "@/views/Authapp/SignUpView.vue";

const routes = [
  {
    path: '/',
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
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
