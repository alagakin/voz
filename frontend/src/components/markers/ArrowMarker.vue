<template>
    <l-polyline :latlngs="[start, endCoords]" color="gray" weight="1" :dashArray="[4, 4]"></l-polyline>
    <custom-marker
        :lat-lng="endCoords"
        :rotation="rotation"
    ></custom-marker>
</template>

<script>
import {LPolyline} from "vue3-leaflet";
import CustomMarker from "@/components/markers/ArrowheadMarker.vue";
const shortenedBy = 0.3
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
    methods: {
        getAngle() {
            return Math.atan2(this.end[1] - this.start[1], this.end[0] - this.start[0]);
        },
    },
    computed: {
        rotation() {
            const direction = this.getAngle();
            return (direction * 180) / Math.PI;
        },
        endCoords() {
            const dx = this.end[0] - this.start[0];
            const dy = this.end[1] - this.start[1];

            const distance = Math.sqrt(dx ** 2 + dy ** 2);
            const shortenedDistance = distance * shortenedBy;

            const angle = Math.atan2(dy, dx);
            const newX = this.end[0] - shortenedDistance * Math.cos(angle);
            const newY = this.end[1] - shortenedDistance * Math.sin(angle);

            return [newX, newY];
        },

    },
};

</script>
