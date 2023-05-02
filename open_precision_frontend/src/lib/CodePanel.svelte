<script>
    export let heading = "";
    export let lines = "";


    function copyToClipBoard() {
        navigator.clipboard.writeText(lines);
    }
</script>
<section class="code-panel theme-dark">
    <header class="code-panel-header u-cross-center">
        <div>
            <h5 class="heading-level-6">{heading}</h5>
        </div>
        <div class="u-flex u-gap-16 u-margin-inline-start-auto">
            <button class="button is-text" on:click={copyToClipBoard}>
                <span class="icon-clipboard-copy" aria-hidden="true"></span>
                <span class="text">Copy To Clipboard</span>
            </button>
        </div>
    </header>
    <code class="code-panel-content grid-code">
        {#each lines.split('\n') as line}
            <div class="grid-code-line-number"></div>
            <pre>{line}</pre>
        {/each}
    </code>
</section>