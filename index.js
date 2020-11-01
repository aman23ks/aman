function splitScroll() {
  const controller = new ScrollMagic.Controller();

  new ScrollMagic.Scene({
    duration: "760.5%",
    triggerElement: ".info-title",
    triggerHook: 0,
  })
    .setPin(".info-title")
    .addTo(controller);
}
splitScroll();
