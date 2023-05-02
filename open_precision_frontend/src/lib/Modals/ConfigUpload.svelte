<script>
    import {closeCurrent} from "./Modals.svelte";
    import {sendAction} from "../../App.svelte";
    import {socket} from "../../stores.ts";
    import CodePanel from "../CodePanel.svelte";
    import {onMount} from 'svelte';

    // set response lines
    export let responseLines = "";

    function setResponseLines(configString) {
        responseLines = configString;
        console.log("set response lines");
    }

    function request_and_update_config() { //arg has to be there
        sendAction($socket, {
                function_identifier: 'config.get_config_string',
                args: [],
                kw_args: {}
            },
            setResponseLines
        );
    }

    function uploadFunction() {
        // get string of file content in variable "content"
        var file = document.getElementById("file-file").files[0];
        if (!(file instanceof Blob)) return;
        var reader = new FileReader();
        reader.onload = function (evt) {
            var content = evt.target.result;
            sendAction($socket, {
                function_identifier: 'config.load_config',
                args: [],
                kw_args: {'yaml': content}
            }, request_and_update_config)
        }
        reader.onerror = function (evt) {
            // do something with error
        }
        reader.readAsText(file, "UTF-8");
    }

    onMount(async () => {
        request_and_update_config();
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