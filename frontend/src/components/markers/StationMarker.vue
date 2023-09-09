<template>
    <template class="hidden">
        <l-marker :lat-lng="point['coordinates']" v-bind:key="point['coordinates'][1]"
                  :iconOptions="iconOptions">
            <l-popup>
                <div>
                    {{ point['name'] }}
                    <div>
                        arrival: {{ format(point['arrival'], 'HH:mm') }}<br>
                        departure: {{ format(point['departure'], 'HH:mm') }} <br>
                    </div>
                </div>
            </l-popup>
        </l-marker>
    </template>
</template>

<script>
import {LMarker, LPopup} from "vue3-leaflet";
import {format} from 'date-fns';

export default {
    methods: {format},
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
                iconUrl: require("@/assets/station-marker.svg"),
                iconAnchor: [9, 18]
            }
        }
    }
}
</script>
