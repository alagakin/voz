<template>
    <l-marker ref="marker"
              :lat-lng="city['coordinates']"
              :iconOptions="iconOptions"
              @click="handleClick"></l-marker>
</template>
<script>

import {LMarker} from "vue3-leaflet";
import * as L from 'leaflet';

const icon = L.icon;

export default {
    components: {
        LMarker
    },
    computed: {
        iconOptions() {
            if (this.city.id === this.cityFrom) {
                return {
                    iconUrl: require("@/assets/start-marker.svg"),
                    iconAnchor: [18, 36]
                }
            } else if (this.city.id === this.cityTo) {
                return {
                    iconUrl: require("@/assets/finish-marker.svg"),
                    iconAnchor: [18, 36]
                }
            } else {
                return {
                    iconUrl: this.city.logo,
                    iconAnchor: [16, 36],
                    iconSize: [32, 36],
                    opacity: 0
                }
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
        },
        updateIcon() {
            if (this.iconOptions.iconUrl !== this.$refs.marker.iconOptions.iconUrl) {
                console.log('reset')
                this.$refs.marker.setIcon(icon(this.iconOptions))
            }
        },

    },
    props: {
        city: {
            type: Object,
            required: true
        },
        unreachable: {
            type: Boolean,
            default: false
        },
        cityFrom: {},
        cityTo: {}
    },
    watch: {
        opacity(newVal) {
            this.$refs.marker.setOpacity(newVal)
        },
        cityFrom() {
            this.updateIcon()
        },
        cityTo() {
            this.updateIcon()
        }
    },
    emits: ['select']
}

</script>