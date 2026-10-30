document.addEventListener("DOMContentLoaded", function () {

    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    // Mobile sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function () {
            document.body.classList.toggle("sidebar-open");
        });
    }

    // Close sidebar when clicking outside
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", function () {
            document.body.classList.remove("sidebar-open");
        });
    }

    // Highlight active sidebar link
    const currentPath = window.location.pathname.replace(/\/$/, "") || "/";

    const sidebarLinks = document.querySelectorAll(".sidebar-link");

    sidebarLinks.forEach(function (link) {

        const linkPath = new URL(link.href).pathname.replace(/\/$/, "") || "/";

        if (linkPath === currentPath) {
            link.classList.add("active");
        }

    });

});