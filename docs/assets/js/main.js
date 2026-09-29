/* AIC × Fondazione di Sardegna — prototipo: comportamenti minimi, nessuna dipendenza. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* Menu mobile */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    var label = toggle.querySelector(".visually-hidden");
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      if (label) label.textContent = open ? "Chiudi il menu" : "Apri il menu";
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  /* Voce di menu attiva in base alla sezione visibile */
  var links = Array.prototype.slice.call(document.querySelectorAll('.main-nav a[href^="#"]'));
  // Le schede dei singoli progetti appartengono alla voce "Le attività".
  var groups = { progetto: "progetto", progetti: "progetti", "in-fuga-dal-glutine": "progetti", qa: "progetti",
    "corsi-cucina": "progetti", dirette: "progetti", associazioni: "associazioni" };
  if ("IntersectionObserver" in window && links.length) {
    var setActive = function (id) {
      links.forEach(function (a) {
        if (a.getAttribute("href") === "#" + id) a.setAttribute("aria-current", "true");
        else a.removeAttribute("aria-current");
      });
    };
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setActive(groups[entry.target.id]);
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(groups).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    var hero = document.querySelector(".hero");
    if (hero) new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) setActive(null);
    }, { rootMargin: "-45% 0px -50% 0px" }).observe(hero);
  }

  /* Stato degli appuntamenti: "Svolto" / "In programma" in base alla data odierna */
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  Array.prototype.forEach.call(document.querySelectorAll(".event[data-date]"), function (el) {
    var parts = el.getAttribute("data-date").split("-");
    var date = new Date(+parts[0], +parts[1] - 1, +parts[2]);
    var past = date < today;
    el.classList.add(past ? "is-past" : "is-upcoming");
    var badge = document.createElement("span");
    badge.className = "event__status";
    badge.textContent = past ? "Svolto" : "In programma";
    var host = el.querySelector(".event__body") || el;
    host.appendChild(badge);
  });

  /* Anno corrente nel footer */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = today.getFullYear();
})();
