<template>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"
         class="clear-input-icon">
        <path
            d="M23.057 7.057l-16 16c-0.52 0.52-0.52 1.365 0 1.885s1.365 0.52 1.885 0l16-16c0.52-0.52 0.52-1.365 0-1.885s-1.365-0.52-1.885 0z"></path>
        <path
            d="M7.057 8.943l16 16c0.52 0.52 1.365 0.52 1.885 0s0.52-1.365 0-1.885l-16-16c-0.52-0.52-1.365-0.52-1.885 0s-0.52 1.365 0 1.885z"></path>
    </svg>
</template>
<script>
export default {
    name: "ClearInputButton"
}
</script>
<style scoped>
.clear-input-icon {
    stroke: currentcolor;
    fill: currentcolor;
    position: absolute;
    top: 50%;
    inset-inline-end: 0;
    transform: translateY(-50%);
    cursor: pointer;
    display: inline-block;
    width: 1rem;
    height: 1rem;
    stroke-width: 0;
    padding: 6px 12px;
    color: #959595;
    box-sizing: content-box;
}
</style>