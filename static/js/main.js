// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function () {
    const toggler = document.querySelector('.navbar-toggler');
    const menu = document.querySelector('.navbar-menu');
    const overlay = document.querySelector('.navbar-overlay');

    if (toggler && menu) {
        toggler.addEventListener('click', function () {
            this.classList.toggle('active');
            menu.classList.toggle('active');

            if (overlay) {
                overlay.classList.toggle('active');
            }
        });

        // Close menu on overlay click
        if (overlay) {
            overlay.addEventListener('click', function () {
                toggler.classList.remove('active');
                menu.classList.remove('active');
                this.classList.remove('active');
            });
        }

        // Close menu on link click
        const navLinks = menu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                toggler.classList.remove('active');
                menu.classList.remove('active');
                if (overlay) {
                    overlay.classList.remove('active');
                }
            });
        });
    }
});