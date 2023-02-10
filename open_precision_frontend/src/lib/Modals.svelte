<script context="module" lang="ts">
    import {writable} from 'svelte/store';
    import {SvelteComponent} from "svelte";

    function createModals() {
        const {subscribe, set, update} = writable([]);

        return {
            subscribe,
            add(item) {
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

    export function openModal(title: string, contentComp: SvelteComponent, footerComp: SvelteComponent) {
        modals.add({title, contentComp, footerComp});
    }

    function closeTopModal() {
        modals.close(0);
    }
</script>

{#if $modals.length !== 0}
    <div class="modal-backdrop">
        <!-- Modal content -->
        <div class="modal is-big">
            <form class="modal-form" method="dialog">
                <header class="modal-header">
                    <div class="avatar is-color-orange">
                        <span class="icon-exclamation" aria-hidden="true"></span>
                    </div>
                    <h4 class="modal-title heading-level-5">
                        {$modals[0].title}
                    </h4>
                    <button class="button is-text is-big is-only-icon" aria-label="Close modal"
                            on:click={closeTopModal}>
                        <span class="icon-x" aria-hidden="true"></span>
                    </button>
                </header>

                <div class="modal-content">
                    {#if (typeof $modals[0].contentComp === 'string' || $modals[0].contentComp instanceof String)}
                        {$modals[0].contentComp}
                    {:else}
                        <svelte:component this={$modals[0].contentComp}/>
                    {/if}
                </div>

                <div class="modal-footer">
                    {#if (typeof $modals[0].footerComp === 'string' || $modals[0].footerComp instanceof String)}
                        {$modals[0].footerComp}
                    {:else}
                        <svelte:component this={$modals[0].footerComp}/>
                    {/if}
                </div>
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

    /* Modal Content */
    .margin-auto {
        margin: auto;
        /*padding: 20px; */
        /*border: 1px solid #888;*/
        /*width: 80%;*/
    }
</style>
