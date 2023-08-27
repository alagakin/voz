<template>
<!--    <SearchInput @setRoutes="setRoutes"/>-->
    <SideBar @setRoutes="setRoutes"/>
    <RouteInfo :routes="routes"/>
    <div style="width: 100%; height: 100vh;">
        <l-map ref="map" v-model:zoom="zoom" :center="[44.787197, 20.457273]" :maxBounds="maxBounds" :maxZoom="13" :minZoom="8">
            <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
            ></l-tile-layer>
            <RouteView :stations="stations"/>
        </l-map>
    </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import {LMap, LTileLayer} from "vue3-leaflet";
// import SearchInput from "@/components/SearchInput.vue";
import RouteView from "@/components/RouteView.vue";
import RouteInfo from "@/components/RouteInfo.vue";
import SideBar from "@/components/bar/SideBar.vue";

export default {
    components: {
        SideBar,
        RouteInfo,
        RouteView,
        // SearchInput,
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

            this.routes = routes
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
            routes: [],
            maxBounds: [
                [38.232407, 10.829536],
                [50.181226, 36.034919],
            ],
        };
    },

};
</script>