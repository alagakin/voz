<template>
    <div class="fixed top-0 left-0 bg-gray-100 p-4 shadow-md z-100" style="z-index: 10000000;">
        <div class="flex gap-4">
            <div class="relative">
                <input v-model="station_from.display_name" placeholder="Station from" class="p-2 border rounded"
                       @input="getSuggestions('from')"/>
                <div v-if="suggestions_from.length > 0"
                     class="absolute mt-2 w-full bg-white border border-gray-300 rounded shadow-md cursor-pointer">
                    <ul>
                        <li v-for="suggestion in suggestions_from" :key="suggestion.id"
                            @click="selectSuggestion('from', suggestion)">
                            {{ suggestion['display_name'] }}
                        </li>
                    </ul>
                </div>
            </div>

            <div class="relative">
                <input v-model="station_to.display_name" placeholder="Station to" class="p-2 border rounded"
                       @input="getSuggestions('to')"/>
                <div v-if="suggestions_to.length > 0"
                     class="absolute mt-2 w-full bg-white border border-gray-300 rounded shadow-md cursor-pointer">
                    <ul>
                        <li v-for="suggestion in suggestions_to" :key="suggestion.id"
                            @click="selectSuggestion('to', suggestion)">
                            {{ suggestion['display_name'] }}
                        </li>
                    </ul>
                </div>
            </div>

            <div class="relative">
                <Calendar @selectDate="selectDate"/>
            </div>

            <button @click="search" class="px-4 py-2 bg-blue-500 text-white rounded" :class="{'bg-gray-400': !searchEnabled}">
                Search
            </button>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Calendar from "@/components/Calendar.vue";
import formatDateToYMD from "../utils/Dates"

export default {
    name: "SearchInput",
    components: {Calendar},
    methods: {
        getSuggestions(inputField) {
            const query = inputField === 'from' ? this.station_from.display_name : this.station_to.display_name;

            if (query.length >= 2) {
                axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/station/search/?query=" + query)
                    .then(response => {
                        if (inputField === 'from') {
                            this.suggestions_from = response.data.hits;
                        } else {
                            this.suggestions_to = response.data.hits;
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching suggestions:', error);
                    });
            } else {
                if (inputField === 'from') {
                    this.suggestions_from = [];
                } else {
                    this.suggestions_to = [];
                }
            }
        },
        selectSuggestion(inputField, suggestion) {
            if (inputField === 'from') {
                this.station_from = {
                    display_name: suggestion['display_name'],
                    id: suggestion['id']
                };
                this.suggestions_from = [];
            } else {
                this.station_to = {
                    display_name: suggestion['display_name'],
                    id: suggestion['id']
                };
                this.suggestions_to = [];
            }
        },
        search() {
            if (!this.searchEnabled){
                return
            }
            const params = {
                station_from: this.station_from.id,
                station_to: this.station_to.id,
                date: this.date
            };

            axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/find-routes/", {params})
                .then(response => {
                    this.$emit('setRoutes', response.data)
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                });
        },
        selectDate(date) {
            this.date = formatDateToYMD(date)
        }
    },
    computed: {
        searchEnabled() {
            return this.date && this.station_from.id && this.station_to.id
        }
    },
    data() {
        return {
            date: null,
            station_from: {
                display_name: '',
                id: false
            },
            station_to: {
                display_name: '',
                id: false
            },
            suggestions_from: [],
            suggestions_to: [],
        };

    },


};
</script>