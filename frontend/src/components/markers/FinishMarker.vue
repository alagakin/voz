<template>
    <template class="hidden">
        <l-marker :lat-lng="point['coordinates']" v-bind:key="point['coordinates'][1]"
                  :iconOptions="iconOptions">
            <l-popup>
                <div>
                    {{ point['name'] }}
                </div>
                <div>
                    arrival: {{ format(point['arrival'], 'HH:mm') }}<br>
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
        LPopup,
        LMarker
    },
    data() {
        return {
            iconOptions: {
                iconUrl: require("@/assets/finish-marker.svg"),
                iconAnchor: [18, 36],
            }
        }

    }
}
</script>
<script setup>
import {format} from "date-fns";
</script>