// Highlight all visible elements with a red border after scanning
function highlightVisibleElements() {
  const elements = document.body.querySelectorAll('*'); // Get all elements on the page
  elements.forEach((el) => {
    const rect = el.getBoundingClientRect();
    const isVisible = rect.width > 0 && rect.height > 0 && rect.bottom > 0 && rect.right > 0;
    if (isVisible) {
      el.style.border = '2px solid red';
    }
  });
}

// Simulate a scanning effect with two green bars and overlay
function simulateScanningEffect() {
  // Create an overlay to grey out the page
  const overlay = document.createElement('div');
  overlay.style.position = 'fixed';
  overlay.style.top = 0;
  overlay.style.left = 0;
  overlay.style.width = '100%';
  overlay.style.height = '100%';
  overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)'; // Grey out
  overlay.style.zIndex = 9999;
  overlay.style.pointerEvents = 'none';

  // Add the scanning message
  const message = document.createElement('div');
  message.innerText = 'Scanning the page, please wait...';
  message.style.position = 'absolute';
  message.style.top = '50%';
  message.style.left = '50%';
  message.style.transform = 'translate(-50%, -50%)';
  message.style.color = 'white';
  message.style.fontSize = '24px';
  message.style.fontWeight = 'bold';
  message.style.textAlign = 'center';
  overlay.appendChild(message);

  // Create the first green scanning bar
  const scanner1 = document.createElement('div');
  scanner1.style.position = 'absolute';
  scanner1.style.top = 0;
  scanner1.style.left = 0;
  scanner1.style.width = '100%';
  scanner1.style.height = '5px';
  scanner1.style.backgroundColor = 'lime';
  scanner1.style.animation = 'scan1 5s linear';

  // Create the second green scanning bar
  const scanner2 = document.createElement('div');
  scanner2.style.position = 'absolute';
  scanner2.style.bottom = 0;
  scanner2.style.left = 0;
  scanner2.style.width = '100%';
  scanner2.style.height = '5px';
  scanner2.style.backgroundColor = 'lime';
  scanner2.style.animation = 'scan2 5s linear';

  // Add scanning bars to the overlay
  overlay.appendChild(scanner1);
  overlay.appendChild(scanner2);

  // Append the overlay to the body
  document.body.appendChild(overlay);

  // Remove overlay and highlight elements after 5 seconds
  setTimeout(() => {
    overlay.remove();
    highlightVisibleElements();
  }, 5000);
}

// Add CSS for scanning animations
const style = document.createElement('style');
style.textContent = `
  @keyframes scan1 {
    0% {
      top: 0;
    }
    100% {
      top: 100%;
    }
  }
  @keyframes scan2 {
    0% {
      bottom: 0;
    }
    100% {
      bottom: 100%;
    }
  }
`;
document.head.appendChild(style);

// Start the scanning effect
simulateScanningEffect();
