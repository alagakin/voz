<template>
    <input v-model="query" :placeholder="placeholder"
           class="p-2 border rounded w-full focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1"
           @input="getSuggestions()"/>

    <ClearInputButton v-if="request.type || query" @click="clearQuery"/>

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
import ClearInputButton from "@/components/bar/ClearInputButton.vue";

export default {
    name: "LocationInput",
    components: {ClearInputButton},
    props: {
        placeholder: String,
        request: {
            type: Object,
            required: true
        }
    },
    watch: {
        request: {
            deep: true,
            immediate: true,
            handler(value) {
                if (value) {
                    this.setDisplayValue()
                }
            }
        }
    },
    methods: {
        clearQuery() {
            this.query = ''
            this.$emit('clearQuery')
        },
        setDisplayValue() {
            let url = ''
            if (this.request.type === 'city') {
                url = process.env.VUE_APP_BACKEND_HOST + "/api/v1/locations/city/?id=" + this.request.id
            } else if (this.request.type === 'station') {
                url = process.env.VUE_APP_BACKEND_HOST + "/api/v1/locations/station/?id=" + this.request.id
            } else {
                return
            }
            axios.get(url).then(response => {
                if (response.data.display_name) {
                    this.query = response.data.display_name
                }
            }).catch(error => {
                console.error('Error fetching names:', error);
            })

        },
        getSuggestions() {
            if (this.query.length >= 2) {
                axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/locations/?query=" + this.query)
                    .then(response => {
                        this.suggestions = response.data
                    })
                    .catch(error => {
                        console.error('Error fetching suggestions:', error);
                    });
            } else {
                this.suggestions = []
            }
        },
        selectSuggestion(suggestion) {
            this.query = suggestion['display_name']
            this.$emit('setLocation', suggestion['type'], suggestion['id'])
            this.suggestions = []
        },
        setQuery(value) {
            this.query = value
        },
        getQuery() {
            return this.query
        }
    },
    data() {
        return {
            suggestions: [],
            query: ''
        }
    },
    emits: ['setLocation', 'clearQuery']
}
</script>
