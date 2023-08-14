<template>
    <l-marker v :lat-lng="latLng" v-bind:key="latLng[1]"
              :iconOptions="iconOptions"></l-marker>
</template>

<script>
import {LMarker} from "vue3-leaflet";
export default {
    props: {
        latLng: {
            custom: true,
            type: [Array, Object],
            default: null,
        },

    },
    components: {
        LMarker
    },
    data() {
        return {
            iconOptions: {
                iconUrl: require("@/assets/marker.svg"),
                iconAnchor: [12, 24],
            }
        }

    }
}
</script>
