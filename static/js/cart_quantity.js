console.log("Cart JS Loaded");
document.addEventListener("DOMContentLoaded", function () {

    function updateCart(cartItemId, quantity, inputField) {

        fetch("/update-cart/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: `cart_item_id=${cartItemId}&quantity=${quantity}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                inputField.value = quantity;
                location.reload();  // simple way (can improve later)
            }
        });
    }

    document.querySelectorAll(".increase").forEach(button => {
        button.addEventListener("click", function () {
            let id = this.dataset.id;
            let input = document.querySelector(`input[data-id='${id}']`);
            let quantity = parseInt(input.value) + 1;
            updateCart(id, quantity, input);
        });
    });

    document.querySelectorAll(".decrease").forEach(button => {
        button.addEventListener("click", function () {
            let id = this.dataset.id;
            let input = document.querySelector(`input[data-id='${id}']`);
            let quantity = parseInt(input.value);

            if (quantity > 1) {
                quantity -= 1;
                updateCart(id, quantity, input);
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});
