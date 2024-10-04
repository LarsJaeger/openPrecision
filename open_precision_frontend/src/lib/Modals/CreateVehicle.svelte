<script>
    import {closeCurrent} from "./Modals.svelte";

    function uploadFunction() {
        // get string of file content in variable "content"

        // close modal
        closeCurrent();
    }
</script>
<div class="modal-content">
    <form class="form u-width-full-line">
        <ul class="form-list">
            <li class="form-item">
                <label class="label">Name</label>
                <div class="input-text-wrapper">
                    <input type="text" class="input-text" placeholder="kleiner roter Traktor"/>
                </div>
                <label class="label">GPS Receiver Offset [meter]</label>
                <div class="input-text-wrapper">
                    <input type="text" class="input-text" placeholder="1"/>
                    <input type="text" class="input-text" placeholder="1"/>
                    <input type="text" class="input-text" placeholder="1"/>
                </div>
            </li>
        </ul>
    </form>
</div>
<div class="modal-footer">
    <div class="u-flex u-main-end u-gap-16">
        <button class="button" on:click={uploadFunction} on:keypress><span class="text">Upload</span></button>
        <button class="button is-secondary" on:click={closeCurrent} on:keypress><span class="text">Cancel</span>
        </button>
    </div>
</div>