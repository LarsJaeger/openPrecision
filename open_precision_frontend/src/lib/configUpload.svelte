<script>
    import {closeTopModal} from './Modals.svelte'
</script>
<p>Hallo, hier dein Gedöns: <input type="file" on:submit={closeTopModal} /></p>
