// loader animation

window.addEventListener('load', function() {
    const loader = document.getElementById('loader');
    const content = document.getElementById('content');
    
    setTimeout(() => {
        loader.style.display = 'none';
        content.style.display = 'block';
    }, 1000); // Match the transition duration

});



// carousel-1

const carousel = document.querySelector(".carousel1"),
firstImg = carousel.querySelector("img")[0],
arrowIcons = document.querySelectorAll(".wrapper-1 i");
let isDragStart = false, isDragging = false, prevPageX, prevScrollLeft, positionDiff;
const showHideIcons = () => {
    // showing and hiding prev/next icon according to carousel scroll left value
    let scrollWidth = carousel.scrollWidth - carousel.clientWidth; // getting max scrollable width
    arrowIcons[0].style.display = carousel.scrollLeft == 0 ? "none" : "block";
    arrowIcons[1].style.display = carousel.scrollLeft == scrollWidth ? "none" : "block";
}
arrowIcons.forEach(icon => {
    icon.addEventListener("click", () => {
        let firstImgWidth = firstImg.clientWidth + 14; // getting first img width & adding 14 margin value
        // if clicked icon is left, reduce width value from the carousel scroll left else add to it
        carousel.scrollLeft += icon.id == "left" ? -firstImgWidth : firstImgWidth;
        setTimeout(() => showHideIcons(), 60); // calling showHideIcons after 60ms
    });
});
const autoSlide = () => {
    // if there is no image left to scroll then return from here
    if(carousel.scrollLeft - (carousel.scrollWidth - carousel.clientWidth) > -1 || carousel.scrollLeft <= 0) return;
    positionDiff = Math.abs(positionDiff); // making positionDiff value to positive
    let firstImgWidth = firstImg.clientWidth + 14;
    // getting difference value that needs to add or reduce from carousel left to take middle img center
    let valDifference = firstImgWidth - positionDiff;
    if(carousel.scrollLeft > prevScrollLeft) { // if user is scrolling to the right
        return carousel.scrollLeft += positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
    }
    // if user is scrolling to the left
    carousel.scrollLeft -= positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
}
const dragStart = (e) => {
    // updatating global variables value on mouse down event
    isDragStart = true;
    prevPageX = e.pageX || e.touches[0].pageX;
    prevScrollLeft = carousel.scrollLeft;
}
const dragging = (e) => {
    // scrolling images/carousel to left according to mouse pointer
    if(!isDragStart) return;
    e.preventDefault();
    isDragging = true;
    carousel.classList.add("dragging");
    positionDiff = (e.pageX || e.touches[0].pageX) - prevPageX;
    carousel.scrollLeft = prevScrollLeft - positionDiff;
    showHideIcons();
}
const dragStop = () => {
    isDragStart = false;
    carousel.classList.remove("dragging");
    if(!isDragging) return;
    isDragging = false;
    autoSlide();
}
carousel.addEventListener("mousedown", dragStart);
carousel.addEventListener("touchstart", dragStart);
document.addEventListener("mousemove", dragging);
carousel.addEventListener("touchmove", dragging);
document.addEventListener("mouseup", dragStop);
carousel.addEventListener("touchend", dragStop);


// contacts resposive

const openIcon = document.querySelector("[data-toggle-open]")
const closeIcon = document.querySelector("[data-toggle-close]")
const open = document.querySelector("[data-toggle]")
const close = document.getElementsByClassName("contacts")
openIcon.addEventListener("click", () => {
    open.style.zIndex = "1000";
    open.style.opacity = "1";
})

closeIcon.addEventListener("click", () => {
    open.style.zIndex = "10";
    open.style.opacity = "0";
})


var swiper = new Swiper(".mySwiper", {
    slidesPerView: 4,
    spaceBetween: 20,
    keyboard: {
    enabled: true,
    },
    navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
    },
    breakpoints: {
    // when window width is <= 768px
    500: {
        slidesPerView: 2,
        spaceBetween: 7.5,
    },
    // when window width is <= 992px
    //750: {
        //slidesPerView: 2,
        //spaceBetween: 15,
    //},
    750: {
        slidesPerView: 3,
        spaceBetween: 15,
    },
    // when window width is <= 1200px
    1200: {
        slidesPerView: 4,
        spaceBetween: 20,
    },
    },
});

const filterList = document.querySelector('.filter');
const filterButton = filterList.querySelectorAll('.filter-button');
const elements = document.querySelectorAll('.element');

filterButton.forEach((button) => {
    button.addEventListener('click', (e) => {
        const filter = e.target.getAttribute('data-filter')

        if(!document.startViewTransition) {
            updateActiveButton(e.target);
            filterCustom(filter);
        }else {
            document.startViewTransition(() => {
                updateActiveButton(e.target);
                filterCustom(filter);
            })
        }
    })
})

function updateActiveButton(newButton) {
    filterList.querySelector(".active").classList.remove("active");
    newButton.classList.add("active");
  }

function filterCustom(elementFilter) {
    elements.forEach((element) => {
        const elementCategory = element.getAttribute('data-category')

    if (elementFilter ==='all' || elementFilter === elementCategory) {
        element.removeAttribute('hidden')
    }else {
        element.setAttribute('hidden', '')
    }
    })
}

document.getElementById("mySelect").addEventListener("change", function() {
    var selectElement = this;
    var placeholderOption = selectElement.querySelector('option[value=""]');
    if (placeholderOption) {
      placeholderOption.remove();
    }
  });

  function renderValue() {
    const buttonValue = document.querySelector('.custom-button').textContent;
    const valueContainer = document.querySelector('.value-container');
    valueContainer.textContent = buttonValue;
  }

//   const filterList = document.querySelector('.filter');
//   const filterButton = filterList.querySelectorAll('.filter-button');
//   const elements = document.querySelectorAll('.element');
  
//   filterButton.forEach((button) => {
//       button.addEventListener('click', (e) => {
//           const filter = e.target.getAttribute('data-filter')
  
//           if(!document.startViewTransition) {
//               updateActiveButton(e.target);
//               filterCustom(filter);
//           }else {
//               document.startViewTransition(() => {
//                   updateActiveButton(e.target);
//                   filterCustom(filter);
//               })
//           }
//       })
//   })
  
//   function updateActiveButton(newButton) {
//       filterList.querySelector(".active").classList.remove("active");
//       newButton.classList.add("active");
//     }
  
//   function filterCustom(elementFilter) {
//       elements.forEach((element) => {
//           const elementCategory = element.getAttribute('data-category')
  
//       if (elementFilter ==='all' || elementFilter === elementCategory) {
//           element.removeAttribute('hidden')
//       }else {
//           element.setAttribute('hidden', '')
//       }
//       })
//   }

