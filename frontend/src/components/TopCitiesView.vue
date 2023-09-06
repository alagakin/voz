<template>
    <template v-for="city in topCities">
        <top-city-marker :city="city" @select="selectCity" v-bind:key="city['id']"
                         v-if="!selectedRoute"
                         :cityFrom="cityFrom"
                         :cityTo="cityTo"
                         :unreachable="connectedCitiesIds !== null && connectedCitiesIds.length >= 0 && !connectedCitiesIds.includes(city['id'])"
        ></top-city-marker>
    </template>
</template>
<script>
import axios from "axios";
import TopCityMarker from "@/components/TopCityMarker.vue";

export default {
    components: {TopCityMarker},
    props: {
        selectedRoute: {},
        connectedCitiesIds: {},
        request: {
            type: Object
        }
    },
    computed: {
        cityFrom() {
            if (this.request.from.type === 'city') {
                return this.request.from.id
            }
            return null
        },
        cityTo() {
            if (this.request.to.type === 'city') {
                return this.request.to.id
            }
            return null
        }
    },
    data() {
        return {
            topCities: []
        }
    },
    methods: {
        selectCity(city) {
            this.$emit('selectCity', city['id'])
        },
        getTopCities() {
            axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/locations/top_cities/").then(response => {
                if (response.data) {
                    this.topCities = response.data
                }
            }).catch(error => {
                console.error('Error fetching names:', error);
            })
        }
    },
    emits: ['selectCity'],
    mounted() {
        this.getTopCities()
    }
}

</script>