<script>
    import GeostoreAdd from "./Modals/GeostoreAdd.svelte";
    import GeostoreUse from "./Modals/GeostoreUse.svelte";
    import {add} from "./Modals/Modals.svelte";
    import {apiAddress} from "../App.svelte";
    import {onMount} from 'svelte';


    let isSelectedLocation = {};

    function activationObjToList(obj) {
        //return all keys where val is true
        return Object.keys(obj).filter(key => obj[key]);
    }

    function switchListItem(name) {
        return ()=> {isSelectedLocation[name] = !isSelectedLocation[name];}
    }

    async function getLocationNames()  {
      console.log("getting locations...")
      await fetch(apiAddress + "/v1/store/waypoint/all", {
          method: "GET",
          headers: {
              "Content-Type": "application/json"
          }
      }).then(async (response) => {
          let data = JSON.parse(await response.json());
          console.log("[DEBUG]: locations data")
          console.log(data);
          let x = {}
          data.forEach((value, index, array)=> {x[value] = (isSelectedLocation[value] == null ? true : isSelectedLocation[value])});
          isSelectedLocation = x;
      }).catch((error) => {
          console.log("[ERROR]: " + error);
      });
    }
    function addLocation() {
      add(
          "Add Location",
          GeostoreAdd,
          null,
          ()=>{
          getLocationNames()
          .then(console.log)
          .catch(console.error);
                              }
      );
    
    }
    function editLocation() {
        console.log("ISSELECTEDLOCATION");
        console.log(isSelectedLocation);
    }
    function useLocation(){
        add(
             "Select Action",
             GeostoreUse,
             {"locationNames":activationObjToList(isSelectedLocation)},
             null
        )        
    }
    
    onMount(async () => {
        await getLocationNames();
    });

</script>
<div class="card">
    <div class="action-bar u-flex u-width-full-line">
        <div class="action-bar-start u-flex u-gap-8">
            <button class="button" on:click={addLocation}><span>Add</span></button>
            <button class="button" on:click={editLocation}><span>Edit</span></button>
            <button class="button" on:click={useLocation}><span>Use</span></button>
        </div>
        <div class="action-bar-end u-flex">
            <button class="button"><span>Delete</span></button>
        </div>
    </div>
    <ul class="clickable-list">
        {#if Object.keys(isSelectedLocation).length === 0}
            <li class="clickable-list-item u-width-full-line">
                <a href="/" class="clickable-list-button">
                    <h5 class="clickable-list-title u-trim-1">
                        <span class="is-text"><i>no entries</i></span>
                    </h5>
                </a>
            </li>
        {/if}
        {#each Object.keys(isSelectedLocation) as name}
            <li class="clickable-list-item u-width-full-line">
                <div class="clickable-list-button u-flex u-gap-8">
                    <input id={"checkbox" + name} type="checkbox" bind:checked={isSelectedLocation[name]}>
                    <label for={"checkbox" + name} class="u-width-full-line">
                        <h5 class="clickable-list-title u-trim-1">
                            <span class="is-text">{name}</span>
                        </h5>
                    </label>
                </div>
            </li>
        {/each}
    </ul>
</div>
