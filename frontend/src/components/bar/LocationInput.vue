<template>
    <input v-model="query_name" placeholder="Station from"
                   class="p-2 border rounded w-full focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1"
                   @input="getSuggestions()"/>

        <div v-if="suggestions.length > 0"
             class="absolute mt-2 w-full bg-white border border-gray-300 rounded shadow-md cursor-pointer"
             style="z-index: 100000000;">
            <ul>
                <li v-for="suggestion in suggestions" :key="suggestion.id"
                    @click="selectSuggestion(suggestion)">
                    {{ suggestion['display_name'] }}
                </li>
            </ul>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "LocationInput",
    methods: {
        getSuggestions() {
            if (this.query_name.length >= 2) {
                axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/station/search/?query=" + this.query_name)
                    .then(response => {
                        this.suggestions = response.data.hits
                    })
                    .catch(error => {
                        console.error('Error fetching suggestions:', error);
                    });
            } else {
                this.suggestions = []
            }
        },
        selectSuggestion(suggestion) {
            this.query_name = suggestion['display_name']
            this.$emit('setLocation', 'station', suggestion['id'])
            this.suggestions = []
        }
    },
    data() {
        return {
            suggestions: [],
            query_name: ''
        }
    },
    emits: ['setLocation']
}
</script>