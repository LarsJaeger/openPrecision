<script>
    import {closeCurrent} from "./Modals.svelte";
    import {apiAddress} from "../../App.svelte";

    let input = {
        name:"",
        use_raw_location: false,
    }
    function sendAddLocation(){
        fetch(apiAddress + "/v1/store/waypoint?" + new URLSearchParams(input), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(async (response) => {
            console.log("[INFO]: added location");
            console.log(response);
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }
</script>
<div class="modal-content">
    <form class="form u-width-full-line">
        <ul class="form-list">
            <li class="form-item u-gap-8">
                <label class="label" for="name">Name</label>
                <div class="input-text-wrapper">
                    <input id="name" type="text" class="input-text" placeholder="my location" bind:value={input.name}/>
                </div>
            </li>
            <li class="form-item">
                <div class="u-flex u-gap-8">
                    <div class="input-text-wrapper">
                        <input id="useRawLocation" type="checkbox" class="input-checkbox is-big" bind:value={input.use_raw_location}/>
                    </div>
                    <label class="label is-text" for="useRawLocation">use raw receiver location</label>
                </div>
            </li>
        </ul>
    </form>
</div>
<div class="modal-footer">
    <div class="u-flex u-main-end u-gap-16">
        <button class="button" on:click={sendAddLocation} on:keypress><span class="text">Add</span></button>
        <button class="button is-secondary" on:click={closeCurrent} on:keypress><span class="text">Cancel</span>
        </button>
    </div>
</div>
