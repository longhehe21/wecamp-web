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

// meal.html swiper
document.addEventListener("DOMContentLoaded", function () {
  const swiper = new Swiper(".comboSwiper", {
    slidesPerView: 1,
    loop: true,
    speed: 800,
    centeredSlides: true,

    // TỰ ĐỘNG CHẠY 4 GIÂY
    autoplay: {
      delay: 4000,
      disableOnInteraction: false, // Vẫn chạy dù đã click
    },

    // CHẤM CÓ THỂ BẤM
    pagination: {
      el: ".combo-pagination",
      clickable: false,
      type: "bullets", // Đảm bảo dùng chấm tròn
    },

    // TẮT KÉO
    allowTouchMove: false,
    simulateTouch: false,
    grabCursor: false,

    // FIX LOOP MƯỢT
    loopAdditionalSlides: 1,
  });

  // ẨN CHẤM NẾU CHỈ 1 SLIDE
  const slideCount = document.querySelectorAll(
    ".comboSwiper .swiper-slide:not(.swiper-slide-duplicate)"
  ).length;
  if (slideCount <= 1) {
    document.querySelector(".swiper-controls").classList.add("single-slide");
  }
});

// coffee.html
document.addEventListener("DOMContentLoaded", function () {
  // Khởi tạo Isotope
  var grid = document.querySelector(".isotope-container");
  if (grid) {
    var iso = new Isotope(grid, {
      itemSelector: ".isotope-item",
      layoutMode: "masonry",
    });

    // Lọc khi click tab
    var filters = document.querySelectorAll(".isotope-filters li");
    filters.forEach(function (filter) {
      filter.addEventListener("click", function () {
        filters.forEach((f) => f.classList.remove("filter-active"));
        this.classList.add("filter-active");
        var filterValue = this.getAttribute("data-filter");
        iso.arrange({ filter: filterValue });
      });
    });
  }
});

// base.html
function toggleFAB() {
  const fab = document.querySelector(".floating-action-buttons");
  fab.classList.toggle("active");

  const icon = document.querySelector(".fab-toggle .toggle-icon");
  icon.classList.toggle("bi-plus");
  icon.classList.toggle("bi-x");
}

// TỰ ĐỘNG MỞ NÚT KHI LOAD XONG
document.addEventListener("DOMContentLoaded", function () {
  // Tắt preloader
  const preloader = document.getElementById("preloader");
  if (preloader) {
    setTimeout(() => preloader.remove(), 500);
  }

  // Cuộn mượt đến form nếu có hash
  if (window.location.hash === "#booking-form-wrapper") {
    setTimeout(() => {
      const el = document.querySelector("#booking-form-wrapper");
      if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 800);
  }

  // MỞ NÚT TỰ ĐỘNG SAU 1 GIÂY (TÙY CHỌN)
  setTimeout(() => {
    document.querySelector(".floating-action-buttons").classList.add("active");
    document.querySelector(".toggle-icon").classList.replace("bi-plus", "bi-x");
  }, 1000);
});

document.addEventListener("DOMContentLoaded", function () {
  const consultBtn = document.querySelector(".auto-tooltip");
  let intervalId = null;
  let isHovered = false;

  // Hàm kích hoạt tooltip
  function triggerTooltip() {
    if (!isHovered) {
      consultBtn.classList.add("force-show");
      setTimeout(() => {
        consultBtn.classList.remove("force-show");
      }, 4000); // Hiện 2s
    }
  }

  // Bắt đầu lặp mỗi 3s
  intervalId = setInterval(triggerTooltip, 10000);

  // Dừng khi hover
  consultBtn.addEventListener("mouseenter", () => {
    isHovered = true;
  });

  consultBtn.addEventListener("mouseleave", () => {
    isHovered = false;
  });

  // Dừng hoàn toàn khi click
  consultBtn.addEventListener("click", () => {
    clearInterval(intervalId);
  });
});
