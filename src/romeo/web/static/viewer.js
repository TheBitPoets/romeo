"use strict";

const canvas = document.querySelector("#arena");
const canvasWrap = document.querySelector("#canvas-wrap");
const context = canvas.getContext("2d");
const emptyState = document.querySelector("#empty-state");
const connectionDot = document.querySelector("#connection-dot");
const connectionStatus = document.querySelector("#connection-status");
const actionStatus = document.querySelector("#action-status");

const fields = {
  scenario: document.querySelector("#scenario-id"),
  running: document.querySelector("#running"),
  clock: document.querySelector("#clock"),
  left: document.querySelector("#motor-left"),
  right: document.querySelector("#motor-right"),
  pan: document.querySelector("#camera-pan"),
  tilt: document.querySelector("#camera-tilt"),
  led: document.querySelector("#led-color"),
  collisions: document.querySelector("#collisions"),
};

let simulationState = null;
let reconnectDelay = 500;
let reconnectTimer = null;
let controlSocket = null;
let controlReconnectDelay = 500;
let controlReconnectTimer = null;
let heartbeatTimer = null;
let activeMovement = null;

function finiteNumber(value, fallback = 0) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function formatNumber(value, digits = 2) {
  return finiteNumber(value).toLocaleString("it-IT", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function setConnection(online, text) {
  connectionDot.classList.toggle("is-online", online);
  connectionStatus.textContent = text;
}

function stateFromMessage(message) {
  if (message && typeof message === "object" && message.state) return message.state;
  return message;
}

function connect() {
  window.clearTimeout(reconnectTimer);
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const socket = new WebSocket(`${protocol}//${window.location.host}/ws/state`);
  setConnection(false, "Connessione…");

  socket.addEventListener("open", () => {
    reconnectDelay = 500;
    setConnection(true, "Connesso");
  });

  socket.addEventListener("message", (event) => {
    try {
      const nextState = stateFromMessage(JSON.parse(event.data));
      if (!nextState || typeof nextState !== "object") throw new Error("stato non valido");
      simulationState = nextState;
      emptyState.hidden = true;
      updateTelemetry(nextState);
      draw();
    } catch (error) {
      console.warn("Messaggio WebSocket ignorato:", error);
    }
  });

  socket.addEventListener("close", () => {
    setConnection(false, "Disconnesso · nuovo tentativo…");
    reconnectTimer = window.setTimeout(connect, reconnectDelay);
    reconnectDelay = Math.min(reconnectDelay * 2, 8000);
  });

  socket.addEventListener("error", () => socket.close());
}

function connectControl() {
  window.clearTimeout(controlReconnectTimer);
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  controlSocket = new WebSocket(`${protocol}//${window.location.host}/ws/control`);

  controlSocket.addEventListener("open", () => {
    controlReconnectDelay = 500;
  });
  controlSocket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "error") {
      actionStatus.classList.add("is-error");
      actionStatus.textContent = message.detail || "Comando di guida non valido.";
    }
  });
  controlSocket.addEventListener("close", () => {
    stopHeartbeat();
    controlReconnectTimer = window.setTimeout(connectControl, controlReconnectDelay);
    controlReconnectDelay = Math.min(controlReconnectDelay * 2, 8000);
  });
  controlSocket.addEventListener("error", () => controlSocket.close());
}

function sendControl(payload) {
  if (!controlSocket || controlSocket.readyState !== WebSocket.OPEN) {
    actionStatus.classList.add("is-error");
    actionStatus.textContent = "Controllo non ancora connesso.";
    return false;
  }
  controlSocket.send(JSON.stringify(payload));
  return true;
}

function selectedSpeed() {
  return finiteNumber(document.querySelector("#drive-speed").value, 0.5);
}

function startMovement(command) {
  if (activeMovement === command) return;
  stopHeartbeat();
  if (!sendControl({ command, speed: selectedSpeed() })) return;
  activeMovement = command;
  heartbeatTimer = window.setInterval(() => sendControl({ command: "ping" }), 250);
}

