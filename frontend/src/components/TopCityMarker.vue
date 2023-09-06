<template>
    <l-marker :lat-lng="city['coordinates']" :iconOptions="iconOptions" @click="$emit('select', city)"></l-marker>
</template>
<script>

import {LMarker} from "vue3-leaflet";

export default {
    components: {
        LMarker
    },
    computed: {
        iconOptions() {
            return {
                iconUrl: this.city.logo,
                iconAnchor: [16, 36],
                iconSize: [32, 36],
            }
        },
    },
    props: {
        city: {
            type: Object,
            required: true
        }
    },
    emits: ['select']
}

</script>