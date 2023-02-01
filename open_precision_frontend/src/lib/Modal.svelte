<script>
    export let header
    export let content
    export let footer

</script>
<button class="button"><span>Open Modal</span></button>
<dialog class="modal" id="dialog">
    <form class="modal-form" method="dialog">
        <header class="modal-header">
            {#if (typeof header === 'string' || header instanceof String)}
                {header}
            {:else}
                <svelte:component this={header}/>
            {/if}
            <button
                    class="button is-text is-small is-only-icon"
                    aria-label="Close modal"
            >
                <span class="icon-x" aria-hidden="true"></span>
            </button>
        </header>
        <div class="modal-content u-small">
            {#if (typeof content === 'string' || content instanceof String)}
                {content}
            {:else}
                <svelte:component this={content}/>
            {/if}
        </div>
        <div class="modal-footer">
            {#if (typeof footer === 'string' || footer instanceof String)}
                {footer}
            {:else}
                <svelte:component this={footer}/>
            {/if}
        </div>
    </form>
</dialog>