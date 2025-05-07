import { ref } from 'vue';
import useAxios from '@/composables/fetchCredentials/axios';

const postProperty = () => {
    const { post } = useAxios();
    const property = ref(null);
    const loading = ref(false);
    const postError = ref(null);

    const submit = async (propertyData) => {
        loading.value = true;
        postError.value = null;

        try {
            const response = await post('booking/owned-property/', propertyData, {
                headers: { 
                    'Content-Type': 'application/json'
                }
            });

            property.value = response.data;
            console.log('Property posted successfully:', property.value);
            return response.data; // Return the created property data

        } catch (err) {
            console.error('Error posting property:', err);

            if (err.response) {
                postError.value = err.response.data?.detail || 'Failed to post property.';
            } else if (err.request) {
                postError.value = 'No response received from the server.';
            } else {
                postError.value = 'Unexpected error occurred.';
            }
            throw err; // Re-throw the error to be handled by the caller
        } finally {
            loading.value = false;
        }
    };

    return { property, submit, loading, postError };
};

export default postProperty;
