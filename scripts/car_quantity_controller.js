async function calc_price() {
    document.querySelectorAll(".quantity").forEach(input => {
      input.addEventListener("input", async function () {
        const quantity = this.value;
        const product = this.dataset.productId;
        const url = this.dataset.url;
        const outputSet = this.dataset.outputId;
        const output = document.getElementById(outputSet).querySelector(".price_output");
        let finalPrice = 0;


        if (quantity === "") return;

        fetch(`order/change/${product}/?quantity=${quantity}`)
                .then(response => response.json())
                .then(data => {
                  output.innerText = data.total
                })
                .catch(() => {
                  output.innerText = "I failed"
                })
        await new Promise(resolve => setTimeout(resolve, 100))
        const finalPriceSpan = document.getElementsByClassName("price_output");

        for (let i = 0; i < finalPriceSpan.length; i++) {
          finalPrice += Number(finalPriceSpan[i].innerText);
          console.log(finalPrice)
        }
        document.getElementById("price_final").innerText = String(finalPrice);
      });
    });
  };
  document.getElementById("price_final").addEventListener("DOMContentLoaded", calc_price());
  document.getElementById("price_final").onload = calc_price();
  calc_price();