function stopHeartbeat() {
  window.clearInterval(heartbeatTimer);
  heartbeatTimer = null;
  activeMovement = null;
}

function stopMovement() {
  stopHeartbeat();
  sendControl({ command: "stop" });
}

function updateTelemetry(state) {
  const motors = state.motors || {};
  const camera = state.camera || {};
  const led = state.led || {};
  fields.scenario.textContent = state.scenario_id || state.scenario?.id || "—";
  fields.running.textContent = state.running ? "In movimento" : "Fermo";
  fields.clock.textContent = `${formatNumber(state.time)} s`;
  fields.left.textContent = formatNumber(motors.left);
  fields.right.textContent = formatNumber(motors.right);
  fields.pan.textContent = `${formatNumber(camera.pan, 0)}°`;
  fields.tilt.textContent = `${formatNumber(camera.tilt, 0)}°`;
  fields.led.textContent = `${Math.round(finiteNumber(led.red))}, ${Math.round(finiteNumber(led.green))}, ${Math.round(finiteNumber(led.blue))}`;
  fields.collisions.textContent = String(Math.max(0, finiteNumber(state.collisions)));
}

function resizeCanvas() {
  const rect = canvasWrap.getBoundingClientRect();
  const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(1, Math.round(rect.width * pixelRatio));
  const height = Math.max(1, Math.round(rect.height * pixelRatio));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
    canvas.style.width = `${rect.width}px`;
    canvas.style.height = `${rect.height}px`;
  }
  draw();
}

function createProjection(world) {
  const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
  const padding = 28 * pixelRatio;
  const width = Math.max(0.01, finiteNumber(world.width, 4));
  const height = Math.max(0.01, finiteNumber(world.height, 3));
  const scale = Math.max(0.01, Math.min(
    (canvas.width - padding * 2) / width,
    (canvas.height - padding * 2) / height,
  ));
  const arenaWidth = width * scale;
  const arenaHeight = height * scale;
  const originX = (canvas.width - arenaWidth) / 2;
  const originY = (canvas.height - arenaHeight) / 2;

  return {
    scale,
    width,
    height,
    originX,
    originY,
    x: (value) => originX + finiteNumber(value) * scale,
    y: (value) => originY + arenaHeight - finiteNumber(value) * scale,
  };
}

function drawGrid(projection) {
  context.fillStyle = "#0b1d19";
  context.fillRect(
    projection.originX,
    projection.originY,
    projection.width * projection.scale,
    projection.height * projection.scale,
  );

  context.save();
  context.strokeStyle = "rgba(125, 170, 161, 0.12)";
  context.lineWidth = 1;
  const step = projection.scale >= 100 ? 0.5 : 1;
  for (let x = 0; x <= projection.width + 1e-9; x += step) {
    context.beginPath();
    context.moveTo(projection.x(x), projection.y(0));
    context.lineTo(projection.x(x), projection.y(projection.height));
    context.stroke();
  }
  for (let y = 0; y <= projection.height + 1e-9; y += step) {
    context.beginPath();
    context.moveTo(projection.x(0), projection.y(y));
    context.lineTo(projection.x(projection.width), projection.y(y));
    context.stroke();
  }
  context.strokeStyle = "#52716a";
  context.lineWidth = 2;
  context.strokeRect(
    projection.originX,
    projection.originY,
    projection.width * projection.scale,
    projection.height * projection.scale,
  );
  context.restore();
}

function drawObstacles(obstacles, projection) {
  context.save();
  for (const obstacle of obstacles || []) {
    const x = projection.x(obstacle.x);
    const y = projection.y(finiteNumber(obstacle.y) + finiteNumber(obstacle.height));
    const width = finiteNumber(obstacle.width) * projection.scale;
    const height = finiteNumber(obstacle.height) * projection.scale;
    context.fillStyle = "#725b55";
    context.strokeStyle = "#aa8378";
    context.lineWidth = 2;
    context.fillRect(x, y, width, height);
    context.strokeRect(x, y, width, height);
  }
  context.restore();
}

