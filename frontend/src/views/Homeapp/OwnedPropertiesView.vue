<template>
    <div class="container">
        <button class="back-button" @click="goToHome">
            <span class="back-icon">←</span> Back to Home
        </button>
        <h1 class="title">My Properties</h1>
        <NavBar></NavBar>
        
        <!-- Loading state -->
        <div v-if="loadingProperties" class="loading-state">
            <div class="spinner"></div>
            <p>Loading your properties...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="error-state">
            <p>{{ error }}</p>
            <button @click="load" class="retry-btn">Try Again</button>
        </div>

        <!-- Properties list -->
        <div v-else>
            <PropertyList 
                :data="properties" 
                :error="error" 
                @view-property="viewPropertyDetail" 
            />
            <p v-if="properties.length === 0" class="no-properties">
                You don't have any listed properties yet. Add your first property below!
            </p>
        </div>

        <form @submit.prevent="handleSubmit" class="form">
            <h1>Post Your Properties</h1>
            <input v-model="newProperty.title" placeholder="Title" required />
            <input v-model="newProperty.city" placeholder="City" required />
            <input v-model="newProperty.address" placeholder="Address" required />
            <input v-model="newProperty.price_per_night" placeholder="Price per Night" required />
            <input v-model="newProperty.max_guests" placeholder="Max Guests" required />
            <input v-model="newProperty.description" placeholder="Description" required />
            <input v-model="newProperty.category" placeholder="Category" required />
            
            <div class="image-upload-container">
                <input 
                    type="file" 
                    @change="handleImageChange" 
                    accept="image/*" 
                    required 
                    id="property-image" 
                    multiple
                />
                <!-- Image previews -->
                <div class="image-previews" v-if="imagePreviews.length > 0">
                    <div v-for="(preview, index) in imagePreviews" :key="index" class="preview-item">
                        <img :src="preview" :alt="'Property image preview ' + (index + 1)" />
                        <button type="button" @click="removeImage(index)" class="remove-image">&times;</button>
                    </div>
                </div>
            </div>
            
            <button type="submit" :disabled="loadingSubmit" class="submit-btn">Submit</button>
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
import { useRouter } from 'vue-router';

