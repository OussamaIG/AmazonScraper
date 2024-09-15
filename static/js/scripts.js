document.getElementById('scrapeForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    const formData = new FormData(this);

    // Show the loading screen
    document.getElementById('loadingScreen').style.display = 'flex';

    fetch('/scrape', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading screen
        document.getElementById('loadingScreen').style.display = 'none';

        // Optionally, you can handle the response data here
        console.log(data.message);  // For example, log the message to the console

        // You can also redirect or update the page based on the response
        // window.location.reload();  // Uncomment if you want to reload the page
    })
    .catch(error => {
        // Hide the loading screen on error
        document.getElementById('loadingScreen').style.display = 'none';
        console.error('Error:', error);
    });
});
