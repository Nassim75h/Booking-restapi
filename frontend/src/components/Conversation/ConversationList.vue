<template>
  <div class="conversations">
    <h2 class="text-2xl font-bold mb-4">My Conversations</h2>
    
    <!-- Conversations List -->
    <div v-if="conversations.length > 0" class="space-y-4">
      <div 
        v-for="conv in conversations" 
        :key="conv.id"
        class="conversation-item"
        :class="{ 'selected': selectedConversation?.id === conv.id }"
        @click="selectConversation(conv)"
      >
        <div class="conversation-header">
          <h3 class="property-title">{{ conv.property?.title || 'Untitled Property' }}</h3>
          <span class="date">{{ formatDate(conv.created_at) }}</span>
        </div>
        <div class="participants">
          <span class="participant" v-for="participant in conv.participants" :key="participant.id">
            {{ participant.username }}
          </span>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <i class="fas fa-comments"></i>
      <p>You don't have any conversations yet</p>
      <router-link to="/properties" class="browse-button">
        Browse Properties
      </router-link>
    </div>

    <!-- Messages Section -->
    <div v-if="selectedConversation" class="messages-section">
      <div class="messages-container">
        <div class="messages-header">
          <h3>{{ selectedConversation.property?.title }}</h3>
          <button class="close-messages" @click="selectedConversation = null">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="messages-list" ref="messagesList">
          <div 
            v-for="message in messages" 
            :key="message.id"
            class="message"
            :class="[
              message.sender.id === currentUserId ? 'sent' : 'received'
            ]"
          >
            <div class="message-content">
              <p>{{ message.content }}</p>
              <span class="message-time">{{ formatDate(message.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Message Input -->
        <form @submit.prevent="sendNewMessage" class="message-form">
          <input 
            v-model="newMessage" 
            type="text" 
            placeholder="Type your message..."
            :disabled="messageLoading"
          >
          <button 
            type="submit"
            :disabled="!newMessage.trim() || messageLoading"
          >
            <i class="fas fa-paper-plane"></i>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import useConversations from '@/composables/conversations/useConversations'
import useMessages from '@/composables/conversations/useMessages'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const currentUserId = userStore.user?.id

const { conversations, loading, fetchConversations } = useConversations()
const { messages, loading: messageLoading, fetchMessages, sendMessage } = useMessages()

const selectedConversation = ref(null)
const newMessage = ref('')
const messagesList = ref(null)

onMounted(async () => {
  try {
    await fetchConversations()
  } catch (error) {
    console.error('Failed to fetch conversations:', error)
  }
})

const selectConversation = async (conversation) => {
  selectedConversation.value = conversation
  try {
    await fetchMessages(conversation.id)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to fetch messages:', error)
  }
}

const sendNewMessage = async () => {
  if (!newMessage.value.trim() || !selectedConversation.value) return

  try {
    await sendMessage(selectedConversation.value.id, newMessage.value)
    newMessage.value = ''
    await fetchMessages(selectedConversation.value.id)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
  }
}

const scrollToBottom = () => {
  if (messagesList.value) {
    messagesList.value.scrollTop = messagesList.value.scrollHeight
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return date.toLocaleDateString('en-US', { weekday: 'long' })
  } else {
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    })
  }
}
</script>

<style scoped>
.conversations {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  min-height: calc(100vh - 64px);
}

.conversation-item {
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e2e8f0;
}

.conversation-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.conversation-item.selected {
  border-color: #4A90E2;
  background-color: #EBF5FF;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.property-title {
  font-weight: 600;
  color: #1e293b;
}

.date {
  font-size: 0.875rem;
  color: #64748b;
}

.participants {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.participant {
  font-size: 0.875rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: white;
  border-radius: 0.5rem;
  text-align: center;
}

.empty-state i {
  font-size: 3rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.browse-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #4A90E2;
  color: white;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.2s;
}

.browse-button:hover {
  background-color: #357ABD;
}

.messages-section {
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.messages-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 128px);
}

.messages-header {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.messages-header h3 {
  font-weight: 600;
  color: #1e293b;
}

.close-messages {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
}

.close-messages:hover {
  color: #1e293b;
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  flex-direction: column;
}

.message.sent {
  align-items: flex-end;
}

.message.received {
  align-items: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  position: relative;
}

.message.sent .message-content {
  background-color: #4A90E2;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.message.received .message-content {
  background-color: #f1f5f9;
  color: #1e293b;
  border-bottom-left-radius: 0.25rem;
}

.message-time {
  font-size: 0.75rem;
  margin-top: 0.25rem;
  opacity: 0.8;
}

.message-form {
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 0.5rem;
}

.message-form input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.message-form input:focus {
  outline: none;
  border-color: #4A90E2;
}

.message-form button {
  padding: 0.75rem;
  background-color: #4A90E2;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.message-form button:hover:not(:disabled) {
  background-color: #357ABD;
}

.message-form button:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .conversations {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .messages-section {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 50;
  }
}
</style>
