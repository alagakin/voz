<template>
    <div class="p-2 text-center text-lg text-gray-500">
        <font-awesome-icon :icon="['far', 'face-frown-open']" /> not found
    </div>
</template>
<script>
import {defineComponent} from 'vue'

export default defineComponent({
    name: "NotFound"
})
</script>
