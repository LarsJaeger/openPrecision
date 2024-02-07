<script>
    let locations;
</script>

<div class="u-z-index-0 u-full-screen-height u-width-full-line u-grid">
    <div class="tabs">
        <ul class="tabs-list">
            <li class="tabs-item">
                <button class="tabs-button is-selected">
                    <img alt="Open Precision" class="u-width-full-line is-center" src="../assets/logo.svg">
                </button>
            </li>
            <li class="tabs-item">
                <button class="tabs-button"><span class="text">Sessions</span></button>
            </li>
            <li class="tabs-item">
                <button class="tabs-button"><span class="text">Activity</span></button>
            </li>
            <li class="tabs-item">
                <button class="tabs-button"><span class="text">Settings</span></button>
            </li>
        </ul>
    </div>
    <div class="Card">
        <ul class="clickable-list">
          {#each locations as location}
              <li class="clickable-list-item">
                <a href="/" class="clickable-list-button">
                  <h5 class="clickable-list-title u-trim-1">
                    <span class="">{location.name}</span>
                  </h5>
                </a>
              </li>
            {/each}
        </ul>
    </div>
</div>
