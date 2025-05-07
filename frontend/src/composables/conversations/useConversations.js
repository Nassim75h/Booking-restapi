import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default function useConversations() {
  const { get, post } = useAxios()
  const loading = ref(false)
  const error = ref(null)
  const conversations = ref([])
  const currentConversation = ref(null)

  const fetchConversations = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await get('booking/conversations/')
      conversations.value = response.data
      return conversations.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch conversations'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const getConversation = async (conversationId) => {
    loading.value = true
    error.value = null

    try {
      const response = await get(`booking/conversations/${conversationId}/`)
      currentConversation.value = response.data
      return currentConversation.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch conversation'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const createConversation = async (propertyId) => {
    loading.value = true
    error.value = null

    try {
      // First check if a conversation already exists for this property
      const existingConversations = await get('booking/conversations/')
      const existing = existingConversations.data.find(conv => 
        Number(conv.property) === Number(propertyId) || 
        Number(conv.property_id) === Number(propertyId)
      )
      
      if (existing) {
        return existing
      }

      // If no existing conversation, create a new one
      const response = await post('booking/conversations/', {
        property: propertyId // Changed from property_id to property
      })

      if (!response.data) {
        throw new Error('No data received from server')
      }

      return response.data
    } catch (err) {
      console.error('Conversation creation error:', err)
      if (err.response?.data?.detail) {
        error.value = err.response.data.detail
      } else if (err.response?.data?.message) {
        error.value = err.response.data.message
      } else if (err.message) {
        error.value = err.message
      } else {
        error.value = 'Failed to create conversation'
      }
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    conversations,
    currentConversation,
    loading,
    error,
    fetchConversations,
    getConversation,
    createConversation
  }
}
