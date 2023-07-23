let accountname = document.getElementById("accountname")
    accountname.innerText = localStorage.getItem('user');

    function redirectTohomepage() {
        // Set the new URL
        var newURL = "../index.html"; // Replace with the URL you want to redirect to

        // Redirect to the new page
        window.location.href = newURL;
    }
    document.getElementById('redirectButtonn').onclick = redirectTohomepage