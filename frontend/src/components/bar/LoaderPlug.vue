<template>
    <div class="absolute w-full h-full top-0 left-0 flex flex-col justify-center"
         style="background-color:rgba(206, 206, 206, 0.3);">
        <font-awesome-icon :icon="['fas', 'spinner']" spin-pulse size="2xl" style="color: #4d5260;"/>
    </div>
</template>

<script>
export default {
    name: "LoaderPlug"
}
</script>