<template>
    <RoutesSearcher ref="searcher"
                    :request="request"
                    @selectRoute="showRouteOnMap"
                    @update-from="updateFromRequest"
                    @update-to="updateToRequest"
                    @update-date="updateDate"/>
    <div style="width: 100%; height: 100vh;">
        <l-map ref="map" v-model:zoom="zoom" :center="[44.787197, 20.457273]" :maxBounds="maxBounds" :maxZoom="20"
               :minZoom="8">
            <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                layer-type="base"
                name="OpenStreetMap"
            ></l-tile-layer>
            <RouteView :route="selectedRoute"/>
            <TopCitiesView :request="request" :connected-cities-ids="connectedCitiesIds"
                           @select-city="selectCity" :selected-route="selectedRoute"/>
        </l-map>
    </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import {LMap, LTileLayer} from "vue3-leaflet";
import RouteView from "@/components/RouteView.vue";
import RoutesSearcher from "@/components/bar/RoutesSearcher.vue";
import TopCitiesView from "@/components/TopCitiesView.vue";
import {calculateDistance, calculateCenter} from "@/utils/Geo"
import axios from "axios";

export default {
    components: {
        TopCitiesView,
        RoutesSearcher,
        RouteView,
        LMap,
        LTileLayer,
    },
    methods: {
        showRouteOnMap(route) {
            this.selectedRoute = route
            this.$refs.searcher.open()
        },
        updateFromRequest(from) {
            this.request.from = from
        },
        updateToRequest(to) {
            this.request.to = to
        },
        updateDate(date) {
            this.request.date = date
        },
        moveView(coords1, coords2) {
            let lat1, lat2, long1, long2;
            lat1 = coords1[0]
            lat2 = coords2[0]
            long1 = coords1[1]
            long2 = coords2[1]
            this.$refs.map.panTo(
                calculateCenter(lat2, long2, lat1, long1),
            )
            setTimeout(() => {
                let distance = calculateDistance(lat1, long1, lat2, long2)
                if (distance > 300) {
                    this.$refs.map.setZoom(8)
                } else if (distance > 200) {
                    this.$refs.map.setZoom(9)
                } else if (distance > 100) {
                    this.$refs.map.setZoom(10)
                } else if (distance > 50) {
                    this.$refs.map.setZoom(10)
                } else {
                    this.$refs.map.setZoom(11)
                }
            }, 500)

        },
        recoverUrl() {
            const queryString = window.location.search;
            const params = new URLSearchParams(queryString);
            const date = params.get('date')
            const from_type = params.get('from_type')
            const from_id = params.get('from_id')
            const to_type = params.get('to_type')
            const to_id = params.get('to_id')

            let request = {
                date: null,
                from: {},
                to: {}
            }
            if (date) {
                request.date = date
            }
            if (from_type && from_id) {
                request.from.type = from_type
                request.from.id = from_id
            }
            if (to_type && to_id) {
                request.to.type = to_type
                request.to.id = to_id
            }
            this.request = request
        },
        setUrl(request) {
            const params = {};
            if (request.date) {
                params.date = request.date
            }
            if (request.from.type) {
                params.from_type = request.from.type
                params.from_id = request.from.id
            }
            if (request.to.type) {
                params.to_type = request.to.type
                params.to_id = request.to.id
            }
            const queryString = Object.keys(params)
                .map((key) => `${key}=${encodeURIComponent(params[key])}`)
                .join('&');
            const newUrl = `/?${queryString}`;
            history.pushState(null, null, newUrl);
        },
        selectCity(id) {
            if (!this.request.from.type) {
                this.request.from.type = 'city'
                this.request.from.id = id
                return;
            } else if (!this.request.to.type) {
                this.request.to.type = 'city'
                this.request.to.id = id
                return;
            } else if (this.request.from.id === this.previousSelectedCity) {
                this.request.to.type = 'city'
                this.request.to.id = id
            } else if (this.request.to.id === this.previousSelectedCity) {
                this.request.from.type = 'city'
                this.request.from.id = id
            } else {
                this.request.from.type = 'city'
                this.request.from.id = id
            }
            this.previousSelectedCity = id
        },
        fetchConnected() {
            let cityId;
            if (this.request.from.type === 'city') {
                cityId = this.request.from.id
            } else if (this.request.to.type === 'city') {
                cityId = this.request.to.id
            } else {
                return
            }
            axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/routes/connected-cities/?city_id=" + cityId)
                .then(response => {
                    if (response.data) {
                        let ids = []
                        response.data.forEach(city => {
                            ids.push(city.id)
                        })
                        this.connectedCitiesIds = ids
                    }
                })
                .catch(error => {
                    if (error.response.status === 404) {
                        this.connectedCitiesIds = []
                    } else {
                        console.error('Error fetching connected cities:', error);
                    }
                });

        }
    },
    data() {
        return {
            zoom: 8,
            selectedRoute: null,
            maxBounds: [
                [38.232407, 10.829536],
                [50.181226, 36.034919],
            ],
            request: {
                date: null,
                from: {},
                to: {}
            },
            previousSelectedCity: null,
            connectedCitiesIds: null
        };
    },
    beforeMount() {
        this.recoverUrl()
    },
    watch: {
        request: {
            deep: true,
            handler(value) {
                this.setUrl(value)
                if (this.$refs.searcher) {
                    this.$refs.searcher.search()
                }
                if ((this.request.from.type === 'city' || this.request.to.type === 'city') && !(this.request.from.type && this.request.to.type)) {
                    this.fetchConnected()
                } else {
                    this.connectedCitiesIds = null
                }
            }
        },
        selectedRoute: {
            handler(newRoute, oldRoute) {
                if (oldRoute?.['first_station'] !== newRoute?.['first_station'] && oldRoute?.['last_station'] !== newRoute?.['last_station']) {
                    if (newRoute?.from?.coordinates && newRoute?.to?.coordinates) {
                        this.moveView(newRoute.from.coordinates, newRoute.to.coordinates)
                    }
                }
            }
        }
    }
};
</script>