let alertContainer = document.querySelector('.alertContainer');
let alerts = document.querySelectorAll(".alert")
let alertCloses = document.querySelectorAll(".alert__close")
let alertCloseArray = Array.from(alertCloses)
let alertArray = Array.from(alerts)

if(alertContainer) {
  alertCloseArray.map((alertClose, index) => {
    alertClose.addEventListener("click", () => {
      alertArray[index].style.display = "none";
    })
  })
}