export default {
    name: "OwnedProperties",
    components: { PropertyList, NavBar, PropertyDetail },
    setup() {
        const router = useRouter();
        const { properties, error, loading: loadingProperties, load } = getOwnedProperties();
        const { property, submit, loading: loadingSubmit, postError } = postProperty();
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
        const selectedImages = ref([]);
        const imagePreviews = ref([]); // Array of preview URLs
        const selectedPropertyData = ref(null);
        const showPropertyDetail = ref(false);

        const handleImageChange = (event) => {
            const files = event.target.files;
            if (!files) return;
            
            // Convert FileList to array
            const newFiles = Array.from(files);
            
            // Validate file types
            const validFiles = newFiles.filter(file => file.type.startsWith('image/'));
            if (validFiles.length !== newFiles.length) {
                postError.value = "Please select only image files";
                event.target.value = ''; // Reset file input
                return;
            }
            
            // Update selected images
            selectedImages.value = [...(selectedImages.value || []), ...validFiles];
            
            // Generate previews for new images
            const newPreviews = validFiles.map(file => URL.createObjectURL(file));
            imagePreviews.value = [...(imagePreviews.value || []), ...newPreviews];
        };

        const removeImage = (index) => {
            // Remove from selectedImages array
            const updatedImages = Array.from(selectedImages.value);
            updatedImages.splice(index, 1);
            selectedImages.value = updatedImages;
            
            // Remove preview
            const updatedPreviews = [...imagePreviews.value];
            URL.revokeObjectURL(updatedPreviews[index]); // Clean up object URL
            updatedPreviews.splice(index, 1);
            imagePreviews.value = updatedPreviews;
        };

        const handleSubmit = async (event) => {
            event.preventDefault();
            if (!selectedImages.value || selectedImages.value.length === 0) {
                postError.value = "Please select at least one image";
                return;
            }

            try {
                // Validate required fields
                const requiredFields = ['title', 'city', 'address', 'price_per_night', 'max_guests', 'description', 'category'];
                const missingFields = requiredFields.filter(field => !newProperty.value[field]);
                
                if (missingFields.length > 0) {
                    postError.value = `Please fill in all required fields: ${missingFields.join(', ')}`;
                    return;
                }

                // Ensure numeric values are properly formatted
                const formattedProperty = {
                    ...newProperty.value,
                    price_per_night: Number(newProperty.value.price_per_night),
                    max_guests: Number(newProperty.value.max_guests)
                };

                // Validate numeric values
                if (isNaN(formattedProperty.price_per_night) || formattedProperty.price_per_night <= 0) {
                    postError.value = 'Price per night must be a valid positive number';
                    return;
                }

                if (isNaN(formattedProperty.max_guests) || formattedProperty.max_guests <= 0) {
                    postError.value = 'Max guests must be a valid positive number';
                    return;
                }

                console.log('Submitting property:', formattedProperty);
                const result = await submit(formattedProperty);
                
                if (result && result.id) {
                    console.log('Property created successfully with ID:', result.id);
                    // Upload all images
                    const uploadPromises = Array.from(selectedImages.value).map(image => 
                        upload(result.id, image, true)
                    );

                    const imageResults = await Promise.all(uploadPromises);
                    const failedUploads = imageResults.filter(r => !r.success);

                    if (failedUploads.length > 0) {
                        postError.value = `Error uploading ${failedUploads.length} images`;
                    } else {
                        // Clear form
                        newProperty.value = {
                            title: "",
                            city: "",
                            address: "",
                            price_per_night: "",
                            max_guests: "",
                            description: "",
                            category: "",
                        };
                        // Clean up object URLs
                        imagePreviews.value.forEach(preview => URL.revokeObjectURL(preview));
                        selectedImages.value = [];
                        imagePreviews.value = [];
                        
                        // Reset file input
                        const fileInput = document.getElementById('property-image');
                        if (fileInput) fileInput.value = '';
                        
                        // Reload properties
                        await load();
                    }
                } else {
                    postError.value = "Failed to create property - no ID returned";
                }
            } catch (error) {
                console.error('Error creating property:', error);
                const errorMessage = error.response?.data?.detail || error.message || "Error creating property";
                console.error('Error details:', errorMessage);
                postError.value = errorMessage;
            }
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

        // Add navigation function
        const goToHome = () => {
            router.push('/home');
        };

        // Load owned properties on component mount
        load();

        return {
            properties,
            error,
            newProperty,
            handleSubmit,
            handleImageChange,
            loadingProperties,
            loadingSubmit,
            postError,
            propertyDetails,
            selectedPropertyData,
            showPropertyDetail,
            viewPropertyDetail,
            closePropertyDetail,
            imagePreviews,
            removeImage,
            load,
            goToHome
        };
    }
}
</script>

<style scoped>
.container {
    background: whitesmoke;
    backdrop-filter: blur(10px);
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    padding: 2rem;
    max-width: 800px;
    margin: 2rem auto;
    animation: fadeIn 0.5s ease-in-out;
    position: relative;
}

.loading-state,
.error-state,
.no-properties {
    text-align: center;
    padding: 2rem;
    background: transparent;
    border-radius: 10px;
    margin: 1rem 0;
}

.modal-content {
    background: transparent;
    backdrop-filter: blur(15px);
    border-radius: 10px;
    width: 90%;
    max-width: 1000px;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    padding: 20px;
}

.preview-item {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(229, 231, 235, 0.5);
    aspect-ratio: 1;
    background: transparent;
}

.remove-image {
    position: absolute;
    top: 5px;
    right: 5px;
    background: transparent;
    backdrop-filter: blur(5px);
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    color: #ef4444;
    transition: all 0.2s;
}

.remove-image:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: scale(1.1);
}

input {
    background: transparent;
    backdrop-filter: blur(5px);
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(229, 231, 235, 0.5);
}

input::placeholder {
    color: rgba(0, 0, 0, 0.5);
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

/* Added styles for image preview */
.image-upload-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.image-previews {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.spinner {
    width: 40px;
    height: 40px;
    margin: 0 auto 1rem;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #4A90E2;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.retry-btn {
    background: #4A90E2;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    margin-top: 1rem;
    cursor: pointer;
    transition: background 0.2s;
}

.retry-btn:hover {
    background: #357ABD;
}

.no-properties {
    color: #666;
    font-style: italic;
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

.back-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background-color: #5B9BD5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
    margin-bottom: 20px;
}

.back-button:hover {
    background-color: #4A8BC2;
}

.back-icon {
    font-size: 18px;
}
</style>