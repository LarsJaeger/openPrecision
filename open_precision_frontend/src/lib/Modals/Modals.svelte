<script context="module" lang="ts">
    import {writable} from 'svelte/store';
    import {SvelteComponent} from "svelte";

    function createModals() {
        const {subscribe, set, update} = writable([]);

        return {
            subscribe,
            add(title: string, bodyComponent: SvelteComponent, bodyProps: Object) {
                let item = {title, bodyComponent, bodyProps};
                update((prev) => {
                    return [item, ...prev];
                })
            },

            close(index) {
                update((prev) => {
                    prev.splice(index, 1);
                    return prev;
                })
            },
            closeAll() {
                update((prev) => {
                    return [];
                })
            }
        };
    }


    const modals = createModals();

    export function add(title: string, bodyComponent: SvelteComponent, bodyProps: Object) {
        modals.add(title, bodyComponent, bodyProps);
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
        <div class="modal u-flex u-flex-wrap u-max-width-100-percent u-overflow-x-auto u-overflow-y-auto">
            <form class="modal-form" method="dialog">
                <header class="modal-header">
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
        z-index: 2; /* Sit on top */
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        background-color: rgb(0, 0, 0); /* Fallback color */
        background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
    }
</style>
