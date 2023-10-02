// import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'
import preprocess from 'svelte-preprocess'
import seqPreprocessor from 'svelte-sequential-preprocessor'
import {importAssets} from 'svelte-preprocess-import-assets'
import {preprocessThrelte} from '@threlte/preprocess'

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
    preprocess: seqPreprocessor([importAssets(), preprocess(), preprocessThrelte()])

}
