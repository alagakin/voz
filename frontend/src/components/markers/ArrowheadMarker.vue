<template>
    <div v-if="ready">
        <slot></slot>
    </div>
</template>

<script>
import Options from "vue3-leaflet/src/mixins/Options";

import L from 'leaflet';
import marker from "@/utils/CustomMarker";

const icon = L.icon;
const extend = L.extend;
import arrowheadSvg from "@/assets/arrowhead.svg";

export default {
    name: 'LMarker',
    inject: ['lMap'],
    mixins: [Options],
    inheritAttrs: false,
    props: {
        latLng: {
            type: [Array, Object],
            default: null,
        },
        latlng: {
            custom: true,
            type: [Array, Object],
            default: null,
        },
        iconOptions: {
            custom: true,
            type: Object,
            default: null,
        },
        divIconOptions: {
            custom: true,
            type: Object,
            default: null,
        },
        rotation: {
            type: Number
        }
    },
    data() {
        return {
            originOptions: {}
        };
    },
    methods: {
        initLeafletObject() {
            this.selfOptions = extend(this.originOptions, this.options, this.$attrs);

            this.selfOptions.icon = icon({
                iconUrl: arrowheadSvg,
                iconAnchor: [9, 9],
                iconSize: [18, 18],
            });
            this.selfOptions.rotation = this.rotation

            let latlng = this.latLng || this.latlng
            this.self = marker(latlng, this.selfOptions);

            this.initFunction();
        },

    },
    mounted() {
        this.initLeafletObject();
    }
}
</script>
