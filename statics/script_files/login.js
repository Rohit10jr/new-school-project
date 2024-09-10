async function login(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/simplelogin/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email, // Sending email and phone as required
            phone: phone
          }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        // Store the token in local storage
        localStorage.setItem("token", data.token);
        // Redirect to home page after successful login
        window.location.href = "/home/";
      } else {
        alert("Login failed: " + data.status);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  }