function monitorEvents(element) {
  const events = Object.getOwnPropertyNames(element)
    .filter(prop => prop.startsWith("on"))
    .filter(event => event !== "ondevicemotion")
    .filter(event => event !== "ondeviceorientation")
    .filter(event => event !== "onmouseout")
    .filter(event => event !== "onmouseover")
    .filter(event => event !== "onmousemove")
    .filter(event => event !== "onmousedown")
    .filter(event => event !== "onpointerup")
    .filter(event => event !== "onpointerover")
    .filter(event => event !== "onpointerdown")
    .filter(event => event !== "onlostpointercapture")
    .filter(event => event !== "ontouchend")
    .filter(event => event !== "ongotpointercapture")
    .filter(event => event !== "onpointerout")
    .filter(event => event !== "ondeviceorientationabsolute");

  for (const event of events) {
    element.addEventListener(event.slice(2), e => console.log(event, e));
  }
}

monitorEvents(window);

// 

monitorEvents(window, { events: ["ontouchstart", "onselectstart"] });


window.addEventListener("ontouchstart", e => console.log("ontouchstart", e));
window.addEventListener("onselectstart", e => console.log("onselectstart", e));

window.addEventListener("selectstart", () => {
  console.log("Selection started");
});