<template>
    <SearchInput @setRoutes="setRoutes"/>
    <div style="width: 100%; height: 100vh;">
        <l-map ref="map" v-model:zoom="zoom" :center="[44.787197, 20.457273]">
            <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
            ></l-tile-layer>
            <l-marker v-for="point in points" :lat-lng="point" v-bind:key="point[0]"></l-marker>
        </l-map>
    </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import {LMap, LTileLayer, LMarker} from "vue3-leaflet";
import SearchInput from "@/components/SearchInput.vue";

export default {
    components: {
        SearchInput,
        LMap,
        LTileLayer,
        LMarker
    },
    methods: {
        setRoutes(routes) {
            this.points = []
            if (!routes.length) {
                alert('Not found')
            }
            let route = routes[0]
            route.stations.forEach(station => {
                this.points.push(station.coordinates)
            })

        }
    },
    data() {
        return {
            zoom: 8,
            points: [],
        };
    },

};
</script>