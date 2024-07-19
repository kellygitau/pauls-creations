// loader animation

window.addEventListener('load', function() {
    const loader = document.getElementById('loader');
    const content = document.getElementById('content');
    
    setTimeout(() => {
        loader.style.display = 'none';
        content.style.display = 'block';
    }, 1000); // Match the transition duration

});

//modalcontrol

const openButton = document.querySelector("[data-open-modal]");
const closeButton = document.querySelector("[data-close-modal]");
const modal = document.querySelector("[data-modal]");

openButton.addEventListener("click", () => {
  modal.showModal();
});

closeButton.addEventListener("click", () => {
  modal.close();
});

modal.addEventListener("click", (e) => {
  const dialogDimensions = modal.getBoundingClientRect();
  if (
    e.clientX < dialogDimensions.left ||
    e.clientX > dialogDimensions.right ||
    e.clientY < dialogDimensions.top ||
    e.clientY > dialogDimensions.bottom
  ) {
    modal.close();
  }
});