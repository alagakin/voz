<template>
    <VueDatePicker v-model="date"
                   :enable-time-picker="false"
                   :allowed-dates="allowedDates"
                   timezone="Europe/Belgrade"
                   format="dd.MM.yyyy"
                   :clearable="false"
                   auto-apply/>
</template>
<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import axios from "axios";

export default {
    name: "CalendarView",
    components: {VueDatePicker},
    data() {
        return {
            date: null,
            allowedDates: []
        }
    },
    mounted() {
        axios.get(process.env.VUE_APP_BACKEND_HOST + "/api/v1/routes/available-days/")
            .then(response => {
                if (response.data) {
                    this.setAllowedDates(response.data)
                }
            })
        this.date = new Date()
    },
    methods: {
        setAllowedDates(dates) {
            let result = []
            dates.forEach((date) => {
                result.push(Date.parse(date))
            })
            this.allowedDates = result
        }
    },
    watch: {
        date(newValue) {
            this.$emit('selectDate', newValue)
        }
    }
}
</script>
<style>
.dp__action_select {
    background: var(--dp-primary-color) !important;
}

:root {
    --dp-input-padding: 8px 40px 8px 12px!important; /*Padding in the input*/

}
</style>
