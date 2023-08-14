<template>
    <l-polyline :latlngs="[start, end]" color="gray" weight="1"></l-polyline>
    <custom-marker
        :lat-lng="end"
        :rotation="rotation"
    ></custom-marker>
</template>

<script>
import {LPolyline} from "vue3-leaflet";
import CustomMarker from "@/components/markers/ArrowheadMarker.vue";

export default {
    components: {
        LPolyline,
        CustomMarker,
    },
    props: {
        start: {
            type: Array
        },
        end: {
            type: Array
        }
    },
    computed: {
        rotation() {
            const lineDirection = Math.atan2(this.end[1] - this.start[1], this.end[0] - this.start[0]);

            return (lineDirection * 180) / Math.PI;
        }
    },
    mounted() {

    },
};

</script>
