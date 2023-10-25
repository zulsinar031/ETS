if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    upd('coffee', 17000, true);
}

function upd(product, price, inc) {
    const inp = document.getElementById(product + '-number');
    let num = inp.value;
    if (inc) {
        num = parseInt(num) + 1;
    } else if (num > 0) {
        num = parseInt(num) - 1;
    }
    inp.value = num;
    // update case total 
    const caseTotal = document.getElementById(product + '-total');
    caseTotal.innerText = num * price;
    calculateTotal();
}

function getInputvalue(product) {
    const productInput = document.getElementById(product + '-number');
    const productNumber = parseInt(productInput.value);
    return productNumber;
}

function calculateTotal() {
    const Total = getInputvalue('coffee') * 17000;
    // const caseTotal = getInputvalue('case') * 59;
    const subTotal = Total;
    const tax = subTotal / 10;
    const totalPrice = subTotal + tax;
    // update on the HTML
    // document.getElementById('sub-total').innerText = subTotal;
    // document.getElementById('tax-amount').innerText = tax;
    document.getElementById('total-price').innerText = 'Rp ' + totalPrice;
}

document.querySelector('.plus-button').addEventListener('click', function () {
    upd('coffee', 17000, true);
});

document.querySelector('.minus-button').addEventListener('click', function () {
    upd('coffee', 17000, false);
});
