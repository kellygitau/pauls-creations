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