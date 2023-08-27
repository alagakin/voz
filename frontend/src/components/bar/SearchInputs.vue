<template>
    <div class="relative">
        <input v-model="station_from.display_name" placeholder="Station from"
               class="p-2 border rounded w-full focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1"
               @input="getSuggestions('from')"/>

        <div v-if="suggestions_from.length > 0"
             class="absolute mt-2 w-full bg-white border border-gray-300 rounded shadow-md cursor-pointer"
             style="z-index: 100000000;">
            <ul>
                <li v-for="suggestion in suggestions_from" :key="suggestion.id"
                    @click="selectSuggestion('from', suggestion)">
                    {{ suggestion['display_name'] }}
                </li>
            </ul>
        </div>
    </div>

    <div class="relative mt-3">
        <input v-model="station_to.display_name" placeholder="Station to"
               class="p-2 border rounded w-full focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1"
               @input="getSuggestions('to')"/>
        <div v-if="suggestions_to.length > 0"
             class="absolute mt-2 w-full bg-white border border-gray-300 rounded shadow-md cursor-pointer"
             style="z-index: 100000000;">
            <ul>
                <li v-for="suggestion in suggestions_to" :key="suggestion.id"
                    @click="selectSuggestion('to', suggestion)">
                    {{ suggestion['display_name'] }}
                </li>
            </ul>
        </div>
    </div>

    <div class="relative mt-3">
        <CalendarView @selectDate="selectDate"/>
    </div>

    <button @click="search" class="mt-6 px-4 py-2 bg-blue-500 text-white rounded"
            :class="{'bg-gray-400': !searchEnabled}">
        Search
    </button>
</template>
<script>
import axios from "axios";
import formatDateToYMD from "@/utils/Dates";
import CalendarView from "@/components/CalendarView.vue";

export default {
    name: "SearchInputs",
    components: {CalendarView},
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
            if (!this.searchEnabled) {
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
            if (date) {
                this.date = formatDateToYMD(date)
            } else {
                this.date = null
            }
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
    emits: ['setRoutes']

}
</script>