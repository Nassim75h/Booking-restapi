<template>
  <div class="conversation-form">
    <h3 class="title">Contact Host</h3>
    
    <form @submit.prevent="handleSubmit" class="form-content">
      <div class="form-group">
        <label for="message">Message</label>
        <textarea
          id="message"
          v-model="messageText"
          rows="4"
          placeholder="Write your message to the host..."
          required
          :disabled="loading"
        ></textarea>
      </div>

      <button 
        type="submit" 
        class="send-button" 
        :disabled="loading || !messageText.trim()"
      >
        <span v-if="loading">
          <i class="fas fa-spinner fa-spin"></i>
          Sending...
        </span>
        <span v-else>
          <i class="fas fa-paper-plane"></i>
          Send Message
        </span>
      </button>

      <p v-if="error" class="error-message">{{ error }}</p>
      <p v-if="success" class="success-message">{{ success }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import useAxios from '@/composables/fetchCredentials/axios'
import useConversations from '@/composables/conversations/useConversations'
import useMessages from '@/composables/conversations/useMessages'

const props = defineProps({
  propertyId: {
    type: [Number, String],
    required: true
  }
})

const emit = defineEmits(['message-sent'])

const { createConversation, loading: convLoading } = useConversations()
const { sendMessage, loading: msgLoading } = useMessages()

const messageText = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const validateMessage = () => {
  if (!messageText.value.trim()) {
    error.value = 'Please enter a message'
    return false
  }
  if (messageText.value.length < 2) {
    error.value = 'Message is too short (minimum 2 characters)'
    return false
  }
  if (messageText.value.length > 1000) {
    error.value = 'Message is too long (maximum 1000 characters)'
    return false
  }
  return true
}

const handleSubmit = async () => {
  error.value = ''
  success.value = ''

  if (!validateMessage()) {
    return
  }

  loading.value = true

  try {
    // First create or get existing conversation
    const conversation = await createConversation(Number(props.propertyId))
    if (!conversation?.id) {
      throw new Error('Could not create conversation')
    }
    
    // Then send the message in that conversation
    const result = await sendMessage(conversation.id, messageText.value)
    if (!result) {
      throw new Error('Failed to send message')
    }
    
    success.value = 'Message sent successfully!'
    messageText.value = ''
    emit('message-sent')
  } catch (err) {
    console.error('Failed to send message:', err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else if (err.response?.data?.message) {
      error.value = err.response.data.message
    } else if (err.message) {
      error.value = err.message
    } else {
      error.value = 'Failed to send message. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.conversation-form {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #1e293b;
}

textarea {
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  resize: vertical;
  min-height: 100px;
  transition: border-color 0.2s;
}

textarea:focus {
  outline: none;
  border-color: #4A90E2;
}

textarea:disabled {
  background-color: #f1f5f9;
  cursor: not-allowed;
}

.send-button {
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.send-button:hover:not(:disabled) {
  background-color: #357ABD;
}

.send-button:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  padding: 0.5rem;
  background-color: #fef2f2;
  border-radius: 0.375rem;
  border: 1px solid #fee2e2;
}

.login-prompt {
  text-align: center;
  padding: 2rem;
  background-color: #f8fafc;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.login-prompt p {
  color: #475569;
  margin: 0;
}

.login-link {
  color: #2563eb;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.login-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.success-message {
  color: #059669;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  padding: 0.5rem;
  background-color: #f0fdf4;
  border-radius: 0.375rem;
  border: 1px solid #dcfce7;
}

i {
  font-size: 1.1rem;
}
</style>
