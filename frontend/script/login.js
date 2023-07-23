const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});



let form1 = document.getElementById("signup-form")
form1.addEventListener("click", (e) => {
    e.preventDefault()
    const payload = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        user_status: "true",
        gender: "male",
        membership_type: "user",
        bio: "im a user",
        date_of_birth: "10-10-2000",
        password: document.getElementById("password").value
    }
    console.log(payload)
    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(payload)
    }).then(res => res.json())
        .then((res) => {
            if (res.message === "Username already exists") {
                Swal.fire({
                    icon: 'error',
                    title: 'Registration Failed!',
                    text: res.message,
                    confirmButtonText: 'OK',
                })
                name: document.getElementById("name").value = ""
                email: document.getElementById("email").value = ""
                password: document.getElementById("password").value = ""
            } else {
                console.log(res)
                Swal.fire(
                    'Successfully Register',
                    'You clicked the button!',
                    'success'
                )
                name: document.getElementById("name").value = ""
                email: document.getElementById("email").value = ""
                password: document.getElementById("password").value = ""
            }

        })
        .catch(err => console.log(err))
})


//signin===========

let form2 = document.getElementById("form-signin")
form2.addEventListener("click", (e) => {
    e.preventDefault()
    const payload = {
        email: document.getElementById("email1").value,
        password: document.getElementById("password1").value
    }
    console.log(payload)
    if(payload.email=="admin@gmail.com" && payload.password=="admin"){
        localStorage.setItem("admin", payload.email);
        window.location.href="admin.html"
    }
    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(payload)
    }).then(res => res.json())
        .then(res => {
            if (res.message === "Login successfully") {
                localStorage.setItem("token", res.access_token)
                localStorage.setItem("user", res.name)
                localStorage.setItem("email", payload.email)
                console.log(res)
                Swal.fire(
                    'Successfully Login',
                    'You clicked the button!',
                    'success'
                )
                document.getElementById("email1").value = ""
                document.getElementById("password1").value = ""
                window.location.href="movie.html"
                // window.open("product.html")
            } else if (res.message === "Invalid username or password") {
                Swal.fire({
                    icon: 'error',
                    title: 'Login Failed!',
                    text: res.message,
                    confirmButtonText: 'OK',
                })
                console.log("wrong")
            }

        })
        .catch(err => console.log(err.message))
})
