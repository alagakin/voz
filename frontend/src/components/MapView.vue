<template>
    <RoutesSearcher @selectRoute="showRouteOnMap"/>
    <div style="width: 100%; height: 100vh;">
        <l-map ref="map" v-model:zoom="zoom" :center="[44.787197, 20.457273]" :maxBounds="maxBounds" :maxZoom="20"
               :minZoom="8">
            <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
            ></l-tile-layer>
            <RouteView :route="selectedRoute"/>
        </l-map>
    </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import {LMap, LTileLayer} from "vue3-leaflet";
import RouteView from "@/components/RouteView.vue";
import RoutesSearcher from "@/components/bar/RoutesSearcher.vue";

export default {
    components: {
        RoutesSearcher,
        RouteView,
        LMap,
        LTileLayer,
    },
    methods: {
        showRouteOnMap(route) {
            this.selectedRoute = route
        }
    },
    data() {
        return {
            zoom: 8,
            selectedRoute: null,
            maxBounds: [
                [38.232407, 10.829536],
                [50.181226, 36.034919],
            ],
        };
    },

};
</script>