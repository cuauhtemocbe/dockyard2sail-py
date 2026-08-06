function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function runPipelineLoop() {
  const steps = Array.from(document.querySelectorAll(".step"));
  if (steps.length === 0) return;

  while (true) {
    steps.forEach((step) => step.classList.remove("visible"));
    await delay(500);

    for (const step of steps) {
      step.classList.add("visible");
      await delay(900);
    }

    await delay(2000);
  }
}

async function pollHealth() {
  const dot = document.getElementById("health-dot");
  const text = document.getElementById("health-text");
  if (!dot || !text) return;

  try {
    const response = await fetch("/health");
    const data = await response.json();

    if (response.ok && data.status === "ok") {
      dot.classList.remove("error");
      dot.classList.add("ok");
      text.textContent = "operativo";
    } else {
      throw new Error("unhealthy");
    }
  } catch {
    dot.classList.remove("ok");
    dot.classList.add("error");
    text.textContent = "no disponible";
  }
}

function setupHelloForm() {
  const form = document.getElementById("hello-form");
  const input = document.getElementById("hello-name");
  const result = document.getElementById("hello-result");
  if (!form || !input || !result) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    result.className = "result";
    result.textContent = "Cargando...";

    const params = new URLSearchParams();
    if (input.value.trim()) {
      params.set("name", input.value.trim());
    }

    try {
      const response = await fetch(`/api/v1/hello?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      result.className = "result success";
      result.textContent = data.message;
    } catch (error) {
      result.className = "result error";
      result.textContent = `Error al llamar al API: ${error}`;
    }
  });
}

function init() {
  runPipelineLoop();
  pollHealth();
  setInterval(pollHealth, 5000);
  setupHelloForm();
}

init();
