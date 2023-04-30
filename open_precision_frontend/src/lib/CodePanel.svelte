<script>
    export let responseLines = [];
</script>
<section class="code-panel u-min-width-100-percent theme-dark">
    <header class="code-panel-header">
        <div class="u-flex u-gap-16 u-margin-inline-start-auto">
            <button class="button is-text">
                <span class="icon-external-link" aria-hidden="true"></span>
                <span class="text">Raw data</span>
            </button>

        </div>
    </header>
    <code class="code-panel-content grid-code">
        {#each responseLines as line}
            <div class="grid-code-line-number"></div>
            <pre>{line}</pre>
        {/each}
    </code>
</section>