Vue.component('reports-sec-nav', {
    delimiters: ['[[',']]'],
    props: [
        'active',
    ],
    mounted(){
        var x = document.getElementById(this.active);
        x.classList.add('active-gas');
    },

    template: /*javascript*/`
    <div class="d-flex font-semibold mb-2 justify-content-center">
        <div class="justify-content-center c-nav-links gas-nav">
            <a id="ledger" href="/ledger/" class="mx-2">Ledger</a>
            <a id="balance-sheet" href="/balance-sheet/" class="mx-2">Balance Sheet</a>
        </div>
    </div>
    `
})