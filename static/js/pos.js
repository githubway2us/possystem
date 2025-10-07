let cart = {};

function addToCart(id, name, price) {
    if (!cart[id]) {
        cart[id] = { name, price, qty: 1 };
    } else {
        cart[id].qty++;
    }
    updateCart();
}

function reduceCart(id) {
    if (cart[id]) {
        cart[id].qty--;
        if (cart[id].qty <= 0) delete cart[id];
        updateCart();
    }
}

function removeCart(id) {
    delete cart[id];
    updateCart();
}

function clearCart() {
    cart = {};
    updateCart();
}

function updateCart() {
    const tbody = document.getElementById("cart-body");
    const totalElem = document.getElementById("total");
    tbody.innerHTML = "";
    let total = 0;

    Object.entries(cart).forEach(([id, item]) => {
        const subtotal = item.qty * item.price;
        total += subtotal;

        tbody.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td class="text-center">
                    <div class="d-flex justify-content-center align-items-center gap-1">
                        <button class="btn btn-sm btn-outline-secondary" onclick="reduceCart('${id}')">-</button>
                        <span>${item.qty}</span>
                        <button class="btn btn-sm btn-outline-primary" onclick="addToCart('${id}','${item.name}',${item.price})">+</button>
                    </div>
                </td>
                <td class="text-end">${item.price.toFixed(2)}</td>
                <td class="text-end">${subtotal.toFixed(2)}</td>
                <td class="text-center">
                    <button class="btn btn-sm btn-danger" onclick="removeCart('${id}')">🗑️</button>
                </td>
            </tr>`;
    });

    totalElem.innerText = total.toFixed(2);

    // Update hidden form
    const productForm = document.getElementById("productForm");
    productForm.innerHTML = "";
    Object.entries(cart).forEach(([id, item]) => {
        productForm.innerHTML += `<input type="hidden" name="product_id" value="${id}">`;
        productForm.innerHTML += `<input type="hidden" name="quantity" value="${item.qty}">`;
    });
}
