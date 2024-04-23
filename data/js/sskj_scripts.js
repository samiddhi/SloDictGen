document.addEventListener("DOMContentLoaded", function () {
  var examples = document.querySelectorAll('[data-group="example"]');
  examples.forEach(function (example) {
    var nextSibling = example.parentNode.nextSibling;
    if (
      nextSibling &&
      nextSibling.nodeType === Node.TEXT_NODE &&
      nextSibling.textContent.trim() === ";"
    ) {
      nextSibling.textContent = nextSibling.textContent.replace(";", "");
    }
  });
});
function removeDiacriticsExceptCarons(text) {
  const carons = "čžšČŽŠ";
  let result = "";
  for (let i = 0; i < text.length; i++) {
    let char = text[i];
    if (carons.includes(char)) {
      result += char;
    } else {
      char = char.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      result += char;
    }
  }
  return result;
}
document.addEventListener("DOMContentLoaded", () => {
  // Select all <a> elements within <span class="font_xlarge">
  // and all elements with class "color_orange"
  const selectors = "span.font_xlarge a, .color_orange";
  const elements = document.querySelectorAll(selectors);
  elements.forEach((element) => {
    // Process the text content of each element
    const originalText = element.textContent;
    const cleanedText = removeDiacriticsExceptCarons(originalText);
    // Update the text content of the element
    element.textContent = cleanedText;
  });
});
