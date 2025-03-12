<template>
    <div class="container">
        <h1 class="title">Owned Properties</h1>
        <NavBar></NavBar>
        <PropertyList :data="properties" :error="error" @view-property="viewPropertyDetail" />

        <form @submit.prevent="handleSubmit" class="form">
            <h1>Post Your Properties</h1>
            <input v-model="newProperty.title" placeholder="Title" required />
            <input v-model="newProperty.city" placeholder="City" required />
            <input v-model="newProperty.address" placeholder="Address" required />
            <input v-model="newProperty.price_per_night" placeholder="Price per Night" required />
            <input v-model="newProperty.max_guests" placeholder="Max Guests" required />
            <input v-model="newProperty.description" placeholder="Description" required />
            <input v-model="newProperty.category" placeholder="Category" required />
            <input type="file" @change="handleImageChange" accept="image/*" required />
            
            <button type="submit" :disabled="loading" class="submit-btn">Submit</button>
            <p v-if="postError" class="error">{{ postError }}</p>
        </form>

        <!-- Property Detail Modal -->
        <div v-if="showPropertyDetail && selectedPropertyData" class="modal-overlay">
            <div class="modal-content">
                <button @click="closePropertyDetail" class="close-btn">×</button>
                <PropertyDetail :property="selectedPropertyData" />
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import PropertyList from '@/components/Property/PropertyList.vue';
import PropertyDetail from '@/components/Property/PropertyDetail.vue';
import getOwnedProperties from '@/composables/fetchProperties/getOwnedProperties';
import postProperty from '@/composables/fetchProperties/postProperty';
import uploadPropertyImage from '@/composables/fetchProperties/uploadPropertyImage';
import getPropertyDetails from '@/composables/fetchProperties/getPropertyDetail';
import NavBar from '@/components/Snippets/NavBar.vue';

export default {
    name: "OwnedProperties",
    components: { PropertyList, NavBar, PropertyDetail },
    setup() {
        const { properties, error, load } = getOwnedProperties();
        const { property, submit, loading, postError } = postProperty();
        const { upload, fetchImages } = uploadPropertyImage();

        const newProperty = ref({
            title: "",
            city: "",
            address: "",
            price_per_night: "",
            max_guests: "",
            description: "",
            category: ""
        });

        const propertyDetails = ref(null);
        const selectedImage = ref(null);
        const showPropertyDetail = ref(false);
        const selectedPropertyData = ref(null);

        const handleImageChange = (event) => {
            selectedImage.value = event.target.files[0];
        };

        const handleSubmit = async () => {
            postError.value = null;

            try {
                await submit(newProperty.value);

                // Ensure property creation was successful
                if (property.value?.id && selectedImage.value) {
                    try {
                        // Upload the image for the owned property
                        const uploadResult = await upload(property.value.id, selectedImage.value, true);
                        console.log('Upload result:', uploadResult);

                        // Refresh property details to include the new image
                        const { property: updatedProperty, load: loadPropertyDetails } = getPropertyDetails(property.value.id);
                        await loadPropertyDetails();
                        propertyDetails.value = updatedProperty.value;
                        
                        // Fetch images specifically
                        const imagesResult = await fetchImages(property.value.id, true);
                        if (imagesResult.success && imagesResult.data) {
                            // If we have new property details, add the images to it
                            if (propertyDetails.value) {
                                propertyDetails.value.images = imagesResult.data;
                            }
                        }
                        
                        console.log('Image uploaded and property updated successfully.');
                        console.log('Updated property:', propertyDetails.value);
                        
                        // Show the property detail with the new image
                        selectedPropertyData.value = propertyDetails.value;
                        showPropertyDetail.value = true;
                        
                        // Reset the form
                        resetForm();
                        
                    } catch (error) {
                        console.error('Image upload failed:', error);
                    }
                } else {
                    console.error('Property creation failed or no image selected.');
                }

                // Refresh the properties list
                await load();
                
            } catch (error) {
                console.error('Error in form submission:', error);
            }
        };

        const resetForm = () => {
            newProperty.value = {
                title: "",
                city: "",
                address: "",
                price_per_night: "",
                max_guests: "",
                description: "",
                category: ""
            };
            selectedImage.value = null;
        };

        const viewPropertyDetail = async (propertyId) => {
            try {
                const { property: fetchedProperty, load: loadPropertyDetails } = getPropertyDetails(propertyId);
                await loadPropertyDetails();
                
                // Fetch images for this property
                const imagesResult = await fetchImages(propertyId, true);
                if (imagesResult.success && imagesResult.data) {
                    // Add images to the property data
                    fetchedProperty.value.images = imagesResult.data;
                }
                
                selectedPropertyData.value = fetchedProperty.value;
                showPropertyDetail.value = true;
            } catch (error) {
                console.error('Error fetching property details:', error);
            }
        };

        const closePropertyDetail = () => {
            showPropertyDetail.value = false;
            selectedPropertyData.value = null;
        };

        // Load owned properties on component mount
        load();

        return {
            properties,
            error,
            newProperty,
            handleSubmit,
            handleImageChange,
            loading,
            postError,
            propertyDetails,
            selectedPropertyData,
            showPropertyDetail,
            viewPropertyDetail,
            closePropertyDetail
        };
    }
}
</script>

<style scoped>
.container {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    padding: 2rem;
    max-width: 600px;
    margin: 2rem auto;
    animation: fadeIn 0.5s ease-in-out;
    position: relative;
}

.title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #4A90E2;
}

.form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

input, .submit-btn {
    padding: 0.8rem;
    border: none;
    border-radius: 10px;
    outline: none;
}

input {
    background-color: #f3f4f6;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
}

.submit-btn {
    background-color: #4A90E2;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.submit-btn:hover {
    background-color: #357ABD;
}

.error {
    color: red;
    text-align: center;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: white;
    border-radius: 10px;
    width: 90%;
    max-width: 1000px;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    padding: 20px;
}

.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    background: none;
    border: none;
    cursor: pointer;
    z-index: 1001;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>