function toHome() {
  window.location.href = " /";
}

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

function signInOrNotForBookingPage() {
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
        registerBtn.onclick = signOutForBookingPage;
      } else {
        window.location.href = "/";
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

function signOutForBookingPage() {
  fetch("/api/user/auth", {
    method: "DELETE",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.ok) {
        alert("已登出系統");
        window.location.href = "/";
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

function signInBooking() {
  fetch("/api/user/auth", {
    method: "GET",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.data !== null) {
        window.location.href = "/booking";
      } else {
        signInBtn();
      }
    });
}

function startBooking() {
  fetch("/api/user/auth", {
    method: "GET",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.data !== null) {
        const nowOn = window.location.pathname;
        const attractionId = nowOn.split("/").reverse()[0];
        const date = document.getElementById("chooseDate").value;
        const feeCount = document.getElementById("feeCount").textContent;
        let time = "";
        let price = 0;

        if (date === "" && feeCount === "") {
          alert("請選擇日期及時間");
        } else if (date === "") {
          alert("請選擇日期");
        } else if (feeCount === "") {
          alert("請選擇時間");
        } else {
          if (feeCount === "新台幣2000元") {
            time = "morning";
            price = 2000;
          } else {
            time = "afternoon";
            price = 2500;
          }
          let bookingInfo = {
            attractionId: attractionId,
            date: date,
            time: time,
            price: price,
          };

          fetch("/api/booking", {
            method: "POST",
            body: JSON.stringify(bookingInfo),
            headers: { "Content-Type": "application/json" },
          })
            .then(function (response) {
              return response.json();
            })
            .then(function (data) {
              if (data.ok) {
                alert("已新增至預定行程，請點右上角按鈕查看");
                // window.location.href = "/booking";
              } else if (data.message === "SameTime") {
                alert("該時段已有預定行程");
              } else {
                alert("伺服器錯誤");
              }
            });
        }
      } else {
        signInBtn();
      }
    });
}

function reservation() {
  fetch("/api/booking", {
    method: "GET",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      const result = data.data;

      if (result.error) {
        const attractionInfo = document.getElementById("attractionInfo");
        attractionInfo.remove();

        const main = document.getElementById("main");
        const noBooking = document.createElement("div");
        const noBookingTitle = document.createElement("div");
        const noBookingMessage = document.createElement("div");

        noBookingTitle.textContent = `您好，${result.userName}，待預定的行程如下：`;
        noBookingTitle.className = "bookingTitle";

        noBookingMessage.textContent = "目前沒有任何待預訂的行程";
        noBookingMessage.className = "bookingText";

        noBooking.appendChild(noBookingTitle);
        noBooking.appendChild(noBookingMessage);
        noBooking.className = "noBooking";

        main.appendChild(noBooking);
        main.style.marginBottom = "-104px";
        main.style.height = "100%";
      } else {
        const bookingTitle = document.getElementById("bookingTitle");
        bookingTitle.textContent = `您好，${result[0].userName}，待預定的行程如下：`;

        const bookingName = document.getElementById("bookingName");
        bookingName.value = result[0].userName;

        const bookingEmail = document.getElementById("bookingEmail");
        bookingEmail.value = result[0].email;

        let total = 0;
        for (let i = 0; i < result.length; i++) {
          const bookingItem = document.getElementById("bookingItem");
          const oneBookingItem = document.createElement("div");
          const bookingItemImg = document.createElement("div");
          const bookingItemInfo = document.createElement("div");
          const bookingItemTitle = document.createElement("div");
          const bookingDate = document.createElement("div");
          const bookingTime = document.createElement("div");
          const bookingPrice = document.createElement("div");
          const bookingAddress = document.createElement("div");
          const trashCan = document.createElement("div");

          bookingItemImg.style.backgroundImage = `url(${result[i].attraction.image})`;
          bookingItemImg.className = "bookingItemImg";
          oneBookingItem.appendChild(bookingItemImg);

          bookingItemTitle.textContent = `台北一日遊：${result[i].attraction.name}`;
          bookingItemTitle.className = "bookingItemTitle";
          // bookingItemTitle.id = `name${i}`;
          bookingItemTitle.id = result[i].attraction.id;
          bookingItemInfo.appendChild(bookingItemTitle);

          bookingDate.textContent = `日期：${result[i].date}`;
          bookingDate.className = "bookingText";
          bookingDate.id = `date${i}`;
          bookingItemInfo.appendChild(bookingDate);

          if (result[i].time === "morning") {
            bookingTime.textContent = "時間：早上9點到下午2點";
            bookingTime.className = "bookingTime";
            bookingTime.id = `morning${i}`;
            bookingItemInfo.appendChild(bookingTime);
          } else {
            bookingTime.textContent = "時間：下午3點到晚上8點";
            bookingTime.className = "bookingTime";
            bookingTime.id = `afternoon${i}`;
            bookingItemInfo.appendChild(bookingTime);
          }

          bookingPrice.textContent = `費用：新台幣${result[i].price}元`;
          bookingPrice.className = "bookingText";
          bookingItemInfo.appendChild(bookingPrice);

          bookingAddress.textContent = `地點：${result[i].attraction.address}`;
          bookingAddress.className = "bookingText";
          bookingAddress.id = `address${i}`;
          bookingItemInfo.appendChild(bookingAddress);

          trashCan.className = "trashCan";
          trashCan.id = `trash${i}`;
          trashCan.onclick = trash;

          bookingItemInfo.appendChild(trashCan);
          bookingItemInfo.className = "bookingItemInfo";

          oneBookingItem.appendChild(bookingItemInfo);
          oneBookingItem.className = "oneBookingItem";
          bookingItem.appendChild(oneBookingItem);

          total += result[i].price;
        }
        const price = document.getElementById("price");
        price.textContent = `總價：新台幣${total}元`;
      }
    });
}

function trash(id) {
  let trashId = id.path[0].id;

  const date = document.getElementById(`date${trashId.slice(5)}`).innerHTML;

  let time =
    document.getElementsByClassName("bookingTime")[trashId.slice(5)]
      .textContent;

  if (time.slice(3) === "早上9點到下午2點") {
    time = "morning";
  } else {
    time = "afternoon";
  }

  let deleteItem = { date: date.slice(3), time: time };

  fetch("/api/booking", {
    method: "DELETE",
    body: JSON.stringify(deleteItem),
    headers: { "Content-Type": "application/json" },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.ok) {
        id.path[2].remove();
        location.reload();
        const trashCan = document.querySelector(".trashCan");
        // if (trashCan === null) {
        //   location.reload();
        // }
      } else {
        alert(data.message);
      }
    });
}
