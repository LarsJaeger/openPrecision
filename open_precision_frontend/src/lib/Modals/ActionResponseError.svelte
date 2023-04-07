<script>
    import {closeCurrent} from "./Modals.svelte";

    export let response;
    let response_lines = response.split("\n");
</script>

<div class="modal-content">
    <section class="code-panel u-min-width-100-percent theme-dark">
        <header class="code-panel-header">
            <div class="u-flex u-gap-16 u-margin-inline-start-auto">
                <button class="button is-text">
                    <span class="icon-external-link" aria-hidden="true"></span>
                    <span class="text">Raw data</span>
                </button>
                <button class="button is-secondary is-disabled">
                    <span class="icon-arrow-narrow-up" aria-hidden="true"></span>
                    <span class="text">Scroll to top</span>
                </button>
            </div>
        </header>
        <code class="code-panel-content grid-code">
            {#each response_lines as line}
                <div class="grid-code-line-number"></div>
                <pre>{line}</pre>
            {/each}
        </code>
    </section>
</div>
<div class="modal-footer">
    <div class="u-flex u-main-end u-gap-16">
        <button class="button" on:click={closeCurrent} on:keypress><span class="text">OK</span></button>
    </div>
</div>