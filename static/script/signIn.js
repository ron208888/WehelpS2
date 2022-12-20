function signInOrNot() {
  fetch("/api/user/auth", {
    method: "GET",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.data !== null) {
        let registerBtn = document.getElementById("register-btn");
        registerBtn.textContent = "登出系統";
        registerBtn.onclick = signOut;
      }
    });
}

function signOut() {
  fetch("/api/user/auth", {
    method: "DELETE",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.ok) {
        alert("已登出系統");
        location.reload();
      }
    });
}

function signUp() {
  const signUpName = document.getElementById("signUpName").value.trim();
  const signUpEmail = document.getElementById("signUpEmail").value.trim();
  const signUpPassword = document.getElementById("signUpPassword").value.trim();
  const signUpMessage = document.getElementById("signUpMessage");

  if (signUpName === "" || signUpEmail === "" || signUpPassword === "") {
    signUpMessage.textContent = "請完整輸入";
  } else {
    let signUpForm = {
      name: signUpName,
      email: signUpEmail,
      password: signUpPassword,
    };

    fetch("/api/user", {
      method: "POST",
      body: JSON.stringify(signUpForm),
      headers: { "Content-Type": "application/json" },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.ok) {
          signUpMessage.textContent = "註冊成功";
        } else if (data.error) {
          signUpMessage.textContent = data.message;
        }
      });
  }
}

function signIn() {
  const signInEmail = document.getElementById("signInEmail").value.trim();
  const signInPassword = document.getElementById("signInPassword").value.trim();
  const signInMessage = document.getElementById("signInMessage");

  if (signInEmail === "" || signInPassword === "") {
    signInMessage.textContent = "請完整輸入";
  } else {
    let signInInfo = {
      email: signInEmail,
      password: signInPassword,
    };

    fetch("/api/user/auth", {
      method: "PUT",
      body: JSON.stringify(signInInfo),
      headers: { "Content-Type": "application/json" },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.ok) {
          alert("登入成功");
          location.reload();
        } else if (data.error) {
          signInMessage.textContent = data.message;
        }
      });
  }
}

function signInBtn() {
  let signBox = document.getElementById("signBox");
  let signIn = document.getElementById("signIn");
  signBox.style.display = "flex";
  signIn.style.display = "block";
}

function cancel() {
  const signBox = document.getElementById("signBox");
  const signIn = document.getElementById("signIn");
  const signUp = document.getElementById("signUp");
  const signInEmail = document.getElementById("signInEmail");
  const signInPassword = document.getElementById("signInPassword");
  const signUpName = document.getElementById("signUpName");
  const signUpEmail = document.getElementById("signUpEmail");
  const signUpPassword = document.getElementById("signUpPassword");
  const signInMessage = document.getElementById("signInMessage");
  const signUpMessage = document.getElementById("signUpMessage");

  signBox.style.display = "none";
  signIn.style.display = "none";
  signUp.style.display = "none";

  signInEmail.value = "";
  signInPassword.value = "";
  signUpName.value = "";
  signUpEmail.value = "";
  signUpPassword.value = "";

  signInMessage.textContent = "";
  signUpMessage.textContent = "";
}

function toSignUp() {
  let signIn = document.getElementById("signIn");
  let signUp = document.getElementById("signUp");
  const signInMessage = document.getElementById("signInMessage");
  const signUpMessage = document.getElementById("signUpMessage");

  if (signIn.style.display === "block") {
    signInMessage.textContent = "";

    signIn.style.display = "none";
    signUp.style.display = "block";
  } else {
    signUpMessage.textContent = "";

    signUp.style.display = "none";
    signIn.style.display = "block";
  }
}
