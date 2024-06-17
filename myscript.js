// Feature 1
function collectTextNodes(element, texts) {
  for (const el of element.childNodes) {
    if (
      el.nodeType === Node.TEXT_NODE &&
      el.nodeValue.trim() !== ""
    ) {
      texts.push({ text: el.nodeValue.trim(), element: el.parentElement });
    } else if (
      el.nodeType === Node.ELEMENT_NODE &&
      el.tagName.toUpperCase() !== "SCRIPT" &&
      el.tagName.toUpperCase() !== "STYLE"
    ) {
      collectTextNodes(el, texts);
    }
  }
}

const allTexts = [];
const targetDiv = document.getElementById("bodyContentOuter"); 

if (targetDiv) {
  collectTextNodes(targetDiv, allTexts);
} else {
  console.error('Element with id "1" not found.');
}

// collectTextNodes(document.body, allTexts);

highlightLimitedTimeDeal(allTexts);

console.log(allTexts);

function highlightLimitedTimeDeal(textarr) {
  fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ txt: allTexts }),
})

.then(response => response.json())
.then(data => {
  const dat=data.result;
  for(var i=0;i<25;i++){
    allTexts[i]['element'].innerText = dat[i]['text'];
    allTexts[i]['element'].style.border = "1px solid red";

  }
})
.catch(error => console.error('Error:', error));
}
























