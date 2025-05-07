import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

const useMessages = () => {
  const { get, post } = useAxios()
  const loading = ref(false)
  const error = ref(null)
  const messages = ref([])

  const fetchMessages = async (conversationId) => {
    loading.value = true
    error.value = null

    try {
      const response = await get(`booking/conversations/${conversationId}/messages/`)
      messages.value = response.data
      return messages.value
    } catch (err) {
      console.error('Error fetching messages:', err)
      error.value = err.response?.data?.message || 'Failed to fetch messages'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const sendMessage = async (conversationId, content) => {
    loading.value = true
    error.value = null

    try {
      // First verify we have a valid token
      const token = localStorage.getItem('access')
      if (!token) {
        throw new Error('Authentication required')
      }

      const response = await post(`booking/conversations/${conversationId}/messages/`, {
        content: content.trim(),
        conversation_id: conversationId
      })

      // Clear any previous errors on success
      error.value = null
      return response.data
    } catch (err) {
      console.error('Error sending message:', err)
      if (err.response?.status === 401) {
        error.value = 'Your session has expired. Please refresh the page.'
      } else if (err.response?.status === 403) {
        error.value = 'You do not have permission to send messages.'
      } else if (err.message === 'Authentication required') {
        error.value = 'Please login to send messages.'
      } else {
        error.value = err.response?.data?.message || 'Failed to send message. Please try again.'
      }
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    messages,
    loading,
    error,
    fetchMessages,
    sendMessage
  }
}

export default useMessages
