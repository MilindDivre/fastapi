document.addEventListener('DOMContentLoaded', () => {
  // Set current date
  const currentDate = new Date().toLocaleDateString();
  document.getElementById('current-date').innerText = currentDate;

  // Handle "Run Scan" button
 
document.getElementById('run-scan').addEventListener('click', () => {
    const progress = document.getElementById('progress');
    progress.classList.remove('hidden');
    const progressBar = progress.querySelector('.progress-bar');
    progressBar.style.width = '0';

    // Simulate a progress bar
    setTimeout(() => {
      progressBar.style.width = '100%';

      // Dynamically inject content.js into the current tab
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
          chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ["content.js"],
          });
        }
      });
    }, 5000); // Simulate a 5-second scan
  });


  // Handle "Upload Tests to DB" button
  document.getElementById('upload-tests').addEventListener('click', () => {
    alert('Tests uploaded to the database!');
  });

  // Handle "Run Tests" button
  document.getElementById('run-tests').addEventListener('click', () => {
    alert('Tests are running...');
  });

  // Handle "Show Results" button
  document.getElementById('show-results').addEventListener('click', () => {
    alert('Displaying test results...');
  });

  // Settings and Help buttons
  document.getElementById('settings-btn').addEventListener('click', () => {
    alert('Settings feature coming soon!');
  });

  document.getElementById('help-btn').addEventListener('click', () => {
    alert('Help feature coming soon!');
  });
});
