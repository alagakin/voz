<template>
    <SearchInput @setRoutes="setRoutes"/>
    <div style="width: 100%; height: 100vh;">
        <l-map ref="map" v-model:zoom="zoom" :center="[44.787197, 20.457273]">
            <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
            ></l-tile-layer>
            <RouteView :stations="stations" />
        </l-map>
    </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import {LMap, LTileLayer} from "vue3-leaflet";
import SearchInput from "@/components/SearchInput.vue";
import RouteView from "@/components/RouteView.vue";

export default {
    components: {
        RouteView,
        SearchInput,
        LMap,
        LTileLayer,
    },
    methods: {
        setRoutes(routes) {
            this.stations = []
            if (!routes.length) {
                alert('Not found')
            }
            //todo function for formatting
            routes.forEach(route => {
                route.stations.forEach(station => {
                    station.arrival = new Date(station.arrival)
                    station.departure = new Date(station.departure)
                })
            })

            let route = routes[0]

            route.stations.forEach(station => {
                this.stations.push(station)
            })
        }
    },
    data() {
        return {
            zoom: 8,
            stations: [],
        };
    },

};
</script>