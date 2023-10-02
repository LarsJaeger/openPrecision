<script lang="ts">
    export let showVisualizer = false;

    function toggleVisualizer() {
        showVisualizer = !showVisualizer;
    }
</script>
<div class="u-z-index-15 u-full-screen-height u-width-full-line u-grid">
    <div class="button u-position u-position-fixed u-inset-block-end-12 u-inset-inline-start-12 is-big icon-cog u-font-size-32 icon-switch-horizontal"
         on:click={toggleVisualizer}>
    </div>
</div>