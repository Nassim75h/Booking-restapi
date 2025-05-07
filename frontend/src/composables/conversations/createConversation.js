import { ref } from 'vue'
import useAxios from '@/composables/fetchCredentials/axios'

export default function useConversations() {
  const { get, post } = useAxios()
  const loading = ref(false)
  const error = ref(null)
  const conversations = ref([])

  const startConversation = async (propertyId, message) => {
    loading.value = true
    error.value = null

    try {
      const response = await post(
        `/booking/properties/${propertyId}/conversations/`,
        { message }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to start conversation'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const getConversations = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await get('/booking/conversations/')
      conversations.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch conversations'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    startConversation,
    getConversations,
    loading,
    error,
    conversations
  }
}
