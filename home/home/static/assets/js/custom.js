document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".clamp-3-lines").forEach((link) => {
    const text = link.textContent;
    const maxLines = 3;
    const lineHeight = 1.4;
    const maxHeight = maxLines * lineHeight * 16;

    const temp = document.createElement("div");
    temp.style.position = "absolute";
    temp.style.visibility = "hidden";
    temp.style.width = link.offsetWidth + "px";
    temp.style.font = window.getComputedStyle(link).font;
    temp.innerHTML = text;
    document.body.appendChild(temp);

    if (temp.offsetHeight > maxHeight) {
      link.title = text; // Tooltip khi hover
    }
    document.body.removeChild(temp);
  });
});
