import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),

  actions: {
    setUser(user) {
      this.user = user
      this.isAuthenticated = !!user
    },

    clearUser() {
      this.user = null
      this.isAuthenticated = false
    }
  },

  getters: {
    getUserId: (state) => state.user?.id,
    getUsername: (state) => state.user?.username,
    getIsAuthenticated: (state) => state.isAuthenticated
  }
})
