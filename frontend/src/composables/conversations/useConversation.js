import { ref } from 'vue';
import useAxios from '../fetchCredentials/axios';

export default function useConversation() {
  const { get, post } = useAxios();
  const loading = ref(false);
  const error = ref(null);
  const conversations = ref([]);

  const getMyConversations = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await get('booking/conversations/');
      conversations.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to fetch conversations';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getConversationById = async (conversationId) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await get(`booking/conversations/${conversationId}/`);
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to fetch conversation';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const sendMessage = async (conversationId, message) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await post(`booking/conversations/${conversationId}/messages/`, {
        content: message
      });
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to send message';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const startConversation = async (propertyId, initialMessage) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await post('booking/conversations/', {
        property_id: propertyId,
        initial_message: initialMessage
      });
      return response.data;
    } catch (err) {
      error.value = err.message || 'Failed to start conversation';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    conversations,
    getMyConversations,
    getConversationById,
    sendMessage,
    startConversation
  };
}
