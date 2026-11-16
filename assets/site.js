for (const year of document.querySelectorAll(".current-year")) {
  year.textContent = String(new Date().getFullYear());
}

const menuButton = document.querySelector(".menu-button");
const mainNav = document.querySelector("#main-nav");
const setMenu = (open) => {
  if (open) {
    const hd = document.querySelector(".site-header");
    const hit = document.elementsFromPoint(window.innerWidth / 2, 36).find((e) => !hd.contains(e));
    let el = hit ? (hit.closest("section, footer") || hit) : document.body;
    let rgb = [246, 243, 239];
    while (el) { const m = getComputedStyle(el).backgroundColor.match(/rgba?\(([^)]+)\)/); if (m) { const v = m[1].split(",").map(parseFloat); if (v.length < 4 || v[3] > 0.5) { rgb = v.slice(0, 3); break; } } el = el.parentElement; }
    const light = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255 > 0.6;
    const fg = light ? "29, 24, 20" : "255, 255, 255";
    hd.style.setProperty("--menu-bg", "rgba(" + rgb.join(",") + ", .95)");
    hd.style.setProperty("--menu-fg", "rgb(" + fg + ")");
    hd.style.setProperty("--menu-line", "rgba(" + fg + ", .3)");
    const r = menuButton.getBoundingClientRect();
    mainNav.style.setProperty("--mx", Math.round(r.left + r.width / 2) + "px");
    mainNav.style.setProperty("--my", Math.round(r.top + r.height / 2) + "px");
  }
  mainNav.classList.toggle("open", open);
  document.body.classList.toggle("menu-open", open);
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "閉じる" : "メニュー");
  window.dispatchEvent(new Event("resize"));
};
if (menuButton && mainNav) {
  menuButton.addEventListener("click", () => setMenu(!mainNav.classList.contains("open")));
  mainNav.addEventListener("click", (event) => { if (event.target.closest("a")) setMenu(false); });
  window.addEventListener("keydown", (event) => { if (event.key === "Escape") setMenu(false); });
}

const header = document.querySelector(".site-header");
const cta = document.querySelector(".mobile-cta");
const hero = document.querySelector(".hero");
const markScrolled = () => {
  if (header) header.classList.toggle("scrolled", window.scrollY > 24);
  if (cta) cta.classList.toggle("show", window.scrollY > (hero ? hero.offsetHeight - 200 : 200));
};
window.addEventListener("scroll", markScrolled, { passive: true });
markScrolled();


// ヘッダーを、その下にある背景色に合わせて変える
if (header) {
  const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(",").map((x) => parseFloat(x)); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
  const bgAt = (el) => { while (el) { const c = parse(getComputedStyle(el).backgroundColor); if (c && c.a > 0.5) return c; el = el.parentElement; } return { r: 246, g: 243, b: 239, a: 1 }; };
  const colorAt = (y) => {
    const hit = document.elementsFromPoint(window.innerWidth / 2, y).find((e) => !header.contains(e));
    const base = hit ? (hit.closest("section, footer") || hit) : document.body;
    const c = bgAt(base);
    return `rgb(${c.r}, ${c.g}, ${c.b})`;
  };
  const lumOf = (css) => { const c = parse(css); return (0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b) / 255; };
  const inkOf = (css) => (lumOf(css) > 0.6 ? "#1d1814" : "#ffffff");
  const invOf = (ink) => (ink === "#ffffff" ? "#1d1814" : "#ffffff");
  const layerA = header.querySelector(".header-inner");
  const layerB = layerA.cloneNode(true);
  layerB.removeAttribute("id");
  layerB.querySelectorAll("[id]").forEach((e) => e.removeAttribute("id"));
  layerB.querySelectorAll("a, button").forEach((e) => e.setAttribute("tabindex", "-1"));
  layerB.setAttribute("aria-hidden", "true");
  layerB.classList.add("header-clone");
  layerB.style.display = "none";
  layerA.after(layerB);
  const paint = (el, ink) => { el.style.color = ink; el.style.setProperty("--hfg", ink); el.style.setProperty("--hinv", invOf(ink)); };
  let ticking = false;
  const run = () => {
    ticking = false;
    const h = Math.round(header.getBoundingClientRect().height);
    const top = colorAt(1);
    const bottom = colorAt(h - 1);
    const menuOpen = document.body.classList.contains("menu-open");
    if (top === bottom || menuOpen) {
      header.style.setProperty("--hbg", top);
      layerA.style.clipPath = "";
      layerB.style.display = "none";
      paint(layerA, inkOf(top));
      return;
    }
    let lo = 1, hi = h - 1;
    while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (colorAt(mid) === top) lo = mid; else hi = mid; }
    header.style.setProperty("--hbg", `linear-gradient(to bottom, ${top} ${hi}px, ${bottom} ${hi}px)`);
    layerA.style.clipPath = `inset(0 0 ${h - hi}px 0)`;
    layerB.style.clipPath = `inset(${hi}px 0 0 0)`;
    layerB.style.display = "";
    paint(layerA, inkOf(top));
    paint(layerB, inkOf(bottom));
  };
  const syncHeader = () => { if (!ticking) { ticking = true; requestAnimationFrame(run); } };
  window.addEventListener("scroll", syncHeader, { passive: true });
  window.addEventListener("resize", syncHeader);
  window.addEventListener("load", syncHeader);
  run();
}

const contactForm = document.querySelector("#contact-form");
if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(contactForm);
    const lines = [
      `お名前：${formData.get("name")}`,
      `メールアドレス：${formData.get("email")}`,
      "",
      "お問い合わせ内容：",
      formData.get("message"),
    ];
    const subject = encodeURIComponent("お問い合わせ");
    const body = encodeURIComponent(lines.join("\n"));
    window.location.href = `mailto:info@example.com?subject=${subject}&body=${body}`;
  });
}
