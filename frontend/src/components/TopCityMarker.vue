<template>
    <l-marker ref="marker"
              :lat-lng="city['coordinates']"
              :iconOptions="iconOptions"
              @click="handleClick"></l-marker>
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
                opacity: 0
            }
        },
        opacity() {
            if (this.unreachable) {
                return 0.3
            }
            return 1
        }
    },
    methods: {
        handleClick() {
            if (!this.unreachable) {
                this.$emit('select', this.city)
            }
        }
    },
    props: {
        city: {
            type: Object,
            required: true
        },
        unreachable: {
            type: Boolean,
            default: false
        }
    },
    watch: {
        opacity(newVal) {
            this.$refs.marker.setOpacity(newVal)
        }
    },
    emits: ['select']
}

</script>