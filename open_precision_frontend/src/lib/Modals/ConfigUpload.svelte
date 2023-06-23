<script>
    import {closeCurrent} from "./Modals.svelte";
    import {apiAddress} from "../../App.svelte";
    import CodePanel from "../CodePanel.svelte";
    import {onMount} from 'svelte';

    // set response lines
    export let responseLines = "";

    function setResponseLines(configString) {
        console.log(configString);
        responseLines = configString;
        console.log("set response lines");
    }

    async function request_and_update_config() { //arg has to be there
        await fetch(apiAddress + "/v1/config/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(async (response) => {
            let data = await response.json()
            console.log(data);
            setResponseLines(data.content);
            console.log("[INFO]: local config updated");
        }).catch((error) => {
            console.log("[ERROR]: " + error);
        });
    }

    function uploadFunction() {
        // get string of file content in variable "content"
        var file = document.getElementById("file-file").files[0];
        if (!(file instanceof Blob)) return;
        var reader = new FileReader();
        reader.onload = function (evt) {
            var content = evt.target.result;

            console.log("[INFO]: Updating config");
            fetch(apiAddress + "/v1/config/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "content": content
                })
            }).then((response) => {
                console.log("[INFO]: remote config updated");
            }).catch((error) => {
                console.log("[ERROR]: " + error);
            });

        }
        reader.onerror = function (evt) {
            // do something with error
        }
        reader.readAsText(file, "UTF-8");
    }

    onMount(async () => {
        await request_and_update_config();
        document.getElementById('file-file').addEventListener('change', () => {
            if (document.getElementById('file-file').files.length === 0) return;
            uploadFunction();
        });
    });


</script>
<!-- align vertically -->
<div>
    <div class="modal-content">
        <CodePanel bind:lines={responseLines} heading="Current Config:"/>
        <label for="file-file">
            <div
                    class="box is-border-dashed is-no-shadow u-padding-24"
                    style="--box-border-radius:var(--border-radius-xsmall);"
            >
                <div class="upload-file-box u-flex u-main-center u-cross-center">
                    <div class="upload-file-box-image">
                        <span class="icon-upload" aria-hidden="true"></span>
                    </div>
                    <div class="u-min-width-0 u-text-center">
                        <h5 class="upload-file-box-title heading-level-7 u-inline">
                            <span>Drag and drop files here or click to upload</span>
                        </h5>
                    </div>
                </div>
            </div>
        </label>
        <input class="u-hide" type="file" name="file" id="file-file" size="1" accept=".yml,.yaml"/>
    </div>
    <div class="modal-footer u-cross-child-end">
        <div class="u-flex u-main-end u-gap-16">
            <button class="button" on:click={closeCurrent} on:keypress><span class="text">OK</span></button>
        </div>
    </div>
</div>