function drawTrajectory(trajectory, projection) {
  if (!Array.isArray(trajectory) || trajectory.length < 2) return;
  context.save();
  context.beginPath();
  context.moveTo(projection.x(trajectory[0].x), projection.y(trajectory[0].y));
  for (const point of trajectory.slice(1)) {
    context.lineTo(projection.x(point.x), projection.y(point.y));
  }
  context.strokeStyle = "#5ec8ff";
  context.lineWidth = Math.max(2, projection.scale * 0.025);
  context.lineCap = "round";
  context.lineJoin = "round";
  context.stroke();
  context.restore();
}

function collectMarkers(state) {
  const world = state.world || {};
  const values = [state.targets, state.checkpoints, world.targets, world.checkpoints];
  const markers = values.flatMap((value) => Array.isArray(value) ? value : []);
  for (const value of [state.target, world.target]) {
    if (value && typeof value === "object") markers.push(value);
  }
  return markers;
}

function drawMarkers(markers, projection) {
  context.save();
  markers.forEach((marker, index) => {
    if (!Number.isFinite(Number(marker.x)) || !Number.isFinite(Number(marker.y))) return;
    const x = projection.x(marker.x);
    const y = projection.y(marker.y);
    const radius = Math.max(7, finiteNumber(marker.radius, 0.1) * projection.scale);
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2);
    context.fillStyle = "rgba(255, 207, 91, 0.1)";
    context.fill();
    context.strokeStyle = "#ffcf5b";
    context.lineWidth = 2;
    context.setLineDash([5, 4]);
    context.stroke();
    context.setLineDash([]);
    context.fillStyle = "#ffdf8e";
    context.font = `${Math.max(11, radius * 0.75)}px system-ui`;
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(String(marker.label || marker.name || index + 1), x, y);
  });
  context.restore();
}

function drawRobot(state, projection) {
  const pose = state.pose || {};
  const world = state.world || {};
  const radiusMetres = finiteNumber(state.robot?.radius ?? world.robot_radius, 0.12);
  const radius = Math.max(8, radiusMetres * projection.scale);
  const x = projection.x(pose.x);
  const y = projection.y(pose.y);
  const heading = finiteNumber(pose.heading);
  const led = state.led || {};
  const ledColor = [led.red, led.green, led.blue]
    .map((value) => Math.max(0, Math.min(255, Math.round(finiteNumber(value)))))
    .join(", ");

  context.save();
  context.shadowColor = "rgba(71, 224, 174, 0.3)";
  context.shadowBlur = 14;
  context.beginPath();
  context.arc(x, y, radius, 0, Math.PI * 2);
  context.fillStyle = "#47e0ae";
  context.fill();
  context.shadowBlur = 0;
  context.strokeStyle = "#cffff0";
  context.lineWidth = 2;
  context.stroke();

  const noseX = x + Math.cos(heading) * radius * 1.25;
  const noseY = y - Math.sin(heading) * radius * 1.25;
  context.beginPath();
  context.moveTo(x, y);
  context.lineTo(noseX, noseY);
  context.strokeStyle = "#06241b";
  context.lineWidth = Math.max(3, radius * 0.2);
  context.lineCap = "round";
  context.stroke();

  context.beginPath();
  context.arc(x, y, Math.max(3, radius * 0.22), 0, Math.PI * 2);
  context.fillStyle = `rgb(${ledColor})`;
  context.fill();
  context.strokeStyle = "#ffffff";
  context.lineWidth = 1;
  context.stroke();
  context.restore();
}

function draw() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  if (!simulationState) return;
  const world = simulationState.world || {};
  const projection = createProjection(world);
  drawGrid(projection);
  drawTrajectory(simulationState.trajectory, projection);
  drawObstacles(world.obstacles, projection);
  drawMarkers(collectMarkers(simulationState), projection);
  drawRobot(simulationState, projection);
}

