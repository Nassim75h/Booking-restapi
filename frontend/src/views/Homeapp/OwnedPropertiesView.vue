<template>
    <div class="container">
        <h1 class="title">Owned Properties</h1>
        <NavBar></NavBar>
        <PropertyList :data="properties" :error="error" />

        <form @submit.prevent="handleSubmit" class="form">
            <input v-model="newProperty.title" placeholder="Title" required />
            <input v-model="newProperty.city" placeholder="City" required />
            <input v-model="newProperty.address" placeholder="Address" required />
            <input v-model="newProperty.price_per_night" placeholder="Price per Night" required />
            <input v-model="newProperty.max_guests" placeholder="Max Guests" required />
            <input v-model="newProperty.description" placeholder="Description" required />
            <input v-model="newProperty.category" placeholder="Category" required />
            <button type="submit" :disabled="loading" class="submit-btn">Submit</button>
            <p v-if="postError" class="error">{{ postError }}</p>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue';
import PropertyList from '@/components/Property/PropertyList.vue';
import getOwnedProperties from '@/composables/fetchProperties/getOwnedProperties';
import postProperty from '@/composables/fetchProperties/postProperty';
import NavBar from '@/components/Snippets/NavBar.vue';

export default {
    name: "OwnedProperties",
    components: { PropertyList, NavBar },
    setup() {
        const { properties, error, load } = getOwnedProperties();
        const { property, submit, loading, postError } = postProperty();

        const newProperty = ref({
            title: "",
            city: "",
            address: "",
            price_per_night: "",
            max_guests: "",
            description: "",
            category: ""
        });

        const handleSubmit = async () => {
            postError.value = null; // ✅ Clear any previous errors before submitting
            await submit(newProperty.value);
            
            if (!postError.value) { 
                await load(); // ✅ Ensures property list refreshes correctly
            }
        };

        load();

        return {
            properties,
            error,
            newProperty,
            handleSubmit,
            loading,
            postError
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
