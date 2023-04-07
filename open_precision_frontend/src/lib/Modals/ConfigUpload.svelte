<script>
    import {closeCurrent} from "./Modals.svelte";
    import {sendAction} from "../ActionButtons.svelte";
    import {socket} from "../../stores.ts";
    function uploadFunction() {
        // get string of file content in variable "content"
        var file = document.getElementById("file-file").files[0];
        if(!(file instanceof Blob)) return;
        var reader = new FileReader();
        reader.onload = function (evt) {
            var content = evt.target.result;
            sendAction($socket, {
                function_identifier: 'config.load_config',
                args: [],
                kw_args: {'yaml': content}
            })
            // do something with content
        }
        reader.onerror = function (evt) {
            // do something with error
        }
        reader.readAsText(file, "UTF-8");

        // close modal
        closeCurrent();
    }
</script>
<div class="modal-content">
<form class="form u-width-full-line">
  <ul class="form-list">
    <li class="form-item">
      <input type="file" name="file" id="file-file" size="1" accept=".yml,.yaml"/>
    </li>
  </ul>
</form>
</div>
<div class="modal-footer">
<div class="u-flex u-main-end u-gap-16">
    <button class="button" on:click={uploadFunction} on:keypress><span class="text">Upload</span></button>
    <button class="button is-secondary" on:click={closeCurrent} on:keypress><span class="text">Cancel</span></button>
</div>
</div>