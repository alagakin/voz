<template>
    <template class="hidden">
        <l-marker :lat-lng="point['coordinates']" v-bind:key="point['coordinates'][1]"
                  :iconOptions="iconOptions">
            <l-popup>
                <div>
                    {{ point['name'] }}
                </div>
            </l-popup>
        </l-marker>
    </template>
</template>

<script>
import {LMarker, LPopup} from "vue3-leaflet";

export default {
    props: {
        point: {
            type: [Array, Object],
            default: null,
        }
    },
    components: {
        LMarker, LPopup
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