async function simulationAction(action, button) {
  const buttons = document.querySelectorAll("button");
  buttons.forEach((item) => { item.disabled = true; });
  actionStatus.classList.remove("is-error");
  actionStatus.textContent = `${button.textContent}…`;
  try {
    const response = await fetch(`/api/simulation/${action}`, { method: "POST" });
    if (!response.ok) throw new Error(`errore HTTP ${response.status}`);
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const body = stateFromMessage(await response.json());
      if (body && body.world && body.pose) {
        simulationState = body;
        emptyState.hidden = true;
        updateTelemetry(body);
        draw();
      }
    }
    actionStatus.textContent = "Comando eseguito.";
  } catch (error) {
    actionStatus.classList.add("is-error");
    actionStatus.textContent = `Comando non riuscito: ${error.message}`;
  } finally {
    buttons.forEach((item) => { item.disabled = false; });
  }
}

document.querySelector("#start-button").addEventListener("click", (event) => {
  simulationAction("start", event.currentTarget);
});
document.querySelector("#stop-button").addEventListener("click", (event) => {
  simulationAction("stop", event.currentTarget);
});
document.querySelector("#reset-button").addEventListener("click", (event) => {
  simulationAction("reset", event.currentTarget);
});

for (const button of document.querySelectorAll(".drive-button")) {
  const command = button.dataset.command;
  if (command === "stop") {
    button.addEventListener("click", stopMovement);
    continue;
  }
  button.addEventListener("pointerdown", () => startMovement(command));
  button.addEventListener("pointerup", stopMovement);
  button.addEventListener("pointercancel", stopMovement);
  button.addEventListener("pointerleave", () => {
    if (activeMovement === command) stopMovement();
  });
}

const keyboardCommands = { KeyW: "forward", KeyA: "left", KeyS: "backward", KeyD: "right" };
window.addEventListener("keydown", (event) => {
  if (event.target instanceof HTMLInputElement && event.target.type !== "range") return;
  if (event.code === "Space") {
    event.preventDefault();
    stopMovement();
    return;
  }
  const command = keyboardCommands[event.code];
  if (command) {
    event.preventDefault();
    startMovement(command);
  }
});
window.addEventListener("keyup", (event) => {
  if (keyboardCommands[event.code] && activeMovement === keyboardCommands[event.code]) {
    stopMovement();
  }
});
window.addEventListener("blur", stopMovement);

const speedInput = document.querySelector("#drive-speed");
speedInput.addEventListener("input", () => {
  document.querySelector("#drive-speed-value").textContent = formatNumber(speedInput.value);
});

const panInput = document.querySelector("#camera-pan-control");
const tiltInput = document.querySelector("#camera-tilt-control");
function updateCameraPosition() {
  document.querySelector("#camera-pan-value").textContent = `${formatNumber(panInput.value, 0)}°`;
  document.querySelector("#camera-tilt-value").textContent = `${formatNumber(tiltInput.value, 0)}°`;
  sendControl({ command: "look", pan: finiteNumber(panInput.value), tilt: finiteNumber(tiltInput.value) });
}
panInput.addEventListener("change", updateCameraPosition);
tiltInput.addEventListener("change", updateCameraPosition);

async function initializeCameraPreview() {
  try {
    const response = await fetch("/api/info");
    const info = await response.json();
    if (!info.camera_available) return;
    const stream = document.querySelector("#camera-stream");
    stream.src = "/api/camera/stream";
    stream.hidden = false;
    document.querySelector("#camera-unavailable").hidden = true;
  } catch (error) {
    console.warn("Anteprima camera non disponibile:", error);
  }
}

if ("ResizeObserver" in window) {
  new ResizeObserver(resizeCanvas).observe(canvasWrap);
} else {
  window.addEventListener("resize", resizeCanvas);
}

resizeCanvas();
connect();
connectControl();
initializeCameraPreview();
