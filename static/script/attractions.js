function getAttraction() {
  let nowOn = window.location.pathname;
  console.log(nowOn);
  let page = nowOn.split("/").reverse()[0];

  fetch(`http://52.9.222.2:3000/api/attractions/${page}`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data);
      let result = data.data;
      let nameInfo = document.getElementById("nameInfo");
      let catInfo = document.getElementById("catInfo");
      let description = document.getElementById("description");
      let address = document.getElementById("address");
      let transport = document.getElementById("transport");

      nameInfo.textContent = result.name;
      catInfo.textContent = `${result.category}at${result.mrt}`;
      description.textContent = result.description;
      address.textContent = result.address;
      transport.textContent = result.transport;

      let images = result.images;
      console.log(images);
      let imgScreen = document.getElementById("imgScreen");
      let sliderMain = document.getElementById("sliderMain");

      let next = document.getElementById("next");
      let prev = document.getElementById("prev");
      let index = document.getElementById("index");

      for (let i = 0; i < images.length; i++) {
        let item = document.createElement("div");
        let a = document.createElement("a");
        let img = document.createElement("img");

        img.src = images[i];
        item.className = "item";
        a.appendChild(img);
        item.appendChild(a);
        sliderMain.appendChild(item);
      }

      let allItem = sliderMain.children;
      for (let i = 0; i < allItem.length; i++) {
        let span = document.createElement("div");
        if (i === 0) {
          span.className = "dot";
        } else {
          span.className = "indexIcon";
        }

        index.appendChild(span);
      }
    });
}

let index = 0;

function refresh() {
  console.log(index);
  if (index > document.querySelectorAll(".indexIcon").length) {
    index = 0;
  } else if (index < 0) {
    index = document.querySelectorAll(".indexIcon").length;
  }

  let imgScreen = document.getElementById("imgScreen");
  let width = getComputedStyle(imgScreen).width;
  width = Number(width.slice(0, -2));

  imgScreen.querySelector("#sliderMain").style.left = index * width * -1 + "px";

  changeIndex();
}

function changeIndex() {
  let indexBox = document.getElementById("index");
  for (let i = 0; i < indexBox.children.length; i++) {
    indexBox.children[i].className = "indexIcon";
  }
  indexBox.children[index].className = "dot";
}

function next() {
  index++;
  refresh();
}

function prev() {
  index--;
  refresh();
}

refresh();

function morning() {
  let feeCount = document.getElementById("feeCount");
  feeCount.textContent = "新台幣2000元";
}

function afternoon() {
  let feeCount = document.getElementById("feeCount");
  feeCount.textContent = "新台幣2500元";
}

function toHome() {
  window.location.href("http://52.9.222.2:3000/");
}
