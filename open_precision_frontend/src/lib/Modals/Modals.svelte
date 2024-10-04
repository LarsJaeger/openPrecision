<script context="module">
    import {writable} from 'svelte/store';
    import {SvelteComponent} from "svelte";

    function createModals() {
        const {subscribe, set, update} = writable([]);

        return {
            subscribe,
            add(title, bodyComponent, bodyProps, onClose) {
                let item = {title, bodyComponent, bodyProps, onClose};
                update((prev) => {
                    // insert item into modal list
                    return [item, ...prev];
                })
            },

            close(index) {
                update((prev) => {
                    // optionally call onClose callback
                    if (prev[index].onClose !== null) {prev[index].onClose()};

                    // remove modal from list
                    prev.splice(index, 1);
                    return prev;
                })
            },
            closeAll() {
                update((prev) => {
                    // optionally call onClose callback
                    prev.forEach((item, index, array) => {if (item.onClose !== null) {item.onClose();}});

                    // empty list
                    return [];
                })
            }
        };
    }


    const modals = createModals();

    export function add(title, bodyComponent, bodyProps, onClose) {
        modals.add(title, bodyComponent, bodyProps, onClose);
    }

    export function closeCurrent() {
        modals.close(0);
    }
    export function clickOutside(e) {
        if(e.target == this) closeCurrent();
    }
</script>

{#if $modals.length !== 0}
    <div class="modal-backdrop u-position-absolute u-cross-center u-main-center u-flex u-flex-wrap u-full-screen-height u-width-full-line u-z-index-20" on:click={clickOutside} on:keypress>
        <!-- Modal content -->
        <div class="modal u-flex u-flex-wrap u-max-width-100-percent u-overflow-x-auto u-overflow-y-auto u-z-index-20">
            <form class="modal-form" method="dialog">
                <header class="modal-header">
                    <div class="u-flex u-main-space-between u-cross-center u-gap-16">
                    <div class="avatar is-color-orange is-size-large">
                        <span>{#if ($modals.length !== 1)}{$modals.length}{/if}<span class="icon-exclamation" aria-hidden="true"></span></span>
                    </div>
                    <h4 class="modal-title heading-level-5">
                        {$modals[0].title}
                    </h4>
                    <button class="button is-text is-big is-only-icon" aria-label="Close modal"
                            on:click={closeCurrent}>
                        <span class="icon-x" aria-hidden="true"></span>
                    </button>
                    </div>
                </header>
                {#if ($modals[0].bodyProps == null)}
                    <svelte:component this={$modals[0].bodyComponent}/>
                {:else}
                    <svelte:component this={$modals[0].bodyComponent} {...$modals[0].bodyProps}/>
                {/if}
            </form>
        </div>
    </div>
{/if}
<style>
    /* The Modal (background) */
    .modal-backdrop {
        position: fixed; /* Stay in place */
        z-index: 22; /* Sit on top */
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        background-color: rgb(0, 0, 0); /* Fallback color */
        background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
    }
</style>
