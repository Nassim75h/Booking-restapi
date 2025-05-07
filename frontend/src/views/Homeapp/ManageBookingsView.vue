<template>
  <div class="manage-bookings">
    <router-link to="/" class="back-home-btn">
      <i class="fas fa-home"></i> Back to Home
    </router-link>
    <nav class="tabs">
      <button 
        :class="{ active: activeTab === 'bookings' }" 
        @click="activeTab = 'bookings'"
      >
        <i class="fas fa-calendar-alt"></i>
        My Bookings
      </button>
      <button 
        :class="{ active: activeTab === 'conversations' }" 
        @click="activeTab = 'conversations'"
      >
        <i class="fas fa-comments"></i>
        My Conversations
      </button>
      <button 
        :class="{ active: activeTab === 'wishlist' }" 
        @click="activeTab = 'wishlist'"
      >
        <i class="fas fa-heart"></i>
        My Wishlist
      </button>
    </nav>

    <!-- Bookings Tab -->
    <div v-if="activeTab === 'bookings'" class="tab-content">
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading bookings...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="bookings && bookings.length === 0" class="empty-state">
        <i class="fas fa-calendar-times"></i>
        <p>You don't have any bookings yet.</p>
        <router-link to="/" class="browse-btn">Browse Properties</router-link>
      </div>

      <div v-else-if="bookings && bookings.length > 0" class="bookings-grid">
        <div v-for="booking in bookings" :key="booking.id" class="booking-card">
          <img 
            v-if="booking.property?.images?.length" 
            :src="booking.property.images[0]" 
            :alt="booking.property?.title" 
            class="property-image"
          />
          <div v-else class="property-image placeholder">
            <i class="fas fa-image"></i>
          </div>
          <div class="booking-info">
            <h3>{{ booking.property?.title || 'Untitled Property' }}</h3>
            <p class="dates">
              <i class="fas fa-calendar"></i>
              {{ formatDate(booking.check_in) }} - {{ formatDate(booking.check_out) }}
            </p>
            <p class="guests">
              <i class="fas fa-user-friends"></i>
              {{ booking.guests || 0 }} guests
            </p>
            <p class="price">
              <i class="fas fa-euro-sign"></i>
              {{ booking.total_price || 0 }}
            </p>
            <p :class="['status', booking.status || 'pending']">
              <i class="fas fa-circle"></i>
              {{ booking.status || 'pending' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Conversations Tab -->
    <div v-if="activeTab === 'conversations'" class="tab-content">
      <div v-if="convLoading" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading conversations...
      </div>

      <div v-else-if="convError" class="error">
        {{ convError }}
      </div>

      <div v-else-if="!conversations.length" class="empty-state">
        <i class="fas fa-comments"></i>
        <p>You don't have any conversations yet.</p>
        <router-link to="/" class="browse-btn">Browse Properties</router-link>
      </div>

      <div v-else class="conversations-list">
        <div v-for="conversation in conversations" :key="conversation.id" class="conversation-card">
          <div class="conversation-header">
            <div class="user-info">
              <i class="fas fa-user-circle"></i>
              <span>{{ conversation.other_user?.username || 'Property Owner' }}</span>
            </div>
            <span class="property-title">
              {{ conversation.property?.title || 'Unknown Property' }}
            </span>
          </div>

          <div class="messages">
            <div v-for="message in conversation.messages" :key="message.id" 
              :class="['message', message.sender_id === userId ? 'sent' : 'received']">
              <div class="message-content">
                <p>{{ message.content }}</p>
                <span class="message-time">{{ formatMessageTime(message.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="reply-form">
            <input 
              v-model="messageText[conversation.id]" 
              type="text" 
              placeholder="Type your message..."
              @keyup.enter="sendMessage(conversation.id)"
            >
            <button @click="sendMessage(conversation.id)" :disabled="!messageText[conversation.id]?.trim()">
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Wishlist Tab -->
    <div v-if="activeTab === 'wishlist'" class="tab-content">
      <div v-if="wishlistLoading" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        Loading wishlist...
      </div>

      <div v-else-if="wishlistError" class="error">
        {{ wishlistError }}
      </div>

      <div v-else-if="wishlistItems && wishlistItems.length === 0" class="empty-state">
        <i class="fas fa-heart-broken"></i>
        <p>Your wishlist is empty.</p>
        <router-link to="/" class="browse-btn">Browse Properties</router-link>
      </div>

      <div v-else-if="wishlistItems && wishlistItems.length > 0" class="wishlist-grid">
        <div v-for="item in wishlistItems" :key="item.id" class="wishlist-card">
          <img 
            v-if="item.images?.length" 
            :src="item.images[0]" 
            :alt="item.title" 
            class="property-image"
          />
          <div v-else class="property-image placeholder">
            <i class="fas fa-image"></i>
          </div>
          <div class="wishlist-info">
            <h3>{{ item.title || 'Untitled Property' }}</h3>
            <p class="price">
              <i class="fas fa-euro-sign"></i>
              {{ item.price_per_night || 0 }} per night
            </p>
            <div class="actions">
              <router-link :to="{ name: 'property-details', params: { id: item.id }}" class="view-btn">
                <i class="fas fa-eye"></i>
                View Property
              </router-link>
              <button @click="handleRemoveFromWishlist(item.id)" class="remove-btn">
                <i class="fas fa-heart-broken"></i>
                Remove
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import useBooking from '@/composables/fetchBookings/useBooking'
import useConversation from '@/composables/conversations/useConversation'
import useWishlist from '@/composables/wishlist/useWishlist'
import useAxios from '@/composables/fetchCredentials/axios'

export default {
  name: 'ManageBookingsView',
  setup() {
    const activeTab = ref('bookings')
    const bookings = ref([])
    const loading = ref(false)
    const error = ref(null)
    const messageText = ref({})
    const convLoading = ref(false)
    const convError = ref(null)
    const conversations = ref([])
    const userId = ref(null)
    
    // Wishlist state
    const wishlistLoading = ref(false)
    const wishlistError = ref(null)
    const wishlistItems = ref([])

    const { getMyBookings } = useBooking()
    const { getMyConversations, sendMessage: sendConversationMessage } = useConversation()
    const { userCredentials } = useAxios()
    const { 
      getWishlist, 
      removeFromWishlist,
      wishlistItems: wishlistItemsRef, 
      loading: wishlistLoadingRef, 
      error: wishlistErrorRef 
    } = useWishlist()

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatMessageTime = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const loadBookings = async () => {
      loading.value = true
      error.value = null
      
      try {
        const data = await getMyBookings()
        bookings.value = data
      } catch (err) {
        error.value = err.message || 'Failed to load bookings'
        console.error('Error loading bookings:', err)
      } finally {
        loading.value = false
      }
    }

    const loadConversations = async () => {
      convLoading.value = true
      convError.value = null
      
      try {
        const data = await getMyConversations()
        conversations.value = data
      } catch (err) {
        convError.value = err.message || 'Failed to load conversations'
        console.error('Error loading conversations:', err)
      } finally {
        convLoading.value = false
      }
    }

    const loadWishlist = async () => {
      wishlistLoading.value = true
      wishlistError.value = null
      
      try {
        const data = await getWishlist()
        wishlistItems.value = data
      } catch (err) {
        wishlistError.value = err.message || 'Failed to load wishlist'
        console.error('Error loading wishlist:', err)
      } finally {
        wishlistLoading.value = false
      }
    }

    const sendMessage = async (conversationId) => {
      if (!messageText.value[conversationId]?.trim()) return

      try {
        await sendConversationMessage(conversationId, messageText.value[conversationId])
        messageText.value[conversationId] = ''
        await loadConversations()
      } catch (err) {
        console.error('Error sending message:', err)
      }
    }

    const handleRemoveFromWishlist = async (propertyId) => {
      if (!propertyId) return
      
      try {
        wishlistLoading.value = true
        await removeFromWishlist(propertyId)
        await loadWishlist() // Reload the wishlist after removal
      } catch (error) {
        console.error('Failed to remove from wishlist:', error)
        wishlistError.value = error.message || 'Failed to remove from wishlist'
      } finally {
        wishlistLoading.value = false
      }
    }

    onMounted(() => {
      loadBookings()
      if (userCredentials.value) {
        userId.value = userCredentials.value.id
      }
    })

    watch(activeTab, (newTab) => {
      if (newTab === 'bookings') {
        loadBookings()
      } else if (newTab === 'conversations') {
        loadConversations()
      } else if (newTab === 'wishlist') {
        loadWishlist()
      }
    })

    return {
      activeTab,
      bookings,
      loading,
      error,
      conversations,
      convLoading,
      convError,
      messageText,
      userId,
      wishlistLoading,
      wishlistError,
      wishlistItems,
      formatDate,
      formatMessageTime,
      sendMessage,
      handleRemoveFromWishlist
    }
  }
}
</script>

<style scoped>
.manage-bookings {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.tabs button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 9999px;
  background: white;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tabs button.active {
  background: #4A90E2;
  color: white;
}

.tab-content {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  min-height: 400px;
}

.loading, .error, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem;
  text-align: center;
  color: #64748b;
}

.loading i {
  font-size: 2rem;
  color: #4A90E2;
}

.error {
  color: #ef4444;
}

.empty-state i {
  font-size: 3rem;
  color: #4A90E2;
  margin-bottom: 1rem;
}

.browse-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #4A90E2;
  color: white;
  text-decoration: none;
  border-radius: 9999px;
  transition: background-color 0.2s;
}

.browse-btn:hover {
  background: #357ABD;
}

.back-home-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #4A90E2;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: fit-content;
}

.back-home-btn:hover {
  background: #357ABD;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

.back-home-btn i {
  font-size: 1.1em;
}

/* Bookings styles */
.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.booking-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.property-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.property-image.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  height: 200px;
}

.property-image.placeholder i {
  font-size: 3rem;
  color: #94a3b8;
}

.booking-info {
  padding: 1.5rem;
}

.booking-info h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 1rem;
}

.booking-info p {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.status {
  font-weight: 500;
}

.status.confirmed {
  color: #10b981;
}

.status.pending {
  color: #f59e0b;
}

.status.cancelled {
  color: #ef4444;
}

/* Conversations styles */
.conversations-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.conversation-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1e293b;
  font-weight: 500;
}

.property-title {
  color: #64748b;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.message {
  padding: 10px;
  margin: 5px 0;
  max-width: 70%;
  border-radius: 10px;
}

.message.sent {
  margin-left: auto;
  background-color: #4A90E2;
  color: white;
}

.message.received {
  margin-right: auto;
  background-color: #f1f5f9;
  color: #1e293b;
}

.message-content {
  display: flex;
  flex-direction: column;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 4px;
  text-align: right;
}

.reply-form {
  display: flex;
  gap: 8px;
  padding: 10px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-radius: 0 0 10px 10px;
}

.reply-form input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  outline: none;
  transition: border-color 0.2s;
}

.reply-form input:focus {
  border-color: #4A90E2;
}

.reply-form button {
  padding: 8px 16px;
  background: #4A90E2;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reply-form button:hover {
  background: #357ABD;
}

.reply-form button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

/* Wishlist styles */
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.wishlist-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.wishlist-info {
  padding: 1.5rem;
}

.wishlist-info h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.price {
  color: #4A90E2;
  font-weight: 500;
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.view-btn, .remove-btn {
  flex: 1;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.view-btn {
  background: #4A90E2;
  color: white;
  text-decoration: none;
}

.view-btn:hover {
  background: #357ABD;
}

.remove-btn {
  background: white;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.remove-btn:hover {
  background: #ef4444;
  color: white;
}

@media (max-width: 640px) {
  .tabs {
    flex-direction: column;
  }

  .tabs button {
    width: 100%;
    justify-content: center;
  }

  .bookings-grid,
  .wishlist-grid {
    grid-template-columns: 1fr;
  }
}
</style>
