    document.addEventListener("DOMContentLoaded", function () {
        const toggle = document.querySelector(".account-toggle");
        const menu = document.querySelector(".account-menu");

        if (!toggle) return;

        toggle.addEventListener("click", function (e) {
            e.stopPropagation();
            menu.style.display = (menu.style.display === "block") ? "none" : "block";
        });

        document.addEventListener("click", function () {
            menu.style.display = "none";
        });
    });