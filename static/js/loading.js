/**
 * Loading Screen Handler
 * Manages the display and hiding of the loading screen on page load
 */

(function() {
    'use strict';

    // Function to hide the loading screen
    function hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen && !loadingScreen.classList.contains('hidden')) {
            loadingScreen.classList.add('hidden');
            // Remove the element from the DOM after the transition completes
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }
    }

    // Hide loading screen when page finishes loading
    window.addEventListener('load', function() {
        // Wait a bit to ensure everything has loaded
        setTimeout(hideLoadingScreen, 300);
    });

    // Fallback: Hide loading screen after 12 seconds to prevent stuck state
    setTimeout(hideLoadingScreen, 12000);

    // Hide loading screen on first user interaction
    document.addEventListener('click', hideLoadingScreen, { once: true });
    document.addEventListener('scroll', hideLoadingScreen, { once: true });
    document.addEventListener('keydown', hideLoadingScreen, { once: true });
    document.addEventListener('touchstart', hideLoadingScreen, { once: true });

    // Also hide on visibilitychange when page becomes fully visible
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(hideLoadingScreen, 100);
        }
    });
})();
