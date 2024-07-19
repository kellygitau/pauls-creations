function renderValue() {
    const buttonValue = document.querySelector('.custom-button').textContent;
    const valueContainer = document.querySelector('.value-container');
    valueContainer.textContent = buttonValue;
  }  