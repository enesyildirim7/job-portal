tailwind.config = {
  theme: {
    fontFamily: {
      sans: ["Inter", "sans-serif"],
    },
  },
};

// Header kullanıcı butonu dropdown menü
function dropClick() {
  document.getElementById("dropy").classList.toggle("show-drop");
}

// Django message otomatik kapama
var message_ele = document.getElementById("message-box-id");
setTimeout(function () {
  message_ele.style.display = "none";
}, 3000);
