<template>
    <template v-for="city in topCities" v-bind:key="city['id']">
        <top-city-marker :city="city" @select="selectCity" v-if="!selected.includes(city['id']) && !selectedRoute"></top-city-marker>
    </template>
</template>
<script>
import axios from "axios";
import TopCityMarker from "@/components/TopCityMarker.vue";

export default {
    components: {TopCityMarker},
    props: {
        selected: {
            type: Array
        },
        selectedRoute: {
            type: Object
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