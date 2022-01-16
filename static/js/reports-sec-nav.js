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
            <a id="income-statement" href="/income-statement/" class="mx-2">Income Statement</a>
            <a id="cash-flow" href="/cash-flow/" class="mx-2">Cash Flow</a>
            <a id="bank-recon" href="/bank-recon/" class="mx-2">Bank Reconciliation</a>
            <a id="2307" href="/2307/" class="mx-2">2307</a>
            <a id="1702Q" href="/1702-Q/" class="mx-2">1702Q</a>
            <a id="1601-C" href="/1601-C/" class="mx-2">1601-C</a>
            <a id="1601-EQ" href="/1601-EQ/" class="mx-2">1601-EQ</a>
            <a id="2316" href="/2316/" class="mx-2">2316</a>
            <a id="0619-E" href="/0619-E/" class="mx-2">0619-E</a>
        </div>
    </div>
    `
})