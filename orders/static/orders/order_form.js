const addItemButton = document.querySelector("#add-order-item");
const orderItems = document.querySelector("#order-items");
const itemTemplate = document.querySelector("#empty-order-item");
const totalForms = document.querySelector("#id_items-TOTAL_FORMS");

addItemButton.addEventListener("click", () => {
    const index = Number(totalForms.value);
    const item = itemTemplate.innerHTML.replaceAll("__prefix__", index);
    orderItems.insertAdjacentHTML("beforeend", item);
    totalForms.value = index + 1;
    orderItems.lastElementChild.querySelector("select").focus();
});
