let isLoading = false;

function attractionRender(data) {
  let result = data.data;
  let attractions = document.getElementById("attractions");
  try {
    for (let i = 0; i < result.length; i++) {
      let addAttraction = document.createElement("div");
      let addImg = document.createElement("img");
      let addName = document.createElement("div");
      let detailInfo = document.createElement("div");
      let mrt = document.createElement("div");
      let cat = document.createElement("div");

      addImg.src = result[i].images[0];
      addImg.className = "attractionImg";
      addAttraction.appendChild(addImg);

      addName.textContent = result[i].name;
      addName.className = "attractionName";
      addAttraction.appendChild(addName);

      mrt.textContent = result[i].mrt;
      cat.textContent = result[i].category;
      detailInfo.appendChild(mrt);
      detailInfo.appendChild(cat);

      mrt.className = "attractionMRT";
      cat.className = "attractionCat";
      detailInfo.className = "attractionDetail";

      addAttraction.appendChild(detailInfo);
      addAttraction.className = "attraction";
      addAttraction.onclick = function () {
        window.location.href = `http://52.9.222.2:3000/attraction/${result[i].id}`;
      };

      attractions.appendChild(addAttraction);
    }
  } catch (e) {
    console.log(e);
  }
}

function getData(page) {
  isLoading = true;
  fetch(`http://52.9.222.2:3000/api/attractions?page=${page}`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data);
      attractionRender(data);
      sessionStorage.setItem("nextPage", data.nextPage);
      isLoading = false;
    });
}

function getCat() {
  let category = document.querySelector("#category");

  fetch(`http://52.9.222.2:3000/api/categories`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      let result = data.data;
      let input = document.querySelector("#search-input");
      let categoryList = document.createElement("div");
      categoryList.className = "categoryList";
      for (let i = 0; i < result.length; i++) {
        let cat = document.createElement("div");
        cat.textContent = result[i];
        cat.className = "cat";
        cat.onclick = function () {
          input.value = cat.textContent;
        };
        categoryList.appendChild(cat);
        category.appendChild(categoryList);
      }
    });
}

function search(page) {
  const searchInput = document.querySelector("#search-input");
  const input = searchInput.value;
  let attractions = document.querySelector("#attractions");
  if (page === 0) {
    while (attractions.firstChild) {
      attractions.removeChild(attractions.firstChild);
    }
  }
  console.log(input);
  isLoading = true;
  fetch(`http://52.9.222.2:3000/api/attractions?page=${page}&keyword=${input}`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data.data);
      try {
        if (data.data === undefined) {
          let attractions = document.getElementById("attractions");
          let error = document.createElement("div");
          error.textContent = "查無此關鍵字";
          error.style.fontSize = "20px";
          attractions.appendChild(error);
        }
        attractionRender(data);
        sessionStorage.setItem("searchNextPage", data.nextPage);
      } catch (e) {
        console.log(e);
      }
      isLoading = false;
    });
}

function scrollTop() {
  let scrollTop = 0;
  if (document.documentElement && document.documentElement.scrollTop) {
    scrollTop = document.documentElement.scrollTop;
  } else if (document.body) {
    scrollTop = document.body.scrollTop;
  }
  return Math.ceil(scrollTop);
}

function scrollBarHeight() {
  let scrollBarHeight = document.documentElement.clientHeight;
  return Math.ceil(scrollBarHeight);
}

function pageHeight() {
  return Math.ceil(
    Math.max(document.body.clientHeight, document.documentElement.scrollHeight)
  );
}

window.addEventListener("load", function () {
  window.onscroll = function () {
    let top = scrollTop();
    let bar = scrollBarHeight();
    let ph = pageHeight();
    let searchInput = document.querySelector("#search-input");
    let keyword = searchInput.value;

    if (top + bar === ph) {
      console.log("到底");
      if (isLoading === false) {
        if (keyword !== "") {
          let page = sessionStorage.getItem("searchNextPage");

          if (page === "null") {
            return false;
          } else {
            search(page);
          }
        } else {
          let page = sessionStorage.getItem("nextPage");
          if (page === "null") {
            return false;
          } else {
            getData(page);
          }
        }
      }
    } else {
      console.log("没有到底部");
    }
  };
});

function toHome() {
  window.location.href = "http://52.9.222.2:3000/";
}
